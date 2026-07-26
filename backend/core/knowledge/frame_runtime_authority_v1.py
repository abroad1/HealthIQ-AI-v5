"""
ARCH-CONV-CORRECT-1 — canonical frame runtime authority.

One decision, consumed upstream: an activation frame whose governed WHY authority
state is ``REJECTED`` is not runtime-eligible anywhere in the medical pipeline.

``why_authority_v1`` answers "which WHY asset may serve this frame". This module
answers the wider question "may this frame exist as an active medical result at
all", which is what the Gate C ratification of the rejected homocysteine metabolic
frame actually requires (do not compile, promote, or use as fallback).

Consumers must call this before a frame can be ranked, scored, narrated, cited by
an intervention, or persisted as an active replay result. Fail closed: an
unreadable register raises rather than admitting a rejected frame.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Any, Dict, FrozenSet, List, Optional, Sequence

from core.knowledge.signal_result_index_v1 import activation_key_or_empty
from core.knowledge.why_authority_v1 import STATE_REJECTED, load_why_authority_register

#: Runtime-eligibility label recorded on audit surfaces for excluded frames.
RUNTIME_STATE_REJECTED_NOT_ELIGIBLE = "REJECTED_NOT_RUNTIME_ELIGIBLE"


@lru_cache(maxsize=1)
def rejected_activation_keys() -> FrozenSet[str]:
    """Activation keys ratified as REJECTED in the governed WHY authority register."""
    register = load_why_authority_register()
    rows: Dict[str, Dict[str, Any]] = register["_by_activation_key"]
    return frozenset(
        key
        for key, row in rows.items()
        if str(row.get("authority_state") or "").strip() == STATE_REJECTED
    )


def clear_frame_runtime_authority_cache() -> None:
    rejected_activation_keys.cache_clear()


def is_frame_runtime_eligible(activation_key: str) -> bool:
    key = str(activation_key or "").strip()
    if not key:
        # Frames without an activation_key are out of the per-frame register's scope;
        # identity enforcement for those belongs to ARCH-CONV-PKG1.
        return True
    return key not in rejected_activation_keys()


def frame_runtime_exclusion_reason(activation_key: str) -> Optional[str]:
    if is_frame_runtime_eligible(activation_key):
        return None
    return RUNTIME_STATE_REJECTED_NOT_ELIGIBLE


def runtime_ineligible_keys_present(rows: Optional[Sequence[Any]]) -> List[str]:
    """Rejected activation keys found in a set of signal-result-shaped rows."""
    found: List[str] = []
    for row in rows or []:
        key = _row_activation_key(row)
        if key and not is_frame_runtime_eligible(key):
            found.append(key)
    return sorted(set(found))


def filter_runtime_eligible_rows(rows: Optional[Sequence[Any]]) -> List[Any]:
    """Drop rejected frames from signal-result-shaped rows (dict or SignalResult)."""
    return [row for row in (rows or []) if is_frame_runtime_eligible(_row_activation_key(row))]


def _row_activation_key(row: Any) -> str:
    if isinstance(row, dict):
        return activation_key_or_empty(row)
    key = str(getattr(row, "activation_key", "") or "").strip()
    if key:
        return key
    signal_id = str(getattr(row, "signal_id", "") or "").strip()
    source_spec_id = str(getattr(row, "source_spec_id", "") or "").strip()
    if signal_id and source_spec_id:
        return f"{signal_id}::{source_spec_id}"
    return ""
