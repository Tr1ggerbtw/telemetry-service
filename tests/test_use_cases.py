import pytest
from unittest.mock import MagicMock
from app.application.use_cases import RegisterUserUseCase, AddSensorUseCase
from app.application.dtos import RegisterUserDTO, AddSensorDTO
from app.domain.entities import Location
from app.domain.exceptions import DomainError

def test_register_user_success():
    user_repo = MagicMock()
    user_repo.get_by_email.return_value = None # user doesn't exist

    use_case = RegisterUserUseCase(user_repo)
    use_case.execute(RegisterUserDTO(email="test@gmail.com", password="123456"))

    user_repo.save.assert_called_once() 

def test_register_user_duplicate_email():
    user_repo = MagicMock()
    user_repo.get_by_email.return_value = MagicMock()  # user exists

    use_case = RegisterUserUseCase(user_repo)
    with pytest.raises(DomainError):
        use_case.execute(RegisterUserDTO(email="test@gmail.com", password="123456"))

def test_add_sensor_forbidden_location():
    sensor_repo = MagicMock()
    location_repo = MagicMock()
    location_repo.get_by_id.return_value = Location(
        location_id=1, name="home", user_id=999 
    )

    use_case = AddSensorUseCase(sensor_repo, location_repo)
    with pytest.raises(DomainError):
        use_case.execute(AddSensorDTO(
            mac_address="AA:BB:CC:DD:EE:FF",
            location_id=1,
            user_id=1 # id doesn't match
        ))

def test_add_sensor_location_not_found():
    sensor_repo = MagicMock()
    location_repo = MagicMock()
    location_repo.get_by_id.return_value = None

    use_case = AddSensorUseCase(sensor_repo, location_repo)
    with pytest.raises(DomainError):
        use_case.execute(AddSensorDTO(
            mac_address="AA:BB:CC:DD:EE:FF",
            location_id=1,
            user_id=1
        ))