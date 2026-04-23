from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from app.application.dependencies import get_register_use_case, get_login_use_case
from app.application.dtos import RegisterUserDTO, LoginUserDTO
from app.domain.exceptions import DomainError, InvalidEmailError

auth = Blueprint("auth", __name__)

@auth.route("/register", methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if password is None or email is None:
        return {"error": "email and password are required"}, 400

    dto = RegisterUserDTO(email=email, password=password)

    try:
        get_register_use_case().execute(dto)
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

    dto = LoginUserDTO(email=email, password=password)

    try:
        user = get_login_use_case().execute(dto)
        access_token = create_access_token(identity=str(user.user_id))
        return {"token": access_token}, 200
    except DomainError:
        return {"error": "Invalid credentials"}, 401