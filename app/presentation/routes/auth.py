from flask import Blueprint, request
from flask_jwt_extended import create_access_token

from app.dependencies import telemetry_module
from app.telemetry.api import (
    RegisterUserCommand,
    LoginUserCommand,
    DomainError,
    InvalidEmailError,
)

auth = Blueprint("auth", __name__)

@auth.route("/register", methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    if password is None or email is None:
        return {"error": "email and password are required"}, 400
    command = RegisterUserCommand(email=email, password=password)
    try:
        telemetry_module.register_user(command)
        return {}, 201
    except InvalidEmailError:
        return {"error": "Invalid email format"}, 400
    except DomainError as e:
        return {"error": str(e)}, 409

@auth.route("/login", methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    if password is None or email is None:
        return {"error": "email and password are required"}, 400
    command = LoginUserCommand(email=email, password=password)
    try:
        user_id = telemetry_module.login_user(command)
        access_token = create_access_token(identity=str(user_id))
        return {"token": access_token}, 200
    except DomainError:
        return {"error": "Invalid credentials"}, 401