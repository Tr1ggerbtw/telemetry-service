from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.dependencies import telemetry_module
from app.telemetry.api import CreateLocationCommand, DomainError

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
        telemetry_module.create_location(command)
        return {}, 201
    except DomainError as e:
        return {"error": str(e)}, 400