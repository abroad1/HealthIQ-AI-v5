"""
Shared activation-frame indexing for signal results (ADR-RT-IDENTITY-PROV-001).

Canonical unit: activation_key = signal_id::source_spec_id.
"""

from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple


def require_activation_key(row: Dict[str, Any]) -> str:
    key = str(row.get("activation_key") or "").strip()
    if key:
        return key
    signal_id = str(row.get("signal_id") or "").strip()
    source_spec_id = str(row.get("source_spec_id") or "").strip()
    if signal_id and source_spec_id:
        return f"{signal_id}::{source_spec_id}"
    raise ValueError(
        "signal result missing activation_key (and cannot reconstruct from signal_id::source_spec_id)"
    )


def activation_key_or_empty(row: Dict[str, Any]) -> str:
    try:
        return require_activation_key(row)
    except ValueError:
        return ""


def signal_family_id(row: Dict[str, Any]) -> str:
    return str(row.get("signal_id") or "").strip()


def index_by_activation_key(
    rows: Optional[Sequence[Dict[str, Any]]],
    *,
    require_key: bool = False,
) -> Dict[str, Dict[str, Any]]:
    """Index frame-bearing rows by activation_key. Duplicate keys raise."""
    out: Dict[str, Dict[str, Any]] = {}
    for row in rows or []:
        if not isinstance(row, dict):
            continue
        if require_key:
            key = require_activation_key(row)
        else:
            key = activation_key_or_empty(row)
            if not key:
                # Legacy single-frame fallback: allow signal_id only when unique later
                sid = signal_family_id(row)
                if not sid:
                    continue
                key = sid
        if key in out:
            raise ValueError(f"Duplicate activation_key (or legacy signal_id key) in signal results: {key}")
        out[key] = row
    return out


def group_by_signal_id(
    rows: Optional[Sequence[Dict[str, Any]]],
) -> Dict[str, List[Dict[str, Any]]]:
    """Group frames by signal_id family. Order within each family is deterministic."""
    groups: Dict[str, List[Dict[str, Any]]] = {}
    for row in rows or []:
        if not isinstance(row, dict):
            continue
        sid = signal_family_id(row)
        if not sid:
            continue
        groups.setdefault(sid, []).append(row)
    for sid in list(groups.keys()):
        groups[sid] = sorted(
            groups[sid],
            key=lambda r: (activation_key_or_empty(r), str(r.get("package_id") or "")),
        )
    return {sid: groups[sid] for sid in sorted(groups.keys())}


def rows_for_signal_id(
    rows: Optional[Sequence[Dict[str, Any]]],
    signal_id: str,
) -> List[Dict[str, Any]]:
    sid = str(signal_id or "").strip()
    if not sid:
        return []
    return group_by_signal_id(rows).get(sid, [])


def family_fired_states(
    rows: Optional[Sequence[Dict[str, Any]]],
    *,
    valid_states: Iterable[str],
) -> Dict[str, str]:
    """
    Family-level presence map for interaction maps keyed by signal_id.

    When multiple frames fire, prefer at_risk over suboptimal over other valid states.
    Participating activation_keys are not collapsed — callers must also retain
    `participating_activation_keys` separately.
    """
    priority = {"at_risk": 0, "suboptimal": 1}
    valid = set(valid_states)
    best: Dict[str, Tuple[int, str]] = {}
    for row in rows or []:
        if not isinstance(row, dict):
            continue
        sid = signal_family_id(row)
        state = str(row.get("signal_state") or "").strip()
        if not sid or state not in valid:
            continue
        rank = priority.get(state, 50)
        prev = best.get(sid)
        if prev is None or rank < prev[0]:
            best[sid] = (rank, state)
    return {sid: state for sid, (_, state) in sorted(best.items())}


def participating_activation_keys(
    rows: Optional[Sequence[Dict[str, Any]]],
    *,
    valid_states: Iterable[str],
) -> List[str]:
    valid = set(valid_states)
    keys: List[str] = []
    for row in rows or []:
        if not isinstance(row, dict):
            continue
        state = str(row.get("signal_state") or "").strip()
        if state not in valid:
            continue
        key = activation_key_or_empty(row)
        if key:
            keys.append(key)
    return sorted(set(keys))


def confidence_by_signal_family(
    rows: Optional[Sequence[Dict[str, Any]]],
) -> Dict[str, Optional[float]]:
    """
    Family-level confidence for interaction-chain medians.

    When multiple frames exist, use the maximum numeric confidence (deterministic).
    """
    out: Dict[str, Optional[float]] = {}
    for sid, group in group_by_signal_id(rows).items():
        values: List[float] = []
        for row in group:
            conf = row.get("confidence")
            if isinstance(conf, (int, float)):
                values.append(float(conf))
        out[sid] = max(values) if values else None
    return out
