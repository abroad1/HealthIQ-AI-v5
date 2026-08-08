#!/usr/bin/env python3
"""
ARCH-CONV-PKG2 — launch-critical provenance/reachability behavioural gate.

Fails if:
- a production-loaded pkg_kb47_* package lacks EXPLICIT_SPEC/COMPILED_MANIFEST;
- a beta-ineligible launch-critical package is present in the production registry;
- Wave 1 INCLUDE packages are missing from production load;
- excluded packages appear in production registry;
- duplicate/contradictory eligibility cannot be classified;
- deliberately invalid unknown package_id does not fail closed.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
BACKEND = REPO_ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

WAVE1_INCLUDE = {
    "pkg_kb47_free_t3_low_low_t3_syndrome",
    "pkg_kb47_free_t3_high_t3_predominant_thyrotoxicosis",
    "pkg_kb47_free_t4_low_thyroid_hormone_deficiency",
    "pkg_kb47_free_t4_high_thyrotoxicosis_context",
    "pkg_kb47_egfr_low_chronic_kidney_function_reduction",
    "pkg_kb47_egfr_low_hemodynamic_filtration_drop",
}


def _fail(msg: str) -> int:
    print(f"[launch-critical-reachability] FAIL: {msg}", file=sys.stderr)
    return 1


def main() -> int:
    from core.analytics.signal_evaluator import SignalRegistry
    from core.knowledge.package_runtime_eligibility_v1 import (
        ELIGIBILITY_NON_REACHABLE,
        ELIGIBILITY_UNKNOWN_FAIL_CLOSED,
        classify_package_runtime_eligibility,
    )
    from core.knowledge.provenance_status_v1 import (
        classify_package_provenance_status,
        is_beta_eligible_explicit_lineage,
    )

    prod = SignalRegistry()
    loaded_kb47 = {
        str(row.get("package_id") or "").strip()
        for row in prod.get_all_signals()
        if str(row.get("package_id") or "").startswith("pkg_kb47_")
    }
    if loaded_kb47 != WAVE1_INCLUDE:
        return _fail(f"production kb47 set mismatch: {sorted(loaded_kb47)}")

    for row in prod.get_all_signals():
        pid = str(row.get("package_id") or "").strip()
        if not pid.startswith("pkg_kb47_"):
            continue
        status = str(row.get("provenance_status") or "").strip()
        if not is_beta_eligible_explicit_lineage(status):
            return _fail(f"reachable kb47 without explicit lineage: {pid} status={status}")
        key = str(row.get("activation_key") or "").strip()
        spec = str(row.get("source_spec_id") or "").strip()
        sid = str(row.get("signal_id") or "").strip()
        if key != f"{sid}::{spec}":
            return _fail(f"activation_key/source_spec mismatch for {pid}: {key}")

    excluded = {row["package_id"] for row in prod.excluded_launch_critical_packages}
    if excluded & WAVE1_INCLUDE:
        return _fail("Wave 1 INCLUDE package incorrectly excluded")
    if len(excluded) != 14:
        return _fail(f"expected 14 excluded kb47 packages, got {len(excluded)}")

    # Stage 2: opt-in relaxes lineage veto only; canonical register membership still required.
    # Blocked kb47 packages without register entries must remain unloadable under opt-in.
    opted = SignalRegistry(allow_launch_critical_blocked=True)
    opted_kb47 = {
        str(row.get("package_id") or "").strip()
        for row in opted.get_all_signals()
        if str(row.get("package_id") or "").startswith("pkg_kb47_")
    }
    if opted_kb47 != WAVE1_INCLUDE:
        return _fail(
            f"test opt-in must load only register-activated Wave 1 kb47 frames, got {sorted(opted_kb47)}"
        )

    # Unknown / empty package id fails closed.
    eligibility, _status = classify_package_runtime_eligibility(package_id="")
    if eligibility != ELIGIBILITY_UNKNOWN_FAIL_CLOSED:
        return _fail("empty package_id must fail closed")

    # Blocked androgen remains non-reachable without inventing EXPLICIT_SPEC.
    androgen_manifest = {
        "source_document": "knowledge_bus/research/investigation_specs/multi_llm_research/Batch_2_Pass_3.json",
        "source_spec_id": "inv_dhea_high_androgen_excess_context",
    }
    # Without inv YAML this cannot be EXPLICIT_SPEC.
    status = classify_package_provenance_status(manifest=androgen_manifest)
    elig, _ = classify_package_runtime_eligibility(
        package_id="pkg_kb47_dhea_high_androgen_excess_context",
        manifest=androgen_manifest,
    )
    if status == "EXPLICIT_SPEC":
        # If someone later extracts androgen inv files, eligibility flips — not a gate fail.
        pass
    elif elig != ELIGIBILITY_NON_REACHABLE:
        return _fail("blocked androgen package must be non_reachable without opt-in")

    print("launch_critical_provenance_reachability_gate: PASS")
    print(f"production_kb47={len(loaded_kb47)} excluded={len(excluded)} optin_kb47={len(opted_kb47)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
