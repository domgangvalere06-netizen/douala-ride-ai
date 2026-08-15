from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from ..services.fare_service import FareService
from ..services.map_service import MapService

estimates_bp = Blueprint("estimates", __name__)


def _coordinate(point, name):
    if not isinstance(point, dict):
        raise ValueError(f"{name} must contain lat and lng")
    try:
        return float(point["lat"]), float(point["lng"])
    except (KeyError, TypeError, ValueError):
        raise ValueError(f"{name} must contain numeric lat and lng")


@estimates_bp.post("/estimate")
@jwt_required()
def estimate_trip():
    data = request.get_json() or {}
    try:
        start_lat, start_lon = _coordinate(data.get("pickup"), "pickup")
        end_lat, end_lon = _coordinate(data.get("destination"), "destination")
        vehicle_type = str(data.get("vehicle_type", "moto")).lower()
        route = MapService().route(start_lon, start_lat, end_lon, end_lat)
        if route.get("code") != "Ok" or not route.get("routes"):
            return jsonify({"error": "route could not be calculated"}), 422
        summary = route["routes"][0]
        distance_km = summary["distance"] / 1000
        duration_minutes = summary["duration"] / 60
        fare = FareService().estimate(distance_km, duration_minutes, vehicle_type)
        return jsonify({
            "pickup": {"lat": start_lat, "lng": start_lon},
            "destination": {"lat": end_lat, "lng": end_lon},
            "distance_km": round(distance_km, 2),
            "duration_minutes": round(duration_minutes),
            "vehicle_type": vehicle_type,
            "fare": fare,
        })
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception:
        return jsonify({"error": "routing service unavailable"}), 503
