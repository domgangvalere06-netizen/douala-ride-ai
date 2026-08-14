"""Fare tool exposed to the AI agent."""

from dataclasses import asdict

from app.services.fare_service import estimate_fare


def estimate_trip_fare(vehicle_type: str, distance_km: float, duration_minutes: int):
    estimate = estimate_fare(vehicle_type, distance_km, duration_minutes)
    return asdict(estimate)
