from datetime import datetime, timezone
from app import db


class AIToolCall(db.Model):
    __tablename__ = "ai_tool_calls"

    id = db.Column(db.BigInteger, primary_key=True)
    ai_request_id = db.Column(db.BigInteger, db.ForeignKey("ai_requests.id", ondelete="CASCADE"), nullable=False, index=True)
    tool_name = db.Column(db.String(100), nullable=False)
    arguments_json = db.Column(db.JSON, nullable=True)
    result_json = db.Column(db.JSON, nullable=True)
    status = db.Column(db.String(30), nullable=False, default="STARTED")
    error_message = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    completed_at = db.Column(db.DateTime, nullable=True)

    ai_request = db.relationship("AIRequest", backref="tool_calls")
