"""AI Mobility Agent orchestration layer.

This first version deliberately keeps execution deterministic. A model adapter
can later select tools from the same allow-list without gaining database
access or unrestricted code execution.
"""

from typing import Any

from app.ai.tools.registry import ToolRegistry


SYSTEM_PROMPT = """You are Douala Ride's Mobility Agent.
Your job is to understand a passenger's mobility objective and use approved
mobility tools to obtain real information. Never invent routes, prices,
drivers, payment status, or trip status. Never access a database directly.
Before a consequential action such as booking or payment, obtain passenger
confirmation unless an explicit product policy says otherwise.
"""


class MobilityAgent:
    def __init__(self, tool_registry: ToolRegistry | None = None, model_adapter: Any = None):
        self.tools = tool_registry or ToolRegistry()
        self.model_adapter = model_adapter

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
        """Return an adapter-ready agent response.

        Until the Mistral adapter is wired in, this endpoint intentionally does
        not pretend to have completed an AI action. It exposes the controlled
        tool contract that the model will use next.
        """
        if self.model_adapter is not None:
            return self.model_adapter.run(self.context(user_message), self.tools)
        return {
            "message": "Mobility Agent ready. Mistral model adapter is not configured yet.",
            "requires_model": True,
            "available_tools": self.available_tools(),
        }
