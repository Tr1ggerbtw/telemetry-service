class DomainError(Exception):
    pass

class InvalidEmailError(DomainError):
    pass

class InvalidTelemetryValueError(DomainError):
    pass