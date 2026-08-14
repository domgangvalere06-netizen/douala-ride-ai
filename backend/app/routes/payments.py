from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from ..services.payment_service import PawaPayService

payments_bp = Blueprint("payments", __name__)


@payments_bp.post("/initiate")
@jwt_required()
def initiate_payment():
    data = request.get_json() or {}
    for field in ("amount", "phone", "external_id"):
        if not data.get(field):
            return jsonify({"error": f"{field} is required"}), 400

    result = PawaPayService().create_payment(
        amount=int(data["amount"]), phone=data["phone"], external_id=data["external_id"]
    )
    return jsonify(result)


@payments_bp.post("/callback")
def payment_callback():
    payload = request.get_json(silent=True) or {}
    # Signature/authentication verification must be added according to the active PawaPay webhook contract.
    return jsonify({"received": True, "payload": payload}), 200
