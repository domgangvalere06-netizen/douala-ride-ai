"""Application service combining Douala catalog search, geocoding and routing."""

from app.integrations.maps.geocoding import NominatimClient
from app.integrations.maps.osrm import OSRMClient
from app.services.location_service import LocationService


class MapService:
    def __init__(self, geocoder=None, router=None, location_service=None):
        self.geocoder = geocoder or NominatimClient()
        self.router = router or OSRMClient()
        self.location_service = location_service or LocationService(self.geocoder)

    def search_location(self, query: str, limit: int = 5):
        return self.location_service.search(query, limit=limit)

    def calculate_route(self, origin: tuple[float, float], destination: tuple[float, float]):
        return self.router.route(
            origin_lat=origin[0],
            origin_lon=origin[1],
            destination_lat=destination[0],
            destination_lon=destination[1],
        )

    def plan_route(self, origin: tuple[float, float], destination: tuple[float, float]):
        route = self.calculate_route(origin, destination)
        return {
            "origin": {"latitude": origin[0], "longitude": origin[1]},
            "destination": {"latitude": destination[0], "longitude": destination[1]},
            **route,
        }
