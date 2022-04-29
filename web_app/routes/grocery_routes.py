from flask import Blueprint, render_template, flash, redirect, current_app, url_for, session, request #, jsonify

from web_app.routes.wrappers import authenticated_route

grocery_routes = Blueprint("grocery_routes", __name__)

@grocery_routes.route("/groceries", methods=["GET","POST"])
@authenticated_route
def orders():

    form_data = dict(request.form)
    print(form_data)

    return render_template("groceries.html")