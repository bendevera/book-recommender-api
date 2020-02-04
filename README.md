# book-recommender-api
API with 10,000 books (each averaging 50,000 reviews) that given a selected book, recommends books with one of two methods: Nearest Neighbors or Correlation Matrix Factorization. 

prod url: books.bendevera.com

## routes
- `GET /api` - root route with constant response. 

- `GET /api/books` - route to get all books in the database.

- `GET /api/books/<id>`- route to get an individual book by id.

- `POST /api/recommend` - route to get book recommendations.

JSON params: 
  - book_id - int - "reference" book that is used to generate recommendations
  - type - string - nearest/matrix/popularity - method used to generate recommendations
  
## local setup
1. install dependencies `pip install -r requirements.txt`
2. create postgres database
3. set flask app `export FLASK_APP=manage.py`
4. initialize flask db and migrations folder `flask db init`
5. create first migration `flask migrate -m "message"`
6. upgrade db `flask db upgrade`
7. store all books using script in root directory `python store_books.py`
8. store all recommendations (preprocess for speed) `python store_recommendations.py both|mf|nn`
9. run app `flask run`
