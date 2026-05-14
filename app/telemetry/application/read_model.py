from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class TelemetryReadModel:
    telemetry_id: int
    value: float
    timestamp: datetime