"""Realtime tracking domain helpers."""

from dataclasses import dataclass
from datetime import datetime, timezone
from math import atan2, cos, radians, sin, sqrt


@dataclass(frozen=True)
class LocationPoint:
    latitude: float
    longitude: float
    recorded_at: datetime


def distance_km(a: LocationPoint, b: LocationPoint) -> float:
    radius = 6371.0
    d_lat = radians(b.latitude - a.latitude)
    d_lon = radians(b.longitude - a.longitude)
    x = sin(d_lat / 2) ** 2 + cos(radians(a.latitude)) * cos(radians(b.latitude)) * sin(d_lon / 2) ** 2
    return 2 * radius * atan2(sqrt(x), sqrt(1 - x))


def normalize_location(latitude: float, longitude: float) -> LocationPoint:
    if not -90 <= latitude <= 90:
        raise ValueError("Invalid latitude")
    if not -180 <= longitude <= 180:
        raise ValueError("Invalid longitude")
    return LocationPoint(latitude, longitude, datetime.now(timezone.utc))
