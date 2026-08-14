"""Map API endpoints."""

from flask import Blueprint, jsonify, request

from app.services.map_service import MapService

maps_bp = Blueprint("maps", __name__, url_prefix="/api/maps")
map_service = MapService()


@maps_bp.get("/search")
def search_location():
    query = request.args.get("q", "", type=str)
    limit = request.args.get("limit", 5, type=int)
    if not query.strip():
        return jsonify({"error": "q is required"}), 400
    try:
        return jsonify({"results": map_service.search_location(query, limit=limit)})
    except Exception as exc:
        return jsonify({"error": str(exc)}), 502


@maps_bp.get("/route")
def calculate_route():
    try:
        origin_lat = float(request.args["origin_lat"])
        origin_lon = float(request.args["origin_lon"])
        destination_lat = float(request.args["destination_lat"])
        destination_lon = float(request.args["destination_lon"])
    except (KeyError, TypeError, ValueError):
        return jsonify({"error": "origin_lat, origin_lon, destination_lat and destination_lon are required"}), 400

    try:
        result = map_service.plan_route(
            (origin_lat, origin_lon),
            (destination_lat, destination_lon),
        )
        return jsonify(result)
    except Exception as exc:
        return jsonify({"error": str(exc)}), 502
