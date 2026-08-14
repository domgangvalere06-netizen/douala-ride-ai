"""Universal route and fare planning for arbitrary pickup/destination pairs."""

from app.services.map_service import MapService
from app.services.fare_service import estimate_fare


class RouteFareService:
    def __init__(self, map_service=None):
        self.map_service = map_service or MapService()

    def plan(self, origin: dict, destination: dict, vehicle_type: str | None = None,
             budget_xaf: int | None = None) -> dict:
        if not isinstance(origin, dict) or not isinstance(destination, dict):
            raise ValueError("Origin and destination are required")
        if vehicle_type and vehicle_type not in {"moto", "car"}:
            raise ValueError("vehicle_type must be moto or car")
        if budget_xaf is not None and budget_xaf < 0:
            raise ValueError("Budget cannot be negative")

        try:
            origin_coords = (float(origin["latitude"]), float(origin["longitude"]))
            destination_coords = (float(destination["latitude"]), float(destination["longitude"]))
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError("Origin and destination need valid latitude and longitude") from exc

        route = self.map_service.plan_route(origin_coords, destination_coords)
        distance_km = float(route.get("distance_km", 0))
        duration_minutes = int(round(float(route.get("duration_minutes", 0))))

        fares = {}
        for kind in ("moto", "car"):
            estimate = estimate_fare(kind, distance_km, duration_minutes)
            fares[kind] = {
                "estimated_fare": estimate.estimated_fare,
                "currency": estimate.currency,
                "base_fare": estimate.base_fare,
                "distance_fare": estimate.distance_fare,
                "time_fare": estimate.time_fare,
                "within_budget": budget_xaf is None or estimate.estimated_fare <= budget_xaf,
            }

        return {
            "origin": origin,
            "destination": destination,
            "route": route,
            "distance_km": round(distance_km, 2),
            "duration_minutes": duration_minutes,
            "fares": fares,
            "selected_vehicle_type": vehicle_type,
            "selected_fare_xaf": fares.get(vehicle_type, {}).get("estimated_fare") if vehicle_type else None,
            "budget_xaf": budget_xaf,
            "affordable_vehicle_types": [k for k, v in fares.items() if v["within_budget"]],
        }
