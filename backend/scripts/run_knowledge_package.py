#!/usr/bin/env python3
"""
Knowledge Bus lifecycle controller.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
KNOWLEDGE_BUS_DIR = REPO_ROOT / "knowledge_bus"
PACKAGES_DIR = KNOWLEDGE_BUS_DIR / "packages"
CURRENT_DIR = KNOWLEDGE_BUS_DIR / "current"
ACTIVE_PACKAGE_PATH = CURRENT_DIR / "active_package.json"
CURRENT_STATUS_PATH = CURRENT_DIR / "knowledge_status.json"
LATEST_STATUS_PATH = CURRENT_DIR / "latest_knowledge_status.json"
ARTIFACT_STATUS_PATH = REPO_ROOT / "backend" / "artifacts" / "knowledge_status.json"
VALIDATOR_SCRIPT_PATH = REPO_ROOT / "backend" / "scripts" / "validate_knowledge_package.py"
PACKAGE_DIR_PATTERN_PREFIX = "pkg_"
LEGACY_PACKAGE_ID_PATTERN_PREFIX = "KBP-"
NUMERIC_PACKAGE_DIR_PATTERN = re.compile(r"^pkg_(\d{4})$")
NUMERIC_LEGACY_PACKAGE_ID_PATTERN = re.compile(r"^KBP-(\d{4})$")


def utc_now_iso() -> str:
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def ensure_structure() -> None:
    PACKAGES_DIR.mkdir(parents=True, exist_ok=True)
    CURRENT_DIR.mkdir(parents=True, exist_ok=True)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        loaded = json.load(handle)
    if not isinstance(loaded, dict):
        raise ValueError(f"JSON payload at {path} must be an object")
    return loaded


def is_working_tree_clean() -> bool:
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    return result.returncode == 0 and result.stdout.strip() == ""


def list_existing_numeric_package_dirs() -> list[str]:
    package_dirs: list[str] = []
    if not PACKAGES_DIR.exists():
        return package_dirs

    for child in PACKAGES_DIR.iterdir():
        if not child.is_dir():
            continue
        name = child.name
        if NUMERIC_PACKAGE_DIR_PATTERN.fullmatch(name):
            package_dirs.append(name)
    return sorted(package_dirs)


def next_package_dir_name() -> str:
    existing = list_existing_numeric_package_dirs()
    if not existing:
        return "pkg_0001"
    highest = max(int(match.group(1)) for value in existing if (match := NUMERIC_PACKAGE_DIR_PATTERN.fullmatch(value)))
    return f"pkg_{highest + 1:04d}"


def package_dir(package_dir_name: str) -> Path:
    return PACKAGES_DIR / package_dir_name


def _legacy_package_id_from_dir_name(package_dir_name: str) -> str:
    match = NUMERIC_PACKAGE_DIR_PATTERN.fullmatch(package_dir_name)
    if not match:
        return ""
    return f"KBP-{match.group(1)}"


def _legacy_to_numeric_pkg_dir(package_id: str) -> str:
    match = NUMERIC_LEGACY_PACKAGE_ID_PATTERN.fullmatch(package_id)
    if not match:
        return ""
    return f"pkg_{match.group(1)}"


def resolve_active_package_dir_name(active_payload: dict[str, Any]) -> str:
    package_dir_name = active_payload.get("package_dir")
    if isinstance(package_dir_name, str) and package_dir_name.startswith(PACKAGE_DIR_PATTERN_PREFIX):
        return package_dir_name

    package_id = active_payload.get("package_id")
    if isinstance(package_id, str):
        if package_id.startswith(PACKAGE_DIR_PATTERN_PREFIX):
            return package_id
        legacy_derived = _legacy_to_numeric_pkg_dir(package_id)
        if legacy_derived:
            return legacy_derived

    return ""


def write_runtime_status(payload: dict[str, Any]) -> None:
    # latest_knowledge_status.json is authoritative runtime state.
    write_json(LATEST_STATUS_PATH, payload)
    # Keep legacy mirror for compatibility with existing operational tooling.
    write_json(CURRENT_STATUS_PATH, payload)


def start_command() -> int:
    ensure_structure()
    if not is_working_tree_clean():
        print("ERROR: Working tree must be clean before start.", file=sys.stderr)
        return 1
    if ACTIVE_PACKAGE_PATH.exists():
        print("ERROR: Active package token already exists.", file=sys.stderr)
        return 1

    package_dir_name = next_package_dir_name()
    target_dir = package_dir(package_dir_name)
    target_dir.mkdir(parents=True, exist_ok=False)

    active_payload = {
        "package_dir": package_dir_name,
        "package_id": _legacy_package_id_from_dir_name(package_dir_name),
        "status": "IN_PROGRESS",
        "created_utc": utc_now_iso(),
    }
    write_json(ACTIVE_PACKAGE_PATH, active_payload)
    write_runtime_status(
        {
            "manifest_validation": "PENDING",
            "research_validation": "PENDING",
            "signal_validation": "PENDING",
            "ready_for_implementation": False,
        }
    )

    print(f"Knowledge package started: {package_dir_name}")
    print(f"Package directory: {target_dir}")
    print(f"Active token: {ACTIVE_PACKAGE_PATH}")
    print(f"Latest status: {LATEST_STATUS_PATH}")
    return 0


def validate_command() -> int:
    ensure_structure()
    if not ACTIVE_PACKAGE_PATH.exists():
        print("ERROR: Active package token not found.", file=sys.stderr)
        return 1

    try:
        active_payload = read_json(ACTIVE_PACKAGE_PATH)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: Failed to read active package token: {exc}", file=sys.stderr)
        return 1

    package_dir_name = resolve_active_package_dir_name(active_payload)
    if not package_dir_name:
        print("ERROR: Active package token contains invalid package_dir/package_id.", file=sys.stderr)
        return 1

    target_dir = package_dir(package_dir_name)
    if not target_dir.exists() or not target_dir.is_dir():
        print(f"ERROR: Package directory not found: {target_dir}", file=sys.stderr)
        return 1

    command = [
        sys.executable,
        str(VALIDATOR_SCRIPT_PATH),
        "--package-dir",
        str(target_dir),
        "--require-behavioural-impact",
    ]

    result = subprocess.run(command, cwd=REPO_ROOT, check=False)
    if not ARTIFACT_STATUS_PATH.exists():
        print(f"ERROR: Validator output missing: {ARTIFACT_STATUS_PATH}", file=sys.stderr)
        return 1
    latest_payload = read_json(ARTIFACT_STATUS_PATH)
    write_runtime_status(latest_payload)

    if result.returncode != 0:
        print(
            f"ERROR: Validator failed for package {package_dir_name}. Latest status updated.",
            file=sys.stderr,
        )
    else:
        print(f"Validation completed for package: {package_dir_name}")
        print(f"Latest status written to: {LATEST_STATUS_PATH}")
    return result.returncode


def finish_command() -> int:
    ensure_structure()
    if not ACTIVE_PACKAGE_PATH.exists():
        print("ERROR: Active package token not found.", file=sys.stderr)
        return 1

    try:
        active_payload = read_json(ACTIVE_PACKAGE_PATH)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: Failed to read active package token: {exc}", file=sys.stderr)
        return 1

    package_dir_name = resolve_active_package_dir_name(active_payload)
    if not package_dir_name:
        print("ERROR: Active package token contains invalid package_dir/package_id.", file=sys.stderr)
        return 1

    if not LATEST_STATUS_PATH.exists():
        print(f"ERROR: Latest knowledge status not found: {LATEST_STATUS_PATH}", file=sys.stderr)
        return 1

    try:
        latest_status = read_json(LATEST_STATUS_PATH)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: Failed to read latest knowledge status: {exc}", file=sys.stderr)
        return 1

    manifest_status = latest_status.get("manifest_validation")
    research_status = latest_status.get("research_validation")
    signal_status = latest_status.get("signal_validation")
    failed: list[str] = []
    if manifest_status != "PASS":
        failed.append(f"manifest_validation={manifest_status}")
    if research_status != "PASS":
        failed.append(f"research_validation={research_status}")
    if signal_status != "PASS":
        failed.append(f"signal_validation={signal_status}")

    if failed:
        print(
            "ERROR: Knowledge package validation not ready for finish. Failed checks: "
            + ", ".join(failed),
            file=sys.stderr,
        )
        return 1

    write_runtime_status(latest_status)
    ACTIVE_PACKAGE_PATH.unlink()

    print(f"Knowledge package finished successfully: {package_dir_name}")
    print(f"Latest status confirmed at: {LATEST_STATUS_PATH}")
    return 0


def status_command() -> int:
    ensure_structure()
    active_exists = ACTIVE_PACKAGE_PATH.exists()
    print(f"Active package token exists: {'yes' if active_exists else 'no'}")

    if active_exists:
        try:
            active_payload = read_json(ACTIVE_PACKAGE_PATH)
            package_dir_name = resolve_active_package_dir_name(active_payload) or "UNKNOWN"
            print(f"Active package directory: {package_dir_name}")
            legacy_package_id = active_payload.get("package_id", "")
            if isinstance(legacy_package_id, str) and legacy_package_id:
                print(f"Legacy package ID: {legacy_package_id}")
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            print(f"Active package directory: unreadable ({exc})")
    else:
        print("Active package directory: none")

    latest_exists = LATEST_STATUS_PATH.exists()
    print(f"Latest knowledge status exists: {'yes' if latest_exists else 'no'}")
    if latest_exists:
        try:
            latest_payload = read_json(LATEST_STATUS_PATH)
            readiness = latest_payload.get("ready_for_implementation")
            validator_status = latest_payload.get("validator_status")
            print(f"Ready for implementation: {readiness}")
            print(f"Validator status: {validator_status}")
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            print(f"Ready for implementation: unreadable ({exc})")
            print(f"Validator status: unreadable ({exc})")

    return 0


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) != 1:
        print("ERROR: Expected exactly one command: start | validate | finish | status", file=sys.stderr)
        return 1

    command = args[0].strip().lower()
    if command == "start":
        return start_command()
    if command == "validate":
        return validate_command()
    if command == "finish":
        return finish_command()
    if command == "status":
        return status_command()

    print(
        f"ERROR: Unsupported command '{args[0]}'. Use one of: start, validate, finish, status.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
