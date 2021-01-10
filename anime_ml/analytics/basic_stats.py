import datetime
import json
import logging
from collections import defaultdict, namedtuple
from typing import Any, DefaultDict, Dict, List, NamedTuple, Union

from anime_ml.api.request import get_anime
from anime_ml.model.objects import Anime  # type: ignore[attr-defined]


class Statistics(object):

    def __init__(self, animelist: List[Anime]):
        self.animelist = animelist
        if not animelist:
            logging.warning("Animelist is empty! Cannot provide any statistics")
            return
        self.number_of_anime: int = len(self.animelist)
        # self.__setattr__("Your List Ranked by the Community Score", self._highest_ranked_anime_by_mal())
        self.user_watching_status: Dict[str, int] = self.get_field_aggregates(field="user_watching_status")
        self.genre_names: Dict[str, int] = self.get_field_aggregates(field="genre_names", _type="list")
        self.studio_names: Dict[str, int] = self.get_field_aggregates(field="studio_names", _type="list")
        self.media_type: Dict[str, int] = self.get_field_aggregates(field="media_type")
        self.anime_source: Dict[str, int] = self.get_field_aggregates(field="anime_source")
        self.anime_age_rating: Dict[str, int] = self.get_field_aggregates(field="anime_age_rating")
        self.priority: Dict[str, int] = self.get_field_aggregates(field="priority")
        self.number_of_times_rewatched: Dict[str, int] = self.get_field_aggregates(field="number_of_times_rewatched")
        self.rewatch_value: Dict[str, int] = self.get_field_aggregates(field="rewatch_value")
        self.recommendations: Dict[str, int] = self._recommendations()
        self.user_score: Dict[str, int] = self.get_field_aggregates(field="user_score")
        self.anime_watched_per_day: Dict[str, int] = self._number_of_anime_per_day()

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
        ranked_list: List[Anime] = sorted(self.animelist, key=lambda a: a.community_mean_score, reverse=True)  # type: ignore[no-any-return]  # fmt: off
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
        AiringDate: NamedTuple = namedtuple(typename="AiringDate", field_names=["start_date", "finish_date"])  # type: ignore[misc]  # fmt: off

        dates: List[AiringDate] = [
            AiringDate(start_date=a.user_start_date_date, finish_date=a.user_finish_date_date)  # type: ignore[call-arg]
            for a in self.animelist if a.user_start_date_date is not None and a.user_finish_date_date is not None
        ]
        sorted_dates: List[AiringDate] = sorted(dates, key=lambda q: q.start_date)  # type: ignore[no-any-return, attr-defined]  # fmt: off
        min_start_date: datetime.date = sorted_dates[0].start_date  # type: ignore[attr-defined]
        end_date: datetime.date = datetime.date.today()
        date_diff: int = (end_date - min_start_date).days

        # do counts per day
        results: DefaultDict[str, int] = defaultdict(int)
        for day in range(date_diff + 1):
            date: datetime.date = min_start_date + datetime.timedelta(days=day)  # 2020-10-01
            for d in sorted_dates:
                if d.start_date <= date <= d.finish_date:  # type: ignore[attr-defined]
                    results[date.isoformat()] += 1

        return dict(results)

    def _recommendations(self) -> Dict[str, int]:

        rec: DefaultDict[str, int] = defaultdict(int)

        for a in self.animelist:
            for r in a.recommendations:
                rec[r["anime_id"]] += r["number_of_recommendations"]

        return dict(rec)


def report(stats: Statistics) -> List[str]:
    logging.info("Here's a generated report based on the aggregate data in your anime list")

    fav_genre: str = sorted(stats.genre_names, key=stats.genre_names.get, reverse=True)[0]  # type: ignore[arg-type]
    top_studio: str = sorted(stats.studio_names, key=stats.studio_names.get, reverse=True)[0]   # type: ignore[arg-type]
    media_type: str = sorted(stats.media_type, key=stats.media_type.get, reverse=True)[0]  # type: ignore[arg-type]
    anime_source: str = sorted(stats.anime_source, key=stats.anime_source.get, reverse=True)[0]  # type: ignore[arg-type] # fmt:off
    anime_age_rating: str = sorted(stats.anime_age_rating, key=stats.anime_age_rating.get, reverse=True)[0]  # type: ignore[arg-type] # fmt: off
    top_recommended_id: str = sorted(stats.recommendations, key=stats.recommendations.get, reverse=True)[0]  # type: ignore[arg-type] # fmt: off
    top_recommended: Anime = Anime(data=get_anime(anime_id=int(top_recommended_id)))  # type: ignore[arg-type]

    data: List[str] = [
        f"Your most common genre is {fav_genre}!",
        f"Your most common studio is {top_studio}!",
        f"Your most common media type is {media_type}",
        f"Your most common anime source is {anime_source}",
        f"Your most common age rating to watch is {anime_age_rating}",
        f"Based on community recommendations, you're recommended to watch {top_recommended.title} "
        f"(id={top_recommended.anime_id})",
    ]

    return data
