from app.application.commands import RegisterUserCommand, CreateLocationCommand, AddSensorCommand, RecordTelemetryCommand, LoginUserCommand, DeleteSensorCommand
from app.application.queries import GetTelemetryHistoryQuery
from app.domain.repositories import IUserRepository, ILocationRepository, ISensorRepository, ITelemetryRepository
from app.domain.services import IAlertingService
from app.application.read_model import TelemetryReadModel
from app.application.read_repository import ITelemetryReadRepository
from app.domain.entities import User, Email, Location, Sensor, MacAddress
from app.domain.exceptions import DomainError, AccessDeniedError
from app.domain.factories import TelemetryFactory
from werkzeug.security import generate_password_hash, check_password_hash


class RegisterUserCommandHandler:
    def __init__(self, user_repo: IUserRepository):
        self._user_repo = user_repo

    def handle(self, command: RegisterUserCommand) -> None:
        email = Email(command.email)
        if self._user_repo.get_by_email(email) is not None:
            raise DomainError(f"User with email {command.email} already exists")
        self._user_repo.save(User(email=email, password_hash=generate_password_hash(command.password)))


class LoginCommandHandler:
    def __init__(self, user_repo: IUserRepository):
        self._user_repo = user_repo

    def handle(self, command: LoginUserCommand) -> User:
        email = Email(command.email)
        user = self._user_repo.get_by_email(email)
        if user is None or not check_password_hash(user.password_hash, command.password):
            raise DomainError("Invalid credentials")
        return user.user_id


class CreateLocationCommandHandler:
    def __init__(self, location_repo: ILocationRepository):
        self._location_repo = location_repo

    def handle(self, command: CreateLocationCommand) -> None:
        self._location_repo.save(Location(name=command.name, user_id=command.user_id))


class AddSensorCommandHandler:
    def __init__(self, sensor_repo: ISensorRepository, location_repo: ILocationRepository):
        self._sensor_repo = sensor_repo
        self._location_repo = location_repo

    def handle(self, command: AddSensorCommand) -> None:
        location = self._location_repo.get_by_id(command.location_id)
        if location is None or location.user_id != command.user_id:
            raise AccessDeniedError("Location not found or access denied")
        mac = MacAddress(command.mac_address)
        if self._sensor_repo.get_by_mac(mac) is not None:
            raise DomainError(f"Sensor with MAC {command.mac_address} already exists")
        self._sensor_repo.save(Sensor(mac_address=mac, location_id=command.location_id))


class DeleteSensorCommandHandler:
    def __init__(self, sensor_repo: ISensorRepository, location_repo: ILocationRepository):
        self._sensor_repo = sensor_repo
        self._location_repo = location_repo

    def handle(self, command: DeleteSensorCommand) -> None:
        sensor = self._sensor_repo.get_by_id(command.sensor_id)
        if sensor is None:
            raise DomainError("Sensor not found")
        location = self._location_repo.get_by_id(sensor.location_id)
        if location is None or location.user_id != command.user_id:
            raise AccessDeniedError("Access denied")
        self._sensor_repo.delete(sensor)


class RecordTelemetryCommandHandler:
    def __init__(self, telemetry_repo: ITelemetryRepository, sensor_repo: ISensorRepository, alerting_service: IAlertingService):
        self._telemetry_repo = telemetry_repo
        self._sensor_repo = sensor_repo
        self._alerting_service = alerting_service
        
    def handle(self, command: RecordTelemetryCommand) -> None:
        if self._sensor_repo.get_by_id(command.sensor_id) is None:
            raise DomainError("Sensor not found")
        
        self._telemetry_repo.save(TelemetryFactory.create(sensor_id=command.sensor_id, value=command.value))

        self._alerting_service.check_and_alert(
            sensor_id=command.sensor_id, 
            value=command.value
        )


class GetTelemetryHistoryQueryHandler:
    def __init__(self, read_repo: ITelemetryReadRepository):
        self._read_repo = read_repo

    def handle(self, query: GetTelemetryHistoryQuery) -> list[TelemetryReadModel]:
        return self._read_repo.get_history(query.mac_address, query.user_id, query.limit)