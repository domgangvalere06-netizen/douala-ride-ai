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

    from app import models  # noqa: F401

    from app.api.ai.routes import ai_bp
    from app.api.maps.routes import maps_bp
    from app.api.payments.routes import payments_bp
    from app.api.trips import trip_plan_bp
    from app.api.web.routes import web_bp
    app.register_blueprint(ai_bp)
    app.register_blueprint(maps_bp)
    app.register_blueprint(payments_bp)
    app.register_blueprint(trip_plan_bp)
    app.register_blueprint(web_bp)

    @app.get("/health")
    def health_check():
        return {"status": "ok", "service": "douala-ride-api"}, 200

    return app
