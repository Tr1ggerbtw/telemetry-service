from app.application.dtos import RegisterUserDTO, CreateLocationDTO, AddSensorDTO, RecordTelemetryDTO, LoginUserDTO, DeleteSensorDTO, GetTelemetryHistoryDTO
from app.domain.repositories import IUserRepository, ILocationRepository, ISensorRepository, ITelemetryRepository
from app.domain.entities import User, Email, Location, Sensor, MacAddress
from app.domain.exceptions import DomainError, AccessDeniedError
from app.domain.factories import TelemetryFactory 
from werkzeug.security import generate_password_hash, check_password_hash

class RegisterUserUseCase:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    def execute(self, dto: RegisterUserDTO) -> None:
        target_email = Email(dto.email)

        if self.user_repo.get_by_email(target_email) is not None:
            raise DomainError(f"User with email {dto.email} already exists")

        hashed_password = generate_password_hash(dto.password)

        new_user = User(email=target_email, password_hash=hashed_password)

        self.user_repo.save(new_user)


class LoginUseCase:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    def execute(self, dto: LoginUserDTO) -> User:
        target_email = Email(dto.email)
        user = self.user_repo.get_by_email(target_email)
        if user is None:
            raise DomainError("Invalid credentials")
        if not check_password_hash(user.password_hash, dto.password):
            raise DomainError("Invalid credentials")
        return user


class CreateLocationUseCase:
    def __init__(self, location_repo: ILocationRepository):
        self.location_repo = location_repo

    def execute(self, dto: CreateLocationDTO) -> None:
        new_location = Location(name=dto.name, user_id=dto.user_id)
        self.location_repo.save(new_location)



class AddSensorUseCase:
    def __init__(self, sensor_repo: ISensorRepository, location_repo: ILocationRepository):
        self.sensor_repo = sensor_repo
        self.location_repo = location_repo

    def execute(self, dto: AddSensorDTO) -> None:
        location = self.location_repo.get_by_id(dto.location_id)
        if location is None or location.user_id != dto.user_id:
            raise AccessDeniedError("Location not found or access denied")

        mac = MacAddress(dto.mac_address)
        if self.sensor_repo.get_by_mac(mac) is not None:
            raise DomainError(f"Sensor with MAC {dto.mac_address} already exists")

        new_sensor = Sensor(mac_address=mac, location_id=dto.location_id)
        self.sensor_repo.save(new_sensor)


class DeleteSensorUseCase:
    def __init__(self, sensor_repo: ISensorRepository, location_repo: ILocationRepository):
        self.sensor_repo = sensor_repo
        self.location_repo = location_repo

    def execute(self, dto: DeleteSensorDTO) -> None:
        sensor = self.sensor_repo.get_by_id(dto.sensor_id)
        if sensor is None:
            raise DomainError("Sensor not found")

        location = self.location_repo.get_by_id(sensor.location_id)
        if location is None or location.user_id != dto.user_id:
            raise AccessDeniedError("Access denied")

        self.sensor_repo.delete(sensor)


class RecordTelemetryUseCase:
    def __init__(self, telemetry_repo: ITelemetryRepository, sensor_repo: ISensorRepository):
        self.telemetry_repo = telemetry_repo
        self.sensor_repo = sensor_repo

    def execute(self, dto: RecordTelemetryDTO) -> None:
        sensor = self.sensor_repo.get_by_id(dto.sensor_id)
        if sensor is None:
            raise DomainError("Sensor not found")

        new_telemetry = TelemetryFactory.create(
            sensor_id=dto.sensor_id,
            value=dto.value
        )
        self.telemetry_repo.save(new_telemetry)

class GetTelemetryHistoryUseCase:
    def __init__(self, sensor_repo: ISensorRepository, location_repo: ILocationRepository, telemetry_repo: ITelemetryRepository):
        self.sensor_repo = sensor_repo
        self.location_repo = location_repo
        self.telemetry_repo = telemetry_repo

    def execute(self, dto: GetTelemetryHistoryDTO) -> list:
        mac = MacAddress(dto.mac_address)
        sensor = self.sensor_repo.get_by_mac(mac)
        if sensor is None:
            raise DomainError("Sensor not found")

        location = self.location_repo.get_by_id(sensor.location_id)
        if location is None or location.user_id != dto.user_id:
            raise DomainError("Access denied")

        return self.telemetry_repo.get_by_sensor_id(sensor.sensor_id, dto.limit)