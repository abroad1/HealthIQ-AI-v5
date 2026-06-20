"""P1-2 — Kidney function launch-core domain card tests."""

from __future__ import annotations

from core.analytics.domain_score_assembler import assemble_consumer_domain_scores_v1
from core.analytics.wave1_subsystem_evidence import (
    WAVE1_DOMAIN_IDS,
    assemble_wave1_subsystem_evidence,
)
from core.contracts.confidence_model_v1 import ConfidenceModelV1
from core.contracts.insight_graph_v1 import InsightGraphV1
from core.knowledge.health_system_card_evidence import get_card_evidence_artefact


def _minimal_graph(*, signal_results: list | None = None) -> InsightGraphV1:
    return InsightGraphV1(
        analysis_id="p1-2",
        signal_results=signal_results or [],
        system_capacity_scores={},
        confidence=ConfidenceModelV1(cluster_confidence={"kidney": 0.8}),
    )


def test_wave1_domain_ids_include_kidney():
    assert "wave1_kidney" in WAVE1_DOMAIN_IDS


def test_kidney_compiled_card_artefact_loads():
    artefact = get_card_evidence_artefact("wave1_ren_glomerular_filtration")
    assert artefact.domain_id == "wave1_kidney"
    assert artefact.subsystem_id == "wave1_ren_glomerular_filtration"
    marker_ids = {m.marker_id for m in artefact.markers}
    assert marker_ids >= {"creatinine", "egfr"}


def test_kidney_subsystem_evidence_from_panel():
    panel = {"creatinine", "egfr", "urea"}
    rows = assemble_wave1_subsystem_evidence(
        domain_id="wave1_kidney",
        panel_biomarker_ids=panel,
        rail_biomarker_scores=[
            {"biomarker_name": "creatinine"},
            {"biomarker_name": "egfr"},
        ],
    )
    assert len(rows) == 1
    assert rows[0].subsystem_id == "wave1_ren_glomerular_filtration"
    assert rows[0].subsystem_label == "Kidney filtration markers"


def test_assembler_emits_four_domains_including_kidney():
    scoring = {
        "health_system_scores": {
            "cardiovascular": {"overall_score": 72.0, "missing_biomarkers": []},
            "metabolic": {"overall_score": 68.0, "missing_biomarkers": []},
            "liver": {"overall_score": 75.0, "missing_biomarkers": []},
            "kidney": {
                "overall_score": 70.0,
                "missing_biomarkers": ["urea"],
                "biomarker_scores": [
                    {"biomarker_name": "creatinine"},
                    {"biomarker_name": "egfr"},
                ],
            },
        }
    }
    panel = {"creatinine", "egfr", "alt", "glucose", "hba1c", "ldl_cholesterol"}
    rows, _ = assemble_consumer_domain_scores_v1(
        scoring_result=scoring,
        insight_graph=_minimal_graph(),
        idl_bundle=None,
        derived_ratios_meta=None,
        panel_biomarker_ids=panel,
    )
    assert len(rows) == 4
    assert [r.domain_id for r in rows] == [
        "wave1_cardiovascular",
        "wave1_blood_sugar",
        "wave1_liver",
        "wave1_kidney",
    ]
    kidney = rows[3]
    assert kidney.consumer_label == "Kidney function"
    assert kidney.subsystems
    assert kidney.subsystems[0].subsystem_id == "wave1_ren_glomerular_filtration"
    joined = " ".join(
        [
            kidney.headline_sentence or "",
            kidney.contributor_sentence or "",
            kidney.consequence_sentence or "",
            kidney.next_step_sentence or "",
        ]
    ).lower()
    assert "ckd" not in joined
    assert "kidney disease" not in joined
    assert "renal failure" not in joined


def test_kidney_collects_egfr_and_creatinine_signals_only():
    scoring = {
        "health_system_scores": {
            "cardiovascular": {"overall_score": 80.0, "missing_biomarkers": []},
            "metabolic": {"overall_score": 80.0, "missing_biomarkers": []},
            "liver": {"overall_score": 80.0, "missing_biomarkers": []},
            "kidney": {"overall_score": 55.0, "missing_biomarkers": []},
        }
    }
    signals = [
        {
            "signal_id": "signal_egfr_low",
            "signal_state": "at_risk",
            "primary_metric": "egfr",
            "system": "renal",
        },
        {
            "signal_id": "signal_creatinine_high",
            "signal_state": "at_risk",
            "primary_metric": "creatinine",
            "system": "renal",
        },
        {
            "signal_id": "signal_urea_high",
            "signal_state": "at_risk",
            "primary_metric": "urea",
            "system": "renal",
        },
    ]
    rows, _ = assemble_consumer_domain_scores_v1(
        scoring_result=scoring,
        insight_graph=_minimal_graph(signal_results=signals),
        idl_bundle=None,
        derived_ratios_meta=None,
        panel_biomarker_ids={"creatinine", "egfr", "urea", "alt", "glucose", "hba1c", "ldl_cholesterol"},
    )
    kidney = rows[3]
    assert "signal_egfr_low" in kidney.active_signal_ids
    assert "signal_creatinine_high" in kidney.active_signal_ids
    assert "signal_urea_high" not in kidney.active_signal_ids
