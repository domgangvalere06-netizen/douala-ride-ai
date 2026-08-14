"""Database-backed driver discovery exposed as a controlled AI tool."""

from app import db
from app.models.driver import Driver
from app.models.driver_location import DriverLocation
from app.models.vehicle import Vehicle
from app.services.driver_matching import rank_drivers


def find_available_drivers(pickup_lat: float, pickup_lon: float, vehicle_type: str | None = None, max_distance_km: float = 10.0, limit: int = 10):
    if vehicle_type is not None and vehicle_type not in {"moto", "car"}:
        raise ValueError("vehicle_type must be moto or car")

    drivers = (
        db.session.query(Driver)
        .join(Vehicle, Vehicle.driver_id == Driver.id)
        .join(DriverLocation, DriverLocation.driver_id == Driver.id)
        .filter(
            Driver.is_online.is_(True),
            Driver.verification_status == "verified",
            Driver.safety_status == "clear",
            Vehicle.is_active.is_(True),
            Vehicle.verification_status == "verified",
        )
        .distinct()
        .all()
    )

    candidates = []
    for driver in drivers:
        vehicle = next((v for v in driver.vehicles if v.is_active and v.verification_status == "verified" and (vehicle_type is None or v.vehicle_type == vehicle_type)), None)
        location = max(driver.locations, key=lambda item: item.recorded_at, default=None)
        if not vehicle or not location:
            continue
        candidate = type("Candidate", (), {
            "id": driver.id,
            "rating": float(driver.rating),
            "latitude": float(location.latitude),
            "longitude": float(location.longitude),
            "vehicle_type": vehicle.vehicle_type,
            "is_online": driver.is_online,
            "is_available": True,
        })()
        candidate.vehicle_id = vehicle.id
        candidates.append(candidate)

    matches = rank_drivers(candidates, pickup_lat, pickup_lon, vehicle_type=vehicle_type, max_distance_km=max_distance_km)
    results = []
    for match in matches[: max(1, min(limit, 20))]:
        candidate = next(item for item in candidates if item.id == match.driver_id)
        results.append({
            "driver_id": match.driver_id,
            "vehicle_id": candidate.vehicle_id,
            "vehicle_type": match.vehicle_type,
            "rating": match.rating,
            "pickup_distance_km": match.distance_km,
            "match_score": match.score,
        })
    return results
