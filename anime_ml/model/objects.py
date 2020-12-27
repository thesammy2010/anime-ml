import json
from collections import defaultdict
from typing import Any, DefaultDict, Dict, List


class base(object):
    def __init__(self, data):
        self._data = data

    def __repr__(self):
        return json.dumps({i: j for i, j in self.__dict__.items() if i != "_data"})


class Title(base):

    def __init__(self, data) -> None:
        super().__init__(data=data)
        self.main: str = self._data.get("title")
        self.synonyms: str = self._data.get("alternative_titles", {}).get("synonyms")
        self.english: str = self._data.get("alternative_titles", {}).get("en")
        self.japanese: str = self._data.get("alternative_titles", {}).get("ja")

    def __str__(self) -> str:
        return self.main


class Dates(base):

    def __init__(self, data):
        super().__init__(data=data)

        for i, j in self._data.items():
            if i in ["start_date", "end_date", "created_at", "updated_at"]:
                self.__setattr__(i, j)

    def __repr__(self) -> str:
        return json.dumps({i: str(j) for i, j in self.__dict__.items() if i != "_data" and j})


class Statistics(base):

    def __init__(self, data):
        super().__init__(data=data)

        stats: Dict[str, Any] = self._data.get("statistics", {})
        status: Dict[str, str] = stats.get("status")

        self.users: int = stats.get("num_list_users")
        for i, j in status.items():
            self.__setattr__(i, None if j == "" else int(j))


class ListStatus(base):

    def __init__(self, data):
        super().__init__(data=data)

        for i, j in self._data.get("my_list_status", {}).items():
            self.__setattr__(i, j)


class RelatedAnime(base):

    def __init__(self, data):
        super().__init__(data=data)

        related_anime: List[Dict[str, Any]] = self._data.get("related_anime", [])
        self.ids: List[int] = [i.get("node", {}).get("id") for i in related_anime]
        self.names: List[str] = [i.get("node", {}).get("title") for i in related_anime]

        relation_types: DefaultDict = defaultdict(int)
        types: List[str] = [i.get("relation_type") for i in related_anime]
        for i in types:
            relation_types[i] += 1
        for i, j in relation_types.items():
            self.__setattr__(i, j)


class Studios(base):

    def __init__(self, data):
        super().__init__(data=data)

        self.ids: List[int] = [i.get("id") for i in self._data.get("studios", [])]
        self.names: List[str] = [i.get("name") for i in self._data.get("studios", [])]


class Genres(base):

    def __init__(self, data):
        super().__init__(data=data)

        genre_names: DefaultDict = defaultdict(int)
        genres: List[str] = [i.get("name") for i in self._data.get("genres", [])]
        for i in genres:
            genre_names[i] += 1
        for i, j in genre_names.items():
            self.__setattr__(i, j)


class Anime(base):

    def __init__(self, data):
        super().__init__(data=data)
        self._data: Dict[str, Any] = data
        self.set_attributes()
        self.__setattr__("Title", Title(data=self._data))
        self.__setattr__("Dates", Dates(data=self._data))
        self.__setattr__("Statistics", Statistics(data=self._data))
        self.__setattr__("Studios", Studios(data=self._data))
        self.__setattr__("RelatedAnime", RelatedAnime(data=self._data))
        self.__setattr__("Genres", Genres(data=self._data))

        # start season
        self.start_season_year: int = self._data.get("start_season", {}).get("year")
        self.start_season_season: str = self._data.get("start_season", {}).get("season")

        # broadcast
        self.broadcast_day_of_the_week: str = self._data.get("broadcast", {}).get("day_of_the_week")
        self.broadcast_start_time: str = self._data.get("broadcast", {}).get("start_time")

    def set_attributes(self) -> None:

        excluded: List[str] = [
            "title", "alternative_titles", "start_date", "end_date", "created_at", "updated_at",
        ]

        for i, j in self._data.items():
            if not isinstance(j, dict) and not isinstance(j, list) and i not in excluded:
                self.__setattr__(i, j)

    def __repr__(self) -> str:
        return "\n".join([f"{i}: {j}" for i, j in self.__dict__.items() if i != "_data" and j])


class AnimeListRanking(Anime):

    def __init__(self, data):

        super().__init__(data=data)
        self.__setattr__("ListStatus", ListStatus(data=self._data))
