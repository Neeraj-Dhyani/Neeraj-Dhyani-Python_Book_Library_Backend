from models.user import User
from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash
from middleware.auth_middleware import authenticate
import jwt 
import os

user_db = Blueprint("user", __name__)


@user_db.route("/register", methods=["POST"])
def creat_user():
    try:
        data = request.get_json()
        if(not data["fullname"] 
           or not data["email"] 
           or not data["password"] 
           or not data["phone"]
           or not data["address"]
           ):
            return jsonify({"message":"Pleas fill Require data"}) ,401
        # print(data)
        # print(type(data))
        if(User.is_user(data["email"])):
            return  {"status":400, "message":"User Already Exit!"}
    
        hashPassoword = generate_password_hash(data["password"])
        print(hashPassoword)
        user = User(
                    fullname=data["fullname"], 
                    email=data["email"],
                    password=hashPassoword,  
                    phone=data["phone"], 
                    address=data["address"],
                    books=data.get('books', [])
                    )
        user.create()

        return jsonify({"status":200, "message":"User Created Successfully!"})
    
    except Exception as err:

        return jsonify({"statu":500, "message":"Somthing Went Wrong!", "error":f"{err}"})


    
@user_db.route("/login", methods=["POST"])
def user_login():
    try:
        data = request.get_json()
        email, password = data["email"], data["password"]

        is_user = User.user_login(email, password)

        if is_user["valid"]:
            token = jwt.encode({"id":is_user["id"]}, os.getenv("SECRET"), algorithm="HS256")
            return jsonify({"status":200, "message":"Login Successfuly!", "token":token})
        else:
            return jsonify({"status":401, "message":f"{is_user["message"]}"})

        
    except Exception as err:
        return jsonify({"status":500, "message":"Somthing Went Wrong!", "error":f"{err}"})
  

@user_db.route("/get_user", methods=["GET"])
def user():
    data = authenticate()
    if data.get("message"):
        return jsonify({"status":401, "message":data["message"]})
    
    try:
        data = User.get_user_by_id(data["user"])

        if not data:
            return jsonify({"status":404, "message":"User Not Found!"})
        
        return jsonify({"statu":200, "user":data["user"].to_dict()})
    
    except Exception as err:
        return jsonify({"statu":500, "message":"Somthing Went Wrong!", "error":f"{err}"})

@user_db.route("/user_update", methods=["PUT"])
def update_user():
    data = authenticate()
    if data.get("message"):
        return jsonify({"status":401, "message":data["message"]})
    try:
        body_data = request.get_json()
        fullname, email, phone, address = body_data["fullname"], body_data["email"], body_data["phone"], body_data["address"]
        # print(fullname, email, phone, address)
        # print(data)
        update = User.update_user(data["user"], fullname, phone, email, address)
        # print("user update : ",update)
        if update.get("error"):
            return jsonify({"stuts":400, "message":update["error"]})
        return jsonify({"status":200, "update_user":update["user"].to_dict(), "message":update["message"]})
    except Exception as err:
        return jsonify({"statu":500, "message":"Somthing Went Wrong!", "error":f"{err}"})

@user_db.route("/user_delete", methods=["DELETE"])
def user_delete():
    data = authenticate
    if data.get("message"):
        return jsonify({"status":401, "message":data["message"]})
    try:
        data_user = User.delete_user(data["user"])
        return{"status":200, "message":data_user["message"]}
    except Exception as err:
        return jsonify({"statu":500, "message":"Somthing Went Wrong!", "error":f"{err}"})

             


    