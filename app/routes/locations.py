from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.db import db
from app.models import Location
locations = Blueprint("locations", __name__)

@locations.route('/locations', methods=['POST'])
@jwt_required()
def create_location():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    name = data.get('name')

    if(name == None):
        return {}, 400
            
    new_location = Location(name=name, user_id=user_id)
    db.session.add(new_location)
    db.session.commit()
    return {}, 201
        