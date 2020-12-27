import datetime
import logging
import os
from typing import Any, Dict, List

from anime_ml.api.auth import authenticate
from anime_ml.api.dump import (ANIME_DETAILS_FILE, ANIME_LIST_FILE,
                               DATA_FILEPATH, FEATURES_FILENAME,
                               read_jsonlines, write_jsonlines)
from anime_ml.api.request import get_anime, get_anime_list, get_profile
from anime_ml.model.features import Features
from anime_ml.model.objects import AnimeListRanking


# extract
def download_anime_list() -> bool:

    logging.info("Authenticating with API for first run")
    authenticate()

    profile: Dict[str, Any] = get_profile()
    logging.info(f"Profile details: {profile}")

    logging.info("Getting most up to date state of anime list")
    response: List[Dict[str, Any]] = get_anime_list()
    write_jsonlines(data=response, filename=ANIME_LIST_FILE)

    return True


def download_anime_details(anime: List[Dict[str, Any]] = None) -> List[Dict[str, Any]]:

    if not anime:
        anime: List[Dict[str, Any]] = read_jsonlines(filename=ANIME_LIST_FILE)

    results: List[Dict[str, Any]] = [
        get_anime(anime_id=row["node"].get("id")) for row in anime if row["node"].get("id")
    ]
    write_jsonlines(data=results, filename=ANIME_DETAILS_FILE)

    return results


def transform_data() -> List[AnimeListRanking]:

    data: List[AnimeListRanking] = []
    for row in read_jsonlines(filename=ANIME_DETAILS_FILE):
        logging.info(row.get("id"))
        data.append(AnimeListRanking(data=row))

    return data


def make_features(animelist: List[AnimeListRanking]) -> List[Features]:

    data: List[Features] = [Features(row) for row in animelist]

    write_jsonlines(data=[i.__dir__() for i in data], filename=FEATURES_FILENAME)

    return data


def main():

    download_anime_list()
    download_anime_details()
    data_2: List[AnimeListRanking] = transform_data()
    data_3: List[Features] = make_features(data_2)


if __name__ == '__main__':
    main()
