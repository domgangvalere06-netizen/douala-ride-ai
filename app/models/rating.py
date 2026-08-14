from datetime import datetime, timezone
from app import db


class Rating(db.Model):
    __tablename__ = "ratings"

    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey("trips.id", ondelete="CASCADE"), nullable=False)
    passenger_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    driver_id = db.Column(db.Integer, db.ForeignKey("drivers.id", ondelete="CASCADE"), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (db.CheckConstraint("score >= 1 AND score <= 5", name="ck_rating_score"),)
