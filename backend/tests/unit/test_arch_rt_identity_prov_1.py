"""ARCH-RT-IDENTITY-PROV-1 — multi-frame preservation and provenance honesty tests.

ARCH-CONV-I-ALT-IDPROV-1: multi-frame mechanics fixtures use a synthetic non-pilot
signal identity so Package A/B pilot-cohort migrations cannot silently break the
contract via real signal_id collision (e.g. former signal_alt_high::inv_alt_high_frame_*).
"""

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
from core.knowledge.why_authority_v1 import is_pilot_signal_id
from core.models.results import SubsystemEvidenceV1
from core.models.signal import SignalResult

REPO_ROOT = Path(__file__).resolve().parents[3]
FRONTEND_ANALYSIS_TYPES = REPO_ROOT / "frontend" / "app" / "types" / "analysis.ts"

# Option A (ARCH-CONV-I-ALT-IDPROV-1): test-only synthetic identity, never piloted.
SYNTHETIC_MULTIFRAME_SIGNAL_ID = "signal_test_synthetic_multiframe_v1"
SYNTHETIC_FRAME_SPEC_PREFIX = "inv_test_synthetic_multiframe_frame_"


def _require_synthetic_non_pilot() -> None:
    """Migration guard: fail loudly if this fixture identity ever becomes piloted."""
    assert not is_pilot_signal_id(SYNTHETIC_MULTIFRAME_SIGNAL_ID), (
        f"{SYNTHETIC_MULTIFRAME_SIGNAL_ID} is now in _PILOT_SIGNAL_IDS; "
        "ARCH-CONV-I-ALT-IDPROV-1 multi-frame fixtures require review before continuing"
    )


def _frame_key(index: int) -> str:
    letter = chr(ord("a") + index)
    return f"{SYNTHETIC_MULTIFRAME_SIGNAL_ID}::{SYNTHETIC_FRAME_SPEC_PREFIX}{letter}"


def _frame_spec(index: int) -> str:
    letter = chr(ord("a") + index)
    return f"{SYNTHETIC_FRAME_SPEC_PREFIX}{letter}"


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
    _require_synthetic_non_pilot()
    return [
        {
            "signal_id": SYNTHETIC_MULTIFRAME_SIGNAL_ID,
            "activation_key": _frame_key(i),
            "source_spec_id": _frame_spec(i),
            "package_id": f"pkg_test_synthetic_mf_{chr(ord('a') + i)}",
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
    assert len(groups[SYNTHETIC_MULTIFRAME_SIGNAL_ID]) == 2


def test_duplicate_activation_key_fails_closed():
    rows = _two_frames()
    rows[1]["activation_key"] = rows[0]["activation_key"]
    rows[1]["source_spec_id"] = rows[0]["source_spec_id"]
    with pytest.raises(ValueError, match="Duplicate activation_key"):
        index_by_activation_key(rows, require_key=True)


def test_interaction_builder_retains_participating_activation_keys():
    map_payload = {
        "map_version": "test",
        "nodes": [{"signal_id": SYNTHETIC_MULTIFRAME_SIGNAL_ID}],
        "edges": [],
    }
    out = build_signal_interactions_v1(_two_frames(), map_payload=map_payload)
    keys = out.get("participating_activation_keys") or []
    assert _frame_key(0) in keys
    assert _frame_key(1) in keys
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
    assert _frame_key(0) in keys
    assert _frame_key(1) in keys
    bundle = build_report_output_authority_provenance_v1(
        signal_results=_two_frames(),
        report=report,
        root_cause=report.root_cause_v1,
    )
    element_ids = [e.output_element_id for e in bundle.governed_elements]
    assert any(_frame_spec(0) in eid for eid in element_ids)
    assert any(_frame_spec(1) in eid for eid in element_ids)


def test_clinician_report_retains_multi_findings_without_silent_singleton():
    report = compile_report_v1(
        signal_results=_two_frames(),
        interaction_summary=[],
        interventions_v1=[],
        signal_registry_version="test",
        signal_registry_hash_sha256="0" * 64,
    )
    payload = report.model_dump()
    payload["root_cause_v1"] = {
        "version": "v1",
        "findings": [
            {
                "signal_id": SYNTHETIC_MULTIFRAME_SIGNAL_ID,
                "activation_key": _frame_key(0),
                "source_spec_id": _frame_spec(0),
                "authority_scope": "family_level",
                "why_role": "causal",
                "primary_metric": "alt",
                "signal_state": "at_risk",
                "signal_confidence": 0.8,
                "hypotheses": [],
            },
            {
                "signal_id": SYNTHETIC_MULTIFRAME_SIGNAL_ID,
                "activation_key": _frame_key(1),
                "source_spec_id": _frame_spec(1),
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
                "signal_id": SYNTHETIC_MULTIFRAME_SIGNAL_ID,
                "activation_key": _frame_key(0),
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
                    "signal_id": SYNTHETIC_MULTIFRAME_SIGNAL_ID,
                    "activation_key": _frame_key(0),
                    "source_spec_id": _frame_spec(0),
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
    assert clinician.sections.root_cause.activation_key == _frame_key(0)


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
        (REPO_ROOT / "knowledge_bus" / "schema" / "package_manifest_schema.yaml").read_text(
            encoding="utf-8"
        )
    )
    assert schema["schema_version"] == "1.1.0"
    assert "source_spec_id" in schema["optional_fields"]


def test_root_cause_compiler_emits_finding_per_frame_for_shared_signal_id(monkeypatch):
    """Per-frame emission using synthetic non-pilot target (not dynamic _ROOT_CAUSE_TARGETS[0])."""
    from core.analytics import root_cause_compiler_v1 as mod

    _require_synthetic_non_pilot()
    signal_id = SYNTHETIC_MULTIFRAME_SIGNAL_ID

    def _synthetic_hypotheses_loader() -> dict:
        return {
            "hypotheses": [
                {
                    "hypothesis_id": "hyp_test_synthetic_multiframe_v1",
                    "title": "Synthetic multi-frame hypothesis",
                    "summary_template": "Test-only hypothesis for frame preservation.",
                    "safety_class": "informational",
                    "evidence_for_rules": [],
                    "evidence_against_rules": [],
                    "missing_data_markers": [],
                    "confirmatory_tests": [],
                }
            ]
        }

    monkeypatch.setattr(
        mod,
        "_ROOT_CAUSE_TARGETS",
        [(signal_id, _synthetic_hypotheses_loader)],
    )
    rows = [
        {
            "signal_id": signal_id,
            "activation_key": _frame_key(0),
            "source_spec_id": _frame_spec(0),
            "package_id": "pkg_test_synthetic_mf_a",
            "system": "test",
            "signal_state": "at_risk",
            "confidence": 0.9,
            "primary_metric": "x",
            "supporting_markers": [],
        },
        {
            "signal_id": signal_id,
            "activation_key": _frame_key(1),
            "source_spec_id": _frame_spec(1),
            "package_id": "pkg_test_synthetic_mf_b",
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
    assert _frame_key(0) in keys
    assert _frame_key(1) in keys


def test_evaluator_independent_firing_same_signal_id_frames():
    """Evaluator emits one SignalResult per registry frame when same signal_id fires."""
    _require_synthetic_non_pilot()
    frames = [
        _synthetic_threshold_frame(
            signal_id=SYNTHETIC_MULTIFRAME_SIGNAL_ID,
            source_spec_id=_frame_spec(0),
            package_id="pkg_test_synthetic_mf_a",
            severity="at_risk",
        ),
        _synthetic_threshold_frame(
            signal_id=SYNTHETIC_MULTIFRAME_SIGNAL_ID,
            source_spec_id=_frame_spec(1),
            package_id="pkg_test_synthetic_mf_b",
            severity="suboptimal",
        ),
    ]
    results = SignalEvaluator(_MultiSignalRegistry(frames)).evaluate_all(
        signal_biomarkers={"alt": 80.0},
        signal_derived={},
        lab_ranges={"alt": {"min": 7.0, "max": 55.0}},
    )
    assert len(results) == 2
    assert {r.signal_id for r in results} == {SYNTHETIC_MULTIFRAME_SIGNAL_ID}
    assert {r.activation_key for r in results} == {_frame_key(0), _frame_key(1)}
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
    assert _frame_key(0) in keys
    assert _frame_key(1) in keys
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
        (_frame_key(0), "SOURCE_DOCUMENT_DERIVED", _frame_spec(0)),
        (_frame_key(1), "LEGACY_INFERRED", _frame_spec(1)),
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
                "signal_id": SYNTHETIC_MULTIFRAME_SIGNAL_ID,
                "activation_key": _frame_key(0),
                "source_spec_id": _frame_spec(0),
                "authority_scope": "family_level",
                "why_role": "causal",
                "primary_metric": "alt",
                "signal_state": "at_risk",
                "signal_confidence": 0.8,
                "hypotheses": [],
            },
            {
                "signal_id": SYNTHETIC_MULTIFRAME_SIGNAL_ID,
                "activation_key": _frame_key(1),
                "source_spec_id": _frame_spec(1),
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
        _frame_key(0),
        _frame_key(1),
    }
    assert revived_clinician.sections.root_cause is None


def test_deterministic_ordering_across_repeated_executions():
    rows = list(reversed(_n_frames(3)))
    grouped = group_by_signal_id(rows)[SYNTHETIC_MULTIFRAME_SIGNAL_ID]
    group_keys = [r["activation_key"] for r in grouped]
    assert group_keys == sorted(group_keys)

    idx_runs = [list(index_by_activation_key(rows, require_key=True).keys()) for _ in range(5)]
    assert all(run == idx_runs[0] for run in idx_runs)
    assert set(idx_runs[0]) == set(group_keys)

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
            [
                f.activation_key
                for f in report.top_findings
                if f.signal_id == SYNTHETIC_MULTIFRAME_SIGNAL_ID
            ]
        )
    assert all(run == report_key_runs[0] for run in report_key_runs)
    assert set(report_key_runs[0]) == {_frame_key(0), _frame_key(1), _frame_key(2)}


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
    assert _frame_key(0) in keys
    assert _frame_key(1) in keys
    assert _frame_key(2) in keys
    map_payload = {
        "map_version": "test",
        "nodes": [{"signal_id": SYNTHETIC_MULTIFRAME_SIGNAL_ID}],
        "edges": [],
    }
    out = build_signal_interactions_v1(rows, map_payload=map_payload)
    part = set(out.get("participating_activation_keys") or [])
    assert len(part) >= 3
    assert part == {_frame_key(0), _frame_key(1), _frame_key(2)}


def test_canonical_compile_manifest_ref_resolution():
    ref = "knowledge_bus/compiled/manifests/arch_rt4_vitamin_d_hypothesis.yaml"
    resolved = resolve_compile_manifest_ref(ref)
    assert resolved is not None
    assert resolved.is_file()
    assert resolved.name == "arch_rt4_vitamin_d_hypothesis.yaml"
    bare = resolve_compile_manifest_ref("arch_rt4_vitamin_d_hypothesis.yaml")
    assert bare is not None and bare.is_file()


def test_internal_compile_manifest_paths_do_not_leak_into_consumer_dtos():
    """Consumer models expose compile_manifest_ref, not compile_manifest_path."""
    fields = SubsystemEvidenceV1.model_fields
    assert "compile_manifest_ref" in fields
    assert "compile_manifest_path" not in fields
    fe = FRONTEND_ANALYSIS_TYPES.read_text(encoding="utf-8")
    assert "compile_manifest_ref" in fe
    assert "compile_manifest_path" not in fe
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
    packages_root = REPO_ROOT / "knowledge_bus" / "packages"
    legacy = [p for p in packages_root.iterdir() if p.is_dir() and not p.name.startswith("pkg_kb47_")]
    assert legacy, "expected non-kb47 packages to prove cohort bounding"
    exit_code = gate_main()
    assert exit_code == 0
    inventory = (
        REPO_ROOT
        / "docs"
        / "architecture"
        / "ARCH-RT-IDENTITY-PROV-1_launch_critical_provenance_inventory.md"
    ).read_text(encoding="utf-8")
    assert "BLOCKED" in inventory or "beta-ineligible" in inventory.lower() or "LEGACY_INFERRED" in inventory
    for pkg in legacy[:5]:
        assert not re.search(rf"\|\s*{re.escape(pkg.name)}\s*\|", inventory) or pkg.name.startswith(
            "pkg_kb47_"
        )


def test_package_manifest_schema_compatibility_and_naming_drift_regression():
    schema = yaml.safe_load(
        (REPO_ROOT / "knowledge_bus" / "schema" / "package_manifest_schema.yaml").read_text(
            encoding="utf-8"
        )
    )
    assert schema["schema_version"] == "1.1.0"
    optional = schema["optional_fields"]
    assert "source_spec_id" in optional
    assert "source_document" in optional
    assert "activation_key" in optional
    required = set(schema["required_fields"])
    assert required == {"package_id", "package_version", "research_brief", "signal_library"}
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
                "signal_id": SYNTHETIC_MULTIFRAME_SIGNAL_ID,
                "activation_key": _frame_key(0),
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
                "signal_id": SYNTHETIC_MULTIFRAME_SIGNAL_ID,
                "activation_key": _frame_key(1),
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
                    "signal_id": SYNTHETIC_MULTIFRAME_SIGNAL_ID,
                    "activation_key": _frame_key(0),
                    "source_spec_id": _frame_spec(0),
                    "authority_scope": "family_level",
                    "why_role": "causal",
                    "primary_metric": "alt",
                    "signal_state": "at_risk",
                    "signal_confidence": 0.8,
                    "hypotheses": [],
                },
                {
                    "signal_id": SYNTHETIC_MULTIFRAME_SIGNAL_ID,
                    "activation_key": _frame_key(1),
                    "source_spec_id": _frame_spec(1),
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
