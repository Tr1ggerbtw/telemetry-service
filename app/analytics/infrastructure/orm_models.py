from app.shared.db import db

class SensorMetricModel(db.Model):
    __tablename__ = 'analytics_sensor_metric'
    
    metric_id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.Integer, unique=True, nullable=False)
    total_records = db.Column(db.Integer, nullable=False, default=0)
    average_value = db.Column(db.Float, nullable=False, default=0.0)
    anomaly_count = db.Column(db.Integer, nullable=False, default=0)
    last_recorded_at = db.Column(db.DateTime, nullable=False)
