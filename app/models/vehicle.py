from datetime import datetime, timezone
from app import db


class Vehicle(db.Model):
    __tablename__ = "vehicles"

    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey("drivers.id", ondelete="CASCADE"), nullable=False, index=True)
    vehicle_type = db.Column(db.String(20), nullable=False, index=True)  # moto | car
    brand = db.Column(db.String(80), nullable=True)
    model = db.Column(db.String(80), nullable=True)
    registration_number = db.Column(db.String(50), unique=True, nullable=False)
    color = db.Column(db.String(40), nullable=True)
    verification_status = db.Column(db.String(20), nullable=False, default="pending")
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    driver = db.relationship("Driver", back_populates="vehicles")
