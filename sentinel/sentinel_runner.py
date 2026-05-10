"""
Phase 1 Sentinel — report-only quality runner.

Usage:
  python sentinel/sentinel_runner.py --changed-files path1 path2 ...
  python sentinel/sentinel_runner.py --surface parser/alias/canonical
  python sentinel/sentinel_runner.py --defect-class ggt_alias_miss
  python sentinel/sentinel_runner.py --all

Governance rules:
  - Never modifies product code or governed assets.
  - Never writes to automation_bus/.
  - Never self-certifies a fix.
  - Reads Automation Bus artefacts; does not write them.
  - Escalates when HIGH-risk or meaning-bearing surfaces are implicated.
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import subprocess
import sys
import tempfile
import uuid
from pathlib import Path
from typing import Optional

REPO_ROOT = Path(__file__).resolve().parent.parent
SENTINEL_ROOT = REPO_ROOT / "sentinel"
REPORTS_DIR = SENTINEL_ROOT / "reports"
STATE_DIR = SENTINEL_ROOT / "state"
PACKS_DIR = SENTINEL_ROOT / "packs"

ESCAPED_DEFECTS_PACK = PACKS_DIR / "escaped_defects_v1.json"

# Surfaces that require governance escalation in the report
ESCALATION_SURFACES = {
    "analytics/scoring/signal",
    "SSOT/canonical_authority",
    "governance/control_plane",
    "knowledge_bus/intelligence",
}

# Test files belonging to each named defect class
DEFECT_CLASS_TESTS: dict[str, list[str]] = {
    "ggt_alias_miss":              ["backend/tests/regression/test_ggt_alias_regression.py"],
    "bilirubin_canonical_mismatch":["backend/tests/regression/test_bilirubin_alias_regression.py"],
    "slug_leakage":                ["backend/tests/regression/test_slug_leakage_regression.py"],
    "wave1_contradiction":         ["backend/tests/regression/test_wave1_contradiction_status.py"],
    "persisted_result_replay":     ["backend/tests/regression/test_persisted_result_replay_status.py"],
    "alias_sweep":                 ["backend/tests/regression/test_alias_canonical_sweep.py"],
    "narrative_compiler_why_surface": [
        "backend/tests/regression/test_narrative_compiler_why_surface_regression.py",
    ],
    "questionnaire_exercise_unknown": [
        "backend/tests/regression/test_obs2_questionnaire_exercise_unknown_regression.py",
    ],
}

ALL_REGRESSION_TESTS = [t for tests in DEFECT_CLASS_TESTS.values() for t in tests]


def _git_branch() -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True, text=True, cwd=str(REPO_ROOT)
        )
        return result.stdout.strip() or "unknown"
    except Exception:
        return "unknown"


def _counts_from_pytest_json_report(report_path: Path) -> dict[str, int] | None:
    """Read pytest-json-report output; returns None if unreadable."""
    try:
        payload = json.loads(report_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    summary = payload.get("summary") or {}
    # Outcomes come from pytest-json-report's Counter(keys = passed/failed/skipped/error/…)
    err_n = summary.get("error")
    if err_n is None:
        err_n = summary.get("errors", 0)
    return {
        "passed": int(summary.get("passed", 0)),
        "failed": int(summary.get("failed", 0)),
        "errors": int(err_n or 0),
        "skipped": int(summary.get("skipped", 0)),
    }


def _run_pytest(test_paths: list[str]) -> dict:
    """Run pytest on the given test paths; return structured result.

    Uses pytest-json-report so pass/fail/skip/error counts match pytest's real
    totals. Plain ``-q`` output does not include a textual summary line, so text
    heuristics alone would stay at zeros.
    """
    abs_paths = [str(REPO_ROOT / p) for p in test_paths]
    fd, json_path_str = tempfile.mkstemp(prefix="sentinel_pytest_", suffix=".json")
    json_path = Path(json_path_str)
    os.close(fd)
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        "--tb=short",
        "-q",
        "--no-header",
        "-m",
        "regression",
        "--json-report",
        f"--json-report-file={json_path}",
        *abs_paths,
    ]

    try:
        proc = subprocess.run(
            cmd, capture_output=True, text=True, cwd=str(REPO_ROOT)
        )
        counts = _counts_from_pytest_json_report(json_path)
        if counts is None:
            counts = _parse_pytest_output(
                "\n".join((proc.stdout or "", proc.stderr or ""))
            )
        return {
            "exit_code": proc.returncode,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
            "passed": proc.returncode == 0,
            "test_counts": counts,
        }
    except Exception as exc:
        try:
            json_path.unlink(missing_ok=True)
        except OSError:
            pass
        zero = {"passed": 0, "failed": 0, "errors": 0, "skipped": 0}
        return {
            "exit_code": -1,
            "stdout": "",
            "stderr": str(exc),
            "passed": False,
            "test_counts": zero,
        }
    finally:
        try:
            json_path.unlink(missing_ok=True)
        except OSError:
            pass


def _parse_pytest_output(stdout: str) -> dict:
    """Extract counts from pytest -q output."""
    counts = {"passed": 0, "failed": 0, "errors": 0, "skipped": 0}
    for line in stdout.splitlines():
        line_l = line.lower()
        if "passed" in line_l:
            for part in line_l.split(","):
                part = part.strip()
                if "passed" in part:
                    try:
                        counts["passed"] = int(part.split()[0])
                    except (ValueError, IndexError):
                        pass
        if "failed" in line_l:
            for part in line_l.split(","):
                part = part.strip()
                if "failed" in part:
                    try:
                        counts["failed"] = int(part.split()[0])
                    except (ValueError, IndexError):
                        pass
        if "error" in line_l:
            for part in line_l.split(","):
                part = part.strip()
                if "error" in part:
                    try:
                        counts["errors"] = int(part.split()[0])
                    except (ValueError, IndexError):
                        pass
        if "skipped" in line_l:
            for part in line_l.split(","):
                part = part.strip()
                if "skipped" in part:
                    try:
                        counts["skipped"] = int(part.split()[0])
                    except (ValueError, IndexError):
                        pass
    return counts


def _load_escaped_defects_pack() -> dict:
    if ESCAPED_DEFECTS_PACK.exists():
        with open(ESCAPED_DEFECTS_PACK, encoding="utf-8") as f:
            return json.load(f)
    return {}


def _determine_escalation(surfaces: list[str]) -> bool:
    return bool(ESCALATION_SURFACES & set(surfaces))


def run(
    changed_files: Optional[list[str]] = None,
    surface: Optional[str] = None,
    defect_class: Optional[str] = None,
    run_all: bool = False,
) -> dict:
    """Core Sentinel runner. Returns the structured report dict."""
    from classifier import classify_files, SURFACE_TEST_MAP  # noqa: local import

    run_id = str(uuid.uuid4())[:8]
    branch = _git_branch()
    utc_now = datetime.datetime.utcnow().isoformat() + "Z"

    # Determine trigger type and selected tests
    trigger_type = "unknown"
    classified_surfaces: list[str] = []
    classified_files_detail: list[dict] = []
    tests_selected: list[str] = []
    coverage_gaps: list[str] = []

    if run_all:
        trigger_type = "all_regression"
        tests_selected = list(dict.fromkeys(ALL_REGRESSION_TESTS))

    elif defect_class:
        trigger_type = "defect_class"
        tests_selected = DEFECT_CLASS_TESTS.get(defect_class, [])
        if not tests_selected:
            available = ", ".join(DEFECT_CLASS_TESTS.keys())
            print(f"[SENTINEL] Unknown defect class '{defect_class}'. Available: {available}")

    elif surface:
        trigger_type = "surface"
        classified_surfaces = [surface]
        tests_selected = SURFACE_TEST_MAP.get(surface, [])
        if not tests_selected:
            coverage_gaps.append(f"No regression tests mapped to surface '{surface}'")

    elif changed_files:
        trigger_type = "changed_files"
        classification = classify_files(changed_files)
        classified_surfaces = classification.surfaces
        classified_files_detail = [
            {"path": f.path, "surface": f.surface, "risk": f.risk, "reason": f.reason}
            for f in classification.files
        ]
        tests_selected = classification.recommended_tests()
        escalation_needed = _determine_escalation(classified_surfaces)
        if classification.max_risk == "HIGH":
            coverage_gaps.append(
                "HIGH-risk surfaces detected — Sentinel reports only; human governance review required"
            )
        for surface_id in classified_surfaces:
            if not SURFACE_TEST_MAP.get(surface_id):
                coverage_gaps.append(f"No regression tests mapped to surface '{surface_id}'")

    # Filter to tests that actually exist on disk
    existing_tests = [t for t in tests_selected if (REPO_ROOT / t).exists()]
    missing_tests = [t for t in tests_selected if t not in existing_tests]
    for mt in missing_tests:
        coverage_gaps.append(f"Regression test file not found on disk: {mt}")

    # Run the tests
    zero_counts = {"passed": 0, "failed": 0, "errors": 0, "skipped": 0}
    pytest_result: dict = {
        "exit_code": -1,
        "stdout": "",
        "stderr": "No tests run",
        "passed": True,
        "test_counts": dict(zero_counts),
    }
    test_counts: dict = dict(zero_counts)
    issues_found: list[str] = []

    if existing_tests:
        print(f"[SENTINEL] Running {len(existing_tests)} test file(s)…")
        pytest_result = _run_pytest(existing_tests)
        test_counts = pytest_result.get("test_counts") or dict(zero_counts)

        if not pytest_result["passed"]:
            issues_found.append(
                f"Pytest exit code {pytest_result['exit_code']} — "
                f"{test_counts['failed']} failed, {test_counts['errors']} errors"
            )
            # Extract FAILED lines for detail
            for line in pytest_result["stdout"].splitlines():
                if line.startswith("FAILED"):
                    issues_found.append(line.strip())
    else:
        coverage_gaps.append("No existing test files found for selected scope — no tests executed")

    # Escalation check
    escalation_required = _determine_escalation(classified_surfaces) or bool(issues_found)

    # Escaped-defect pack status
    pack = _load_escaped_defects_pack()
    defect_pack_status = {
        dc: {
            "guard_type": meta.get("guard_type", "unknown"),
            "status": meta.get("status", "unknown"),
            "test_file": meta.get("test_file", ""),
        }
        for dc, meta in pack.get("defect_classes", {}).items()
    }

    report = {
        "sentinel_version": "1.0.0-phase1",
        "run_id": run_id,
        "utc": utc_now,
        "trigger_type": trigger_type,
        "branch": branch,
        "changed_files": changed_files or [],
        "classified_files": classified_files_detail,
        "classified_surfaces": classified_surfaces,
        "tests_selected": tests_selected,
        "tests_run": existing_tests,
        "test_counts": test_counts,
        "pytest_exit_code": pytest_result["exit_code"],
        "issues_found": issues_found,
        "coverage_gaps": coverage_gaps,
        "escaped_defect_pack_status": defect_pack_status,
        "governance_escalation_required": escalation_required,
        "auto_remediation_attempted": False,
        "sentinel_note": "Phase 1 — report only. No product code or governed assets were modified.",
    }

    # Write report
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORTS_DIR / f"sentinel_run_{run_id}.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print(f"[SENTINEL] Report written: {report_path}")
    print(f"[SENTINEL] Issues found: {len(issues_found)} | Coverage gaps: {len(coverage_gaps)}")
    print(f"[SENTINEL] Governance escalation required: {escalation_required}")

    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="HealthIQ AI Phase 1 Sentinel — report-only quality runner")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--changed-files", nargs="+", metavar="PATH", help="List of changed file paths to classify and check")
    group.add_argument("--surface", metavar="SURFACE", help="Specific surface to check (e.g. parser/alias/canonical)")
    group.add_argument("--defect-class", metavar="CLASS", help="Named defect class (e.g. ggt_alias_miss)")
    group.add_argument("--all", dest="run_all", action="store_true", help="Run full escaped-defect regression pack")
    args = parser.parse_args()

    report = run(
        changed_files=args.changed_files,
        surface=args.surface,
        defect_class=args.defect_class,
        run_all=args.run_all,
    )

    all_pass = not report["issues_found"] and not any(
        v.get("status") == "FAIL" for v in report["escaped_defect_pack_status"].values()
    )
    sys.exit(0 if all_pass else 1)


if __name__ == "__main__":
    # Ensure sentinel/ is on the path so `from classifier import` works
    sys.path.insert(0, str(Path(__file__).parent))
    main()
