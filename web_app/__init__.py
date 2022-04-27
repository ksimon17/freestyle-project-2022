# web_app/__init__.py

import os
from dotenv import load_dotenv
from flask import Flask

from authlib.integrations.flask_client import OAuth

from app import APP_ENV, APP_VERSION
from app.firebase_service import FirebaseService

from web_app.routes.home_routes import home_routes
from web_app.routes.login_routes import login_routes
from web_app.routes.recipe_routes import recipe_routes
from web_app.routes.nutrition_routes import nutrition_routes
from web_app.routes.list_routes import list_routes
from web_app.routes.help_routes import help_routes
from web_app.routes.auth_routes import auth_routes

load_dotenv()

# for google oauth login:
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID") # need to setup
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET") # need to setup

# for google analytics (universal analytics):
GA_TRACKER_ID = os.getenv("GA_TRACKER_ID", default="G-OOPS")


SECRET_KEY = os.getenv("SECRET_KEY", default="super secret") # set this to something else on production!!!

def create_app():
    app = Flask(__name__)

    # for flask flash messaging:
    app.config["SECRET_KEY"] = SECRET_KEY

    # for front-end (maybe doesn't belong here but its ok):
    app.config["APP_ENV"] = APP_ENV
    app.config["APP_VERSION"] = APP_VERSION
    # app.config["APP_TITLE"] = APP_TITLE
    # app.config["NAV_ICON_CLASS"] = NAV_ICON_CLASS
    # app.config["NAV_COLOR_CLASS"] = NAV_COLOR_CLASS

    # for client-side google analytics:
    app.config["GA_TRACKER_ID"] = GA_TRACKER_ID

    

    os.environ["TZ"] = "UTC"

    oauth = OAuth(app)
    oauth.register(
        name="google",
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={"scope": "openid email profile"},
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        #authorize_params={"access_type": "offline"} # give us the refresh token! see: https://stackoverflow.com/questions/62293888/obtaining-and-storing-refresh-token-using-authlib-with-flask
    )
    app.config["OAUTH"] = oauth


    #
    # SERVICES
    #
    app.config["FIREBASE_SERVICE"] = FirebaseService()



    # ROUTES
    app.register_blueprint(home_routes)
    app.register_blueprint(login_routes)
    app.register_blueprint(recipe_routes)
    app.register_blueprint(nutrition_routes)
    app.register_blueprint(list_routes)
    app.register_blueprint(help_routes)
    app.register_blueprint(auth_routes)


    return app

if __name__ == "__main__":
    my_app = create_app()
    my_app.run(debug=True)