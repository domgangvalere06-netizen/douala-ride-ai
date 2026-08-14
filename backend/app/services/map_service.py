import requests
from flask import current_app


class MapService:
    def route(self, start_lon: float, start_lat: float, end_lon: float, end_lat: float) -> dict:
        base_url = current_app.config["OSRM_BASE_URL"].rstrip("/")
        url = f"{base_url}/route/v1/driving/{start_lon},{start_lat};{end_lon},{end_lat}"
        response = requests.get(url, params={"overview": "false"}, timeout=15)
        response.raise_for_status()
        return response.json()
