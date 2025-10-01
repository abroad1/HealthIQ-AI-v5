import os
from supabase import create_client, Client
from typing import Optional

_URL = os.getenv("SUPABASE_URL")
_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

_client: Optional[Client] = None

def get_supabase_client() -> Client:
    global _client
    if _client is None:
        if not _URL or not _KEY:
            raise RuntimeError("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set")
        _client = create_client(_URL, _KEY)
    return _client
