# web_app/__init__.py

import os
from dotenv import load_dotenv
from flask import Flask

from web_app.routes.home_routes import home_routes
from web_app.routes.login_routes import login_routes
from web_app.routes.recipe_routes import recipe_routes
from web_app.routes.nutrition_routes import nutrition_routes
from web_app.routes.list_routes import list_routes
from web_app.routes.help_routes import help_routes


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", default="super secret") # set this to something else on production!!!

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = SECRET_KEY
    app.register_blueprint(home_routes)
    app.register_blueprint(login_routes)
    app.register_blueprint(recipe_routes)
    app.register_blueprint(nutrition_routes)
    app.register_blueprint(list_routes)
    app.register_blueprint(help_routes)
    return app

if __name__ == "__main__":
    my_app = create_app()
    my_app.run(debug=True)