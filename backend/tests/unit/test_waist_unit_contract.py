"""Waist circumference explicit-unit contract + legacy unitless compatibility."""

from __future__ import annotations

import pytest

from app.analysis_payload import apply_questionnaire_objective_waist_to_user, normalize_analysis_user_dict
from core.context import ContextFactory
from core.pipeline.questionnaire_mapper import QuestionnaireMapper
from core.pipeline.waist_circumference_v1 import (
    WAIST_CM_DICT_KEY,
    WAIST_EXPLICIT_UNIT_CONTRACT,
    WAIST_INCHES_DICT_KEY,
    WaistUnitInvalidError,
    WaistUnitRequiredError,
    classify_legacy_bare_waist_outcome,
    is_legacy_unitless_waist_questionnaire,
)


def _contracted(waist) -> dict:
    return {
        "waist_circumference": waist,
        "_questionnaire_contract": {"version": WAIST_EXPLICIT_UNIT_CONTRACT},
    }


@pytest.fixture
def mapper() -> QuestionnaireMapper:
    return QuestionnaireMapper()


def test_explicit_90_cm_passthrough(mapper):
    out = mapper.extract_objective_lifestyle_inputs(
        _contracted({WAIST_CM_DICT_KEY: 90.0})
    )
    assert out["waist_circumference_cm"] == 90.0


def test_explicit_166_cm_passthrough(mapper):
    out = mapper.extract_objective_lifestyle_inputs(
        _contracted({WAIST_CM_DICT_KEY: 166.0})
    )
    assert out["waist_circumference_cm"] == 166.0


def test_explicit_36_inches_converts_once(mapper):
    out = mapper.extract_objective_lifestyle_inputs(
        _contracted({WAIST_INCHES_DICT_KEY: 36.0})
    )
    assert abs(out["waist_circumference_cm"] - 91.44) < 1e-6


def test_explicit_40_inches_converts_once(mapper):
    out = mapper.extract_objective_lifestyle_inputs(
        _contracted({WAIST_INCHES_DICT_KEY: 40.0})
    )
    assert abs(out["waist_circumference_cm"] - 101.6) < 1e-6


def test_current_bare_90_rejected(mapper):
    with pytest.raises(WaistUnitRequiredError, match="explicit unit"):
        mapper.extract_objective_lifestyle_inputs(_contracted(90.0))


def test_current_bare_166_rejected(mapper):
    with pytest.raises(WaistUnitRequiredError, match="explicit unit"):
        mapper.extract_objective_lifestyle_inputs(_contracted(166.0))


def test_legacy_bare_79_as_cm(mapper):
    # No contract stamp → known former unitless FE → centimetres.
    assert is_legacy_unitless_waist_questionnaire({"waist_circumference": 79})
    out = mapper.extract_objective_lifestyle_inputs({"waist_circumference": 79})
    assert out["waist_circumference_cm"] == 79.0


def test_legacy_bare_90_as_cm(mapper):
    out = mapper.extract_objective_lifestyle_inputs({"waist_circumference": 90})
    assert out["waist_circumference_cm"] == 90.0


def test_value_above_300_cm_rejected_without_clamp():
    user = normalize_analysis_user_dict(
        {"age": 40, "sex": "male", "height_cm": 180, "weight_kg": 80}
    )
    with pytest.raises(ValueError, match="at most 300 cm"):
        apply_questionnaire_objective_waist_to_user(
            user,
            _contracted({WAIST_CM_DICT_KEY: 301.0}),
        )


def test_invalid_unit_key_rejected(mapper):
    with pytest.raises(WaistUnitInvalidError, match="not recognised"):
        mapper.extract_objective_lifestyle_inputs(
            _contracted({"Waist circumference (mm)": 900.0})
        )


def test_both_units_rejected(mapper):
    with pytest.raises(WaistUnitInvalidError, match="single unit"):
        mapper.extract_objective_lifestyle_inputs(
            _contracted({WAIST_CM_DICT_KEY: 90.0, WAIST_INCHES_DICT_KEY: 36.0})
        )


def test_no_double_conversion_on_apply_and_usercontext():
    user = normalize_analysis_user_dict(
        {"user_id": "u1", "age": 40, "sex": "male", "height_cm": 180, "weight_kg": 80}
    )
    q = _contracted({WAIST_CM_DICT_KEY: 166.0})
    apply_questionnaire_objective_waist_to_user(user, q)
    assert user["waist_cm"] == 166.0
    ctx = ContextFactory(enable_logging=False).create_context(
        {
            "biomarkers": {"glucose": {"value": 5.0, "unit": "mmol/L"}},
            "user": user,
            "questionnaire": q,
        }
    )
    assert ctx.user.waist_cm == 166.0


def test_legacy_regeneration_path_applies_bare_as_cm():
    """Historical persisted bare waist (no stamp) must regenerate as cm, not inches."""
    user = normalize_analysis_user_dict(
        {"user_id": "u-legacy", "age": 40, "sex": "male", "height_cm": 193, "weight_kg": 77}
    )
    apply_questionnaire_objective_waist_to_user(user, {"waist_circumference": 90})
    assert user["waist_circumference_cm"] == 90.0
    assert user["waist_cm"] == 90.0


def test_magnitude_heuristic_not_used_for_legacy_80():
    """80 must stay 80 cm under legacy rule (not 203.2)."""
    out = QuestionnaireMapper().extract_objective_lifestyle_inputs({"waist_circumference": 80})
    assert out["waist_circumference_cm"] == 80.0


def test_classify_legacy_audit_outcomes():
    assert classify_legacy_bare_waist_outcome(78)[0] == "used_incorrectly"
    assert classify_legacy_bare_waist_outcome(79)[0] == "dropped_as_implausible"
    assert classify_legacy_bare_waist_outcome(119)[0] == "analysis_start_blocked"
