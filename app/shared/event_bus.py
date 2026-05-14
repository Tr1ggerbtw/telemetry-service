from typing import Callable, Dict, List, Type, Any

class EventBus:
    def __init__(self):
        # Ключ - тип події; значення - список функцій, які на неї підписані
        self._handlers: Dict[Type, List[Callable]] = {}

    def subscribe(self, event_type: Type, handler: Callable) -> None:
        self._handlers.setdefault(event_type, []).append(handler)

    def publish(self, event: Any) -> None:
        for handler in self._handlers.get(type(event), []):
            handler(event)