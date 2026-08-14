"""Location-independent route and fare orchestration.

The same pipeline is used for every supported pickup/destination pair.
External routing is delegated to MapService; pricing is centralized here so
clients never invent the final fare.
"""

from app.services.map_service import MapService


class RouteFareService:
    def __init__(self, map_service=None):
        self.map_service = map_service or MapService()

    def plan(self, origin: dict, destination: dict, vehicle_type: str | None = None,
             budget_xaf: int | None = None) -> dict:
        if not origin or not destination:
            raise ValueError("Origin and destination are required")
        if vehicle_type and vehicle_type not in {"moto", "car"}:
            raise ValueError("vehicle_type must be moto or car")
        if budget_xaf is not None and budget_xaf < 0:
            raise ValueError("Budget cannot be negative")

        route = self.map_service.get_route(origin, destination)
        distance_km = float(route.get("distance_km", 0))
        duration_min = int(round(float(route.get("duration_min", 0))))

        # Centralized prototype pricing rules in XAF. Replace rates with the
        # persisted pricing configuration before production launch.
        options = {
            "moto": max(500, round(500 + distance_km * 250 / 100) * 100),
            "car": max(1000, round(1000 + distance_km * 450 / 100) * 100),
        }
        selected = options.get(vehicle_type) if vehicle_type else None
        affordable = [kind for kind, fare in options.items() if budget_xaf is None or fare <= budget_xaf]

        return {
            "origin": origin,
            "destination": destination,
            "distance_km": round(distance_km, 2),
            "duration_min": duration_min,
            "fares_xaf": options,
            "selected_vehicle_type": vehicle_type,
            "selected_fare_xaf": selected,
            "budget_xaf": budget_xaf,
            "affordable_vehicle_types": affordable,
        }
