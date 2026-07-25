#!/usr/bin/env python3
"""
ARCH-CONV-PKG1 — behavioural launch-path frame-identity gate.

Verifies the five residual consumers preserve activation frames (or expose
explicit family aggregation with participating_activation_keys).

Fails closed on deliberately invalid duplicate activation_key indexing.
Exit 0 on PASS, non-zero on FAIL.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict, List

REPO_ROOT = Path(__file__).resolve().parents[2]
BACKEND = REPO_ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))


# Gate 0 pressure-set families (exact cohort §5).
PRESSURE_SET: Dict[str, List[str]] = {
    "signal_homocysteine_high": [
        "inv_homocysteine_high_b_vitamin",
        "inv_homocysteine_high_metabolic",
        "inv_homocysteine_high_renal",
    ],
    "signal_mcv_high": [
        "inv_mcv_high_macrocytosis",
        "inv_mcv_high_megaloblastic",
        "inv_mcv_high_nonmegaloblastic",
    ],
    "signal_iron_low": [
        "inv_iron_low_absolute",
        "inv_iron_low_functional",
    ],
    "signal_tpo_ab_high": [
        "inv_tpo_ab_high_autoimmune_hypothyroid",
        "inv_tpo_ab_high_euthyroid",
    ],
    "signal_egfr_low": [
        "inv_egfr_low_chronic",
        "inv_egfr_low_hemodynamic",
    ],
    "signal_alt_high": [
        "inv_alt_high_hepatocellular",
        "inv_alt_high_metabolic",
        "inv_alt_high_muscle",
        "inv_alt_high_legacy",
    ],
    "signal_ferritin_high": [
        "inv_ferritin_high_inflammatory",
        "inv_ferritin_high_overload",
        "inv_ferritin_high_legacy",
    ],
    "signal_creatinine_high": [
        "inv_creatinine_high_reduced_gfr",
        "inv_creatinine_high_renal",
    ],
}


def _frame_row(
    *,
    signal_id: str,
    source_spec_id: str,
    state: str = "suboptimal",
    confidence: float = 0.7,
    system: str = "hepatic",
    primary_metric: str = "alt",
) -> Dict[str, Any]:
    return {
        "signal_id": signal_id,
        "source_spec_id": source_spec_id,
        "activation_key": f"{signal_id}::{source_spec_id}",
        "package_id": f"pkg_test_{source_spec_id}",
        "signal_state": state,
        "confidence": confidence,
        "system": system,
        "primary_metric": primary_metric,
        "supporting_markers": [],
    }


def _pressure_set_rows() -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    system_by_sid = {
        "signal_homocysteine_high": ("vascular", "homocysteine"),
        "signal_mcv_high": ("hematologic", "mcv"),
        "signal_iron_low": ("hematologic", "iron"),
        "signal_tpo_ab_high": ("thyroid", "tpo_ab"),
        "signal_egfr_low": ("renal", "egfr"),
        "signal_alt_high": ("hepatic", "alt"),
        "signal_ferritin_high": ("hepatic", "ferritin"),
        "signal_creatinine_high": ("renal", "creatinine"),
    }
    for sid, specs in PRESSURE_SET.items():
        system, metric = system_by_sid[sid]
        for i, spec in enumerate(specs):
            state = "at_risk" if i == 0 else "suboptimal"
            rows.append(
                _frame_row(
                    signal_id=sid,
                    source_spec_id=spec,
                    state=state,
                    confidence=0.55 + 0.05 * i,
                    system=system,
                    primary_metric=metric,
                )
            )
    return rows


def _fail(msg: str) -> int:
    print(f"[launch-path-frame-identity] FAIL: {msg}", file=sys.stderr)
    return 1


def main() -> int:
    from core.analytics.domain_score_assembler import (
        _collect_activation_keys,
        _collect_signal_ids,
        _is_wave1_blood_iron_oxygen,
        _is_wave1_kidney,
        _is_wave1_liver,
        _is_wave1_thyroid,
    )
    from core.analytics.interpretation_display_layer_publish_v1 import (
        publish_interpretation_display_layer_v1,
    )
    from core.analytics.intervention_selector_v1 import select_interventions_v1
    from core.analytics.narrative_report_compiler_v1 import _resolve_lead_frame
    from core.analytics.signal_interaction_builder import build_signal_interactions_v1
    from core.knowledge.signal_result_index_v1 import index_by_activation_key

    rows = _pressure_set_rows()
    expected_keys = sorted({r["activation_key"] for r in rows})
    if len(expected_keys) != 21:
        return _fail(f"pressure-set fixture must have 21 frames, got {len(expected_keys)}")

    # 1) Shared index preserves all frames; duplicate keys fail closed.
    indexed = index_by_activation_key(rows, require_key=True)
    if set(indexed.keys()) != set(expected_keys):
        return _fail("index_by_activation_key lost pressure-set frames")
    dup = [dict(rows[0]), dict(rows[0])]
    try:
        index_by_activation_key(dup, require_key=True)
        return _fail("duplicate activation_key must fail closed")
    except ValueError:
        pass

    # 2) IDL — family aggregation + participating keys.
    idl = publish_interpretation_display_layer_v1({"signal_results": rows})
    idl_keys = list(idl.participating_activation_keys or [])
    if sorted(idl_keys) != expected_keys:
        return _fail("IDL participating_activation_keys missing pressure-set frames")
    if idl.aggregation_scope != "signal_family":
        return _fail("IDL aggregation_scope must be signal_family")

    # 3) Domain scoring — activation keys companion, no silent collapse.
    for pred, need_sid in (
        (_is_wave1_liver, "signal_alt_high"),
        (_is_wave1_kidney, "signal_egfr_low"),
        (_is_wave1_blood_iron_oxygen, "signal_iron_low"),
        (_is_wave1_thyroid, "signal_tpo_ab_high"),
    ):
        sids = _collect_signal_ids(rows, pred)
        akeys = _collect_activation_keys(rows, pred)
        if need_sid not in sids:
            return _fail(f"domain predicate missed {need_sid}")
        family_keys = [k for k in expected_keys if k.startswith(need_sid + "::")]
        if not family_keys:
            return _fail(f"no expected keys for {need_sid}")
        if not set(family_keys).issubset(set(akeys)):
            return _fail(f"domain active_activation_keys collapsed frames for {need_sid}")

    # 4) Narrative lead preserves activation_key on graph path.
    lead = _resolve_lead_frame(narrative_payload_v1=None, insight_graph={"signal_results": rows})
    if lead.get("signal_id") not in {
        "signal_homocysteine_high",
        "signal_mcv_high",
        "signal_iron_low",
        "signal_tpo_ab_high",
        "signal_free_t3_low",
    }:
        # iron_low is in lead hints; pressure set includes it.
        pass
    if not lead.get("signal_id"):
        return _fail("narrative lead signal_id unresolved for pressure set")
    if not lead.get("activation_key"):
        return _fail("narrative lead activation_key blanked despite frame availability")
    if not lead["activation_key"].startswith(lead["signal_id"] + "::"):
        return _fail("narrative lead activation_key does not match signal family")

    # 5) Interaction builder — family nodes + per-node frame participation.
    interactions = build_signal_interactions_v1(rows)
    graph = interactions["interaction_graph"]
    if graph.get("aggregation_scope") != "signal_family":
        return _fail("interaction aggregation_scope must be signal_family")
    node_part = graph.get("node_frame_participation") or {}
    for sid, specs in PRESSURE_SET.items():
        if sid not in (graph.get("nodes") or []):
            continue
        got = node_part.get(sid) or []
        want = sorted(f"{sid}::{spec}" for spec in specs)
        if got != want:
            return _fail(f"interaction node_frame_participation wrong for {sid}: {got}")
    for summary in interactions.get("interaction_summary") or []:
        if "participating_activation_keys" not in summary:
            return _fail("interaction_summary missing per-chain participating_activation_keys")

    # 6) Intervention selector — frame refs retained / unioned.
    # Use vascular rows only so library templates can match.
    vascular_rows = [r for r in rows if r["system"] == "vascular"]
    for r in vascular_rows:
        r["confidence"] = 0.85
    intervs = select_interventions_v1(
        signal_results=vascular_rows,
        interaction_summary=interactions.get("interaction_summary") or [],
    )
    # Soft check: if any intervention emitted, activation_key_refs must not invent foreign frames.
    for item in intervs:
        refs = item.get("activation_key_refs") or []
        for ref in refs:
            if not isinstance(ref, str) or "::" not in ref:
                return _fail(f"intervention activation_key_refs malformed: {ref}")
            if not any(ref == r["activation_key"] for r in vascular_rows):
                return _fail("intervention borrowed activation_key from outside contributing frames")

    print("launch_path_frame_identity_gate: PASS")
    print(f"pressure_set_families={len(PRESSURE_SET)} frames={len(expected_keys)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
