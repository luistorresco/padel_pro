"""Privacy settings value object."""


class PrivacySettings:
    def __init__(
        self,
        user_id: str,
        profile_visibility: str = "PUBLIC",
        points_visibility: str = "PUBLIC",
        games_visibility: str = "PUBLIC",
        tournaments_visibility: str = "PUBLIC",
    ):
        self.user_id = user_id
        self.profile_visibility = profile_visibility
        self.points_visibility = points_visibility
        self.games_visibility = games_visibility
        self.tournaments_visibility = tournaments_visibility

    def is_profile_public(self) -> bool:
        return self.profile_visibility == "PUBLIC"

    def is_points_public(self) -> bool:
        return self.points_visibility == "PUBLIC"

    def is_games_public(self) -> bool:
        return self.games_visibility == "PUBLIC"
