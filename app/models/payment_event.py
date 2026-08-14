from datetime import datetime, timezone
from app import db


class PaymentEvent(db.Model):
    __tablename__ = "payment_events"

    id = db.Column(db.Integer, primary_key=True)
    payment_id = db.Column(db.Integer, db.ForeignKey("payments.id", ondelete="CASCADE"), nullable=False, index=True)
    provider_event_id = db.Column(db.String(120), unique=True, nullable=True)
    event_type = db.Column(db.String(80), nullable=False)
    payload_json = db.Column(db.JSON, nullable=False)
    received_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    payment = db.relationship("Payment", backref="events")
