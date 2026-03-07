#!/usr/bin/env python3
"""
Knowledge Bus lifecycle controller.
"""

from __future__ import annotations

import json
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
LATEST_STATUS_PATH = CURRENT_DIR / "latest_knowledge_status.json"
SCHEMA_PATH = KNOWLEDGE_BUS_DIR / "schema" / "signal_library_schema.yaml"
VALIDATOR_SCRIPT_PATH = REPO_ROOT / "backend" / "scripts" / "validate_signal_library.py"
PACKAGE_ID_PATTERN_PREFIX = "KBP-"


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


def list_existing_package_ids() -> list[str]:
    package_ids: list[str] = []
    if not PACKAGES_DIR.exists():
        return package_ids

    for child in PACKAGES_DIR.iterdir():
        if not child.is_dir():
            continue
        name = child.name
        if not name.startswith(PACKAGE_ID_PATTERN_PREFIX):
            continue
        suffix = name[len(PACKAGE_ID_PATTERN_PREFIX) :]
        if len(suffix) == 4 and suffix.isdigit():
            package_ids.append(name)
    return sorted(package_ids)


def next_package_id() -> str:
    existing = list_existing_package_ids()
    if not existing:
        return "KBP-0001"
    highest = max(int(package_id.split("-")[1]) for package_id in existing)
    return f"KBP-{highest + 1:04d}"


def package_dir(package_id: str) -> Path:
    return PACKAGES_DIR / package_id


def start_command() -> int:
    ensure_structure()
    if not is_working_tree_clean():
        print("ERROR: Working tree must be clean before start.", file=sys.stderr)
        return 1
    if ACTIVE_PACKAGE_PATH.exists():
        print("ERROR: Active package token already exists.", file=sys.stderr)
        return 1

    package_id = next_package_id()
    target_dir = package_dir(package_id)
    target_dir.mkdir(parents=True, exist_ok=False)

    active_payload = {
        "package_id": package_id,
        "status": "IN_PROGRESS",
        "created_utc": utc_now_iso(),
    }
    write_json(ACTIVE_PACKAGE_PATH, active_payload)

    print(f"Knowledge package started: {package_id}")
    print(f"Package directory: {target_dir}")
    print(f"Active token: {ACTIVE_PACKAGE_PATH}")
    return 0


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

    package_id = active_payload.get("package_id")
    if not isinstance(package_id, str) or not package_id.startswith(PACKAGE_ID_PATTERN_PREFIX):
        print("ERROR: Active package token contains invalid package_id.", file=sys.stderr)
        return 1

    target_dir = package_dir(package_id)
    if not target_dir.exists() or not target_dir.is_dir():
        print(f"ERROR: Package directory not found: {target_dir}", file=sys.stderr)
        return 1

    library_path = target_dir / "signal_library.yaml"
    if not library_path.exists():
        print(f"ERROR: Required package artefact missing: {library_path}", file=sys.stderr)
        return 1

    command = [
        sys.executable,
        str(VALIDATOR_SCRIPT_PATH),
        "--library",
        str(library_path),
        "--schema",
        str(SCHEMA_PATH),
        "--output-dir",
        str(target_dir),
    ]

    result = subprocess.run(command, cwd=REPO_ROOT, check=False)
    if result.returncode != 0:
        print(
            f"ERROR: Validator failed for package {package_id}. Active token preserved.",
            file=sys.stderr,
        )
        return 1

    audit_path = target_dir / "architecture_audit.md"
    status_path = target_dir / "knowledge_status.json"
    if not audit_path.exists():
        print(f"ERROR: Validator output missing: {audit_path}", file=sys.stderr)
        return 1
    if not status_path.exists():
        print(f"ERROR: Validator output missing: {status_path}", file=sys.stderr)
        return 1

    shutil.copyfile(status_path, LATEST_STATUS_PATH)
    ACTIVE_PACKAGE_PATH.unlink()

    print(f"Knowledge package finished successfully: {package_id}")
    print(f"Latest status copied to: {LATEST_STATUS_PATH}")
    return 0


def status_command() -> int:
    ensure_structure()
    active_exists = ACTIVE_PACKAGE_PATH.exists()
    print(f"Active package token exists: {'yes' if active_exists else 'no'}")

    if active_exists:
        try:
            active_payload = read_json(ACTIVE_PACKAGE_PATH)
            package_id = active_payload.get("package_id", "UNKNOWN")
            print(f"Active package ID: {package_id}")
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            print(f"Active package ID: unreadable ({exc})")
    else:
        print("Active package ID: none")

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
        print("ERROR: Expected exactly one command: start | finish | status", file=sys.stderr)
        return 1

    command = args[0].strip().lower()
    if command == "start":
        return start_command()
    if command == "finish":
        return finish_command()
    if command == "status":
        return status_command()

    print(
        f"ERROR: Unsupported command '{args[0]}'. Use one of: start, finish, status.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
