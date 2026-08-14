"""Passenger web experience routes."""

from flask import Blueprint, render_template

web_bp = Blueprint("web", __name__)


@web_bp.get("/")
def passenger_map():
    return render_template("passenger_map.html")
