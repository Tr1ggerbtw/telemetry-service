from app.analytics.application.queries import (
    SensorMetricDTO,
    GetSensorMetricsQueryHandler,
    GetSensorMetricByIdQueryHandler,
)
from app.analytics.infrastructure.repositories import SqlAlchemySensorMetricRepository
 
class AnalyticsModule:

    def __init__(self):
        self._metric_repo = SqlAlchemySensorMetricRepository()
 
    def get_all_metrics(self) -> list[SensorMetricDTO]:
        return GetSensorMetricsQueryHandler(self._metric_repo).handle()
 
    def get_metric_by_sensor(self, sensor_id: int) -> SensorMetricDTO | None:
        return GetSensorMetricByIdQueryHandler(self._metric_repo).handle(sensor_id)
 
 
__all__ = [
    "AnalyticsModule",
    "SensorMetricDTO",
]
