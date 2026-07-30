from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv


import os

load_dotenv()

root = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")


db = SQLAlchemy()

def connect_db(app):
    service_uri = f"mysql+pymysql://avnadmin:{password}@{root}:11680/library_db"
    app.config['SQLALCHEMY_DATABASE_URI'] = service_uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    with app.app_context():
        try:
            db.engine.connect()
            db.create_all()
            print("Data Base Connect Successfuly!")
            print("Table Created Successfuly!")
        except Exception as err:
            print(f"Data Base Connection Error! : {err}")

