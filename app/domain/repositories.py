from abc import ABC, abstractmethod
from app.domain.entities import User, Email, Sensor, MacAddress, Telemetry

class IUserRepository(ABC):
    @abstractmethod
    def save(self, user: User) -> None:
        pass

    @abstractmethod
    def get_by_email(self, email: Email) -> User | None:
        pass

class ISensorRepository(ABC):
    @abstractmethod
    def save(self, sensor: Sensor) -> None:
        pass
        
    @abstractmethod
    def get_by_mac(self, mac: MacAddress) -> Sensor | None:
        pass
        
    @abstractmethod
    def delete(self, sensor: Sensor) -> None:
        pass

class ITelemetryRepository(ABC):
    @abstractmethod
    def save(self, telemetry: Telemetry) -> None:
        pass