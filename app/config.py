import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-jwt-secret-change-me")

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "mysql+pymysql://douala_ride:password@localhost:3306/douala_ride",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
    MISTRAL_MODEL = os.getenv("MISTRAL_MODEL", "mistral-small-latest")
    MISTRAL_BASE_URL = os.getenv("MISTRAL_BASE_URL", "https://api.mistral.ai/v1")

    OSRM_BASE_URL = os.getenv("OSRM_BASE_URL", "https://router.project-osrm.org")
    NOMINATIM_BASE_URL = os.getenv(
        "NOMINATIM_BASE_URL", "https://nominatim.openstreetmap.org"
    )

    PAWAPAY_API_URL = os.getenv("PAWAPAY_API_URL", "https://api.sandbox.pawapay.io")
    PAWAPAY_API_TOKEN = os.getenv("PAWAPAY_API_TOKEN")
    PAWAPAY_PROVIDER = os.getenv("PAWAPAY_PROVIDER", "MTN_MOMO_CMR")
    PAWAPAY_CALLBACK_URL = os.getenv("PAWAPAY_CALLBACK_URL")

    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_URL", "sqlite:///:memory:")


class ProductionConfig(Config):
    DEBUG = False
