"""LAUNCH-CORE-3 — result versioning and stale persisted snapshot classification."""

from __future__ import annotations

import copy

from core.dto.result_versioning_policy_v1 import (
    CURRENT_COMPLETENESS_POLICY_ID,
    REFERENCE_STALE_ANALYSIS_IDS,
    assess_result_versioning,
    build_result_versioning_metadata,
    detect_launch_core_stale_reasons,
    stamp_current_policy_meta,
)


def _render_contract_shell(**overrides: object) -> dict:
    """Minimal dict satisfying LC-S20 root + render required keys."""
    base = {
        "analysis_id": "lc3-test",
        "biomarkers": [],
        "clusters": [],
        "insights": [],
        "status": "complete",
        "created_at": "2026-01-01T00:00:00Z",
        "overall_score": 0.0,
        "primary_driver_system_id": None,
        "system_capacity_scores": [],
        "burden_hash": "",
        "risk_assessment": {},
        "recommendations": [],
        "result_version": "1.0.0",
        "derived_markers": [],
        "meta": {},
        "clinician_report_v1": {"sections": {"page1": {"primary_concern": "test"}}},
        "balanced_systems_v1": {},
        "replay_manifest": {"manifest_version": "1.0.0"},
        "interpretation_display_layer_v1": {"records": [{"retail_display_label": "x"}]},
        "narrative_report_v1": {"retail_summary": "ok"},
        "consumer_domain_scores": [],
        "intervention_annotations_v1": {},
    }
    base.update(overrides)
    return base


def _blood_sugar_stale_card() -> dict:
    """Simulates pre-LC-1 persisted blood sugar card (1/3 vs subsystem 2/4)."""
    return {
        "domain_id": "wave1_blood_sugar",
        "evidence_completeness_numerator": 1,
        "evidence_completeness_denominator": 3,
        "subsystems": [
            {
                "subsystem_id": "wave1_met_glycaemic_control",
                "included_marker_ids": ["hba1c"],
                "missing_marker_ids": ["glucose"],
                "source_trace": "health_system_card_evidence_v1:wave1_met_glycaemic_control_v1:manifest",
            },
            {
                "subsystem_id": "wave1_met_insulin_metabolic",
                "included_marker_ids": ["triglycerides"],
                "missing_marker_ids": ["insulin"],
                "source_trace": "health_system_card_evidence_v1:wave1_met_insulin_metabolic_v1:manifest",
            },
        ],
    }


def test_stale_blood_sugar_completeness_mismatch_detected():
    stored = {
        "result_version": "1.0.0",
        "replay_manifest": {"manifest_version": "1.0.0"},
        "meta": {},
        "consumer_domain_scores": [_blood_sugar_stale_card()],
        "clinician_report_v1": {"sections": {"page1": {"primary_concern": "test"}}},
        "narrative_report_v1": {"retail_summary": "ok"},
        "interpretation_display_layer_v1": {"records": [{"retail_display_label": "x"}]},
    }
    reasons = detect_launch_core_stale_reasons(stored)
    assert any("card_subsystem_completeness_mismatch:wave1_blood_sugar" in r for r in reasons)


def test_current_policy_stamp_not_stale():
    stored = _render_contract_shell(
        meta=stamp_current_policy_meta({}),
        consumer_domain_scores=[
            {
                "domain_id": "wave1_blood_sugar",
                "evidence_completeness_numerator": 2,
                "evidence_completeness_denominator": 4,
                "subsystems": _blood_sugar_stale_card()["subsystems"],
            }
        ],
    )
    assessment = assess_result_versioning(stored)
    assert not any("card_subsystem_completeness_mismatch" in r for r in assessment.stale_reasons)


def test_legacy_total_bilirubin_missing_flagged():
    stored = {
        "result_version": "1.0.0",
        "replay_manifest": {"manifest_version": "1.0.0"},
        "meta": {},
        "consumer_domain_scores": [
            {
                "domain_id": "wave1_liver",
                "evidence_completeness_numerator": 2,
                "evidence_completeness_denominator": 5,
                "subsystems": [
                    {
                        "subsystem_id": "wave1_liv_processing_context",
                        "included_marker_ids": ["bilirubin"],
                        "missing_marker_ids": ["total_bilirubin", "ast"],
                        "source_trace": "wave1_subsystem_evidence_v1:legacy",
                    }
                ],
            }
        ],
    }
    reasons = detect_launch_core_stale_reasons(stored)
    assert "legacy_total_bilirubin_false_missing" in reasons


def test_metadata_marks_stale_and_immutable():
    stored = _render_contract_shell(consumer_domain_scores=[_blood_sugar_stale_card()])
    meta = build_result_versioning_metadata(stored)
    assert meta["immutable_snapshot"] is True
    assert meta["result_status"] == "stale"
    assert meta["regeneration_available"] is False
    assert meta["user_message"]


def test_reference_stale_analysis_ids_documented():
    assert "18e14232-9f93-45e6-820c-004ab5a16235" in REFERENCE_STALE_ANALYSIS_IDS


def test_version_mismatch_from_lc_s20_still_stale():
    stored = _render_contract_shell(
        meta=stamp_current_policy_meta({}),
        result_version="0.9.0",
    )
    assessment = assess_result_versioning(stored)
    assert assessment.stale
    assert any("result_version_mismatch" in r for r in assessment.stale_reasons)
