"""
Paywall for POST /api/analysis/start (Sprint 7).
First N completed analyses free; unlimited while subscription_status is active.
"""

from __future__ import annotations

import os

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from core.dependencies.auth import CurrentUser
from core.profile_bridge import ensure_profile_for_auth_user
from repositories import AnalysisRepository, ProfileRepository


def _free_completed_cap() -> int:
    raw = (os.getenv("HEALTHIQ_FREE_COMPLETED_ANALYSES") or "1").strip()
    try:
        n = int(raw)
    except ValueError:
        return 1
    return max(0, n)


def enforce_new_analysis_entitlement(db: Session, auth_user: CurrentUser) -> None:
    """
    Raise 402 when the user has exhausted free completed analyses and is not subscribed.
    Does not block reads of existing results.
    """
    owner_uuid = ensure_profile_for_auth_user(db, auth_user)
    profile_repo = ProfileRepository(db)
    profile = profile_repo.get_by_user_id(owner_uuid)
    sub = (profile.subscription_status or "free").strip().lower() if profile else "free"
    if sub == "active":
        return

    completed = AnalysisRepository(db).count_completed_by_user_id(owner_uuid)
    cap = _free_completed_cap()
    if completed >= cap:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail={
                "error": "upgrade_required",
                "message": (
                    "Your included analysis allotment is used. Subscribe to run further analyses. "
                    "You can still view results from tests you already completed."
                ),
                "completed_analyses": completed,
                "free_limit": cap,
            },
        )
