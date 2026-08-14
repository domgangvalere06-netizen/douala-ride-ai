"""Payment API endpoints."""

from flask import Blueprint, jsonify, request

from app.integrations.payments.pawapay import PawaPayClient, PawaPayError
from app.services.payment_service import PaymentService

payments_bp = Blueprint("payments", __name__, url_prefix="/api/payments")


@payments_bp.post("/initiate")
def initiate_payment():
    body = request.get_json(silent=True) or {}
    reference = body.get("reference")
    amount = body.get("amount_xaf")
    phone = body.get("phone_number")
    if not reference or not isinstance(amount, int) or amount <= 0 or not phone:
        return jsonify({"error": "reference, positive amount_xaf and phone_number are required"}), 400

    try:
        payment = PaymentService(PawaPayClient()).initiate(reference, amount, phone)
        return jsonify({
            "reference": payment.reference,
            "amount_xaf": payment.amount_xaf,
            "currency": payment.currency,
            "status": payment.status.value,
            "provider": payment.provider,
        }), 202
    except PawaPayError as exc:
        return jsonify({"error": str(exc)}), 502
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400


@payments_bp.post("/webhook")
def payment_webhook():
    payload = request.get_json(silent=True) or {}
    try:
        normalized = PawaPayClient().verify_webhook(payload)
    except PawaPayError as exc:
        return jsonify({"error": str(exc)}), 400

    if not normalized.get("reference") or not normalized.get("status"):
        return jsonify({"error": "reference and status are required"}), 400

    # Persistence and signature verification should be implemented in the
    # payment application service before this endpoint is used in production.
    return jsonify({"received": True, "payment": normalized}), 200
