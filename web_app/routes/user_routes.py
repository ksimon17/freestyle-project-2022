
from flask import Blueprint, render_template, flash, redirect, current_app, url_for, session, request #, jsonify

from web_app.routes.wrappers import authenticated_route

user_routes = Blueprint("user_routes", __name__)

#
# USER ORDERS
#

@user_routes.route("/user/orders")
@authenticated_route
def orders():
    print("USER RECIPES...")
    current_user = session.get("current_user")
    service = current_app.config["FIREBASE_SERVICE"]
    recipes = service.fetch_user_recipes(current_user["email"])
    return render_template("user_orders.html", recipes=recipes)


@user_routes.route("/user/recipes/create", methods=["POST"])
@authenticated_route
def create_order():
    print("CREATE USER RECIPES...")

    form_data = dict(request.form)
    print("FORM DATA:", form_data)
    print("name:",form_data["recipe_name"])
    print("video_url:", form_data["video_url"])
    print("area:", form_data["area"])
    print("category:", form_data["category"])
    recipe_info = {
        "name": form_data["recipe_name"],
        "video_url": form_data["video_url"],
        "area": form_data["area"],
        "category": form_data["category"]
    }

    #return redirect("/")
    current_user = session.get("current_user")

    service = current_app.config["FIREBASE_SERVICE"]

    try:
        service.create_recipe(user_email=current_user["email"], recipe_info=recipe_info)
        flash(f"Recipe Added!", "success")
        return redirect("/user/orders")
    except Exception as err:
        print(err)
        flash(f"Oops, something went wrong: {err}", "warning")
        return redirect("/products")


#
# USER PROFILE
#

@user_routes.route("/user/profile")
@authenticated_route
def profile():
    print("USER PROFILE...")
    current_user = session.get("current_user")
    #user = fetch_user(email=current_user["email"])
    return render_template("user_profile.html", user=current_user) # user=user