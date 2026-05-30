"""LAUNCH-CORE-1 — card summary completeness aligned with compiled subsystem evidence."""

from __future__ import annotations

from core.analytics.domain_score_assembler import (
    _evidence_completeness_from_subsystems,
    assemble_consumer_domain_scores_v1,
)
from core.contracts.confidence_model_v1 import ConfidenceModelV1
from core.contracts.insight_graph_v1 import InsightGraphV1


def _minimal_graph() -> InsightGraphV1:
    return InsightGraphV1(
        analysis_id="launch-core-1",
        signal_results=[],
        system_capacity_scores={"metabolic": 70, "cardiovascular": 80, "hepatic": 70},
        confidence=ConfidenceModelV1(cluster_confidence={"metabolic": 0.4}),
    )


def test_blood_sugar_completeness_matches_compiled_subsystems():
    """UAT panel: hba1c + triglycerides present; glucose + insulin absent → 2 of 4."""
    scoring = {
        "health_system_scores": {
            "cardiovascular": {"overall_score": 80.0, "missing_biomarkers": [], "biomarker_scores": []},
            "metabolic": {
                "overall_score": 100.0,
                "missing_biomarkers": ["glucose", "insulin"],
                "biomarker_scores": [{"biomarker_name": "hba1c", "score": 100.0}],
            },
            "liver": {"overall_score": 75.0, "missing_biomarkers": [], "biomarker_scores": []},
        }
    }
    panel = {
        "hba1c",
        "triglycerides",
        "total_cholesterol",
        "ldl_cholesterol",
        "hdl_cholesterol",
        "alt",
    }
    rows, _ = assemble_consumer_domain_scores_v1(
        scoring_result=scoring,
        insight_graph=_minimal_graph(),
        idl_bundle=None,
        derived_ratios_meta=None,
        panel_biomarker_ids=panel,
    )
    blood = next(r for r in rows if r.domain_id == "wave1_blood_sugar")
    assert blood.evidence_completeness_numerator == 2
    assert blood.evidence_completeness_denominator == 4
    assert blood.subsystems is not None
    included_union = set()
    expected_union = set()
    for sub in blood.subsystems:
        included_union.update(sub.included_marker_ids)
        expected_union.update(sub.included_marker_ids)
        expected_union.update(sub.missing_marker_ids)
    assert len(included_union) == blood.evidence_completeness_numerator
    assert len(expected_union) == blood.evidence_completeness_denominator


def test_subsystem_union_helper_counts_unique_markers():
    class _Row:
        def __init__(self, included, missing):
            self.included_marker_ids = included
            self.missing_marker_ids = missing

    num, den = _evidence_completeness_from_subsystems(
        [
            _Row(["hba1c"], ["glucose"]),
            _Row(["triglycerides"], ["insulin"]),
        ]
    )
    assert (num, den) == (2, 4)
