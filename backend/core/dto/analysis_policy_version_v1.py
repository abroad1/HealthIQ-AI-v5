"""
CLIN-PRIORITY-RESULT-REGEN-1 — governed analysis-policy version and result_date provenance.

The analysis-policy version is the broad trigger for personalised-output change.
Specialised stale reasons remain additive diagnostics; this version is the governing stamp.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Any, Dict, Optional, Tuple

# Advances when deployed personalised analytical behaviour changes.
CURRENT_ANALYSIS_POLICY_VERSION = "analysis_policy_v1_clin_priority_core"

RESULT_DATE_PROVENANCE_USER_ENTERED = "user_entered"
RESULT_DATE_PROVENANCE_LEGACY_EQUIVALENT = "legacy_equivalent_source"
RESULT_DATE_PROVENANCE_LEGACY_CREATED_AT = "legacy_created_at_fallback"

VALID_RESULT_DATE_PROVENANCES = frozenset(
    {
        RESULT_DATE_PROVENANCE_USER_ENTERED,
        RESULT_DATE_PROVENANCE_LEGACY_EQUIVALENT,
        RESULT_DATE_PROVENANCE_LEGACY_CREATED_AT,
    }
)


def parse_result_date(value: Any) -> Optional[date]:
    """Parse ISO date or datetime string / date / datetime into a calendar date."""
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    text = str(value).strip()
    if not text:
        return None
    if "T" in text:
        text = text.split("T", 1)[0]
    try:
        return date.fromisoformat(text[:10])
    except ValueError:
        return None


def resolve_result_date_for_new_analysis(
    *,
    requested_result_date: Any = None,
    created_at: Any = None,
) -> Tuple[date, str]:
    """
    Deterministic result_date resolution for new analyses.

    Hierarchy (Outcome A):
    1. user-entered result_date
    2. legacy equivalent source (none exists in repo today — reserved)
    3. created_at calendar date as legacy fallback
    """
    user_date = parse_result_date(requested_result_date)
    if user_date is not None:
        return user_date, RESULT_DATE_PROVENANCE_USER_ENTERED

    fallback = parse_result_date(created_at)
    if fallback is None:
        fallback = date.today()
    return fallback, RESULT_DATE_PROVENANCE_LEGACY_CREATED_AT


def stamp_analysis_policy_meta(meta: Dict[str, Any]) -> Dict[str, Any]:
    """Stamp current analysis-policy version onto result meta."""
    out = dict(meta)
    out["analysis_policy_version"] = CURRENT_ANALYSIS_POLICY_VERSION
    return out


def detect_analysis_policy_stale_reasons(stored: Dict[str, Any]) -> list[str]:
    """Stale when analysis-policy version is missing or mismatched."""
    meta = stored.get("meta") if isinstance(stored.get("meta"), dict) else {}
    policy = str(meta.get("analysis_policy_version") or "").strip()
    if not policy:
        return ["analysis_policy_version_missing"]
    if policy != CURRENT_ANALYSIS_POLICY_VERSION:
        return [f"analysis_policy_version_mismatch:{policy}"]
    return []
