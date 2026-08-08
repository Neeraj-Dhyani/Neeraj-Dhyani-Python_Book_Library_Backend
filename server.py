from flask import Flask, send_from_directory, render_template
from flask_cors import CORS
from dataBase import connect_db
from services.user_service import user_db
from services.books_services import book_db
from router.template_router import template
from services.admin_auth import admin_db

import os

version = "v1"
app = Flask(__name__, static_folder='static')

CORS(app, origins=["http://localhost:5173", "https://netlibrary.web-craft.in", "https://library-frontend-react.vercel.app"])

connect_db(app)
# print(app.static_folder)
# print(os.path.exists(os.path.join(app.static_folder, "favicon.ico")))
@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        app.static_folder,
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon"
    )
@app.route("/")
def server():
    return send_from_directory(app.static_folder, "index.html")
    # return f"""
    # <!DOCTYPE html>
    # <html>
    # <head>
    #     <title>Library API</title>
    #     <link rel="icon" type="image/x-icon" href="/favicon.ico">
    # </head>
    # <body>
    #     <h1>Server health ok!</h1>
    # </body>
    # </html>
    # """
    

app.register_blueprint(user_db, url_prefix=f"/api/{version}/users")
app.register_blueprint(book_db, url_prefix=f"/api/{version}/books")
app.register_blueprint(admin_db, url_prefix=f"/api/{version}/admin")
app.register_blueprint(template)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

