import logging
import os
from typing import Any, Dict, List

import numpy
from sklearn.linear_model import LinearRegression

from anime_ml.api.auth import authenticate
from anime_ml.api.request import get_anime, get_anime_list, get_profile
from anime_ml.model.model import model_features
from anime_ml.model.objects import Anime

from anime_ml.api.dump import (  # isort: skip
    ANIME_DETAILS_FILE,
    ANIME_LIST_FILE,
    DATA_FILEPATH,
    FEATURES_FILENAME,
    read_jsonlines,
    write_jsonlines
)


# extract
def download_anime_list() -> bool:

    logging.info("Authenticating with API for first run")
    authenticate()

    profile: Dict[str, Any] = get_profile().get("name")
    logging.info(f"Profile details: {profile}")

    if ANIME_LIST_FILE not in os.listdir(DATA_FILEPATH):
        logging.warning(f"{ANIME_LIST_FILE} not in {DATA_FILEPATH}. Querying from MyAnimeList")
        response: List[Dict[str, Any]] = get_anime_list()
        write_jsonlines(data=response, filename=ANIME_LIST_FILE)
    else:
        logging.info(f"{ANIME_LIST_FILE} exists, skipping")
    return True


def download_anime_details() -> bool:

    if ANIME_DETAILS_FILE in os.listdir(DATA_FILEPATH):
        logging.info(f"{ANIME_DETAILS_FILE} exists, skipping")
    else:
        anime: List[Dict[str, Any]] = read_jsonlines(filename=ANIME_LIST_FILE)
        results: List[Dict[str, Any]] = [
            get_anime(anime_id=row["node"].get("id")) for row in anime if row["node"].get("id")
        ]
        write_jsonlines(data=results, filename=ANIME_DETAILS_FILE)

    return True


def transform_data() -> List[Anime]:

    data: List[Anime] = []
    for row in read_jsonlines(filename=ANIME_DETAILS_FILE):
        # logging.debug(f"Anime id: {row.get('id')} transformed")
        data.append(Anime(data=row))

    logging.info(f"{len(data)} anime downloaded from anime list")

    return data


def main():

    download_anime_list()
    download_anime_details()
    data_1: List[Anime] = transform_data()
    data_2: LinearRegression = model_features(input_data=data_1)
    logging.info("Linear modelling complete")
    logging.info(data_2.coef_)


if __name__ == '__main__':
    main()
