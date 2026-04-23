import pytest
from app.domain.entities import Email, MacAddress
from app.domain.factories import TelemetryFactory
from app.domain.exceptions import InvalidEmailError, InvalidMacAddressError, InvalidTelemetryValueError

def test_valid_email_creates_object():
    email = Email("test@gmail.com")
    assert email.value == "test@gmail.com"

def test_invalid_email_raises_exception():
    with pytest.raises(InvalidEmailError):
        Email("notanemail")

def test_valid_mac_creates_object():
    mac = MacAddress("AA:BB:CC:DD:EE:FF")
    assert mac.value == "AA:BB:CC:DD:EE:FF"

def test_invalid_mac_raises_exception():
    with pytest.raises(InvalidMacAddressError):
        MacAddress("not-a-mac")

def test_telemetry_factory_creates_object():
    telemetry = TelemetryFactory.create(sensor_id=1, value=50.0)
    assert telemetry.sensor_id == 1
    assert telemetry.value == 50.0
    assert telemetry.timestamp is not None

def test_telemetry_factory_invalid_value():
    with pytest.raises(InvalidTelemetryValueError):
        TelemetryFactory.create(sensor_id=1, value=5234809)

def test_telemetry_factory_negative_value():
    with pytest.raises(InvalidTelemetryValueError):
        TelemetryFactory.create(sensor_id=1, value=-1)