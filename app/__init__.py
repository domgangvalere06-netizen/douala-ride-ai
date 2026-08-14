from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app.config import DevelopmentConfig, ProductionConfig, TestingConfig


db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()


def create_app(config_object=None):
    app = Flask(__name__)

    if config_object is None:
        config_object = DevelopmentConfig

    app.config.from_object(config_object)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    origins = app.config.get("CORS_ORIGINS", "*")
    CORS(app, origins=[item.strip() for item in origins.split(",")])

    # Import models so SQLAlchemy metadata knows every table before migrations.
    from app import models  # noqa: F401

    @app.get("/health")
    def health_check():
        return {"status": "ok", "service": "douala-ride-api"}, 200

    return app
