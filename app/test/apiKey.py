from dotenv import load_dotenv
import os

load_dotenv()  # load variables from .env

api_key = os.environ.get("MAILERSEND_API_KEY")
print("MailerSend key:", api_key)
