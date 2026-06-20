"""Governance tests for active signal context gate reachability validator."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[3]

BATCH2_REGISTER = REPO_ROOT / "knowledge_bus/governance/batch2_full_coverage_activation_execution_register_v1.yaml"
POLICY = REPO_ROOT / "knowledge_bus/governance/active_signal_context_gate_reachability_policy_v1.yaml"
VALIDATOR = REPO_ROOT / "backend/scripts/validate_active_signal_context_gate_reachability.py"


def test_batch2_active_package_count_is_four():
    payload = yaml.safe_load(BATCH2_REGISTER.read_text(encoding="utf-8")) or {}
    activated = payload.get("activated_packages") or []
    assert payload.get("activated_package_count") == 4
    assert len(activated) == 4


def test_pregnancy_absent_from_questionnaire_policy():
    payload = yaml.safe_load(POLICY.read_text(encoding="utf-8")) or {}
    absent = payload.get("questionnaire_absent_context_keys") or {}
    pregnancy = absent.get("pregnancy_status") or {}
    safe = set(pregnancy.get("safe_missing_states") or [])
    assert "not_answered" in safe
    assert "not_applicable" in safe


def test_active_gate_reachability_validator_passes():
    proc = subprocess.run(
        [sys.executable, str(VALIDATOR)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr or proc.stdout


def test_dhea_s_high_and_low_packages_in_expected_registers():
    payload = yaml.safe_load(BATCH2_REGISTER.read_text(encoding="utf-8")) or {}
    activated = {row["package_id"] for row in payload.get("activated_packages") or []}
    inactive = {row["package_id"] for row in payload.get("kept_inactive_packages") or []}
    assert "pkg_kb47_dhea_high_androgen_excess_context" in activated
    assert "pkg_kb47_dhea_low_adrenal_androgen_reduction" in inactive
