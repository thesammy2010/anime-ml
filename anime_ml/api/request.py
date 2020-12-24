import json
import logging
from typing import Any, Dict, List

import requests

from anime_ml.settings import BASE_URL

with open(file="token.json") as f:
    access_token_data: Dict[str, Any] = json.load(f)
    HEADERS: Dict[str, str] = {"Authorization": f"Bearer {access_token_data.get('access_token')}"}


def get_profile() -> Dict[Any, Any]:

    url: str = f"{BASE_URL}/users/@me"
    r = requests.get(url=url, headers=HEADERS)
    r.raise_for_status()
    return r.json()


def get_anime_list() -> List[Dict[str, Any]]:

    url: str = f"{BASE_URL}/users/@me/animelist"
    results: List[Dict[str, Any]] = []

    # lazy pagination
    while True:
        r = requests.get(url=url, headers=HEADERS)
        r.raise_for_status()
        results.append(r.json())
        url = r.json().get("paging", {}).get("next")
        if not url:
            break
        logging.info("New URL: " + url)

    return results


def get_anime(anime_id: str) -> Dict[str, Any]:

    url: str = f"{BASE_URL}/anime/{anime_id}"

    r = requests.get(url=url, headers=HEADERS)
    r.raise_for_status()
    return r.json()
