"""Pairs router."""

from fastapi import APIRouter, Depends, HTTPException, Body
from typing import Optional

from presentation.deps_module import (
    list_pairs_uc,
    get_pair_uc,
    create_pair_uc,
    delete_pair_uc,
    get_current_user,
    require_admin,
)

pairs_router = APIRouter()


@pairs_router.get("")
def get_pairs():
    try:
        return list_pairs_uc.execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@pairs_router.get("/{pair_id}")
def get_pair(pair_id: str):
    try:
        return get_pair_uc.execute(pair_id)
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@pairs_router.post("")
def create_pair(pair: dict, payload: dict = Depends(get_current_user)):
    try:
        return create_pair_uc.execute(pair)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@pairs_router.delete("/{pair_id}")
def delete_pair(pair_id: str, payload: dict = Depends(require_admin)):
    try:
        return delete_pair_uc.execute(pair_id)
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))
