import os
import json
import boto3
from dotenv import load_dotenv

load_dotenv()  # still load local .env for local dev

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_TYPE = 'filesystem'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False      # True only if using HTTPS
    SESSION_COOKIE_SAMESITE = 'Lax'

    # --- Check if running on EC2 (production) ---
    is_ec2 = os.path.exists("/sys/hypervisor/uuid") or os.path.exists("/sys/devices/virtual/dmi/id/product_uuid")

    if is_ec2:
        # --- Fetch DB credentials from AWS Secrets Manager ---
        secrets_client = boto3.client("secretsmanager", region_name="us-east-2")
        secret_value = secrets_client.get_secret_value(
            SecretId='rds!db-b8a71aed-fd5d-4cbb-b8d1-4c4484f913fc'
        )
        secret = json.loads(secret_value["SecretString"])

        DB_USER = secret["username"]
        DB_PASSWORD = secret["password"]
        DB_HOST = "referdb.cbemcy8c28z4.us-east-2.rds.amazonaws.com"
        DB_PORT = "5432"
        DB_NAME = "refer_db"

        SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

        # --- Fetch MAIL_PW from SSM Parameter Store ---
        ssm_client = boto3.client("ssm", region_name="us-east-2")
        MAIL_PW = ssm_client.get_parameter(
            Name="/MAIL_PW",  # your parameter name in SSM
            WithDecryption=True
        )["Parameter"]["Value"]
    else:
        # --- Local development uses .env ---
        SQLALCHEMY_DATABASE_URI = "sqlite:///local.db"
        MAIL_PW = os.environ.get("MAIL_PW")
