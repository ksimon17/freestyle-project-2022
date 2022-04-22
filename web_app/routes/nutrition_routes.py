# web_app/routes/nutrition_routes.py

from flask import Blueprint, request, render_template

nutrition_routes = Blueprint("nutrition_routes", __name__)

@nutrition_routes.route("/")
@nutrition_routes.route("/nutrition")
def index():
    print("Nutrition...")
    return render_template("nutrition.html")