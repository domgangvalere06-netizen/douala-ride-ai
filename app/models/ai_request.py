from datetime import datetime, timezone
from app import db


class AIRequest(db.Model):
    __tablename__ = "ai_requests"

    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    request_text = db.Column(db.Text, nullable=False)
    intent = db.Column(db.String(80), nullable=True)
    status = db.Column(db.String(30), nullable=False, default="RECEIVED", index=True)
    response_text = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    completed_at = db.Column(db.DateTime, nullable=True)

    user = db.relationship("User", backref="ai_requests")
