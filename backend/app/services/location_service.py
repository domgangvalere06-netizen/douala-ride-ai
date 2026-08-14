import requests
from flask import current_app


class LocationService:
    """Resolve a human place name to coordinates using public Nominatim."""

    def geocode(self, place: str) -> dict:
        response = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={"q": place, "format": "json", "limit": 1, "countrycodes": "cm"},
            headers={"User-Agent": "DoualaRide/1.0"},
            timeout=15,
        )
        response.raise_for_status()
        results = response.json()
        if not results:
            raise ValueError(f"Location not found: {place}")
        item = results[0]
        return {
            "label": item.get("display_name", place),
            "latitude": float(item["lat"]),
            "longitude": float(item["lon"]),
        }
