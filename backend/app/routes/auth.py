"""
Supabase Auth–backed HTTP surface for FE-FOUNDATION-A.

Contract for FE-FOUNDATION-B: JSON shapes below are stable; use Authorization:
Bearer <access_token> for /me. Logout is client-side token discard for JWT flows.
"""

from __future__ import annotations

from typing import Annotated, Any, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from gotrue.errors import AuthApiError
from gotrue.types import User as GotrueUser
from pydantic import BaseModel, Field

from core.dependencies.auth import (
    get_gotrue_user,
    gotrue_user_app_metadata,
    gotrue_user_user_metadata,
)
from core.supabase_anon import get_supabase_anon_client

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


@router.post(
    "/register",
    response_model=AuthSessionResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(body: RegisterRequest) -> AuthSessionResponse:
    client = get_supabase_anon_client()
    try:
        res = client.auth.sign_up({"email": body.email, "password": body.password})
    except AuthApiError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc) or "Registration failed",
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
    client = get_supabase_anon_client()
    try:
        res = client.auth.sign_in_with_password(
            {"email": body.email, "password": body.password}
        )
    except AuthApiError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc) or "Invalid credentials",
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
def me(user: Annotated[GotrueUser, Depends(get_gotrue_user)]) -> MeResponse:
    return MeResponse(
        user=_identity_from_gotrue_user(user),
        app_metadata=gotrue_user_app_metadata(user),
        user_metadata=gotrue_user_user_metadata(user),
    )


@router.post("/logout", response_model=LogoutResponse)
def logout() -> LogoutResponse:
    return LogoutResponse()
