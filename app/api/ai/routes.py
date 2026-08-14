"""AI Mobility Agent API."""

from flask import Blueprint, jsonify, request

from app.ai.agent import MobilityAgent

ai_bp = Blueprint("ai", __name__, url_prefix="/api/ai")
agent = MobilityAgent()


@ai_bp.post("/chat")
def chat():
    body = request.get_json(silent=True) or {}
    message = body.get("message")
    if not isinstance(message, str) or not message.strip():
        return jsonify({"error": "message is required"}), 400
    return jsonify(agent.respond(message.strip()))


@ai_bp.get("/tools")
def tools():
    return jsonify({"tools": agent.available_tools()})
