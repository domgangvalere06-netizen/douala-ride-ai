from flask import Blueprint, jsonify, request

from flask_jwt_extended import create_access_token

from ..extensions import db
from ..models.user import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/register")
def register():
    data = request.get_json() or {}
    phone = data.get("phone")
    name = data.get("name")
    role = data.get("role", "passenger")

    if not phone or not name:
        return jsonify({"error": "name and phone are required"}), 400
    if role not in {"passenger", "driver", "admin"}:
        return jsonify({"error": "invalid role"}), 400
    if User.query.filter_by(phone=phone).first():
        return jsonify({"error": "phone already registered"}), 409

    user = User(name=name, phone=phone, role=role)
    db.session.add(user)
    db.session.commit()
    return jsonify({"id": user.id, "name": user.name, "phone": user.phone, "role": user.role}), 201


@auth_bp.post("/login")
def login():
    data = request.get_json() or {}
    user = User.query.filter_by(phone=data.get("phone")).first()
    if not user:
        return jsonify({"error": "user not found"}), 404
    return jsonify({"access_token": create_access_token(identity=str(user.id)), "user": {"id": user.id, "role": user.role}})
