"""
Authenticated caller for analysis write paths (FE-PERSISTENCE-A).

In HEALTHIQ_MODE=test, X-Test-Auth-User-Id may supply a synthetic user UUID so
unit/integration tests do not require Supabase. This header is ignored outside test mode.
"""

from __future__ import annotations

import os
from typing import Annotated, Optional

from fastapi import Depends, Header, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from core.dependencies.auth import CurrentUser, _gotrue_user_from_access_token

_bearer_optional = HTTPBearer(auto_error=False)


def require_analysis_submitter(
    credentials: Annotated[Optional[HTTPAuthorizationCredentials], Depends(_bearer_optional)],
    x_test_auth_user_id: Annotated[
        Optional[str],
        Header(alias="X-Test-Auth-User-Id"),
    ] = None,
) -> CurrentUser:
    if os.getenv("HEALTHIQ_MODE", "").lower() == "test" and x_test_auth_user_id:
        uid = x_test_auth_user_id.strip()
        if not uid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid X-Test-Auth-User-Id",
            )
        return CurrentUser(id=uid, email="analysis-test@healthiq.local")

    if credentials is None or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = _gotrue_user_from_access_token(credentials.credentials)
    return CurrentUser(id=user.id, email=user.email)
