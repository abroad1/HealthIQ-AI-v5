"""
Bearer-token auth dependency: verifies Supabase access JWT via SDK (get_user).

Returns a minimal identity object for protected routes (distinct from
core.models.user.User, which is analysis/profile domain, not Auth).
"""

from __future__ import annotations

from typing import Annotated, Any, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from gotrue.errors import AuthApiError
from gotrue.types import User as GotrueUser
from pydantic import BaseModel, ConfigDict, Field

from core.supabase_anon import get_supabase_anon_client

bearer_scheme = HTTPBearer(auto_error=True)


class CurrentUser(BaseModel):
    """Authenticated caller identity from Supabase Auth (JWT / session)."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    id: str = Field(..., description="Supabase Auth user id (matches JWT sub)")
    email: Optional[str] = Field(default=None, description="Email when present on the user")


def _gotrue_user_from_access_token(token: str) -> GotrueUser:
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing bearer token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    client = get_supabase_anon_client()
    try:
        user_resp = client.auth.get_user(token)
    except AuthApiError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc) or "Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
    if user_resp is None or user_resp.user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user_resp.user


def get_gotrue_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],
) -> GotrueUser:
    return _gotrue_user_from_access_token(credentials.credentials)


def get_current_user(user: Annotated[GotrueUser, Depends(get_gotrue_user)]) -> CurrentUser:
    return CurrentUser(id=user.id, email=user.email)


def gotrue_user_app_metadata(user: GotrueUser) -> dict[str, Any]:
    return dict(user.app_metadata or {})


def gotrue_user_user_metadata(user: GotrueUser) -> dict[str, Any]:
    return dict(user.user_metadata or {})
