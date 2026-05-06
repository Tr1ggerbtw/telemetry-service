from app.domain.services import IAlertingService

class ConsoleAlertingService(IAlertingService):
    def __init__(self, threshold: float = 80.0):
        self._threshold = threshold

    def check_and_alert(self, sensor_id: int, value: float) -> None:
        if value > self._threshold:
            print(f"Сенсор з айді {sensor_id} зафіксував критичне значення: {value} (Норма: {self._threshold})")
        # ??? 