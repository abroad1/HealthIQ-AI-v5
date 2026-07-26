"""Auth token verification → controlled 401 (stale Supabase session resilience)."""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest
from fastapi import HTTPException
from gotrue.errors import AuthApiError, AuthRetryableError, AuthUnknownError

from core.dependencies.auth import _gotrue_user_from_access_token


def test_valid_token_returns_user():
    fake_user = SimpleNamespace(id=str(uuid4()), email="a@example.com")
    client = MagicMock()
    client.auth.get_user.return_value = SimpleNamespace(user=fake_user)
    with patch("core.dependencies.auth.get_supabase_anon_client", return_value=client):
        got = _gotrue_user_from_access_token("valid-token")
    assert got.id == fake_user.id
    client.auth.get_user.assert_called_once_with("valid-token")


def test_auth_api_error_401_maps_to_backend_401():
    client = MagicMock()
    client.auth.get_user.side_effect = AuthApiError("invalid JWT", 401, "bad_jwt")
    with patch("core.dependencies.auth.get_supabase_anon_client", return_value=client):
        with pytest.raises(HTTPException) as ei:
            _gotrue_user_from_access_token("expired-token")
    assert ei.value.status_code == 401
    assert "Invalid or expired" in str(ei.value.detail)


def test_auth_api_error_403_maps_to_backend_401():
    """Observed Supabase /auth/v1/user 403 must not become backend 500."""
    client = MagicMock()
    client.auth.get_user.side_effect = AuthApiError("forbidden", 403, "session_not_found")
    with patch("core.dependencies.auth.get_supabase_anon_client", return_value=client):
        with pytest.raises(HTTPException) as ei:
            _gotrue_user_from_access_token("revoked-token")
    assert ei.value.status_code == 401


def test_malformed_token_auth_unknown_maps_to_401():
    client = MagicMock()
    client.auth.get_user.side_effect = AuthUnknownError("parse failed", Exception("boom"))
    with patch("core.dependencies.auth.get_supabase_anon_client", return_value=client):
        with pytest.raises(HTTPException) as ei:
            _gotrue_user_from_access_token("not-a-jwt")
    assert ei.value.status_code == 401


def test_retryable_upstream_maps_to_503_not_401():
    client = MagicMock()
    client.auth.get_user.side_effect = AuthRetryableError("gateway", 503)
    with patch("core.dependencies.auth.get_supabase_anon_client", return_value=client):
        with pytest.raises(HTTPException) as ei:
            _gotrue_user_from_access_token("any-token")
    assert ei.value.status_code == 503


def test_empty_token_401():
    with pytest.raises(HTTPException) as ei:
        _gotrue_user_from_access_token("")
    assert ei.value.status_code == 401


def test_null_user_response_401():
    client = MagicMock()
    client.auth.get_user.return_value = SimpleNamespace(user=None)
    with patch("core.dependencies.auth.get_supabase_anon_client", return_value=client):
        with pytest.raises(HTTPException) as ei:
            _gotrue_user_from_access_token("token")
    assert ei.value.status_code == 401


def test_me_profile_db_failure_returns_500_not_401():
    from fastapi.testclient import TestClient

    from app.main import app
    from core.dependencies.auth import get_gotrue_user

    fake_user = SimpleNamespace(
        id=str(uuid4()),
        email="ok@example.com",
        app_metadata={},
        user_metadata={},
    )

    def _override():
        return fake_user

    app.dependency_overrides[get_gotrue_user] = _override
    try:
        with patch("app.routes.auth.get_db_optional") as gdb:
            # Force db path: provide a fake session and exploding repository.
            fake_db = MagicMock()
            gdb.return_value = fake_db
            # FastAPI Depends(get_db_optional) — override via dependency_overrides instead.
            pass

        from config.database import get_db_optional

        app.dependency_overrides[get_db_optional] = lambda: MagicMock()
        with patch("app.routes.auth.ProfileRepository") as Repo:
            Repo.return_value.get_by_user_id.side_effect = RuntimeError("db down")
            client = TestClient(app, raise_server_exceptions=False)
            res = client.get("/api/auth/me", headers={"Authorization": "Bearer unused"})
        assert res.status_code == 500
        assert res.status_code != 401
        assert "profile" in res.json().get("detail", "").lower()
    finally:
        app.dependency_overrides.clear()
