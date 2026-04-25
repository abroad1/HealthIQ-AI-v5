"""
Supabase Auth–backed HTTP surface for FE-FOUNDATION-A.

Contract for FE-FOUNDATION-B: JSON shapes below are stable; use Authorization:
Bearer <access_token> for /me. Logout is client-side token discard for JWT flows.
"""

from __future__ import annotations

from typing import Annotated, Any, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from gotrue.errors import AuthError
from gotrue.types import User as GotrueUser
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from config.database import get_db_optional
from core.dependencies.auth import (
    get_gotrue_user,
    gotrue_user_app_metadata,
    gotrue_user_user_metadata,
)
from core.supabase_anon import get_supabase_anon_client
from repositories import ProfileRepository

router = APIRouter(prefix="/auth", tags=["auth"])


class RegisterRequest(BaseModel):
    email: str = Field(..., min_length=3)
    password: str = Field(..., min_length=8)


class LoginRequest(BaseModel):
    email: str = Field(..., min_length=3)
    password: str = Field(..., min_length=1)


class UserIdentity(BaseModel):
    id: str
    email: Optional[str] = None


class SessionPayload(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int
    token_type: str
    expires_at: Optional[int] = None


class AuthSessionResponse(BaseModel):
    user: UserIdentity
    session: SessionPayload


class MeResponse(BaseModel):
    """Current user + optional metadata for future profile linkage (profiles.id == user.id)."""

    user: UserIdentity
    app_metadata: dict[str, Any] = Field(default_factory=dict)
    user_metadata: dict[str, Any] = Field(default_factory=dict)
    subscription_status: Optional[str] = Field(
        default=None,
        description="profiles.subscription_status when DATABASE_URL is configured",
    )


class LogoutResponse(BaseModel):
    ok: bool = True
    detail: str = "Discard access and refresh tokens on the client."


def _session_from_gotrue(session: Any) -> SessionPayload:
    return SessionPayload(
        access_token=session.access_token,
        refresh_token=session.refresh_token,
        expires_in=session.expires_in,
        token_type=session.token_type or "bearer",
        expires_at=session.expires_at,
    )


def _identity_from_gotrue_user(user: Any) -> UserIdentity:
    return UserIdentity(id=user.id, email=user.email)


def _http_exception_from_gotrue(exc: AuthError, *, default_status: int) -> HTTPException:
    """Map any GoTrue AuthError (not only AuthApiError) to an HTTP error response."""
    status_code = getattr(exc, "status", None)
    if isinstance(status_code, int) and 400 <= status_code < 600:
        code = status_code
    elif status_code == 0:
        code = status.HTTP_503_SERVICE_UNAVAILABLE
    else:
        code = default_status
    detail = getattr(exc, "message", None) or str(exc) or "Authentication request failed"
    return HTTPException(status_code=code, detail=detail)


def _get_anon_client():
    try:
        return get_supabase_anon_client()
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc


@router.post(
    "/register",
    response_model=AuthSessionResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(body: RegisterRequest) -> AuthSessionResponse:
    client = _get_anon_client()
    try:
        res = client.auth.sign_up({"email": body.email, "password": body.password})
    except AuthError as exc:
        raise _http_exception_from_gotrue(
            exc, default_status=status.HTTP_400_BAD_REQUEST
        ) from exc
    if res.session is None or res.user is None:
        raise HTTPException(
            status_code=status.HTTP_202_ACCEPTED,
            detail="Registration accepted; confirm email if required before sign-in.",
        )
    return AuthSessionResponse(
        user=_identity_from_gotrue_user(res.user),
        session=_session_from_gotrue(res.session),
    )


@router.post("/login", response_model=AuthSessionResponse)
def login(body: LoginRequest) -> AuthSessionResponse:
    client = _get_anon_client()
    try:
        res = client.auth.sign_in_with_password(
            {"email": body.email, "password": body.password}
        )
    except AuthError as exc:
        raise _http_exception_from_gotrue(
            exc, default_status=status.HTTP_401_UNAUTHORIZED
        ) from exc
    if res.session is None or res.user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sign-in did not return a session",
        )
    return AuthSessionResponse(
        user=_identity_from_gotrue_user(res.user),
        session=_session_from_gotrue(res.session),
    )


@router.get("/me", response_model=MeResponse)
def me(
    user: Annotated[GotrueUser, Depends(get_gotrue_user)],
    db: Annotated[Optional[Session], Depends(get_db_optional)],
) -> MeResponse:
    subscription_status: Optional[str] = None
    if db is not None:
        try:
            uid = UUID(user.id)
        except ValueError:
            uid = None
        if uid is not None:
            profile = ProfileRepository(db).get_by_user_id(uid)
            if profile is not None:
                subscription_status = profile.subscription_status

    return MeResponse(
        user=_identity_from_gotrue_user(user),
        app_metadata=gotrue_user_app_metadata(user),
        user_metadata=gotrue_user_user_metadata(user),
        subscription_status=subscription_status,
    )


@router.post("/logout", response_model=LogoutResponse)
def logout() -> LogoutResponse:
    return LogoutResponse()
