from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.db import db
from app.infrastructure.orm_models import Telemetry, Sensor, Location
from app.domain.validators import is_valid_telemetry_value
from datetime import datetime, timezone

telemetry = Blueprint("telemetry", __name__)
@telemetry.route("/telemetry-send", methods=['POST'])
def send():
    data = request.get_json()
    sensor_id = data.get('sensor_id')
    value = data.get('value')

    if sensor_id is None or value is None:
        return {"error": "sensor_id and value are required"}, 400
    
    if not(is_valid_telemetry_value(value)):
        return {"error": "Value out of physical range"}, 400

    if Sensor.query.filter_by(sensor_id=sensor_id).first() is None: 
        return {}, 404
        
    new_telemetry = Telemetry(sensor_id=sensor_id, value=value, timestamp=datetime.now(timezone.utc))
    db.session.add(new_telemetry)
    db.session.commit()
    return {}, 201

@telemetry.route("/telemetry-history", methods=['GET'])
@jwt_required()
def get_history():
    user_id = int(get_jwt_identity())
    mac_address = request.args.get('mac_address')
    limit = request.args.get('limit', 50, type=int)

    if mac_address is None:
        return {"error": "mac_address is required"}, 400

    sensor = Sensor.query.filter_by(mac_address=mac_address).first()
    if sensor is None:
        return {"error": "Sensor not found"}, 404

    location = Location.query.filter_by(location_id=sensor.location_id, user_id=user_id).first()
    if location is None:
        return {"error": "Forbidden"}, 403

    records = Telemetry.query.filter_by(sensor_id=sensor.sensor_id)\
        .order_by(Telemetry.timestamp.desc())\
        .limit(limit)\
        .all()

    result = [{"telemetry_id": r.telemetry_id, "value": r.value, "timestamp": str(r.timestamp)} for r in records]
    return {"data": result}, 200