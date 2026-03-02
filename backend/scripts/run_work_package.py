from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BUS_VERSION = "1.2"


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def get_repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def run_git(repo_root: Path, *args: str) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
    )
    return proc.stdout.strip()


def parse_front_matter(path: Path) -> dict[str, str]:
    content = path.read_text(encoding="utf-8")
    lines = content.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}

    data: dict[str, str] = {}
    for line in lines[1:]:
        stripped = line.strip()
        if stripped == "---":
            break
        if not stripped or stripped.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip("'\"")
    return data


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_failed_status(
    status_path: Path,
    work_id: str,
    branch: str,
    head_sha: str,
    started_utc: str | None,
) -> bool:
    now = utc_now_iso()
    payload = {
        "bus_version": BUS_VERSION,
        "work_id": work_id,
        "status": "FAILED",
        "cursor_started_utc": started_utc or now,
        "cursor_completed_utc": now,
        "branch": branch,
        "head_sha": head_sha,
        "raw_stop_condition": None,
    }
    try:
        write_json(status_path, payload)
    except OSError:
        return False
    return True


def main() -> int:
    repo_root = get_repo_root()
    bus_dir = repo_root / "automation_bus"
    prompt_path = bus_dir / "latest_cursor_prompt.md"
    hardening_path = bus_dir / "latest_prompt_hardening.json"
    status_path = bus_dir / "latest_cursor_status.json"
    evidence_path = bus_dir / "latest_gate_evidence.json"
    gate_path = repo_root / "backend" / "scripts" / "golden_gate_local.py"

    # Preflight validation (hard fail, non-zero).
    if not prompt_path.exists():
        print("Missing automation_bus/latest_cursor_prompt.md", file=sys.stderr)
        return 2
    if not hardening_path.exists():
        print("Missing automation_bus/latest_prompt_hardening.json", file=sys.stderr)
        return 2

    try:
        front_matter = parse_front_matter(prompt_path)
    except OSError as exc:
        print(f"Failed to read prompt file: {exc}", file=sys.stderr)
        return 1

    work_id = front_matter.get("work_id")
    prompt_branch = front_matter.get("branch")
    if not work_id or not prompt_branch:
        print("Prompt front matter must include work_id and branch", file=sys.stderr)
        return 2

    try:
        hardening = read_json(hardening_path)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Failed to read latest_prompt_hardening.json: {exc}", file=sys.stderr)
        return 2

    if hardening.get("work_id") != work_id:
        print("latest_prompt_hardening.json work_id must match prompt work_id", file=sys.stderr)
        return 2

    try:
        current_branch = run_git(repo_root, "rev-parse", "--abbrev-ref", "HEAD")
        head_sha = run_git(repo_root, "rev-parse", "HEAD")
        porcelain = run_git(repo_root, "status", "--porcelain")
    except subprocess.CalledProcessError as exc:
        print(f"Git command failed: {exc}", file=sys.stderr)
        return 1

    if porcelain:
        print("Working tree must be clean (git status --porcelain must be empty)", file=sys.stderr)
        return 2

    if current_branch != prompt_branch:
        print(
            f"Branch mismatch. prompt branch={prompt_branch}, current branch={current_branch}",
            file=sys.stderr,
        )
        return 2

    started_utc: str | None = None
    if status_path.exists():
        try:
            previous = read_json(status_path)
        except (OSError, json.JSONDecodeError):
            previous = None
        if isinstance(previous, dict) and previous.get("work_id") == work_id:
            previous_status = previous.get("status")
            previous_head_sha = previous.get("head_sha")
            if previous_status == "COMPLETE":
                print("Refusing re-run: same work_id is already COMPLETE", file=sys.stderr)
                return 3
            if previous_status == "IN_PROGRESS" and previous_head_sha == head_sha:
                started_utc = previous.get("cursor_started_utc")

    in_progress = {
        "bus_version": BUS_VERSION,
        "work_id": work_id,
        "status": "IN_PROGRESS",
        "cursor_started_utc": started_utc or utc_now_iso(),
        "branch": current_branch,
        "head_sha": head_sha,
        "raw_stop_condition": None,
    }
    try:
        write_json(status_path, in_progress)
    except OSError as exc:
        print(f"Failed to write latest_cursor_status.json: {exc}", file=sys.stderr)
        return 1

    try:
        gate_proc = subprocess.run(
            [sys.executable, str(gate_path)],
            cwd=repo_root,
            stdout=None,
            stderr=None,
            shell=False,
            check=False,
        )
    except OSError as exc:
        if not write_failed_status(status_path, work_id, current_branch, head_sha, in_progress["cursor_started_utc"]):
            print(f"Golden gate invocation failed and status write failed: {exc}", file=sys.stderr)
            return 1
        print(f"Golden gate invocation failed: {exc}", file=sys.stderr)
        return 1

    if not evidence_path.exists():
        if not write_failed_status(status_path, work_id, current_branch, head_sha, in_progress["cursor_started_utc"]):
            print("Missing automation_bus/latest_gate_evidence.json and failed to write FAILED status", file=sys.stderr)
            return 1
        print("Missing automation_bus/latest_gate_evidence.json", file=sys.stderr)
        return 2

    try:
        evidence = read_json(evidence_path)
    except (OSError, json.JSONDecodeError) as exc:
        if not write_failed_status(status_path, work_id, current_branch, head_sha, in_progress["cursor_started_utc"]):
            print(f"Failed to read gate evidence and failed to write FAILED status: {exc}", file=sys.stderr)
            return 1
        print(f"Failed to read latest_gate_evidence.json: {exc}", file=sys.stderr)
        return 2

    if evidence.get("work_id") != work_id:
        if not write_failed_status(status_path, work_id, current_branch, head_sha, in_progress["cursor_started_utc"]):
            print("Gate evidence work_id mismatch and failed to write FAILED status", file=sys.stderr)
            return 1
        print("latest_gate_evidence.json work_id must match prompt work_id", file=sys.stderr)
        return 2

    evidence["bus_version"] = BUS_VERSION
    try:
        write_json(evidence_path, evidence)
    except OSError as exc:
        if not write_failed_status(status_path, work_id, current_branch, head_sha, in_progress["cursor_started_utc"]):
            print(f"Failed to update gate evidence and failed to write FAILED status: {exc}", file=sys.stderr)
            return 1
        print(f"Failed to update latest_gate_evidence.json: {exc}", file=sys.stderr)
        return 1

    terminal_status = "COMPLETE" if gate_proc.returncode == 0 else "FAILED"
    terminal_payload = {
        "bus_version": BUS_VERSION,
        "work_id": work_id,
        "status": terminal_status,
        "cursor_started_utc": in_progress["cursor_started_utc"],
        "cursor_completed_utc": utc_now_iso(),
        "branch": current_branch,
        "head_sha": head_sha,
        "raw_stop_condition": None,
    }
    try:
        write_json(status_path, terminal_payload)
    except OSError as exc:
        print(f"Failed to write terminal status: {exc}", file=sys.stderr)
        return 1

    return gate_proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
