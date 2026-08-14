"""Controlled payment tools for the Mobility Agent."""

from app.services.payment_application import PaymentApplicationService


_payment_service = PaymentApplicationService()


def initiate_payment(booking_id: int, amount_xaf: int, phone_number: str, provider: str | None = None, confirmed: bool = False):
    if not confirmed:
        raise ValueError("Passenger confirmation is required before initiating payment")
    return _payment_service.initiate_for_booking(booking_id, amount_xaf, phone_number, provider)


def get_payment_status(reference: str):
    return _payment_service.get_status(reference)
