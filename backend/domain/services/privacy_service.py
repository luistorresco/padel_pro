"""Privacy service - domain logic for privacy filtering."""

from typing import Any
from domain.value_objects.privacy_settings import PrivacySettings


class PrivacyService:
    def apply_user_privacy(
        self, user: dict, privacy: PrivacySettings, viewer_is_self: bool = False
    ) -> dict:
        if viewer_is_self:
            return user
        filtered = dict(user)
        if not privacy.is_profile_public():
            filtered["name"] = ""
            filtered["surname"] = ""
            filtered["username"] = ""
            filtered["avatar"] = ""
            filtered["email"] = ""
            filtered["level"] = ""
            filtered["position"] = ""
            filtered["dominant_hand"] = ""
        if not privacy.is_points_public():
            filtered["points"] = 0
            filtered["stats"] = {}
        if not privacy.is_games_public():
            filtered["stats"] = {}
        return filtered

    def apply_match_privacy(self, match: dict, privacy_map: dict[str, PrivacySettings]) -> dict:
        mm = dict(match)
        for prefix in ["playerA1", "playerA2", "playerB1", "playerB2"]:
            user_id = match.get(f"{prefix}Id")
            if not user_id:
                continue
            priv = privacy_map.get(user_id)
            if priv and not priv.is_profile_public():
                mm[f"{prefix}Name"] = "Usuario Privado"
                mm[f"{prefix}Avatar"] = ""
        return mm
