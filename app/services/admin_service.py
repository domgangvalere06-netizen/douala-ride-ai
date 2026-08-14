"""Admin mobility analytics service.

This service is intentionally persistence-agnostic. Flask handlers can inject
real repositories later, while the dashboard remains based on explicit
metrics rather than AI-generated numbers.
"""

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class MobilityMetrics:
    total_users: int
    active_drivers: int
    active_trips: int
    completed_trips: int
    cancelled_trips: int
    revenue_xaf: int


def build_metrics(*, total_users: int, active_drivers: int, active_trips: int,
                  completed_trips: int, cancelled_trips: int, revenue_xaf: int) -> MobilityMetrics:
    values = [total_users, active_drivers, active_trips, completed_trips, cancelled_trips, revenue_xaf]
    if any(v < 0 for v in values):
        raise ValueError("Dashboard metrics cannot be negative")
    return MobilityMetrics(total_users, active_drivers, active_trips, completed_trips, cancelled_trips, revenue_xaf)


def demand_by_area(trips: Iterable[dict]) -> list[dict]:
    """Aggregate trip counts by pickup area from normalized trip records."""
    counts: dict[str, int] = {}
    for trip in trips:
        area = str(trip.get("pickup_area") or "Unknown")
        counts[area] = counts.get(area, 0) + 1
    return sorted(
        [{"area": area, "trip_count": count} for area, count in counts.items()],
        key=lambda item: item["trip_count"],
        reverse=True,
    )
