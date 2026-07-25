from models.admin import Admin
from flask import Blueprint, jsonify, request, make_response, redirect, url_for
from werkzeug.security import generate_password_hash
from dataBase import db
from middleware.admin_auth import authenticate
from router.template_router import template
import jwt 
import os

admin_db = Blueprint('admin', __name__)


@admin_db.route("/admin", methods=["POST"])
def creat_admin():
    if db.session.execute(db.select(Admin)).scalar():
        return jsonify({"message":"Admin Already Created!"})
    
    try:
        data = request.get_json()
        if(not data["name"] or not data["email"] or not data["password"]):
            return jsonify({"message":"Pleas fill Require data"}) ,401
        
        hash_pass = generate_password_hash(data["password"])
        
        admin = Admin(admin_name=data["name"], email=data["email"], password=hash_pass)

        admin.creat()
        
        return jsonify(admin)
    except Exception as err:
        return jsonify({"statu":500, "message":"Somthing Went Wrong!", "error":f"{err}"})
    
@admin_db.route("/admin_login", methods=["POST"])
def admin_login():
    try:
        data = request.get_json(silent=True) or request.form

        print(request.content_type)
        print(request.get_json(silent=True))
        print(request.form)

        if(not data.get("email") or not data.get("password")):
            return jsonify({"message":"Please fill Require data"}) ,401
        
        email, password = data.get("email"), data.get("password")

        is_user = Admin.admin_login(email, password)
        if is_user["valid"]:
            token = jwt.encode({"id":is_user["id"]}, os.getenv("SECRET"), algorithm="HS256")
            #  make_response(jsonify({"status":200,"messages":"Login Successfully!"}))
            res = redirect (url_for("template.all_books"))
            res.set_cookie('token', token, 86400, httponly=True)

            return res
        else:
            return jsonify({"status":401, "message":f"{is_user["message"]}"})
    except Exception as err:
        return jsonify({"statu":500, "message":"Somthing Went Wrong!", "error":f"{err}"})

@admin_db.route("/admin_logout", methods=["GET"])
def admin_logout():
    try:
        # make_response(jsonify({'message':"Your are Successfully Logout!"}))
        res = redirect(url_for("template.login_page"))
        res.delete_cookie("token")
        return res
    except Exception as err:
        return jsonify({"statu":500, "message":"Somthing Went Wrong!", "error":f"{err}"})