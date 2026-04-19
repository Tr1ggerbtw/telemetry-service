from abc import ABC, abstractmethod
from app.domain.entities import User, Email, Sensor, MacAddress, Telemetry, Location

class IUserRepository(ABC):
    @abstractmethod
    def save(self, user: User) -> None:
        pass

    @abstractmethod
    def get_by_email(self, email: Email) -> User | None:
        pass

class ILocationRepository(ABC):
    @abstractmethod
    def save(self, location: Location) -> None:
        pass

    @abstractmethod
    def get_by_id(self, location_id: int) -> Location | None:
        pass

class ISensorRepository(ABC):
    @abstractmethod
    def save(self, sensor: Sensor) -> None:
        pass

    @abstractmethod
    def get_by_mac(self, mac: MacAddress) -> Sensor | None:
        pass

    @abstractmethod
    def get_by_id(self, sensor_id: int) -> Sensor | None:
        pass

    @abstractmethod
    def delete(self, sensor: Sensor) -> None:
        pass

class ITelemetryRepository(ABC):
    @abstractmethod
    def save(self, telemetry: Telemetry) -> None:
        pass

    @abstractmethod
    def get_by_sensor_id(self, sensor_id: int, limit: int) -> list[Telemetry]:
        pass