from app.infrastructure.repositories import (
    SqlAlchemyUserRepository,
    SqlAlchemyLocationRepository,
    SqlAlchemySensorRepository,
    SqlAlchemyTelemetryRepository,
    SqlAlchemyTelemetryReadRepository
)
from app.application.handlers import (
    RegisterUserCommandHandler,
    LoginCommandHandler,
    CreateLocationCommandHandler,
    AddSensorCommandHandler,
    DeleteSensorCommandHandler,
    RecordTelemetryCommandHandler,
    GetTelemetryHistoryQueryHandler,
    RecordTelemetryCommandHandlerSync
)
from app.infrastructure.services import ConsoleAlertingService
from app.infrastructure.event_bus import EventBus
from app.domain.events import TelemetryRecorded

global_event_bus = EventBus()

alerting_service = ConsoleAlertingService(threshold=80.0)

global_event_bus.subscribe(TelemetryRecorded, alerting_service.handle_telemetry_recorded)

def get_register_handler() -> RegisterUserCommandHandler:
    return RegisterUserCommandHandler(user_repo=SqlAlchemyUserRepository())

def get_login_handler() -> LoginCommandHandler:
    return LoginCommandHandler(user_repo=SqlAlchemyUserRepository())

def get_create_location_handler() -> CreateLocationCommandHandler:
    return CreateLocationCommandHandler(location_repo=SqlAlchemyLocationRepository())

def get_add_sensor_handler() -> AddSensorCommandHandler:
    return AddSensorCommandHandler(
        sensor_repo=SqlAlchemySensorRepository(),
        location_repo=SqlAlchemyLocationRepository()
    )

def get_delete_sensor_handler() -> DeleteSensorCommandHandler:
    return DeleteSensorCommandHandler(
        sensor_repo=SqlAlchemySensorRepository(),
        location_repo=SqlAlchemyLocationRepository()
    )

def get_record_telemetry_handler() -> RecordTelemetryCommandHandler:
    return RecordTelemetryCommandHandler(
        telemetry_repo=SqlAlchemyTelemetryRepository(),
        sensor_repo=SqlAlchemySensorRepository(),
        event_bus=global_event_bus
        # alerting_service=ConsoleAlertingService(threshold=80.0)
    )

def get_telemetry_history_handler() -> GetTelemetryHistoryQueryHandler:
    return GetTelemetryHistoryQueryHandler(
        read_repo=SqlAlchemyTelemetryReadRepository()
    )

def get_record_telemetry_handler_sync() -> RecordTelemetryCommandHandlerSync:
    return RecordTelemetryCommandHandlerSync(
        telemetry_repo=SqlAlchemyTelemetryRepository(),
        sensor_repo=SqlAlchemySensorRepository(),
        alerting_service=ConsoleAlertingService(threshold=80.0),
    )