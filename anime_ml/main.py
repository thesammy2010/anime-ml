import json
import logging
import os
from typing import Any, Dict, List

from anime_ml import __version__
from anime_ml.analytics.basic_stats import Statistics, report
from anime_ml.api.auth import authenticate
from anime_ml.api.request import get_anime, get_anime_list, get_profile
from anime_ml.model.ml import ml  # type: ignore[attr-defined]
from anime_ml.model.objects import Anime  # type: ignore[attr-defined]

from anime_ml.api.dump import (  # isort: skip
    ANIME_DETAILS_FILENAME,
    ANIME_LIST_FILENAME,
    DATA_FILEPATH,
    FEATURES_FILENAME,
    read_jsonlines,
    STATISTICS_FILENAME,
    write_jsonlines
)


# download data
def download_anime_list() -> bool:

    logging.info("Authenticating with API for first run")
    authenticate()

    profile: Dict[str, Any] = get_profile().get("name")
    logging.info(f"Authenticated user: {profile}")

    if ANIME_LIST_FILENAME not in os.listdir(DATA_FILEPATH):
        logging.warning(f"{ANIME_LIST_FILENAME} not in {DATA_FILEPATH}. Querying from MyAnimeList")
        response: List[Dict[str, Any]] = get_anime_list()
        write_jsonlines(data=response, filename=ANIME_LIST_FILENAME)
    else:
        logging.info(f"{ANIME_LIST_FILENAME} exists, skipping")
    return True


def download_anime_details() -> bool:

    if ANIME_DETAILS_FILENAME in os.listdir(DATA_FILEPATH):
        logging.info(f"{ANIME_DETAILS_FILENAME} exists, skipping")
    else:
        anime: List[Dict[str, Any]] = read_jsonlines(filename=ANIME_LIST_FILENAME)
        results: List[Dict[str, Any]] = [
            get_anime(anime_id=row["node"].get("id")) for row in anime if row["node"].get("id")
        ]
        write_jsonlines(data=results, filename=ANIME_DETAILS_FILENAME)

    return True


# transform data into Anime objects
def transform_data() -> List[Anime]:

    data: List[Anime] = []
    for row in read_jsonlines(filename=ANIME_DETAILS_FILENAME):
        # logging.debug(f"Anime id: {row.get('id')} transformed")
        data.append(Anime(data=row, is_part_of_list=True))

    logging.info(f"{len(data)} anime downloaded from anime list")

    return data


def write_features_to_disk(data: List[Anime]) -> bool:
    logging.info(f"writing features data to {FEATURES_FILENAME}")
    write_jsonlines(
        data=(a.features_dict() for a in data), filename=FEATURES_FILENAME
    )
    return True


def ml_recommend():
    # based on the ML model, what to predict
    # also look at the plan to watch column as a separate column
    pass


def main():
    logging.info("")
    logging.info("---------------------------------------")
    logging.info(f"--- Running anime-ml [ver: {__version__}] ---")
    logging.info("---------------------------------------")
    logging.info("")

    download_anime_list()
    download_anime_details()
    data_1: List[Anime] = transform_data()

    logging.info("Calculating List Statistics")
    data_2: Statistics = Statistics(data_1)
    with open(file=f"{DATA_FILEPATH}/{STATISTICS_FILENAME}", mode="w") as f:
        json.dump(obj=data_2.data(), fp=f, indent=4)
    data_3: List[str] = report(stats=data_2)

    logging.info("")
    logging.info("---------------------------------------")
    for i in data_3:
        logging.info(i)
    logging.info("---------------------------------------")
    logging.info("")

    logging.info("Calculating features")
    write_features_to_disk(data=data_1)
    ml()


if __name__ == '__main__':
    main()
