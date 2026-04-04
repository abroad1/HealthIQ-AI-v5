"""
Bounded AB/VR acceptance harness runner (KB-S53-ABVR-HARNESS).

This script does NOT replace golden_gate_local.py or verify_three_layer_pipeline.
The control-plane gate still anchors on golden_panel_160.json by default.

Run this script in CI or locally when validating AB/VR acceptance explicitly, alongside
the standard gate. See docs/investigations/KB-S53_AB_VR_ACCEPTANCE_HARNESS.md.

Usage (from repo root):
  python backend/scripts/run_ab_vr_acceptance_harness.py

Exit: 0 if all listed tests pass, non-zero otherwise.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> int:
    backend = Path(__file__).resolve().parents[1]
    tests: list[str] = [
        "tests/unit/test_clinician_report_runtime_alignment.py",
        "tests/unit/test_golden_panel_runner.py::test_report_v1_present_and_stable_for_ab_vr_panels",
        "tests/unit/test_golden_panel_runner.py::test_ab_vr_interaction_chains_include_homocysteine_context_and_confidence_floor",
        "tests/unit/test_root_cause_v1_homocysteine.py::test_root_cause_v1_present_for_homocysteine_and_non_regression",
        "tests/unit/test_root_cause_v1_homocysteine.py::test_root_cause_v1_text_fields_respect_safety_denylist",
        "tests/unit/test_root_cause_v1_homocysteine.py::test_confirmatory_test_suppression_and_repeat_behavior_for_ab_panel",
        "tests/unit/test_root_cause_v1_homocysteine.py::test_confirmatory_test_suppression_output_is_deterministic_for_ab_panel",
    ]
    cmd = [sys.executable, "-m", "pytest", *tests, "-v", "--tb=short"]
    print("$ " + " ".join(cmd), flush=True)
    proc = subprocess.run(cmd, cwd=backend, check=False)
    return int(proc.returncode)


if __name__ == "__main__":
    raise SystemExit(main())
