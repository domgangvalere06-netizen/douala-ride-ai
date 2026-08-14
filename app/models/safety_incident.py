from datetime import datetime, timezone
from app import db


class SafetyIncident(db.Model):
    __tablename__ = "safety_incidents"

    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey("trips.id", ondelete="SET NULL"), nullable=True, index=True)
    reporter_user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    incident_type = db.Column(db.String(60), nullable=False)
    description = db.Column(db.Text, nullable=True)
    latitude = db.Column(db.Numeric(10, 7), nullable=True)
    longitude = db.Column(db.Numeric(10, 7), nullable=True)
    status = db.Column(db.String(30), nullable=False, default="OPEN", index=True)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    resolved_at = db.Column(db.DateTime, nullable=True)

    trip = db.relationship("Trip", backref="safety_incidents")
