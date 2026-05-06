import pytest
from unittest.mock import MagicMock
from app.application.commands import (
    RegisterUserCommand, AddSensorCommand,
    DeleteSensorCommand, RecordTelemetryCommand
)
from app.application.handlers import (
    RegisterUserCommandHandler, AddSensorCommandHandler,
    DeleteSensorCommandHandler, RecordTelemetryCommandHandler
)
from app.domain.entities import User, Email, Location, Sensor, MacAddress
from app.domain.exceptions import DomainError, AccessDeniedError
from app.domain.repositories import (
    IUserRepository, ILocationRepository,
    ISensorRepository, ITelemetryRepository
)

### InMemory 

class InMemoryUserRepository(IUserRepository):
    def __init__(self):
        self._users: dict[str, User] = {}
        self._next_id = 1

    def save(self, user: User) -> None:
        user.user_id = self._next_id
        self._next_id += 1
        self._users[user.email.value] = user

    def get_by_email(self, email: Email) -> User | None:
        return self._users.get(email.value)


class InMemoryLocationRepository(ILocationRepository):
    def __init__(self):
        self._locations: dict[int, Location] = {}
        self._next_id = 1

    def save(self, location: Location) -> None:
        location.location_id = self._next_id
        self._next_id += 1
        self._locations[location.location_id] = location

    def get_by_id(self, location_id: int) -> Location | None:
        return self._locations.get(location_id)


class InMemorySensorRepository(ISensorRepository):
    def __init__(self):
        self._sensors: dict[int, Sensor] = {}
        self._next_id = 1

    def save(self, sensor: Sensor) -> None:
        sensor.sensor_id = self._next_id
        self._next_id += 1
        self._sensors[sensor.sensor_id] = sensor

    def get_by_mac(self, mac: MacAddress) -> Sensor | None:
        for s in self._sensors.values():
            if s.mac_address.value == mac.value:
                return s
        return None

    def get_by_id(self, sensor_id: int) -> Sensor | None:
        return self._sensors.get(sensor_id)

    def delete(self, sensor: Sensor) -> None:
        self._sensors.pop(sensor.sensor_id, None)


class InMemoryTelemetryRepository(ITelemetryRepository):
    def __init__(self):
        self._records = []

    def save(self, telemetry) -> None:
        self._records.append(telemetry)

    def get_by_sensor_id(self, sensor_id: int, limit: int):
        return [t for t in self._records if t.sensor_id == sensor_id][:limit]


# RegisterUserCommandHandler

def test_register_success():
    user_repo = InMemoryUserRepository()
    handler = RegisterUserCommandHandler(user_repo)
    handler.handle(RegisterUserCommand(email="test@gmail.com", password="123456"))
    assert user_repo.get_by_email(Email("test@gmail.com")) is not None


def test_register_duplicate_email_raises():
    user_repo = InMemoryUserRepository()
    handler = RegisterUserCommandHandler(user_repo)
    handler.handle(RegisterUserCommand(email="test@gmail.com", password="123456"))
    with pytest.raises(DomainError):
        handler.handle(RegisterUserCommand(email="test@gmail.com", password="654321"))


# AddSensorCommandHandler

def test_add_sensor_success():
    sensor_repo = InMemorySensorRepository()
    location_repo = InMemoryLocationRepository()
    location_repo.save(Location(name="home", user_id=1, location_id=1))

    handler = AddSensorCommandHandler(sensor_repo, location_repo)
    handler.handle(AddSensorCommand(mac_address="AA:BB:CC:DD:EE:FF", location_id=1, user_id=1))

    assert sensor_repo.get_by_mac(MacAddress("AA:BB:CC:DD:EE:FF")) is not None


def test_add_sensor_wrong_owner_raises():
    sensor_repo = InMemorySensorRepository()
    location_repo = InMemoryLocationRepository()
    location_repo.save(Location(name="home", user_id=999, location_id=1))

    handler = AddSensorCommandHandler(sensor_repo, location_repo)
    with pytest.raises(AccessDeniedError):
        handler.handle(AddSensorCommand(mac_address="AA:BB:CC:DD:EE:FF", location_id=1, user_id=1))


def test_add_sensor_location_not_found_raises():
    handler = AddSensorCommandHandler(InMemorySensorRepository(), InMemoryLocationRepository())
    with pytest.raises(AccessDeniedError):
        handler.handle(AddSensorCommand(mac_address="AA:BB:CC:DD:EE:FF", location_id=999, user_id=1))


def test_add_sensor_duplicate_mac_raises():
    sensor_repo = InMemorySensorRepository()
    location_repo = InMemoryLocationRepository()
    location_repo.save(Location(name="home", user_id=1, location_id=1))

    handler = AddSensorCommandHandler(sensor_repo, location_repo)
    handler.handle(AddSensorCommand(mac_address="AA:BB:CC:DD:EE:FF", location_id=1, user_id=1))
    with pytest.raises(DomainError):
        handler.handle(AddSensorCommand(mac_address="AA:BB:CC:DD:EE:FF", location_id=1, user_id=1))


# DeleteSensorCommandHandler

def test_delete_sensor_success():
    sensor_repo = InMemorySensorRepository()
    location_repo = InMemoryLocationRepository()
    location_repo.save(Location(name="home", user_id=1, location_id=1))
    sensor_repo.save(Sensor(mac_address=MacAddress("AA:BB:CC:DD:EE:FF"), location_id=1, sensor_id=1))

    handler = DeleteSensorCommandHandler(sensor_repo, location_repo)
    handler.handle(DeleteSensorCommand(sensor_id=1, user_id=1))

    assert sensor_repo.get_by_id(1) is None


def test_delete_sensor_wrong_owner_raises():
    sensor_repo = InMemorySensorRepository()
    location_repo = InMemoryLocationRepository()
    location_repo.save(Location(name="home", user_id=999, location_id=1))
    sensor_repo.save(Sensor(mac_address=MacAddress("AA:BB:CC:DD:EE:FF"), location_id=1, sensor_id=1))

    handler = DeleteSensorCommandHandler(sensor_repo, location_repo)
    with pytest.raises(AccessDeniedError):
        handler.handle(DeleteSensorCommand(sensor_id=1, user_id=1))


# RecordTelemetrCommandHandler

def test_record_telemetry_success():
    telemetry_repo = InMemoryTelemetryRepository()
    sensor_repo = InMemorySensorRepository()
    sensor_repo.save(Sensor(mac_address=MacAddress("AA:BB:CC:DD:EE:FF"), location_id=1, sensor_id=1))
    
    dummy_event_bus = MagicMock()

    handler = RecordTelemetryCommandHandler(telemetry_repo, sensor_repo, dummy_event_bus)
    handler.handle(RecordTelemetryCommand(sensor_id=1, value=50.0))

    assert len(telemetry_repo._records) == 1
    dummy_event_bus.publish.assert_called_once()


def test_record_telemetry_sensor_not_found_raises():
    dummy_event_bus = MagicMock()
    handler = RecordTelemetryCommandHandler(InMemoryTelemetryRepository(), InMemorySensorRepository(), dummy_event_bus)
    with pytest.raises(DomainError):
        handler.handle(RecordTelemetryCommand(sensor_id=999, value=50.0))