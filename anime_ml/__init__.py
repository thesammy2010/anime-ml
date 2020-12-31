from .api.auth import authenticate
from .api.request import get_anime, get_anime_list, get_profile
from .cli import *  # file is empty
from .main import download_anime_details, download_anime_list, main
from .model.transform import *  # file is empty

from .api.dump import (  # isort: skip
    ANIME_DETAILS_FILE,
    ANIME_LIST_FILE,
    FEATURES_FILENAME,
    read_jsonlines,
    write_jsonlines
)
from .model.model import extract_label, create_array, create_linear_model, model_features  # isort: skip

from .settings import (BASE_URL, AUTH_URL, CLIENT_ID, CLIENT_SECRET)  # isort: skip

__version__ = "0.0.5"
