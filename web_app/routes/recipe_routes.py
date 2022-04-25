# web_app/routes/recipe_routes.py

from flask import Blueprint, request, render_template

from pprint import pprint

from app.recipe_generator_new import display_category, display_area, display_name, display_random, display_ingredient
from app.email_service import send_email

recipe_routes = Blueprint("recipe_routes", __name__)

@recipe_routes.route("/")
@recipe_routes.route("/recipes")
def index():
    print("Recipe...")
    return render_template("recipes.html")

# @recipe_routes.route("/recipes/list", methods=["GET", "POST"])
@recipe_routes.route("/recipes/list", methods=["GET","POST"])
def recipe_list():
    print("Recipe List...")

    form_data = dict(request.form)
    print(form_data)

    method = form_data["method"]
    selection = form_data["selection"]
    email = form_data["email"]
    print(method)
    print(selection)
    print(email)

    # recipes= [{'name':'apple',
    #            'picture': 'url',
    #            'ingredients':
    #                 [{'measure': '12 oz', 'name': 'Whiskey'},
    #                 {'measure': '12 oz', 'name': 'Beer'},
    #                 {'measure': '12 oz frozen', 'name': 'Lemonade'},
    #                 {'measure': '1 cup crushed', 'name': 'Ice'}],
    #             'instructions': 'paragraph of instructions',
    #             'video_link' : 'url'},
    #            {'name':'pasta',
    #            'picture': 'url',
    #            'ingredients':
    #                 [{'measure': '12 oz', 'name': 'Whiskey'},
    #                 {'measure': '12 oz', 'name': 'Beer'},
    #                 {'measure': '12 oz frozen', 'name': 'Lemonade'},
    #                 {'measure': '1 cup crushed', 'name': 'Ice'}],
    #             'instructions': 'paragraph of instructions',
    #             'video_link' : 'url'}
    #          ]

    #recipes = display_name(selection)

    if method == "By Category":
        recipes = display_category(selection)
    elif method == "By Nationality/Country of Origin":
        recipes = display_area(selection)
    elif method == "By Ingredient":
        recipes = display_ingredient(selection)
    elif method == "Random Selection":
        recipes = display_random()
    #pprint(recipes)

    if email:
        subject = "Custom Recipe List - Recipe Generator App Search"
        
        recipe_list = ""
        for recipe in recipes:
            name = recipe["name"]
            recipe_list += f"<li>Name: {name}</li>"

        print(recipe_list)
        # html = f"""
        # <html>
        # <head></head>
        # <body>
        #     <p>Thank you for using the Recipe Generator.<br>
        #     Here is your individual recipe based on your search:<br>
        #     <br>
        #     <br>
        #     <h1>{recipes}</h1>
        #     <br>
        #     </p>
        # </body>
        # </html>
        # """
        
        html = ""
        html += f"<h>Recipe Generator Search Results</h>"
        html += "<br>"
        html += f"<p>Here is you individual recipe list based on your search: .</p>"
        html += "<br>"
        # html += "<ul>"
        
        for recipe in recipes:
            html += f"<h> {recipe['name']} </h>"
            html += "<br>"
            html += "<br>"
            html += f"<img src={recipe['picture_url']} alt='Picture' width='400' height= '233' >"
            html += "<ul>"
            html += "<li>Ingredients</li>"
            html += "<ul>"
            for ingredient in recipe["ingredients"]:
                html += f"<li>{ingredient['name']} ({ingredient['measure']})</li>" 
            html += "</ul>"
            html += f"<li>Instructions: {recipe['instructions']} </li>"
            html += f"<li>Video URL: {recipe['video_url']}</li>"
            html += "</ul>"
            html += "<br>"
            html += "<hr>"
        # html += "</ul>"

        send_email(subject, html)


    return render_template("recipes_list.html", recipes=recipes)
   
#     if request.method == "GET":
#         print("URL PARAMS:", dict(request.args))
#         request_data = dict(request.args)
#     elif request.method == "POST": # the form will send a POST
#         print("FORM DATA:", dict(request.form))
#         request_data = dict(request.form)
         
#     country_code = request_data.get("country_code") or "US"
#     zip_code = request_data.get("zip_code") or "20057"

#     results = get_hourly_forecasts(country_code=country_code, zip_code=zip_code)
#     if results:
#         flash("Weather Forecast Generated Successfully!", "success")
#         return render_template("weather_forecast.html", country_code=country_code, zip_code=zip_code, results=results)
#     else:
#         flash("Geography Error. Please try again!", "danger")
#         return redirect("/weather/form")