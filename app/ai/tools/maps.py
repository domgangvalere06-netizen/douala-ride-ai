"""Map tools exposed to the AI agent."""

from app.services.map_service import MapService


class MapTools:
    def __init__(self, map_service=None):
        self.map_service = map_service or MapService()

    def search_location(self, query: str, limit: int = 5):
        return self.map_service.search_location(query, limit=limit)

    def calculate_route(self, origin_lat: float, origin_lon: float, destination_lat: float, destination_lon: float):
        return self.map_service.calculate_route(
            (origin_lat, origin_lon),
            (destination_lat, destination_lon),
        )
