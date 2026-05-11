"""
CONTEXT-HARDENING-A — regression tests for analysis request contract and normalisation.
"""

import pytest
from app.analysis_payload import (
    apply_questionnaire_medication_representation_to_user,
    apply_questionnaire_objective_waist_to_user,
    build_context_factory_payload,
    normalize_analysis_user_dict,
    propagate_waist_to_user_after_assembly,
    resolve_waist_circumference_cm,
)
from app.routes.analysis import AnalysisStartRequest
from core.context import ContextFactory


def test_normalize_user_dict_aligns_aliases():
    raw = {"user_id": " u1 ", "age": 40, "sex": "Female", "height": 170.0, "weight": 72.5}
    out = normalize_analysis_user_dict(raw)
    assert out["chronological_age"] == 40
    assert out["age"] == 40
    assert out["sex"] == "female"
    assert out["gender"] == "female"
    assert out["height_cm"] == 170.0
    assert out["height"] == 170.0
    assert out["weight_kg"] == 72.5
    assert out["weight"] == 72.5


def test_normalize_user_dict_gender_falls_back_from_sex():
    raw = {"gender": "male", "chronological_age": 30, "height_cm": 180, "weight_kg": 75}
    out = normalize_analysis_user_dict(raw)
    assert out["sex"] == "male"
    assert out["gender"] == "male"


def test_analysis_start_request_accepts_questionnaire_alias():
    body = {
        "biomarkers": {"glucose": {"value": 5.0, "unit": "mmol/L"}},
        "user": {"user_id": "x", "age": 35, "sex": "male", "height_cm": 180, "weight_kg": 75},
        "questionnaire": {"date_of_birth": "1990-01-01", "smoking_status": "never"},
    }
    req = AnalysisStartRequest.model_validate(body)
    assert req.questionnaire_data == body["questionnaire"]


def test_build_context_factory_payload_uses_questionnaire_key():
    payload = build_context_factory_payload(
        biomarkers={"glucose": {"value": 5.0, "unit": "mmol/L"}},
        user={"age": 35, "sex": "male", "height_cm": 180, "weight_kg": 75},
        questionnaire={"q": 1},
    )
    assert "questionnaire" in payload
    assert "questionnaire_data" not in payload
    assert payload["questionnaire"] == {"q": 1}


def test_normalize_mirrors_canonical_waist_to_legacy_alias():
    raw = {
        "age": 40,
        "sex": "male",
        "height_cm": 180,
        "weight_kg": 80,
        "waist_circumference_cm": 92.0,
    }
    out = normalize_analysis_user_dict(raw)
    assert out["waist_circumference_cm"] == 92.0
    assert out["waist_cm"] == 92.0


def test_normalize_promotes_legacy_waist_cm_to_canonical():
    raw = {
        "age": 40,
        "sex": "male",
        "height_cm": 180,
        "weight_kg": 80,
        "waist_cm": 88.0,
    }
    out = normalize_analysis_user_dict(raw)
    assert out["waist_circumference_cm"] == 88.0
    assert out["waist_cm"] == 88.0


def test_canonical_waist_wins_when_legacy_differs():
    raw = {
        "age": 40,
        "sex": "male",
        "height_cm": 180,
        "weight_kg": 80,
        "waist_circumference_cm": 90.0,
        "waist_cm": 999.0,
    }
    out = normalize_analysis_user_dict(raw)
    assert out["waist_circumference_cm"] == 90.0
    assert out["waist_cm"] == 90.0


def test_resolve_waist_single_semantics_match_usercontext_and_engine():
    m = {"waist_circumference_cm": 91.0, "waist_cm": 91.0}
    assert resolve_waist_circumference_cm(m) == 91.0
    assembled = {"waist_circumference_cm": resolve_waist_circumference_cm(m)}
    assert assembled["waist_circumference_cm"] == 91.0


def test_propagate_assembled_waist_mirrors_user_top_level():
    ud = {"height_cm": 180.0, "weight_kg": 80.0}
    assembled = {"height_cm": 180.0, "weight_kg": 80.0, "waist_circumference_cm": 93.0}
    propagate_waist_to_user_after_assembly(ud, assembled)
    assert ud["waist_circumference_cm"] == 93.0
    assert ud["waist_cm"] == 93.0


def test_apply_questionnaire_waist_updates_user_canonical_and_mirror():
    user = normalize_analysis_user_dict(
        {"age": 40, "sex": "male", "height_cm": 180, "weight_kg": 80}
    )
    apply_questionnaire_objective_waist_to_user(
        user,
        {"waist_circumference": {"Waist circumference (cm)": 87.0}},
    )
    assert user["waist_circumference_cm"] == 87.0
    assert user["waist_cm"] == 87.0


def test_context_factory_usercontext_reads_canonical_waist_only():
    factory = ContextFactory(enable_logging=False)
    u = normalize_analysis_user_dict(
        {
            "age": 40,
            "sex": "male",
            "height_cm": 180,
            "weight_kg": 80,
            "waist_circumference_cm": 94.0,
        }
    )
    payload = {
        "biomarkers": {"glucose": {"value": 5.0, "unit": "mmol/L"}},
        "user": u,
    }
    ctx = factory.create_context(payload)
    assert ctx.user.waist_cm == 94.0


def test_apply_questionnaire_medication_representation_aligns_usercontext():
    factory = ContextFactory(enable_logging=False)
    u = normalize_analysis_user_dict(
        {"user_id": "u-med", "age": 40, "sex": "male", "height_cm": 180, "weight_kg": 80}
    )
    q = {
        "long_term_medications": ["None"],
        "supplements": ["Vitamin D", "Omega-3"],
        "chronic_conditions": ["None"],
    }
    apply_questionnaire_medication_representation_to_user(u, q)
    payload = {
        "biomarkers": {"glucose": {"value": 5.0, "unit": "mmol/L"}},
        "user": u,
        "questionnaire": q,
    }
    ctx = factory.create_context(payload)
    assert ctx.user.medications == []
    assert ctx.user.supplements == ["Vitamin D", "Omega-3"]
