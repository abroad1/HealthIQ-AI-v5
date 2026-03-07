#!/usr/bin/env python3
"""
Orchestrate Knowledge Bus package validation.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS_DIR = ROOT / "backend" / "artifacts"
RESEARCH_AUDIT_PATH = ARTIFACTS_DIR / "research_audit.md"
ARCHITECTURE_AUDIT_PATH = ARTIFACTS_DIR / "architecture_audit.md"
AGGREGATED_STATUS_PATH = ARTIFACTS_DIR / "knowledge_status.json"
RESEARCH_SCHEMA_PATH = ROOT / "knowledge_bus" / "schema" / "research_brief_schema.yaml"
SIGNAL_SCHEMA_PATH = ROOT / "knowledge_bus" / "schema" / "signal_library_schema.yaml"
BIOMARKER_REGISTRY_PATH = ROOT / "backend" / "ssot" / "biomarkers.yaml"

RESEARCH_VALIDATOR = ROOT / "backend" / "scripts" / "validate_research_brief.py"
SIGNAL_VALIDATOR = ROOT / "backend" / "scripts" / "validate_signal_library.py"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate a Knowledge Bus package by orchestrating validators."
    )
    parser.add_argument(
        "--package-dir",
        required=True,
        help="Path to a package directory containing research_brief.yaml and signal_library.yaml.",
    )
    return parser.parse_args(argv)


def write_aggregated_status(research_status: str, signal_status: str) -> None:
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "research_validation": research_status,
        "signal_validation": signal_status,
        "ready_for_implementation": research_status == "PASS" and signal_status == "PASS",
    }
    AGGREGATED_STATUS_PATH.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )


def run_validator(command: list[str]) -> int:
    process = subprocess.run(command, cwd=ROOT, check=False)
    return process.returncode


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    package_dir = Path(args.package_dir)
    if not package_dir.is_absolute():
        package_dir = (ROOT / package_dir).resolve()

    research_brief_path = package_dir / "research_brief.yaml"
    signal_library_path = package_dir / "signal_library.yaml"

    if not research_brief_path.exists():
        print(f"ERROR: Missing required file: {research_brief_path}", file=sys.stderr)
        return 1
    if not signal_library_path.exists():
        print(f"ERROR: Missing required file: {signal_library_path}", file=sys.stderr)
        return 1

    research_exit = run_validator(
        [
            sys.executable,
            str(RESEARCH_VALIDATOR),
            "--brief",
            str(research_brief_path),
            "--schema",
            str(RESEARCH_SCHEMA_PATH),
            "--biomarkers-registry",
            str(BIOMARKER_REGISTRY_PATH),
            "--audit-path",
            str(RESEARCH_AUDIT_PATH),
        ]
    )
    research_status = "PASS" if research_exit == 0 else "FAIL"

    signal_exit = run_validator(
        [
            sys.executable,
            str(SIGNAL_VALIDATOR),
            "--library",
            str(signal_library_path),
            "--schema",
            str(SIGNAL_SCHEMA_PATH),
            "--output-dir",
            str(ARTIFACTS_DIR),
        ]
    )
    signal_status = "PASS" if signal_exit == 0 else "FAIL"

    write_aggregated_status(research_status, signal_status)

    print(f"research_validation: {research_status}")
    print(f"signal_validation: {signal_status}")
    print(
        "ready_for_implementation: "
        f"{research_status == 'PASS' and signal_status == 'PASS'}"
    )
    print(f"research_audit_path: {RESEARCH_AUDIT_PATH}")
    print(f"architecture_audit_path: {ARCHITECTURE_AUDIT_PATH}")
    print(f"aggregated_status_path: {AGGREGATED_STATUS_PATH}")

    return 0 if research_status == "PASS" and signal_status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
