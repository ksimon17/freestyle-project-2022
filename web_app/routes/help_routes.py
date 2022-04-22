# web_app/routes/help_routes.py

from flask import Blueprint, request, render_template

help_routes = Blueprint("help_routes", __name__)

# /home routes
@help_routes.route("/")
@help_routes.route("/help")
def index():
    print("HELP...")
    return render_template("help.html")