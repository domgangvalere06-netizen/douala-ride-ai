"""Schemas used at the AI boundary.

The model is allowed to propose structured actions, but application code
validates every action before execution.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class ToolCall:
    name: str
    arguments: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class MobilityPlan:
    origin_text: str | None = None
    destination_text: str | None = None
    budget_xaf: int | None = None
    departure_time: str | None = None
    preferred_vehicle: str | None = None
    needs_confirmation: bool = True
