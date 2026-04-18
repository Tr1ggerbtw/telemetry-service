from app.domain.validators import is_valid_email, is_valid_telemetry_value

def test_valid_email():
    assert is_valid_email("valid@gmail.com") is True

def test_email_no_domain():
    assert is_valid_email("blafsdl@") is False

def test_email_empty():
    assert is_valid_email("") is False

def test_email_no_at():
    assert is_valid_email("coolEmailButnoAt") is False

def test_valid_telemetry_value():
    assert is_valid_telemetry_value(100) is True

def test_negative_telemetry_value():
    assert is_valid_telemetry_value(-1) is False

def test_too_big_temeletry_value():
    assert is_valid_telemetry_value(101) is False

def test_NaN_telemetry_value():
    assert is_valid_telemetry_value("SQL") is False



