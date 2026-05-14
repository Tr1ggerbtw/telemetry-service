from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.dependencies import telemetry_module
from app.telemetry.api import (
    RecordTelemetryCommand,
    GetTelemetryHistoryQuery,
    DomainError,
    InvalidTelemetryValueError,
)

telemetry = Blueprint("telemetry", __name__)

@telemetry.route("/telemetry-send", methods=['POST'])
def send():
    data = request.get_json()
    sensor_id = data.get('sensor_id')
    value = data.get('value')
    if sensor_id is None or value is None:
        return {"error": "sensor_id and value are required"}, 400
    command = RecordTelemetryCommand(sensor_id, value)
    try:
        telemetry_module.record_telemetry(command)
        return {}, 201
    except InvalidTelemetryValueError:
        return {"error": "Invalid telemetry value"}, 400
    except DomainError as e:
        return {"error": str(e)}, 404

@telemetry.route("/telemetry-history", methods=['GET'])
@jwt_required()
def get_history():
    user_id = int(get_jwt_identity())
    mac_address = request.args.get('mac_address')
    limit = request.args.get('limit', 50, type=int)
    if mac_address is None:
        return {"error": "mac_address is required"}, 400
    query = GetTelemetryHistoryQuery(mac_address, user_id, limit)
    try:
        records = telemetry_module.get_telemetry_history(query)
        return {
            "data": [
                {
                    "telemetry_id": t.telemetry_id,
                    "value": t.value,
                    "timestamp": str(t.timestamp),
                }
                for t in records
            ]
        }, 200
    except DomainError as e:
        return {"error": str(e)}, 403