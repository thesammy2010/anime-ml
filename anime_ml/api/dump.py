import datetime
import json
from typing import Any, Dict, Iterable, List

date: str = datetime.date.today().isoformat()

ANIME_LIST_FILENAME: str = f"{date}-anime-list.json"
ANIME_DETAILS_FILENAME: str = f"{date}-anime-details.json"
FEATURES_FILENAME: str = f"{date}-features.json"
STATISTICS_FILENAME: str = f"{date}-statistics.json"
DATA_FILEPATH: str = "anime_ml/data"


def write_jsonlines(data: Iterable[Dict[str, Any]], filename: str) -> bool:

    with open(file=f"{DATA_FILEPATH}/{filename}", mode="w") as f:
        for row in data:
            json.dump(obj=row, fp=f)
            f.write("\n")

    return True


def read_jsonlines(filename: str) -> List[Dict[str, str]]:

    data: List[Dict[str, str]] = []
    with open(file=f"{DATA_FILEPATH}/{filename}", mode="r") as f:
        for row in f:
            data.append(json.loads(row))

    return data
