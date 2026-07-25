"""ARCH-RT-IDENTITY-PROV-1 — multi-frame preservation and provenance honesty tests."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from core.analytics.output_authority_provenance_builder_v1 import build_report_output_authority_provenance_v1
from core.analytics.report_compiler_v1 import compile_clinician_report_v1, compile_report_v1
from core.analytics.root_cause_compiler_v1 import compile_root_cause_v1
from core.analytics.signal_interaction_builder import build_signal_interactions_v1
from core.contracts.report_v1 import ReportV1
from core.knowledge.provenance_status_v1 import classify_package_provenance_status
from core.knowledge.signal_result_index_v1 import (
    group_by_signal_id,
    index_by_activation_key,
    participating_activation_keys,
)


def _two_frames() -> list[dict]:
    return [
        {
            "signal_id": "signal_alt_high",
            "activation_key": "signal_alt_high::inv_alt_high_frame_a",
            "source_spec_id": "inv_alt_high_frame_a",
            "package_id": "pkg_test_alt_a",
            "provenance_status": "LEGACY_INFERRED",
            "system": "liver",
            "signal_state": "at_risk",
            "confidence": 0.8,
            "confidence_reasons": ["test"],
            "primary_metric": "alt",
            "supporting_markers": [],
        },
        {
            "signal_id": "signal_alt_high",
            "activation_key": "signal_alt_high::inv_alt_high_frame_b",
            "source_spec_id": "inv_alt_high_frame_b",
            "package_id": "pkg_test_alt_b",
            "provenance_status": "LEGACY_INFERRED",
            "system": "liver",
            "signal_state": "suboptimal",
            "confidence": 0.6,
            "confidence_reasons": ["test"],
            "primary_metric": "alt",
            "supporting_markers": [],
        },
    ]


def test_index_preserves_two_activation_keys():
    idx = index_by_activation_key(_two_frames(), require_key=True)
    assert len(idx) == 2
    groups = group_by_signal_id(_two_frames())
    assert len(groups["signal_alt_high"]) == 2


def test_duplicate_activation_key_fails_closed():
    rows = _two_frames()
    rows[1]["activation_key"] = rows[0]["activation_key"]
    with pytest.raises(ValueError, match="Duplicate activation_key"):
        index_by_activation_key(rows, require_key=True)


def test_interaction_builder_retains_participating_activation_keys():
    # Minimal map with signal_alt_high node so family presence is exercised.
    map_payload = {
        "map_version": "test",
        "nodes": [{"signal_id": "signal_alt_high"}],
        "edges": [],
    }
    out = build_signal_interactions_v1(_two_frames(), map_payload=map_payload)
    keys = out.get("participating_activation_keys") or []
    assert "signal_alt_high::inv_alt_high_frame_a" in keys
    assert "signal_alt_high::inv_alt_high_frame_b" in keys
    assert out["interaction_graph"].get("aggregation_scope") == "signal_family"


def test_report_and_output_authority_preserve_both_frames():
    report = compile_report_v1(
        signal_results=_two_frames(),
        interaction_summary=[],
        interventions_v1=[],
        signal_registry_version="test",
        signal_registry_hash_sha256="0" * 64,
    )
    keys = {f.activation_key for f in report.top_findings}
    assert "signal_alt_high::inv_alt_high_frame_a" in keys
    assert "signal_alt_high::inv_alt_high_frame_b" in keys
    bundle = build_report_output_authority_provenance_v1(
        signal_results=_two_frames(),
        report=report,
        root_cause=report.root_cause_v1,
    )
    element_ids = [e.output_element_id for e in bundle.governed_elements]
    assert any("inv_alt_high_frame_a" in eid for eid in element_ids)
    assert any("inv_alt_high_frame_b" in eid for eid in element_ids)


def test_clinician_report_retains_multi_findings_without_silent_singleton():
    # Synthesize multi finding root_cause_v1 payload
    report = compile_report_v1(
        signal_results=_two_frames(),
        interaction_summary=[],
        interventions_v1=[],
        signal_registry_version="test",
        signal_registry_hash_sha256="0" * 64,
    )
    payload = report.model_dump()
    # Force two root findings with distinct activation keys
    payload["root_cause_v1"] = {
        "version": "v1",
        "findings": [
            {
                "signal_id": "signal_alt_high",
                "activation_key": "signal_alt_high::inv_alt_high_frame_a",
                "source_spec_id": "inv_alt_high_frame_a",
                "authority_scope": "family_level",
                "primary_metric": "alt",
                "signal_state": "at_risk",
                "signal_confidence": 0.8,
                "hypotheses": [],
            },
            {
                "signal_id": "signal_alt_high",
                "activation_key": "signal_alt_high::inv_alt_high_frame_b",
                "source_spec_id": "inv_alt_high_frame_b",
                "authority_scope": "family_level",
                "primary_metric": "alt",
                "signal_state": "suboptimal",
                "signal_confidence": 0.6,
                "hypotheses": [],
            },
        ],
    }
    clinician = compile_clinician_report_v1(report_v1_payload=payload, biomarker_rows=[])
    assert clinician is not None
    assert len(clinician.sections.root_causes) == 2
    assert clinician.sections.root_cause is None  # no silent first pick


def test_clinician_report_legacy_singleton_when_one_finding():
    payload = {
        "top_findings": [
            {
                "priority_rank": 1,
                "signal_id": "signal_alt_high",
                "activation_key": "signal_alt_high::inv_alt_high_frame_a",
                "system": "liver",
                "signal_state": "at_risk",
                "confidence": 0.8,
                "confidence_reasons": [],
                "primary_metric": "alt",
                "supporting_markers": [],
                "why_it_matters": "test",
            }
        ],
        "top_chains": [],
        "meta": {},
        "root_cause_v1": {
            "version": "v1",
            "findings": [
                {
                    "signal_id": "signal_alt_high",
                    "activation_key": "signal_alt_high::inv_alt_high_frame_a",
                    "source_spec_id": "inv_alt_high_frame_a",
                    "authority_scope": "family_level",
                    "primary_metric": "alt",
                    "signal_state": "at_risk",
                    "signal_confidence": 0.8,
                    "hypotheses": [],
                }
            ],
        },
    }
    clinician = compile_clinician_report_v1(report_v1_payload=payload, biomarker_rows=[])
    assert clinician is not None
    assert len(clinician.sections.root_causes) == 1
    assert clinician.sections.root_cause is not None
    assert clinician.sections.root_cause.activation_key == "signal_alt_high::inv_alt_high_frame_a"


def test_provenance_batch_json_not_explicit():
    status = classify_package_provenance_status(
        manifest={
            "source_document": "knowledge_bus/research/investigation_specs/multi_llm_research/Batch_2_Pass_3.json",
            "source_spec_id": "inv_dhea_high_androgen_excess_context",
        }
    )
    assert status != "EXPLICIT_SPEC"
    assert status in {"SOURCE_DOCUMENT_DERIVED", "BLOCKED", "LEGACY_INFERRED"}


def test_package_manifest_schema_declares_source_spec_id():
    schema = yaml.safe_load(
        Path("knowledge_bus/schema/package_manifest_schema.yaml").read_text(encoding="utf-8")
    )
    assert schema["schema_version"] == "1.1.0"
    assert "source_spec_id" in schema["optional_fields"]


def test_root_cause_compiler_emits_finding_per_frame_for_shared_signal_id(monkeypatch):
    # Use a registered target if available; otherwise skip.
    from core.analytics import root_cause_compiler_v1 as mod

    targets = list(mod._ROOT_CAUSE_TARGETS)
    if not targets:
        pytest.skip("no root cause targets")
    signal_id, _loader = targets[0]
    rows = [
        {
            "signal_id": signal_id,
            "activation_key": f"{signal_id}::frame_a",
            "source_spec_id": "frame_a",
            "package_id": "pkg_a",
            "system": "test",
            "signal_state": "at_risk",
            "confidence": 0.9,
            "primary_metric": "x",
            "supporting_markers": [],
        },
        {
            "signal_id": signal_id,
            "activation_key": f"{signal_id}::frame_b",
            "source_spec_id": "frame_b",
            "package_id": "pkg_b",
            "system": "test",
            "signal_state": "suboptimal",
            "confidence": 0.7,
            "primary_metric": "x",
            "supporting_markers": [],
        },
    ]
    result = compile_root_cause_v1(signal_results=rows)
    assert result is not None
    keyed = [f for f in result.findings if f.signal_id == signal_id]
    assert len(keyed) >= 2
    keys = {f.activation_key for f in keyed}
    assert f"{signal_id}::frame_a" in keys
    assert f"{signal_id}::frame_b" in keys
