from abc import ABC, abstractmethod
from app.telemetry.domain.events import TelemetryRecorded
class IAlertingService(ABC):
    @abstractmethod
    def check_and_alert(self, sensor_id: int, value: float):
        pass 
    
    @abstractmethod
    def handle_telemetry_recorded(self, event: TelemetryRecorded) -> None:
        pass