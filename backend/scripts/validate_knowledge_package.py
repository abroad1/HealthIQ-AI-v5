#!/usr/bin/env python3
"""
Orchestrate Knowledge Bus package validation.

This is the canonical package promotion validator authority for Knowledge Bus.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
SIGNAL_CONTRACT_V2 = "2.0.0"
ARTIFACTS_DIR = ROOT / "backend" / "artifacts"
MANIFEST_AUDIT_PATH = ARTIFACTS_DIR / "package_manifest_audit.md"
RESEARCH_AUDIT_PATH = ARTIFACTS_DIR / "research_audit.md"
ARCHITECTURE_AUDIT_PATH = ARTIFACTS_DIR / "architecture_audit.md"
AGGREGATED_STATUS_PATH = ARTIFACTS_DIR / "knowledge_status.json"
RESEARCH_SCHEMA_PATH = ROOT / "knowledge_bus" / "schema" / "research_brief_schema.yaml"
SIGNAL_SCHEMA_PATH = ROOT / "knowledge_bus" / "schema" / "signal_library_schema.yaml"
BIOMARKER_REGISTRY_PATH = ROOT / "backend" / "ssot" / "biomarkers.yaml"

MANIFEST_VALIDATOR = ROOT / "backend" / "scripts" / "validate_package_manifest.py"
RESEARCH_VALIDATOR = ROOT / "backend" / "scripts" / "validate_research_brief.py"
SIGNAL_VALIDATOR = ROOT / "backend" / "scripts" / "validate_signal_library.py"


def _signal_library_contract_version(package_dir: Path) -> str:
    """Read library.schema_version from signal_library.yaml (defaults to 1.0.0)."""
    path = package_dir / "signal_library.yaml"
    try:
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError):
        return "1.0.0"
    if not isinstance(payload, dict):
        return "1.0.0"
    lib = payload.get("library")
    if isinstance(lib, dict) and isinstance(lib.get("schema_version"), str):
        return lib["schema_version"].strip()
    return "1.0.0"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate a Knowledge Bus package by orchestrating validators."
    )
    parser.add_argument(
        "--package-dir",
        required=True,
        help="Path to a package directory containing research_brief.yaml and signal_library.yaml.",
    )
    parser.add_argument(
        "--require-behavioural-impact",
        action="store_true",
        help="Require behavioural_impact in package_manifest.yaml during validation.",
    )
    parser.add_argument(
        "--require-engine-compatibility",
        action="store_true",
        help="Require engine_compatibility in package_manifest.yaml during validation.",
    )
    parser.add_argument(
        "--authoritative-engine-compatibility",
        default="",
        help="Authoritative engine_compatibility value to enforce in manifest validation.",
    )
    return parser.parse_args(argv)


def write_aggregated_status(
    manifest_status: str,
    research_status: str,
    signal_status: str,
) -> None:
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "manifest_validation": manifest_status,
        "research_validation": research_status,
        "signal_validation": signal_status,
        "ready_for_implementation": (
            manifest_status == "PASS"
            and research_status == "PASS"
            and signal_status == "PASS"
        ),
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

    manifest_path = package_dir / "package_manifest.yaml"
    research_brief_path = package_dir / "research_brief.yaml"
    signal_library_path = package_dir / "signal_library.yaml"

    if not manifest_path.exists():
        print(f"ERROR: Missing required file: {manifest_path}", file=sys.stderr)
        return 1
    if not research_brief_path.exists():
        print(f"ERROR: Missing required file: {research_brief_path}", file=sys.stderr)
        return 1
    if not signal_library_path.exists():
        print(f"ERROR: Missing required file: {signal_library_path}", file=sys.stderr)
        return 1

    manifest_exit = run_validator(
        [
            sys.executable,
            str(MANIFEST_VALIDATOR),
            "--manifest",
            str(manifest_path),
            "--audit-path",
            str(MANIFEST_AUDIT_PATH),
            *(["--require-behavioural-impact"] if args.require_behavioural_impact else []),
            *(["--require-engine-compatibility"] if args.require_engine_compatibility else []),
            *(
                [
                    "--authoritative-engine-compatibility",
                    args.authoritative_engine_compatibility,
                ]
                if isinstance(args.authoritative_engine_compatibility, str)
                and args.authoritative_engine_compatibility.strip()
                else []
            ),
        ]
    )
    manifest_status = "PASS" if manifest_exit == 0 else "FAIL"

    lib_contract = _signal_library_contract_version(package_dir)

    research_cmd = [
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
    if lib_contract == SIGNAL_CONTRACT_V2:
        research_cmd.append("--research-fidelity")

    research_exit = run_validator(research_cmd)
    research_status = "PASS" if research_exit == 0 else "FAIL"

    signal_cmd = [
        sys.executable,
        str(SIGNAL_VALIDATOR),
        "--library",
        str(signal_library_path),
        "--schema",
        str(SIGNAL_SCHEMA_PATH),
        "--output-dir",
        str(ARTIFACTS_DIR),
    ]
    if lib_contract == SIGNAL_CONTRACT_V2:
        signal_cmd.extend(["--research-brief", str(research_brief_path)])

    signal_exit = run_validator(signal_cmd)
    signal_status = "PASS" if signal_exit == 0 else "FAIL"

    write_aggregated_status(manifest_status, research_status, signal_status)

    print(f"manifest_validation: {manifest_status}")
    print(f"research_validation: {research_status}")
    print(f"signal_validation: {signal_status}")
    print(
        "ready_for_implementation: "
        f"{manifest_status == 'PASS' and research_status == 'PASS' and signal_status == 'PASS'}"
    )
    print(f"manifest_audit_path: {MANIFEST_AUDIT_PATH}")
    print(f"research_audit_path: {RESEARCH_AUDIT_PATH}")
    print(f"architecture_audit_path: {ARCHITECTURE_AUDIT_PATH}")
    print(f"aggregated_status_path: {AGGREGATED_STATUS_PATH}")

    return (
        0
        if manifest_status == "PASS" and research_status == "PASS" and signal_status == "PASS"
        else 1
    )


if __name__ == "__main__":
    raise SystemExit(main())
