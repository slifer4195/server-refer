from flask import Flask
from flask_cors import CORS
from flask_session import Session
from .models import db
from .config import Config
from apscheduler.schedulers.background import BackgroundScheduler
import os
from .routes.reminder import send_weekly_reminders

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Init extensions
    db.init_app(app)
    Session(app)
    CORS(app, supports_credentials=True, origins=["http://localhost:3000"])

    # Register Blueprints
    from .routes.auth_routes import auth_bp
    from .routes.user_routes import user_bp
    from .routes.functionality import functionality
    from .routes.menu import menu_bp 
    from .routes.point_system import point_bp
    from .routes.flask_test import api_bp

    app.register_blueprint(point_bp)
    app.register_blueprint(menu_bp)
    app.register_blueprint(functionality)
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(api_bp)

    with app.app_context():
        db.create_all()

        # scheduler = BackgroundScheduler()
        # scheduler.add_job(func=send_weekly_reminders, args=[app], trigger="interval", days=7)

        # if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        #     scheduler.start()

    return app

