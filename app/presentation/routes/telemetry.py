from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.application.commands import RecordTelemetryCommand
from app.application.queries import GetTelemetryHistoryQuery
from app.application.dependencies import get_record_telemetry_use_case, get_telemetry_history_use_case
from app.domain.exceptions import InvalidTelemetryValueError, DomainError

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
        get_record_telemetry_use_case().execute(command)
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
        records = get_telemetry_history_use_case().execute(query)
        result = [
            {
                "telemetry_id": t.telemetry_id,
                "value": t.value,
                "timestamp": str(t.timestamp)
            }
            for t in records
        ]
        return {"data": result}, 200
    except DomainError as e:
        return {"error": str(e)}, 403