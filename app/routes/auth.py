from flask import Blueprint, request
from werkzeug.security import generate_password_hash
from app.db import db
from app.models import User
auth = Blueprint("auth", __name__)

@auth.route("/register", methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    if(password == None or email == None):
        return {}, 400

    if User.query.filter_by(email=email).first() is not None:
        return {"Error": "Email already exists"}, 409
    
    new_user = User(email = email, password = generate_password_hash(password))
    db.session.add(new_user)
    db.session.commit()
    return {}, 201