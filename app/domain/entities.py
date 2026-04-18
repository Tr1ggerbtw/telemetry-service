from dataclasses import dataclass
from datetime import datetime
from app.domain.exceptions import InvalidEmailError, InvalidMacAddressError
from app.domain.validators import is_valid_email, is_valid_mac_address

@dataclass(frozen=True)
class Email:
    value: str

    def __post_init__(self):
        if not is_valid_email(self.value):
            raise InvalidEmailError(f"Invalid email: {self.value}")

@dataclass(frozen=True)
class MacAddress:
    value: str

    def __post_init__(self):
        if not is_valid_mac_address(self.value):
            raise InvalidMacAddressError(f"Invalid MAC address format: {self.value}")

@dataclass
class User:
    email: Email
    password_hash: str
    user_id: int | None = None 

@dataclass
class Location:
    name: str
    user_id: int
    location_id: int | None = None

@dataclass
class Sensor:
    mac_address: MacAddress
    location_id: int
    sensor_id: int | None = None

@dataclass
class Telemetry:
    sensor_id: int
    timestamp: datetime
    value: float
    telemetry_id: int | None = None