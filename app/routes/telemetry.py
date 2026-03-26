from flask import Blueprint, request
from app.db import db
from app.models import Telemetry, Sensor

telemetry = Blueprint("telemetry", __name__)
@telemetry.route("/telemetry-send", methods=['POST'])
def send():
    data = request.get_json()
    sensor_id = data.get('sensor_id')
    value = data.get('value')

    if sensor_id is None or value is None:
        return {"error": "sensor_id and value are required"}, 400
    
    if Sensor.query.filter_by(sensor_id=sensor_id).first() is None: 
        return {}, 404
    
    if not(0 <= value <= 100):
        return {"error": "Value out of physical range"}, 400
    
    new_telemetry = Telemetry(sensor_id=sensor_id, value=value)
    db.session.add(telemetry)
    db.session.commit()
    return {}, 201
    
