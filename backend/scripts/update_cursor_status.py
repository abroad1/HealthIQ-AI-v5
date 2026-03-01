from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BUS_VERSION = "1.1"
ALLOWED_STATUSES = {"IN_PROGRESS", "COMPLETE", "FAILED"}


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def get_repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def ensure_automation_bus_dir(repo_root: Path) -> Path:
    bus_dir = repo_root / "automation_bus"
    bus_dir.mkdir(parents=True, exist_ok=True)
    return bus_dir


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
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def validate_prompt_hardening(bus_dir: Path, expected_work_id: str) -> tuple[bool, str]:
    hardening_path = bus_dir / "latest_prompt_hardening.json"
    if not hardening_path.exists():
        return False, "Missing automation_bus/latest_prompt_hardening.json"

    try:
        hardening = read_json(hardening_path)
    except (OSError, json.JSONDecodeError) as exc:
        return False, f"Failed to read latest_prompt_hardening.json: {exc}"

    if hardening.get("status") != "HARDENED":
        return False, "latest_prompt_hardening.json status must be HARDENED"

    if hardening.get("work_id") != expected_work_id:
        return False, "latest_prompt_hardening.json work_id must match prompt work_id"

    if "changes" not in hardening:
        return False, "latest_prompt_hardening.json must include changes field"

    if not isinstance(hardening.get("changes"), list):
        return False, "latest_prompt_hardening.json changes must be a list"

    return True, ""


def validate_gate_pass(bus_dir: Path, expected_work_id: str) -> tuple[bool, str]:
    evidence_path = bus_dir / "latest_gate_evidence.json"
    if not evidence_path.exists():
        return False, "Missing automation_bus/latest_gate_evidence.json"

    try:
        evidence = read_json(evidence_path)
    except (OSError, json.JSONDecodeError) as exc:
        return False, f"Failed to read latest_gate_evidence.json: {exc}"

    if evidence.get("work_id") != expected_work_id:
        return False, "latest_gate_evidence.json work_id must match prompt work_id"

    overall = evidence.get("overall")
    if not isinstance(overall, dict):
        return False, "latest_gate_evidence.json overall section is missing or invalid"

    if overall.get("status") != "PASS":
        return False, "Gate not PASS: latest_gate_evidence.json overall.status must be PASS"

    if overall.get("exit_code") != 0:
        return False, "Gate not PASS: latest_gate_evidence.json overall.exit_code must be 0"

    return True, ""


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python backend/scripts/update_cursor_status.py <IN_PROGRESS|COMPLETE|FAILED>", file=sys.stderr)
        return 2

    requested_status = sys.argv[1].strip().upper()
    if requested_status not in ALLOWED_STATUSES:
        print(f"Invalid status: {requested_status}", file=sys.stderr)
        return 2

    repo_root = get_repo_root()
    try:
        bus_dir = ensure_automation_bus_dir(repo_root)
    except OSError as exc:
        print(f"Failed to create automation_bus directory: {exc}", file=sys.stderr)
        return 1

    prompt_path = bus_dir / "latest_cursor_prompt.md"
    status_path = bus_dir / "latest_cursor_status.json"

    if not prompt_path.exists():
        print("Missing automation_bus/latest_cursor_prompt.md", file=sys.stderr)
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
        current_branch = run_git(repo_root, "rev-parse", "--abbrev-ref", "HEAD")
        head_sha = run_git(repo_root, "rev-parse", "HEAD")
    except subprocess.CalledProcessError as exc:
        print(f"Git command failed: {exc}", file=sys.stderr)
        return 1

    previous: dict[str, Any] | None = None
    if status_path.exists():
        try:
            previous = read_json(status_path)
        except json.JSONDecodeError:
            previous = None

    if (
        requested_status == "IN_PROGRESS"
        and previous
        and previous.get("work_id") == work_id
        and previous.get("status") == "IN_PROGRESS"
    ):
        print("Refusing overwrite: same work_id is already IN_PROGRESS", file=sys.stderr)
        return 3

    if requested_status == "IN_PROGRESS":
        ok, message = validate_prompt_hardening(bus_dir, work_id)
        if not ok:
            print(message, file=sys.stderr)
            return 2

    if requested_status == "COMPLETE":
        ok, message = validate_gate_pass(bus_dir, work_id)
        if not ok:
            print(message, file=sys.stderr)
            return 2

    now = utc_now_iso()
    started_utc = previous.get("cursor_started_utc") if previous else None
    if requested_status == "IN_PROGRESS":
        started_utc = now

    if not started_utc:
        started_utc = now

    completed_utc: str | None
    if requested_status == "IN_PROGRESS":
        completed_utc = None
    else:
        completed_utc = now

    payload = {
        "bus_version": BUS_VERSION,
        "work_id": work_id,
        "status": requested_status,
        "cursor_started_utc": started_utc,
        "cursor_completed_utc": completed_utc,
        "branch": current_branch,
        "head_sha": head_sha,
        "raw_stop_condition": None,
    }

    write_json(status_path, payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
