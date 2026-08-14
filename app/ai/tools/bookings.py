"""Booking tool exposed to the AI agent.

This tool deliberately creates a pending booking and moves the trip into
SEARCHING_DRIVER. It does not claim payment success or activate a trip.
"""

from app import db
from app.models.booking import Booking
from app.models.trip import Trip


def create_booking(
    passenger_id: int,
    pickup_address: str,
    pickup_latitude: float,
    pickup_longitude: float,
    destination_address: str,
    destination_latitude: float,
    destination_longitude: float,
    vehicle_type: str,
    estimated_fare: int,
    distance_km: float,
    estimated_duration_minutes: int,
    confirmed: bool = False,
):
    if not confirmed:
        raise ValueError("Passenger confirmation is required before creating a booking")
    if vehicle_type not in {"moto", "car"}:
        raise ValueError("vehicle_type must be moto or car")
    if passenger_id <= 0 or estimated_fare <= 0:
        raise ValueError("Invalid passenger or fare")

    trip = Trip(
        passenger_id=passenger_id,
        pickup_address=pickup_address,
        pickup_latitude=pickup_latitude,
        pickup_longitude=pickup_longitude,
        destination_address=destination_address,
        destination_latitude=destination_latitude,
        destination_longitude=destination_longitude,
        vehicle_type=vehicle_type,
        estimated_fare=estimated_fare,
        distance_km=distance_km,
        estimated_duration_minutes=estimated_duration_minutes,
        status="REQUESTED",
    )
    trip.transition_to("SEARCHING_DRIVER")
    db.session.add(trip)
    db.session.flush()

    booking = Booking(trip_id=trip.id, passenger_id=passenger_id, status="PENDING")
    db.session.add(booking)
    db.session.commit()

    return {
        "booking_id": booking.id,
        "booking_reference": booking.reference,
        "trip_id": trip.id,
        "status": trip.status,
        "payment_required": True,
        "message": "Booking created and searching for a driver. Payment must be confirmed before trip activation.",
    }
