from datetime import datetime
from dataclasses import dataclass

from app.telemetry.api import TelemetryRecorded
from app.analytics.domain.entities import AnomalyEvent

ANOMALY_THRESHOLD = 80.0

@dataclass(frozen=True)
class IncomingTelemetryData:
    sensor_id: int
    value: float
    recorded_at: datetime
    is_anomaly: bool

class TelemetryEventTranslator:
    @staticmethod
    def to_incoming_data(event: TelemetryRecorded) -> IncomingTelemetryData:
        return IncomingTelemetryData(
            sensor_id=event.sensor_id,
            value=event.value,
            recorded_at=event.happened_at,
            is_anomaly=event.value > ANOMALY_THRESHOLD,
        )

    @staticmethod
    def to_anomaly_event(event: TelemetryRecorded) -> AnomalyEvent | None:
        if event.value <= ANOMALY_THRESHOLD:
            return None
        return AnomalyEvent(
            sensor_id=event.sensor_id,
            value=event.value,
            detected_at=event.happened_at,
        )