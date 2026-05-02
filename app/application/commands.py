from dataclasses import dataclass

@dataclass(frozen=True)
class RegisterUserCommand:
    email: str
    password: str

@dataclass(frozen=True)
class LoginUserCommand:
    email: str
    password: str

@dataclass(frozen=True)
class CreateLocationCommand:
    name: str
    user_id: int

@dataclass(frozen=True)
class AddSensorCommand:
    mac_address: str
    location_id: int
    user_id: int

@dataclass(frozen=True)
class DeleteSensorCommand:
    sensor_id: int
    user_id: int

@dataclass(frozen=True)
class RecordTelemetryCommand:
    sensor_id: int
    value: float