from abc import ABC, abstractmethod
from app.analytics.domain.entities import SensorMetric
 
class ISensorMetricRepository(ABC):
    @abstractmethod
    def get_by_sensor_id(self, sensor_id: int) -> SensorMetric | None:
        pass
 
    @abstractmethod
    def save(self, metric: SensorMetric) -> None:
        pass
 
    @abstractmethod
    def get_all(self) -> list[SensorMetric]:
        pass
