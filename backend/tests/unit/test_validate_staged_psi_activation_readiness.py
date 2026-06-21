"""Unit tests for staged PSI activation-readiness validator (P1-13)."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]
SCRIPTS = ROOT / "backend" / "scripts"
if str(ROOT / "backend") not in sys.path:
    sys.path.insert(0, str(ROOT / "backend"))

from scripts.validate_staged_psi_activation_readiness import (  # noqa: E402
    STAGED_BATCHES,
    audit_all_staged,
    audit_staged_batch,
    classify_item,
    load_ssot_keys,
)


def _minimal_psi(primary: str, supporting: list[dict] | None = None) -> dict:
    return {
        "promoted_signal_intelligence_contract_version": "1.0.0",
        "schema_version": "1.0.0",
        "package_id": "pkg_test",
        "signals": [
            {
                "signal_id": "signal_test",
                "research_domain": "hematologic",
                "signal_system": "hematologic",
                "primary_metric": {
                    "biomarker_id": primary,
                    "rationale": "Test primary metric rationale for validator fixture.",
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
                "supporting_markers": supporting
                or [
                    {
                        "biomarker_id": "hemoglobin",
                        "expected_direction": "low",
                        "role": "corroborator",
                        "relationship_kind": "corroboration",
                        "availability": "common",
                        "rationale": "Fixture corroborator marker for structural validation.",
                    }
                ],
                "contradiction_markers": [],
                "missing_data": {"policies": ["Review context before assigning interpretation."]},
                "confidence": {"evidence_strength": "moderate"},
                "override_rules": [
                    {
                        "rule_id": "or_test_fixture",
                        "resulting_state": "at_risk",
                        "description": "Escalate when corroborating marker supports the test fixture pattern.",
                        "conditions": [],
                        "source_refs": ["source_test_fixture"],
                    }
                ],
                "evidence": {
                    "evidence_strength": "moderate",
                    "physiological_claim": "Fixture physiological claim for staged PSI validator testing only.",
                    "threshold_notes": "Laboratory range only for fixture validation.",
                },
                "confirmatory_test_refs": [
                    {
                        "test_id": "ct_test",
                        "rationale": "Fixture confirmatory test reference for validator coverage.",
                    }
                ],
            }
        ],
    }


def test_load_ssot_keys_includes_hemoglobin():
    keys = load_ssot_keys(ROOT / "backend" / "ssot" / "biomarkers.yaml")
    assert "hemoglobin" in keys
    assert "white_blood_cells" in keys
    assert "lym" not in keys


def test_classify_item_priority():
    assert classify_item(["compile manifest hash mismatch"]) == "BLOCKED_MANIFEST_OR_HASH"
    assert classify_item(["primary_metric.biomarker_id not in SSOT: wbc"]) == "BLOCKED_BIOMARKER_IDENTITY"
    assert classify_item(["derived-marker supporting dependency: transferrin_saturation"]) == (
        "BLOCKED_DERIVED_MARKER_DEPENDENCY"
    )
    assert classify_item([]) == "ACTIVATION_READY"


def _sync_manifest_hash(dest_pkg: Path) -> None:
    """Align compile manifest hash with copied PSI bytes (fixture isolation only)."""
    psi_path = dest_pkg / "promoted_signal_intelligence.yaml"
    manifest_path = dest_pkg / "compile_manifest.yaml"
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    digest = hashlib.sha256(psi_path.read_bytes()).hexdigest()
    manifest.setdefault("output_hashes_sha256", {})[
        "promoted_signal_intelligence.yaml"
    ] = digest
    manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")


def test_audit_staged_batch_detects_non_canonical_primary(tmp_path):
    src_pkg = (
        ROOT
        / "knowledge_bus/generated_pilot/p1_12_batch_c/pkg_kb52c_wbc_high_reactive_leukocytosis"
    )
    batch_root = tmp_path / "p1_test"
    dest_pkg = batch_root / src_pkg.name
    dest_pkg.mkdir(parents=True)
    for name in ("promoted_signal_intelligence.yaml", "compile_manifest.yaml"):
        dest_pkg.joinpath(name).write_bytes(src_pkg.joinpath(name).read_bytes())
    _sync_manifest_hash(dest_pkg)

    ssot_keys = load_ssot_keys(ROOT / "backend" / "ssot" / "biomarkers.yaml")
    items = audit_staged_batch(
        "p1_test",
        batch_root,
        ssot_keys=ssot_keys,
        signal_systems={"hematologic", "inflammatory", "hepatic", "metabolic", "lipid_transport", "renal", "vascular", "hormonal", "mitochondrial", "endocrine", "bone", "mineral", "nutritional", "other"},
        trigger_directions={"high", "low", "bidirectional", "context_dependent"},
        production_opt_ins=set(),
        psi_schema_path=ROOT / "knowledge_bus" / "schema" / "promoted_signal_intelligence_schema_v1.yaml",
    )
    assert len(items) == 1
    assert items[0].activation_readiness == "BLOCKED_BIOMARKER_IDENTITY"
    assert items[0].primary_metric_biomarker_id == "wbc"
    assert items[0].compile_manifest_hash_status == "pass"


def test_audit_staged_batch_detects_derived_marker_supporting(tmp_path):
    src_pkg = (
        ROOT
        / "knowledge_bus/generated_pilot/p1_12_batch_c/pkg_kb52c_iron_low_absolute_iron_deficiency"
    )
    batch_root = tmp_path / "p1_test"
    dest_pkg = batch_root / src_pkg.name
    dest_pkg.mkdir(parents=True)
    for name in ("promoted_signal_intelligence.yaml", "compile_manifest.yaml"):
        dest_pkg.joinpath(name).write_bytes(src_pkg.joinpath(name).read_bytes())
    _sync_manifest_hash(dest_pkg)

    ssot_keys = load_ssot_keys(ROOT / "backend" / "ssot" / "biomarkers.yaml")
    items = audit_staged_batch(
        "p1_test",
        batch_root,
        ssot_keys=ssot_keys,
        signal_systems={"hematologic", "inflammatory", "hepatic", "metabolic", "lipid_transport", "renal", "vascular", "hormonal", "mitochondrial", "endocrine", "bone", "mineral", "nutritional", "other"},
        trigger_directions={"high", "low", "bidirectional", "context_dependent"},
        production_opt_ins=set(),
        psi_schema_path=ROOT / "knowledge_bus" / "schema" / "promoted_signal_intelligence_schema_v1.yaml",
    )
    assert items[0].activation_readiness == "BLOCKED_DERIVED_MARKER_DEPENDENCY"
    assert any("transferrin_saturation" in b for b in items[0].blockers)


def test_audit_all_staged_repo_estate_counts():
    report = audit_all_staged(batches=STAGED_BATCHES)
    estate = report["staged_estate"]
    assert estate["psi_files_found"] == 41
    assert estate["compile_manifests_found"] == 41
    assert report["summary"]["blocked_count"] == 41
    assert report["summary"]["activation_ready_count"] == 0


def test_cli_runs_on_repo_estate():
    cmd = [
        sys.executable,
        str(SCRIPTS / "validate_staged_psi_activation_readiness.py"),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=False, cwd=str(ROOT))
    assert proc.returncode == 0
    assert "psi_files_found: 41" in proc.stdout
    assert "activation_ready_count: 0" in proc.stdout
