"""
DOMAIN-UX1C — Governed subsystem evidence model regression.

Sentinel classes:
  health_system_subsystems_missing_from_dto
  health_system_subsystem_labels_frontend_defined
  health_system_subsystem_marker_grouping_frontend_defined
  health_system_subsystem_fake_status_emitted
  health_system_wave2_subsystems_prematurely_emitted
"""

from __future__ import annotations

from pathlib import Path

import pytest

from core.analytics.domain_score_assembler import assemble_consumer_domain_scores_v1
from core.analytics.wave1_subsystem_evidence import WAVE1_DOMAIN_IDS
from core.contracts.confidence_model_v1 import ConfidenceModelV1
from core.contracts.insight_graph_v1 import InsightGraphV1
from core.knowledge.health_system_card_evidence import get_card_evidence_artefact

_REPO_ROOT = Path(__file__).resolve().parents[3]
_WAVE1_CARDS = _REPO_ROOT / "frontend" / "app" / "components" / "results" / "Wave1DomainCards.tsx"
_SUBSYSTEM_MODULE = _REPO_ROOT / "backend" / "core" / "analytics" / "wave1_subsystem_evidence.py"
_FRONTEND_TYPES = _REPO_ROOT / "frontend" / "app" / "types" / "analysis.ts"


def _read(path: Path) -> str:
    assert path.is_file(), f"missing {path}"
    return path.read_text(encoding="utf-8")


def _minimal_rows(panel: set[str] | None = None):
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
        analysis_id="ux1c",
        signal_results=[],
        system_capacity_scores={"hepatic": 70, "cardiovascular": 80, "metabolic": 70},
        confidence=ConfidenceModelV1(cluster_confidence={"cardiovascular": 0.9, "metabolic": 0.7, "hepatic": 0.7}),
    )
    panel = panel or {
        "total_cholesterol",
        "glucose",
        "hba1c",
        "alt",
        "ast",
        "ldl_cholesterol",
        "hdl_cholesterol",
        "triglycerides",
    }
    rows, _ = assemble_consumer_domain_scores_v1(
        scoring_result=scoring,
        insight_graph=ig,
        idl_bundle=None,
        derived_ratios_meta=None,
        panel_biomarker_ids=panel,
    )
    return rows


@pytest.mark.regression
def test_wave1_domains_emit_subsystems() -> None:
    by_id = {r.domain_id: r for r in _minimal_rows()}
    assert len(by_id["wave1_cardiovascular"].subsystems or []) == 1
    assert len(by_id["wave1_blood_sugar"].subsystems or []) == 1
    assert by_id["wave1_liver"].subsystems in (None, [])


@pytest.mark.regression
def test_subsystem_rows_have_required_fields() -> None:
    for row in _minimal_rows():
        for sub in row.subsystems or []:
            assert sub.subsystem_id.startswith("wave1_")
            assert sub.subsystem_label.strip()
            assert isinstance(sub.included_marker_ids, list)
            assert isinstance(sub.missing_marker_ids, list)
            assert isinstance(sub.included_markers, list)
            assert isinstance(sub.missing_markers, list)
            assert all(m.id and m.display_label for m in sub.included_markers or [])
            assert all(m.id and m.display_label for m in sub.missing_markers or [])
            assert sub.source_trace.startswith("health_system_card_evidence_v1:")
            if sub.subsystem_id == "wave1_met_glycaemic_control":
                assert sub.source_trace.startswith("health_system_card_evidence_v1:")
                assert sub.card_evidence_schema_version == "1.0.0"
                assert sub.visibility_tier == "scored_subsystem"
                assert sub.subsystem_label == "Long-term blood sugar"
                assert sub.marker_evidence is not None
                assert len(sub.marker_evidence) == 2
            elif sub.subsystem_id == "wave1_cv_lipid_transport":
                assert sub.subsystem_label == "Atherogenic lipid pattern"
            assert sub.status_label is None


@pytest.mark.regression
def test_subsystem_marker_ids_are_canonical_and_partitioned() -> None:
    cv = next(r for r in _minimal_rows() if r.domain_id == "wave1_cardiovascular")
    lipid = next(s for s in cv.subsystems or [] if s.subsystem_id == "wave1_cv_lipid_transport")
    assert "total_cholesterol" in lipid.included_marker_ids
    assert "tc_hdl_ratio" in lipid.missing_marker_ids
    for mid in lipid.included_marker_ids + lipid.missing_marker_ids:
        assert mid == mid.lower()
        assert " " not in mid
    included_map = {m.id: m.display_label for m in lipid.included_markers or []}
    missing_map = {m.id: m.display_label for m in lipid.missing_markers or []}
    assert included_map["ldl_cholesterol"] == "LDL Cholesterol"
    assert included_map["hdl_cholesterol"] == "HDL Cholesterol"
    assert missing_map["tc_hdl_ratio"] == "TC:HDL ratio"


@pytest.mark.regression
def test_liver_processing_bilirubin_canonical_not_total_bilirubin_false_missing() -> None:
    """Canonical bilirubin satisfies liver processing artefact; total_bilirubin is rail-only."""
    from core.knowledge.health_system_card_evidence import assemble_subsystem_from_compiled_card_evidence

    processing = assemble_subsystem_from_compiled_card_evidence(
        subsystem_id="wave1_liv_processing_context",
        panel_biomarker_ids={"bilirubin", "alp", "albumin"},
        scored_on_rail=set(),
    )
    assert processing is None
    artefact = get_card_evidence_artefact("wave1_liv_processing_context")
    marker_ids = {m.marker_id for m in artefact.markers}
    assert "bilirubin" in marker_ids
    assert "total_bilirubin" not in marker_ids


@pytest.mark.regression
def test_missing_markers_receive_governed_display_labels_even_when_absent_from_panel() -> None:
    from core.knowledge.health_system_card_evidence import assemble_subsystem_from_compiled_card_evidence

    glycaemic = assemble_subsystem_from_compiled_card_evidence(
        subsystem_id="wave1_met_glycaemic_control",
        panel_biomarker_ids={"hba1c"},
        scored_on_rail=set(),
    )
    assert glycaemic is not None
    missing_map = {m.id: m.display_label for m in glycaemic.missing_markers or []}
    assert "glucose" in glycaemic.missing_marker_ids
    assert missing_map["glucose"] == "Glucose"


@pytest.mark.regression
def test_health_system_subsystems_missing_from_dto_sentinel() -> None:
    """Sentinel: health_system_subsystems_missing_from_dto."""
    src = _read(_SUBSYSTEM_MODULE)
    assert "assemble_wave1_subsystem_evidence" in src
    by_id = {r.domain_id: r for r in _minimal_rows()}
    assert by_id["wave1_cardiovascular"].subsystems
    assert by_id["wave1_blood_sugar"].subsystems


@pytest.mark.regression
def test_wave1_backend_module_has_no_hard_coded_subsystem_defs_sentinel() -> None:
    """Sentinel: hard-coded Wave 1 subsystem fallback partition removed (ARCH-LEGACY-2)."""
    src = _read(_SUBSYSTEM_MODULE)
    assert "_Wave1SubsystemDef" not in src
    assert "WAVE1_DOMAIN_SUBSYSTEM_DEFS" not in src


@pytest.mark.regression
def test_health_system_subsystem_labels_frontend_defined_sentinel() -> None:
    """Sentinel: health_system_subsystem_labels_frontend_defined."""
    cards = _read(_WAVE1_CARDS)
    types_src = _read(_FRONTEND_TYPES)
    assert "Lipid transport" not in cards
    assert "wave1_cv_lipid_transport" not in cards
    assert "WAVE1_DOMAIN_SUBSYSTEM_DEFS" not in types_src
    assert "SubsystemEvidenceV1" in types_src


@pytest.mark.regression
def test_health_system_subsystem_marker_grouping_frontend_defined_sentinel() -> None:
    """Sentinel: health_system_subsystem_marker_grouping_frontend_defined."""
    cards = _read(_WAVE1_CARDS)
    assert "included_marker_ids" not in cards
    assert "assemble_wave1_subsystem_evidence" not in cards
    assert "wave1_subsystem_evidence" not in cards


@pytest.mark.regression
def test_health_system_subsystem_fake_status_emitted_sentinel() -> None:
    """Sentinel: health_system_subsystem_fake_status_emitted."""
    for row in _minimal_rows():
        for sub in row.subsystems or []:
            assert sub.status_label is None


@pytest.mark.regression
def test_health_system_wave2_subsystems_prematurely_emitted_sentinel() -> None:
    """Sentinel: health_system_wave2_subsystems_prematurely_emitted."""
    assert WAVE1_DOMAIN_IDS == frozenset(
        {"wave1_cardiovascular", "wave1_blood_sugar", "wave1_liver"}
    )
    from core.analytics.wave1_subsystem_evidence import assemble_wave1_subsystem_evidence

    assert assemble_wave1_subsystem_evidence(
        domain_id="blood_iron_oxygen",
        panel_biomarker_ids=set(),
        rail_biomarker_scores=[],
    ) == []
