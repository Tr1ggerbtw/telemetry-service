from dataclasses import dataclass
from datetime import datetime
 
 
@dataclass
class SensorMetric:
    sensor_id: int
    total_records: int
    average_value: float
    anomaly_count: int
    last_recorded_at: datetime
    metric_id: int | None = None
 
 
@dataclass(frozen=True)
class AnomalyEvent:
    sensor_id: int
    value: float
    detected_at: datetime
