import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("API_KEY")

class Config:
    SECRET_KEY = api_key
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")  # <-- use Railway DB
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SESSION_TYPE = 'filesystem'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_SAMESITE = 'Lax'