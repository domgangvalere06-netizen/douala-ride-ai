"""Controlled map and trip-planning tools exposed to the AI agent."""

from app.services.map_service import MapService
from app.services.route_fare_service import RouteFareService


class MapTools:
    def __init__(self, map_service=None, trip_planner=None):
        self.map_service = map_service or MapService()
        self.trip_planner = trip_planner or RouteFareService(self.map_service)

    def search_location(self, query: str, limit: int = 5):
        return self.map_service.search_location(query, limit=limit)

    def calculate_route(self, origin_lat: float, origin_lon: float,
                        destination_lat: float, destination_lon: float):
        return self.map_service.calculate_route(
            (origin_lat, origin_lon),
            (destination_lat, destination_lon),
        )

    def plan_trip(self, origin: dict, destination: dict,
                  budget_xaf: int | None = None,
                  vehicle_type: str | None = None):
        """Plan any pickup-to-destination journey through the backend services."""
        return self.trip_planner.plan(
            origin=origin,
            destination=destination,
            budget_xaf=budget_xaf,
            vehicle_type=vehicle_type,
        )
