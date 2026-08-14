"""PawaPay Mobile Money integration boundary for Cameroon.

The adapter keeps provider credentials server-side and exposes the stable
PaymentProvider contract used by the application.
"""

import os
import uuid
from typing import Any

import requests


class PawaPayError(RuntimeError):
    pass


class PawaPayClient:
    def __init__(self, api_token: str | None = None, base_url: str | None = None, timeout: int = 15):
        self.api_token = api_token or os.getenv("PAWAPAY_API_TOKEN")
        self.base_url = (base_url or os.getenv("PAWAPAY_API_URL", os.getenv("PAWAPAY_BASE_URL", "https://api.sandbox.pawapay.io"))).rstrip("/")
        self.default_provider = os.getenv("PAWAPAY_PROVIDER", "MTN_MOMO_CMR")
        self.timeout = timeout

    def initiate(self, reference: str, amount_xaf: int, phone_number: str, description: str = "Douala Ride trip", provider: str | None = None) -> dict[str, Any]:
        if not self.api_token:
            raise PawaPayError("PAWAPAY_API_TOKEN is not configured")
        if amount_xaf <= 0:
            raise ValueError("Payment amount must be positive")
        if not phone_number.strip():
            raise ValueError("Phone number is required")

        deposit_id = str(uuid.uuid4())
        payload = {
            "depositId": deposit_id,
            "amount": str(amount_xaf),
            "currency": "XAF",
            "payer": {
                "type": "MMO",
                "accountDetails": {
                    "phoneNumber": phone_number.strip(),
                    "provider": provider or self.default_provider,
                },
            },
            "clientReferenceId": reference,
            "customerMessage": description[:22],
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
        initiation_status = data.get("status", "REJECTED")
        normalized_status = "PROCESSING" if initiation_status in {"ACCEPTED", "PROCESSING"} else "FAILED"
        return {
            "provider": "pawapay",
            "status": normalized_status,
            "deposit_id": data.get("depositId", deposit_id),
            "raw": data,
        }

    def verify_webhook(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Normalize a PawaPay deposit callback.

        Signed-callback verification should be enabled and enforced before
        production deployment when signed callbacks are configured in PawaPay.
        """
        if not isinstance(payload, dict):
            raise PawaPayError("Invalid webhook payload")
        status = payload.get("status")
        if status not in {"COMPLETED", "FAILED", "PROCESSING"}:
            raise PawaPayError("Unsupported PawaPay callback status")
        return {
            "reference": payload.get("clientReferenceId"),
            "deposit_id": payload.get("depositId"),
            "status": status,
            "provider_transaction_id": payload.get("providerTransactionId"),
            "failure_reason": payload.get("failureReason"),
            "provider": "pawapay",
            "raw": payload,
        }
