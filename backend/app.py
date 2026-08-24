import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv


load_dotenv()


db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.getenv(
        "SECRET_KEY",
        "development-secret"
    )

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL",
        "sqlite:///hostel_manager.db"
    )

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    CORS(app)

    from backend.routes.auth import auth_bp
    from backend.routes.complaints import complaints_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(complaints_bp)

    with app.app_context():
        from backend.models.user import User
        from backend.models.room import Room
        from backend.models.complaint import Complaint

        db.create_all()

    return app
