import secrets
import os

print(secrets.token_hex(32))
print("DB URL:", os.environ.get("DATABASE_URL"))
