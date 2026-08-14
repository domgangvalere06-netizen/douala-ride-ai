"""Payment API endpoints and asynchronous PawaPay callback handling."""

from decimal import Decimal

from flask import Blueprint, jsonify, request

from app import db
from app.integrations.payments.pawapay import PawaPayClient, PawaPayError
from app.models.booking import Booking
from app.models.payment import Payment
from app.models.payment_event import PaymentEvent
from app.services.payment_service import PaymentService

payments_bp = Blueprint("payments", __name__, url_prefix="/api/payments")


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

    booking = db.session.get(Booking, booking_id)
    if not booking:
        return jsonify({"error": "Booking not found"}), 404
    if booking.payment is not None:
        return jsonify({"error": "Payment already exists for this booking", "reference": booking.payment.reference}), 409

    payment = Payment(booking_id=booking.id, amount=Decimal(amount), currency="XAF", status="PENDING", payment_method=provider or "MOBILE_MONEY")
    db.session.add(payment)
    db.session.flush()

    try:
        intent = PaymentService(PawaPayClient()).initiate(
            payment.reference,
            amount,
            phone,
            provider=provider,
        )
        payment.status = intent.status.value
        payment.provider_transaction_id = intent.provider_reference
        payment.payment_method = provider or "MOBILE_MONEY"
        db.session.commit()
        return jsonify({
            "reference": payment.reference,
            "booking_id": booking.id,
            "amount_xaf": amount,
            "currency": "XAF",
            "status": payment.status,
            "provider": payment.provider,
            "deposit_id": intent.provider_reference,
        }), 202
    except PawaPayError as exc:
        payment.status = "FAILED"
        payment.failure_reason = str(exc)
        db.session.commit()
        return jsonify({"error": str(exc), "reference": payment.reference}), 502
    except ValueError as exc:
        db.session.rollback()
        return jsonify({"error": str(exc)}), 400


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

    event = PaymentEvent(
        payment_id=payment.id,
        provider_event_id=normalized.get("deposit_id"),
        event_type=f"PAWAPAY_{normalized['status']}",
        payload_json=normalized["raw"],
    )
    db.session.add(event)

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
