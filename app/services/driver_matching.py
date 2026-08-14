"""Driver matching domain service.

This module defines the deterministic ranking contract used by the booking
engine. The actual database query is injected so matching remains testable and
does not allow the AI to access persistence directly.
"""

from dataclasses import dataclass
from math import atan2, cos, radians, sin, sqrt
from typing import Iterable, Protocol


class DriverCandidate(Protocol):
    id: int
    rating: float
    latitude: float
    longitude: float
    vehicle_type: str
    is_online: bool
    is_available: bool


@dataclass(frozen=True)
class DriverMatch:
    driver_id: int
    score: float
    distance_km: float
    rating: float
    vehicle_type: str


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    radius = 6371.0
    d_lat = radians(lat2 - lat1)
    d_lon = radians(lon2 - lon1)
    a = sin(d_lat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(d_lon / 2) ** 2
    return 2 * radius * atan2(sqrt(a), sqrt(1 - a))


def rank_drivers(
    candidates: Iterable[DriverCandidate],
    pickup_lat: float,
    pickup_lon: float,
    vehicle_type: str | None = None,
    max_distance_km: float = 10.0,
) -> list[DriverMatch]:
    matches: list[DriverMatch] = []
    for driver in candidates:
        if not driver.is_online or not driver.is_available:
            continue
        if vehicle_type and driver.vehicle_type != vehicle_type:
            continue

        distance = haversine_km(pickup_lat, pickup_lon, driver.latitude, driver.longitude)
        if distance > max_distance_km:
            continue

        # Lower distance is better; rating contributes positively.
        proximity_score = max(0.0, 1.0 - distance / max_distance_km)
        rating_score = max(0.0, min(float(driver.rating) / 5.0, 1.0))
        score = round((proximity_score * 0.7) + (rating_score * 0.3), 4)

        matches.append(
            DriverMatch(
                driver_id=driver.id,
                score=score,
                distance_km=round(distance, 3),
                rating=float(driver.rating),
                vehicle_type=driver.vehicle_type,
            )
        )

    return sorted(matches, key=lambda item: (-item.score, item.distance_km))
