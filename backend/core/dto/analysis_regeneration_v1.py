"""
MED-REV-2 — Versioned result regeneration availability (read-only assessment).
"""

from __future__ import annotations

from typing import Any, Dict, Mapping, Optional

REGENERATION_POLICY_ID = "med_rev2_versioned_regeneration_v1"


def stored_raw_biomarkers_sufficient(raw: Optional[Mapping[str, Any]]) -> bool:
    """True when preserved upload biomarkers can drive a deterministic re-run."""
    if not isinstance(raw, Mapping) or not raw:
        return False
    for value in raw.values():
        if isinstance(value, dict) and value.get("value") is not None:
            return True
        if value is not None and not isinstance(value, dict):
            return True
    return False


def regeneration_unavailable_reason(raw: Optional[Mapping[str, Any]]) -> Optional[str]:
    if stored_raw_biomarkers_sufficient(raw):
        return None
    return "Original upload biomarkers were not preserved for this result. Upload the panel again to run a new analysis."


def assess_regeneration_available(
    *,
    raw_biomarkers: Optional[Mapping[str, Any]],
) -> bool:
    return stored_raw_biomarkers_sufficient(raw_biomarkers)
