# web_app/routes/login_routes.py

from flask import Blueprint, request, render_template

login_routes = Blueprint("login_routes", __name__)

@login_routes.route("/")
@login_routes.route("/login")
def index():
    print("Login...")
    return render_template("login.html")