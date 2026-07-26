#!/usr/bin/env python3
"""
ARCH-CONV-CORRECT-1 — deterministic replay of the audited live UAT case.

Replays the panel recorded for ``analysis_id=e34aaedf-b09f-42f0-8cc8-4653a00b4c10`` in
``docs/testing/ARCH-CONV-FINAL_frontend_end_to_end_uat.md`` through Layer B and the report
assembly boundary, and prints the surfaces the final audit flagged as ACTIVE_LEAK:

- fired activation keys;
- ``report_v1.top_findings`` activation keys;
- intervention ``activation_key_refs`` / ``signal_refs``;
- root-cause findings with their governed ``why_role``;
- a retired-wording fingerprint over the whole assembled payload.

``--baseline`` reproduces pre-correction behaviour by disabling the canonical frame runtime
authority, so the before/after delta can be recorded from one script. Baseline mode is for
evidence only and must never be used by a gate.

No credentials and no network access: the panel values come from the committed UAT artefact.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

REPO_ROOT = Path(__file__).resolve().parents[2]
BACKEND = REPO_ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

ANALYSIS_ID = "e34aaedf-b09f-42f0-8cc8-4653a00b4c10"
REJECTED_KEY = "signal_homocysteine_high::inv_homocysteine_high_metabolic"
RETIRED_PHRASES = ("methylation capacity", "methylation pathway pattern")

LAB_RANGES: Dict[str, Dict[str, float]] = {
    "homocysteine": {"min": 5.0, "max": 15.0},
    "mcv": {"min": 80.0, "max": 96.0},
    "folate": {"min": 3.9, "max": 26.8},
    "vitamin_b12": {"min": 197.0, "max": 771.0},
    "active_b12": {"min": 37.5, "max": 188.0},
    "ggt": {"min": 10.0, "max": 71.0},
    "alt": {"min": 0.0, "max": 41.0},
    "egfr": {"min": 90.0, "max": 120.0},
    "creatinine": {"min": 59.0, "max": 104.0},
}

#: Values as rendered on the audited results page.
UAT_PANEL: Dict[str, float] = {
    "homocysteine": 16.2,
    "mcv": 99.5,
    "folate": 7.7,
    "vitamin_b12": 336.0,
    "active_b12": 139.2,
    "ggt": 30.0,
    "alt": 22.0,
    "egfr": 84.0,
    "creatinine": 90.0,
}


def _disable_runtime_authority() -> None:
    """Baseline mode: pretend every frame is runtime-eligible (pre-correction behaviour)."""
    from core.knowledge import frame_runtime_authority_v1 as authority

    authority.rejected_activation_keys.cache_clear()
    authority.is_frame_runtime_eligible = lambda activation_key: True  # type: ignore[assignment]
    authority.frame_runtime_exclusion_reason = lambda activation_key: None  # type: ignore[assignment]
    authority.filter_runtime_eligible_rows = lambda rows: list(rows or [])  # type: ignore[assignment]

    # Rebind the names already imported by consumers.
    from core.analytics import insight_graph_builder, signal_evaluator

    insight_graph_builder.filter_runtime_eligible_rows = authority.filter_runtime_eligible_rows
    signal_evaluator.filter_runtime_eligible_rows = authority.filter_runtime_eligible_rows
    signal_evaluator.frame_runtime_exclusion_reason = authority.frame_runtime_exclusion_reason


def _fired_rows(baseline: bool) -> List[Dict[str, Any]]:
    from core.analytics.signal_evaluator import SignalEvaluator, SignalRegistry

    rows = [
        r.model_dump()
        for r in SignalEvaluator(SignalRegistry()).evaluate_all(UAT_PANEL, {}, lab_ranges=LAB_RANGES)
    ]
    if baseline and not any(str(r.get("activation_key") or "") == REJECTED_KEY for r in rows):
        # The rejected frame is excluded at registry load; re-inject it so baseline mode shows
        # the surfaces the final audit observed.
        rows.append(
            {
                "signal_id": "signal_homocysteine_high",
                "activation_key": REJECTED_KEY,
                "source_spec_id": "inv_homocysteine_high_metabolic",
                "signal_state": "suboptimal",
                "confidence": 0.92,
                "primary_metric": "homocysteine",
                "system": "vascular",
                "interpretation": "Reflects methylation capacity and B-vitamin status.",
            }
        )
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--baseline",
        action="store_true",
        help="disable the canonical frame runtime authority to reproduce pre-correction output",
    )
    args = parser.parse_args()

    if args.baseline:
        _disable_runtime_authority()

    from core.analytics.insight_graph_builder import build_insight_graph_v1
    from core.analytics.root_cause_compiler_v1 import compile_root_cause_v1

    rows = _fired_rows(args.baseline)
    graph = build_insight_graph_v1(
        analysis_id=ANALYSIS_ID,
        scoring_result={},
        clustering_result={"clusters": []},
        input_reference_ranges=LAB_RANGES,
        filtered_biomarkers={k: {"value": v} for k, v in UAT_PANEL.items()},
        signal_results=rows,
    )
    root = compile_root_cause_v1(
        signal_results=graph.signal_results,
        biomarker_context={k: {"value": v} for k, v in UAT_PANEL.items()},
        input_reference_ranges=LAB_RANGES,
    )

    payload = graph.model_dump_json()
    if root is not None:
        payload += root.model_dump_json()

    mode = "BASELINE (authority disabled)" if args.baseline else "CORRECTED"
    print(f"analysis_id={ANALYSIS_ID}  mode={mode}")
    print("")

    fired = sorted(str(r.get("activation_key") or "") for r in graph.signal_results)
    print("fired activation keys:")
    for key in fired:
        print(f"  {key}{'   <-- REJECTED' if key == REJECTED_KEY else ''}")

    top = [
        (f.priority_rank, f.signal_id, getattr(f, "activation_key", ""))
        for f in (graph.report_v1.top_findings if graph.report_v1 else [])
    ]
    print("\nreport_v1.top_findings:")
    for rank, signal_id, key in top:
        print(f"  #{rank} {signal_id} {key}{'   <-- REJECTED' if key == REJECTED_KEY else ''}")

    print("\ninterventions_v1 references:")
    for iv in graph.interventions_v1 or []:
        refs = iv.get("activation_key_refs") or []
        print(f"  {iv.get('intervention_id')} signal_refs={iv.get('signal_refs')} activation_key_refs={refs}")

    print("\nroot_cause_v1 findings (activation_key / why_role / hypotheses):")
    for finding in (root.findings if root else []):
        hyp_ids = [h.hypothesis_id for h in finding.hypotheses]
        print(f"  {finding.activation_key or finding.signal_id} role={finding.why_role} hyps={hyp_ids}")

    print("\nretired-wording fingerprint over assembled payload:")
    lowered = payload.lower()
    for phrase in RETIRED_PHRASES:
        hit = phrase in lowered
        print(f"  {phrase!r}: {'ACTIVE_LEAK' if hit else 'absent'}")

    print("\nprimary_driver_v1 (Layer B lead projected for Layer C):")
    print(f"  {json.dumps(graph.primary_driver_v1, sort_keys=True) if graph.primary_driver_v1 else 'None'}")

    rejected_present = REJECTED_KEY in payload
    retired_present = any(phrase in lowered for phrase in RETIRED_PHRASES)
    print("")
    print(f"rejected_frame_present={rejected_present}  retired_wording_present={retired_present}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
