from flask import Flask
from flask_cors import CORS
from .config import Config
from .extensions import db, jwt


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    jwt.init_app(app)
    CORS(app, origins=app.config["CORS_ORIGINS"])

    from .routes.health import health_bp
    from .routes.auth import auth_bp
    from .routes.trips import trips_bp
    from .routes.payments import payments_bp
    from .routes.ai import ai_bp

    app.register_blueprint(health_bp, url_prefix="/api/v1")
    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")
    app.register_blueprint(trips_bp, url_prefix="/api/v1/trips")
    app.register_blueprint(payments_bp, url_prefix="/api/v1/payments")
    app.register_blueprint(ai_bp, url_prefix="/api/v1/ai")

    return app
