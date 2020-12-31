from collections import defaultdict
from typing import Any, DefaultDict, Dict, List, Union


class Anime(object):

    def __init__(self, data: Dict[str, Any], is_part_of_list: bool = False):

        # title data
        self.__title__: Dict[str, Any] = data.get("alternative_titles", {})
        self.anime_id: int = data["id"]
        self.title: str = data.get("title")
        self.synonyms: str = data.get("alternative_titles", {}).get("synonyms")
        self.title_english: str = data.get("alternative_titles", {}).get("en")
        self.title_japanese: str = data.get("alternative_titles", {}).get("ja")

        # Statistics data
        self.__statistics__: Dict[str, str] = data.get("statistics", {}).get("status", {})
        self.watching: int = None if self.__statistics__.get("watching") == "" else int(self.__statistics__.get("watching"))
        self.completed: int = None if self.__statistics__.get("completed") == "" else int(self.__statistics__.get("completed"))
        self.on_hold: int = None if self.__statistics__.get("on_hold") == "" else int(self.__statistics__.get("on_hold"))
        self.dropped: int = None if self.__statistics__.get("dropped") == "" else int(self.__statistics__.get("dropped"))
        self.plan_to_watch: int = None if self.__statistics__.get("plan_to_watch") == "" else int(self.__statistics__.get("plan_to_watch"))
        self.num_list_users: int = data.get("num_list_users")
        self.community_mean_score: float = data.get("mean")
        self.community_popularity_ranking: int = data.get("popularity")
        self.community_number_of_scoring_users: int = data.get("num_scoring_users")
        for key in [
            "num_list_users",
            "community_mean_score",
            "community_popularity_ranking",
            "community_number_of_scoring_users"
        ]:
            self.__statistics__[key] = self.__getattribute__(key)

        # Studio data
        self.__studios__: List[Dict[str, Union[str, int]]] = data.get("studios", [])
        self.studio_ids: List[int] = [i.get("id") for i in self.__studios__]
        self.studio_names: List[str] = [i.get("name") for i in self.__studios__]

        # Genre data
        self.__genres__: List[Dict[str, Union[str, int]]] = data.get("genres", [])
        self.genre_ids: List[int] = [i.get("id") for i in self.__genres__]
        self.genre_names: List[str] = [i.get("name") for i in self.__genres__]

        # Related anime
        self.__related_anime__: List[Dict[str, Any]] = data.get("related_anime", [])
        self.related_anime_ids: List[int] = [i.get("node", {}).get("id") for i in self.__related_anime__]
        self.related_anime_names: List[str] = [i.get("node", {}).get("title") for i in self.__related_anime__]
        self.related_anime_aggregated_relations: DefaultDict = defaultdict(int)
        for relation_type in self.__related_anime__:
            self.related_anime_aggregated_relations[relation_type["relation_type_formatted"]] += 1

        # List status data
        self.__list_status__: Dict[str, Union[str, int, bool]] = data.get("my_list_status", {})
        self.user_watching_status: str = self.__list_status__.get("status")
        self.user_score: int = self.__list_status__.get("score")
        self.user_number_of_episodes_watched: int = self.__list_status__.get("num_episodes_watched")
        self.user_rewatching: bool = self.__list_status__.get("is_rewatching")

        # recommendation data
        self.__recommendation_data__: List[Dict[str, Any]] = data.get("recommendations", [])
        self.recommendations: List[Dict[str, int]] = [
            {"anime_id": i.get("node").get("id"), "number_of_recommendations": i.get("num_recommendations")}
            for i in self.__recommendation_data__
        ]
        self.recommendations = sorted(self.recommendations, key=lambda k: k["number_of_recommendations"])

        # metadata
        self.start_season_year: int = data.get("start_season", {}).get("year")
        self.start_season_season: str = data.get("start_season", {}).get("season")
        self.broadcast_day_of_the_week: str = data.get("broadcast", {}).get("day_of_the_week")
        self.broadcast_start_time: str = data.get("broadcast", {}).get("start_time")
        self.total_episodes: int = data.get("num_episodes")
        self.synopsis: str = data.get("synopsis")
        self.start_date: str = data.get("start_date")
        self.end_date: str = data.get("end_date")
        self.nsfw_tag_type: str = data.get("nsfw")
        self.media_type: str = data.get("media_type")
        self.airing_status: str = data.get("status")
        self.anime_source: str = data.get("source")
        self.average_episode_duration_in_minutes: int = data.get("average_episode_duration")
        self.anime_age_rating: str = data.get("rating")
        self.is_part_of_list: bool = is_part_of_list

        self.create_features()

    def __repr__(self) -> str:
        return "\n".join([f"{i}: {j}" for i, j in self.__dict__.items() if not i.startswith("_") and not i != "synopsis"])

    def create_features(self):

        self.__setattr__("three_episode_rule", True if self.user_number_of_episodes_watched >= 3 else False)
        self.__setattr__(
            "episode_percentage",
            None if not self.total_episodes else self.user_number_of_episodes_watched / self.total_episodes
        )
        self.__setattr__(
            "episode_percentage_floored",
            None if not self.total_episodes else self.user_number_of_episodes_watched // self.total_episodes
        )
        self.__setattr__(
            "episode_v_rating", None if not self.user_score else self.user_number_of_episodes_watched / self.user_score
        )
        self.__setattr__(
            "rating_v_time_spent",
            None if not self.user_number_of_episodes_watched or not self.average_episode_duration_in_minutes else
            self.user_score / (self.total_episodes * self.average_episode_duration_in_minutes)
        )

    def return_attributes(self) -> Dict[str, Any]:
        return dict({i: j for i, j in self.__dict__.items() if not i.startswith("_")})

    def return_attributes_temp(self) -> Dict[str, Union[str, int]]:
        return dict({i: j for i, j in self.__dict__.items() if i in ["anime_id", "total_episodes", "airing_status", "user_score"]})
