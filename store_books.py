from app.server import db 
from app.server.models import Book 
import pandas as pd 

books = pd.read_csv('./data/books.csv')

def add_to_db(cell):
    pub_year = cell['original_publication_year']
    if type(pub_year) is not int:
        pub_year = None
    curr_book = Book(
                    title=cell['title'], 
                    book_id=cell['book_id'], 
                    org_title=cell['original_title'],
                    authors=cell['authors'],
                    pub_year=pub_year,
                    avg_rating=cell['average_rating'],
                    img_url=cell['image_url'],
                    small_img_url=cell['small_image_url']
                    )
    db.session.add(curr_book)
    db.session.commit()

Book.query.delete()
books.apply(add_to_db, axis=1)
all_books = Book.query.all()
print(f"Num books: {len(all_books)}")