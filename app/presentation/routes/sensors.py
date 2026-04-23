from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.application.dtos import AddSensorDTO, DeleteSensorDTO
from app.application.dependencies import get_add_sensor_use_case, get_delete_sensor_use_case 
from app.domain.exceptions import InvalidMacAddressError, DomainError

sensors = Blueprint("sensors", __name__)
@sensors.route("/create-sensor", methods=['POST'] )
@jwt_required()
def create_sensor():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    location_id = data.get('location_id')
    address = data.get('mac_address')

    if location_id is None or address is None:
        return {}, 400

    dto = AddSensorDTO(address, location_id, user_id);

    try:
        get_add_sensor_use_case().execute(dto)
        return {}, 201
    except InvalidMacAddressError:
        return {"error": "Invalid MAC address format"}, 400
    except DomainError as e:
        return {"error": str(e)}, 409
    
@sensors.route("/delete-sensor", methods=['DELETE'])
@jwt_required()
def delete_sensor():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    sensor_id = data.get('sensor_id')
    
    dto = DeleteSensorDTO(sensor_id, user_id)

    try:
        get_delete_sensor_use_case().execute(dto)
        return {}, 204
    except DomainError as e:
        return {"error": str(e)}, 409
