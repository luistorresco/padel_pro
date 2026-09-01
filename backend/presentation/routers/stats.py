"""Stats router."""

from fastapi import APIRouter, HTTPException

from presentation.deps_module import get_stats_uc

stats_router = APIRouter()


@stats_router.get("")
def get_stats():
    try:
        return get_stats_uc.execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
