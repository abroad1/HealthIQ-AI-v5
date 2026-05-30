"""ARCH-RT-3 — card evidence schema, loader, pilot assembly, and regression boundaries."""

from __future__ import annotations

import copy
from pathlib import Path

import pytest
import yaml

from core.analytics.domain_score_assembler import assemble_consumer_domain_scores_v1
from core.analytics.wave1_subsystem_evidence import assemble_wave1_subsystem_evidence
from core.contracts.confidence_model_v1 import ConfidenceModelV1
from core.contracts.insight_graph_v1 import InsightGraphV1
from core.knowledge.health_system_card_evidence import (
    PILOT_SUBSYSTEM_ID,
    CardEvidenceValidationError,
    compiled_cards_dir,
    get_card_evidence_artefact,
    load_card_evidence_artefact,
    schema_path,
    validate_card_evidence_payload,
)
from core.models.results import SubsystemEvidenceV1, SubsystemMarkerEvidenceV1

_REPO_ROOT = Path(__file__).resolve().parents[3]
_PILOT_PATH = compiled_cards_dir() / f"{PILOT_SUBSYSTEM_ID}.yaml"
_FRONTEND_SUBSYSTEM = (
    _REPO_ROOT / "frontend" / "app" / "components" / "results" / "Wave1SubsystemEvidenceSection.tsx"
)


def _minimal_scoring():
    return {
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


def _assemble_rows(panel: set[str] | None = None):
    ig = InsightGraphV1(
        analysis_id="arch-rt-3",
        signal_results=[],
        system_capacity_scores={"hepatic": 70, "cardiovascular": 80, "metabolic": 70},
        confidence=ConfidenceModelV1(
            cluster_confidence={"cardiovascular": 0.9, "metabolic": 0.7, "hepatic": 0.7}
        ),
    )
    panel = panel or {"total_cholesterol", "glucose", "hba1c", "alt", "ldl_cholesterol", "hdl_cholesterol", "triglycerides"}
    rows, _ = assemble_consumer_domain_scores_v1(
        scoring_result=_minimal_scoring(),
        insight_graph=ig,
        idl_bundle=None,
        derived_ratios_meta=None,
        panel_biomarker_ids=panel,
    )
    return rows


def test_schema_file_exists_and_loads():
    payload = yaml.safe_load(schema_path().read_text(encoding="utf-8"))
    assert payload["schema_version"] == "1.0.0"
    assert "markers" in payload["root_required_fields"]


def test_pilot_artefact_validates():
    payload = yaml.safe_load(_PILOT_PATH.read_text(encoding="utf-8"))
    validate_card_evidence_payload(payload, path=str(_PILOT_PATH))
    artefact = load_card_evidence_artefact(PILOT_SUBSYSTEM_ID)
    assert artefact.subsystem_id == PILOT_SUBSYSTEM_ID
    assert artefact.domain_id == "wave1_blood_sugar"
    assert tuple(m.marker_id for m in artefact.markers) == ("glucose", "hba1c")


def test_loader_fail_closed_on_invalid_artefact(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    bad = {
        "schema_version": "1.0.0",
        "artefact_id": "bad",
        "domain_id": "wave1_blood_sugar",
        "subsystem_id": PILOT_SUBSYSTEM_ID,
        "subsystem_label": "Glycaemic control",
        "visibility_tier": "scored_subsystem",
        "source_spec_ids": ["inv_test"],
        "compile_manifest_ref": "bad-ref",
        "markers": [],
        "provenance": {"artefact_kind": "health_system_card_evidence_v1", "compile_status": "pilot_manual"},
    }
    with pytest.raises(CardEvidenceValidationError):
        validate_card_evidence_payload(bad)

    payload = yaml.safe_load(_PILOT_PATH.read_text(encoding="utf-8"))
    broken = copy.deepcopy(payload)
    broken["markers"][0]["marker_id"] = "total_bilirubin"
    with pytest.raises(CardEvidenceValidationError):
        validate_card_evidence_payload(broken)


def test_pilot_subsystem_assembly_uses_compiled_roles():
    rows = _assemble_rows()
    sugar = next(r for r in rows if r.domain_id == "wave1_blood_sugar")
    glycaemic = next(s for s in sugar.subsystems or [] if s.subsystem_id == PILOT_SUBSYSTEM_ID)
    assert glycaemic.source_trace.startswith("health_system_card_evidence_v1:")
    assert glycaemic.marker_evidence is not None
    roles = {m.marker_id: m.marker_role for m in glycaemic.marker_evidence}
    assert roles["glucose"] == "score_contributor"
    assert roles["hba1c"] == "score_contributor"
    assert "glucose" in glycaemic.included_marker_ids
    assert "hba1c" in glycaemic.included_marker_ids


def test_non_pilot_subsystem_uses_compiled_path_after_rt5b():
    rows = _assemble_rows()
    cv = next(r for r in rows if r.domain_id == "wave1_cardiovascular")
    lipid = next(s for s in cv.subsystems or [] if s.subsystem_id == "wave1_cv_lipid_transport")
    assert lipid.source_trace.startswith("health_system_card_evidence_v1:")
    assert lipid.card_evidence_schema_version == "1.0.0"
    assert lipid.marker_evidence is not None


def test_direct_assembly_all_wave1_subsystems_use_compiled_path():
    panel = {"glucose", "hba1c", "total_cholesterol", "insulin"}
    rail = [{"biomarker_name": "glucose"}, {"biomarker_name": "total_cholesterol"}]
    sugar_rows = assemble_wave1_subsystem_evidence(
        domain_id="wave1_blood_sugar",
        panel_biomarker_ids=panel,
        rail_biomarker_scores=rail,
    )
    for row in sugar_rows:
        assert row.source_trace.startswith("health_system_card_evidence_v1:")
        assert row.marker_evidence is not None


def test_dto_serialisation_new_optional_fields():
    artefact = get_card_evidence_artefact(PILOT_SUBSYSTEM_ID)
    row = SubsystemEvidenceV1(
        subsystem_id=artefact.subsystem_id,
        subsystem_label=artefact.subsystem_label,
        included_marker_ids=["glucose"],
        missing_marker_ids=["hba1c"],
        source_trace="health_system_card_evidence_v1:test",
        card_evidence_schema_version="1.0.0",
        visibility_tier="scored_subsystem",
        source_spec_ids=list(artefact.source_spec_ids),
        compile_manifest_ref=artefact.compile_manifest_ref,
        marker_evidence=[
            SubsystemMarkerEvidenceV1(
                marker_id="glucose",
                display_label="Glucose",
                marker_role="score_contributor",
                relationship_kind="direct_score_input",
                presence_policy="required_for_subsystem",
            )
        ],
    )
    dumped = row.model_dump()
    assert dumped["marker_evidence"][0]["marker_role"] == "score_contributor"
    assert dumped["visibility_tier"] == "scored_subsystem"


def test_bilirubin_fix_not_reintroduced_on_liver_path():
    panel = {
        "bilirubin",
        "alp",
        "albumin",
        "glucose",
        "hba1c",
        "alt",
        "total_cholesterol",
    }
    rows = _assemble_rows(panel=panel)
    liver = next(r for r in rows if r.domain_id == "wave1_liver")
    processing = next(s for s in liver.subsystems or [] if s.subsystem_id == "wave1_liv_processing_context")
    assert "bilirubin" in processing.included_marker_ids
    assert "total_bilirubin" not in processing.missing_marker_ids


def test_frontend_does_not_infer_marker_roles_from_names():
    src = _FRONTEND_SUBSYSTEM.read_text(encoding="utf-8")
    assert "markerRoleFromId" not in src
    assert "marker_role" in src
    assert "marker_evidence" in src
    assert "score_contributor" not in src
