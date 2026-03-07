from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BUS_VERSION = "1.2"
STATE_DIR = Path("automation_bus") / "state"
ACTIVE_FILE = STATE_DIR / "work_package_active.json"
KB_READINESS_FILE = Path("knowledge_bus") / "current" / "latest_knowledge_status.json"


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


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

    first_non_empty_index: int | None = None
    for idx, line in enumerate(lines):
        if line.strip():
            first_non_empty_index = idx
            break
    if first_non_empty_index is None or lines[first_non_empty_index].strip() != "---":
        return {}

    data: dict[str, str] = {}
    closed = False
    for line in lines[first_non_empty_index + 1 :]:
        stripped = line.strip()
        if stripped == "---":
            closed = True
            break
        if not stripped or stripped.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip("'\"")

    if not closed:
        return {}
    return data


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise json.JSONDecodeError("Expected object", "", 0)
    return value


def _requires_signal_library_readiness(front_matter: dict[str, str]) -> bool:
    return front_matter.get("knowledge_dependency") == "SIGNAL_LIBRARY"


def _check_signal_library_readiness(repo_root: Path) -> str | None:
    readiness_path = repo_root / KB_READINESS_FILE
    readiness_label = "knowledge_bus/current/latest_knowledge_status.json"

    if not readiness_path.exists():
        return f"Knowledge Bus readiness file missing: {readiness_label}"

    try:
        readiness = read_json(readiness_path)
    except json.JSONDecodeError:
        return "Knowledge Bus readiness file is not valid JSON"
    except OSError:
        return "Knowledge Bus readiness file is not valid JSON"

    if "ready_for_implementation" not in readiness:
        return "Knowledge Bus readiness file missing required field: ready_for_implementation"

    ready_flag = readiness.get("ready_for_implementation")
    if not isinstance(ready_flag, bool):
        return "Knowledge Bus readiness field must be boolean"
    if not ready_flag:
        return "Knowledge Bus promotion not complete (ready_for_implementation=false)"

    return None


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_active_token(work_id: str, branch: str) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "work_id": work_id,
        "branch": branch,
        "status": "STARTED",
        "timestamp_utc": _utc_now_iso(),
    }
    ACTIVE_FILE.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _remove_active_token() -> None:
    if ACTIVE_FILE.exists():
        ACTIVE_FILE.unlink()


def load_prompt_and_hardening(bus_dir: Path) -> tuple[str, str]:
    prompt_path = bus_dir / "latest_cursor_prompt.md"
    hardening_path = bus_dir / "latest_prompt_hardening.json"

    if not prompt_path.exists():
        raise ValueError("Missing automation_bus/latest_cursor_prompt.md")
    if not hardening_path.exists():
        raise ValueError("Missing automation_bus/latest_prompt_hardening.json")

    try:
        front_matter = parse_front_matter(prompt_path)
    except OSError as exc:
        raise RuntimeError(f"Failed to read prompt file: {exc}") from exc

    work_id = front_matter.get("work_id")
    prompt_branch = front_matter.get("branch")
    if not work_id or not prompt_branch:
        raise ValueError("Prompt front matter must include work_id and branch")

    try:
        hardening = read_json(hardening_path)
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Failed to read latest_prompt_hardening.json: {exc}") from exc

    if hardening.get("work_id") != work_id:
        raise ValueError("latest_prompt_hardening.json work_id must match prompt work_id")
    return work_id, prompt_branch


def write_terminal_status(
    status_path: Path,
    work_id: str,
    branch: str,
    head_sha: str,
    started_utc: str,
    status: str,
) -> None:
    payload = {
        "bus_version": BUS_VERSION,
        "work_id": work_id,
        "status": status,
        "cursor_started_utc": started_utc,
        "cursor_completed_utc": utc_now_iso(),
        "branch": branch,
        "head_sha": head_sha,
        "raw_stop_condition": None,
    }
    write_json(status_path, payload)


def run_start(repo_root: Path) -> int:
    bus_dir = repo_root / "automation_bus"
    status_path = bus_dir / "latest_cursor_status.json"
    prompt_path = bus_dir / "latest_cursor_prompt.md"

    try:
        work_id, prompt_branch = load_prompt_and_hardening(bus_dir)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    try:
        current_branch = run_git(repo_root, "rev-parse", "--abbrev-ref", "HEAD")
        head_sha = run_git(repo_root, "rev-parse", "HEAD")
    except subprocess.CalledProcessError as exc:
        print(f"Git command failed: {exc}", file=sys.stderr)
        return 1

    if current_branch != prompt_branch:
        print(
            f"Branch mismatch. prompt branch={prompt_branch}, current branch={current_branch}",
            file=sys.stderr,
        )
        return 2

    try:
        porcelain = run_git(repo_root, "status", "--porcelain")
    except subprocess.CalledProcessError as exc:
        print(f"Git command failed: {exc}", file=sys.stderr)
        return 1

    if porcelain:
        print("Working tree must be clean (git status --porcelain must be empty)", file=sys.stderr)
        return 2

    try:
        front_matter = parse_front_matter(prompt_path)
    except OSError as exc:
        print(f"Failed to read prompt file: {exc}", file=sys.stderr)
        return 1

    if _requires_signal_library_readiness(front_matter):
        readiness_error = _check_signal_library_readiness(repo_root)
        if readiness_error is not None:
            print(readiness_error, file=sys.stderr)
            return 2

    previous: dict[str, Any] | None = None
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
                return 0

    payload = {
        "bus_version": BUS_VERSION,
        "work_id": work_id,
        "status": "IN_PROGRESS",
        "cursor_started_utc": utc_now_iso(),
        "branch": current_branch,
        "head_sha": head_sha,
        "raw_stop_condition": None,
    }
    try:
        write_json(status_path, payload)
    except OSError as exc:
        print(f"Failed to write latest_cursor_status.json: {exc}", file=sys.stderr)
        return 1
    try:
        _write_active_token(work_id=work_id, branch=current_branch)
    except OSError as exc:
        print(f"Failed to write active work package token: {exc}", file=sys.stderr)
        return 1
    return 0


def run_finish(repo_root: Path) -> int:
    bus_dir = repo_root / "automation_bus"
    status_path = bus_dir / "latest_cursor_status.json"
    evidence_path = bus_dir / "latest_gate_evidence.json"
    gate_path = repo_root / "backend" / "scripts" / "golden_gate_local.py"

    try:
        work_id, prompt_branch = load_prompt_and_hardening(bus_dir)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    try:
        current_branch = run_git(repo_root, "rev-parse", "--abbrev-ref", "HEAD")
        head_sha = run_git(repo_root, "rev-parse", "HEAD")
    except subprocess.CalledProcessError as exc:
        print(f"Git command failed: {exc}", file=sys.stderr)
        return 1

    if current_branch != prompt_branch:
        print(
            f"Branch mismatch. prompt branch={prompt_branch}, current branch={current_branch}",
            file=sys.stderr,
        )
        return 2

    if not status_path.exists():
        print("Missing automation_bus/latest_cursor_status.json", file=sys.stderr)
        return 2

    try:
        existing_status = read_json(status_path)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Failed to read latest_cursor_status.json: {exc}", file=sys.stderr)
        return 2

    if existing_status.get("work_id") != work_id:
        print("latest_cursor_status.json work_id must match prompt work_id", file=sys.stderr)
        return 2

    if existing_status.get("status") != "IN_PROGRESS":
        print("latest_cursor_status.json status must be IN_PROGRESS for finish", file=sys.stderr)
        return 2

    started_utc = existing_status.get("cursor_started_utc")
    if not isinstance(started_utc, str) or not started_utc:
        print("latest_cursor_status.json cursor_started_utc is missing or invalid", file=sys.stderr)
        return 2

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
        try:
            write_terminal_status(
                status_path=status_path,
                work_id=work_id,
                branch=current_branch,
                head_sha=head_sha,
                started_utc=started_utc,
                status="FAILED",
            )
        except OSError as status_exc:
            print(f"Golden gate invocation failed and status write failed: {status_exc}", file=sys.stderr)
            return 1
        print(f"Golden gate invocation failed: {exc}", file=sys.stderr)
        return 1

    evidence_ok = False
    if evidence_path.exists():
        try:
            evidence = read_json(evidence_path)
        except (OSError, json.JSONDecodeError):
            evidence = None
        if isinstance(evidence, dict):
            overall = evidence.get("overall")
            if isinstance(overall, dict):
                evidence_ok = (
                    evidence.get("work_id") == work_id
                    and overall.get("status") == "PASS"
                    and overall.get("exit_code") == 0
                )

    success = gate_proc.returncode == 0 and evidence_ok
    terminal_status = "COMPLETE" if success else "FAILED"

    try:
        write_terminal_status(
            status_path=status_path,
            work_id=work_id,
            branch=current_branch,
            head_sha=head_sha,
            started_utc=started_utc,
            status=terminal_status,
        )
    except OSError as exc:
        print(f"Failed to write terminal status: {exc}", file=sys.stderr)
        return 1

    if success:
        try:
            _remove_active_token()
        except OSError as exc:
            print(f"Failed to remove active work package token: {exc}", file=sys.stderr)
            return 1

    return 0 if success else 4


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="run_work_package.py")
    parser.add_argument("command", choices=("start", "finish"))
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    repo_root = get_repo_root()
    if args.command == "start":
        return run_start(repo_root)
    return run_finish(repo_root)


if __name__ == "__main__":
    raise SystemExit(main())
