from dataBase import db
from uuid import uuid4
import datetime
from werkzeug.security import check_password_hash

class Admin(db.Model):
    __tablename__ = "admin_data"

    id = db.Column(db.String(36), primary_key=True, default=lambda:str(uuid4()))
    admin_name = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(150), unique=True, nullable=True)
    password = db.Column(db.String(300), nullable=True)
    created_at = db.Column(db.String(300), default=datetime.datetime.now)


    def __init__(self, admin_name, email, password):
        self.admin_name = admin_name
        self.email = email
        self.password = password

    def to_dict(self):
       return {
        "name": self.admin_name,
        "email": self.email
        }
    
    def is_user(self):
        return db.session.query(Admin).filter(Admin.email == self.email).first() is not None
    
    def admin_login(email, password):
        admin = db.session.query(Admin).filter(Admin.email == email).first()

        if not admin:
           return {"valid":False, "message":"Your Email is Wrong!"}
   
        is_valid = check_password_hash(admin.password, password)

        if is_valid:
            return {"valid":True, "id": admin.id}
        else:
            return {"valid":False, "message":" Your Password is Wrong!"}

    def creat(self):
        db.session.add(self)
        db.session.commit()
        return{"message":"Admin Created Successfully!"}
    
    def delete(id):
        db.session.query(Admin).filter(Admin.id == id)
        db.session.commit()
        return{"message":"Admin Delete Successfully!"}
        
