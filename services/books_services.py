from models.book import Book
from flask import Blueprint, jsonify, request, send_from_directory
from middleware.admin_auth import cookie_auth
import os


book_db = Blueprint("books", __name__)
base_dir = os.getcwd()


@book_db.route('/upload_book', methods=["POST"])
def uplaod_file():
    token = cookie_auth()
    if token.get("message"):
        return token["message"]
    
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

@book_db.route("/books_data", methods=["GET"])
def all_books():
    token = cookie_auth()
    if token.get("message"):
        return token["message"]
    try:
        data = Book.get_books()
        return jsonify({"books":[book.to_dict() for book in data]}), 200
    except Exception as err:
        return jsonify({"statu":500, "message":"Somthing Went Wrong!", "error":f"{err}"})

@book_db.route("/delete_book/<book_id>", methods=["DELETE"])
def delete_books(book_id):
    token = cookie_auth()
    if token.get("message"):
        return token["message"]
    try:
        res = Book.delete_book_by_id(book_id)
        return jsonify({res}), 200
    except Exception as err:
        return jsonify({"statu":500, "message":"Somthing Went Wrong!", "error":f"{err}"})

@book_db.route("/media/book/<filename>")
def get_book(filename):
   
    return send_from_directory(os.path.join(base_dir, "Book_PDF", "Books"), filename)

@book_db.route("/media/thumbnail/<filename>")
def get_thumbnail(filename):
    return send_from_directory(os.path.join(base_dir, "Book_PDF", "Thumbnails"), filename)
