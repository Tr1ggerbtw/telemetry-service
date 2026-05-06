from abc import ABC, abstractmethod

class IAlertingService(ABC):
    @abstractmethod
    def check_and_alert(self, sensor_id: int, value: float):
        pass 