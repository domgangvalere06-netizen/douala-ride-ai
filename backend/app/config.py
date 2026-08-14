import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-change-me")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///douala_ride.sqlite3")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-change-me")
    CORS_ORIGINS = [x.strip() for x in os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",") if x.strip()]

    MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY", "")
    MISTRAL_MODEL = os.getenv("MISTRAL_MODEL", "mistral-small-latest")

    PAWAPAY_API_TOKEN = os.getenv("PAWAPAY_API_TOKEN", "")
    PAWAPAY_BASE_URL = os.getenv("PAWAPAY_BASE_URL", "https://api.sandbox.pawapay.io")
    PAWAPAY_CALLBACK_URL = os.getenv("PAWAPAY_CALLBACK_URL", "http://localhost:5000/api/v1/payments/callback")

    OSRM_BASE_URL = os.getenv("OSRM_BASE_URL", "https://router.project-osrm.org")
