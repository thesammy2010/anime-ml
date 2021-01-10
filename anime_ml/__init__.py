__version__ = "0.2.0"

from .analytics.basic_stats import Statistics, report
from .api.auth import authenticate
from .api.request import get_anime, get_anime_list, get_profile
from .cli import *  # file is empty
from .main import download_anime_details, download_anime_list, main
from .model.ml import ml  # type: ignore[attr-defined]
from .model.objects import Anime  # type: ignore[attr-defined]

from .api.dump import (  # isort: skip
    ANIME_DETAILS_FILENAME,
    ANIME_LIST_FILENAME,
    STATISTICS_FILENAME,
    FEATURES_FILENAME,
    read_jsonlines,
    write_jsonlines
)

from .settings import (BASE_URL, AUTH_URL, CLIENT_ID, CLIENT_SECRET)  # isort: skip
