"""Tournaments router."""

from fastapi import APIRouter, Depends, HTTPException, Body
from typing import Optional

from presentation.deps_module import (
    list_tournaments_uc,
    get_tournament_uc,
    get_tournament_full_uc,
    create_tournament_uc,
    update_tournament_uc,
    delete_tournament_uc,
    register_for_tournament_uc,
    require_admin,
)

tournaments_router = APIRouter()


@tournaments_router.get("")
def get_tournaments():
    try:
        return list_tournaments_uc.execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@tournaments_router.get("/{tournament_id}")
def get_tournament(tournament_id: str):
    try:
        return get_tournament_uc.execute(tournament_id)
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@tournaments_router.get("/{tournament_id}/full")
def get_tournament_full(tournament_id: str):
    try:
        return get_tournament_full_uc.execute(tournament_id)
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@tournaments_router.post("")
def create_tournament(tournament: dict, payload: dict = Depends(require_admin)):
    try:
        return create_tournament_uc.execute(tournament)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@tournaments_router.put("/{tournament_id}")
def update_tournament(tournament_id: str, tournament: dict, payload: dict = Depends(require_admin)):
    try:
        return update_tournament_uc.execute(tournament_id, tournament)
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@tournaments_router.delete("/{tournament_id}")
def delete_tournament(tournament_id: str, payload: dict = Depends(require_admin)):
    try:
        return delete_tournament_uc.execute(tournament_id)
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@tournaments_router.post("/{tournament_id}/register")
def register_for_tournament(tournament_id: str, body: dict, payload: dict = Depends(require_admin)):
    try:
        return register_for_tournament_uc.execute(tournament_id, body, payload.get("sub", ""))
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@tournaments_router.post("/{tournament_id}/register_user")
def register_user_for_tournament(tournament_id: str, body: dict, payload: dict = Depends(require_admin)):
    try:
        return register_for_tournament_uc.execute(tournament_id, body, payload.get("sub", ""))
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))
