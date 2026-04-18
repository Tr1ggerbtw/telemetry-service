from app.domain.repositories import IUserRepository, ILocationRepository, ISensorRepository, ITelemetryRepository
from app.domain.entities import User, Email, Location, Sensor, MacAddress, Telemetry
from app.infrastructure.orm_models import UserModel, LocationModel, SensorModel, TelemetryModel
from app.db import db

class SqlAlchemyUserRepository(IUserRepository):
    def save(self, user: User) -> None:
        orm_user = UserModel(
            email=user.email.value, 
            password=user.password_hash
        )
        db.session.add(orm_user)
        db.session.commit()
        user.user_id = orm_user.user_id

    def get_by_email(self, email: Email) -> User | None:
        orm_user = UserModel.query.filter_by(email=email.value).first()
        if orm_user is None:
            return None
        return User(
            user_id=orm_user.user_id,
            email=Email(orm_user.email),
            password_hash=orm_user.password
        )

class SqlAlchemyLocationRepository(ILocationRepository):
    def save(self, location: Location) -> None:
        orm_location = LocationModel(
            name=location.name,
            user_id=location.user_id
        )
        db.session.add(orm_location)
        db.session.commit()
        location.location_id = orm_location.location_id
        
    def get_by_id(self, location_id: int) -> Location | None:
        orm_location = LocationModel.query.filter_by(location_id=location_id).first()
        if orm_location is None:
            return None
        return Location(
            location_id=orm_location.location_id,
            name=orm_location.name,
            user_id=orm_location.user_id
        )

class SqlAlchemySensorRepository(ISensorRepository):
    def save(self, sensor: Sensor) -> None:
        orm_sensor = SensorModel(
            mac_address=sensor.mac_address.value,
            location_id=sensor.location_id
        )
        db.session.add(orm_sensor)
        db.session.commit()
        sensor.sensor_id = orm_sensor.sensor_id

    def get_by_mac(self, mac: MacAddress) -> Sensor | None:
        orm_sensor = SensorModel.query.filter_by(mac_address=mac.value).first()
        if orm_sensor is None:
            return None
        return Sensor(
            sensor_id=orm_sensor.sensor_id,
            mac_address=MacAddress(orm_sensor.mac_address),
            location_id=orm_sensor.location_id
        )

    def delete(self, sensor: Sensor) -> None:
        orm_sensor = SensorModel.query.filter_by(sensor_id=sensor.sensor_id).first()
        if orm_sensor:
            db.session.delete(orm_sensor)
            db.session.commit()

class SqlAlchemyTelemetryRepository(ITelemetryRepository):
    def save(self, telemetry: Telemetry) -> None:
        orm_telemetry = TelemetryModel(
            sensor_id=telemetry.sensor_id,
            timestamp=telemetry.timestamp,
            value=telemetry.value
        )
        db.session.add(orm_telemetry)
        db.session.commit()
        telemetry.telemetry_id = orm_telemetry.telemetry_id