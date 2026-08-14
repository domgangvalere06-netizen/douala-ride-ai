"""PawaPay Mobile Money integration boundary.

Credentials and provider-specific details stay server-side. The adapter is
intentionally isolated so the rest of the application depends on our stable
PaymentProvider contract.
"""

import os
from typing import Any

import requests


class PawaPayError(RuntimeError):
    pass


class PawaPayClient:
    def __init__(self, api_token: str | None = None, base_url: str | None = None, timeout: int = 15):
        self.api_token = api_token or os.getenv("PAWAPAY_API_TOKEN")
        self.base_url = (base_url or os.getenv("PAWAPAY_BASE_URL", "https://api.pawapay.io")).rstrip("/")
        self.timeout = timeout

    def initiate(self, reference: str, amount_xaf: int, phone_number: str, description: str = "Douala Ride trip") -> dict[str, Any]:
        if not self.api_token:
            raise PawaPayError("PAWAPAY_API_TOKEN is not configured")

        # PawaPay's exact provider payload can vary by collection method and
        # currency/channel. Keep this adapter isolated and configure the
        # provider-specific payload from environment/configuration before live use.
        payload = {
            "reference": reference,
            "amount": str(amount_xaf),
            "currency": "XAF",
            "phoneNumber": phone_number,
            "description": description,
        }
        response = requests.post(
            f"{self.base_url}/v2/deposits",
            headers={"Authorization": f"Bearer {self.api_token}", "Content-Type": "application/json"},
            json=payload,
            timeout=self.timeout,
        )
        if not response.ok:
            raise PawaPayError(f"PawaPay request failed: {response.status_code} {response.text[:500]}")

        data = response.json()
        return {"provider": "pawapay", "status": data.get("status", "PENDING"), "raw": data}

    def verify_webhook(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Normalize a provider callback; signature verification belongs here."""
        if not isinstance(payload, dict):
            raise PawaPayError("Invalid webhook payload")
        return {
            "reference": payload.get("reference"),
            "status": payload.get("status"),
            "provider": "pawapay",
            "raw": payload,
        }
