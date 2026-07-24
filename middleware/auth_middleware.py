from flask import request, jsonify, g, make_response
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

