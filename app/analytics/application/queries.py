from dataclasses import dataclass
from datetime import datetime
from app.analytics.domain.repositories import ISensorMetricRepository

@dataclass(frozen=True)
class SensorMetricDTO:
    sensor_id: int
    total_records: int
    average_value: float
    anomaly_count: int
    last_recorded_at: datetime
 
class GetSensorMetricsQueryHandler:
    def __init__(self, metric_repo: ISensorMetricRepository):
        self._metric_repo = metric_repo
 
    def handle(self) -> list[SensorMetricDTO]:
        metrics = self._metric_repo.get_all()
        return [
            SensorMetricDTO(
                sensor_id=m.sensor_id,
                total_records=m.total_records,
                average_value=m.average_value,
                anomaly_count=m.anomaly_count,
                last_recorded_at=m.last_recorded_at,
            )
            for m in metrics
        ]
     
class GetSensorMetricByIdQueryHandler:
    def __init__(self, metric_repo: ISensorMetricRepository):
        self._metric_repo = metric_repo
 
    def handle(self, sensor_id: int) -> SensorMetricDTO | None:
        metric = self._metric_repo.get_by_sensor_id(sensor_id)
        if metric is None:
            return None
        return SensorMetricDTO(
            sensor_id=metric.sensor_id,
            total_records=metric.total_records,
            average_value=metric.average_value,
            anomaly_count=metric.anomaly_count,
            last_recorded_at=metric.last_recorded_at,
        )
