"""
First-party wedge analytics ingestion (WEDGE-METRICS-B).

Persists minimised events to structured logs (append-only operational stream).
Does not touch analytical / Intelligence Core pipelines.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from typing import Annotated, Literal, Optional

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, Field, field_validator

from core.dependencies.auth import _gotrue_user_from_access_token

logger = logging.getLogger("healthiq.wedge_events")

router = APIRouter(tags=["wedge-events"])

optional_bearer = HTTPBearer(auto_error=False)

ALLOWED_EVENTS = frozenset(
    [
        "wedge_auth_register_completed",
        "wedge_auth_register_failed",
        "wedge_auth_login_success",
        "wedge_auth_login_failed",
        "wedge_upload_started",
        "wedge_upload_parse_completed",
        "wedge_upload_parse_failed",
        "wedge_questionnaire_submitted",
        "wedge_analysis_started",
        "wedge_analysis_completed",
        "wedge_analysis_failed",
        "wedge_results_viewed",
        "wedge_clinician_report_viewed",
        "wedge_results_export_json_clicked",
        "wedge_results_share_link_clicked",
        "wedge_analysis_reopened_from_history",
    ]
)


class WedgeEventIn(BaseModel):
    event_name: str = Field(..., min_length=8, max_length=80)
    timestamp: str = Field(..., min_length=10, max_length=40)
    env: Literal["development", "staging", "production"]
    route: Optional[str] = Field(default=None, max_length=200)
    analysis_id: Optional[str] = Field(default=None, max_length=80)
    entry: Optional[Literal["fresh", "from_url", "from_history"]] = None
    source: Optional[Literal["file", "paste"]] = None
    error_class: Optional[str] = Field(default=None, max_length=64)
    phase: Optional[str] = Field(default=None, max_length=64)

    @field_validator("event_name")
    @classmethod
    def validate_event_name(cls, v: str) -> str:
        if v not in ALLOWED_EVENTS:
            raise ValueError("unknown or disallowed event_name for Phase 1 contract")
        return v


@router.post("", status_code=status.HTTP_204_NO_CONTENT)
async def ingest_wedge_event(
    body: WedgeEventIn,
    credentials: Annotated[Optional[HTTPAuthorizationCredentials], Depends(optional_bearer)],
) -> Response:
    user_sub: Optional[str] = None
    if credentials and credentials.credentials:
        try:
            user = _gotrue_user_from_access_token(credentials.credentials)
            user_sub = str(user.id)
        except HTTPException:
            user_sub = None

    payload = body.model_dump(exclude_none=True)
    payload["received_at_utc"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    if user_sub:
        payload["user_sub"] = user_sub

    logger.info(json.dumps(payload, sort_keys=True))
    return Response(status_code=status.HTTP_204_NO_CONTENT)
