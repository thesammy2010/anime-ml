from .analytics.basic_stats import Statistics
from .api.auth import authenticate
from .api.request import get_anime, get_anime_list, get_profile
from .cli import *  # file is empty
from .main import download_anime_details, download_anime_list, main

from .api.dump import (  # isort: skip
    ANIME_DETAILS_FILENAME,
    ANIME_LIST_FILENAME,
    STATISTICS_FILENAME,
    FEATURES_FILENAME,
    read_jsonlines,
    write_jsonlines
)
from .model.model import extract_label, create_array, create_linear_model, model_features  # isort: skip
from .settings import (BASE_URL, AUTH_URL, CLIENT_ID, CLIENT_SECRET)  # isort: skip

__version__ = "0.1.0"
