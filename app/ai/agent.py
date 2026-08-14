"""AI Mobility Agent orchestration layer."""

from typing import Any

from app.ai.mistral_adapter import MistralAdapter
from app.ai.tools.registry import ToolRegistry


SYSTEM_PROMPT = """You are Douala Ride's Mobility Agent.
Your job is to understand a passenger's mobility objective and use approved mobility tools to obtain real information. Never invent routes, prices, drivers, payment status, or trip status. Never access a database directly. Before a consequential action such as booking or payment, obtain passenger confirmation unless an explicit product policy says otherwise.
For place names, use search_location before calculating a route. Use the route result for distance and duration. Use compare_transport_options when the passenger wants the best transport choice, budget-aware recommendations, or moto/car comparison. Use find_available_drivers only after a pickup coordinate is known. Never create a booking unless the passenger has explicitly confirmed the proposed trip.
"""


class MobilityAgent:
    def __init__(self, tool_registry: ToolRegistry | None = None, model_adapter: Any = None):
        self.tools = tool_registry or ToolRegistry()
        self.model_adapter = model_adapter or MistralAdapter()

    def available_tools(self) -> list[str]:
        return self.tools.names()

    def execute_tool(self, name: str, arguments: dict[str, Any]):
        return self.tools.execute(name, arguments)

    def context(self, user_message: str) -> dict[str, Any]:
        return {
            "system": SYSTEM_PROMPT,
            "user_message": user_message,
            "available_tools": self.available_tools(),
        }

    def respond(self, user_message: str) -> dict[str, Any]:
        return self.model_adapter.run(self.context(user_message), self.tools)
