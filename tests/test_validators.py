from app.validators import is_valid_email, is_valid_telemetry_value

def test_valid_email():
    assert is_valid_email("valid@gmail.com") is True

def test_email_no_domain():
    assert is_valid_email("blafsdl@") is False

def test_email_empty():
    assert is_valid_email("") is False

def test_email_no_at():
    assert is_valid_email("coolEmailButnoAt") is False



