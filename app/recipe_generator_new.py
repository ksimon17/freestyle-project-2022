# app/recipe_generator.py

import requests, json, os
from pprint import pprint
from IPython.display import Image, display 

# FUNCTION TO CONVERT API DATA TO A MORE ACCESSIBLE FORMAT - PARAM COMMENT MADE 
def read_data(url):
  """
  This function fetches JSON data from the MealDB API and converts its to a Python Dictionary 
  Params: url, which is a valid URL which leads to JSON data from the MealDB API
  Datatypes of Params: url is a String
  Return: This function returns a dictionary of API data based on the contents within the valid url 

  Invoke the function like this: read_data(url) where url is an appropriate url that will reach Meal DB API Data
  """
  response = requests.get(url)
  data = json.loads(response.text)
  return data

# FUNCTION TO PRINT THE RECIPE'S NAME AND PICTURE - DON'T THINK I USE THIS
def display_name_pics(data):
  print(data["strMeal"])
  display(Image(url=data["strMealThumb"], height=100))

# FUNCTION TO MORE EFFICIENTLY DISPLAY OUTPUT - DON'T THINK I USE THIS
def display_recipe(recipe):
  
  # PRINT LIST OF INGREDIENTS
  print("---------------------")   
  print("List of Ingredients")
  print("---------------------")
  for x in range (1,19):
      #define variables
      ingredientString = f'strIngredient{x}'
      measureString = f'strMeasure{x}'
      ingredient = recipe["meals"][0][ingredientString] 
      measure = recipe["meals"][0][measureString]

      # PRINT INGREDIENT IF IT EXISTS
      if ingredient:
        print(ingredient, "(" + measure + ")")
  print("---------------------")  

  # PRINT THE RECIPE INSTRUCTIONS
  print("Instructions")
  print("---------------------")
  print(recipe["meals"][0]["strInstructions"])
  print("---------------------")

  # PRINT CORRESPONDING VIDEO IF IT EXISTS
  video = recipe["meals"][0]["strYoutube"]
  if video:
    print("Video Link:", video)
  print("---------------------")

# FUNCTION TO CONVERT A RECIPE DATA TO A MORE READABLE AND APPLICABLE DICTIONARY 
def convert_to_dict(recipe):
  """
  This function takes a dictionary of data of a recipe from the MealDB API database , takes the necessary information, and 
  returns a more readable/workable dictionary for further use in the program 
  Params: recipe, which is a dictionary of information of a recipe from the MealDB API database
  Datatypes of Params: recipe is a Dictionary
  Return: This function returns a dictionary with desired information of the recipe passed in to the function. This dictionary 
  will contain the name of the recipe, a jpg url of its picture, instructions, a video URL if its exists, its country of 
  origin/nationality (e.g., Canadaian), its category (e.g., Seafood), and the recipe's ingredients and their corresponding 
  measures.

  Invoke the function like this: convert_to_dict(recipe) where recipe is a dictionary of recipe data of a single recipe from 
  the MealDB API database. 
  """
  ingredients = []
  for x in range (1,19):
    #define variables
    ingredientString = f'strIngredient{x}'
    measureString = f'strMeasure{x}'
    ingredient = recipe["meals"][0][ingredientString] 
    measure = recipe["meals"][0][measureString]

    # APPEND INGREDIENT AND MEASURE IF THEY BOTH EXIST
    if ingredient and measure:
      ingredients.append({
                          "name": ingredient.strip(),
                          "measure": measure.strip()
                         })
  title = recipe["meals"][0]["strMeal"]
  picture_url = recipe["meals"][0]["strMealThumb"]
  instructions = recipe["meals"][0]["strInstructions"]
  video_url = recipe["meals"][0]["strYoutube"]
  area = recipe["meals"][0]["strArea"]
  category = recipe["meals"][0]["strCategory"]
  
  recipes = {
        "name": title.strip(),
        "picture_url": picture_url.strip(),
        "ingredients": ingredients,
        "instructions": instructions.strip(),
        "video_url": video_url.strip(),
        "area": area.strip(),
        "category": category.strip()
       }
  #pprint(recipes)
  return recipes

# FUNCTION TO RETURN A DICTIONARY OF RECIPE INFORMATION BASED OFF OF THE RECIPE'S NAME 
def display_name(name):
  """
  This function takes in a recipe name and returns a useful dictionary of that recipe's information.
  
  Params: name, which is the name of a recipe in the mealDB database
  Datatypes of Params: name is a String 
  Return: This function returns a dictionary of the recipe of the name passed, containing information on the recipe's
  name, picture URL, ingredients (and corresponding measures), instructions, a video URL (if it exists), the recipe's country 
  of origin/nationality (e.g., Canadian), and the recipe's category (e.g., Seafood)

  Invoke the function like this: display_name("Tunisian Orange Cake")
  """
  recipe_url = f'https://www.themealdb.com/api/json/v1/1/search.php?s={name}'
  recipe = read_data(recipe_url)
  recipes = convert_to_dict(recipe)
  #pprint(recipes)
  return recipes

# FUNCTION TO RETURN A LIST OF DICTIONARIES OF RECIPE INFORMATION FOR RECIPES IN A PARTICULAR CATEGORY (e.g., Seafood)
def display_category(category): 
  """
  This function takes in a recipe category and returns a list of dictionaries which contain information for recipes in that
  specific food category
  
  Params: category, which is the category of food the user is searching for (e.g., Seafood)
  Datatypes of Params: category is a String
  Return: This function returns a list of dictionaries for recipes in the MealDB database that are a part of the passed in 
  food category. Each dictionary within the list will contain information on a single recipe, specifically the recipe's
  name, picture URL, ingredients (and corresponding measures), instructions, a video URL (if it exists), the recipe's country 
  of origin/nationality (e.g., Canadian), and the recipe's category (e.g., Seafood)

  Invoke the function like this: display_category("Seafood")
  """

  category_url = f'https://www.themealdb.com/api/json/v1/1/filter.php?c={category}'
  category = read_data(category_url)

  #print(category)
  #meals = []
  recipes_list = []
  for meal in category["meals"]:

    #meals.append(meal["strMeal"])

    #display_name_pics(meal)
    name = meal["strMeal"]

    # Find the instructions and ingredients for each 
    recipe1_url = f'https://www.themealdb.com/api/json/v1/1/search.php?s={name}'
    current = read_data(recipe1_url)

    # Display ingredients, intstruction, and video
    #display_recipe(current)
    recipe = convert_to_dict(current)
    recipes_list.append(recipe)
  #pprint(recipes_list)
  return recipes_list

# FUNCTION TO RETURN A LIST OF DICTIONARIES OF RECIPE INFORMATION FOR RECIPES IN A PARTICULAR NATIONALITY (e.g., Italian)
def display_area(area):
  """
  This function takes in the name of a country/nationality and returns a list of dictionaries 
  which contain information for recipes in that specific area
  
  Params: area, which is the country of origin/nationality that the user wishes to find recipes from
  Datatypes of Params: area is a String
  Return: This function returns a list of dictionaries for recipes in the MealDB database that are a part of the passed in 
  food country of origin/nationality. Each dictionary within the list will contain information on a single recipe, 
  specifically the recipe's name, picture URL, ingredients (and corresponding measures), instructions, 
  a video URL (if it exists), the recipe's country of origin/nationality (e.g., Canadian), and 
  the recipe's category (e.g., Seafood)

  Invoke the function like this: display_area("Italian")
  """
  area_url = f'https://www.themealdb.com/api/json/v1/1/filter.php?a={area}'
  area = read_data(area_url)

  recipes_list = []
  for meal in area["meals"]:
    
    # Display the recipe's name and picture
    #display_name_pics(meal)
    name = meal["strMeal"]

    # Find the instructions and ingredients for each 
    recipe1_url = f'https://www.themealdb.com/api/json/v1/1/search.php?s={name}'
    current = read_data(recipe1_url)

    # Display ingredients, intstruction, and video

    #display_recipe(current)

    recipe = convert_to_dict(current)
    recipes_list.append(recipe)
  return recipes_list

# FUNCTION TO RETURN A LIST OF DICTIONARIES OF RECIPE INFORMATION FOR 10 RANDOMLY SELECTED RECIPES
def display_random():
  """
  This function returns a list of dictionaries which contain information for 10 random recipes in the MealDB API database
  
  Params: none
  Datatypes of Params: no Paramas
  Return: This function returns a list of dictionaries for 10 random recipes in the MealDB database. 
  Each dictionary within the list will contain information on a single recipe, specifically the recipe's name, 
  picture URL, ingredients (and corresponding measures), instructions, a video URL (if it exists), the recipe's country 
  of origin/nationality (e.g., Canadian), and the recipe's category (e.g., Seafood)

  Invoke the function like this: display_random()
  """
  
  recipes_list = []
  for x in range (0,10):
    random_url = "https://www.themealdb.com/api/json/v1/1/random.php"
    random = read_data(random_url)
    
    # Display the recipe's name and picture
    #display_name_pics(random["meals"][0])

    # Display ingredients, intstruction, and video
    #display_recipe(random)

    recipe = convert_to_dict(random)
    recipes_list.append(recipe)
  return recipes_list

# FUNCTION TO RETURN A LIST OF DICTIONARIES OF RECIPE INFORMATION FOR RECIPES CONTAINING A PARTICULAR INGREDIENT (e.g., chicken)
def display_ingredient(ingredient):
  """
  This function takes in an ingredients and returns a list of dictionaries which contain information for all recipes in the 
  MealDB API database that contain that ingredient
  
  Params: ingredient, which is a food ingredient and the user is searching for recipes containing that ingredient
  Datatypes of Params: ingredient is a String
  Return: This function returns a list of dictionaries for recipes in the MealDB database that contain the passed in ingredient. 
  Each dictionary within the list will contain information on a single recipe, specifically the recipe's
  name, picture URL, ingredients (and corresponding measures), instructions, a video URL (if it exists), the recipe's country 
  of origin/nationality (e.g., Canadian), and the recipe's category (e.g., Seafood)

  Invoke the function like this: display_ingredient("Chicken")
  """
  ingredient_url=f'https://www.themealdb.com/api/json/v1/1/filter.php?i={ingredient}'
  ingredient = read_data(ingredient_url)

  recipes_list = []
  for meal in ingredient["meals"]:
    name = meal["strMeal"]
    
    recipe_url = f'https://www.themealdb.com/api/json/v1/1/search.php?s={name}'
    current = read_data(recipe_url)
    
    recipe = convert_to_dict(current)
    recipes_list.append(recipe)
  return recipes_list

# FETCH ALL POSSIBLE CATEGORIES IN MEALlDB API DATABASE
def fetch_categories():
  """
  This function fetches data from the MealDB API database and returns a list of all of the valid categories of Food 
  in the MealDB API database
  
  Params: none
  Datatypes of Params: no Params
  Return: returns a list of all of the valid categories of Food in the MealDB API database

  Invoke the function like this: fetch_categories()
  """

  url = "https://www.themealdb.com/api/json/v1/1/list.php?c=list"
  data = read_data(url)

  categories = []
  for category in data["meals"]:
    categories.append(category["strCategory"])
  
  return categories

# FETCH ALL POSSIBLE FOOD NATIONALITIES IN MEALlDB API DATABASE
def fetch_nationalities():
  """
  This function fetches data from the MealDB API database and returns a list of all of the valid nationalities of food 
  in the MealDB API database
  
  Params: none
  Datatypes of Params: no Params
  Return: returns a list of all of the valid countries of origin/nationalities of food in the MealDB API database

  Invoke the function like this: fetch_nationalities()
  """

  url = "https://www.themealdb.com/api/json/v1/1/list.php?a=list"
  data = read_data(url)

  nationalities = []
  for nationality in data["meals"]:
    nationalities.append(nationality["strArea"])

  return nationalities

# FETCH ALL POSSIBLE INGREDIENTS IN MEALlDB API DATABASE
def fetch_ingredients():
  """
  This function fetches data from the MealDB API database and returns a list of all of the valid ingredients of food 
  in the MealDB API database
  
  Params: none
  Datatypes of Params: no Params
  Return: returns a list of all of the valid ingredients of Food in the MealDB API database

  Invoke the function like this: fetch_ingredients()
  """

  url = "https://www.themealdb.com/api/json/v1/1/list.php?i=list"
  data = read_data(url)

  ingredients = []
  for ingredient in data["meals"]:
    ingredients.append(ingredient["strIngredient"])
  return ingredients

# FETCH ONLY THE CATEGORY OF A RECIPE BASED ON ITS NAME 
def fetch_recipe_category(recipe_name):
  """
  This function fetches the category of a recipe from the MealDB API database based on its name
  
  Params: recipe_name, which is the recipe of interest that information is needed from
  Datatypes of Params: recipe_name is a String
  Return: returns the category (in a string) of a recipe from the MealDB API database based off of recipe_name
  

  Invoke the function like this: fetch_recipe_category("Tunisian Orange Cake")
  """   

  recipe_url = f'https://www.themealdb.com/api/json/v1/1/search.php?s={recipe_name}'
  recipe = read_data(recipe_url)
  category = recipe["meals"][0]["strCategory"]
  return category

# FETCH ONLY THE NATIONALITY/COUNTRY OF ORIGIN OF A RECIPE BASED ON ITS NAME 
def fetch_recipe_area(recipe_name):
  """
  This function fetches the nationality/country of origin of a recipe from the MealDB API database based on its name
  
  Params: recipe_name, which is the recipe of interest that information is needed from
  Datatypes of Params: recipe_name is a String
  Return: returns the nationality/country of origin (in a string) of a recipe from the MealDB API database based off 
  of recipe_name.
  
  Invoke the function like this: fetch_recipe_area("Tunisian Orange Cake")
  """   
  recipe_url = f'https://www.themealdb.com/api/json/v1/1/search.php?s={recipe_name}'
  recipe = read_data(recipe_url)
  area = recipe["meals"][0]["strArea"]
  return area

# FETCH ONLY THE PICTURE URL OF A RECIPE BASED ON ITS NAME 
def fetch_recipe_url(recipe_name):
  """
  This function fetches the picture URL of a recipe from the MealDB API database based on its name
  
  Params: recipe_name, which is the recipe of interest that information is needed from
  Datatypes of Params: recipe_name is a String
  Return: returns the picture URL (in a string) of a recipe from the MealDB API database based off of recipe_name
  

  Invoke the function like this: fetch_recipe_url("Tunisian Orange Cake")
  """   

  recipe_url = f'https://www.themealdb.com/api/json/v1/1/search.php?s={recipe_name}'
  recipe = read_data(recipe_url)
  picture_url = recipe["meals"][0]["strMealThumb"]
  return picture_url




if __name__ == "__main__":
    name = "orange"
    selection =  "Seafood"
    area = "Canadian"
    ingredient = "chicken"


    # # data = read_data(f'https://www.themealdb.com/api/json/v1/1/search.php?s=Tunisian%20Orange%20Cake')
    # # print(data)
    # # display_name(name)
    # # display_category(category)
    # # display_area(area)

    # #recipes = display_category(selection)
    # #recipes = display_name(name)
    # #recipes = display_area(area)
    # recipes = display_random()
    # # recipes = display_ingredient(ingredient)
    # #print(recipes)
    # pprint(recipes)

    # # categories = fetch_categories()
    # # print(categories)
    # # nationalities = fetch_nationalities()
    # # print(nationalities)
    # # ingredients = fetch_ingredients()
    # # print(ingredients)
    # # recipe_name = "Arrabiata"
    # # category = fetch_recipe_category(recipe_name)
    # # area = fetch_recipe_area(recipe_name)
    # # url = fetch_recipe_url(recipe_name)
    # # print(category)
    # # print(area)
    # # print(url)
    

  