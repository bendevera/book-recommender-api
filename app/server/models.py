# app/server/models.py

from app.server import app, db

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_id = db.Column(db.Integer)
    title = db.Column(db.String)
    org_title = db.Column(db.String)
    authors = db.Column(db.String)
    pub_year = db.Column(db.Integer)
    avg_rating = db.Column(db.Float)
    img_url = db.Column(db.String)
    small_img_url = db.Column(db.String)
    recommendations = db.relationship("Recommendation", backref="book")

    def tojson(self):
        return {
            "id": self.id,
            "book_id": self.book_id,
            "title": self.title,
            "author": self.authors,
            "pub_year": self.pub_year,
            "avg_rating": self.avg_rating,
            "img_url": self.img_url
        }

class Recommendation(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recommendation_id = db.Column(db.Integer)
    type = db.Column(db.String)
    rank = db.Column(db.Float)
    parent_book_id = db.Column(db.Integer, db.ForeignKey('book.id'))

    def tojson(self):
        rec_book = Book.query.filter_by(book_id=self.recommendation_id).first()
        return {
            "id": self.id,
            "parent_book_id": self.parent_book_id,
            "title": rec_book.title,
            "author": rec_book.authors,
            "pub_year": rec_book.pub_year,
            "avg_rating": rec_book.avg_rating,
            "img_url": rec_book.img_url,
            "rank": self.rank,
            "type": self.type
        }

