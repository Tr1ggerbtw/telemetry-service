import re

def is_valid_email(email):
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_pattern, email) is not None

def is_valid_telemetry_value(value):
    if isinstance(value, (int, float)) is False:
        return False
    return 0 <= value <= 100

def is_valid_mac_address(mac_address):
    mac_address_pattern = "^(?:[0-9A-Fa-f]{2}[:-]){5}(?:[0-9A-Fa-f]{2})$"
    return re.match(mac_address_pattern, mac_address) is not None