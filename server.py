from flask import Flask
from dataBase import connect_db
from services.user_service import user_db
from services.books_services import book_db
from router.template_router import template
from services.admin_auth import admin_db



app = Flask(__name__)

connect_db(app)

@app.route("/")
def server():
    return f"<h1>server health ok!</h1>"

app.register_blueprint(user_db)
app.register_blueprint(book_db)
app.register_blueprint(admin_db)
app.register_blueprint(template)

if __name__ == "__main__":
    app.run(debug=True)

