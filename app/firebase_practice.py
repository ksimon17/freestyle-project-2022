import os
from pprint import pprint
from datetime import datetime, timezone
from operator import itemgetter

from firebase_admin import credentials, initialize_app, firestore

CREDENTIALS_FILEPATH = os.path.join(os.path.dirname(__file__), "..", "google-credentials.json")


def generate_timestamp():
    return datetime.now(tz=timezone.utc)


class FirebaseService:

    # Add a new doc in collection 'cities' with ID 'LA'

    def __init__(self):
            self.creds = credentials.Certificate(CREDENTIALS_FILEPATH)
            self.app = initialize_app(self.creds) # or set FIREBASE_CONFIG variable and initialize without creds
            self.db = firestore.client()

    @property
    def recipes_ref(self):
        return self.db.collection("recipes")

    def create_recipe(self, user_email, recipe_info):
        """
        Params :

            user_email (str)

            product_info (dict) with name, description, price, and url

        """
        print("hello")
        data = {
            u'name': u'Los Angeles',
            u'state': u'CA',
            u'country': u'USA'
        }
        self.db.collection(u'cities').document(u'LA').set(data)

        new_collection = {
            u'name': u'New York',
            u'state':u'NY',
            u'country': u'USA'
        }
        new_ref = self.db.collection(u'cities').document(u'NY')
        new_ref.set({
             u'capital': True
        }, merge=True)

        new_recipe_ref = self.recipes_ref.document() # new document with auto-generated id
        new_recipe = {
            "user_email": user_email,
            "recipe_info": recipe_info,
            "order_at": generate_timestamp()
        }
        results = new_recipe_ref.set(new_recipe)
        #print(results) #> {update_time: {seconds: 1648419942, nanos: 106452000}}
        
        return new_recipe, results

    def fetch_recipes(self):
        recipes = [doc.to_dict() for doc in self.recipes_ref.stream()]
        return recipes

    def fetch_user_recipes(self, user_email):
        query_ref = self.recipes_ref.where("user_email", "==", user_email)

        # sorting requires configuration of a composite index on the "orders" collection,
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
        recipes = sorted(recipes, key=itemgetter("order_at"), reverse=True)
        return recipes


if __name__ == "__main__":
    service = FirebaseService()

    # print("-----------")
    # print("PRODUCTS...")
    # products = service.fetch_products()
    # pprint(products)

    # print("-----------")
    # print("ORDERS...")
    # orders = service.fetch_orders()
    # print(len(orders))

    print("-----------")
    print("NEW RECIPE...")
    # product = products[0]
    recipe = "Chicken"
    email_address = input("Email Address: ") or "hello@example.com"
    new_order, results = service.create_recipe(email_address, recipe)
    pprint(new_order)

    print("-----------")
    print("USER RECIPES...")
    user_recipes = service.fetch_user_recipes(email_address)
    print(len(user_recipes))
    print(user_recipes)