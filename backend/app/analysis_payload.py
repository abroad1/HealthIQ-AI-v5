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

# CONTEXT-HARDENING-B — single canonical waist field (cm), SSOT-aligned with lifestyle_registry / engine.
CANONICAL_WAIST_CM_KEY = "waist_circumference_cm"
# Compatibility only: mirrors CANONICAL_WAIST_CM_KEY for UserContext model field name `waist_cm`.
LEGACY_USERCONTEXT_WAIST_CM_KEY = "waist_cm"


def resolve_waist_circumference_cm(mapping: Mapping[str, Any]) -> Optional[float]:
    """
    Return one positive waist circumference in cm.
    Canonical key wins when present; legacy ``waist_cm`` is accepted as input only.
    """
    def _positive_cm(x: Any) -> Optional[float]:
        if x is None:
            return None
        try:
            v = float(x)
        except (TypeError, ValueError):
            return None
        return v if v > 0 else None

    c = _positive_cm(mapping.get(CANONICAL_WAIST_CM_KEY))
    if c is not None:
        return c
    return _positive_cm(mapping.get(LEGACY_USERCONTEXT_WAIST_CM_KEY))


def sync_waist_mirror_to_user_dict(user: Dict[str, Any]) -> None:
    """Write canonical + legacy mirror from ``resolve_waist_circumference_cm`` (no duplicate semantics)."""
    w = resolve_waist_circumference_cm(user)
    if w is not None:
        user[CANONICAL_WAIST_CM_KEY] = w
        user[LEGACY_USERCONTEXT_WAIST_CM_KEY] = w
    else:
        user.pop(CANONICAL_WAIST_CM_KEY, None)
        user.pop(LEGACY_USERCONTEXT_WAIST_CM_KEY, None)


def apply_questionnaire_objective_waist_to_user(
    user: Dict[str, Any],
    questionnaire: Optional[Mapping[str, Any]],
) -> None:
    """Promote questionnaire-derived waist into canonical user keys (then mirror legacy)."""
    if questionnaire:
        from core.pipeline.questionnaire_mapper import QuestionnaireMapper

        qobj = QuestionnaireMapper().extract_objective_lifestyle_inputs(dict(questionnaire))
        w_raw = qobj.get(CANONICAL_WAIST_CM_KEY)
        if w_raw is not None:
            try:
                w = float(w_raw)
            except (TypeError, ValueError):
                w = None
            else:
                if w > 0:
                    user[CANONICAL_WAIST_CM_KEY] = w
    sync_waist_mirror_to_user_dict(user)


def propagate_waist_to_user_after_assembly(
    user_data: Dict[str, Any],
    assembled_objective: Mapping[str, Any],
) -> None:
    """
    After objective assembly, copy canonical waist from ``lifestyle_inputs`` shape into top-level user
    so UserContext and engine share the same numeric cm value.
    """
    w_raw = assembled_objective.get(CANONICAL_WAIST_CM_KEY)
    if w_raw is not None:
        try:
            w = float(w_raw)
        except (TypeError, ValueError):
            w = None
        else:
            if w > 0:
                user_data[CANONICAL_WAIST_CM_KEY] = w
                user_data[LEGACY_USERCONTEXT_WAIST_CM_KEY] = w
                return
    sync_waist_mirror_to_user_dict(user_data)


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

    sync_waist_mirror_to_user_dict(out)

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
