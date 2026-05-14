from flask import Blueprint
from flask_jwt_extended import jwt_required

from app.dependencies import analytics_module

analytics = Blueprint("analytics", __name__)

@analytics.route("/analytics/metrics", methods=["GET"])
@jwt_required()
def get_all_metrics():

    metrics = analytics_module.get_all_metrics()
    return {
        "data": [
            {
                "sensor_id": m.sensor_id,
                "total_records": m.total_records,
                "average_value": m.average_value,
                "anomaly_count": m.anomaly_count,
                "last_recorded_at": str(m.last_recorded_at),
            }
            for m in metrics
        ]
    }, 200

@analytics.route("/analytics/metrics/<int:sensor_id>", methods=["GET"])
@jwt_required()
def get_metric_by_sensor(sensor_id: int):
    metric = analytics_module.get_metric_by_sensor(sensor_id)
    if metric is None:
        return {"error": "No metrics found for this sensor"}, 404
    return {
        "sensor_id": metric.sensor_id,
        "total_records": metric.total_records,
        "average_value": metric.average_value,
        "anomaly_count": metric.anomaly_count,
        "last_recorded_at": str(metric.last_recorded_at),
    }, 200