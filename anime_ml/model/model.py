from typing import Any, Dict, List, Tuple

import numpy
from sklearn import linear_model
from sklearn.feature_extraction import DictVectorizer

from anime_ml.model.objects import Anime


def extract_label(anime: Anime) -> (int, int, Dict[str, Any]):
    """

    :param anime:
    :return: Row ID, User Score (label), dictionary of features
    """
    data: Dict[str, Any] = anime.return_attributes_temp()
    return data.pop("anime_id"), data.pop("user_score"), data


def create_array(data: List[Dict[str, Any]]) -> numpy.ndarray:
    vector = DictVectorizer()
    return vector.fit_transform(data).toarray()


def create_linear_model(labels: List[int], array_data: numpy.ndarray) -> linear_model.LinearRegression():
    reg = linear_model.LinearRegression()
    reg.fit(X=array_data, y=labels)
    return reg


def model_features(input_data: List[Anime]) -> linear_model.LinearRegression():

    anime_objects_sorted: List[Anime] = sorted(input_data, key=lambda x: x.anime_id)
    anime_objects_separated: List[Tuple[int, int, Dict[str, str]]] = [extract_label(a) for a in anime_objects_sorted]
    anime_ids, labels, anime_features = (
        [i[0] for i in anime_objects_separated],
        [i[1] for i in anime_objects_separated],
        create_array([i[2] for i in anime_objects_separated])
    )

    model = create_linear_model(array_data=anime_features, labels=labels)

    return model
