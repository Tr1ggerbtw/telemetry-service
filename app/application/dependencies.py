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
    GetTelemetryHistoryQueryHandler
)
from app.infrastructure.services import ConsoleAlertingService

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
        alerting_service=ConsoleAlertingService(threshold=80.0)
    )

def get_telemetry_history_handler() -> GetTelemetryHistoryQueryHandler:
    return GetTelemetryHistoryQueryHandler(
        read_repo=SqlAlchemyTelemetryReadRepository()
    )