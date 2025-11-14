from flask import Flask
from flask_cors import CORS
from flask_session import Session
import os

from app.models import db
from app.config import Config
from apscheduler.schedulers.background import BackgroundScheduler
from app.routes.reminder import send_weekly_reminders

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize database and session
    db.init_app(app)
    Session(app)

    # Global CORS setup
    CORS(
        app,
        supports_credentials=True,
        origins=[
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "http://localhost:5000",
        ]
    )

    # Register Blueprints
    from app.routes.auth_routes import auth_bp
    from app.routes.user_routes import user_bp
    from app.routes.functionality import functionality
    from app.routes.menu import menu_bp 
    from app.routes.point_system import point_bp
    from app.routes.flask_test import api_bp

    app.register_blueprint(point_bp)
    app.register_blueprint(menu_bp)
    app.register_blueprint(functionality)
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(api_bp)

    # Create tables only (don’t drop)
    with app.app_context():
        db.create_all()

    return app
