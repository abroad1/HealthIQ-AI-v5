"""Targeted tests for D-1 consumer domain score assembler (Wave 1)."""

from __future__ import annotations

from core.analytics.domain_score_assembler import assemble_consumer_domain_scores_v1
from core.contracts.confidence_model_v1 import ConfidenceModelV1
from core.contracts.insight_graph_v1 import InsightGraphV1


def _minimal_graph(
    *,
    signal_results: list,
    capacity: dict,
    cluster_confidence: dict | None = None,
) -> InsightGraphV1:
    cc = cluster_confidence or {}
    return InsightGraphV1(
        analysis_id="t1",
        signal_results=signal_results,
        system_capacity_scores=capacity,
        confidence=ConfidenceModelV1(cluster_confidence=cc),
    )


def test_wave1_emits_three_domains_score_and_confidence_together():
    scoring = {
        "health_system_scores": {
            "cardiovascular": {"overall_score": 72.0, "missing_biomarkers": []},
            "metabolic": {"overall_score": 68.0, "missing_biomarkers": ["insulin"]},
            "liver": {"overall_score": 75.0, "missing_biomarkers": []},
        }
    }
    panel = {
        "total_cholesterol",
        "ldl_cholesterol",
        "hdl_cholesterol",
        "triglycerides",
        "glucose",
        "hba1c",
        "alt",
        "ast",
    }
    ig = _minimal_graph(
        signal_results=[],
        capacity={"hepatic": 40, "cardiovascular": 80, "metabolic": 70},
        cluster_confidence={
            "cardiovascular": 1.0,
            "metabolic": 0.7,
            "hepatic": 0.7,
        },
    )
    dr = {"ratios": {"tc_hdl_ratio": 3.2}, "ratio_registry_version": "t"}
    rows = assemble_consumer_domain_scores_v1(
        scoring_result=scoring,
        insight_graph=ig,
        idl_bundle=None,
        derived_ratios_meta=dr,
        panel_biomarker_ids=panel,
    )
    assert len(rows) == 3
    ids = [r.domain_id for r in rows]
    assert ids == ["wave1_cardiovascular", "wave1_blood_sugar", "wave1_liver"]
    for r in rows:
        assert 0.0 <= r.score <= 1.0
        assert r.confidence_tier in ("high", "medium", "low")
        assert r.band_label in ("strong", "stable", "watch", "review")
        assert r.source_track
        assert r.headline_sentence
        assert r.contributor_sentence
        assert r.confidence_sentence
        assert r.consequence_sentence
        assert r.next_step_sentence


def test_wave1_next_step_sentences_are_domain_distinct_without_insights():
    """D-3: per-domain next-step routing (governed fallbacks when no category insight)."""
    scoring = {
        "health_system_scores": {
            "cardiovascular": {"overall_score": 80.0, "missing_biomarkers": []},
            "metabolic": {"overall_score": 80.0, "missing_biomarkers": []},
            "liver": {"overall_score": 80.0, "missing_biomarkers": []},
        }
    }
    ig = _minimal_graph(signal_results=[], capacity={"hepatic": 80}, cluster_confidence={})
    rows = assemble_consumer_domain_scores_v1(
        scoring_result=scoring,
        insight_graph=ig,
        idl_bundle=None,
        derived_ratios_meta=None,
        panel_biomarker_ids={"alt", "glucose", "hba1c", "ldl_cholesterol"},
        insight_results=None,
        narrative_report_v1=None,
    )
    ns = [r.next_step_sentence for r in rows]
    assert len(set(ns)) == 3


def test_liver_blends_with_hepatic_capacity_not_liver_key():
    scoring = {
        "health_system_scores": {
            "cardiovascular": {"overall_score": 90.0, "missing_biomarkers": []},
            "metabolic": {"overall_score": 90.0, "missing_biomarkers": []},
            "liver": {"overall_score": 90.0, "missing_biomarkers": []},
        }
    }
    ig = _minimal_graph(
        signal_results=[],
        capacity={"hepatic": 30},
        cluster_confidence={"hepatic": 1.0},
    )
    rows = assemble_consumer_domain_scores_v1(
        scoring_result=scoring,
        insight_graph=ig,
        idl_bundle=None,
        derived_ratios_meta=None,
        panel_biomarker_ids={"alt"},
    )
    liver = rows[2]
    assert liver.score == 0.30
    assert "hepatic" in liver.source_track
    assert liver.raw_evidence_refs.get("blended_with_hepatic_capacity") is True
    assert liver.raw_evidence_refs.get("burden_capacity_hepatic") == 30
