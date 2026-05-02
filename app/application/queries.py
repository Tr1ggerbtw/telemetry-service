from dataclasses import dataclass

@dataclass(frozen=True)
class GetTelemetryHistoryQuery:
    mac_address: str
    user_id: int
    limit: int = 50

    