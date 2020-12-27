import datetime

from anime_ml.model.objects import AnimeListRanking


class Features(object):

    def __init__(self, anime: AnimeListRanking, is_on_list: bool = True):

        self.anime_id: int = getattr(anime, "id")
        self.is_on_list = is_on_list

        # dynamic features
        # user
        self.score: int = getattr(anime, "ListStatus", {}).get("score")
        self.watching_status: str = getattr(anime, "ListStatus", {}).get("status")
        self.number_of_episodes_watched: int = getattr(anime, "ListStatus", {}).get("num_episodes_watched")
        self.rewatching: bool = getattr(anime, "ListStatus", {}).get("is_rewatching")
        last_updated: str = getattr(anime, "ListStatus", {}).get("updated_at")

        # anime
        # genre data
        for genre, case in getattr(anime, "Genres", {}).items():
            self.__setattr__(genre, bool(case))
        # studio data
        for studio, case in getattr(anime, "Studios", {}).items():
            self.__setattr__(studio, bool(case))
        # types of related anime
        for relation, case in getattr(anime, "RelatedAnime", {}).items():
            self.__setattr__(relation, bool(case))
        self.num_episodes: int = getattr(anime, "num_episodes")
        self.status: str = getattr(anime, "status")
        self.average_episode_duration: float = getattr(anime, "average_episode_duration")

        # stats
        self.mean_community_rating: float = getattr(anime, "mean")
        self.popularity_ranking: float = getattr(anime, "popularity")
        self.number_of_users_in_community: int = getattr(anime, "num_list_users")
        self.number_of_users_rated: int = getattr(anime, "num_scoring_users")
        self.number_of_users_watching: int = getattr(anime, "Statistics", {}).get("watching")
        self.number_of_users_completed: int = getattr(anime, "Statistics", {}).get("completed")
        self.number_of_users_on_hold: int = getattr(anime, "Statistics", {}).get("on_hold")
        self.number_of_users_dropped: int = getattr(anime, "Statistics", {}).get("dropped")
        self.number_of_users_plan_to_watch: int = getattr(anime, "Statistics", {}).get("plan_to_watch")

        # static features
        self.synopsis: str = getattr(anime, "synopsis")
        self.start_season: str = getattr(anime, "start_season_season") + getattr(anime, "start_season_year")
        self.start_season_year: int = int(getattr(anime, "start_season_year"))
        self.start_season_season: str = getattr(anime, "start_season_season")
        self.rating: str = getattr(anime, "rating")
        self.source: str = getattr(anime, "source")
        self.media_type: str = getattr(anime, "media_type")
        self.nsfw_rating: str = getattr(anime, "nsfw")

        # custom features
        self.three_episode_rule: bool = True if self.number_of_episodes_watched > 3 else False
        self.episode_percentage: float = (
            None if not self.num_episodes else
            self.number_of_episodes_watched / self.num_episodes
        )
        self.episode_percentage_floored: int = (
            None if not self.num_episodes else
            self.number_of_episodes_watched // self.num_episodes
        )
        self.episode_v_rating: float = (
            None if not self.rating else
            self.number_of_episodes_watched / self.score
        )
        self.rating_v_time_spent: float = (
            None if not self.number_of_episodes_watched or not self.average_episode_duration else
            self.score / (self.num_episodes * self.average_episode_duration)
        )
        self.completed_month = (
            None if self.watching_status != "completed" or not last_updated else
            datetime.datetime.fromisoformat(last_updated).month
        )
        self.completed_year = (
            None if self.watching_status != "completed" or not last_updated else
            datetime.datetime.fromisoformat(last_updated).year
        )

        self.calculated_weight_1 = self.calculated_weight_1()

    def calculated_weight_1(self):
        # weighted feature

        weight: float = 0
        if self.three_episode_rule:
            weight += 2
        if self.watching_status == "completed":
            weight += 2
        if self.watching_status == "dropped":
            weight -= 1
        try:
            if self.Adverture or self.Mystery:
                weight += 3
        except AttributeError:
            pass

        weight += self.episode_percentage

        return weight
