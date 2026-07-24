from flask import request, jsonify
import os
from jwt import ExpiredSignatureError, InvalidTokenError
import jwt

def authenticate():
        header = request.headers.get("Authorization")
        if not header:
            return {"message":"No heardes!"}
        
        token = header.replace("Bearer ", "")
        try:
            data = jwt.decode(token, os.getenv("SECRET"), algorithms="HS256")
            
        except ExpiredSignatureError:
            return {"message": 'Token Expir!'}
        except InvalidTokenError:
            return {"message":"Invalid Token!"}
        
        return {"user":data["id"]}

def cookie_auth():
    token = request.cookies.get("token")
    if not token :
        return {"message":"Your Not Login!"}
    try:
        data = jwt.decode(token, os.getenv("SECRET"), algorithms="HS256")
    except ExpiredSignatureError:
            return {"message": 'Token Expir!'}
    except InvalidTokenError:
            return {"message":"Invalid Token!"}
    
    return {"user":data["id"]}
          