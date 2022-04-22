# web_app/routes/recipe_routes.py

from flask import Blueprint, request, render_template

recipe_routes = Blueprint("recipe_routes", __name__)

@recipe_routes.route("/")
@recipe_routes.route("/recipes")
def index():
    print("Recipe...")
    return render_template("recipes.html")