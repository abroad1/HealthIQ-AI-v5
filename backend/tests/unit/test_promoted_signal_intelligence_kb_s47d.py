"""KB-S47d — promoted signal intelligence contract, translation, loader."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest
import yaml

from core.knowledge.investigation_spec_to_promoted_signal import (
    translate_investigation_spec_v3_to_promoted_signals,
)
from core.knowledge.load_promoted_signal_intelligence import (
    load_promoted_signal_intelligence_for_package,
)

REPO_ROOT = Path(__file__).resolve().parents[3]
VALIDATE_PROMOTED = REPO_ROOT / "backend" / "scripts" / "validate_promoted_signal_intelligence.py"
VALIDATE_PACKAGE = REPO_ROOT / "backend" / "scripts" / "validate_knowledge_package.py"
PROMOTED_SCHEMA = REPO_ROOT / "knowledge_bus" / "schema" / "promoted_signal_intelligence_schema_v1.yaml"
FIXTURE_VALID = REPO_ROOT / "backend" / "tests" / "fixtures" / "pkg_promoted_signal_v1_valid"


def _minimal_investigation_spec_v3() -> dict:
    return {
        "investigation_spec_contract_version": "3.0.0",
        "spec_id": "inv_test_signal_high",
        "signal_id": "signal_test_metric_high",
        "research_domain": "metabolic",
        "primary_marker": {
            "biomarker_id": "test_metric",
            "rationale": "Primary test marker with sufficient rationale length.",
            "signal_system": "metabolic",
        },
        "trigger_direction": "high",
        "activation": {
            "activation_logic": "lab_range_exceeded",
            "activation_config": {
                "enable_upper_bound": True,
                "upper_bound_state": "suboptimal",
                "enable_lower_bound": False,
                "lower_bound_state": "suboptimal",
            },
        },
        "states": {"baseline_state": "suboptimal", "escalation_state": "at_risk"},
        "supporting_markers": [
            {
                "biomarker_id": "ctx_a",
                "expected_direction": "high",
                "role": "corroborator",
                "relationship_kind": "corroboration",
                "availability": "common",
                "rationale": "Corroborating context marker for this test signal only.",
            },
            {
                "biomarker_id": "ctx_b",
                "expected_direction": "high",
                "role": "differential_marker",
                "relationship_kind": "differential",
                "availability": "common",
                "rationale": "Differential marker to satisfy promoted contract differential rule.",
            },
        ],
        "hypotheses": [
            {
                "hypothesis_id": "hyp_primary_mechanism",
                "rank": 1,
                "physiological_claim": "First ranked mechanism claim for test purposes.",
                "evidence_strength": "strong",
                "caveats": ["Test caveat one."],
                "missing_data": {"policy": "If ctx_a missing, treat as unknown."},
                "supporting_marker_refs": ["ctx_a"],
                "contradiction_markers": [
                    {
                        "contradiction_id": "ctr_ctx_a_normal",
                        "marker_reference": "ctx_a",
                        "contradiction_rationale": "Normal ctx_a contradicts sustained elevation pattern here.",
                        "contradiction_strength": "moderate",
                    }
                ],
            },
            {
                "hypothesis_id": "hyp_alternate",
                "rank": 2,
                "physiological_claim": "Alternate explanation for testing translation rollup.",
                "evidence_strength": "moderate",
                "caveats": ["Test caveat two."],
                "missing_data": {"policy": "Second policy string for merge sort."},
                "supporting_marker_refs": ["ctx_b"],
                "contradiction_markers": [],
            },
        ],
        "hypothesis_ranking": {
            "ordered_hypothesis_ids": ["hyp_primary_mechanism", "hyp_alternate"],
        },
        "confirmatory_tests": [
            {
                "test_id": "ct_repeat_labs",
                "rationale": "Repeat testing confirms persistence beyond acute fluctuation.",
            }
        ],
        "override_rules": [
            {
                "rule_id": "or_test_escalation",
                "resulting_state": "at_risk",
                "description": "Escalate when test metric crosses numeric governance threshold.",
                "conditions": [
                    {
                        "metric_id": "test_metric",
                        "operator": ">=",
                        "condition_type": "all_of",
                        "comparator_type": "numeric_value",
                        "numeric_value": 99.0,
                    }
                ],
                "source_refs": ["source_test_fixture"],
            }
        ],
        "evidence": {
            "evidence_strength": "strong",
            "sources": [
                {
                    "source_id": "source_test_fixture",
                    "paper_title": "Fixture study for promoted signal translation",
                    "journal": "Test",
                    "year": 2024,
                }
            ],
            "physiological_claim": "Elevated test_metric indicates structured fixture risk.",
            "threshold_notes": "Fixture threshold notes for validator length.",
        },
        "narrative": {
            "mechanism": "Narrative prose must not appear in promoted output translation.",
            "biological_pathway": "This block is intentionally excluded from promoted signal YAML.",
            "interpretation": "Consumers must load hypotheses from adjacent assets by signal_id.",
            "implications": "ADR-008 defines boundary between signal intelligence and explanation.",
            "supporting_marker_roles": "Promoted contract uses structured supporting_marker objects only.",
        },
    }


def test_translate_investigation_v3_then_validate_passes(tmp_path: Path) -> None:
    inv = _minimal_investigation_spec_v3()
    promoted = translate_investigation_spec_v3_to_promoted_signals(
        inv, package_id="pkg_fixture_promoted_signal_v1"
    )
    assert "hypotheses" not in promoted
    assert promoted["signals"][0]["signal_id"] == "signal_test_metric_high"
    assert len(promoted["signals"][0]["contradiction_markers"]) == 1
    assert promoted["signals"][0]["missing_data"]["policies"] == sorted(
        {
            "If ctx_a missing, treat as unknown.",
            "Second policy string for merge sort.",
        }
    )

    model_path = tmp_path / "promoted_signal_intelligence.yaml"
    model_path.write_text(yaml.safe_dump(promoted, sort_keys=False), encoding="utf-8")
    audit_path = tmp_path / "audit.md"
    proc = subprocess.run(
        [
            sys.executable,
            str(VALIDATE_PROMOTED),
            "--model",
            str(model_path),
            "--schema",
            str(PROMOTED_SCHEMA),
            "--audit-path",
            str(audit_path),
        ],
        cwd=str(REPO_ROOT),
        check=False,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr + proc.stdout


def test_translate_rejects_wrong_investigation_contract() -> None:
    bad = dict(_minimal_investigation_spec_v3())
    bad["investigation_spec_contract_version"] = "2.0.0"
    with pytest.raises(ValueError, match="3.0.0"):
        translate_investigation_spec_v3_to_promoted_signals(bad, package_id="pkg_x")


def test_load_promoted_signal_intelligence_for_package_optional(tmp_path: Path) -> None:
    pkg = tmp_path / "pkg"
    pkg.mkdir()
    (pkg / "package_manifest.yaml").write_text(
        "package_id: pkg_tmp\npackage_version: 1.0.0\nresearch_brief: r.yaml\nsignal_library: s.yaml\n",
        encoding="utf-8",
    )
    assert load_promoted_signal_intelligence_for_package(pkg) is None

    promoted = translate_investigation_spec_v3_to_promoted_signals(
        _minimal_investigation_spec_v3(), package_id="pkg_tmp"
    )
    (pkg / "psi.yaml").write_text(yaml.safe_dump(promoted, sort_keys=False), encoding="utf-8")
    (pkg / "package_manifest.yaml").write_text(
        "package_id: pkg_tmp\npackage_version: 1.0.0\nresearch_brief: r.yaml\n"
        "signal_library: s.yaml\npromoted_signal_intelligence: psi.yaml\n",
        encoding="utf-8",
    )
    loaded = load_promoted_signal_intelligence_for_package(pkg)
    assert isinstance(loaded, dict)
    assert loaded.get("package_id") == "pkg_tmp"


# ---------------------------------------------------------------------------
# Committed fixture — end-to-end (M-2)
# ---------------------------------------------------------------------------


def _run_package(path: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(VALIDATE_PACKAGE), "--package-dir", str(path)],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )


def _run_promoted_validator(model_path: Path, audit_path: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [
            sys.executable,
            str(VALIDATE_PROMOTED),
            "--model", str(model_path),
            "--schema", str(PROMOTED_SCHEMA),
            "--audit-path", str(audit_path),
        ],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )


def test_fixture_valid_package_passes_end_to_end() -> None:
    proc = _run_package(FIXTURE_VALID)
    assert proc.returncode == 0, proc.stderr + proc.stdout
    assert "promoted_signal_intelligence_validation: PASS" in proc.stdout


def test_forbidden_key_hypotheses_rejected(tmp_path: Path) -> None:
    bad = yaml.safe_load(
        (FIXTURE_VALID / "promoted_signal_intelligence.yaml").read_text(encoding="utf-8")
    )
    bad["hypotheses"] = [{"hypothesis_id": "hyp_smuggled"}]
    model_path = tmp_path / "psi.yaml"
    model_path.write_text(yaml.safe_dump(bad, sort_keys=False), encoding="utf-8")
    proc = _run_promoted_validator(model_path, tmp_path / "audit.md")
    assert proc.returncode != 0


def test_forbidden_key_hypothesis_ranking_rejected(tmp_path: Path) -> None:
    bad = yaml.safe_load(
        (FIXTURE_VALID / "promoted_signal_intelligence.yaml").read_text(encoding="utf-8")
    )
    bad["hypothesis_ranking"] = {"ordered_hypothesis_ids": ["hyp_x"]}
    model_path = tmp_path / "psi.yaml"
    model_path.write_text(yaml.safe_dump(bad, sort_keys=False), encoding="utf-8")
    proc = _run_promoted_validator(model_path, tmp_path / "audit.md")
    assert proc.returncode != 0


def test_forbidden_key_narrative_rejected(tmp_path: Path) -> None:
    bad = yaml.safe_load(
        (FIXTURE_VALID / "promoted_signal_intelligence.yaml").read_text(encoding="utf-8")
    )
    bad["narrative"] = {"mechanism": "smuggled narrative"}
    model_path = tmp_path / "psi.yaml"
    model_path.write_text(yaml.safe_dump(bad, sort_keys=False), encoding="utf-8")
    proc = _run_promoted_validator(model_path, tmp_path / "audit.md")
    assert proc.returncode != 0


def test_relationship_kind_role_misalignment_rejected(tmp_path: Path) -> None:
    bad = yaml.safe_load(
        (FIXTURE_VALID / "promoted_signal_intelligence.yaml").read_text(encoding="utf-8")
    )
    # corroboration kind requires corroborator role — pair it with mechanism_marker instead
    bad["signals"][0]["supporting_markers"][0]["relationship_kind"] = "corroboration"
    bad["signals"][0]["supporting_markers"][0]["role"] = "mechanism_marker"
    model_path = tmp_path / "psi.yaml"
    model_path.write_text(yaml.safe_dump(bad, sort_keys=False), encoding="utf-8")
    proc = _run_promoted_validator(model_path, tmp_path / "audit.md")
    assert proc.returncode != 0


def test_legacy_package_without_field_skips(tmp_path: Path) -> None:
    pkg = tmp_path / "pkg_legacy"
    pkg.mkdir()
    (pkg / "package_manifest.yaml").write_text(
        "package_id: pkg_legacy_test\npackage_version: 1.0.0\n"
        "research_brief: research_brief.yaml\nsignal_library: signal_library.yaml\n"
        "behavioural_impact: NONE\n",
        encoding="utf-8",
    )
    # copy minimal research_brief and signal_library from valid fixture
    import shutil
    shutil.copy(FIXTURE_VALID / "research_brief.yaml", pkg / "research_brief.yaml")
    shutil.copy(FIXTURE_VALID / "signal_library.yaml", pkg / "signal_library.yaml")
    proc = _run_package(pkg)
    assert "promoted_signal_intelligence_validation: SKIP" in proc.stdout
