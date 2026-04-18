from flask import Blueprint, request
from werkzeug.security import generate_password_hash, check_password_hash 
from flask_jwt_extended import create_access_token
import re
from app.db import db
from app.infrastructure.orm_models import User
from app.domain.validators import is_valid_email
auth = Blueprint("auth", __name__)

@auth.route("/register", methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    if(password == None or email == None):
        return {}, 400

    if(is_valid_email(email)) == False:
        return {}, 400
    
    if User.query.filter_by(email=email).first() is not None:
        return {"Error": "Email already exists"}, 409
    
    new_user = User(email = email, password = generate_password_hash(password))
    db.session.add(new_user)
    db.session.commit()
    return {}, 201

@auth.route("/login", methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    if(password == None or email == None):
        return {}, 400

    user = User.query.filter_by(email=email).first()

    if(user == None):
        return {"error": "Invalid credentials"}, 401

    if(check_password_hash(user.password, password)):
        access_token = create_access_token(identity=str(user.user_id)) 
        return {"token": access_token}, 200

    return {"error": "Invalid credentials"}, 401