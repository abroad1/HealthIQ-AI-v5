"""Governance tests for ARCH-COMPLETION-3 day-one launch estate gate."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[3]
GATE = REPO_ROOT / "knowledge_bus/governance/day_one_launch_estate_gate_v1.yaml"
VALIDATOR = REPO_ROOT / "backend/scripts/validate_day_one_launch_estate_gate.py"


def _load_gate() -> dict:
    assert GATE.is_file(), "day_one_launch_estate_gate_v1.yaml missing"
    return yaml.safe_load(GATE.read_text(encoding="utf-8")) or {}


def test_launch_estate_gate_has_allowed_verdict():
    gate = _load_gate()
    verdict = gate.get("final_verdict")
    allowed = gate.get("allowed_final_verdicts") or []
    assert verdict in allowed
    assert verdict in {
        "DAY_ONE_ARCHITECTURE_COMPLETE",
        "DAY_ONE_ARCHITECTURE_COMPLETE_WITH_NON_BLOCKING_CARRY_FORWARD",
        "DAY_ONE_ARCHITECTURE_NOT_COMPLETE",
    }


def test_launch_estate_gate_references_traceability_manifest():
    gate = _load_gate()
    manifest_ref = gate.get("traceability_manifest") or ""
    assert "day_one_full_traceability_manifest_v1.yaml" in manifest_ref
    assert (REPO_ROOT / manifest_ref).is_file()


def test_launch_estate_validator_passes():
    proc = subprocess.run(
        [sys.executable, str(VALIDATOR)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr or proc.stdout
