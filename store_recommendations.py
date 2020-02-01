import pandas as pd 
import numpy as np 
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
from sklearn.decomposition import TruncatedSVD
import pickle 
import sys 
from app.server import db
from app.server.models import Book, Recommendation

'''
Need to save:
- r_pivot
- corr
'''

# avoid warnings
import warnings 
warnings.filterwarnings('ignore', category=RuntimeWarning)

DATA_PATH = './data/'
ratings = pd.read_csv( DATA_PATH + 'ratings.csv' )
books = pd.read_csv( DATA_PATH + 'books.csv' )
print(f"# ratings: {ratings.shape[0]}")
print(f"# books: {books.shape[0]}")

# making pivot table with user_id as index and book_id as the columns
r_pivot = ratings.pivot(index="user_id", columns="book_id", values="rating")
# filling NaNs with 0
r_pivot = r_pivot.fillna(0)
# transposing pivot table to have book_id as index
r_pivot = r_pivot.T

# lib_path = './app/server/lib/'
# r_pivot.to_csv(lib_path+'r_pivot.csv', index=True)
book_ids = r_pivot.index

# ---------- nearest function -----------------
def get_nearest_recommendations(book_id):
    global r_pivot 
    global model 
    query_index = book_id-1
    distances, indices = model.kneighbors(r_pivot.iloc[query_index, :].values.reshape(1, -1),
                                         n_neighbors=6)

    recommendations = []
    for i in range(1, len(distances.flatten())):
        curr_book_id = r_pivot.index[indices.flatten()[i]]
        curr_distance = float(distances.flatten()[i])
        curr_book = {
            "id": int(curr_book_id),
            "distance": float(curr_distance)
        }
        # curr_book = Book.query.filter_by(book_id=curr_book_id).first()
        # if curr_book:
        #     curr_book = curr_book.tojson()
        #     curr_book['distance'] = float(distances.flatten()[i])
        #     recommendations.append(curr_book)
        # else:
        #     print(f"Couldn't find book id: {curr_book_id}")
        recommendations.append(curr_book)
    return recommendations

def build_nearest_neighbors():
    global model 
    print("Building Nearest Neighbors")
    # making ratings matrix
    ratings_matrix = csr_matrix(r_pivot.values)
    # instantiating model 
    model = NearestNeighbors(metric="cosine", algorithm="brute")
    # fitting model to rating_matrix
    model.fit(ratings_matrix)

    # nearest_path = lib_path+'nearest.pkl'
    # with open(nearest_path, 'wb') as f:
    #     pickle.dump(model, f)
    # print("NN built and saved.")
    for book_id in list(book_ids):
        curr_book = Book.query.filter_by(book_id=book_id).first()
        if curr_book:
            recommendations = get_nearest_recommendations(book_id)
            for recommendation in recommendations:
                curr_recommendation = Recommendation(
                    parent_book_id=curr_book.id, 
                    recommendation_id=recommendation['id'], 
                    rank=recommendation['distance'],
                    type="nearest")
                db.session.add(curr_recommendation)
                db.session.commit()
        else:
            print(f"Can't find {book_id}")

# ---------- matrix function -----------------
def get_matrix_recommendations(book_id):
    global book_ids
    global corr
    curr_corr = corr[book_id]
    threshold = .9
    recommendation_ids = list(book_ids[(curr_corr<1.0)&(curr_corr>threshold)])
    recommendations = []
    while len(recommendation_ids) == 0 and threshold > .1:
        threshold -= .05
        recommendation_ids = list(book_ids[(curr_corr<1.0)&(curr_corr>threshold)])
    # for idx in recommendation_ids:
        # curr_book = Book.query.filter_by(book_id=idx).first()
        # if curr_book:
        #     recommendations.append(curr_book.tojson())
        # else:
        #     print(f"Couldn't find {idx}")
    return recommendation_ids

def matrix_factorization():
    global corr
    print("Building Matrix Factorization")
    # getting numpy array of the pivot table
    X = r_pivot.values
    # use SVD to reduce dimensiontality of data
    svd = TruncatedSVD(n_components=12, random_state=42)
    matrix = svd.fit_transform(X)
    # getting correlation coef matrix of the data
    # basically each cell represents the relationship between two books
    corr = np.corrcoef(matrix)
    # need to save corr somehow
    corr = pd.DataFrame(corr)
    # I think this should be index=False and then no index_col when reading
    # corr.to_csv(lib_path+'corr.csv', index=True)
    # print("corr.csv created and saved")
    for book_id in list(book_ids):
        curr_book = Book.query.filter_by(book_id=book_id).first()
        if curr_book:
            # have to subtract 1 because book_id starts at 1 and corr index starts at 0
            recommendations = get_matrix_recommendations(book_id-1)
            for recommendation in recommendations:
                curr_recommendation = Recommendation(
                    parent_book_id=curr_book.id, 
                    recommendation_id=recommendation, 
                    type="matrix")
                db.session.add(curr_recommendation)
                db.session.commit()
        else:
            print(f"Can't find {book_id}")
            


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Must have argument nn|mf|both")
    if sys.argv[1] == "nn":
        Recommendation.query.filter_by(type="nearest").delete()
        build_nearest_neighbors()
    elif sys.argv[1] == "mf":
        Recommendation.query.filter_by(type="matrix").delete()
        matrix_factorization()
    elif sys.argv[1] == "both":
        Recommendation.query.delete()
        build_nearest_neighbors()
        matrix_factorization()
    else:
        print("2nd argument must be: nn|mf|both")
    all_recommendations = Recommendation.query.all()
    print(f"# recommendations: {len(all_recommendations)}")