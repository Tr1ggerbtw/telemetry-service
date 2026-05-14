from datetime import datetime

from app.analytics.acl.telemetry_translator import TelemetryEventTranslator
from app.analytics.domain.entities import SensorMetric
from app.analytics.domain.repositories import ISensorMetricRepository
from app.telemetry.api import TelemetryRecorded

class OnTelemetryRecordedHandler:
    def __init__(
        self,
        metric_repo: ISensorMetricRepository,
        translator: TelemetryEventTranslator,
    ):
        self._metric_repo = metric_repo
        self._translator = translator

    def handle(self, event: TelemetryRecorded) -> None:
        data = self._translator.to_incoming_data(event)

        metric = self._metric_repo.get_by_sensor_id(data.sensor_id)

        if metric is None:
            metric = SensorMetric(
                sensor_id=data.sensor_id,
                total_records=1,
                average_value=data.value,
                anomaly_count=1 if data.is_anomaly else 0,
                last_recorded_at=data.recorded_at,
            )
        else:
            new_total = metric.total_records + 1
            new_avg = (metric.average_value * metric.total_records + data.value) / new_total
            metric.total_records = new_total
            metric.average_value = round(new_avg, 4)
            metric.anomaly_count += 1 if data.is_anomaly else 0
            metric.last_recorded_at = data.recorded_at

        self._metric_repo.save(metric)