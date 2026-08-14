"""Compare moto and car options using real route data and deterministic fares."""

from app.ai.tools.fares import estimate_trip_fare


def compare_transport_options(distance_km: float, duration_minutes: int, budget_xaf: int | None = None, preferred_vehicle: str | None = None):
    if distance_km < 0 or duration_minutes < 0:
        raise ValueError("distance_km and duration_minutes must be non-negative")
    if budget_xaf is not None and budget_xaf < 0:
        raise ValueError("budget_xaf must be non-negative")
    if preferred_vehicle is not None and preferred_vehicle not in {"moto", "car"}:
        raise ValueError("preferred_vehicle must be moto or car")

    options = [estimate_trip_fare(vehicle, distance_km, duration_minutes) for vehicle in ("moto", "car")]
    result = []
    for option in options:
        within_budget = budget_xaf is None or option.estimated_fare <= budget_xaf
        preference_bonus = 1 if preferred_vehicle == option.vehicle_type else 0
        budget_bonus = 1 if within_budget else 0
        score = budget_bonus * 2 + preference_bonus
        result.append({
            "vehicle_type": option.vehicle_type,
            "estimated_fare": option.estimated_fare,
            "currency": option.currency,
            "distance_km": option.distance_km,
            "duration_minutes": option.duration_minutes,
            "within_budget": within_budget,
            "recommendation_score": score,
        })
    return sorted(result, key=lambda item: (-item["recommendation_score"], item["estimated_fare"]))
