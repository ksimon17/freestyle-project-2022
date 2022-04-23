# web_app/routes/recipe_routes.py

from flask import Blueprint, request, render_template

from pprint import pprint

from app.recipe_generator_new import display_category, display_area, display_name, display_random

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
    print(method)
    print(selection)

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

    recipes = display_name(selection)
    pprint(recipes)

    # if method == "By Category":
    #     recipes = display_category(selection)
    # elif method == "By Nationality/Country of Origin":
    #     recipes = display_area(selection)
    # elif method == "By Keyword":
    #     recipes = display_name(selection)
    # elif method == "Random Selection":
    #     recipes = display_random()
    
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