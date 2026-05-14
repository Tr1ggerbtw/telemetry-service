from app.telemetry.application.commands import (
    RegisterUserCommand,
    LoginUserCommand,
    CreateLocationCommand,
    AddSensorCommand,
    DeleteSensorCommand,
    RecordTelemetryCommand,
)
from app.telemetry.application.queries import GetTelemetryHistoryQuery
from app.telemetry.application.read_model import TelemetryReadModel
from app.telemetry.domain.events import TelemetryRecorded
from app.telemetry.domain.exceptions import (
    DomainError,
    AccessDeniedError,
    InvalidEmailError,
    InvalidMacAddressError,
    InvalidTelemetryValueError,
)
from app.telemetry.infrastructure.repositories import (
    SqlAlchemyUserRepository,
    SqlAlchemyLocationRepository,
    SqlAlchemySensorRepository,
    SqlAlchemyTelemetryRepository,
    SqlAlchemyTelemetryReadRepository,
)
from app.telemetry.application.handlers import (
    RegisterUserCommandHandler,
    LoginCommandHandler,
    CreateLocationCommandHandler,
    AddSensorCommandHandler,
    DeleteSensorCommandHandler,
    RecordTelemetryCommandHandler,
    GetTelemetryHistoryQueryHandler,
)
from app.shared.event_bus import EventBus
 
 
class TelemetryModule:
    def __init__(self, event_bus: EventBus):
        self._user_repo = SqlAlchemyUserRepository()
        self._location_repo = SqlAlchemyLocationRepository()
        self._sensor_repo = SqlAlchemySensorRepository()
        self._telemetry_repo = SqlAlchemyTelemetryRepository()
        self._read_repo = SqlAlchemyTelemetryReadRepository()
        self._event_bus = event_bus
 
    def register_user(self, command: RegisterUserCommand) -> None:
        RegisterUserCommandHandler(self._user_repo).handle(command)
 
    def login_user(self, command: LoginUserCommand) -> int:
        return LoginCommandHandler(self._user_repo).handle(command)
 
    def create_location(self, command: CreateLocationCommand) -> None:
        CreateLocationCommandHandler(self._location_repo).handle(command)
 
    def add_sensor(self, command: AddSensorCommand) -> None:
        AddSensorCommandHandler(self._sensor_repo, self._location_repo).handle(command)
 
    def delete_sensor(self, command: DeleteSensorCommand) -> None:
        DeleteSensorCommandHandler(self._sensor_repo, self._location_repo).handle(command)
 
    def record_telemetry(self, command: RecordTelemetryCommand) -> None:
        RecordTelemetryCommandHandler(
            self._telemetry_repo, self._sensor_repo, self._event_bus
        ).handle(command)
 
    def get_telemetry_history(self, query: GetTelemetryHistoryQuery) -> list[TelemetryReadModel]:
        return GetTelemetryHistoryQueryHandler(self._read_repo).handle(query)
 
 
__all__ = [
    # Entry for roiutes
    "TelemetryModule",
    # Commands
    "RegisterUserCommand",
    "LoginUserCommand",
    "CreateLocationCommand",
    "AddSensorCommand",
    "DeleteSensorCommand",
    "RecordTelemetryCommand",
    # Queries
    "GetTelemetryHistoryQuery",
    # Read models
    "TelemetryReadModel",
    # Events
    "TelemetryRecorded",
    # Exceptions
    "DomainError",
    "AccessDeniedError",
    "InvalidEmailError",
    "InvalidMacAddressError",
    "InvalidTelemetryValueError",
]
