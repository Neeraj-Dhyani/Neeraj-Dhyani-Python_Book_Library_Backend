from flask import Blueprint, render_template, jsonify
from middleware.admin_auth import cookie_auth
from models.book import Book
template = Blueprint('template', __name__)

@template.route("/login_page", methods=["GET"])
def login_page():
    return render_template("login.j2")

@template.route('/upload', methods=["GET"])
def upload_render():
    token = cookie_auth()
    if token.get("message"):
        return token["message"]
    return render_template("/upload.j2")

@template.route("/all_books", methods=["GET"])
def all_books():
   try:
        token = cookie_auth()
        if token.get("message"):
            return token["message"]
    
        data = Book.get_books()
        return render_template("/all_books.j2", books=data)
   except Exception as err:
       return jsonify({"status":500, "message":"Somthing Went Wrong!", "error":f"{err}"})

@template.route('/home', methods=['GET'])
def home():
   try:
        token = cookie_auth()
        if token.get("message"):
            return token["message"]
    
        return render_template("/index.j2")
   except Exception as err:
       return jsonify({"status":500, "message":"Somthing Went Wrong!", "error":f"{err}"})

