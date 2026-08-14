"""OpenStreetMap Nominatim geocoding integration."""

from typing import Any

import requests


class GeocodingError(RuntimeError):
    pass


class NominatimClient:
    def __init__(self, base_url: str = "https://nominatim.openstreetmap.org", timeout: int = 8):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def search(self, query: str, limit: int = 5) -> list[dict[str, Any]]:
        if not query or not query.strip():
            return []
        try:
            response = requests.get(
                f"{self.base_url}/search",
                params={
                    "q": query,
                    "format": "jsonv2",
                    "limit": max(1, min(limit, 10)),
                    "countrycodes": "cm",
                    "addressdetails": 1,
                },
                headers={"User-Agent": "DoualaRide/1.0 (prototype)"},
                timeout=self.timeout,
            )
            response.raise_for_status()
            payload = response.json()
        except (requests.RequestException, ValueError) as exc:
            raise GeocodingError("Location search service is unavailable") from exc

        return [
            {
                "display_name": item.get("display_name"),
                "latitude": float(item["lat"]),
                "longitude": float(item["lon"]),
                "type": item.get("type"),
                "address": item.get("address", {}),
            }
            for item in payload
            if item.get("lat") is not None and item.get("lon") is not None
        ]
