import datetime
from collections import defaultdict
from typing import Any, DefaultDict, Dict, List, Union


class Anime(object):

    def __init__(self, data: Dict[str, Any], is_part_of_list: bool = False):

        # title data
        self.anime_id: int = data["id"]
        self.title: str = data.get("title")
        self.synonyms: str = data.get("alternative_titles", {}).get("synonyms")
        self.title_english: str = data.get("alternative_titles", {}).get("en")
        self.title_japanese: str = data.get("alternative_titles", {}).get("ja")

        # Statistics data
        stats: Dict[str, str] = data.get("statistics", {}).get("status", {})
        self.watching: int = None if stats.get("watching") == "" else int(stats.get("watching"))
        self.completed: int = None if stats.get("completed") == "" else int(stats.get("completed"))
        self.on_hold: int = None if stats.get("on_hold") == "" else int(stats.get("on_hold"))
        self.dropped: int = None if stats.get("dropped") == "" else int(stats.get("dropped"))
        self.plan_to_watch: int = None if stats.get("plan_to_watch") == "" else int(stats.get("plan_to_watch"))
        self.num_list_users: int = data.get("num_list_users")
        self.community_mean_score: float = data.get("mean")
        self.community_popularity_ranking: int = data.get("popularity")
        self.community_number_of_scoring_users: int = data.get("num_scoring_users")

        # Studio data
        self.studio_ids: List[int] = [i.get("id") for i in data.get("studios", [])]
        self.studio_names: List[str] = [i.get("name") for i in data.get("studios", [])]

        # Genre data
        self.genre_ids: List[int] = [i.get("id") for i in data.get("genres", [])]
        self.genre_names: List[str] = [i.get("name") for i in data.get("genres", [])]

        # Related anime
        self.related_anime_ids: List[int] = [i.get("node", {}).get("id") for i in data.get("related_anime", [])]
        self.related_anime_names: List[str] = [i.get("node", {}).get("title") for i in data.get("related_anime", [])]
        self.related_anime_aggregated_relations: DefaultDict = defaultdict(int)
        for relation_type in data.get("related_anime", []):
            self.related_anime_aggregated_relations[relation_type["relation_type_formatted"]] += 1

        # List status data
        self.user_watching_status: str = data.get("my_list_status", {}).get("status")
        self.user_score: int = data.get("my_list_status", {}).get("score")
        self.user_number_of_episodes_watched: int = data.get("my_list_status", {}).get("num_episodes_watched")
        self.user_rewatching: bool = data.get("my_list_status", {}).get("is_rewatching")
        self.user_start_date: str = data.get("my_list_status", {}).get("start_date")
        self.user_finish_date: str = data.get("my_list_status", {}).get("finish_date")
        self.updated_at: str = data.get("my_list_status", {}).get("updated_at")
        self.priority: int = data.get("my_list_status", {}).get("priority")
        self.number_of_times_rewatched: int = data.get("my_list_status", {}).get("num_times_rewatched")
        self.rewatch_value: int = data.get("my_list_status", {}).get("rewatch_value")

        # recommendation data
        self.recommendations: List[Dict[str, int]] = [
            {"anime_id": i.get("node").get("id"), "number_of_recommendations": i.get("num_recommendations")}
            for i in data.get("recommendations", [])
        ]
        self.recommendations = sorted(self.recommendations, key=lambda k: k["number_of_recommendations"])

        # metadata
        self.start_season_year: int = data.get("start_season", {}).get("year")
        self.start_season_season: str = data.get("start_season", {}).get("season")
        self.broadcast_day_of_the_week: str = data.get("broadcast", {}).get("day_of_the_week")
        self.broadcast_start_time: str = data.get("broadcast", {}).get("start_time")
        self.total_episodes: int = data.get("num_episodes")
        self.synopsis: str = data.get("synopsis")
        self.series_image_url: str = data.get("main_picture", {}).get("large")
        self.start_date: str = data.get("start_date")
        self.finish_date: str = data.get("finish_date")
        self.nsfw_tag_type: str = data.get("nsfw")
        self.media_type: str = data.get("media_type")
        self.airing_status: str = data.get("status")
        self.anime_source: str = data.get("source")
        self.average_episode_duration_in_seconds: int = data.get("average_episode_duration")
        self.anime_age_rating: str = data.get("rating")
        self.is_part_of_list: bool = is_part_of_list

        # extra features
        try:
            self.user_start_date_date: datetime.date = datetime.date.fromisoformat(self.user_start_date)
        except (ValueError, TypeError):
            self.user_start_date_date = None
        try:
            self.user_finish_date_date: datetime.date = datetime.date.fromisoformat(self.user_finish_date)
        except (ValueError, TypeError):
            self.user_finish_date_date = None

        self.three_episode_rule: bool = self._calculate_three_episode_rule()
        self.series_progress: float = self._calculate_series_progress()
        self.days_watched: int = self._calculate_days_watched()
        self.user_completed: bool = self._calculate_completed()

    def _calculate_days_watched(self) -> Union[None, int]:

        if not self.user_start_date_date or not self.user_finish_date_date:
            return
        else:
            return (self.user_finish_date_date - self.user_start_date_date).days

    def _calculate_series_progress(self) -> Union[None, float]:
        if not self.total_episodes:
            return
        else:
            return self.user_number_of_episodes_watched / self.total_episodes

    def _calculate_three_episode_rule(self) -> bool:
        return True if self.user_number_of_episodes_watched >= 3 else False

    def _calculate_completed(self) -> bool:

        if (
                self.finish_date
                or self.user_rewatching
                or self.total_episodes == self.user_number_of_episodes_watched
                or self.number_of_times_rewatched
                or self.user_watching_status == "completed"
        ):
            return True
        else:
            return False

    def features_dict(self) -> Dict[str, Any]:
        return {i: j for i, j in self.__dict__.items() if i not in ["synopsis", "data"]}

    def __repr__(self) -> str:
        return str(self.features_dict())
