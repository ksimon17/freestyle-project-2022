from flask import Blueprint, render_template, flash, redirect, current_app, url_for, session, request #, jsonify

from web_app.routes.wrappers import authenticated_route

from app.recipe_generator_new import display_name

grocery_routes = Blueprint("grocery_routes", __name__)

@grocery_routes.route("/groceries/create", methods=["GET","POST"])
@authenticated_route
def orders():

    form_data = dict(request.form)
    # print(form_data)

    recipe_info = {
        "name": form_data["recipe_name"]
    }
    # print(recipe_info)
    current_user = session.get("current_user")

    service = current_app.config["FIREBASE_SERVICE"]

    try:
        service.create_grocery(user_email=current_user["email"], recipe_info=recipe_info)
        flash(f"Grocery Added!", "success")
        return redirect("/groceries")
    except Exception as err:
        print(err)
        flash(f"Oops, something went wrong: {err}", "warning")
        return redirect("/home")


@grocery_routes.route("/groceries")
@authenticated_route
def groceries():
    current_user = session.get("current_user")
    service = current_app.config["FIREBASE_SERVICE"]
    groceries = service.fetch_user_groceries(current_user["email"])

    # print(groceries)

    # print(type(groceries))


    list_of_groceries = []
    for grocery in groceries:
        print(grocery["recipe_info"]["name"])
        name = grocery["recipe_info"]["name"]
        info = display_name(name)
        list_of_groceries.append(info)
    
    # print(list_of_groceries)


    return render_template("groceries.html",list_of_groceries=list_of_groceries)

