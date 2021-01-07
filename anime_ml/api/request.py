import json
import logging
from typing import Any, Dict, List

import requests

from anime_ml.settings import BASE_URL

try:
    with open(file="token.json") as f:
        access_token_data: Dict[str, Any] = json.load(f)
        HEADERS: Dict[str, str] = {"Authorization": f"Bearer {access_token_data.get('access_token')}"}
except FileNotFoundError:
    logging.warning("no tokens found")


def get_profile() -> Dict[Any, Any]:

    url: str = f"{BASE_URL}/users/@me"
    r = requests.get(url=url, headers=HEADERS)
    r.raise_for_status()
    return r.json()


def get_anime_list() -> List[Dict[str, Any]]:

    url: str = f"{BASE_URL}/users/@me/animelist?fields=id"
    results: List[Dict[str, Any]] = []

    # lazy pagination
    while True:
        r = requests.get(url=url, headers=HEADERS)
        r.raise_for_status()
        results.append(r.json())
        url = r.json().get("paging", {}).get("next")
        if not url:
            break

    anime_list: List[Dict[str, Any]] = []
    for r in results:
        for rr in r.get("data", []):
            anime_list.append(rr)

    return anime_list


def get_anime(anime_id: int) -> Dict[str, Any]:

    url: str = (
        f"{BASE_URL}/anime/{anime_id}?fields=id,title,alternative_titles,start_date,end_date,synopsis,"
        "mean,rank,popularity,num_list_users,num_scoring_users,nsfw,created_at,updated_at,media_type,status,genres,"
        "list_status{start_date,end_date,priority,num_times_rewatched,rewatch_value,tags,comments},num_episodes,"
        "start_season,broadcast,source,average_episode_duration,rating,pictures,background,related_anime,"
        "recommendations,studios,statistics"
    )

    r = requests.get(url=url, headers=HEADERS)
    r.raise_for_status()
    return r.json()


def get_user_stats() -> Dict[str, Any]:

    url: str = f"{BASE_URL}/users/@me?fields=anime_statistics"
    r = requests.get(url=url, headers=HEADERS)
    r.raise_for_status()
    return r.json()
