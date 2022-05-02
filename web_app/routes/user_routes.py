
from flask import Blueprint, render_template, flash, redirect, current_app, url_for, session, request #, jsonify

from web_app.routes.wrappers import authenticated_route

user_routes = Blueprint("user_routes", __name__)

#
# USER ORDERS
#


@user_routes.route("/user/recipes/create", methods=["POST"])
@authenticated_route
def create_order():
    print("CREATE USER RECIPES...")

    form_data = dict(request.form)
    # print("FORM DATA:", form_data)
    # print("name:",form_data["recipe_name"])
    # print("picture_url:", form_data["picture_url"])
    # print("area:", form_data["area"])
    # print("category:", form_data["category"])
    recipe_info = {
        "name": form_data["recipe_name"],
        "picture_url": form_data["picture_url"],
        "area": form_data["area"],
        "category": form_data["category"]
    }

    #return redirect("/")
    current_user = session.get("current_user")

    service = current_app.config["FIREBASE_SERVICE"]



    try:
        result = service.create_recipe(user_email=current_user["email"], recipe_info=recipe_info)
        if not result:
            flash(f"You've already added this recipe to your list!", "warning")
        else:
            flash(f"Recipe Added!", "success")
        return redirect("/list")
    except Exception as err:
        print(err)
        flash(f"Oops, something went wrong: {err}", "warning")
        return redirect("/home")
