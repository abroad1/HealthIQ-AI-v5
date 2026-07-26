"""
ARCH-CONV-PKG3 — per-activation_key WHY authority selection.

Fail-closed for unknown pilot keys. Out-of-pilot signals remain on legacy path.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, Mapping, Optional, Tuple

import yaml

STATE_COMPILED_ACTIVE = "COMPILED_ACTIVE"
STATE_LEGACY_ACTIVE = "LEGACY_ACTIVE"
STATE_LEGACY_RETIRED = "LEGACY_RETIRED"
STATE_REJECTED = "REJECTED"
STATE_DEFERRED = "DEFERRED"
STATE_BLOCKED = "BLOCKED"

_PILOT_SIGNAL_IDS = frozenset(
    {
        "signal_vitamin_d_low",
        "signal_homocysteine_high",
        "signal_mcv_high",
        "signal_free_t3_low",
        "signal_tpo_ab_high",
    }
)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def authority_register_path() -> Path:
    return _repo_root() / "knowledge_bus" / "governance" / "compiled_why_authority_register_v1.yaml"


@lru_cache(maxsize=1)
def load_why_authority_register() -> Dict[str, Any]:
    path = authority_register_path()
    if not path.is_file():
        raise FileNotFoundError(f"missing WHY authority register: {path}")
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(payload, dict):
        raise ValueError("WHY authority register root must be a mapping")
    frames = payload.get("frames")
    if not isinstance(frames, list) or not frames:
        raise ValueError("WHY authority register frames must be a non-empty list")
    by_key: Dict[str, Dict[str, Any]] = {}
    for row in frames:
        if not isinstance(row, dict):
            raise ValueError("authority frame row must be a mapping")
        key = str(row.get("activation_key") or "").strip()
        state = str(row.get("authority_state") or "").strip()
        if not key or not state:
            raise ValueError("authority frame requires activation_key and authority_state")
        if key in by_key:
            raise ValueError(f"duplicate activation_key in authority register: {key}")
        by_key[key] = row
    payload = dict(payload)
    payload["_by_activation_key"] = by_key
    return payload


def clear_why_authority_cache() -> None:
    load_why_authority_register.cache_clear()


def authority_row_for(activation_key: str) -> Optional[Dict[str, Any]]:
    key = str(activation_key or "").strip()
    if not key:
        return None
    reg = load_why_authority_register()
    by_key: Mapping[str, Dict[str, Any]] = reg["_by_activation_key"]
    return by_key.get(key)


def authority_state_for(activation_key: str) -> Optional[str]:
    row = authority_row_for(activation_key)
    if row is None:
        return None
    return str(row.get("authority_state") or "").strip() or None


def is_pilot_signal_id(signal_id: str) -> bool:
    return str(signal_id or "").strip() in _PILOT_SIGNAL_IDS


def resolve_frame_why_authority(
    *,
    signal_id: str,
    activation_key: str,
) -> Tuple[str, Optional[Dict[str, Any]]]:
    """
    Return (mode, register_row).

    mode:
      - compiled: use compiled artefact for this activation_key
      - legacy: use legacy YAML loader
      - skip: emit no WHY for this frame (rejected / retired legacy without compiled)
      - fail_closed: contradictory or missing pilot registration
    """
    sid = str(signal_id or "").strip()
    key = str(activation_key or "").strip()
    row = authority_row_for(key) if key else None

    if is_pilot_signal_id(sid):
        if not key:
            # Bare signal_id is forbidden for multi-frame pilot signals.
            # Unique COMPILED_ACTIVE resolution is allowed (e.g. vitamin D / free T3).
            reg = load_why_authority_register()
            matches = [
                r
                for r in reg["_by_activation_key"].values()
                if str(r.get("signal_id") or "").strip() == sid
                and str(r.get("authority_state") or "").strip() == STATE_COMPILED_ACTIVE
            ]
            if len(matches) == 1:
                return "compiled", matches[0]
            return "fail_closed", None
        if row is None:
            return "fail_closed", None
        state = str(row.get("authority_state") or "").strip()
        if state == STATE_COMPILED_ACTIVE:
            return "compiled", row
        if state == STATE_REJECTED:
            return "skip", row
        if state == STATE_LEGACY_RETIRED:
            # Retired legacy with no compiled path must not emit.
            return "skip", row
        if state == STATE_LEGACY_ACTIVE:
            return "legacy", row
        if state in {STATE_DEFERRED, STATE_BLOCKED}:
            return "skip", row
        return "fail_closed", row

    # Out of pilot cohort: preserve pre-PKG3 legacy behaviour.
    return "legacy", None


def list_compiled_active_activation_keys() -> Tuple[str, ...]:
    reg = load_why_authority_register()
    keys = [
        key
        for key, row in sorted(reg["_by_activation_key"].items())
        if str(row.get("authority_state") or "").strip() == STATE_COMPILED_ACTIVE
    ]
    return tuple(keys)


def artefact_path_for_activation_key(activation_key: str) -> Path:
    row = authority_row_for(activation_key)
    if row is None:
        raise KeyError(f"no authority row for {activation_key!r}")
    rel = str(row.get("artefact_path") or "").strip()
    if not rel:
        raise KeyError(f"no artefact_path for COMPILED_ACTIVE key {activation_key!r}")
    return _repo_root() / rel
