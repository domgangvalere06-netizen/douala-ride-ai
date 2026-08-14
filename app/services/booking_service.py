"""Booking orchestration for the mobility core."""

from dataclasses import dataclass
from typing import Any

from app.services.trip_service import TripStatus, transition


@dataclass(frozen=True)
class BookingDecision:
    driver_id: int
    estimated_fare: int
    currency: str
    vehicle_type: str


def validate_booking_confirmation(
    trip: Any,
    driver_id: int,
    estimated_fare: int,
    vehicle_type: str,
) -> BookingDecision:
    """Validate the minimum information required before creating a booking.

    Persistence is intentionally outside this function. A route/API handler or
    application service should open the transaction and save the booking/trip.
    """
    current = TripStatus(getattr(trip, "status", TripStatus.REQUESTED))
    if current != TripStatus.SEARCHING_DRIVER:
        raise ValueError("A trip must be searching for a driver before assignment")
    if driver_id <= 0:
        raise ValueError("A valid driver is required")
    if estimated_fare <= 0:
        raise ValueError("Estimated fare must be positive")
    if vehicle_type not in {"moto", "car"}:
        raise ValueError("Vehicle type must be moto or car")

    transition(current, TripStatus.DRIVER_ASSIGNED)
    return BookingDecision(
        driver_id=driver_id,
        estimated_fare=estimated_fare,
        currency="XAF",
        vehicle_type=vehicle_type,
    )
