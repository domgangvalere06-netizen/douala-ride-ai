from datetime import datetime
from ..extensions import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(30), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False, default="passenger")
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
