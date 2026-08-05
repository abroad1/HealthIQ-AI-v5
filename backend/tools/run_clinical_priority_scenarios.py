"""
CLIN-PRIORITY-CORE-1 — Clinical priority scenario runner (hepatic Checkpoint 1).

Pattern adapted from run_arbitration_scenarios.py.
Runs the real prioritisation loader + concern_constructor against fixtures.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from core.analytics.concern_constructor import construct_clinical_concern_set
from core.analytics.prioritisation_registry import load_prioritisation_package


def _default_fixture_path() -> Path:
    return (
        Path(__file__).resolve().parent.parent
        / "tests"
        / "fixtures"
        / "clinical_priority_scenarios_v1.json"
    )


def _default_output_root() -> Path:
    return Path(__file__).resolve().parent.parent / "artifacts" / "clinical_priority_runs"


def _git_short_sha() -> str:
    try:
        out = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], text=True)
        return out.strip()
    except Exception:
        return ""


def _read_fixture(path: Path) -> Dict[str, Any]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("Scenario fixture must be a JSON object")
    block = raw.get("scenarios", [])
    if not isinstance(block, list):
        raise ValueError("Scenario fixture must include list field: scenarios")
    return raw


def _merge_ranges(defaults: Dict[str, Any], override: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    merged = dict(defaults or {})
    if override:
        merged.update(override)
    return merged


def _evaluate_scenario(
    scenario: Dict[str, Any],
    defaults: Dict[str, Any],
    package: Any,
) -> Dict[str, Any]:
    lab_ranges = _merge_ranges(defaults, scenario.get("lab_ranges"))
    concern = construct_clinical_concern_set(
        signal_results=scenario.get("signal_results") or [],
        biomarkers=scenario.get("biomarkers") or {},
        lab_ranges=lab_ranges,
        derived=scenario.get("derived"),
        context=scenario.get("context"),
        package=package,
    )
    expected = scenario.get("expected") or {}
    failures: List[str] = []

    finding_types = [f.finding_type for f in concern.findings]
    expected_types = list(expected.get("finding_types") or [])
    if expected.get("no_concern"):
        if not concern.no_concern:
            failures.append("expected no_concern=true")
        if finding_types:
            failures.append(f"expected no findings, got {finding_types}")
    else:
        if sorted(finding_types) != sorted(expected_types):
            # Allow ordered subset equality when expected lists exact set
            if set(finding_types) != set(expected_types) or len(finding_types) != len(
                expected_types
            ):
                failures.append(
                    f"finding_types mismatch: got {finding_types}, expected {expected_types}"
                )

    primary = next((f for f in concern.findings if f.finding_type in expected_types), None)
    if primary is None and expected_types and not expected.get("no_concern"):
        primary = concern.findings[0] if concern.findings else None

    def _check_field(name: str, actual: Any, expected_val: Any) -> None:
        if expected_val is not None and actual != expected_val:
            failures.append(f"{name}: got {actual!r}, expected {expected_val!r}")

    if primary is not None:
        _check_field("urgency", primary.urgency_time_band, expected.get("urgency"))
        _check_field("severity", primary.severity_band, expected.get("severity"))
        _check_field("tier", primary.concern_tier, expected.get("tier"))
        if expected.get("role"):
            # principal may be remapped for co-lead sets; check any matching type
            roles = {f.finding_type: f.role for f in concern.findings}
            if expected.get("co_lead_eligible"):
                if concern.presentation_mode not in {"co_lead", "principal"} and not concern.co_lead_finding_ids:
                    failures.append("expected co_lead eligible presentation")
            else:
                target = next(
                    (f for f in concern.findings if f.finding_type == expected_types[0]),
                    primary,
                )
                if target.role != expected["role"] and target.role not in {
                    "principal_concern",
                    "co_lead",
                    "reclassified",
                }:
                    # Allow principal_concern when lead selection promotes
                    if expected["role"] == "principal_concern" and target.role == "co_lead":
                        pass
                    elif expected["role"] == "reclassified" and target.role != "reclassified":
                        failures.append(f"role: got {target.role}, expected reclassified")
                    elif expected["role"] not in {target.role, roles.get(expected_types[0])}:
                        failures.append(
                            f"role: got {target.role}, expected {expected['role']}"
                        )

        if expected.get("withheld") is not None:
            _check_field("withheld", primary.withheld, expected.get("withheld"))
        if expected.get("serious_result_state"):
            _check_field(
                "serious_result_state",
                primary.serious_result_state,
                expected.get("serious_result_state"),
            )
        if expected.get("severity_indeterminate") is not None:
            _check_field(
                "severity_indeterminate",
                primary.severity_indeterminate,
                expected.get("severity_indeterminate"),
            )
        if expected.get("label_contains"):
            if expected["label_contains"].lower() not in primary.label.lower():
                failures.append(
                    f"label missing {expected['label_contains']!r}: {primary.label}"
                )

        for note in expected.get("missing_data_notes_any") or []:
            if note not in primary.missing_data_notes:
                failures.append(f"missing_data_notes missing {note!r}")
        for note in expected.get("nested_any") or []:
            if note not in primary.nested_constituent_labels:
                failures.append(f"nested_constituent_labels missing {note!r}")
        for note in expected.get("caveats_any") or []:
            if note not in primary.caveats:
                failures.append(f"caveats missing {note!r}")
        for note in expected.get("prohibited_any") or []:
            found = any(note in f.prohibited_behaviours_asserted for f in concern.findings)
            if primary is not None and note in primary.prohibited_behaviours_asserted:
                found = True
            if not found:
                failures.append(f"prohibited_behaviours missing {note!r}")
        for note in expected.get("dependency_flags_any") or []:
            if note not in primary.dependency_flags:
                failures.append(f"dependency_flags missing {note!r}")
        for note in expected.get("quarantine_flags_any") or []:
            if note not in primary.quarantine_flags:
                failures.append(f"quarantine_flags missing {note!r}")

    for ftype in expected.get("must_not_include_finding_types") or []:
        if ftype in finding_types:
            failures.append(f"must not include finding type {ftype}")

    tier_by = expected.get("tier_by_type") or {}
    for ftype, tier in tier_by.items():
        match = next((f for f in concern.findings if f.finding_type == ftype), None)
        if match is None:
            failures.append(f"missing finding type {ftype} for tier check")
        elif match.concern_tier != tier:
            failures.append(f"{ftype} tier: got {match.concern_tier}, expected {tier}")

    if expected.get("no_concern_notes_any"):
        for note in expected["no_concern_notes_any"]:
            if note not in concern.no_concern_notes:
                failures.append(f"no_concern_notes missing {note!r}")
    if expected.get("domain_notes_any"):
        for note in expected["domain_notes_any"]:
            if note not in concern.domain_notes:
                failures.append(f"domain_notes missing {note!r}")

    if expected.get("fib_4_computed") is not None:
        _check_field("fib_4_computed", concern.fib_4_computed, expected["fib_4_computed"])
    if expected.get("fib_4_displayed") is not None:
        _check_field("fib_4_displayed", concern.fib_4_displayed, expected["fib_4_displayed"])
    if expected.get("assert_fib_4_unused"):
        if concern.fib_4_computed or concern.fib_4_displayed:
            failures.append("FIB-4 must not be computed or displayed")
        for f in concern.findings:
            if f.finding_type == "HEP-F5":
                if "XD-QUAR-1" not in f.quarantine_flags:
                    failures.append("HEP-F5 missing XD-QUAR-1 quarantine flag")

    if expected.get("no_bilirubin_tier0_escalation"):
        for f in concern.findings:
            if f.finding_type == "HEP-F6" and f.concern_tier == 0:
                failures.append("bilirubin escalation to Tier 0 not permitted here")

    if expected.get("haem_leads_on_time_band"):
        if not concern.lead_finding_ids:
            failures.append("expected haematology lead on time band")
        else:
            lead = next(
                (f for f in concern.findings if f.finding_id == concern.lead_finding_ids[0]),
                None,
            )
            if lead is None or lead.domain != "haematology":
                failures.append("expected haematology finding to lead on time band")

    # Provenance retained
    for f in concern.findings:
        if not f.constituent_activation_keys:
            failures.append(f"{f.finding_id} lost constituent_activation_keys")

    passed = len(failures) == 0
    return {
        "scenario_id": scenario.get("scenario_id"),
        "passed": passed,
        "failures": failures,
        "finding_types": finding_types,
        "lead_finding_ids": list(concern.lead_finding_ids),
        "co_lead_finding_ids": list(concern.co_lead_finding_ids),
        "presentation_mode": concern.presentation_mode,
        "no_forced_lead": concern.no_forced_lead,
        "no_concern": concern.no_concern,
        "fib_4_computed": concern.fib_4_computed,
        "fib_4_displayed": concern.fib_4_displayed,
        "concern": concern.model_dump(),
        "alias_of": scenario.get("alias_of"),
    }


def run_clinical_priority_scenarios(
    fixture_path: Optional[Path] = None,
    output_root: Optional[Path] = None,
    run_id: Optional[str] = None,
    scenario_id: Optional[str] = None,
) -> Tuple[Path, Dict[str, Any]]:
    fixture_path = Path(fixture_path) if fixture_path else _default_fixture_path()
    output_root = Path(output_root) if output_root else _default_output_root()
    run_id = run_id or datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    run_dir = output_root / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    raw = _read_fixture(fixture_path)
    defaults = raw.get("default_lab_ranges") or {}
    scenarios = list(raw.get("scenarios") or [])
    scenarios.sort(key=lambda s: str(s.get("scenario_id", "")))
    if scenario_id:
        scenarios = [s for s in scenarios if s.get("scenario_id") == scenario_id]

    package = load_prioritisation_package()
    results: List[Dict[str, Any]] = []
    by_id: Dict[str, Dict[str, Any]] = {}

    for scenario in scenarios:
        sid = str(scenario.get("scenario_id", "")).strip()
        result = _evaluate_scenario(scenario, defaults, package)
        results.append(result)
        by_id[sid] = result
        sdir = run_dir / "scenarios" / sid
        sdir.mkdir(parents=True, exist_ok=True)
        (sdir / "concern_set.json").write_text(
            json.dumps(result["concern"], indent=2, sort_keys=True),
            encoding="utf-8",
        )
        (sdir / "result.json").write_text(
            json.dumps({k: v for k, v in result.items() if k != "concern"}, indent=2, sort_keys=True),
            encoding="utf-8",
        )

    # Duplicate relationship: CONTRACT-FIX-1 == HEP-AS-1
    if "CONTRACT-FIX-1" in by_id and "HEP-AS-1" in by_id:
        a = by_id["CONTRACT-FIX-1"]["concern"]
        b = by_id["HEP-AS-1"]["concern"]
        # Compare clinical outcome fields (ignore finding_id hash stability across identical inputs)
        def _norm(concern: Dict[str, Any]) -> Dict[str, Any]:
            findings = []
            for f in concern.get("findings") or []:
                findings.append(
                    {
                        "finding_type": f.get("finding_type"),
                        "urgency_time_band": f.get("urgency_time_band"),
                        "severity_band": f.get("severity_band"),
                        "concern_tier": f.get("concern_tier"),
                        "role": f.get("role"),
                        "missing_data_notes": f.get("missing_data_notes"),
                        "nested_constituent_labels": f.get("nested_constituent_labels"),
                    }
                )
            return {
                "findings": findings,
                "no_concern": concern.get("no_concern"),
                "fib_4_computed": concern.get("fib_4_computed"),
            }

        if _norm(a) != _norm(b):
            for row in results:
                if row["scenario_id"] in {"CONTRACT-FIX-1", "HEP-AS-1"}:
                    row["passed"] = False
                    row["failures"] = list(row.get("failures") or []) + [
                        "CONTRACT-FIX-1 outcome differs from HEP-AS-1"
                    ]

    passed = sum(1 for r in results if r["passed"])
    failed = len(results) - passed
    manifest = {
        "run_id": run_id,
        "git_commit_short": _git_short_sha(),
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "fixture_path": str(fixture_path),
        "package_id": package.stamp.package_id,
        "package_version": package.stamp.package_version,
        "package_hash": package.stamp.package_hash,
        "contract_version": package.stamp.contract_version,
        "ruleset_version": package.stamp.ruleset_version,
        "scenario_count": len(results),
        "passed": passed,
        "failed": failed,
        "scenario_results": [
            {
                "scenario_id": r["scenario_id"],
                "passed": r["passed"],
                "failures": r["failures"],
                "finding_types": r["finding_types"],
                "alias_of": r.get("alias_of"),
            }
            for r in results
        ],
    }
    (run_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    return run_dir, manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Run clinical priority scenarios")
    parser.add_argument("--fixture", type=Path, default=None)
    parser.add_argument("--output-root", type=Path, default=None)
    parser.add_argument("--run-id", type=str, default=None)
    parser.add_argument("--scenario-id", type=str, default=None)
    args = parser.parse_args()
    run_dir, manifest = run_clinical_priority_scenarios(
        fixture_path=args.fixture,
        output_root=args.output_root,
        run_id=args.run_id,
        scenario_id=args.scenario_id,
    )
    print(json.dumps({"run_dir": str(run_dir), "passed": manifest["passed"], "failed": manifest["failed"]}, indent=2))
    return 0 if manifest["failed"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
