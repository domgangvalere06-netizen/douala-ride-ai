"""AI Mobility Agent orchestration layer."""

from typing import Any

from app.ai.mistral_adapter import MistralAdapter
from app.ai.tools.registry import ToolRegistry


SYSTEM_PROMPT = """You are Douala Ride's Mobility Agent.
Your job is to understand a passenger's mobility objective and use approved mobility tools to obtain real information. Never invent routes, prices, drivers, payment status, or trip status. Never access a database directly. Before consequential actions such as booking or payment, obtain explicit passenger confirmation.
For place names, use search_location before planning a trip. Prefer plan_trip when the passenger wants a complete journey plan: it returns real route, distance, duration, moto/car fares and budget filtering. Use find_available_drivers only after a pickup coordinate is known. Use create_booking only after the passenger confirms the proposed trip. Use initiate_payment only after the passenger explicitly confirms the payment amount, booking and Mobile Money action. Use get_payment_status when the passenger asks about payment state. Payment success is determined only by backend state updated from the payment provider callback; never claim success from frontend input or an initiation response alone.
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
