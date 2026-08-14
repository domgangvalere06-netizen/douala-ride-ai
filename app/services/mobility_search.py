"""Unified location/route planning for every supported Douala location."""

from app.services.location_catalog import search as catalog_search


def search_locations(query: str, limit: int = 10):
    """Search the full local catalog; the map service can provide OSM fallback."""
    return catalog_search(query, limit=limit)


def build_trip_request(origin: dict, destination: dict, budget_xaf: int | None = None,
                       vehicle_type: str | None = None) -> dict:
    if not origin or not destination:
        raise ValueError("Origin and destination are required")
    if budget_xaf is not None and budget_xaf < 0:
        raise ValueError("Budget cannot be negative")
    if vehicle_type is not None and vehicle_type not in {"moto", "car"}:
        raise ValueError("vehicle_type must be moto or car")
    return {
        "origin": origin,
        "destination": destination,
        "budget_xaf": budget_xaf,
        "vehicle_type": vehicle_type,
    }
