"""Deterministic fare estimation for Douala Ride.

The AI may request a fare estimate, but it never invents or persists prices.
This service owns the pricing rules and returns a transparent estimate.
"""

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP


@dataclass(frozen=True)
class FareEstimate:
    vehicle_type: str
    distance_km: float
    duration_minutes: int
    base_fare: int
    distance_fare: int
    time_fare: int
    estimated_fare: int
    currency: str = "XAF"


# Initial prototype pricing. These values are configuration-level business rules,
# not AI-generated values. They should later move to database/configuration so an
# administrator can manage pricing by vehicle type and operating area.
PRICING = {
    "moto": {"base": 300, "per_km": 180, "per_minute": 10, "minimum": 500},
    "car": {"base": 700, "per_km": 300, "per_minute": 15, "minimum": 1000},
}


def _round_50(value: Decimal) -> int:
    """Round a fare to the nearest 50 XAF."""
    rounded = (value / Decimal(50)).quantize(Decimal("1"), rounding=ROUND_HALF_UP) * Decimal(50)
    return int(rounded)


def estimate_fare(vehicle_type: str, distance_km: float, duration_minutes: int) -> FareEstimate:
    vehicle_type = vehicle_type.lower().strip()
    if vehicle_type not in PRICING:
        raise ValueError(f"Unsupported vehicle type: {vehicle_type}")
    if distance_km < 0 or duration_minutes < 0:
        raise ValueError("Distance and duration must be non-negative")

    rules = PRICING[vehicle_type]
    distance_fare = int(Decimal(str(distance_km)) * Decimal(rules["per_km"]))
    time_fare = int(Decimal(duration_minutes) * Decimal(rules["per_minute"]))
    raw_total = Decimal(rules["base"] + distance_fare + time_fare)
    estimated = max(rules["minimum"], _round_50(raw_total))

    return FareEstimate(
        vehicle_type=vehicle_type,
        distance_km=round(distance_km, 2),
        duration_minutes=int(duration_minutes),
        base_fare=rules["base"],
        distance_fare=distance_fare,
        time_fare=time_fare,
        estimated_fare=estimated,
    )
