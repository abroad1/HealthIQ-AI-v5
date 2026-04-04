"""
Lazy Supabase client for end-user Auth (anon key).

Storage and admin paths use SUPABASE_SERVICE_ROLE_KEY elsewhere; auth flows here
must not use the service role. Tokens are validated via the SDK (GoTrue), not
local JWT secret decoding.
"""

from __future__ import annotations

import os
from typing import Optional

from supabase import Client, create_client

_client: Optional[Client] = None


def get_supabase_anon_client() -> Client:
    """Return a process-wide Supabase client configured with the anon key."""
    global _client
    if _client is None:
        url = os.getenv("SUPABASE_URL", "").strip()
        key = os.getenv("SUPABASE_ANON_KEY", "").strip()
        if not url or not key:
            raise RuntimeError(
                "SUPABASE_URL and SUPABASE_ANON_KEY must be set for auth. "
                "Align with frontend NEXT_PUBLIC_SUPABASE_URL / NEXT_PUBLIC_SUPABASE_ANON_KEY."
            )
        _client = create_client(url, key)
    return _client


def reset_supabase_anon_client_for_tests() -> None:
    """Clear cached client (tests only)."""
    global _client
    _client = None
