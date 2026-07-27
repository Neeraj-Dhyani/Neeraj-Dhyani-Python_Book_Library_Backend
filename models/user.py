from dataBase import db
import uuid
from werkzeug.security import check_password_hash
from datetime import datetime, timezone


class User(db.Model):
    __tablename__ = 'user_data'

    id = db.Column(db.String(36), primary_key=True, default=lambda:str(uuid.uuid4()))
    fullname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50),unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    phone =db.Column(db.String(10),nullable=False)
    address = db.Column(db.String(200), nullable=False)
    books = db.Column(db.JSON)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    

    def __init__(self, fullname, email, password, phone, address, books):
        self.fullname = fullname
        self.email = email
        self.password = password
        self.phone = phone
        self.address = address
        self.books = books or []
    
    def to_dict(self):
       return {
        "id": self.id,
        "fullname": self.fullname,
        "email": self.email,
        "phone": self.phone,
        "address": self.address,
        "books": self.books,
        "created_at": self.created_at
        }

    def create(self):
        # new_user = User(self.fullname, self.email, self.password, self.phone, self.address, self.books)
        db.session.add(self)
        db.session.commit()

    def is_user(email):
        return db.session.query(User).filter(User.email == email).first() is not None
        # print(user)
        # if(user):
        #     return True
        # else:
        #     return False

    def user_login(email, password):
        user = db.session.query(User).filter(User.email == email).first()

        if not user:
           return {"valid":False, "message":"Your Email is Wrong!"}
   
        is_valid = check_password_hash(user.password, password)

        if is_valid:
            return {"valid":True, "id": user.id}
        else:
            return {"valid":False, "message":" Your Password is Wrong!"}
    
    def get_user_by_id(id):
        user = db.session.query(User).filter(User.id == id).first()
        if not user:
            return False
        return {"user":user}
    
    def update_user(id, fullname, phone, email, address):
        user = db.session.query(User).filter(User.id == id).first()
        # if(fullname):
        #     user.fullname = fullname
        #     db.session.commit()
        # elif(phone):
        #     user.phone = phone
        #     db.session.commit()
        # elif(email):
        #     user.email = email
        #     db.session.commit()
        # elif(address):
        #     user.address = address
        #     db.session.commit()
        # else:
        #     return{"error":"No Data to be Change!"}

        #return {"user":user, "message":"Your Data Change Successfully!"}

        if(fullname):
            user.fullname = fullname
            db.session.commit()
            return {"user":user, "message":"Name change Successfully!"}
        elif(phone):
            user.phone = phone
            db.session.commit()
            return {"user":user, "message":"Phone Change Successfully!"}
        elif(email):
            user.email = email
            db.session.commit()
            return {"user":user, "message": "Email Change Successfully!"}
        elif(address):
            user.address = address
            db.session.commit()
            return {"user":user, "message":"Address Change Successfully!"}
        else:
            return{"error":"No Data to be Change!"}
        
    def delete_user(id):
        db.session.query(User).filter(User.id == id).delete(synchronize_session=False)
        return {'message':"Successfully Deleted!"}
    

    @staticmethod
    def print_all_user():
        user_data = User.query.all()
        return user_data