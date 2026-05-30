"""ARCH-RT-5B — Wave 1 card evidence estate promotion and provenance boundaries."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from core.analytics.wave1_subsystem_evidence import assemble_wave1_subsystem_evidence
from core.knowledge.health_system_card_evidence import (
    WAVE1_COMPILED_SUBSYSTEM_IDS,
    CardEvidenceValidationError,
    compiled_cards_dir,
    get_card_evidence_artefact,
    load_card_evidence_artefact,
    validate_card_evidence_payload,
)
from core.knowledge.launch_estate_v1 import estate_index_path, resolve_compile_manifest_ref

_REPO = Path(__file__).resolve().parents[3]
_FRONTEND_SUBSYSTEM = (
    _REPO / "frontend" / "app" / "components" / "results" / "Wave1SubsystemEvidenceSection.tsx"
)

_RT5B_PROMOTED = (
    "wave1_cv_lipid_transport",
    "wave1_cv_homocysteine_pathway",
    "wave1_cv_vascular_strain",
    "wave1_met_insulin_metabolic",
    "wave1_liv_enzyme_pattern",
    "wave1_liv_processing_context",
)


@pytest.mark.parametrize("subsystem_id", _RT5B_PROMOTED)
def test_rt5b_artefact_validates(subsystem_id: str):
    path = compiled_cards_dir() / f"{subsystem_id}.yaml"
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    validate_card_evidence_payload(payload, path=str(path))
    artefact = load_card_evidence_artefact(subsystem_id)
    assert artefact.subsystem_id == subsystem_id
    assert "total_bilirubin" not in {m.marker_id for m in artefact.markers}


@pytest.mark.parametrize("subsystem_id", WAVE1_COMPILED_SUBSYSTEM_IDS)
def test_manifest_ref_resolves_for_all_compiled(subsystem_id: str):
    artefact = get_card_evidence_artefact(subsystem_id)
    assert resolve_compile_manifest_ref(artefact.compile_manifest_ref) is not None


def test_estate_index_covers_all_wave1_subsystems():
    payload = yaml.safe_load(estate_index_path().read_text(encoding="utf-8"))
    indexed = {row["subsystem_id"] for row in payload["card_evidence_artefacts"]}
    assert indexed == set(WAVE1_COMPILED_SUBSYSTEM_IDS)


@pytest.mark.parametrize("subsystem_id", _RT5B_PROMOTED)
def test_loader_registered_for_promoted(subsystem_id: str):
    artefact = get_card_evidence_artefact(subsystem_id)
    assert artefact.compile_manifest_ref


def test_loader_fail_closed_for_unregistered_subsystem():
    with pytest.raises(CardEvidenceValidationError):
        get_card_evidence_artefact("wave2_unknown_subsystem")


@pytest.mark.parametrize("subsystem_id", _RT5B_PROMOTED)
def test_assembler_uses_compiled_path(subsystem_id: str):
    domain_map = {
        "wave1_cv_lipid_transport": "wave1_cardiovascular",
        "wave1_cv_homocysteine_pathway": "wave1_cardiovascular",
        "wave1_cv_vascular_strain": "wave1_cardiovascular",
        "wave1_met_insulin_metabolic": "wave1_blood_sugar",
        "wave1_liv_enzyme_pattern": "wave1_liver",
        "wave1_liv_processing_context": "wave1_liver",
    }
    panel = {
        "total_cholesterol",
        "ldl_cholesterol",
        "hdl_cholesterol",
        "triglycerides",
        "homocysteine",
        "crp",
        "insulin",
        "alt",
        "ast",
        "ggt",
        "alp",
        "albumin",
        "bilirubin",
    }
    rows = assemble_wave1_subsystem_evidence(
        domain_id=domain_map[subsystem_id],
        panel_biomarker_ids=panel,
        rail_biomarker_scores=[{"biomarker_name": "alt"}],
    )
    row = next(r for r in rows if r.subsystem_id == subsystem_id)
    assert row.source_trace.startswith("health_system_card_evidence_v1:")
    assert row.marker_evidence is not None


def test_bilirubin_canonical_on_processing_context_compiled():
    rows = assemble_wave1_subsystem_evidence(
        domain_id="wave1_liver",
        panel_biomarker_ids={"bilirubin", "alp", "albumin"},
        rail_biomarker_scores=[],
    )
    processing = next(r for r in rows if r.subsystem_id == "wave1_liv_processing_context")
    assert "bilirubin" in processing.included_marker_ids
    assert "total_bilirubin" not in processing.missing_marker_ids
    marker_ids = {m.marker_id for m in processing.marker_evidence or []}
    assert "bilirubin" in marker_ids
    assert "total_bilirubin" not in marker_ids


def test_lipid_artefact_does_not_reference_pkg_lipid_transport():
    artefact = get_card_evidence_artefact("wave1_cv_lipid_transport")
    refs = artefact.provenance.get("package_refs") or []
    assert "pkg_lipid_transport" not in refs


def test_frontend_filters_internal_source_trace():
    src = _FRONTEND_SUBSYSTEM.read_text(encoding="utf-8")
    assert "isConsumerSafeSourceTrace" in src
    assert "wave1_subsystem_evidence_v1:" not in src
