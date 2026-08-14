from flask import current_app
from mistralai import Mistral


class AIService:
    def __init__(self):
        self.api_key = current_app.config.get("MISTRAL_API_KEY")
        self.model = current_app.config.get("MISTRAL_MODEL", "mistral-small-latest")

    def plan_trip(self, user_request: str) -> dict:
        if not self.api_key:
            return {"status": "unconfigured", "message": "Mistral API key is not configured."}

        client = Mistral(api_key=self.api_key)
        response = client.chat.complete(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are Douala Ride's mobility assistant. Help plan urban trips in Douala. "
                        "Never claim a payment, booking, route, or database action was completed unless a backend tool confirms it."
                    ),
                },
                {"role": "user", "content": user_request},
            ],
        )
        return {"status": "ok", "message": response.choices[0].message.content}
