import requests
from flask import current_app


class PawaPayService:
    """Payment adapter. Credentials stay in environment variables."""

    def create_payment(self, amount: int, phone: str, external_id: str) -> dict:
        token = current_app.config.get("PAWAPAY_API_TOKEN")
        base_url = current_app.config.get("PAWAPAY_BASE_URL")
        callback_url = current_app.config.get("PAWAPAY_CALLBACK_URL")

        if not token:
            return {"status": "unconfigured", "message": "PawaPay token is not configured."}

        # Provider-specific payload should be finalized against the active PawaPay account/API version.
        payload = {
            "amount": str(amount),
            "currency": "XAF",
            "externalId": external_id,
            "customerMsisdn": phone,
            "callbackUrl": callback_url,
        }
        response = requests.post(
            f"{base_url.rstrip('/')}/v2/deposits",
            json=payload,
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            timeout=20,
        )
        response.raise_for_status()
        return response.json()
