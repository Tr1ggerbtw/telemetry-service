from dataclasses import dataclass

@dataclass
class RegisterUserDTO:
    email: str
    password: str

@dataclass
class CreateLocationDTO:
    name: str
    user_id: int

@dataclass
class AddSensorDTO:
    mac_address: str
    location_id: int

@dataclass
class RecordTelemetryDTO:
    sensor_id: int
    value: float