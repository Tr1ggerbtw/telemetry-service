from abc import ABC, abstractmethod
from read_model import TelemetryReadModel
class ITelemetryReadRepository(ABC):
    @abstractmethod
    def get_history(self, mac_address: str, user_id: int, limit: int) -> list[TelemetryReadModel]:
        pass