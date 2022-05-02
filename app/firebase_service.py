# app/firebase_service.py

import os
from pprint import pprint
from datetime import datetime, timezone
from operator import itemgetter

from firebase_admin import credentials, initialize_app, firestore

CREDENTIALS_FILEPATH = os.path.join(os.path.dirname(__file__), "..", "google-credentials.json")
print("credential filepath")

def generate_timestamp():
    return datetime.now(tz=timezone.utc) #returns the current time stamp


class FirebaseService:
    """
    Fetches data from the cloud firestore database.

    Uses locally downloaded credentials JSON file.
    """
    def __init__(self):
        self.creds = credentials.Certificate(CREDENTIALS_FILEPATH)
        self.app = initialize_app(self.creds) # or set FIREBASE_CONFIG variable and initialize without creds
        self.db = firestore.client()

    #
    # PRODUCTS
    #

    def fetch_products(self):
        products_ref = self.db.collection("products")
        products = [doc.to_dict() for doc in products_ref.stream()]
        return products

    #
    # ORDERS
    #

    @property
    def recipes_ref(self):
        return self.db.collection("recipes")

    @property
    def groceries_ref(self):
        return self.db.collection("groceries")

    def create_grocery(self, user_email, recipe_info):
        """
        This function creates and stores a new grocery in a Cloud Firestore Database named "groceries"
        Params :

            user_email (str)

            recipe_info (dict) with name, category, area (i.e., nationality), and picture URL

        """
        new_grocery_ref = self.groceries_ref.document() # new document with auto-generated id
        new_grocery = {
            "user_email": user_email,
            "recipe_info": recipe_info,
            "recipe_at": generate_timestamp()
        }
        results = new_grocery_ref.set(new_grocery)
        return new_grocery, results

    def create_recipe(self, user_email, recipe_info):
        """
        This function creates and stores a new recipe in a Cloud Firestore Database named "recipes"
        Params :

            user_email (str)

            recipe_info (dict) with name, category, area (i.e., nationality), and picture URL

        """
        new_recipe_ref = self.recipes_ref.document() # new document with auto-generated id
        new_recipe = {
            "user_email": user_email,
            "recipe_info": recipe_info,
            "recipe_at": generate_timestamp()
        }
        results = new_recipe_ref.set(new_recipe)
        #print(results) #> {update_time: {seconds: 1648419942, nanos: 106452000}}
        return new_recipe, results

    # DON'T THINK I USE THIS FUNCTION
    def fetch_recipes(self):
        recipes = [doc.to_dict() for doc in self.recipes_ref.stream()]
        return recipes

    # DON'T THINK I USE THIS FUNCTION
    def fetch_groceries(self):
        groceries = [doc.to_dict() for doc in self.groceries_ref.stream()]
        return groceries


    def fetch_user_groceries(self, user_email):
        """
        This function fetches a user's groceries from a Cloud Firestore Database named "groceries" based off their email
        Params :

            user_email (str)

        """
        query_ref = self.groceries_ref.where("user_email", "==", user_email)
        docs = list(query_ref.stream())
        groceries = []
        for doc in docs:
            grocery = doc.to_dict()
            grocery["id"] = doc.id
            #breakpoint()
            #order["order_at"] = order["order_at"].strftime("%Y-%m-%d %H:%M")
            groceries.append(grocery)
        # sorting so latest order is first
        groceries = sorted(groceries, key=itemgetter("recipe_at"), reverse=True)
        return groceries

    def fetch_user_recipes(self, user_email):
        """
        This function fetches a user's saved recipes from a Cloud Firestore Database named "recipes" based off their email
        Params :

            user_email (str)
            
        """
        query_ref = self.recipes_ref.where("user_email", "==", user_email)

        # sorting requires configuration of a composite index on the "recipes" collection,
        # ... so to keep it simple for students, we'll sort manually (see below)
        #query_ref = query_ref.order_by("order_at", direction=firestore.Query.DESCENDING) #.limit_to_last(20)

        # let's return the dictionaries, so these are serializable (and can be stored in the session)
        docs = list(query_ref.stream())
        recipes = []
        for doc in docs:
            recipe = doc.to_dict()
            recipe["id"] = doc.id
            #breakpoint()
            #order["order_at"] = order["order_at"].strftime("%Y-%m-%d %H:%M")
            recipes.append(recipe)
        # sorting so latest order is first
        recipes = sorted(recipes, key=itemgetter("recipe_at"), reverse=True)
        return recipes





if __name__ == "__main__":


    service = FirebaseService()

    # print("-----------")
    # print("PRODUCTS...")
    # products = service.fetch_products()
    # pprint(products)

    print("-----------")
    print("ORDERS...")
    orders = service.fetch_orders()
    print(len(orders))

    print("-----------")
    print("NEW ORDER...")
    #product = products[0]
    product = "orange"
    email_address = input("Email Address: ") or "hello@example.com"
    new_order, results = service.create_order(email_address, product)
    pprint(new_order)

    print("-----------")
    print("USER ORDERS...")
    user_orders = service.fetch_user_orders(email_address)
    print(len(user_orders))