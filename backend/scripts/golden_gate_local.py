from __future__ import annotations

import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BUS_VERSION = "1.1"


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


def get_current_branch(repo_root: Path) -> str:
    return run_git(repo_root, "rev-parse", "--abbrev-ref", "HEAD")


def get_head_sha(repo_root: Path) -> str:
    return run_git(repo_root, "rev-parse", "HEAD")


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


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def build_stub_evidence(work_id: str | None, branch: str, head_sha: str) -> dict[str, Any]:
    return {
        "bus_version": BUS_VERSION,
        "work_id": work_id,
        "created_utc": utc_now_iso(),
        "branch": branch,
        "head_sha": head_sha,
        "overall": {
            "status": "FAIL",
            "exit_code": -1,
        },
        "checks": [],
        "artifacts": {},
        "stdout_tail": [],
    }


def main() -> int:
    repo_root = get_repo_root()

    try:
        bus_dir = ensure_automation_bus_dir(repo_root)
    except OSError as exc:
        print(f"Failed to create automation_bus directory: {exc}", file=sys.stderr)
        return 1

    prompt_path = bus_dir / "latest_cursor_prompt.md"
    evidence_path = bus_dir / "latest_gate_evidence.json"
    transcript_path = bus_dir / "latest_gate_output.txt"

    try:
        current_branch = get_current_branch(repo_root)
        head_sha = get_head_sha(repo_root)
    except subprocess.CalledProcessError as exc:
        with transcript_path.open("w", encoding="utf-8") as transcript_file:
            transcript_file.write(
                f"[gate-start] created_utc={utc_now_iso()} work_id=null branch=unknown head_sha=unknown\n"
            )
            transcript_file.write(f"[error] git metadata lookup failed: {exc}\n")
            transcript_file.flush()
        print(f"Git command failed: {exc}", file=sys.stderr)
        return 1

    work_id: str | None = None
    prompt_branch: str | None = None
    all_output: list[str] = []
    with transcript_path.open("w", encoding="utf-8") as transcript_file:
        if prompt_path.exists():
            try:
                front_matter = parse_front_matter(prompt_path)
                work_id = front_matter.get("work_id")
                prompt_branch = front_matter.get("branch")
            except OSError as exc:
                transcript_file.write(f"[error] failed to read prompt file: {exc}\n")
                transcript_file.flush()
                print(f"Failed to read prompt file: {exc}", file=sys.stderr)

        transcript_file.write(
            f"[gate-start] created_utc={utc_now_iso()} work_id={work_id if work_id is not None else 'null'} "
            f"branch={current_branch} head_sha={head_sha}\n"
        )
        transcript_file.flush()

        evidence = build_stub_evidence(work_id, current_branch, head_sha)
        write_json(evidence_path, evidence)

        if not prompt_path.exists():
            reason = "Missing automation_bus/latest_cursor_prompt.md"
            transcript_file.write(f"[error] {reason}\n")
            transcript_file.flush()
            print(reason, file=sys.stderr)
            evidence["overall"] = {"status": "FAIL", "exit_code": 2}
            write_json(evidence_path, evidence)
            return 2

        if not work_id or not prompt_branch:
            reason = "Prompt front matter must include work_id and branch"
            transcript_file.write(f"[error] {reason}\n")
            transcript_file.flush()
            print(reason, file=sys.stderr)
            evidence["work_id"] = work_id
            evidence["overall"] = {"status": "FAIL", "exit_code": 2}
            write_json(evidence_path, evidence)
            return 2

        evidence["work_id"] = work_id

        if current_branch != prompt_branch:
            reason = f"Branch mismatch. prompt branch={prompt_branch}, current branch={current_branch}"
            transcript_file.write(f"[error] {reason}\n")
            transcript_file.flush()
            print(reason, file=sys.stderr)
            evidence["overall"] = {"status": "FAIL", "exit_code": 3}
            write_json(evidence_path, evidence)
            return 3

        checks = [
            {
                "name": "run_baseline_tests",
                "args": [sys.executable, str(repo_root / "backend" / "scripts" / "run_baseline_tests.py")],
            },
            {
                "name": "verify_three_layer_pipeline",
                "args": [sys.executable, str(repo_root / "backend" / "scripts" / "verify_three_layer_pipeline.py")],
            },
        ]

        evidence["checks"] = []

        for check in checks:
            display_command = " ".join(check["args"])
            started = time.perf_counter()
            proc = subprocess.run(
                check["args"],
                cwd=repo_root,
                capture_output=True,
                text=True,
                shell=False,
            )
            duration_ms = int((time.perf_counter() - started) * 1000)

            chunk = (
                f"$ {display_command}\n"
                f"--- STDOUT ---\n{proc.stdout}"
                f"--- STDERR ---\n{proc.stderr}"
                f"[exit_code={proc.returncode}]\n"
            )
            all_output.append(chunk)
            transcript_file.write(chunk)
            transcript_file.flush()

            status = "PASS" if proc.returncode == 0 else "FAIL"
            evidence["checks"].append(
                {
                    "name": check["name"],
                    "command": display_command,
                    "exit_code": proc.returncode,
                    "duration_ms": duration_ms,
                    "status": status,
                }
            )

            if proc.returncode != 0:
                evidence["overall"] = {"status": "FAIL", "exit_code": proc.returncode}
                tail_lines = "".join(all_output).splitlines()[-50:]
                evidence["stdout_tail"] = tail_lines
                write_json(evidence_path, evidence)
                return proc.returncode

        evidence["overall"] = {"status": "PASS", "exit_code": 0}
        tail_lines = "".join(all_output).splitlines()[-50:]
        evidence["stdout_tail"] = tail_lines
        write_json(evidence_path, evidence)
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
