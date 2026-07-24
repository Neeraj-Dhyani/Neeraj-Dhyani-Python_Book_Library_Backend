from models.book import Book
from flask import Blueprint, jsonify, request, send_from_directory
from middleware.auth_middleware import authenticate
import os


book_db = Blueprint("books", __name__)
base_dir = os.getcwd()


@book_db.route('/upload_book', methods=["POST"])
def uplaod_file():
    book_name = request.form.get('book_name')
    book_pdf = request.files.get('book')
    try:
        res = Book.add_file(book_pdf, base_dir)
        if res.get("message"):
            return jsonify({"message":res["message"]}), 400

        book = Book(bookname=book_name, 
                         bookpdf=res["book_url"], 
                         thumbnail=res["thumbnail_url"])
        
        res = book.creat()
        return jsonify(res["message"]),201

    except Exception as err:
        return jsonify({"statu":500, "message":"Somthing Went Wrong!", "error":f"{err}"})
    
@book_db.route("/media/book/<filename>")
def get_book(filename):
    return send_from_directory(os.path.join(base_dir, "Book_PDF", "Books"), filename)

@book_db.route("/media/thumbnail/<filename>")
def get_thumbnail(filename):
    return send_from_directory(os.path.join(base_dir, "Book_PDF", "Thumbnails"), filename)
