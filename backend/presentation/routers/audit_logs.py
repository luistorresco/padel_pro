"""Audit logs router."""

import logging
from fastapi import APIRouter, Depends, HTTPException, Body
from typing import Optional

from presentation.deps_module import (
    list_audit_logs_uc,
    create_audit_log_uc,
    require_admin,
)

logger = logging.getLogger(__name__)
audit_logs_router = APIRouter()


@audit_logs_router.get("")
def get_audit_logs(payload: dict = Depends(require_admin)):
    try:
        return list_audit_logs_uc.execute()
    except Exception as e:
        logger.exception("Failed to list audit logs")
        raise HTTPException(status_code=500, detail=str(e))


@audit_logs_router.post("")
def create_audit_log(log: dict, payload: dict = Depends(require_admin)):
    try:
        return create_audit_log_uc.execute(log)
    except Exception as e:
        logger.exception("Failed to create audit log")
        raise HTTPException(status_code=500, detail=str(e))
