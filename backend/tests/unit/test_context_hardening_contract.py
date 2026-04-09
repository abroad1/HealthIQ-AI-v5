"""
CONTEXT-HARDENING-A — regression tests for analysis request contract and normalisation.
"""

import pytest
from app.analysis_payload import normalize_analysis_user_dict, build_context_factory_payload
from app.routes.analysis import AnalysisStartRequest


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
