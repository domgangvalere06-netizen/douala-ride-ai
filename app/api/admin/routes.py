"""Admin Mobility Command Center API."""

from flask import Blueprint, jsonify

from app.services.admin_service import build_metrics

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")


@admin_bp.get("/dashboard")
def dashboard():
    # Repository-backed aggregation replaces these prototype values when the
    # authentication/admin repository layer is connected.
    metrics = build_metrics(
        total_users=0,
        active_drivers=0,
        active_trips=0,
        completed_trips=0,
        cancelled_trips=0,
        revenue_xaf=0,
    )
    return jsonify({
        "total_users": metrics.total_users,
        "active_drivers": metrics.active_drivers,
        "active_trips": metrics.active_trips,
        "completed_trips": metrics.completed_trips,
        "cancelled_trips": metrics.cancelled_trips,
        "revenue_xaf": metrics.revenue_xaf,
    })


@admin_bp.get("/live-map")
def live_map():
    return jsonify({"drivers": [], "active_trips": []})
