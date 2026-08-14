"""Universal trip planning API for arbitrary supported locations."""

from flask import Blueprint, jsonify, request

from app.services.route_fare_service import RouteFareService

trip_plan_bp = Blueprint("trip_plan", __name__, url_prefix="/api/trips")


@trip_plan_bp.post("/plan")
def plan_trip():
    data = request.get_json(silent=True) or {}
    origin = data.get("origin")
    destination = data.get("destination")
    budget_xaf = data.get("budget_xaf")
    vehicle_type = data.get("vehicle_type")

    if not isinstance(origin, dict) or not isinstance(destination, dict):
        return jsonify({"error": "origin and destination objects are required"}), 400

    try:
        plan = RouteFareService().plan(
            origin=origin,
            destination=destination,
            vehicle_type=vehicle_type,
            budget_xaf=budget_xaf,
        )
        return jsonify({"success": True, "trip_plan": plan}), 200
    except ValueError as exc:
        return jsonify({"success": False, "error": str(exc)}), 400
    except Exception:
        return jsonify({"success": False, "error": "Unable to calculate trip plan"}), 502
