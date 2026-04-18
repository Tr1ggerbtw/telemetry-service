from dataclasses import dataclass
from datetime import datetime

@dataclass
class User:
    email: str
    password_hash: str
    user_id: int | None = None 

@dataclass
class Location:
    name: str
    user_id: int
    location_id: int | None = None

@dataclass
class Sensor:
    mac_address: str
    location_id: int
    sensor_id: int | None = None

@dataclass
class Telemetry:
    sensor_id: int
    timestamp: datetime
    value: float
    telemetry_id: int | None = None