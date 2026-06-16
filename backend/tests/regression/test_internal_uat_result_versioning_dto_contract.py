"""INTERNAL-UAT-RESULT-VERSIONING-1 — DTO render contract compatibility regression tests."""

from __future__ import annotations

from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.main import app
from config.database import get_db_optional
from core.dto.builders import build_analysis_result_dto
from core.dto.result_versioning_policy_v1 import (
    build_result_versioning_metadata,
    stamp_current_policy_meta,
)
from tests.unit.test_report_compiler_v1 import _report_v1_with_informational_root_cause_fallback

client = TestClient(app)
FIXTURE_ANALYSIS_ID = "iuat-rv1-fresh-0001"


def _no_db_session():
    yield None


@pytest.fixture(autouse=True)
def _disable_db_for_tests():
    app.dependency_overrides[get_db_optional] = _no_db_session
    yield
    app.dependency_overrides.pop(get_db_optional, None)


def _wave1_domain_rows() -> list[dict]:
    return [
        {
            "domain_id": "wave1_cardiovascular",
            "evidence_completeness_numerator": 1,
            "evidence_completeness_denominator": 1,
            "subsystems": [],
        },
        {
            "domain_id": "wave1_blood_sugar",
            "evidence_completeness_numerator": 1,
            "evidence_completeness_denominator": 1,
            "subsystems": [],
        },
        {
            "domain_id": "wave1_liver",
            "evidence_completeness_numerator": 1,
            "evidence_completeness_denominator": 1,
            "subsystems": [],
        },
    ]


def _fresh_persisted_without_derived_fields() -> dict:
    """Simulates persisted client_result_shape_v1 without read-time derived fields."""
    return {
        "analysis_id": FIXTURE_ANALYSIS_ID,
        "biomarkers": [],
        "clusters": [],
        "insights": [],
        "status": "completed",
        "created_at": "2026-06-16T00:00:00Z",
        "overall_score": 0.72,
        "primary_driver_system_id": "vascular",
        "system_capacity_scores": [],
        "burden_hash": "",
        "risk_assessment": {},
        "recommendations": [],
        "result_version": "1.0.0",
        "derived_markers": [],
        "meta": stamp_current_policy_meta(
            {
                "insight_graph": {
                    "report_v1": _report_v1_with_informational_root_cause_fallback(),
                }
            }
        ),
        "replay_manifest": {"manifest_version": "1.0.0"},
        "narrative_report_v1": {"retail_summary": "Panel summary for UAT."},
        "interpretation_display_layer_v1": {"records": [{"retail_display_label": "Homocysteine"}]},
        "consumer_domain_scores": _wave1_domain_rows(),
        "intervention_annotations_v1": None,
    }


def test_persisted_raw_false_incompatible_when_clinician_report_not_stored():
    raw = _fresh_persisted_without_derived_fields()
    meta = build_result_versioning_metadata(raw)
    assert meta["compatible"] is False
    assert "clinician_report_v1" in meta["render_blockers"]
    assert meta["result_status"] == "incompatible"


def test_assembled_dto_compatible_when_report_v1_compiles():
    raw = _fresh_persisted_without_derived_fields()
    dto = build_analysis_result_dto(raw)
    assert dto["clinician_report_v1"] is not None
    meta = build_result_versioning_metadata(dto)
    assert meta["compatible"] is True
    assert meta["render_blockers"] == []
    assert meta["result_status"] == "current"


def test_missing_report_v1_still_surfaces_render_blocker_on_dto():
    raw = _fresh_persisted_without_derived_fields()
    raw["meta"] = stamp_current_policy_meta({"insight_graph": {}})
    raw["narrative_report_v1"] = {}
    raw["interpretation_display_layer_v1"] = {"records": []}
    dto = build_analysis_result_dto(raw)
    assert dto["clinician_report_v1"] is None
    meta = build_result_versioning_metadata(dto)
    assert "missing_primary_finding" in meta["render_blockers"]


def test_stale_heuristics_unchanged_on_assembled_dto():
    from core.dto.result_versioning_policy_v1 import assess_result_versioning
    from tests.unit.test_launch_core3_result_versioning import _blood_sugar_stale_card

    raw = _fresh_persisted_without_derived_fields()
    raw["consumer_domain_scores"] = [_blood_sugar_stale_card()]
    raw["meta"] = {}
    dto = build_analysis_result_dto(raw)
    assessment = assess_result_versioning(dto)
    assert any("card_subsystem_completeness_mismatch" in r for r in assessment.stale_reasons)


@patch("app.routes.analysis._analysis_results", {})
def test_get_analysis_result_assesses_assembled_dto_not_raw_snapshot():
    from app.routes import analysis

    stored = _fresh_persisted_without_derived_fields()
    analysis._analysis_results[FIXTURE_ANALYSIS_ID] = stored

    response = client.get(f"/api/analysis/result?analysis_id={FIXTURE_ANALYSIS_ID}")
    assert response.status_code == 200
    data = response.json()

    assert data["clinician_report_v1"] is not None
    rv = data["result_versioning"]
    assert rv["compatible"] is True
    assert rv["result_status"] != "incompatible"
    assert rv["render_blockers"] == []
    assert rv["result_status"] != "stale"
