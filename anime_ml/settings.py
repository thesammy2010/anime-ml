import logging
import os

logging.basicConfig(level=logging.NOTSET, format=f"%(asctime)s - %(levelname)s - %(message)s")

BASE_URL: str = "https://api.myanimelist.net/v2"
AUTH_URL: str = "https://myanimelist.net/v1/oauth2/authorize"

CLIENT_ID: str = os.getenv("CLIENT_ID")
CLIENT_SECRET: str = os.getenv("CLIENT_SECRET")
