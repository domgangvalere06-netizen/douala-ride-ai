import os

from app import create_app
from app.config import DevelopmentConfig, ProductionConfig, TestingConfig


CONFIG_MAP = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}


environment = os.getenv("FLASK_ENV", "development")
app = create_app(CONFIG_MAP.get(environment, DevelopmentConfig))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")))
