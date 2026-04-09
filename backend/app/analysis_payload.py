"""
CONTEXT-HARDENING-A — single bounded normalisation for analysis /start payloads.

Canonical internal user shape (after normalise_analysis_user_dict):
- age, chronological_age: int (aligned)
- sex, gender: str in {male, female, other} (aligned; pipeline reads gender, FE often sends sex)
- height, height_cm: float, centimetres
- weight, weight_kg: float, kilograms

Questionnaire coalescing: API model accepts questionnaire_data | questionnaire (Pydantic aliases);
this helper merges any legacy top-level questionnaire for ContextFactory payloads that expect
payload["questionnaire"].
"""

from __future__ import annotations

from typing import Any, Dict, Mapping, Optional

_ALLOWED_SEX = frozenset({"male", "female", "other"})


def _canonical_sex(raw: Any) -> str:
    if raw is None:
        return "other"
    s = str(raw).strip().lower()
    if s in ("male", "m"):
        return "male"
    if s in ("female", "f"):
        return "female"
    if s in ("intersex", "other", "o"):
        return "other"
    if s in _ALLOWED_SEX:
        return s
    return "other"


def normalize_analysis_user_dict(user: Mapping[str, Any]) -> Dict[str, Any]:
    """
    Return a mutable copy of user with canonical demographic keys populated from known aliases.
    Does not validate ranges — ContextFactory / Pydantic enforce bounds.
    """
    out: Dict[str, Any] = dict(user)

    if out.get("chronological_age") is not None:
        ca = int(out["chronological_age"])
    elif out.get("age") is not None:
        ca = int(out["age"])
    else:
        ca = 0
    out["chronological_age"] = ca
    out["age"] = ca

    sx = _canonical_sex(out.get("sex") if out.get("sex") is not None else out.get("gender"))
    out["sex"] = sx
    out["gender"] = sx

    h = out.get("height_cm")
    if h is None:
        h = out.get("height")
    try:
        hf = float(h) if h is not None else 0.0
    except (TypeError, ValueError):
        hf = 0.0
    out["height_cm"] = hf
    out["height"] = hf

    w = out.get("weight_kg")
    if w is None:
        w = out.get("weight")
    try:
        wf = float(w) if w is not None else 0.0
    except (TypeError, ValueError):
        wf = 0.0
    out["weight_kg"] = wf
    out["weight"] = wf

    return out


def build_context_factory_payload(
    *,
    biomarkers: Mapping[str, Any],
    user: Mapping[str, Any],
    questionnaire: Optional[Mapping[str, Any]],
) -> Dict[str, Any]:
    """Shape expected by core.context.ContextFactory.create_context (questionnaire key, not questionnaire_data)."""
    payload: Dict[str, Any] = {
        "biomarkers": dict(biomarkers),
        "user": normalize_analysis_user_dict(user),
    }
    if questionnaire is not None:
        payload["questionnaire"] = dict(questionnaire)
    return payload
