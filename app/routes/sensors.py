from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.db import db 
from app.models import Sensor, Location, User

sensors = Blueprint("sensors", __name__)
@sensors.route("/create-sensor", methods=['POST'] )
@jwt_required()
def create_sensor():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    location_id = data.get('location_id')

    if location_id is None or address is None:
        return {}, 400

    if Location.query.filter_by(location_id=location_id, user_id=user_id).first() is None:
        return {"error": "Location not found"}, 403
    
    address = data.get('mac_address')

    if Sensor.query.filter_by(mac_address=address).first() is not None: 
        return {"Error": "Sensor with such address already exists"}, 409
    
    new_sensor = Sensor(mac_address = address, location_id=location_id)
    db.session.add(new_sensor)
    db.session.commit()
    return {}, 201

@sensors.route("/delete-sensor", methods=['DELETE'])
@jwt_required()
def delete_sensor():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    sensor_id = data.get('sensor_id')

    sensor = Sensor.query.filter_by(sensor_id=sensor_id).first()
    if sensor is None:
        return {"error": "Sensor not found"}, 404
    
    location = Location.query.filter_by(location_id=sensor.location_id, user_id=user_id).first()
    if location is None:
        return {"error": "Forbidden"}, 403
    
    db.session.delete(sensor)
    db.session.commit()
    return {}, 204