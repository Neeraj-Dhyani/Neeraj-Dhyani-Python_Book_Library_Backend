# 📁 Project Structure

```
library_backend/
│
├── helper/
│   └── service.py
│
├── middleware/
│   └── auth_middleware.py
│
├── models/
│   ├── admin.py
│   ├── book.py
│   └── user.py
│
├── router/
│   └── template_router.py
│
├── services/
│   ├── admin_auth.py
│   ├── books_services.py
│   └── user_service.py
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── templates/
│   ├── index.j2
│   ├── login.j2
│   ├── upload.j2
│   └── all_books.j2
│
├── Book_PDF/
│   ├── Books/
│   └── Thumbnails/
│
├── dataBase.py          # Database configuration
├── server.py            # Flask application entry point
├── requirements.txt
├── .env
└── README.md
```

---

# ⚙️ Configuration

Create a `.env` file in the project root.

```env
DB_USER=your_aiven_host
DB_PASSWORD=your_database_password
SECRET=your_jwt_secret
```

Example:

```env
DB_USER=mysql-xxxx.aivencloud.com
DB_PASSWORD=your_password
SECRET=mysecretkey
```

---

# 🗄️ Database Configuration (`dataBase.py`)

```python
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

root = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")

db = SQLAlchemy()

def connect_db(app):
    service_uri = (
        f"mysql+pymysql://avnadmin:{password}@{root}:11680/library_db"
    )

    app.config["SQLALCHEMY_DATABASE_URI"] = service_uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    with app.app_context():
        try:
            db.engine.connect()
            db.create_all()

            print("Data Base Connected Successfully!")
            print("Tables Created Successfully!")

        except Exception as err:
            print(f"Database Connection Error: {err}")
```

---

# 🚀 Application Entry Point (`server.py`)

```python
from flask import Flask

from dataBase import connect_db
from services.user_service import user_db
from services.books_services import book_db
from services.admin_auth import admin_db
from router.template_router import template

app = Flask(__name__)

connect_db(app)

@app.route("/")
def server():
    return "<h1>Server Health OK!</h1>"

app.register_blueprint(user_db)
app.register_blueprint(book_db)
app.register_blueprint(admin_db)
app.register_blueprint(template)

if __name__ == "__main__":
    app.run(debug=True)
```

---

# ▶️ Run the Project

Install dependencies

```bash
pip install -r requirements.txt
```

Start the Flask server

```bash
python server.py
```

or

```bash
flask run
```

The application will be available at:

```
http://localhost:5000
```