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

@dataclass
class LoginUserDTO:
    email: str
    password: str

@dataclass
class DeleteSensorDTO:
    sensor_id: int
    user_id: int

@dataclass
class GetTelemetryHistoryDTO:
    mac_address: str
    user_id: int
    limit: int = 50