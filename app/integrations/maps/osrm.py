"""OSRM routing integration.

The public OSRM endpoint is useful for the prototype. Production should use a
managed or self-hosted routing service with appropriate reliability controls.
"""

from typing import Any

import requests


class RoutingError(RuntimeError):
    pass


class OSRMClient:
    def __init__(self, base_url: str = "https://router.project-osrm.org", timeout: int = 8):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def route(self, origin_lat: float, origin_lon: float, destination_lat: float, destination_lon: float) -> dict[str, Any]:
        url = (
            f"{self.base_url}/route/v1/driving/"
            f"{origin_lon},{origin_lat};{destination_lon},{destination_lat}"
        )
        try:
            response = requests.get(
                url,
                params={"overview": "full", "geometries": "geojson", "steps": "false"},
                timeout=self.timeout,
            )
            response.raise_for_status()
            payload = response.json()
        except (requests.RequestException, ValueError) as exc:
            raise RoutingError("Routing service is unavailable") from exc

        if payload.get("code") != "Ok" or not payload.get("routes"):
            raise RoutingError("No route found")

        route = payload["routes"][0]
        return {
            "distance_km": round(route["distance"] / 1000, 2),
            "duration_minutes": round(route["duration"] / 60),
            "geometry": route.get("geometry"),
        }
