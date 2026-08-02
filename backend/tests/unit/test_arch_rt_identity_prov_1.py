"""ARCH-RT-IDENTITY-PROV-1 — multi-frame preservation and provenance honesty tests."""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest
import yaml

from core.analytics.output_authority_provenance_builder_v1 import build_report_output_authority_provenance_v1
from core.analytics.report_compiler_v1 import compile_clinician_report_v1, compile_report_v1
from core.analytics.root_cause_compiler_v1 import compile_root_cause_v1
from core.analytics.signal_evaluator import SignalEvaluator
from core.analytics.signal_interaction_builder import build_signal_interactions_v1
from core.contracts.clinician_report_v1 import ClinicianReportV1
from core.contracts.report_v1 import ReportV1
from core.knowledge.launch_estate_v1 import resolve_compile_manifest_ref
from core.knowledge.provenance_status_v1 import (
    classify_package_provenance_status,
    is_beta_eligible_explicit_lineage,
)
from core.knowledge.signal_result_index_v1 import (
    group_by_signal_id,
    index_by_activation_key,
    participating_activation_keys,
)
from core.models.results import SubsystemEvidenceV1
from core.models.signal import SignalResult

REPO_ROOT = Path(__file__).resolve().parents[3]
FRONTEND_ANALYSIS_TYPES = REPO_ROOT / "frontend" / "app" / "types" / "analysis.ts"


class _MultiSignalRegistry:
    def __init__(self, signals: list[dict]) -> None:
        self._signals = [dict(s) for s in signals]

    def get_all_signals(self) -> list[dict]:
        return [dict(s) for s in self._signals]


def _synthetic_threshold_frame(
    *,
    signal_id: str,
    source_spec_id: str,
    package_id: str,
    primary_metric: str = "alt",
    threshold_value: float = 40.0,
    severity: str = "at_risk",
    provenance_status: str = "LEGACY_INFERRED",
) -> dict:
    return {
        "signal_id": signal_id,
        "activation_key": f"{signal_id}::{source_spec_id}",
        "source_spec_id": source_spec_id,
        "package_id": package_id,
        "provenance_status": provenance_status,
        "system": "liver",
        "primary_metric": primary_metric,
        "activation_logic": "deterministic_threshold",
        "thresholds": [
            {
                "threshold_id": f"{source_spec_id}_thr",
                "metric_id": primary_metric,
                "operator": ">=",
                "value": threshold_value,
                "severity": severity,
            }
        ],
        "output": {"supporting_markers": []},
    }


def _n_frames(n: int) -> list[dict]:
    return [
        {
            "signal_id": "signal_alt_high",
            "activation_key": f"signal_alt_high::inv_alt_high_frame_{chr(ord('a') + i)}",
            "source_spec_id": f"inv_alt_high_frame_{chr(ord('a') + i)}",
            "package_id": f"pkg_test_alt_{chr(ord('a') + i)}",
            "provenance_status": "LEGACY_INFERRED",
            "system": "liver",
            "signal_state": "at_risk" if i == 0 else "suboptimal",
            "confidence": max(0.4, 0.9 - 0.1 * i),
            "confidence_reasons": ["test"],
            "primary_metric": "alt",
            "supporting_markers": [],
        }
        for i in range(n)
    ]


def _two_frames() -> list[dict]:
    return _n_frames(2)


def test_index_preserves_two_activation_keys():
    idx = index_by_activation_key(_two_frames(), require_key=True)
    assert len(idx) == 2
    groups = group_by_signal_id(_two_frames())
    assert len(groups["signal_alt_high"]) == 2


def test_duplicate_activation_key_fails_closed():
    rows = _two_frames()
    rows[1]["activation_key"] = rows[0]["activation_key"]
    rows[1]["source_spec_id"] = rows[0]["source_spec_id"]
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
                "why_role": "causal",
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
                "why_role": "causal",
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
                    "why_role": "causal",
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


def test_evaluator_independent_firing_same_signal_id_frames():
    """Evaluator emits one SignalResult per registry frame when same signal_id fires."""
    frames = [
        _synthetic_threshold_frame(
            signal_id="signal_alt_high",
            source_spec_id="inv_alt_high_frame_a",
            package_id="pkg_test_alt_a",
            severity="at_risk",
        ),
        _synthetic_threshold_frame(
            signal_id="signal_alt_high",
            source_spec_id="inv_alt_high_frame_b",
            package_id="pkg_test_alt_b",
            severity="suboptimal",
        ),
    ]
    results = SignalEvaluator(_MultiSignalRegistry(frames)).evaluate_all(
        signal_biomarkers={"alt": 80.0},
        signal_derived={},
        lab_ranges={"alt": {"min": 7.0, "max": 55.0}},
    )
    assert len(results) == 2
    assert {r.signal_id for r in results} == {"signal_alt_high"}
    assert {r.activation_key for r in results} == {
        "signal_alt_high::inv_alt_high_frame_a",
        "signal_alt_high::inv_alt_high_frame_b",
    }
    assert all(isinstance(r, SignalResult) for r in results)


def test_dto_serialization_preserves_multiple_frames():
    report = compile_report_v1(
        signal_results=_two_frames(),
        interaction_summary=[],
        interventions_v1=[],
        signal_registry_version="test",
        signal_registry_hash_sha256="0" * 64,
    )
    dumped = report.model_dump()
    restored = ReportV1.model_validate(dumped)
    keys = {f.activation_key for f in restored.top_findings}
    assert "signal_alt_high::inv_alt_high_frame_a" in keys
    assert "signal_alt_high::inv_alt_high_frame_b" in keys
    wire = json.loads(report.model_dump_json())
    assert len(wire["top_findings"]) >= 2


def test_persistence_replay_round_trip_preserves_activation_identity_and_provenance():
    """DTO JSON round-trip preserves activation identity and provenance_status."""
    rows = _two_frames()
    rows[0]["provenance_status"] = "SOURCE_DOCUMENT_DERIVED"
    rows[1]["provenance_status"] = "LEGACY_INFERRED"
    signal_models = [
        SignalResult(
            signal_id=r["signal_id"],
            activation_key=r["activation_key"],
            source_spec_id=r["source_spec_id"],
            package_id=r["package_id"],
            provenance_status=r["provenance_status"],
            system=r["system"],
            signal_state=r["signal_state"],
            signal_value=80.0,
            confidence=r["confidence"],
            confidence_reasons=r["confidence_reasons"],
            primary_metric=r["primary_metric"],
            supporting_markers=r["supporting_markers"],
        )
        for r in rows
    ]
    persisted = json.loads(json.dumps([s.model_dump() for s in signal_models]))
    revived = [SignalResult.model_validate(item) for item in persisted]
    assert {(s.activation_key, s.provenance_status, s.source_spec_id) for s in revived} == {
        ("signal_alt_high::inv_alt_high_frame_a", "SOURCE_DOCUMENT_DERIVED", "inv_alt_high_frame_a"),
        ("signal_alt_high::inv_alt_high_frame_b", "LEGACY_INFERRED", "inv_alt_high_frame_b"),
    }

    report = compile_report_v1(
        signal_results=rows,
        interaction_summary=[],
        interventions_v1=[],
        signal_registry_version="test",
        signal_registry_hash_sha256="0" * 64,
    )
    payload = json.loads(report.model_dump_json())
    payload["root_cause_v1"] = {
        "version": "v1",
        "findings": [
            {
                "signal_id": "signal_alt_high",
                "activation_key": "signal_alt_high::inv_alt_high_frame_a",
                "source_spec_id": "inv_alt_high_frame_a",
                "authority_scope": "family_level",
                "why_role": "causal",
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
                "why_role": "causal",
                "primary_metric": "alt",
                "signal_state": "suboptimal",
                "signal_confidence": 0.6,
                "hypotheses": [],
            },
        ],
    }
    clinician = compile_clinician_report_v1(report_v1_payload=payload, biomarker_rows=[])
    assert clinician is not None
    wire = json.loads(clinician.model_dump_json())
    revived_clinician = ClinicianReportV1.model_validate(wire)
    assert len(revived_clinician.sections.root_causes) == 2
    assert {f.activation_key for f in revived_clinician.sections.root_causes} == {
        "signal_alt_high::inv_alt_high_frame_a",
        "signal_alt_high::inv_alt_high_frame_b",
    }
    assert revived_clinician.sections.root_cause is None


def test_deterministic_ordering_across_repeated_executions():
    rows = list(reversed(_n_frames(3)))
    # group_by_signal_id: stable activation_key ascending within signal_id.
    grouped = group_by_signal_id(rows)["signal_alt_high"]
    group_keys = [r["activation_key"] for r in grouped]
    assert group_keys == sorted(group_keys)

    # index_by_activation_key: insertion-stable and identical across repeated builds.
    idx_runs = [list(index_by_activation_key(rows, require_key=True).keys()) for _ in range(5)]
    assert all(run == idx_runs[0] for run in idx_runs)
    assert set(idx_runs[0]) == set(group_keys)

    # Report compiler ranking is a named presentation policy; order must be stable across runs.
    report_key_runs = []
    for _ in range(5):
        report = compile_report_v1(
            signal_results=rows,
            interaction_summary=[],
            interventions_v1=[],
            signal_registry_version="test",
            signal_registry_hash_sha256="0" * 64,
        )
        report_key_runs.append(
            [f.activation_key for f in report.top_findings if f.signal_id == "signal_alt_high"]
        )
    assert all(run == report_key_runs[0] for run in report_key_runs)
    assert set(report_key_runs[0]) == {
        "signal_alt_high::inv_alt_high_frame_a",
        "signal_alt_high::inv_alt_high_frame_b",
        "signal_alt_high::inv_alt_high_frame_c",
    }


def test_three_or_more_simultaneous_frames():
    rows = _n_frames(3)
    assert len(index_by_activation_key(rows, require_key=True)) == 3
    report = compile_report_v1(
        signal_results=rows,
        interaction_summary=[],
        interventions_v1=[],
        signal_registry_version="test",
        signal_registry_hash_sha256="0" * 64,
    )
    keys = {f.activation_key for f in report.top_findings}
    assert "signal_alt_high::inv_alt_high_frame_a" in keys
    assert "signal_alt_high::inv_alt_high_frame_b" in keys
    assert "signal_alt_high::inv_alt_high_frame_c" in keys
    map_payload = {
        "map_version": "test",
        "nodes": [{"signal_id": "signal_alt_high"}],
        "edges": [],
    }
    out = build_signal_interactions_v1(rows, map_payload=map_payload)
    part = set(out.get("participating_activation_keys") or [])
    assert len(part) >= 3
    assert part == {
        "signal_alt_high::inv_alt_high_frame_a",
        "signal_alt_high::inv_alt_high_frame_b",
        "signal_alt_high::inv_alt_high_frame_c",
    }


def test_canonical_compile_manifest_ref_resolution():
    ref = "knowledge_bus/compiled/manifests/arch_rt4_vitamin_d_hypothesis.yaml"
    resolved = resolve_compile_manifest_ref(ref)
    assert resolved is not None
    assert resolved.is_file()
    assert resolved.name == "arch_rt4_vitamin_d_hypothesis.yaml"
    # Bare filename form also resolves under manifests/
    bare = resolve_compile_manifest_ref("arch_rt4_vitamin_d_hypothesis.yaml")
    assert bare is not None and bare.is_file()


def test_internal_compile_manifest_paths_do_not_leak_into_consumer_dtos():
    """Consumer models expose compile_manifest_ref, not compile_manifest_path."""
    fields = SubsystemEvidenceV1.model_fields
    assert "compile_manifest_ref" in fields
    assert "compile_manifest_path" not in fields
    # Frontend contract mirrors ref naming (no path leak).
    fe = FRONTEND_ANALYSIS_TYPES.read_text(encoding="utf-8")
    assert "compile_manifest_ref" in fe
    assert "compile_manifest_path" not in fe
    # Estate index may keep internal path; that is not a consumer DTO.
    estate = yaml.safe_load(
        (REPO_ROOT / "knowledge_bus" / "compiled" / "estate_index_v1.yaml").read_text(encoding="utf-8")
    )
    assert "compile_manifest_path" in json.dumps(estate)


def test_blocked_launch_critical_reported_without_blocking_unrelated_legacy():
    """Gate cohort is kb47-prefixed; blocked lineage is warning, not estate-wide fail."""
    from scripts.validate_identity_provenance_gate import (  # type: ignore
        LAUNCH_CRITICAL_PACKAGE_PREFIXES,
        _active_kb47_packages,
        main as gate_main,
    )

    assert LAUNCH_CRITICAL_PACKAGE_PREFIXES == ("pkg_kb47_",)
    cohort = _active_kb47_packages()
    assert cohort
    assert all(p.name.startswith("pkg_kb47_") for p in cohort)
    # Unrelated legacy packages exist outside cohort
    packages_root = REPO_ROOT / "knowledge_bus" / "packages"
    legacy = [p for p in packages_root.iterdir() if p.is_dir() and not p.name.startswith("pkg_kb47_")]
    assert legacy, "expected non-kb47 packages to prove cohort bounding"
    exit_code = gate_main()
    assert exit_code == 0
    inventory = (REPO_ROOT / "docs" / "architecture" / "ARCH-RT-IDENTITY-PROV-1_launch_critical_provenance_inventory.md").read_text(
        encoding="utf-8"
    )
    assert "BLOCKED" in inventory or "beta-ineligible" in inventory.lower() or "LEGACY_INFERRED" in inventory
    for pkg in legacy[:5]:
        # Inventory may mention packages only in cohort rows — legacy ids must not appear as gate errors.
        # Soft check: non-kb47 package_id not required in inventory table.
        assert not re.search(rf"\|\s*{re.escape(pkg.name)}\s*\|", inventory) or pkg.name.startswith("pkg_kb47_")


def test_package_manifest_schema_compatibility_and_naming_drift_regression():
    schema = yaml.safe_load(
        (REPO_ROOT / "knowledge_bus" / "schema" / "package_manifest_schema.yaml").read_text(encoding="utf-8")
    )
    assert schema["schema_version"] == "1.1.0"
    optional = schema["optional_fields"]
    assert "source_spec_id" in optional
    assert "source_document" in optional
    assert "activation_key" in optional
    # Historical required fields unchanged — packages without optional provenance remain valid shape.
    required = set(schema["required_fields"])
    assert required == {"package_id", "package_version", "research_brief", "signal_library"}
    # Naming drift: consumer DTO uses compile_manifest_ref exclusively.
    assert "compile_manifest_path" not in SubsystemEvidenceV1.model_fields
    assert "compile_manifest_ref" in SubsystemEvidenceV1.model_fields


def test_provenance_status_matrix_explicit_derived_inferred_unresolved_blocked():
    explicit = classify_package_provenance_status(
        manifest={"source_spec_id": "inv_alt_high_hepatocellular_injury_v1"}
    )
    assert explicit == "EXPLICIT_SPEC"
    assert is_beta_eligible_explicit_lineage(explicit)

    derived = classify_package_provenance_status(
        manifest={
            "source_spec_id": "inv_not_a_real_spec_zzzz",
            "source_document": "knowledge_bus/research/investigation_specs/inv_alt_high_hepatocellular_injury_v1.yaml",
        }
    )
    assert derived == "SOURCE_DOCUMENT_DERIVED"
    assert derived != "EXPLICIT_SPEC"

    inferred = classify_package_provenance_status(
        manifest={"source_spec_id": "inv_not_a_real_spec_zzzz"}
    )
    assert inferred == "LEGACY_INFERRED"

    unresolved = classify_package_provenance_status(manifest={})
    assert unresolved == "UNRESOLVED"
    assert not is_beta_eligible_explicit_lineage(unresolved)

    blocked = classify_package_provenance_status(
        manifest={
            "source_document": "knowledge_bus/research/investigation_specs/multi_llm_research/Batch_2_Pass_3.json",
        }
    )
    assert blocked == "BLOCKED"


def test_clinician_report_multi_finding_serialization_backend_and_frontend_contracts():
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
            },
            {
                "priority_rank": 2,
                "signal_id": "signal_alt_high",
                "activation_key": "signal_alt_high::inv_alt_high_frame_b",
                "system": "liver",
                "signal_state": "suboptimal",
                "confidence": 0.6,
                "confidence_reasons": [],
                "primary_metric": "alt",
                "supporting_markers": [],
                "why_it_matters": "test",
            },
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
                    "why_role": "causal",
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
                    "why_role": "causal",
                    "primary_metric": "alt",
                    "signal_state": "suboptimal",
                    "signal_confidence": 0.6,
                    "hypotheses": [],
                },
            ],
        },
    }
    clinician = compile_clinician_report_v1(report_v1_payload=payload, biomarker_rows=[])
    assert clinician is not None
    dumped = json.loads(clinician.model_dump_json())
    sections = dumped["sections"]
    assert len(sections["root_causes"]) == 2
    assert sections["root_cause"] is None
    for finding in sections["root_causes"]:
        assert finding["activation_key"]
        assert finding["source_spec_id"]

    fe = FRONTEND_ANALYSIS_TYPES.read_text(encoding="utf-8")
    assert "export interface ClinicianRootCauseFindingV1" in fe
    assert "root_causes?: ClinicianRootCauseFindingV1[]" in fe
    assert "activation_key?: string" in fe
    # Additive list + legacy singleton documented in frontend types
    assert re.search(r"root_cause:\s*ClinicianRootCauseFindingV1\s*\|\s*null", fe)


def test_source_spec_id_resolves_to_authoritative_investigation_spec():
    spec_id = "inv_alt_high_hepatocellular_injury_v1"
    path = REPO_ROOT / "knowledge_bus" / "research" / "investigation_specs" / f"{spec_id}.yaml"
    assert path.is_file()
    status = classify_package_provenance_status(manifest={"source_spec_id": spec_id})
    assert status == "EXPLICIT_SPEC"


def test_participating_activation_keys_helper_preserves_all_frames():
    keys = participating_activation_keys(
        _n_frames(3),
        valid_states={"at_risk", "suboptimal"},
    )
    assert len(keys) == 3
