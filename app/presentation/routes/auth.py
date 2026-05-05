from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from app.application.dependencies import get_register_handler, get_login_handler
from app.application.commands import RegisterUserCommand, LoginUserCommand
from app.domain.exceptions import DomainError, InvalidEmailError

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
        get_register_handler().handle(command)
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
        user_id = get_login_handler().handle(command)
        access_token = create_access_token(identity=str(user_id))
        return {"token": access_token}, 200
    except DomainError:
        return {"error": "Invalid credentials"}, 401