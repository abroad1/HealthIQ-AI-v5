"""
Lazy Supabase client for end-user Auth (anon key).

Storage and admin paths use SUPABASE_SERVICE_ROLE_KEY elsewhere; auth flows here
must not use the service role. Tokens are validated via the SDK (GoTrue), not
local JWT secret decoding.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from supabase import Client, create_client

# Auth routes must see backend/.env even when nothing else imported config.env
# (e.g. first request is POST /api/auth/login). Load once; shell env still wins
# when override=False.
_BACKEND_DIR = Path(__file__).resolve().parent.parent
load_dotenv(_BACKEND_DIR / ".env", override=False)

_client: Optional[Client] = None


def _anon_url_and_key() -> tuple[str, str]:
    """Resolve project URL and anon key (backend names, with NEXT_PUBLIC_* fallback)."""
    url = (
        os.getenv("SUPABASE_URL", "").strip()
        or os.getenv("NEXT_PUBLIC_SUPABASE_URL", "").strip()
    )
    key = (
        os.getenv("SUPABASE_ANON_KEY", "").strip()
        or os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY", "").strip()
    )
    return url, key


def get_supabase_anon_client() -> Client:
    """Return a process-wide Supabase client configured with the anon key."""
    global _client
    if _client is None:
        url, key = _anon_url_and_key()
        if not url or not key:
            raise RuntimeError(
                "Supabase URL and anon key must be set for auth. Use SUPABASE_URL and "
                "SUPABASE_ANON_KEY in backend/.env (or NEXT_PUBLIC_SUPABASE_URL and "
                "NEXT_PUBLIC_SUPABASE_ANON_KEY with the same values)."
            )
        _client = create_client(url, key)
    return _client


def reset_supabase_anon_client_for_tests() -> None:
    """Clear cached client (tests only)."""
    global _client
    _client = None
