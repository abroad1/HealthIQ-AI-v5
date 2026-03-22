"""Target intelligence schema v1 (KB-S47a) — contract and validator enforcement."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[3]
VALIDATE_PACKAGE = REPO_ROOT / "backend" / "scripts" / "validate_knowledge_package.py"
VALIDATE_INTEL = REPO_ROOT / "backend" / "scripts" / "validate_intelligence_model.py"
INTEL_SCHEMA = REPO_ROOT / "knowledge_bus" / "schema" / "intelligence_model_schema_v1.yaml"
FIXTURE_VALID = REPO_ROOT / "backend" / "tests" / "fixtures" / "pkg_target_schema_v1_valid"


def _bucket2_keys() -> list[str]:
    doc = yaml.safe_load(INTEL_SCHEMA.read_text(encoding="utf-8"))
    return list(doc.get("future_bucket2_homes_required_keys") or [])


def _run_intel(path: Path, *, audit_path: Path | None = None) -> subprocess.CompletedProcess:
    ap = audit_path or (REPO_ROOT / "backend" / "artifacts" / "intelligence_model_audit.md")
    return subprocess.run(
        [
            sys.executable,
            str(VALIDATE_INTEL),
            "--model",
            str(path),
            "--schema",
            str(INTEL_SCHEMA),
            "--audit-path",
            str(ap),
        ],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )


def _run_package(path: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [
            sys.executable,
            str(VALIDATE_PACKAGE),
            "--package-dir",
            str(path),
        ],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )


def test_intelligence_fixture_package_passes_end_to_end():
    proc = _run_package(FIXTURE_VALID)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "intelligence_validation: PASS" in proc.stdout


def test_intelligence_validator_rejects_single_hypothesis(tmp_path):
    bad = {
        "schema_version": "1.0.0",
        "package_id": "pkg_bad",
        "signals": [
            {
                "signal_id": "signal_x",
                "trigger_direction": "high",
                "primary_biomarker": "x",
                "hypotheses": [
                    {
                        "hypothesis_id": "h1",
                        "rank": 1,
                        "physiological_claim": "x" * 15,
                        "evidence_strength": "strong",
                        "caveats": ["c"],
                        "missing_data": {"policy": "p"},
                        "supporting_markers": [
                            {
                                "biomarker_id": "y",
                                "expected_direction": "high",
                                "role": "differential_marker",
                                "relationship_kind": "differential",
                                "availability": "common",
                            }
                        ],
                        "contradiction_markers": [],
                    }
                ],
                "provenance": {"evidence_source_ids": [], "rule_provenance_refs": []},
                "longitudinal_minimum": {
                    "stable_identity_key": None,
                    "snapshot_timestamp": None,
                    "signal_state_snapshot": None,
                },
                "future_bucket2_homes": {k: None for k in _bucket2_keys()},
            }
        ],
    }
    p = tmp_path / "intelligence_model.yaml"
    p.write_text(yaml.safe_dump(bad), encoding="utf-8")
    proc = _run_intel(p, audit_path=tmp_path / "audit.md")
    assert proc.returncode == 1
    out = proc.stdout + proc.stderr
    assert "at least 2 structured hypotheses" in out


def test_intelligence_validator_rejects_flat_supporting_markers(tmp_path):
    b2 = {k: None for k in _bucket2_keys()}
    bad = {
        "schema_version": "1.0.0",
        "package_id": "pkg_bad",
        "signals": [
            {
                "signal_id": "signal_x",
                "trigger_direction": "high",
                "primary_biomarker": "x",
                "hypotheses": [
                    {
                        "hypothesis_id": "h1",
                        "rank": 1,
                        "physiological_claim": "claim one text",
                        "evidence_strength": "strong",
                        "caveats": ["c"],
                        "missing_data": {"policy": "p"},
                        "supporting_markers": ["sodium"],
                        "contradiction_markers": [],
                    },
                    {
                        "hypothesis_id": "h2",
                        "rank": 2,
                        "physiological_claim": "claim two text",
                        "evidence_strength": "moderate",
                        "caveats": ["c"],
                        "missing_data": {"policy": "p"},
                        "supporting_markers": [
                            {
                                "biomarker_id": "y",
                                "expected_direction": "low",
                                "role": "differential_marker",
                                "relationship_kind": "differential",
                                "availability": "common",
                            }
                        ],
                        "contradiction_markers": [],
                    },
                ],
                "provenance": {"evidence_source_ids": [], "rule_provenance_refs": []},
                "longitudinal_minimum": {
                    "stable_identity_key": None,
                    "snapshot_timestamp": None,
                    "signal_state_snapshot": None,
                },
                "future_bucket2_homes": b2,
            }
        ],
    }
    p = tmp_path / "bad.yaml"
    p.write_text(yaml.safe_dump(bad), encoding="utf-8")
    proc = _run_intel(p, audit_path=tmp_path / "audit.md")
    assert proc.returncode == 1
    out = proc.stdout + proc.stderr
    assert "must be an object" in out


def test_intelligence_validator_rejects_forbidden_rendering_root(tmp_path):
    b2 = {k: None for k in _bucket2_keys()}
    base = {
        "schema_version": "1.0.0",
        "package_id": "pkg_bad",
        "rendering": {"layout": "x"},
        "signals": [
            {
                "signal_id": "signal_x",
                "trigger_direction": "high",
                "primary_biomarker": "x",
                "hypotheses": [
                    {
                        "hypothesis_id": "h1",
                        "rank": 1,
                        "physiological_claim": "claim one text",
                        "evidence_strength": "strong",
                        "caveats": ["c"],
                        "missing_data": {"policy": "p"},
                        "supporting_markers": [
                            {
                                "biomarker_id": "a",
                                "expected_direction": "high",
                                "role": "differential_marker",
                                "relationship_kind": "differential",
                                "availability": "common",
                            }
                        ],
                        "contradiction_markers": [],
                    },
                    {
                        "hypothesis_id": "h2",
                        "rank": 2,
                        "physiological_claim": "claim two text",
                        "evidence_strength": "moderate",
                        "caveats": ["c"],
                        "missing_data": {"policy": "p"},
                        "supporting_markers": [
                            {
                                "biomarker_id": "b",
                                "expected_direction": "low",
                                "role": "mechanism_marker",
                                "relationship_kind": "mechanism",
                                "availability": "common",
                            }
                        ],
                        "contradiction_markers": [],
                    },
                ],
                "provenance": {"evidence_source_ids": [], "rule_provenance_refs": []},
                "longitudinal_minimum": {
                    "stable_identity_key": None,
                    "snapshot_timestamp": None,
                    "signal_state_snapshot": None,
                },
                "future_bucket2_homes": b2,
            }
        ],
    }
    p = tmp_path / "bad.yaml"
    p.write_text(yaml.safe_dump(base), encoding="utf-8")
    proc = _run_intel(p, audit_path=tmp_path / "audit.md")
    assert proc.returncode == 1
    assert "Forbidden root key" in proc.stdout + proc.stderr


def test_intelligence_validator_rejects_signal_level_contradiction_markers(tmp_path):
    b2 = {k: None for k in _bucket2_keys()}
    bad = {
        "schema_version": "1.0.0",
        "package_id": "pkg_bad",
        "signals": [
            {
                "signal_id": "signal_x",
                "trigger_direction": "high",
                "primary_biomarker": "x",
                "contradiction_markers": [],
                "hypotheses": [
                    {
                        "hypothesis_id": "h1",
                        "rank": 1,
                        "physiological_claim": "claim one text",
                        "evidence_strength": "strong",
                        "caveats": ["c"],
                        "missing_data": {"policy": "p"},
                        "supporting_markers": [
                            {
                                "biomarker_id": "a",
                                "expected_direction": "high",
                                "role": "differential_marker",
                                "relationship_kind": "differential",
                                "availability": "common",
                            }
                        ],
                        "contradiction_markers": [],
                    },
                    {
                        "hypothesis_id": "h2",
                        "rank": 2,
                        "physiological_claim": "claim two text",
                        "evidence_strength": "moderate",
                        "caveats": ["c"],
                        "missing_data": {"policy": "p"},
                        "supporting_markers": [
                            {
                                "biomarker_id": "b",
                                "expected_direction": "low",
                                "role": "mechanism_marker",
                                "relationship_kind": "mechanism",
                                "availability": "common",
                            }
                        ],
                        "contradiction_markers": [],
                    },
                ],
                "provenance": {"evidence_source_ids": [], "rule_provenance_refs": []},
                "longitudinal_minimum": {
                    "stable_identity_key": None,
                    "snapshot_timestamp": None,
                    "signal_state_snapshot": None,
                },
                "future_bucket2_homes": b2,
            }
        ],
    }
    p = tmp_path / "bad.yaml"
    p.write_text(yaml.safe_dump(bad), encoding="utf-8")
    proc = _run_intel(p, audit_path=tmp_path / "audit.md")
    assert proc.returncode == 1
    assert "must not appear at signal level" in proc.stdout + proc.stderr


def test_kb45_chloride_package_skips_intelligence_validation():
    pkg = REPO_ROOT / "knowledge_bus" / "packages" / "pkg_kb45_chloride_high_hyperchloremia"
    proc = _run_package(pkg)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "intelligence_validation: SKIP" in proc.stdout


def test_aggregated_status_includes_intelligence_field():
    proc = _run_package(FIXTURE_VALID)
    assert proc.returncode == 0
    status_path = REPO_ROOT / "backend" / "artifacts" / "knowledge_status.json"
    data = json.loads(status_path.read_text(encoding="utf-8"))
    assert data.get("intelligence_validation") == "PASS"
