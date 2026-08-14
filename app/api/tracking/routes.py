"""Tracking and safety HTTP endpoints."""

from flask import Blueprint, jsonify, request

from app.services.safety_service import create_safety_event
from app.services.tracking_service import normalize_location

tracking_bp = Blueprint("tracking", __name__, url_prefix="/api/tracking")


@tracking_bp.post("/location")
def update_location():
    body = request.get_json(silent=True) or {}
    try:
        driver_id = int(body["driver_id"])
        point = normalize_location(float(body["latitude"]), float(body["longitude"]))
    except (KeyError, TypeError, ValueError) as exc:
        return jsonify({"error": str(exc)}), 400
    if driver_id <= 0:
        return jsonify({"error": "driver_id must be positive"}), 400
    # Persistence/broadcast is added in the realtime adapter. This endpoint
    # currently validates and normalizes incoming GPS data.
    return jsonify({"driver_id": driver_id, "latitude": point.latitude, "longitude": point.longitude, "recorded_at": point.recorded_at.isoformat()}), 202


@tracking_bp.post("/safety")
def safety_event():
    body = request.get_json(silent=True) or {}
    try:
        event = create_safety_event(int(body["trip_id"]), body["event_type"], body.get("description", ""))
    except (KeyError, TypeError, ValueError) as exc:
        return jsonify({"error": str(exc)}), 400
    return jsonify({"trip_id": event.trip_id, "event_type": event.event_type, "severity": event.severity, "description": event.description}), 201
