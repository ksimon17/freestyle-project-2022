# web_app/routes/list_routes

from flask import Blueprint, request, render_template

list_routes = Blueprint("list_routes", __name__)

@list_routes.route("/")
@list_routes.route("/list")
def index():
    print("List...")
    return render_template("list.html")