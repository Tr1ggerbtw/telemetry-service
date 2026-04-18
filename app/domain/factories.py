from datetime import datetime, timezone
from app.domain.entities import User, Telemetry
from app.domain.validators import is_valid_email, is_valid_telemetry_value
from app.domain.exceptions import InvalidEmailError, InvalidTelemetryValueError

class UserFactory:
    @staticmethod
    def create(email: str, password_hash: str):
        if not is_valid_email(email):
            raise InvalidEmailError(f"Invalid email format: {email}")
        
        return User(email=email, password_hash=password_hash)

class TelemetryFactory:
    @staticmethod
    def create(sensor_id: int, value: float):
        if not is_valid_telemetry_value(value):
            raise InvalidTelemetryValueError("Value must be a number between 0 and 100")
        
        return Telemetry(
            sensor_id=sensor_id,
            value=value,
            timestamp=datetime.now(timezone.utc)
        )