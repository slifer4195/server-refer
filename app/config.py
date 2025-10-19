import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("API_KEY")

class Config:
    SECRET_KEY = api_key 
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SESSION_TYPE = 'filesystem'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = True        # must be True for HTTPS
    SESSION_COOKIE_SAMESITE = 'None'    # allow cross-site requests
