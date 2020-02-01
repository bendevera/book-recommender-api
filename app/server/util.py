# app/server/util.py

# from sklearn.neighbors import NearestNeighbors
# import pandas as pd 
# import numpy as np 
from app.server.models import Book, Recommendation
# import os 
# import pickle 

# lib_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib/')

# need to load r_pivot 
# r_pivot = pd.read_csv(lib_path+"r_pivot.csv", index_col=0)
# print("r_pivot loaded")
# book_ids = r_pivot.index
# need to load corr
# corr = pd.read_csv(lib_path+"corr.csv", index_col=0).values
# print("corr loaded")
# need to load model 
# model = NearestNeighbors()
# model = pickle.load(open(lib_path+"nearest.pkl", 'rb'))
# print("model loaded")

def get_popularity_recommendations():
    recommendations = Book.query.order_by(Book.avg_rating.desc()).limit(10)
    recommendations = [book.tojson() for book in recommendations]
    return recommendations

def get_nearest_recommendations(book_id):
    # query_index = book_id-1
    # distances, indices = model.kneighbors(r_pivot.iloc[query_index, :].values.reshape(1, -1),
    #                                      n_neighbors=6)

    # recommendations = []
    # for i in range(1, len(distances.flatten())):
    #     curr_book_id = r_pivot.index[indices.flatten()[i]]
    #     curr_book = Book.query.filter_by(book_id=curr_book_id).first()
    #     if curr_book:
    #         curr_book = curr_book.tojson()
    #         curr_book['distance'] = float(distances.flatten()[i])
    #         recommendations.append(curr_book)
    #     else:
    #         print(f"Couldn't find book id: {curr_book_id}")
    recommendations = Recommendation.query.filter_by(parent_book_id=book_id, type="nearest").all()
    recommendations = [book.tojson() for book in recommendations]
    return recommendations

def get_matrix_recommendations(book_id):
    # curr_corr = corr[book_id]
    # threshold = .9
    # recommendation_ids = list(book_ids[(curr_corr<1.0)&(curr_corr>threshold)])
    # recommendations = []
    # while len(recommendation_ids) == 0 and threshold > .1:
    #     threshold -= .05
    #     recommendation_ids = list(book_ids[(curr_corr<1.0)&(curr_corr>threshold)])
    # for idx in recommendation_ids:
    #     curr_book = Book.query.filter_by(book_id=idx).first()
    #     if curr_book:
    #         recommendations.append(curr_book.tojson())
    #     else:
    #         print(f"Couldn't find {idx}")
    recommendations = Recommendation.query.filter_by(parent_book_id=book_id, type="matrix").all()
    recommendations = [book.tojson() for book in recommendations]
    return recommendations