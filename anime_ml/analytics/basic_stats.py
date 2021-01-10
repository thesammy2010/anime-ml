import datetime
import json
import logging
from collections import defaultdict, namedtuple
from typing import Any, DefaultDict, Dict, List, NamedTuple, Union

from anime_ml.model.objects import Anime


class Statistics(object):

    def __init__(self, animelist: List[Anime]):
        self.animelist = animelist
        if not animelist:
            logging.warning("Animelist is empty! Cannot provide any statistics")
            return

        # self.__setattr__("Your List Ranked by the Community Score", self._highest_ranked_anime_by_mal())
        self.__setattr__("user_watching_status", self.get_field_aggregates(field="user_watching_status"))
        self.__setattr__("genre_names", self.get_field_aggregates(field="genre_names", _type="list"))
        self.__setattr__("studio_names", self.get_field_aggregates(field="studio_names", _type="list"))
        self.__setattr__("media_type", self.get_field_aggregates(field="media_type"))
        self.__setattr__("anime_source", self.get_field_aggregates(field="anime_source"))
        self.__setattr__("anime_age_rating", self.get_field_aggregates(field="anime_age_rating"))
        self.__setattr__("priority", self.get_field_aggregates(field="priority"))
        self.__setattr__("number_of_times_rewatched", self.get_field_aggregates(field="number_of_times_rewatched"))
        self.__setattr__("rewatch_value", self.get_field_aggregates(field="rewatch_value"))
        self.__setattr__("recommendations", self._recommendations())
        self.__setattr__("Anime watched per day", self._number_of_anime_per_day())

    def __repr__(self) -> str:
        return json.dumps(self.data(), indent=4)

    def data(self) -> Dict[str, Any]:
        data: Dict[str, Any] = self.__dict__
        data.pop("animelist")
        return data

    def _limit_fields(self, anime: Anime, additional_fields: List[str] = []) -> Dict[str, Any]:
        fields: List[str] = ["id", "title", "title_english"] + additional_fields
        return {i: getattr(anime, i) for i in fields}

    def _highest_ranked_anime_by_mal(self) -> List[Dict[str, Any]]:
        ranked_list: List[Anime] = sorted(self.animelist, key=lambda a: a.community_mean_score, reverse=True)
        return [
            self._limit_fields(anime=a, additional_fields=["community_mean_score", "user_score"]) for a in ranked_list
        ]

    def get_field_aggregates(self, field: str, _type: str = "string") -> Dict[str, int]:

        aggregates_dict: DefaultDict[str, int] = defaultdict(int)

        for a in self.animelist:
            if _type == "list":
                for f in getattr(a, field):
                    aggregates_dict[str(f)] += 1
            else:
                aggregates_dict[getattr(a, field)] += 1

        return dict(aggregates_dict)

    def _number_of_anime_per_day(self) -> Dict[str, int]:

        # min starting_date
        AiringDate: NamedTuple = namedtuple(typename="AiringDate", field_names=["start_date", "finish_date"])

        dates: List[AiringDate] = [
            AiringDate(start_date=a.user_start_date_date, finish_date=a.user_finish_date_date) for a in self.animelist
            if a.user_start_date_date is not None and a.user_finish_date_date is not None
        ]
        sorted_dates: List[AiringDate] = sorted(dates, key=lambda q: q.start_date)
        min_start_date: datetime.date = sorted_dates[0].start_date
        end_date: datetime.date = datetime.date.today()
        date_diff: int = (end_date - min_start_date).days

        # do counts per day
        results: DefaultDict[str, int] = defaultdict(int)
        for day in range(date_diff + 1):
            date: datetime.date = min_start_date + datetime.timedelta(days=day)  # 2020-10-01
            for d in sorted_dates:
                if d.start_date <= date <= d.finish_date:
                    results[date.isoformat()] += 1

        return dict(results)

    def _recommendations(self) -> Dict[str, int]:

        rec: DefaultDict[str, int] = defaultdict(int)

        for a in self.animelist:
            for r in a.recommendations:
                rec[r["anime_id"]] += r["number_of_recommendations"]

        return dict(rec)
