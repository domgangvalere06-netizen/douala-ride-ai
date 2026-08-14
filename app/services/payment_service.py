"""Payment domain service and provider contract."""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Protocol


class PaymentStatus(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"


@dataclass(frozen=True)
class PaymentIntent:
    reference: str
    amount_xaf: int
    currency: str
    status: PaymentStatus
    provider: str
    provider_reference: str | None = None


class PaymentProvider(Protocol):
    def initiate(self, reference: str, amount_xaf: int, phone_number: str, description: str, **kwargs: Any) -> dict[str, Any]: ...


class PaymentService:
    def __init__(self, provider: PaymentProvider):
        self.provider = provider

    def initiate(self, reference: str, amount_xaf: int, phone_number: str, description: str = "Douala Ride trip", **kwargs: Any) -> PaymentIntent:
        if amount_xaf <= 0:
            raise ValueError("Payment amount must be positive")
        if not phone_number or not phone_number.strip():
            raise ValueError("Phone number is required")
        result = self.provider.initiate(reference, amount_xaf, phone_number, description, **kwargs)
        status = PaymentStatus(result.get("status", PaymentStatus.PENDING))
        return PaymentIntent(
            reference,
            amount_xaf,
            "XAF",
            status,
            result.get("provider", "unknown"),
            result.get("deposit_id"),
        )
