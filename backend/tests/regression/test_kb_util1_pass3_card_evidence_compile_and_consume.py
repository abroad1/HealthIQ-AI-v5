"""
KB-UTIL-1 — Pass 3 card evidence compile and consume regression.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from core.analytics.domain_score_assembler import assemble_consumer_domain_scores_v1
from core.analytics.wave1_subsystem_evidence import assemble_wave1_flat_domain_evidence
from core.contracts.confidence_model_v1 import ConfidenceModelV1
from core.contracts.insight_graph_v1 import InsightGraphV1
from core.knowledge.domain_flat_card_evidence import load_domain_flat_evidence_artefact
from core.knowledge.health_system_card_evidence import (
    WAVE1_MED_REV1_HIDDEN_SUBSYSTEM_IDS,
    WAVE1_MED_REV1_SCORED_VISIBLE_SUBSYSTEM_IDS,
    assemble_subsystem_from_compiled_card_evidence,
    get_card_evidence_artefact,
)
from core.models.results import ConsumerDomainScoreV1

_REPO = Path(__file__).resolve().parents[3]
_CORE = _REPO / "backend" / "core"
_FRONTEND_SUBSYSTEM = _REPO / "frontend" / "app" / "components" / "results" / "Wave1SubsystemEvidenceSection.tsx"
_FRONTEND_FLAT = _REPO / "frontend" / "app" / "components" / "results" / "Wave1FlatDomainEvidenceSection.tsx"


def _rows(panel: set[str]):
    scoring = {
        "health_system_scores": {
            "cardiovascular": {
                "overall_score": 72.0,
                "missing_biomarkers": [],
                "biomarker_scores": [
                    {"biomarker_name": "total_cholesterol"},
                    {"biomarker_name": "ldl_cholesterol"},
                    {"biomarker_name": "hdl_cholesterol"},
                    {"biomarker_name": "triglycerides"},
                ],
            },
            "metabolic": {
                "overall_score": 68.0,
                "missing_biomarkers": ["glucose"],
                "biomarker_scores": [{"biomarker_name": "hba1c"}],
            },
            "liver": {
                "overall_score": 75.0,
                "missing_biomarkers": ["ast", "ggt"],
                "biomarker_scores": [{"biomarker_name": "alt"}],
            },
        }
    }
    ig = InsightGraphV1(
        analysis_id="kb-util-1",
        signal_results=[],
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
def test_compiled_lipid_artefact_has_kb_util1_enrichment_fields():
    artefact = get_card_evidence_artefact("wave1_cv_lipid_transport")
    assert artefact.subsystem_summary
    assert artefact.evidence_limitations_line
    assert "inflammation" in artefact.evidence_limitations_line.lower()
    assert artefact.provenance.get("compile_status") == "kb_util1_package_enrichment"


@pytest.mark.regression
def test_compiled_glycaemic_artefact_avoids_insulin_subsystem_framing():
    artefact = get_card_evidence_artefact("wave1_met_glycaemic_control")
    assert artefact.subsystem_summary
    assert "insulin" in artefact.evidence_limitations_line.lower()
    row = assemble_subsystem_from_compiled_card_evidence(
        subsystem_id="wave1_met_glycaemic_control",
        panel_biomarker_ids={"hba1c"},
        scored_on_rail={"hba1c"},
    )
    assert row is not None
    assert row.subsystem_summary
    assert row.evidence_limitations_line
    assert row.subsystem_label == "Long-term blood sugar"


@pytest.mark.regression
def test_hidden_subsystems_remain_suppressed():
    for sid in WAVE1_MED_REV1_HIDDEN_SUBSYSTEM_IDS:
        assert (
            assemble_subsystem_from_compiled_card_evidence(
                subsystem_id=sid,
                panel_biomarker_ids={"homocysteine", "crp", "insulin", "alt", "ggt"},
                scored_on_rail=set(),
            )
            is None
        )


@pytest.mark.regression
def test_domain_cards_receive_enriched_visible_subsystems():
    rows = _rows(
        {
            "total_cholesterol",
            "ldl_cholesterol",
            "hdl_cholesterol",
            "triglycerides",
            "tc_hdl_ratio",
            "hba1c",
            "alt",
        }
    )
    by_id = {r.domain_id: r for r in rows}
    cv = by_id["wave1_cardiovascular"]
    assert cv.subsystems and len(cv.subsystems) == 1
    assert cv.subsystems[0].subsystem_label == "Atherogenic lipid pattern"
    assert cv.subsystems[0].subsystem_summary
    assert cv.subsystems[0].marker_evidence
    assert any(m.rationale_short for m in cv.subsystems[0].marker_evidence or [])

    met = by_id["wave1_blood_sugar"]
    assert met.subsystems and len(met.subsystems) == 1
    assert met.subsystems[0].evidence_limitations_line
    assert "insulin" in met.subsystems[0].evidence_limitations_line.lower()

    liv: ConsumerDomainScoreV1 = by_id["wave1_liver"]
    assert liv.subsystems in (None, [])
    assert liv.flat_domain_evidence is not None
    assert liv.flat_domain_evidence.domain_summary_line
    assert liv.flat_domain_evidence.marker_evidence


@pytest.mark.regression
def test_liver_flat_does_not_reintroduce_scored_subsystems():
    flat = assemble_wave1_flat_domain_evidence(
        domain_id="wave1_liver",
        panel_biomarker_ids={"alt", "albumin"},
        rail_biomarker_scores=[{"biomarker_name": "alt"}],
    )
    assert flat is not None
    assert flat.included_marker_ids
    artefact = load_domain_flat_evidence_artefact("wave1_liver")
    assert "bilirubin" in {m.marker_id for m in artefact.markers}
    assert "total_bilirubin" not in {m.marker_id for m in artefact.markers}


@pytest.mark.regression
def test_no_pass3_json_runtime_reads_in_card_evidence_loaders():
    paths = [
        _REPO / "backend" / "core" / "knowledge" / "health_system_card_evidence.py",
        _REPO / "backend" / "core" / "knowledge" / "domain_flat_card_evidence.py",
        _REPO / "backend" / "core" / "analytics" / "wave1_subsystem_evidence.py",
        _REPO / "backend" / "core" / "analytics" / "domain_score_assembler.py",
    ]
    text = "\n".join(p.read_text(encoding="utf-8") for p in paths)
    assert "Pass_3.json" not in text
    assert "knowledge_bus/packages" not in text


@pytest.mark.regression
def test_frontend_render_only_no_package_reads():
    subsystem_src = _FRONTEND_SUBSYSTEM.read_text(encoding="utf-8")
    flat_src = _FRONTEND_FLAT.read_text(encoding="utf-8")
    for src in (subsystem_src, flat_src):
        assert "knowledge_bus" not in src
        assert "packages/" not in src
        assert "Pass_3" not in src


@pytest.mark.regression
def test_visible_scored_subsystems_unchanged_after_med_rev1():
    assert WAVE1_MED_REV1_SCORED_VISIBLE_SUBSYSTEM_IDS == frozenset(
        {"wave1_cv_lipid_transport", "wave1_met_glycaemic_control"}
    )
