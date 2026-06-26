"""P2-1 — prose substrate wave 1 wired (iron / thyroid lead hints + signal-scoped routing)."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from core.analytics.narrative_compiler_lc_s3_assembly_v1 import (
    _LEAD_SIGNAL_HINTS as LC3_LEAD_HINTS,
    infer_yaml_flags_from_payload,
)
from core.analytics.narrative_payload_builder_v1 import build_narrative_payload_v1
from core.analytics.narrative_report_compiler_v1 import (
    _LEAD_SIGNAL_HINTS as COMPILER_LEAD_HINTS,
    compile_narrative_report_v1,
)
from core.contracts.narrative_payload_v1 import NarrativePayloadV1
from core.contracts.report_v1 import (
    ReportActionsV1,
    ReportMetaV1,
    ReportTopFindingV1,
    ReportV1,
)

_REPO = Path(__file__).resolve().parents[3]
_ENTITIES = _REPO / "knowledge_bus" / "interpretation_entities_v1" / "benchmark_interpretation_entities_v1.yaml"
_PATHWAYS = _REPO / "knowledge_bus" / "pathway_explainers_v1" / "pathway_explainers_v1.yaml"
_FUNCTIONAL = _REPO / "knowledge_bus" / "functional_interpretation_v1" / "functional_interpretation_v1.yaml"

_IRON_SIGNALS = ("signal_iron_low", "signal_iron_high")
_THYROID_SIGNALS = ("signal_free_t3_low", "signal_tpo_ab_high")

_HOMOCYSTEINE_MARKERS = ("homocysteine", "one-carbon", "methylation")
_IRON_MARKERS = ("iron", "transferrin", "ferritin")
_THYROID_MARKERS = ("thyroid", "free t3", "tpo")

_PROHIBITED_IRON = (
    "iron deficiency diagnosis",
    "you have iron deficiency",
    "anaemia of inflammation",
    "haemochromatosis",
    "iron overload disorder",
    "you need iron",
)

_PROHIBITED_THYROID = (
    "hypothyroidism diagnosis",
    "you have hypothyroidism",
    "hashimoto's disease",
    "your immune system is attacking your thyroid",
    "your thyroid will fail",
)


def _report_meta() -> ReportMetaV1:
    return ReportMetaV1(
        signal_registry_version="reg_v1",
        signal_registry_hash_sha256="0" * 64,
        interaction_map_revision="imap_v1",
        safety_contract_version="safe_v1",
        generated_at="2026-06-26T00:00:00Z",
    )


def _payload_for_lead_signal(signal_id: str) -> NarrativePayloadV1:
    lead = ReportTopFindingV1(
        priority_rank=1,
        signal_id=signal_id,
        system="hematologic" if "iron" in signal_id else "thyroid",
        signal_state="at_risk",
        confidence=0.7,
        primary_metric="iron" if "iron" in signal_id else "free_t3",
        why_it_matters="Pattern warrants contextual review on this panel.",
    )
    rep = ReportV1(
        actions=ReportActionsV1(),
        meta=_report_meta(),
        top_findings=[lead],
        root_cause_v1=None,
        intervention_annotations_v1=None,
    )
    return build_narrative_payload_v1(analysis_id=f"p2-1-{signal_id}", report_v1=rep)


def _insight_graph_lead_only(signal_id: str) -> dict:
    return {
        "signal_results": [{"signal_id": signal_id, "signal_state": "at_risk"}],
        "primary_driver_system_id": "hematologic",
    }


def _assert_markers_present(text: str, markers: tuple[str, ...]) -> None:
    low = text.lower()
    assert any(m in low for m in markers), f"expected one of {markers} in lead narrative"


def _assert_markers_absent(text: str, markers: tuple[str, ...]) -> None:
    low = text.lower()
    assert not any(m in low for m in markers), f"did not expect {markers} in lead narrative"


def test_python_lead_hint_sets_remain_aligned() -> None:
    assert LC3_LEAD_HINTS == COMPILER_LEAD_HINTS
    for sid in _IRON_SIGNALS + _THYROID_SIGNALS:
        assert sid in LC3_LEAD_HINTS


@pytest.mark.parametrize("signal_id", _IRON_SIGNALS + _THYROID_SIGNALS)
def test_lead_signal_triggers_yaml_inclusion_flags(signal_id: str) -> None:
    payload = _payload_for_lead_signal(signal_id)
    inc_lead, _ = infer_yaml_flags_from_payload(payload)
    assert inc_lead is True


@pytest.mark.parametrize("signal_id", _IRON_SIGNALS)
def test_iron_top_finding_routes_iron_domain_prose_legacy(signal_id: str) -> None:
    rep = compile_narrative_report_v1(
        analysis_id=f"p2-1-iron-legacy-{signal_id}",
        meta={},
        insight_graph=_insight_graph_lead_only(signal_id),
        idl_bundle=None,
    )
    assert rep.lead_narrative.strip()
    _assert_markers_present(rep.lead_narrative, _IRON_MARKERS)
    _assert_markers_absent(rep.lead_narrative, _HOMOCYSTEINE_MARKERS)
    assert rep.meta.get("lead_entity_id") == "int_benchmark_blood_iron_oxygen_lead_v1"


@pytest.mark.parametrize("signal_id", _THYROID_SIGNALS)
def test_thyroid_top_finding_routes_thyroid_domain_prose_legacy(signal_id: str) -> None:
    rep = compile_narrative_report_v1(
        analysis_id=f"p2-1-thy-legacy-{signal_id}",
        meta={},
        insight_graph=_insight_graph_lead_only(signal_id),
        idl_bundle=None,
    )
    assert rep.lead_narrative.strip()
    _assert_markers_present(rep.lead_narrative, _THYROID_MARKERS)
    _assert_markers_absent(rep.lead_narrative, _HOMOCYSTEINE_MARKERS)
    assert rep.meta.get("lead_entity_id") == "int_benchmark_thyroid_hormone_antibody_lead_v1"


@pytest.mark.parametrize("signal_id", _IRON_SIGNALS)
def test_iron_top_finding_routes_iron_domain_prose_payload(signal_id: str) -> None:
    payload = _payload_for_lead_signal(signal_id)
    rep = compile_narrative_report_v1(
        analysis_id=f"p2-1-iron-payload-{signal_id}",
        meta={},
        insight_graph={"primary_driver_system_id": "hematologic"},
        idl_bundle=None,
        narrative_payload_v1=payload,
    )
    assert rep.lead_narrative.strip()
    _assert_markers_present(rep.lead_narrative, _IRON_MARKERS)
    _assert_markers_absent(rep.lead_narrative, _HOMOCYSTEINE_MARKERS)


@pytest.mark.parametrize("signal_id", _THYROID_SIGNALS)
def test_thyroid_top_finding_routes_thyroid_domain_prose_payload(signal_id: str) -> None:
    payload = _payload_for_lead_signal(signal_id)
    rep = compile_narrative_report_v1(
        analysis_id=f"p2-1-thy-payload-{signal_id}",
        meta={},
        insight_graph={"primary_driver_system_id": "thyroid"},
        idl_bundle=None,
        narrative_payload_v1=payload,
    )
    assert rep.lead_narrative.strip()
    _assert_markers_present(rep.lead_narrative, _THYROID_MARKERS)
    _assert_markers_absent(rep.lead_narrative, _HOMOCYSTEINE_MARKERS)


def test_homocysteine_lead_block_unchanged() -> None:
    ig = {
        "signal_results": [{"signal_id": "signal_homocysteine_high", "signal_state": "at_risk"}],
        "primary_driver_system_id": "vascular",
    }
    rep = compile_narrative_report_v1(analysis_id="p2-1-hcy", meta={}, insight_graph=ig, idl_bundle=None)
    assert rep.lead_narrative
    _assert_markers_present(rep.lead_narrative, _HOMOCYSTEINE_MARKERS)
    _assert_markers_absent(rep.lead_narrative, _IRON_MARKERS[:1])
    assert rep.meta.get("lead_entity_id") == "int_benchmark_one_carbon_homocysteine_macrocytosis_v1"


def test_lipid_secondary_block_unchanged() -> None:
    ig = {
        "signal_results": [{"signal_id": "signal_ldl_cholesterol_high", "signal_state": "suboptimal"}],
    }
    rep = compile_narrative_report_v1(analysis_id="p2-1-ldl", meta={}, insight_graph=ig, idl_bundle=None)
    assert rep.secondary_narratives
    low = rep.secondary_narratives.lower()
    assert "lipid" in low or "ldl" in low


def test_lead_fallback_graceful_when_no_signal_scoped_entity_matches(monkeypatch, tmp_path) -> None:
    from core.analytics import narrative_report_compiler_v1 as mod

    scoped_only = tmp_path / "entities.yaml"
    scoped_only.write_text(
        """
interpretation_entities:
  - interpretation_entity_id: int_benchmark_one_carbon_homocysteine_macrocytosis_v1
    compiler_role: benchmark_lead_domain
    phenotype_id: ph_one_carbon_homocysteine_macrocytosis_v1
    idl_internal_id: ph_one_carbon_homocysteine_macrocytosis_v1
    pathway_explainer_id: one_carbon_methylation_homocysteine_v1
    functional_interpretation_domain_id: one_carbon_methylation_functional_v1
    signal_ids:
      - signal_homocysteine_high
""",
        encoding="utf-8",
    )
    monkeypatch.setattr(mod, "_ENTITIES_PATH", scoped_only)
    ig = _insight_graph_lead_only("signal_iron_low")
    rep = compile_narrative_report_v1(analysis_id="p2-1-fallback", meta={}, insight_graph=ig, idl_bundle=None)
    assert not rep.lead_narrative.strip()
    assert "lead_domain_no_signal_scoped_entity" in rep.meta.get("skipped", [])


def test_compiler_no_raise_when_pathway_assets_missing(monkeypatch, tmp_path) -> None:
    from core.analytics import narrative_report_compiler_v1 as mod

    monkeypatch.setattr(mod, "_ENTITIES_PATH", tmp_path / "missing.yaml")
    payload = _payload_for_lead_signal("signal_iron_low")
    rep = compile_narrative_report_v1(
        analysis_id="p2-1-missing",
        meta={},
        insight_graph={},
        idl_bundle=None,
        narrative_payload_v1=payload,
    )
    assert isinstance(rep.lead_narrative, str)
    assert rep.meta.get("skipped")


def test_kb_yaml_claim_boundaries() -> None:
    blob = (
        _PATHWAYS.read_text(encoding="utf-8")
        + _FUNCTIONAL.read_text(encoding="utf-8")
        + _ENTITIES.read_text(encoding="utf-8")
    ).lower()
    for phrase in _PROHIBITED_IRON:
        assert phrase not in blob
    for phrase in _PROHIBITED_THYROID:
        assert phrase not in blob


def test_kb_pathway_entries_present_for_wave1_domains() -> None:
    pathways = yaml.safe_load(_PATHWAYS.read_text(encoding="utf-8"))
    ids = {p.get("pathway_id") for p in pathways.get("pathways", []) if isinstance(p, dict)}
    assert "blood_iron_oxygen_handling_v1" in ids
    assert "thyroid_hormone_antibody_context_v1" in ids


def test_kb_functional_domains_present_for_wave1() -> None:
    functional = yaml.safe_load(_FUNCTIONAL.read_text(encoding="utf-8"))
    ids = {d.get("domain_id") for d in functional.get("domains", []) if isinstance(d, dict)}
    assert "blood_iron_oxygen_functional_v1" in ids
    assert "thyroid_hormone_antibody_functional_v1" in ids
