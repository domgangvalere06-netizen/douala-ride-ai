"""Trip lifecycle domain service.

All trip status transitions are validated here so API handlers and the AI
agent cannot arbitrarily mutate trip state.
"""

from enum import Enum


class TripStatus(str, Enum):
    REQUESTED = "REQUESTED"
    SEARCHING_DRIVER = "SEARCHING_DRIVER"
    DRIVER_ASSIGNED = "DRIVER_ASSIGNED"
    DRIVER_ACCEPTED = "DRIVER_ACCEPTED"
    DRIVER_ARRIVING = "DRIVER_ARRIVING"
    DRIVER_ARRIVED = "DRIVER_ARRIVED"
    TRIP_STARTED = "TRIP_STARTED"
    TRIP_COMPLETED = "TRIP_COMPLETED"
    CANCELLED = "CANCELLED"
    NO_DRIVER_FOUND = "NO_DRIVER_FOUND"
    PAYMENT_FAILED = "PAYMENT_FAILED"


ALLOWED_TRANSITIONS = {
    TripStatus.REQUESTED: {TripStatus.SEARCHING_DRIVER, TripStatus.CANCELLED},
    TripStatus.SEARCHING_DRIVER: {TripStatus.DRIVER_ASSIGNED, TripStatus.NO_DRIVER_FOUND, TripStatus.CANCELLED},
    TripStatus.DRIVER_ASSIGNED: {TripStatus.DRIVER_ACCEPTED, TripStatus.CANCELLED},
    TripStatus.DRIVER_ACCEPTED: {TripStatus.DRIVER_ARRIVING, TripStatus.CANCELLED},
    TripStatus.DRIVER_ARRIVING: {TripStatus.DRIVER_ARRIVED, TripStatus.CANCELLED},
    TripStatus.DRIVER_ARRIVED: {TripStatus.TRIP_STARTED, TripStatus.CANCELLED},
    TripStatus.TRIP_STARTED: {TripStatus.TRIP_COMPLETED},
    TripStatus.TRIP_COMPLETED: set(),
    TripStatus.CANCELLED: set(),
    TripStatus.NO_DRIVER_FOUND: set(),
    TripStatus.PAYMENT_FAILED: {TripStatus.CANCELLED},
}


class InvalidTripTransition(ValueError):
    pass


def can_transition(current: TripStatus | str, target: TripStatus | str) -> bool:
    current = TripStatus(current)
    target = TripStatus(target)
    return target in ALLOWED_TRANSITIONS[current]


def transition(current: TripStatus | str, target: TripStatus | str) -> TripStatus:
    current = TripStatus(current)
    target = TripStatus(target)
    if not can_transition(current, target):
        raise InvalidTripTransition(f"Cannot transition trip from {current.value} to {target.value}")
    return target
