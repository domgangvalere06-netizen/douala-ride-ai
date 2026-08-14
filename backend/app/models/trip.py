from datetime import datetime
from ..extensions import db


class Trip(db.Model):
    __tablename__ = "trips"

    id = db.Column(db.Integer, primary_key=True)
    passenger_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    driver_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    vehicle_type = db.Column(db.String(20), nullable=False, default="moto")
    pickup = db.Column(db.String(255), nullable=False)
    destination = db.Column(db.String(255), nullable=False)
    estimated_fare = db.Column(db.Integer, nullable=True)
    status = db.Column(db.String(30), nullable=False, default="requested")
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
