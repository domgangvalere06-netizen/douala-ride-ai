"""Mistral adapter for the controlled Douala Ride Mobility Agent.

The adapter translates Mistral tool calls into the application's allow-listed
ToolRegistry. It never gives the model database credentials or arbitrary code
execution.
"""

import json
import os
from typing import Any

import requests


class MistralError(RuntimeError):
    pass


class MistralAdapter:
    def __init__(self, api_key: str | None = None, model: str | None = None):
        self.api_key = api_key or os.getenv("MISTRAL_API_KEY")
        self.model = model or os.getenv("MISTRAL_MODEL", "mistral-small-latest")
        self.base_url = os.getenv("MISTRAL_BASE_URL", "https://api.mistral.ai/v1")
        self.timeout = int(os.getenv("MISTRAL_TIMEOUT_SECONDS", "30"))

    def _tool_definitions(self, tool_names: list[str]) -> list[dict[str, Any]]:
        definitions = {
            "search_location": {
                "type": "function",
                "function": {
                    "name": "search_location",
                    "description": "Search for a place in Cameroon and return coordinates.",
                    "parameters": {"type": "object", "properties": {"query": {"type": "string"}, "limit": {"type": "integer", "minimum": 1, "maximum": 10}}, "required": ["query"]},
                },
            },
            "calculate_route": {
                "type": "function",
                "function": {
                    "name": "calculate_route",
                    "description": "Calculate a driving route between two geographic coordinates.",
                    "parameters": {"type": "object", "properties": {"origin_lat": {"type": "number"}, "origin_lon": {"type": "number"}, "destination_lat": {"type": "number"}, "destination_lon": {"type": "number"}}, "required": ["origin_lat", "origin_lon", "destination_lat", "destination_lon"]},
                },
            },
            "estimate_fare": {
                "type": "function",
                "function": {
                    "name": "estimate_fare",
                    "description": "Estimate a trip fare using Douala Ride's deterministic pricing engine.",
                    "parameters": {"type": "object", "properties": {"vehicle_type": {"type": "string", "enum": ["moto", "car"]}, "distance_km": {"type": "number"}, "duration_minutes": {"type": "integer"}}, "required": ["vehicle_type", "distance_km", "duration_minutes"]},
                },
            },
        }
        return [definitions[name] for name in tool_names if name in definitions]

    def run(self, context: dict[str, Any], tools):
        if not self.api_key:
            raise MistralError("MISTRAL_API_KEY is not configured")

        messages = [
            {"role": "system", "content": context["system"]},
            {"role": "user", "content": context["user_message"]},
        ]
        available = context["available_tools"]
        tool_defs = self._tool_definitions(available)

        for _ in range(6):
            payload = {"model": self.model, "messages": messages, "tools": tool_defs, "tool_choice": "auto", "temperature": 0.1}
            response = requests.post(
                f"{self.base_url.rstrip('/')}/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
                json=payload,
                timeout=self.timeout,
            )
            if not response.ok:
                raise MistralError(f"Mistral request failed: {response.status_code} {response.text[:500]}")

            data = response.json()
            message = data["choices"][0]["message"]
            tool_calls = message.get("tool_calls") or []
            messages.append(message)

            if not tool_calls:
                return {"message": message.get("content", ""), "tool_calls": []}

            executed = []
            for call in tool_calls:
                function = call["function"]
                name = function["name"]
                try:
                    arguments = json.loads(function.get("arguments") or "{}")
                except json.JSONDecodeError as exc:
                    raise MistralError(f"Invalid arguments for tool {name}") from exc

                result = tools.execute(name, arguments)
                executed.append({"name": name, "arguments": arguments, "result": result})
                messages.append({"role": "tool", "tool_call_id": call["id"], "name": name, "content": json.dumps(result)})

        raise MistralError("AI tool-call loop exceeded safety limit")
