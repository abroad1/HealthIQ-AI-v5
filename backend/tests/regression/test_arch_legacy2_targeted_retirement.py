"""
ARCH-LEGACY-2 — Targeted legacy pathway retirement regression guards.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from core.analytics.domain_narrative_wave1 import (
    confidence_sentence_cv_coherent,
    confidence_sentence_for,
    cv_contributor_for_lipid_visible_card,
    cv_uses_lipid_subsystem_narrative_authority,
)
from core.analytics.domain_score_assembler import assemble_consumer_domain_scores_v1
from core.analytics.wave1_subsystem_evidence import assemble_wave1_subsystem_evidence
from core.contracts.confidence_model_v1 import ConfidenceModelV1
from core.contracts.insight_graph_v1 import InsightGraphV1
from core.knowledge.health_system_card_evidence import (
    WAVE1_MED_REV1_HIDDEN_SUBSYSTEM_IDS,
    WAVE1_MED_REV1_SCORED_VISIBLE_SUBSYSTEM_IDS,
    assemble_subsystem_from_compiled_card_evidence,
)

_REPO = Path(__file__).resolve().parents[3]
_NARRATIVE_MODULE = _REPO / "backend" / "core" / "analytics" / "domain_narrative_wave1.py"
_WAVE1_MODULE = _REPO / "backend" / "core" / "analytics" / "wave1_subsystem_evidence.py"


def _minimal_cv_rows(panel: set[str]):
    scoring = {
        "health_system_scores": {
            "cardiovascular": {
                "overall_score": 72.0,
                "missing_biomarkers": [],
                "biomarker_scores": [{"biomarker_name": "total_cholesterol"}],
            },
            "metabolic": {"overall_score": 68.0, "missing_biomarkers": [], "biomarker_scores": []},
            "liver": {"overall_score": 75.0, "missing_biomarkers": [], "biomarker_scores": []},
        }
    }
    ig = InsightGraphV1(
        analysis_id="arch-legacy-2",
        signal_results=[],
        system_capacity_scores={"hepatic": 70, "cardiovascular": 80, "metabolic": 70},
        confidence=ConfidenceModelV1(cluster_confidence={"cardiovascular": 0.9, "metabolic": 0.7, "hepatic": 0.7}),
    )
    return assemble_consumer_domain_scores_v1(
        scoring_result=scoring,
        insight_graph=ig,
        idl_bundle=None,
        derived_ratios_meta=None,
        panel_biomarker_ids=panel,
    )[0]


@pytest.mark.regression
def test_wave1_module_has_no_hard_coded_subsystem_fallback_symbols() -> None:
    src = _WAVE1_MODULE.read_text(encoding="utf-8")
    for token in ("_Wave1SubsystemDef", "_partition_subsystem_markers", "WAVE1_DOMAIN_SUBSYSTEM_DEFS"):
        assert token not in src


@pytest.mark.regression
def test_cv_contributor_dead_helper_not_defined() -> None:
    tree = ast.parse(_NARRATIVE_MODULE.read_text(encoding="utf-8"))
    names = {node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)}
    assert "cv_contributor" not in names


@pytest.mark.regression
def test_compiled_wave1_subsystems_never_emit_hard_coded_source_trace() -> None:
    panel = {
        "total_cholesterol",
        "ldl_cholesterol",
        "hdl_cholesterol",
        "triglycerides",
        "homocysteine",
        "glucose",
        "hba1c",
    }
    rows = assemble_wave1_subsystem_evidence(
        domain_id="wave1_cardiovascular",
        panel_biomarker_ids=panel,
        rail_biomarker_scores=[{"biomarker_name": "total_cholesterol"}],
    )
    assert rows
    for row in rows:
        assert row.source_trace.startswith("health_system_card_evidence_v1:")
        assert "wave1_subsystem_evidence_v1:" not in row.source_trace
        assert row.subsystem_label not in ("Lipid transport", "Glycaemic control")


@pytest.mark.regression
def test_hidden_subsystems_remain_suppressed_from_visible_rows() -> None:
    panel = {"homocysteine", "crp", "insulin"}
    for hidden_id in WAVE1_MED_REV1_HIDDEN_SUBSYSTEM_IDS:
        row = assemble_subsystem_from_compiled_card_evidence(
            subsystem_id=hidden_id,
            panel_biomarker_ids=panel,
            scored_on_rail=set(),
        )
        assert row is None


@pytest.mark.regression
def test_lipid_visible_cv_confidence_excludes_homocysteine_bridge() -> None:
    panel = {
        "total_cholesterol",
        "ldl_cholesterol",
        "hdl_cholesterol",
        "triglycerides",
        "homocysteine",
    }
    cv = next(r for r in _minimal_cv_rows(panel) if r.domain_id == "wave1_cardiovascular")
    assert cv_uses_lipid_subsystem_narrative_authority(cv.subsystems)
    conf = (cv.confidence_sentence or "").lower()
    assert "homocysteine" not in conf
    assert cv.confidence_sentence == confidence_sentence_for(cv.confidence_tier or "medium", "cv")
    assert confidence_sentence_cv_coherent("medium", "Homocysteine is elevated") == confidence_sentence_for(
        "medium", "cv"
    )


@pytest.mark.regression
def test_lipid_visible_contributor_helper_excludes_homocysteine_signals() -> None:
    contrib = cv_contributor_for_lipid_visible_card(
        {},
        ["signal_homocysteine_elevation"],
        [{"signal_id": "signal_homocysteine_elevation", "signal_state": "at_risk"}],
        None,
    )
    assert "homocysteine" not in contrib.lower()


@pytest.mark.regression
def test_scored_visible_subsystems_match_med_rev1_partition() -> None:
    panel = {
        "total_cholesterol",
        "ldl_cholesterol",
        "hdl_cholesterol",
        "triglycerides",
        "hba1c",
    }
    cv = next(r for r in _minimal_cv_rows(panel) if r.domain_id == "wave1_cardiovascular")
    visible = {s.subsystem_id for s in cv.subsystems or []}
    assert visible == set(WAVE1_MED_REV1_SCORED_VISIBLE_SUBSYSTEM_IDS) & {"wave1_cv_lipid_transport"}
