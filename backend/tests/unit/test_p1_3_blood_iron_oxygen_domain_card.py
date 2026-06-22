"""P1-3 — Blood / iron / oxygen launch-core domain card tests."""

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
        analysis_id="p1-3",
        signal_results=signal_results or [],
        system_capacity_scores={},
        confidence=ConfidenceModelV1(cluster_confidence={"cbc": 0.8}),
    )


def test_wave1_domain_ids_include_blood_iron_oxygen():
    assert "wave1_blood_iron_oxygen" in WAVE1_DOMAIN_IDS


def test_blood_iron_oxygen_compiled_card_artefact_loads():
    artefact = get_card_evidence_artefact("wave1_bio_oxygen_carrying_capacity")
    assert artefact.domain_id == "wave1_blood_iron_oxygen"
    assert artefact.subsystem_id == "wave1_bio_oxygen_carrying_capacity"
    marker_ids = {m.marker_id for m in artefact.markers}
    assert marker_ids >= {"hemoglobin", "hematocrit", "ferritin"}


def test_blood_iron_oxygen_subsystem_evidence_from_panel():
    panel = {"hemoglobin", "hematocrit", "ferritin"}
    rows = assemble_wave1_subsystem_evidence(
        domain_id="wave1_blood_iron_oxygen",
        panel_biomarker_ids=panel,
        rail_biomarker_scores=[
            {"biomarker_name": "hemoglobin"},
            {"biomarker_name": "hematocrit"},
        ],
    )
    assert len(rows) == 1
    assert rows[0].subsystem_id == "wave1_bio_oxygen_carrying_capacity"
    assert rows[0].subsystem_label == "Red-cell and oxygen-carrying markers"


def test_assembler_emits_five_domains_including_blood_iron_oxygen():
    scoring = {
        "health_system_scores": {
            "cardiovascular": {"overall_score": 72.0, "missing_biomarkers": []},
            "metabolic": {"overall_score": 68.0, "missing_biomarkers": []},
            "liver": {"overall_score": 75.0, "missing_biomarkers": []},
            "kidney": {"overall_score": 70.0, "missing_biomarkers": []},
            "cbc": {
                "overall_score": 65.0,
                "missing_biomarkers": [],
                "biomarker_scores": [
                    {"biomarker_name": "hemoglobin"},
                    {"biomarker_name": "hematocrit"},
                ],
            },
            "hormonal": {"overall_score": 70.0, "missing_biomarkers": []},
        }
    }
    panel = {
        "hemoglobin",
        "hematocrit",
        "ferritin",
        "creatinine",
        "egfr",
        "alt",
        "glucose",
        "hba1c",
        "ldl_cholesterol",
    }
    rows, _ = assemble_consumer_domain_scores_v1(
        scoring_result=scoring,
        insight_graph=_minimal_graph(),
        idl_bundle=None,
        derived_ratios_meta=None,
        panel_biomarker_ids=panel,
    )
    assert len(rows) == 6
    assert [r.domain_id for r in rows][:5] == [
        "wave1_cardiovascular",
        "wave1_blood_sugar",
        "wave1_liver",
        "wave1_kidney",
        "wave1_blood_iron_oxygen",
    ]
    bio = rows[4]
    assert bio.consumer_label == "Blood / iron / oxygen"
    assert bio.subsystems
    assert bio.subsystems[0].subsystem_id == "wave1_bio_oxygen_carrying_capacity"
    joined = " ".join(
        [
            bio.headline_sentence or "",
            bio.contributor_sentence or "",
            bio.consequence_sentence or "",
            bio.next_step_sentence or "",
        ]
    ).lower()
    assert "anaemia" not in joined
    assert "iron deficiency" not in joined
    assert "bleeding" not in joined
    assert "haemochromatosis" not in joined
    assert "cancer" not in joined


def test_blood_iron_oxygen_excludes_blocked_signals_from_active_list():
    scoring = {
        "health_system_scores": {
            "cardiovascular": {"overall_score": 80.0, "missing_biomarkers": []},
            "metabolic": {"overall_score": 80.0, "missing_biomarkers": []},
            "liver": {"overall_score": 80.0, "missing_biomarkers": []},
            "kidney": {"overall_score": 80.0, "missing_biomarkers": []},
            "cbc": {"overall_score": 55.0, "missing_biomarkers": []},
            "hormonal": {"overall_score": 55.0, "missing_biomarkers": []},
        }
    }
    signals = [
        {
            "signal_id": "signal_hemoglobin_low",
            "signal_state": "at_risk",
            "primary_metric": "hemoglobin",
            "system": "hematologic",
        },
        {
            "signal_id": "signal_ferritin_low",
            "signal_state": "at_risk",
            "primary_metric": "ferritin",
            "system": "immune",
        },
        {
            "signal_id": "signal_white_blood_cells_high",
            "signal_state": "at_risk",
            "primary_metric": "white_blood_cells",
            "system": "cbc",
        },
    ]
    rows, _ = assemble_consumer_domain_scores_v1(
        scoring_result=scoring,
        insight_graph=_minimal_graph(signal_results=signals),
        idl_bundle=None,
        derived_ratios_meta=None,
        panel_biomarker_ids={
            "hemoglobin",
            "hematocrit",
            "ferritin",
            "white_blood_cells",
            "creatinine",
            "egfr",
            "alt",
            "glucose",
            "hba1c",
            "ldl_cholesterol",
        },
    )
    bio = rows[4]
    assert bio.active_signal_ids == []
