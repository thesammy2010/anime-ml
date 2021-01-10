import logging
import os

logging.basicConfig(level=logging.NOTSET, format=f"%(asctime)s - %(levelname)s - %(message)s")

BASE_URL: str = "https://api.myanimelist.net/v2"
AUTH_URL: str = "https://myanimelist.net/v1/oauth2/authorize"

CLIENT_ID: str = os.getenv("CLIENT_ID")  # type: ignore[arg-type, assignment]
CLIENT_SECRET: str = os.getenv("CLIENT_SECRET")  # type: ignore[arg-type, assignment]

if not CLIENT_ID:
    logging.warning("Client ID is missing")
if not CLIENT_SECRET:
    logging.warning("Client Secret is missing")
