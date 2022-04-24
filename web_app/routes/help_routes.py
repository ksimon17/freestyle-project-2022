# web_app/routes/help_routes.py

from flask import Blueprint, request, render_template
from app.recipe_generator_new import fetch_nationalities, fetch_categories

help_routes = Blueprint("help_routes", __name__)



# /home routes
@help_routes.route("/")
@help_routes.route("/help")
def index():
    print("HELP...")

    nationalities = fetch_nationalities()
    print("Nationalities:", nationalities)
    categories = fetch_categories()
    print("Categories: ",categories)

    return render_template("help.html",nationalities=nationalities, categories=categories)