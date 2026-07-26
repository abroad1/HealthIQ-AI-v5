"""
Bearer-token auth dependency: verifies Supabase access JWT via SDK (get_user).

Returns a minimal identity object for protected routes (distinct from
core.models.user.User, which is analysis/profile domain, not Auth).
"""

from __future__ import annotations

import logging
from typing import Annotated, Any, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from gotrue.errors import AuthApiError, AuthError, AuthRetryableError
from gotrue.types import User as GotrueUser
from pydantic import BaseModel, ConfigDict, Field

from core.supabase_anon import get_supabase_anon_client

logger = logging.getLogger(__name__)

bearer_scheme = HTTPBearer(auto_error=True)


class CurrentUser(BaseModel):
    """Authenticated caller identity from Supabase Auth (JWT / session)."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    id: str = Field(..., description="Supabase Auth user id (matches JWT sub)")
    email: Optional[str] = Field(default=None, description="Email when present on the user")


def _unauthorized(detail: str = "Invalid or expired token") -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )


def _is_token_rejection_status(code: Any) -> bool:
    """Upstream auth rejection statuses that must become backend 401."""
    try:
        n = int(code)
    except (TypeError, ValueError):
        return False
    # Include observed Supabase /auth/v1/user 403 for revoked/rejected sessions.
    return n in (401, 403) or 400 <= n < 500


def _http_exception_from_token_verification(exc: BaseException) -> HTTPException:
    """
    Map token-verification failures to controlled 401.

    Does not convert AuthRetryableError (upstream 502/503/504) into 401 —
    those remain service-unavailable class faults.
    """
    if isinstance(exc, AuthRetryableError):
        upstream = getattr(exc, "status", None)
        logger.warning(
            "auth_token_verification_retryable status=%s err_type=%s",
            upstream,
            type(exc).__name__,
        )
        return HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication service temporarily unavailable",
        )

    if isinstance(exc, AuthApiError):
        upstream = getattr(exc, "status", None)
        logger.info(
            "auth_token_rejected status=%s err_type=%s",
            upstream,
            type(exc).__name__,
        )
        if upstream is None or _is_token_rejection_status(upstream):
            return _unauthorized("Invalid or expired token")
        # Unexpected AuthApiError status (e.g. 5xx not classified retryable).
        logger.error(
            "auth_token_verification_upstream_error status=%s err_type=%s",
            upstream,
            type(exc).__name__,
        )
        return HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication service error",
        )

    if isinstance(exc, AuthError):
        upstream = getattr(exc, "status", None)
        logger.info(
            "auth_token_rejected status=%s err_type=%s",
            upstream,
            type(exc).__name__,
        )
        return _unauthorized("Invalid or expired token")

    # Non-JSON / unexpected SDK transport failures during get_user — treat as
    # token verification failure only when clearly client-auth related wrappers.
    logger.warning(
        "auth_token_verification_unexpected err_type=%s",
        type(exc).__name__,
    )
    return _unauthorized("Invalid or expired token")


def _gotrue_user_from_access_token(token: str) -> GotrueUser:
    if not token:
        raise _unauthorized("Missing bearer token")
    client = get_supabase_anon_client()
    try:
        user_resp = client.auth.get_user(token)
    except AuthRetryableError as exc:
        raise _http_exception_from_token_verification(exc) from exc
    except AuthError as exc:
        # AuthApiError (incl. upstream 403), AuthUnknownError, AuthInvalidJwtError, etc.
        raise _http_exception_from_token_verification(exc) from exc
    except Exception as exc:
        # Last-resort: SDK/httpx anomalies during token verification must not 500
        # the session probe. Unrelated route/DB faults are outside this helper.
        raise _http_exception_from_token_verification(exc) from exc
    if user_resp is None or user_resp.user is None:
        raise _unauthorized("Invalid or expired token")
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
