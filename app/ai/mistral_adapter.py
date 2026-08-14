"""Mistral adapter for the controlled Douala Ride Mobility Agent."""

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
            "search_location": {"type": "function", "function": {"name": "search_location", "description": "Search for a place in Cameroon and return coordinates.", "parameters": {"type": "object", "properties": {"query": {"type": "string"}, "limit": {"type": "integer", "minimum": 1, "maximum": 10}}, "required": ["query"]}}},
            "calculate_route": {"type": "function", "function": {"name": "calculate_route", "description": "Calculate a driving route between two geographic coordinates.", "parameters": {"type": "object", "properties": {"origin_lat": {"type": "number"}, "origin_lon": {"type": "number"}, "destination_lat": {"type": "number"}, "destination_lon": {"type": "number"}}, "required": ["origin_lat", "origin_lon", "destination_lat", "destination_lon"]}}},
            "plan_trip": {"type": "function", "function": {"name": "plan_trip", "description": "Plan a complete Douala Ride journey for any pickup and destination coordinates, including real route, distance, ETA, moto/car fares and budget filtering.", "parameters": {"type": "object", "properties": {"origin": {"type": "object", "properties": {"name": {"type": "string"}, "latitude": {"type": "number"}, "longitude": {"type": "number"}}, "required": ["latitude", "longitude"]}, "destination": {"type": "object", "properties": {"name": {"type": "string"}, "latitude": {"type": "number"}, "longitude": {"type": "number"}}, "required": ["latitude", "longitude"]}, "budget_xaf": {"type": "integer", "minimum": 0}, "vehicle_type": {"type": "string", "enum": ["moto", "car"]}}, "required": ["origin", "destination"]}}},
            "estimate_fare": {"type": "function", "function": {"name": "estimate_fare", "description": "Estimate a trip fare using Douala Ride's deterministic pricing engine.", "parameters": {"type": "object", "properties": {"vehicle_type": {"type": "string", "enum": ["moto", "car"]}, "distance_km": {"type": "number"}, "duration_minutes": {"type": "integer"}}, "required": ["vehicle_type", "distance_km", "duration_minutes"]}}},
            "find_available_drivers": {"type": "function", "function": {"name": "find_available_drivers", "description": "Find verified, safe, online drivers near a pickup coordinate.", "parameters": {"type": "object", "properties": {"pickup_lat": {"type": "number"}, "pickup_lon": {"type": "number"}, "vehicle_type": {"type": "string", "enum": ["moto", "car"]}, "max_distance_km": {"type": "number"}, "limit": {"type": "integer"}}, "required": ["pickup_lat", "pickup_lon"]}}},
            "compare_transport_options": {"type": "function", "function": {"name": "compare_transport_options", "description": "Compare moto and car using route distance, duration, budget and preference.", "parameters": {"type": "object", "properties": {"distance_km": {"type": "number"}, "duration_minutes": {"type": "integer"}, "budget_xaf": {"type": "integer"}, "preferred_vehicle": {"type": "string", "enum": ["moto", "car"]}}, "required": ["distance_km", "duration_minutes"]}}},
            "create_booking": {"type": "function", "function": {"name": "create_booking", "description": "Create a passenger-confirmed pending booking and start driver search. Payment remains required before trip activation.", "parameters": {"type": "object", "properties": {"passenger_id": {"type": "integer"}, "pickup_address": {"type": "string"}, "pickup_latitude": {"type": "number"}, "pickup_longitude": {"type": "number"}, "destination_address": {"type": "string"}, "destination_latitude": {"type": "number"}, "destination_longitude": {"type": "number"}, "vehicle_type": {"type": "string", "enum": ["moto", "car"]}, "estimated_fare": {"type": "integer"}, "distance_km": {"type": "number"}, "estimated_duration_minutes": {"type": "integer"}, "confirmed": {"type": "boolean"}}, "required": ["passenger_id", "pickup_address", "pickup_latitude", "pickup_longitude", "destination_address", "destination_latitude", "destination_longitude", "vehicle_type", "estimated_fare", "distance_km", "estimated_duration_minutes", "confirmed"]}}},
            "initiate_payment": {"type": "function", "function": {"name": "initiate_payment", "description": "Initiate Mobile Money payment for an existing booking only after the passenger explicitly confirms payment.", "parameters": {"type": "object", "properties": {"booking_id": {"type": "integer"}, "amount_xaf": {"type": "integer", "minimum": 1}, "phone_number": {"type": "string"}, "provider": {"type": "string", "enum": ["MTN_MOMO_CMR", "ORANGE_CMR"]}, "confirmed": {"type": "boolean"}}, "required": ["booking_id", "amount_xaf", "phone_number", "confirmed"]}}},
            "get_payment_status": {"type": "function", "function": {"name": "get_payment_status", "description": "Read the backend payment status for a Douala Ride payment reference.", "parameters": {"type": "object", "properties": {"reference": {"type": "string"}}, "required": ["reference"]}}},
        }
        return [definitions[name] for name in tool_names if name in definitions]

    def run(self, context: dict[str, Any], tools):
        if not self.api_key:
            raise MistralError("MISTRAL_API_KEY is not configured")
        messages = [{"role": "system", "content": context["system"]}, {"role": "user", "content": context["user_message"]}]
        tool_defs = self._tool_definitions(context["available_tools"])
        for _ in range(6):
            payload = {"model": self.model, "messages": messages, "tools": tool_defs, "tool_choice": "auto", "temperature": 0.1}
            response = requests.post(f"{self.base_url.rstrip('/')}/chat/completions", headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}, json=payload, timeout=self.timeout)
            if not response.ok:
                raise MistralError(f"Mistral request failed: {response.status_code} {response.text[:500]}")
            data = response.json()
            message = data["choices"][0]["message"]
            tool_calls = message.get("tool_calls") or []
            messages.append(message)
            if not tool_calls:
                return {"message": message.get("content", ""), "tool_calls": []}
            for call in tool_calls:
                function = call["function"]
                name = function["name"]
                try:
                    arguments = json.loads(function.get("arguments") or "{}")
                except json.JSONDecodeError as exc:
                    raise MistralError(f"Invalid arguments for tool {name}") from exc
                result = tools.execute(name, arguments)
                messages.append({"role": "tool", "tool_call_id": call["id"], "name": name, "content": json.dumps(result)})
        raise MistralError("AI tool-call loop exceeded safety limit")
