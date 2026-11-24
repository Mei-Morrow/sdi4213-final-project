import secrets
from pathlib import Path

env_file = Path(".env")

if env_file.exists():
    print("Existing .env left unchanged.")
else:
    env_file.write_text(
        f"POSTGRES_PASSWORD={secrets.token_hex(24)}\n"
        "POSTGRES_HOST=127.0.0.1\n"
        "POSTGRES_PORT=5433\n"
        "POSTGRES_DB=tasktracker\n"
        "POSTGRES_USER=tasktracker\n",
        encoding="utf-8",
    )
    print("Created local .env file.")