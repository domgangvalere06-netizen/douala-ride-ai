from datetime import datetime, timezone
from app import db


class DriverLocation(db.Model):
    __tablename__ = "driver_locations"

    id = db.Column(db.BigInteger, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey("drivers.id", ondelete="CASCADE"), nullable=False, index=True)
    latitude = db.Column(db.Numeric(10, 7), nullable=False)
    longitude = db.Column(db.Numeric(10, 7), nullable=False)
    heading = db.Column(db.Numeric(6, 2), nullable=True)
    speed = db.Column(db.Numeric(8, 2), nullable=True)
    accuracy = db.Column(db.Numeric(8, 2), nullable=True)
    recorded_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), index=True)

    driver = db.relationship("Driver", back_populates="locations")
