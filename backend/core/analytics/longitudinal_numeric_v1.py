"""
N-3 — Deterministic longitudinal lab numeric comparison helpers.

Used by future narrative compilation; does not imply clinical interpretation.
"""

from __future__ import annotations

from typing import Any, Dict, Optional


def comparable_lab_delta(
    prior_value: Optional[float],
    prior_unit: Optional[str],
    current_value: Optional[float],
    current_unit: Optional[str],
) -> Optional[Dict[str, Any]]:
    """
    When both measurements exist, return a bounded numeric delta dict.

    Units must match (case-insensitive, stripped) when either side declares a unit.
    When both sides omit units, a delta is returned with unit \"\" (caller must treat
    this as weakly asserted; prefer explicit units in persisted rows).
    """
    if prior_value is None or current_value is None:
        return None
    try:
        p = float(prior_value)
        c = float(current_value)
    except (TypeError, ValueError):
        return None

    pu = (prior_unit or "").strip()
    cu = (current_unit or "").strip()
    if pu and cu:
        if pu.casefold() != cu.casefold():
            return None
        u = pu
    elif pu or cu:
        return None
    else:
        u = ""

    return {"prior": p, "current": c, "delta": c - p, "unit": u}
