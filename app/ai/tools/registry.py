"""Allow-list of tools that the AI agent is permitted to request."""

from typing import Any, Callable

from app.ai.tools.fares import estimate_trip_fare
from app.ai.tools.maps import MapTools


class ToolRegistry:
    def __init__(self, map_tools: MapTools | None = None):
        maps = map_tools or MapTools()
        self._tools: dict[str, Callable[..., Any]] = {
            "search_location": maps.search_location,
            "calculate_route": maps.calculate_route,
            "estimate_fare": estimate_trip_fare,
        }

    def names(self) -> list[str]:
        return list(self._tools.keys())

    def execute(self, name: str, arguments: dict[str, Any]):
        if name not in self._tools:
            raise ValueError(f"Tool is not allowed: {name}")
        return self._tools[name](**arguments)
