"""Payment API endpoints and asynchronous PawaPay callback handling."""

from flask import Blueprint, jsonify, request

from app import db
from app.integrations.payments.pawapay import PawaPayClient, PawaPayError
from app.models.payment import Payment
from app.models.payment_event import PaymentEvent
from app.services.payment_application import PaymentApplicationService

payments_bp = Blueprint("payments", __name__, url_prefix="/api/payments")
payment_service = PaymentApplicationService()


@payments_bp.post("/initiate")
def initiate_payment():
    body = request.get_json(silent=True) or {}
    booking_id = body.get("booking_id")
    amount = body.get("amount_xaf")
    phone = body.get("phone_number")
    provider = body.get("provider")

    if not isinstance(booking_id, int) or booking_id <= 0:
        return jsonify({"error": "booking_id is required"}), 400
    if not isinstance(amount, int) or amount <= 0 or not phone:
        return jsonify({"error": "positive amount_xaf and phone_number are required"}), 400

    try:
        return jsonify(payment_service.initiate_for_booking(booking_id, amount, phone, provider)), 202
    except PawaPayError as exc:
        return jsonify({"error": str(exc)}), 502
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400


@payments_bp.get("/<reference>")
def payment_status(reference: str):
    try:
        return jsonify(payment_service.get_status(reference)), 200
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 404


@payments_bp.post("/webhook")
def payment_webhook():
    payload = request.get_json(silent=True) or {}
    try:
        normalized = PawaPayClient().verify_webhook(payload)
    except PawaPayError as exc:
        return jsonify({"error": str(exc)}), 400

    reference = normalized.get("reference")
    if not reference:
        return jsonify({"error": "clientReferenceId is required"}), 400

    payment = db.session.query(Payment).filter_by(reference=reference).one_or_none()
    if not payment:
        return jsonify({"error": "Payment not found"}), 404

    # PawaPay callbacks can be retried. Treat a previously received deposit
    # event as idempotent instead of inserting duplicate provider events.
    deposit_id = normalized.get("deposit_id")
    if deposit_id and db.session.query(PaymentEvent).filter_by(provider_event_id=deposit_id).first():
        return jsonify({"received": True, "reference": reference, "status": payment.status}), 200

    db.session.add(PaymentEvent(
        payment_id=payment.id,
        provider_event_id=deposit_id,
        event_type=f"PAWAPAY_{normalized['status']}",
        payload_json=normalized["raw"],
    ))

    status = normalized["status"]
    payment.status = {"COMPLETED": "SUCCESS", "PROCESSING": "PROCESSING", "FAILED": "FAILED"}[status]
    if normalized.get("provider_transaction_id"):
        payment.provider_transaction_id = normalized["provider_transaction_id"]
    if normalized.get("failure_reason"):
        payment.failure_reason = str(normalized["failure_reason"])

    if payment.status == "SUCCESS":
        payment.booking.status = "PAID"
    elif payment.status == "FAILED":
        payment.booking.status = "PAYMENT_FAILED"

    db.session.commit()
    return jsonify({"received": True, "reference": reference, "status": payment.status}), 200
