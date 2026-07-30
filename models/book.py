from dataBase import db
from helper.service import genrate_random_num
from helper.service import is_folder, generate_thumnail
from werkzeug.utils import secure_filename
import os 
import uuid
import datetime

class Book(db.Model):
    __tablename__ = "books_data"

    id = db.Column(db.String(36), primary_key=True, default=lambda:str(uuid.uuid4()))
    bookname = db.Column(db.String(50), nullable=False)
    bookcode = db.Column(db.String(5), unique=True, default=genrate_random_num, nullable=False)
    thumbnail = db.Column(db.String(300), nullable=False)
    bookpdf = db.Column(db.String(300), nullable=False)
    created_at = db.Column(db.String(500), default=datetime.datetime.now)

    def __init__(self, bookname, bookpdf, thumbnail):
        self.bookname = bookname
        self.bookpdf = bookpdf
        self.thumbnail = thumbnail
    
    def to_dict(self):
        return{
            "id":self.id,
            "bookname":self.bookname,
            "bookcode":self.bookcode,
            "thumbnail":self.thumbnail,
            "bookpdf":self.bookpdf,
            "created_at":self.created_at
        }
    
    def add_file(book, base_dir):
        is_folder()

        if not book:
            return {'message':'Book not Upload!'}
        
        file_name = secure_filename(book.filename)

        book_folder = os.path.join(base_dir, "Book_PDF", "Books")
        thumbnail_folder = os.path.join(base_dir ,"Book_PDF", "Thumbnails")

        os.makedirs(book_folder, exist_ok=True)
        os.makedirs(thumbnail_folder, exist_ok=True)

        pdf_path = os.path.join(book_folder, file_name)
        book.save(pdf_path)

        books_url = f"/media/book/{file_name}"
        thumbnail_url = generate_thumnail(pdf_path, thumbnail_folder)

        return {"book_url":books_url, "thumbnail_url":thumbnail_url}
    
    def get_books():
        all_books = db.session.query(Book).all()
        return all_books

    def delete_book_by_id(id):
        data = db.session.query(Book).filter(Book.id == id).first()
        if not data:
            return{"message":"Book not Found!"}
        pdf_path = f"Book_PDF/{data.bookpdf}"
        thumb_path = f"Book_PDF/{data.thumbnail}"
        if os.path.exists(pdf_path):
            os.remove()
        if os.path.exists(thumb_path):
            os.remove()
        db.session.delete()
        db.session.commit()
        return {"message":"Book Deleted Successfully!"}
    
    def creat(self):
        db.session.add(self)
        db.session.commit()
        return {"message":"Book Created Successfully!"}
    