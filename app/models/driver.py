from datetime import datetime, timezone
from app import db


class Driver(db.Model):
    __tablename__ = "drivers"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    license_number = db.Column(db.String(80), unique=True, nullable=False)
    verification_status = db.Column(db.String(20), nullable=False, default="pending", index=True)
    safety_status = db.Column(db.String(20), nullable=False, default="clear")
    rating = db.Column(db.Numeric(3, 2), nullable=False, default=5.00)
    total_trips = db.Column(db.Integer, nullable=False, default=0)
    is_online = db.Column(db.Boolean, nullable=False, default=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user = db.relationship("User", backref=db.backref("driver_profile", uselist=False))
    vehicles = db.relationship("Vehicle", back_populates="driver", cascade="all, delete-orphan")
    locations = db.relationship("DriverLocation", back_populates="driver", cascade="all, delete-orphan")
