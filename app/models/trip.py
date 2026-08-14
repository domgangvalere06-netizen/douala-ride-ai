from datetime import datetime, timezone
from app import db


TRIP_STATES = {
    "REQUESTED",
    "SEARCHING_DRIVER",
    "DRIVER_ASSIGNED",
    "DRIVER_ACCEPTED",
    "DRIVER_ARRIVING",
    "DRIVER_ARRIVED",
    "TRIP_STARTED",
    "TRIP_COMPLETED",
    "CANCELLED",
    "NO_DRIVER_FOUND",
    "PAYMENT_FAILED",
}

VALID_TRANSITIONS = {
    "REQUESTED": {"SEARCHING_DRIVER", "CANCELLED"},
    "SEARCHING_DRIVER": {"DRIVER_ASSIGNED", "NO_DRIVER_FOUND", "CANCELLED"},
    "DRIVER_ASSIGNED": {"DRIVER_ACCEPTED", "CANCELLED"},
    "DRIVER_ACCEPTED": {"DRIVER_ARRIVING", "CANCELLED"},
    "DRIVER_ARRIVING": {"DRIVER_ARRIVED", "CANCELLED"},
    "DRIVER_ARRIVED": {"TRIP_STARTED", "CANCELLED"},
    "TRIP_STARTED": {"TRIP_COMPLETED", "CANCELLED"},
    "TRIP_COMPLETED": set(),
    "CANCELLED": set(),
    "NO_DRIVER_FOUND": set(),
    "PAYMENT_FAILED": {"CANCELLED", "REQUESTED"},
}


class Trip(db.Model):
    __tablename__ = "trips"

    id = db.Column(db.Integer, primary_key=True)
    passenger_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    driver_id = db.Column(db.Integer, db.ForeignKey("drivers.id", ondelete="SET NULL"), nullable=True, index=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey("vehicles.id", ondelete="SET NULL"), nullable=True)
    pickup_address = db.Column(db.String(255), nullable=False)
    pickup_latitude = db.Column(db.Numeric(10, 7), nullable=False)
    pickup_longitude = db.Column(db.Numeric(10, 7), nullable=False)
    destination_address = db.Column(db.String(255), nullable=False)
    destination_latitude = db.Column(db.Numeric(10, 7), nullable=False)
    destination_longitude = db.Column(db.Numeric(10, 7), nullable=False)
    distance_km = db.Column(db.Numeric(8, 2), nullable=True)
    estimated_duration_minutes = db.Column(db.Integer, nullable=True)
    vehicle_type = db.Column(db.String(20), nullable=False)
    estimated_fare = db.Column(db.Numeric(10, 2), nullable=True)
    final_fare = db.Column(db.Numeric(10, 2), nullable=True)
    currency = db.Column(db.String(3), nullable=False, default="XAF")
    status = db.Column(db.String(30), nullable=False, default="REQUESTED", index=True)
    requested_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    driver_assigned_at = db.Column(db.DateTime, nullable=True)
    driver_arrived_at = db.Column(db.DateTime, nullable=True)
    started_at = db.Column(db.DateTime, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)
    cancelled_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    passenger = db.relationship("User", backref="trips")
    driver = db.relationship("Driver", backref="trips")
    vehicle = db.relationship("Vehicle", backref="trips")

    def transition_to(self, new_status: str) -> None:
        if new_status not in TRIP_STATES:
            raise ValueError(f"Unknown trip state: {new_status}")
        if new_status not in VALID_TRANSITIONS.get(self.status, set()):
            raise ValueError(f"Invalid trip transition: {self.status} -> {new_status}")
        self.status = new_status
        now = datetime.now(timezone.utc)
        if new_status == "DRIVER_ASSIGNED":
            self.driver_assigned_at = now
        elif new_status == "DRIVER_ARRIVED":
            self.driver_arrived_at = now
        elif new_status == "TRIP_STARTED":
            self.started_at = now
        elif new_status == "TRIP_COMPLETED":
            self.completed_at = now
        elif new_status == "CANCELLED":
            self.cancelled_at = now
