import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("API_KEY")
mail_pw = os.environ.get("MAIL_PW")

class Config:
    SECRET_KEY = api_key
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_TYPE = 'filesystem'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False      # keep False for local (True only in production)
    SESSION_COOKIE_SAMESITE = 'Lax'    # use 'None' only if using HTTPS + cross-site cookies

    # Use SQLite locally, Postgres on Railway
    if os.environ.get("FLASK_ENV") == "production":
        SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    else:
        SQLALCHEMY_DATABASE_URI = "sqlite:///local.db"
