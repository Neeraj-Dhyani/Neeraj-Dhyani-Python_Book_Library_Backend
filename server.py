from flask import Flask
from dataBase import connect_db
from services.user_service import user_db
from services.books_services import book_db
from router.template_router import template
from services.admin_auth import admin_db
import os

version = "v1"
app = Flask(__name__)

connect_db(app)

@app.route("/")
def server():
    return f"<h1>server health ok!</h1>"

app.register_blueprint(user_db, url_prefix=f"/api/{version}/users")
app.register_blueprint(book_db, url_prefix=f"/api/{version}/books")
app.register_blueprint(admin_db, url_prefix=f"/api/{version}/admin")
app.register_blueprint(template)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

