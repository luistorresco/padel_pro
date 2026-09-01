"""Audit logs router."""

from fastapi import APIRouter, Depends, HTTPException, Body
from typing import Optional

from presentation.deps_module import (
    list_audit_logs_uc,
    create_audit_log_uc,
    require_admin,
)

audit_logs_router = APIRouter()


@audit_logs_router.get("")
def get_audit_logs(payload: dict = Depends(require_admin)):
    try:
        return list_audit_logs_uc.execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@audit_logs_router.post("")
def create_audit_log(log: dict, payload: dict = Depends(require_admin)):
    try:
        return create_audit_log_uc.execute(log)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
