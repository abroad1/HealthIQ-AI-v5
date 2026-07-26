"""
Waist circumference unit contract (closure stabilisation).

Current submissions must carry an explicit unit via the recognised unit-labelled
dictionary shape (SSOT labels). Bare numerics are rejected unless the payload is
a known legacy unitless questionnaire record (pre-explicit-unit FE contract).
"""

from __future__ import annotations

from typing import Any, Mapping, Optional, Tuple

# SSOT dictionary keys (questionnaire.json label / alternativeUnit.label).
WAIST_CM_DICT_KEY = "Waist circumference (cm)"
WAIST_INCHES_DICT_KEY = "Waist circumference (inches)"

# Stamped by current FE on submit. Distinguishes new contract from historic rows.
QUESTIONNAIRE_CONTRACT_KEY = "_questionnaire_contract"
WAIST_EXPLICIT_UNIT_CONTRACT = "waist_explicit_unit_v1"

INCHES_TO_CM = 2.54


class WaistUnitError(ValueError):
    """Base class for waist unit contract failures."""


class WaistUnitRequiredError(WaistUnitError):
    """Bare / unitless waist under the current explicit-unit contract."""


class WaistUnitInvalidError(WaistUnitError):
    """Unrecognised or conflicting waist unit payload."""


def _contract_version(questionnaire: Optional[Mapping[str, Any]]) -> Optional[str]:
    if not questionnaire:
        return None
    raw = questionnaire.get(QUESTIONNAIRE_CONTRACT_KEY)
    if isinstance(raw, str) and raw.strip():
        return raw.strip()
    if isinstance(raw, Mapping):
        version = raw.get("version") or raw.get("waist_unit")
        if isinstance(version, str) and version.strip():
            v = version.strip()
            if v in ("explicit_v1", WAIST_EXPLICIT_UNIT_CONTRACT):
                return WAIST_EXPLICIT_UNIT_CONTRACT
            return v
    return None


def is_current_waist_unit_contract(questionnaire: Optional[Mapping[str, Any]]) -> bool:
    """True when the payload declares the explicit-unit contract stamp."""
    return _contract_version(questionnaire) == WAIST_EXPLICIT_UNIT_CONTRACT


def is_legacy_unitless_waist_questionnaire(questionnaire: Optional[Mapping[str, Any]]) -> bool:
    """
    Known former FE contract: label ``Waist circumference`` with no unit selector;
    stored bare numbers only (DB audit: 48 bare, 0 unit-labelled dicts).

    Boundary (narrowest reliable marker available):
    - no current-contract stamp; and
    - ``waist_circumference`` is a bare number (not a unit-labelled dict).

    Limitation: an unstamped modern client that still posts a bare number is also
    treated as legacy centimetres. Current FE always stamps and always posts a dict.
    """
    if not questionnaire or is_current_waist_unit_contract(questionnaire):
        return False
    raw = questionnaire.get("waist_circumference")
    return isinstance(raw, (int, float)) and not isinstance(raw, bool)


def _positive_float(value: Any) -> Optional[float]:
    if value is None or value == "":
        return None
    try:
        n = float(value)
    except (TypeError, ValueError):
        return None
    if n != n:  # NaN
        return None
    return n if n > 0 else None


def resolve_waist_circumference_cm_from_raw(
    raw: Any,
    *,
    allow_legacy_unitless_as_cm: bool = False,
) -> Optional[float]:
    """
    Resolve questionnaire ``waist_circumference`` to centimetres.

    - Explicit cm dict → pass through once
    - Explicit inches dict → convert exactly once
    - Bare number + legacy flag → interpret as centimetres (historic unitless FE)
    - Bare number without legacy flag → WaistUnitRequiredError
    - Invalid / conflicting unit payload → WaistUnitInvalidError
    """
    if raw is None or raw == "":
        return None

    if isinstance(raw, dict):
        cm = _positive_float(raw.get(WAIST_CM_DICT_KEY))
        inches = _positive_float(raw.get(WAIST_INCHES_DICT_KEY))
        if cm is not None and inches is not None:
            raise WaistUnitInvalidError(
                "Waist circumference must use a single unit (cm or inches), not both."
            )
        if cm is not None:
            return cm
        if inches is not None:
            return round(inches * INCHES_TO_CM, 4)
        # Unknown dict keys only — not a recognised unit-labelled shape.
        recognised = {WAIST_CM_DICT_KEY, WAIST_INCHES_DICT_KEY}
        other = [k for k in raw.keys() if k not in recognised]
        if other:
            raise WaistUnitInvalidError(
                "Waist circumference unit is not recognised. "
                f"Use '{WAIST_CM_DICT_KEY}' or '{WAIST_INCHES_DICT_KEY}'."
            )
        return None

    if isinstance(raw, bool):
        raise WaistUnitInvalidError("Waist circumference value is invalid.")

    if isinstance(raw, (int, float)):
        n = float(raw)
        if n <= 0:
            return None
        if allow_legacy_unitless_as_cm:
            return n
        raise WaistUnitRequiredError(
            "Waist circumference must include an explicit unit (cm or inches). "
            "Bare numeric values are not accepted for new submissions."
        )

    if isinstance(raw, str):
        raise WaistUnitRequiredError(
            "Waist circumference must include an explicit unit (cm or inches)."
        )

    raise WaistUnitInvalidError("Waist circumference value is invalid.")


def resolve_questionnaire_waist_cm(
    questionnaire: Optional[Mapping[str, Any]],
) -> Optional[float]:
    """Resolve waist from a full questionnaire mapping using contract rules."""
    if not questionnaire or "waist_circumference" not in questionnaire:
        return None
    legacy = is_legacy_unitless_waist_questionnaire(questionnaire)
    return resolve_waist_circumference_cm_from_raw(
        questionnaire.get("waist_circumference"),
        allow_legacy_unitless_as_cm=legacy,
    )


def classify_legacy_bare_waist_outcome(value_cm: float) -> Tuple[str, float]:
    """
    Classify historic bare-as-inches mishandling outcome for audit only.
    Returns (likely_outcome, incorrect_mapped_cm_if_treated_as_inches).
    """
    incorrect = round(float(value_cm) * INCHES_TO_CM, 4)
    if incorrect > 300:
        return "analysis_start_blocked", incorrect
    if incorrect > 200 or incorrect < 40:
        return "dropped_as_implausible", incorrect
    return "used_incorrectly", incorrect
