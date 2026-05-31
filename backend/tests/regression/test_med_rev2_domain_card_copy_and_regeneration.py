"""
MED-REV-2 — domain card copy alignment and regeneration availability regression.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from core.analytics.domain_score_assembler import assemble_consumer_domain_scores_v1
from core.contracts.confidence_model_v1 import ConfidenceModelV1
from core.contracts.insight_graph_v1 import InsightGraphV1
from core.dto.analysis_regeneration_v1 import (
    assess_regeneration_available,
    regeneration_unavailable_reason,
    stored_raw_biomarkers_sufficient,
)
from core.dto.result_versioning_policy_v1 import build_result_versioning_metadata
from core.knowledge.health_system_card_evidence import WAVE1_MED_REV1_HIDDEN_SUBSYSTEM_IDS

_REPO = Path(__file__).resolve().parents[3]
_FRONTEND_BANNER = _REPO / "frontend" / "app" / "components" / "results" / "StaleResultBanner.tsx"


def _rows(panel: set[str]):
    scoring = {
        "health_system_scores": {
            "cardiovascular": {
                "overall_score": 72.0,
                "missing_biomarkers": [],
                "biomarker_scores": [
                    {"biomarker_name": "total_cholesterol"},
                    {"biomarker_name": "ldl_cholesterol"},
                ],
            },
            "metabolic": {
                "overall_score": 68.0,
                "missing_biomarkers": ["glucose"],
                "biomarker_scores": [{"biomarker_name": "hba1c"}],
            },
            "liver": {
                "overall_score": 75.0,
                "missing_biomarkers": [],
                "biomarker_scores": [{"biomarker_name": "alt"}],
            },
        }
    }
    ig = InsightGraphV1(
        analysis_id="med-rev-2",
        signal_results=[
            {
                "signal_id": "signal_homocysteine_elevation",
                "signal_state": "at_risk",
                "system": "metabolic",
                "primary_metric": "homocysteine",
            },
            {
                "signal_id": "signal_crp_high",
                "signal_state": "at_risk",
                "system": "metabolic",
                "primary_metric": "crp",
            },
        ],
        system_capacity_scores={"hepatic": 70, "cardiovascular": 80, "metabolic": 70},
        confidence=ConfidenceModelV1(
            cluster_confidence={"cardiovascular": 0.9, "metabolic": 0.7, "hepatic": 0.7}
        ),
    )
    return assemble_consumer_domain_scores_v1(
        scoring_result=scoring,
        insight_graph=ig,
        idl_bundle=None,
        derived_ratios_meta=None,
        panel_biomarker_ids=panel,
    )[0]


@pytest.mark.regression
def test_cv_card_anchor_uses_visible_subsystem_not_vascular_inflammation():
    panel = {
        "total_cholesterol",
        "ldl_cholesterol",
        "hdl_cholesterol",
        "triglycerides",
        "homocysteine",
        "crp",
    }
    cv = next(r for r in _rows(panel) if r.domain_id == "wave1_cardiovascular")
    assert cv.evidence_anchor_sentence == "Based mainly on: Atherogenic lipid pattern"
    assert "Vascular Inflammation" not in (cv.evidence_anchor_sentence or "")


@pytest.mark.regression
def test_blood_sugar_plain_descriptor_and_anchor_align_with_long_term_blood_sugar():
    panel = {"hba1c", "glucose", "total_cholesterol", "ldl_cholesterol"}
    met = next(r for r in _rows(panel) if r.domain_id == "wave1_blood_sugar")
    assert met.plain_english_descriptor == "Long-term blood sugar pattern"
    assert met.evidence_anchor_sentence == "Based mainly on: Long-term blood sugar"
    assert "insulin" not in (met.plain_english_descriptor or "").lower()


@pytest.mark.regression
def test_liver_confidence_does_not_claim_missing_markers_when_present():
    panel = {
        "alt",
        "ggt",
        "alp",
        "albumin",
        "total_cholesterol",
        "ldl_cholesterol",
        "hba1c",
    }
    liver = next(r for r in _rows(panel) if r.domain_id == "wave1_liver")
    conf = liver.confidence_sentence or ""
    assert "GGT" not in conf or "adding GGT" not in conf
    assert "albumin" not in conf.lower() or "adding albumin" not in conf.lower()


@pytest.mark.regression
def test_hidden_subsystems_remain_hidden_med_rev1():
    panel = {
        "homocysteine",
        "crp",
        "insulin",
        "triglycerides",
        "alt",
        "total_cholesterol",
        "ldl_cholesterol",
        "hba1c",
    }
    by_id = {r.domain_id: r for r in _rows(panel)}
    cv_ids = {s.subsystem_id for s in by_id["wave1_cardiovascular"].subsystems or []}
    assert cv_ids == {"wave1_cv_lipid_transport"}
    for hid in WAVE1_MED_REV1_HIDDEN_SUBSYSTEM_IDS:
        assert hid not in cv_ids


def test_regeneration_available_only_with_stored_raw_biomarkers():
    assert stored_raw_biomarkers_sufficient({"glucose": {"value": 5.1, "unit": "mmol/L"}})
    assert not stored_raw_biomarkers_sufficient({})
    assert not stored_raw_biomarkers_sufficient(None)
    assert assess_regeneration_available(raw_biomarkers={"hba1c": {"value": 42, "unit": "mmol/mol"}})
    assert regeneration_unavailable_reason(None)


def test_result_versioning_metadata_includes_regeneration_fields():
    stored = {
        "result_version": "1.0.0",
        "replay_manifest": {"manifest_version": "1.0.0"},
        "meta": {},
        "consumer_domain_scores": [],
        "clinician_report_v1": {"sections": {"page1": {"primary_concern": "test"}}},
        "narrative_report_v1": {"retail_summary": "ok"},
        "interpretation_display_layer_v1": {"records": [{"retail_display_label": "x"}]},
    }
    meta = build_result_versioning_metadata(
        stored,
        raw_biomarkers={"glucose": {"value": 5.0, "unit": "mmol/L"}},
    )
    assert meta["regeneration_available"] is True
    assert meta["regeneration_unavailable_reason"] is None


def test_stale_result_banner_renders_regenerate_button_when_available():
    src = _FRONTEND_BANNER.read_text(encoding="utf-8")
    assert "regenerate-result-button" in src
    assert "regeneration_available" in src
    assert "Regenerate with latest engine" in src
