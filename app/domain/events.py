from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class TelemetryRecorded:
    sensor_id: int
    value: float
    happened_at: datetime