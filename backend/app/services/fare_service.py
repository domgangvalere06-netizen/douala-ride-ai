class FareService:
    """Transparent MVP fare engine. Prices are centralized for easy adjustment."""

    RATES = {
        "moto": {"base": 500, "per_km": 150, "per_minute": 15, "minimum": 500},
        "car": {"base": 1000, "per_km": 300, "per_minute": 25, "minimum": 1000},
    }

    def estimate(self, distance_km: float, duration_minutes: float, vehicle_type: str) -> dict:
        if vehicle_type not in self.RATES:
            raise ValueError("vehicle_type must be moto or car")
        if distance_km < 0 or duration_minutes < 0:
            raise ValueError("distance and duration cannot be negative")

        rate = self.RATES[vehicle_type]
        distance_cost = distance_km * rate["per_km"]
        time_cost = duration_minutes * rate["per_minute"]
        raw_total = rate["base"] + distance_cost + time_cost
        total = max(rate["minimum"], round(raw_total / 50) * 50)
        return {
            "vehicle_type": vehicle_type,
            "currency": "XAF",
            "distance_km": round(distance_km, 2),
            "duration_minutes": round(duration_minutes),
            "base_fare": rate["base"],
            "distance_cost": round(distance_cost),
            "time_cost": round(time_cost),
            "estimated_fare": int(total),
        }
