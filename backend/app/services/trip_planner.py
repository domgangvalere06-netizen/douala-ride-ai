from .fare_service import FareService
from .location_service import LocationService
from .map_service import MapService


class TripPlanner:
    def __init__(self):
        self.location = LocationService()
        self.maps = MapService()
        self.fares = FareService()

    def plan(self, pickup: str, destination: str, vehicle_type: str = "moto") -> dict:
        origin = self.location.geocode(pickup)
        target = self.location.geocode(destination)
        route = self.maps.route(
            origin["longitude"], origin["latitude"],
            target["longitude"], target["latitude"],
        )
        if not route.get("routes"):
            raise ValueError("No route found")

        best = route["routes"][0]
        distance_km = best["distance"] / 1000
        duration_minutes = best["duration"] / 60
        fare = self.fares.estimate(distance_km, duration_minutes, vehicle_type)
        return {
            "pickup": origin,
            "destination": target,
            "route": {
                "distance_km": round(distance_km, 2),
                "duration_minutes": round(duration_minutes),
            },
            "fare": fare,
        }
