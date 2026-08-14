from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from ..services.ai_service import AIService

aI_bp = Blueprint("ai", __name__)
ai_bp = aI_bp


@ai_bp.post("/plan")
@jwt_required()
def plan_trip():
    data = request.get_json() or {}
    prompt = data.get("request")
    if not prompt:
        return jsonify({"error": "request is required"}), 400
    return jsonify(AIService().plan_trip(prompt))
