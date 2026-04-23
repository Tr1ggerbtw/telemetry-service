from app.infrastructure.repositories import (
    SqlAlchemyUserRepository,
    SqlAlchemyLocationRepository,
    SqlAlchemySensorRepository,
    SqlAlchemyTelemetryRepository
)
from app.application.use_cases import (
    RegisterUserUseCase,
    LoginUseCase,
    CreateLocationUseCase,
    AddSensorUseCase,
    DeleteSensorUseCase,
    RecordTelemetryUseCase,
    GetTelemetryHistoryUseCase
)


def get_register_use_case() -> RegisterUserUseCase:
    return RegisterUserUseCase(
        user_repo=SqlAlchemyUserRepository()
    )


def get_login_use_case() -> LoginUseCase:
    return LoginUseCase(
        user_repo=SqlAlchemyUserRepository()
    )


def get_create_location_use_case() -> CreateLocationUseCase:
    return CreateLocationUseCase(
        location_repo=SqlAlchemyLocationRepository()
    )


def get_add_sensor_use_case() -> AddSensorUseCase:
    return AddSensorUseCase(
        sensor_repo=SqlAlchemySensorRepository(),
        location_repo=SqlAlchemyLocationRepository()
    )


def get_delete_sensor_use_case() -> DeleteSensorUseCase:
    return DeleteSensorUseCase(
        sensor_repo=SqlAlchemySensorRepository(),
        location_repo=SqlAlchemyLocationRepository()
    )


def get_record_telemetry_use_case() -> RecordTelemetryUseCase:
    return RecordTelemetryUseCase(
        telemetry_repo=SqlAlchemyTelemetryRepository(),
        sensor_repo=SqlAlchemySensorRepository()
    )


def get_telemetry_history_use_case() -> GetTelemetryHistoryUseCase:
    return GetTelemetryHistoryUseCase(
        sensor_repo=SqlAlchemySensorRepository(),
        location_repo=SqlAlchemyLocationRepository(),
        telemetry_repo=SqlAlchemyTelemetryRepository()
    )