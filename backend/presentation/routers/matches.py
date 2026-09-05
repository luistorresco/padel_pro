"""Matches router."""

from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
import json

from presentation.deps_module import (
    list_matches_uc,
    get_match_uc,
    get_match_players_uc,
    create_match_uc,
    update_match_court_uc,
    update_match_date_time_uc,
    update_match_uc,
    finish_match_uc,
    create_match_event_uc,
    delete_match_uc,
    require_admin,
    container,
    privacy_service,
)
from domain.value_objects.privacy_settings import PrivacySettings

matches_router = APIRouter()


def _get_privacy(user_id: str) -> PrivacySettings:
    try:
        privacy = container.user_repo.find_privacy(user_id)
        return PrivacySettings(
            user_id=user_id,
            profile_visibility=privacy.get("profile_visibility", "PUBLIC"),
            points_visibility=privacy.get("points_visibility", "PUBLIC"),
            games_visibility=privacy.get("games_visibility", "PUBLIC"),
            tournaments_visibility=privacy.get("tournaments_visibility", "PUBLIC"),
        )
    except Exception:
        return PrivacySettings(user_id=user_id)


def _apply_privacy_to_matches(matches):
    user_ids = set()
    for m in matches:
        for uid in [
            m.get("playerA1Id"), m.get("playerA2Id"),
            m.get("playerB1Id"), m.get("playerB2Id"),
        ]:
            if uid:
                user_ids.add(uid)
    privacy_map = {}
    for uid in user_ids:
        privacy_map[uid] = _get_privacy(uid)
    result = []
    for m in matches:
        mm = dict(m)
        for prefix in ["playerA1", "playerA2", "playerB1", "playerB2"]:
            uid = m.get(f"{prefix}Id")
            if not uid:
                continue
            priv = privacy_map.get(uid, {})
            if priv and not priv.is_profile_public():
                mm[f"{prefix}Name"] = "Usuario Privado"
                mm[f"{prefix}Avatar"] = ""
        result.append(mm)
    return result


@matches_router.get("")
def get_matches():
    try:
        matches = list_matches_uc.execute()
        return _apply_privacy_to_matches(matches)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@matches_router.get("/{match_id}")
def get_match(match_id: str):
    try:
        m = get_match_uc.execute(match_id)
        return _apply_privacy_to_matches([m])[0]
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@matches_router.get("/{match_id}/players")
def get_match_players(match_id: str):
    try:
        return get_match_players_uc.execute(match_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@matches_router.post("")
def create_match(match: dict, payload: dict = Depends(require_admin)):
    try:
        return create_match_uc.execute(match)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@matches_router.put("/{match_id}/court")
def update_match_court(match_id: str, body: dict):
    try:
        return update_match_court_uc.execute(match_id, body)
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@matches_router.put("/{match_id}/datetime")
def update_match_datetime(match_id: str, body: dict):
    try:
        return update_match_date_time_uc.execute(match_id, body)
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@matches_router.put("/{match_id}")
def update_match(match_id: str, body: dict):
    try:
        return update_match_uc.execute(match_id, body)
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@matches_router.post("/{match_id}/finish")
def finish_match(match_id: str, body: dict):
    try:
        m = get_match_uc.execute(match_id)
        if m.status == 'FINISHED':
            return {"status": "finished", "matchId": match_id, "alreadyFinished": True}
        return finish_match_uc.execute(match_id, body)
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@matches_router.post("/{match_id}/events")
def create_match_event(match_id: str, event: dict):
    try:
        return create_match_event_uc.execute(match_id, event)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@matches_router.delete("/{match_id}")
def delete_match(match_id: str, payload: dict = Depends(require_admin)):
    try:
        return delete_match_uc.execute(match_id)
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))
