"""Safety rules for active trips."""

from dataclasses import dataclass


@dataclass(frozen=True)
class SafetyEvent:
    trip_id: int
    event_type: str
    severity: str
    description: str


ALLOWED_EVENTS = {
    "SOS": "CRITICAL",
    "ROUTE_DEVIATION": "HIGH",
    "TRIP_SHARED": "INFO",
    "SAFETY_REPORT": "MEDIUM",
}


def create_safety_event(trip_id: int, event_type: str, description: str = "") -> SafetyEvent:
    if trip_id <= 0:
        raise ValueError("trip_id must be positive")
    severity = ALLOWED_EVENTS.get(event_type)
    if severity is None:
        raise ValueError("Unsupported safety event")
    return SafetyEvent(trip_id, event_type, severity, description[:1000])
