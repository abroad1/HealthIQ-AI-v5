"""
MED-REV-1 — Wave 1 subsystem medical visibility policy regression.

Proves Layer B enforces compiled visibility_tier and medical review v1 surfacing model.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from core.analytics.domain_score_assembler import assemble_consumer_domain_scores_v1
from core.analytics.wave1_subsystem_evidence import assemble_wave1_subsystem_evidence
from core.contracts.confidence_model_v1 import ConfidenceModelV1
from core.contracts.insight_graph_v1 import InsightGraphV1
from core.knowledge.health_system_card_evidence import (
    WAVE1_COMPILED_SUBSYSTEM_IDS,
    WAVE1_MED_REV1_HIDDEN_SUBSYSTEM_IDS,
    WAVE1_MED_REV1_SCORED_VISIBLE_SUBSYSTEM_IDS,
    assemble_subsystem_from_compiled_card_evidence,
    get_card_evidence_artefact,
)

_REPO = Path(__file__).resolve().parents[3]
_FRONTEND_SUBSYSTEM = (
    _REPO / "frontend" / "app" / "components" / "results" / "Wave1SubsystemEvidenceSection.tsx"
)

_FULL_PANEL = {
    "total_cholesterol",
    "ldl_cholesterol",
    "hdl_cholesterol",
    "triglycerides",
    "homocysteine",
    "crp",
    "glucose",
    "hba1c",
    "insulin",
    "alt",
    "ast",
    "ggt",
    "alp",
    "albumin",
    "bilirubin",
}


def _domain_rows(panel: set[str] | None = None):
    scoring = {
        "health_system_scores": {
            "cardiovascular": {
                "overall_score": 72.0,
                "missing_biomarkers": ["tc_hdl_ratio"],
                "biomarker_scores": [{"biomarker_name": "total_cholesterol"}],
            },
            "metabolic": {
                "overall_score": 68.0,
                "missing_biomarkers": ["insulin"],
                "biomarker_scores": [
                    {"biomarker_name": "glucose"},
                    {"biomarker_name": "hba1c"},
                ],
            },
            "liver": {
                "overall_score": 75.0,
                "missing_biomarkers": [],
                "biomarker_scores": [{"biomarker_name": "alt"}],
            },
        }
    }
    ig = InsightGraphV1(
        analysis_id="med-rev-1",
        signal_results=[],
        system_capacity_scores={"hepatic": 70, "cardiovascular": 80, "metabolic": 70},
        confidence=ConfidenceModelV1(
            cluster_confidence={"cardiovascular": 0.9, "metabolic": 0.7, "hepatic": 0.7}
        ),
    )
    rows, _ = assemble_consumer_domain_scores_v1(
        scoring_result=scoring,
        insight_graph=ig,
        idl_bundle=None,
        derived_ratios_meta=None,
        panel_biomarker_ids=panel or _FULL_PANEL,
    )
    return rows


@pytest.mark.regression
def test_med_rev1_compiled_tier_partition_covers_all_seven() -> None:
    assert (
        WAVE1_MED_REV1_SCORED_VISIBLE_SUBSYSTEM_IDS | WAVE1_MED_REV1_HIDDEN_SUBSYSTEM_IDS
        == WAVE1_COMPILED_SUBSYSTEM_IDS
    )


@pytest.mark.parametrize("subsystem_id", sorted(WAVE1_MED_REV1_HIDDEN_SUBSYSTEM_IDS))
def test_med_rev1_hidden_subsystems_suppressed_at_layer_b(subsystem_id: str) -> None:
    row = assemble_subsystem_from_compiled_card_evidence(
        subsystem_id=subsystem_id,
        panel_biomarker_ids=_FULL_PANEL,
        scored_on_rail=set(),
    )
    assert row is None


@pytest.mark.parametrize("subsystem_id", sorted(WAVE1_MED_REV1_SCORED_VISIBLE_SUBSYSTEM_IDS))
def test_med_rev1_scored_subsystems_emitted_at_layer_b(subsystem_id: str) -> None:
    row = assemble_subsystem_from_compiled_card_evidence(
        subsystem_id=subsystem_id,
        panel_biomarker_ids=_FULL_PANEL,
        scored_on_rail=set(),
    )
    assert row is not None
    assert row.visibility_tier == "scored_subsystem"


@pytest.mark.regression
def test_med_rev1_consumer_labels_aligned() -> None:
    lipid = get_card_evidence_artefact("wave1_cv_lipid_transport")
    assert lipid.subsystem_label == "Atherogenic lipid pattern"
    glycaemic = get_card_evidence_artefact("wave1_met_glycaemic_control")
    assert glycaemic.subsystem_label == "Long-term blood sugar"


@pytest.mark.regression
def test_med_rev1_dto_surfacing_matches_medical_model() -> None:
    by_id = {r.domain_id: r for r in _domain_rows()}
    cv_ids = {s.subsystem_id for s in by_id["wave1_cardiovascular"].subsystems or []}
    assert cv_ids == {"wave1_cv_lipid_transport"}
    met_ids = {s.subsystem_id for s in by_id["wave1_blood_sugar"].subsystems or []}
    assert met_ids == {"wave1_met_glycaemic_control"}
    assert by_id["wave1_liver"].subsystems in (None, [])


@pytest.mark.regression
def test_med_rev1_homocysteine_not_scored_standalone_subsystem() -> None:
    rows = assemble_wave1_subsystem_evidence(
        domain_id="wave1_cardiovascular",
        panel_biomarker_ids={"homocysteine", "total_cholesterol", "ldl_cholesterol"},
        rail_biomarker_scores=[{"biomarker_name": "total_cholesterol"}],
    )
    assert "wave1_cv_homocysteine_pathway" not in {r.subsystem_id for r in rows}


@pytest.mark.regression
def test_med_rev1_vascular_strain_not_over_surfaced() -> None:
    rows = assemble_wave1_subsystem_evidence(
        domain_id="wave1_cardiovascular",
        panel_biomarker_ids={"crp", "total_cholesterol"},
        rail_biomarker_scores=[{"biomarker_name": "total_cholesterol"}],
    )
    assert "wave1_cv_vascular_strain" not in {r.subsystem_id for r in rows}


@pytest.mark.regression
def test_med_rev1_insulin_context_hidden_on_thin_panel() -> None:
    rows = assemble_wave1_subsystem_evidence(
        domain_id="wave1_blood_sugar",
        panel_biomarker_ids={"triglycerides", "hba1c"},
        rail_biomarker_scores=[{"biomarker_name": "hba1c"}],
    )
    assert "wave1_met_insulin_metabolic" not in {r.subsystem_id for r in rows}


@pytest.mark.regression
def test_med_rev1_liver_flat_card_no_scored_subsystems() -> None:
    rows = assemble_wave1_subsystem_evidence(
        domain_id="wave1_liver",
        panel_biomarker_ids={"alt", "bilirubin", "alp", "albumin"},
        rail_biomarker_scores=[{"biomarker_name": "alt"}],
    )
    assert rows == []


@pytest.mark.regression
def test_med_rev1_total_bilirubin_protection_intact() -> None:
    artefact = get_card_evidence_artefact("wave1_liv_processing_context")
    assert "total_bilirubin" not in {m.marker_id for m in artefact.markers}


@pytest.mark.regression
def test_med_rev1_frontend_render_only_no_visibility_inference() -> None:
    src = _FRONTEND_SUBSYSTEM.read_text(encoding="utf-8")
    assert "visibility_tier" not in src
    assert "inferClinical" not in src
    assert "deriveSubsystem" not in src
