"""Minimal Profile row creation for FK integrity (auth user → analyses.user_id)."""

from __future__ import annotations

from uuid import UUID, uuid4

from sqlalchemy.orm import Session

from core.dependencies.auth import CurrentUser
from repositories import ProfileRepository


def ensure_profile_for_auth_user(db: Session, auth: CurrentUser) -> UUID:
    """
    Return profiles.user_id for this auth subject, creating a Profile row on first use.

    email falls back to a deterministic placeholder when Supabase does not expose email.
    """
    user_uuid = UUID(auth.id)
    repo = ProfileRepository(db)
    existing = repo.get_by_user_id(user_uuid)
    if existing:
        return user_uuid

    email = (auth.email or "").strip() or f"user+{auth.id}@auth.unverified.healthiq"
    repo.create(
        id=uuid4(),
        user_id=user_uuid,
        email=email,
        consent_given=False,
        consent_version="1.0",
    )
    return user_uuid
