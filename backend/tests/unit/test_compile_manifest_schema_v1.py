"""ARCH-RT-1 — compile manifest schema and validator smoke tests."""

from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[3]
SCHEMA_PATH = REPO_ROOT / "knowledge_bus" / "schema" / "compile_manifest_schema_v1.yaml"
VALIDATOR = REPO_ROOT / "backend" / "scripts" / "validate_compile_manifest.py"


def _minimal_pilot_manifest() -> dict:
    spec_path = "knowledge_bus/research/investigation_specs/inv_vitamin_d_low_deficiency_v1.yaml"
    spec_bytes = (REPO_ROOT / spec_path).read_bytes()
    spec_hash = hashlib.sha256(spec_bytes).hexdigest()
    activation_key = "signal_vitamin_d_low::inv_vitamin_d_low_deficiency"
    return {
        "compile_id": "pilot-arch-rt-1-vitamin-d-001",
        "compiler_name": "activation_compile_v1",
        "compiler_version": "0.0.0-pilot",
        "compile_mode": "pilot",
        "source_contract_version": "3.0.0",
        "source_specs": [
            {
                "source_spec_id": "inv_vitamin_d_low_deficiency",
                "source_path": spec_path,
                "source_hash": spec_hash,
                "source_hash_algorithm": "sha256",
            }
        ],
        "outputs": [
            {
                "output_type": "package_manifest",
                "output_path": "knowledge_bus/packages/pkg_s24_vitamin_d_low_deficiency/package_manifest.yaml",
                "output_hash": "existing-on-disk-not-recompiled",
                "output_hash_algorithm": "sha256",
                "package_id": "pkg_s24_vitamin_d_low_deficiency",
                "signal_id": "signal_vitamin_d_low",
                "activation_key": activation_key,
                "source_spec_id": "inv_vitamin_d_low_deficiency",
            }
        ],
        "translation_rules_version": "1.0.0",
        "compiled_at_utc": "2026-05-28T22:30:00Z",
        "compiled_by": "arch-rt-1-test",
        "provenance_status": "pilot_evidence_only",
        "policy_version": "ADR-RT-004-v1",
        "activation_keys_emitted": [activation_key],
        "collisions_detected": [],
    }


def test_compile_manifest_schema_yaml_loads():
    payload = yaml.safe_load(SCHEMA_PATH.read_text(encoding="utf-8"))
    assert payload["schema_version"] == "1.0.0"
    assert "compile_id" in payload["root_required_fields"]
    output_rules = payload.get("output_field_rules") or {}
    assert "activation_key" in output_rules


def test_validate_compile_manifest_accepts_minimal_pilot(tmp_path: Path):
    manifest_path = tmp_path / "compile_manifest.yaml"
    manifest_path.write_text(
        yaml.safe_dump(_minimal_pilot_manifest(), sort_keys=False),
        encoding="utf-8",
    )
    proc = subprocess.run(
        [sys.executable, str(VALIDATOR), "--manifest", str(manifest_path)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
