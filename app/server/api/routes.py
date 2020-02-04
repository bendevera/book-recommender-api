# app/server/api/routes.py

from app.server.models import Book
from flask import jsonify, request, Blueprint
from app.server.util import get_popularity_recommendations, get_matrix_recommendations, get_nearest_recommendations

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/')
def index():
    return jsonify({"message": "Welcome to the book recommender API!"}), 200

@api.route('/books')
def books():
    books = Book.query.all()
    books = [book.tojson() for book in books]
    return jsonify({"books": books}), 200

@api.route('/books/<id>')
def books_by_id(id):
    book = Book.query.filter_by(id=id).first()
    if not book:
        return jsonify({"message": "Book not found with id {}".format(id)}), 204
    return jsonify({"book": book.tojson()}), 200

@api.route('/recommend', methods=["POST"])
def recommend():
    params = request.json 
    curr_book_id = params['book_id']
    curr_type = params['type']
    if curr_type == 'popularity':
        recommendations = get_popularity_recommendations()
        return jsonify({"recommendations": recommendations}), 200
    else:
        if curr_book_id:
            # do stuff to get recommendation 
            if curr_type == "nearest":
                recommendations = get_nearest_recommendations(curr_book_id)
            else:
                recommendations = get_matrix_recommendations(curr_book_id)
            reference_book = Book.query.filter_by(book_id=curr_book_id).first()
            if reference_book:
                reference_book = reference_book.tojson()
            return jsonify({"reference": reference_book, "recommendations": recommendations}), 200
        else:
            return jsonify({"message": "Parameter book_id is required."}), 400