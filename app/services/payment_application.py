"""Application service for booking payments.

Keeps payment persistence, provider initiation and callback-facing state in one
controlled backend service that can be used by API handlers and AI tools.
"""

from decimal import Decimal

from app import db
from app.integrations.payments.pawapay import PawaPayClient
from app.models.booking import Booking
from app.models.payment import Payment
from app.services.payment_service import PaymentService


class PaymentApplicationService:
    def initiate_for_booking(self, booking_id: int, amount_xaf: int, phone_number: str, provider: str | None = None):
        if booking_id <= 0 or amount_xaf <= 0 or not phone_number.strip():
            raise ValueError("booking_id, positive amount and phone number are required")

        booking = db.session.get(Booking, booking_id)
        if not booking:
            raise ValueError("Booking not found")
        if booking.payment is not None:
            raise ValueError("Payment already exists for this booking")

        payment = Payment(
            booking_id=booking.id,
            amount=Decimal(amount_xaf),
            currency="XAF",
            status="PENDING",
            payment_method=provider or "MOBILE_MONEY",
        )
        db.session.add(payment)
        db.session.flush()

        try:
            intent = PaymentService(PawaPayClient()).initiate(
                payment.reference,
                amount_xaf,
                phone_number,
                provider=provider,
            )
            payment.status = intent.status.value
            payment.provider_transaction_id = intent.provider_reference
            payment.payment_method = provider or "MOBILE_MONEY"
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

        return {
            "reference": payment.reference,
            "booking_id": booking.id,
            "amount_xaf": amount_xaf,
            "currency": "XAF",
            "status": payment.status,
            "provider": payment.provider,
            "deposit_id": intent.provider_reference,
        }

    def get_status(self, reference: str):
        payment = db.session.query(Payment).filter_by(reference=reference).one_or_none()
        if not payment:
            raise ValueError("Payment not found")
        return {
            "reference": payment.reference,
            "booking_id": payment.booking_id,
            "status": payment.status,
            "amount_xaf": float(payment.amount),
            "currency": payment.currency,
            "provider": payment.provider,
        }
