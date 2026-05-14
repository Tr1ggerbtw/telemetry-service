from app.analytics.domain.repositories import ISensorMetricRepository
from app.analytics.domain.entities import SensorMetric
from app.analytics.infrastructure.orm_models import SensorMetricModel
from app.shared.db import db
 
 
class SqlAlchemySensorMetricRepository(ISensorMetricRepository):
    def get_by_sensor_id(self, sensor_id: int) -> SensorMetric | None:
        row = SensorMetricModel.query.filter_by(sensor_id=sensor_id).first()
        if row is None:
            return None
        return SensorMetric(
            metric_id=row.metric_id,
            sensor_id=row.sensor_id,
            total_records=row.total_records,
            average_value=row.average_value,
            anomaly_count=row.anomaly_count,
            last_recorded_at=row.last_recorded_at,
        )
 
    def save(self, metric: SensorMetric) -> None:
        row = SensorMetricModel.query.filter_by(sensor_id=metric.sensor_id).first()
        if row is None:
            row = SensorMetricModel(
                sensor_id=metric.sensor_id,
                total_records=metric.total_records,
                average_value=metric.average_value,
                anomaly_count=metric.anomaly_count,
                last_recorded_at=metric.last_recorded_at,
            )
            db.session.add(row)
        else:
            row.total_records = metric.total_records
            row.average_value = metric.average_value
            row.anomaly_count = metric.anomaly_count
            row.last_recorded_at = metric.last_recorded_at
 
        db.session.commit()
        metric.metric_id = row.metric_id
 
    def get_all(self) -> list[SensorMetric]:
        rows = SensorMetricModel.query.order_by(SensorMetricModel.sensor_id).all()
        return [
            SensorMetric(
                metric_id=row.metric_id,
                sensor_id=row.sensor_id,
                total_records=row.total_records,
                average_value=row.average_value,
                anomaly_count=row.anomaly_count,
                last_recorded_at=row.last_recorded_at,
            )
            for row in rows
        ]
