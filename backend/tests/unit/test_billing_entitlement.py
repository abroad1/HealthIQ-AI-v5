"""Sprint 7 paywall: entitlement uses completed analysis count vs free cap."""

from __future__ import annotations

from unittest.mock import MagicMock, patch
from uuid import UUID, uuid4

import pytest
from fastapi import HTTPException

from app.billing_entitlement import enforce_new_analysis_entitlement
from core.dependencies.auth import CurrentUser


def _patch_repos(m, *, sub_status: str, completed: int, owner_uuid: UUID | None = None):
    uid = owner_uuid or uuid4()
    m.setattr(
        "app.billing_entitlement.ensure_profile_for_auth_user",
        lambda _db, _a: uid,
    )
    prof = MagicMock()
    prof.subscription_status = sub_status
    prof_repo = MagicMock()
    prof_repo.get_by_user_id = MagicMock(return_value=prof)
    prof_cls = MagicMock(return_value=prof_repo)
    m.setattr("app.billing_entitlement.ProfileRepository", prof_cls)

    ar_repo = MagicMock()
    ar_repo.count_completed_by_user_id = MagicMock(return_value=completed)
    ar_cls = MagicMock(return_value=ar_repo)
    m.setattr("app.billing_entitlement.AnalysisRepository", ar_cls)


def test_entitlement_allows_when_under_cap(monkeypatch):
    monkeypatch.setenv("HEALTHIQ_FREE_COMPLETED_ANALYSES", "1")
    db = MagicMock()
    auth = CurrentUser(id=str(uuid4()), email="t@example.com")

    with pytest.MonkeyPatch.context() as m:
        _patch_repos(m, sub_status="free", completed=0)
        enforce_new_analysis_entitlement(db, auth)


def test_entitlement_blocks_402_when_at_cap(monkeypatch):
    monkeypatch.setenv("HEALTHIQ_FREE_COMPLETED_ANALYSES", "1")
    monkeypatch.delenv("HEALTHIQ_DISABLE_BILLING_ENFORCEMENT", raising=False)
    db = MagicMock()
    auth = CurrentUser(id=str(uuid4()), email="t@example.com")

    with pytest.MonkeyPatch.context() as m:
        _patch_repos(m, sub_status="free", completed=1)
        with pytest.raises(HTTPException) as ei:
            enforce_new_analysis_entitlement(db, auth)
        assert ei.value.status_code == 402


def test_entitlement_bypassed_when_disable_billing_enforcement_flag(monkeypatch):
    """HEALTHIQ_DISABLE_BILLING_ENFORCEMENT truthy skips paywall; no profile/402 path."""
    monkeypatch.setenv("HEALTHIQ_DISABLE_BILLING_ENFORCEMENT", "1")
    monkeypatch.setenv("HEALTHIQ_FREE_COMPLETED_ANALYSES", "1")
    db = MagicMock()
    auth = CurrentUser(id=str(uuid4()), email="t@example.com")

    with patch("app.billing_entitlement.ensure_profile_for_auth_user") as ep:
        enforce_new_analysis_entitlement(db, auth)
        ep.assert_not_called()


def test_entitlement_still_402_at_cap_when_bypass_flag_false(monkeypatch):
    """Explicit 0 (false) does not enable bypass — default entitlement applies."""
    monkeypatch.setenv("HEALTHIQ_DISABLE_BILLING_ENFORCEMENT", "0")
    monkeypatch.setenv("HEALTHIQ_FREE_COMPLETED_ANALYSES", "1")
    db = MagicMock()
    auth = CurrentUser(id=str(uuid4()), email="t@example.com")

    with pytest.MonkeyPatch.context() as m:
        _patch_repos(m, sub_status="free", completed=1)
        with pytest.raises(HTTPException) as ei:
            enforce_new_analysis_entitlement(db, auth)
        assert ei.value.status_code == 402


def test_entitlement_ignores_cap_when_active(monkeypatch):
    monkeypatch.setenv("HEALTHIQ_FREE_COMPLETED_ANALYSES", "1")
    db = MagicMock()
    auth = CurrentUser(id=str(uuid4()), email="t@example.com")

    with pytest.MonkeyPatch.context() as m:
        _patch_repos(m, sub_status="active", completed=99)
        enforce_new_analysis_entitlement(db, auth)
