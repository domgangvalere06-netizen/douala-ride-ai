from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from ..services.trip_planner import TripPlanner

planning_bp = Blueprint("planning", __name__)


@planning_bp.post("/plan")
@jwt_required()
def plan():
    data = request.get_json() or {}
    pickup = data.get("pickup")
    destination = data.get("destination")
    vehicle_type = data.get("vehicle_type", "moto")

    if not pickup or not destination:
        return jsonify({"error": "pickup and destination are required"}), 400
    if vehicle_type not in {"moto", "car"}:
        return jsonify({"error": "vehicle_type must be moto or car"}), 400

    try:
        return jsonify(TripPlanner().plan(pickup, destination, vehicle_type))
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception:
        return jsonify({"error": "Unable to calculate this trip right now"}), 502
