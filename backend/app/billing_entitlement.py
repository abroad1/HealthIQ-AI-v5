"""
Paywall for POST /api/analysis/start (Sprint 7).
First N completed analyses free; unlimited while subscription_status is active.

Free-tier cap: set ``HEALTHIQ_FREE_COMPLETED_ANALYSES`` (integer, >= 0).
If unset or empty, the process default is 1. Invalid values fall back to 1.
Local/dev templates in ``backend/.env.example`` set 99 for repeat UAT; production
should leave this unset (1) or set explicitly—never commit real secrets in .env.

**Local manual testing only:** set ``HEALTHIQ_DISABLE_BILLING_ENFORCEMENT`` to ``1``,
``true``, or ``yes`` to skip all paywall checks in ``enforce_new_analysis_entitlement``
(``POST /api/analysis/start``). Must be **absent or false in production.**
"""

from __future__ import annotations

import logging
import os

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from core.dependencies.auth import CurrentUser
from core.profile_bridge import ensure_profile_for_auth_user
from repositories import AnalysisRepository, ProfileRepository

logger = logging.getLogger(__name__)


def _free_completed_cap() -> int:
    # Config-only; default 1 when unset (see module docstring).
    raw = (os.getenv("HEALTHIQ_FREE_COMPLETED_ANALYSES") or "1").strip()
    try:
        n = int(raw)
    except ValueError:
        return 1
    return max(0, n)


def _billing_enforcement_disabled() -> bool:
    """True when local/dev should skip paywall (env only; never use in production)."""
    v = (os.getenv("HEALTHIQ_DISABLE_BILLING_ENFORCEMENT") or "").strip().lower()
    return v in ("1", "true", "yes")


def enforce_new_analysis_entitlement(db: Session, auth_user: CurrentUser) -> None:
    """
    Raise 402 when the user has exhausted free completed analyses and is not subscribed.
    Does not block reads of existing results.
    """
    if _billing_enforcement_disabled():
        logger.warning(
            "HEALTHIQ_DISABLE_BILLING_ENFORCEMENT is active: skipping new-analysis billing checks (dev only)"
        )
        return
    owner_uuid = ensure_profile_for_auth_user(db, auth_user)
    profile_repo = ProfileRepository(db)
    profile = profile_repo.get_by_user_id(owner_uuid)
    sub = (profile.subscription_status or "free").strip().lower() if profile else "free"
    if sub == "active":
        if os.getenv("HEALTHIQ_DEBUG_ENTITLEMENT", "").strip().lower() in ("1", "true", "yes"):
            raw = (os.getenv("HEALTHIQ_FREE_COMPLETED_ANALYSES") or "(unset)").strip()
            logger.info(
                "entitlement: user_id=%s subscription_status=%s completed=(n/a) free_cap=%s "
                "HEALTHIQ_FREE_COMPLETED_ANALYSES_raw=%s branch=allow_subscribed",
                owner_uuid,
                sub,
                _free_completed_cap(),
                raw,
            )
        return

    completed = AnalysisRepository(db).count_completed_by_user_id(owner_uuid)
    cap = _free_completed_cap()
    if os.getenv("HEALTHIQ_DEBUG_ENTITLEMENT", "").strip().lower() in ("1", "true", "yes"):
        raw = (os.getenv("HEALTHIQ_FREE_COMPLETED_ANALYSES") or "(unset)").strip()
        logger.info(
            "entitlement: user_id=%s subscription_status=%s completed=%s free_cap=%s "
            "HEALTHIQ_FREE_COMPLETED_ANALYSES_raw=%s branch=%s",
            owner_uuid,
            sub,
            completed,
            cap,
            raw,
            "block_402_free_exhausted" if completed >= cap else "allow_free_tier",
        )
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
