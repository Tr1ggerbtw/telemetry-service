from flask import Blueprint

auth = Blueprint("auth", __name__)

@auth.route("/register")
def register():
    return "<h3>You're registered!!!!!!</h3>"