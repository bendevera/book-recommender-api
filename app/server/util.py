# app/server/util.py

from app.server.models import Book, Recommendation


def get_popularity_recommendations():
    recommendations = Book.query.order_by(Book.avg_rating.desc()).limit(10)
    recommendations = [book.tojson() for book in recommendations]
    return recommendations

def get_nearest_recommendations(book_id):
    recommendations = Recommendation.query.filter_by(parent_book_id=book_id, type="nearest").all()
    recommendations = [book.tojson() for book in recommendations]
    return recommendations

def get_matrix_recommendations(book_id):
    recommendations = Recommendation.query.filter_by(parent_book_id=book_id, type="matrix").all()
    recommendations = [book.tojson() for book in recommendations]
    return recommendations