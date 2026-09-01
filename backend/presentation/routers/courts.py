"""Courts router."""

from fastapi import APIRouter, Depends, HTTPException, Body
from typing import Optional

from presentation.deps_module import (
    list_courts_uc,
    get_court_uc,
    create_court_uc,
    update_court_uc,
    delete_court_uc,
    require_admin,
)

courts_router = APIRouter()


@courts_router.get("")
def get_courts():
    try:
        return list_courts_uc.execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@courts_router.get("/{court_id}")
def get_court(court_id: str):
    try:
        return get_court_uc.execute(court_id)
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@courts_router.post("")
def create_court(court: dict, payload: dict = Depends(require_admin)):
    try:
        return create_court_uc.execute(court)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@courts_router.put("/{court_id}")
def update_court(court_id: str, court: dict, payload: dict = Depends(require_admin)):
    try:
        return update_court_uc.execute(court_id, court)
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@courts_router.delete("/{court_id}")
def delete_court(court_id: str, payload: dict = Depends(require_admin)):
    try:
        return delete_court_uc.execute(court_id)
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))
