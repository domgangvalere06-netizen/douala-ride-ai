"""Allow-list of tools that the AI agent is permitted to request."""

from typing import Any, Callable

from app.ai.tools.bookings import create_booking
from app.ai.tools.drivers import find_available_drivers
from app.ai.tools.fares import estimate_trip_fare
from app.ai.tools.maps import MapTools
from app.ai.tools.options import compare_transport_options
from app.ai.tools.payments import get_payment_status, initiate_payment


class ToolRegistry:
    def __init__(self, map_tools: MapTools | None = None):
        maps = map_tools or MapTools()
        self._tools: dict[str, Callable[..., Any]] = {
            "search_location": maps.search_location,
            "calculate_route": maps.calculate_route,
            "plan_trip": maps.plan_trip,
            "estimate_fare": estimate_trip_fare,
            "find_available_drivers": find_available_drivers,
            "compare_transport_options": compare_transport_options,
            "create_booking": create_booking,
            "initiate_payment": initiate_payment,
            "get_payment_status": get_payment_status,
        }

    def names(self) -> list[str]:
        return list(self._tools.keys())

    def execute(self, name: str, arguments: dict[str, Any]):
        if name not in self._tools:
            raise ValueError(f"Tool is not allowed: {name}")
        return self._tools[name](**arguments)
