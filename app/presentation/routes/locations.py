from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.application.commands import CreateLocationCommand
from app.application.dependencies import get_create_location_use_case
from app.domain.exceptions import DomainError

locations = Blueprint("locations", __name__)

@locations.route('/locations', methods=['POST'])
@jwt_required()
def create_location():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    name = data.get('name')

    if not name:
        return {"error": "name is required"}, 400
            
    command = CreateLocationCommand(name, user_id)
    try:
        get_create_location_use_case().execute(command)
        return {}, 201
    except DomainError as e:
        return {"error": str(e)}, 400
        