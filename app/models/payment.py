from datetime import datetime, timezone
import uuid
from app import db


class Payment(db.Model):
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)
    reference = db.Column(db.String(50), unique=True, nullable=False, index=True, default=lambda: f"PAY-{uuid.uuid4().hex[:14].upper()}")
    booking_id = db.Column(db.Integer, db.ForeignKey("bookings.id", ondelete="CASCADE"), nullable=False, unique=True)
    provider = db.Column(db.String(40), nullable=False, default="pawapay")
    provider_transaction_id = db.Column(db.String(120), unique=True, nullable=True)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    currency = db.Column(db.String(3), nullable=False, default="XAF")
    status = db.Column(db.String(20), nullable=False, default="PENDING", index=True)
    payment_method = db.Column(db.String(40), nullable=True)
    failure_reason = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    booking = db.relationship("Booking", backref=db.backref("payment", uselist=False))
