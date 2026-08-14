from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from ..extensions import db
from ..models.trip import Trip

trips_bp = Blueprint("trips", __name__)


@trips_bp.post("")
@jwt_required()
def create_trip():
    data = request.get_json() or {}
    required = ["pickup", "destination"]
    if any(not data.get(field) for field in required):
        return jsonify({"error": "pickup and destination are required"}), 400

    trip = Trip(
        passenger_id=int(get_jwt_identity()),
        pickup=data["pickup"],
        destination=data["destination"],
        vehicle_type=data.get("vehicle_type", "moto"),
        estimated_fare=data.get("estimated_fare"),
    )
    db.session.add(trip)
    db.session.commit()
    return jsonify({"id": trip.id, "status": trip.status}), 201


@trips_bp.get("/<int:trip_id>")
@jwt_required()
def get_trip(trip_id):
    trip = db.session.get(Trip, trip_id)
    if not trip:
        return jsonify({"error": "trip not found"}), 404
    return jsonify({
        "id": trip.id,
        "pickup": trip.pickup,
        "destination": trip.destination,
        "vehicle_type": trip.vehicle_type,
        "estimated_fare": trip.estimated_fare,
        "status": trip.status,
    })
