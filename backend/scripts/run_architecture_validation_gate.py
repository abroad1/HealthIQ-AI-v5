#!/usr/bin/env python3
"""
CI-ARCH-GATE-1 — Standard architecture validation gate (local + Automation Bus).

Runs governance validators, day-one architecture validation (includes medical-intelligence
delegation), explicit medical-intelligence validator, and architecture/regression pytest.

Exit: 0 on pass, non-zero on first failure.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def _run_step(
    repo_root: Path,
    label: str,
    args: list[str],
    extra_env: dict[str, str] | None = None,
) -> int:
    print(f"[architecture-gate] {label}")
    env = os.environ.copy()
    if extra_env:
        env.update(extra_env)
    proc = subprocess.run(args, cwd=repo_root, shell=False, env=env)
    if proc.returncode != 0:
        print(f"[architecture-gate] FAIL: {label} (exit {proc.returncode})", file=sys.stderr)
    return proc.returncode


def main() -> int:
    repo_root = Path(__file__).resolve().parents[2]
    py = sys.executable
    scripts = repo_root / "backend" / "scripts"

    steps: list[tuple[str, list[str], dict[str, str] | None]] = [
        (
            "validate_medical_frame_identity_index",
            [
                py,
                str(scripts / "validate_medical_frame_identity_index.py"),
                "--index",
                str(repo_root / "knowledge_bus/governance/medical_frame_identity_index_v1.yaml"),
            ],
            None,
        ),
        (
            "validate_context_modifier_catalogue",
            [
                py,
                str(scripts / "validate_context_modifier_catalogue.py"),
                "--catalogue",
                str(repo_root / "knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml"),
            ],
            None,
        ),
        (
            "validate_day_one_architecture",
            [py, str(scripts / "validate_day_one_architecture.py")],
            None,
        ),
        (
            "validate_medical_intelligence_architecture",
            [py, str(scripts / "validate_medical_intelligence_architecture.py")],
            None,
        ),
        (
            "pytest_architecture_guardrails",
            [
                py,
                "-m",
                "pytest",
                "backend/tests/architecture/test_day_one_architecture_guardrails.py",
                "backend/tests/architecture/test_medical_intelligence_architecture_sentinels.py",
                "-q",
            ],
            {"ARCHITECTURE_GATE_CHILD": "1"},
        ),
        (
            "pytest_governance_regression",
            [
                py,
                "-m",
                "pytest",
                "backend/tests/regression/test_med_frame_identity_index.py",
                "backend/tests/regression/test_context_modifier_catalogue.py",
                "-q",
            ],
            None,
        ),
    ]

    for label, args, step_env in steps:
        code = _run_step(repo_root, label, args, step_env)
        if code != 0:
            return code

    print("architecture_validation_gate: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
