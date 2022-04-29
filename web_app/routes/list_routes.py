# web_app/routes/list_routes

from flask import Blueprint, render_template, flash, redirect, current_app, url_for, session, request

from web_app.routes.wrappers import authenticated_route

list_routes = Blueprint("list_routes", __name__)

@list_routes.route("/")
@list_routes.route("/list")
@authenticated_route
def orders():
    print("List...")

    print("USER ORDERS...")
    current_user = session.get("current_user")
    service = current_app.config["FIREBASE_SERVICE"]
    recipes = service.fetch_user_recipes(current_user["email"])

    print("orders:", recipes)

    return render_template("list.html",recipes=recipes)