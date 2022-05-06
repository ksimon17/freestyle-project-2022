from flask import Blueprint, render_template, flash, redirect, current_app, session, request #, jsonify

from web_app.routes.wrappers import authenticated_route

from app.recipe_generator_new import display_name
from app.email_service import send_email


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
        #grocery = service.create_grocery(user_email=current_user["email"], recipe_info=recipe_info)
        grocery = service.create_firebase_document(user_email=current_user["email"], recipe_info=recipe_info, type="groceries")
        if not grocery:
            flash(f"You've already added this recipe to your grocery list!", "warning")
        else:
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
    # groceries = service.fetch_user_groceries(current_user["email"])
    groceries = service.fetch_user_items(current_user["email"], type="groceries")

    # print(groceries)

    # print(type(groceries))


    list_of_groceries = []
    for grocery in groceries:
        #print(grocery["recipe_info"]["name"])
        name = grocery["recipe_info"]["name"]
        info = display_name(name)
        list_of_groceries.append(info)
    
    # print(list_of_groceries)


    return render_template("groceries.html",list_of_groceries=list_of_groceries)

@grocery_routes.route("/groceries/recipe",methods=["POST"])
def recipe():
    print("/groceries/recipe")

    form_data = dict(request.form)
    grocery_name = form_data["grocery_name"]
    recipe = display_name(grocery_name)

    return render_template("grocery_recipe.html",recipe=recipe)

@grocery_routes.route("/groceries/email",methods=["POST"])
@authenticated_route
def email():
    print("/groceries/email")

    current_user = session.get("current_user")
    service = current_app.config["FIREBASE_SERVICE"]
    # groceries = service.fetch_user_groceries(current_user["email"])
    groceries = service.fetch_user_items(current_user["email"], type="groceries")
    
    # develop list of dictionaries containing the name and ingredients of each recipe in a user's grocery list
    groceries_list = []
    for recipe in groceries:
        recipe_name = recipe["recipe_info"]["name"]
        recipe = display_name(recipe_name)
        ingredients = recipe["ingredients"]
        ingredient_list = []
        for ingredient in ingredients: 
            ingredient_list.append(f"{ingredient['name']} ({ingredient['measure']})")
        
        grocery = {
            "name": recipe_name.strip(),
            "ingredients": ingredient_list
        }
        groceries_list.append(grocery)

   # print(groceries_list)


    # Creating the email of the user's grocery list 
    

    # Creating the subject of the email    
    subject = "Grocery List Reminder - Recipe Generator App"

     #creating HTML body of hte email
    html = ""
    html += f"<h2><strong>Grocery List Reminder!</strong></h2>"
    html += "<hr>"
    html += "<br>"
    html += f"<p>Hello! Here is the grocery list provided by the Recipe Generator App. Please find the ingredients for your groceries below!</p>"
    html += "<br>"
    
    # Iterating through each recipe in the grocery and display their name, ingredients, and accompanying measures
    for grocery in groceries_list:
        html += f"<h2><strong> {grocery['name']}</strong> </h2>"
        html += "<br>"
        html += "<h><strong>Ingredients</strong></h>"
        html += "<ul>"
        for ingredient in recipe["ingredients"]:
            html += f"<li>{ingredient['name']} ({ingredient['measure']})</li>" 
        html += "</ul>"
        html += "<br>"
        html += "<hr>"

    # Send the email to the user 
    send_email(subject, html, current_user["email"])

    return redirect("/home")
