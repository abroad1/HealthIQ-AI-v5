#!/usr/bin/env python3
"""
ARCH-CONV-CORRECT-1 — re-run of the 13 ARCH-CONV-FINAL-AUDIT end-to-end scenarios.

The final audit executed these 13 Layer B scenarios ad hoc and reported 13/13 PASS at its
baseline SHA. They are reproduced here as an executable harness so the correction package can
prove none of them regressed.

Scenario numbering follows the table in
``docs/architecture/ARCH-CONV-FINAL_end_to_end_pipeline_and_leakage_report.md``.

Exit code 0 = all scenarios PASS.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parents[2]
BACKEND = REPO_ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

RANGES = {
    "homocysteine": {"min": 5.0, "max": 15.0},
    "mcv": {"min": 80.0, "max": 96.0},
    "folate": {"min": 3.9, "max": 26.8},
    "vitamin_b12": {"min": 197.0, "max": 771.0},
    "active_b12": {"min": 37.5, "max": 188.0},
    "ggt": {"min": 10.0, "max": 71.0},
    "alt": {"min": 0.0, "max": 41.0},
    "egfr": {"min": 90.0, "max": 120.0},
    "creatinine": {"min": 59.0, "max": 104.0},
    "vitamin_d": {"min": 75.0, "max": 200.0},
    "free_t3": {"min": 3.1, "max": 6.8},
    "tpo_ab": {"min": 0.0, "max": 34.0},
}

RESULTS: List[Tuple[int, str, str, str]] = []


def _row(signal_id: str, source_spec_id: str, metric: str, *, state: str = "at_risk", conf: float = 0.8):
    return {
        "signal_id": signal_id,
        "activation_key": f"{signal_id}::{source_spec_id}",
        "source_spec_id": source_spec_id,
        "signal_state": state,
        "confidence": conf,
        "primary_metric": metric,
    }


def _compile(rows: List[Dict[str, Any]], context: Dict[str, Any]):
    from core.analytics.root_cause_compiler_v1 import compile_root_cause_v1

    return compile_root_cause_v1(
        signal_results=rows,
        biomarker_context=context,
        input_reference_ranges=RANGES,
    )


def _hyp_ids(root, activation_key: Optional[str] = None) -> set:
    if root is None:
        return set()
    out = set()
    for finding in root.findings:
        if activation_key and finding.activation_key != activation_key:
            continue
        out |= {h.hypothesis_id for h in finding.hypotheses}
    return out


def _summaries(root) -> str:
    if root is None:
        return ""
    return " ".join(
        f"{h.title} {h.summary}" for f in root.findings for h in f.hypotheses
    ).lower()


def record(number: int, name: str, ok: bool, detail: str) -> None:
    RESULTS.append((number, name, "PASS" if ok else "FAIL", detail))


def scenario_1() -> None:
    key = "signal_homocysteine_high::inv_homocysteine_high_metabolic"
    root = _compile([_row("signal_homocysteine_high", "inv_homocysteine_high_metabolic", "homocysteine")], {"homocysteine": {"value": 22.0}})
    record(1, "Rejected hcy metabolic", root is None, f"compile_root_cause_v1 -> {None if root is None else 'findings'} for {key}")


def scenario_2() -> None:
    key = "signal_homocysteine_high::inv_homocysteine_high_b_vitamin_related_methylation_impairment"
    root = _compile(
        [_row("signal_homocysteine_high", "inv_homocysteine_high_b_vitamin_related_methylation_impairment", "homocysteine")],
        {"homocysteine": {"value": 18.0}, "folate": {"value": 2.0}},
    )
    ids = _hyp_ids(root, key)
    ok = ids == {
        "hyp_folate_related_hyperhomocysteinemia",
        "hyp_b12_related_or_combined_methylation_impairment",
    } and "methylation capacity" not in _summaries(root)
    record(2, "Hcy B-vitamin compiled only", ok, f"hyps={sorted(ids)}")


def scenario_3() -> None:
    key = "signal_homocysteine_high::inv_homocysteine_high_renal_clearance_reduction"
    root = _compile(
        [_row("signal_homocysteine_high", "inv_homocysteine_high_renal_clearance_reduction", "homocysteine")],
        {"homocysteine": {"value": 20.0}, "egfr": {"value": 55.0}, "creatinine": {"value": 130.0}},
    )
    ids = _hyp_ids(root, key)
    text = _summaries(root)
    ok = bool(ids) and "chronic kidney disease" not in text
    record(3, "Hcy renal, no CKD diagnosis", ok, f"hyps={sorted(ids)}")


def scenario_4() -> None:
    key = "signal_mcv_high::inv_mcv_high_macrocytosis"
    root = _compile([_row("signal_mcv_high", "inv_mcv_high_macrocytosis", "mcv")], {"mcv": {"value": 99.5}})
    ids = _hyp_ids(root, key)
    roles = {f.activation_key: f.why_role for f in (root.findings if root else [])}
    ok = ids == {"mcv_high_anchor_pattern_v1"} and roles.get(key) == "morphology_context"
    record(4, "MCV anchor morphology only", ok, f"hyps={sorted(ids)} role={roles.get(key)}")


def scenario_5() -> None:
    key = "signal_mcv_high::inv_mcv_high_megaloblastic_macrocytosis"
    root = _compile(
        [_row("signal_mcv_high", "inv_mcv_high_megaloblastic_macrocytosis", "mcv")],
        {"mcv": {"value": 101.0}, "folate": {"value": 2.1}, "vitamin_b12": {"value": 180.0}},
    )
    ids = _hyp_ids(root, key)
    ok = bool(ids) and not any("hepatic" in i or "alcohol" in i for i in ids)
    record(5, "MCV megaloblastic supported", ok, f"hyps={sorted(ids)}")


def scenario_6() -> None:
    key = "signal_mcv_high::inv_mcv_high_nonmegaloblastic_macrocytosis"
    root = _compile(
        [_row("signal_mcv_high", "inv_mcv_high_nonmegaloblastic_macrocytosis", "mcv")],
        {"mcv": {"value": 101.0}, "ggt": {"value": 120.0}, "alt": {"value": 60.0}},
    )
    ids = _hyp_ids(root, key)
    text = _summaries(root)
    ok = bool(ids) and "marrow disorder" not in text
    record(6, "MCV non-megaloblastic evidence-gated", ok, f"hyps={sorted(ids)}")


def scenario_7() -> None:
    key = "signal_free_t3_low::inv_free_t3_low_low_t3_syndrome"
    root = _compile([_row("signal_free_t3_low", "inv_free_t3_low_low_t3_syndrome", "free_t3")], {"free_t3": {"value": 2.5}})
    ids = _hyp_ids(root, key)
    text = _summaries(root)
    ok = bool(ids) and "prescrib" not in text and "start treatment" not in text
    record(7, "Free T3 low NTI pattern", ok, f"hyps={sorted(ids)}")


def scenario_8() -> None:
    key = "signal_tpo_ab_high::inv_tpo_ab_high_autoimmune_hypothyroid_pattern"
    root = _compile(
        [_row("signal_tpo_ab_high", "inv_tpo_ab_high_autoimmune_hypothyroid_pattern", "tpo_ab")],
        {"tpo_ab": {"value": 300.0}, "tsh": {"value": 6.5}},
    )
    record(8, "TPO autoimmune hypothyroid pattern", bool(_hyp_ids(root, key)), f"hyps={sorted(_hyp_ids(root, key))}")


def scenario_9() -> None:
    key = "signal_tpo_ab_high::inv_tpo_ab_high_euthyroid_autoimmune_risk"
    root = _compile(
        [_row("signal_tpo_ab_high", "inv_tpo_ab_high_euthyroid_autoimmune_risk", "tpo_ab")],
        {"tpo_ab": {"value": 200.0}, "tsh": {"value": 2.0}},
    )
    ids = _hyp_ids(root, key)
    text = _summaries(root)
    ok = bool(ids) and "you have hypothyroidism" not in text
    record(9, "TPO euthyroid risk, no present-disease claim", ok, f"hyps={sorted(ids)}")


def scenario_10() -> None:
    from core.analytics.signal_evaluator import SignalRegistry

    registry = SignalRegistry()
    blocked_present = any(
        "kb47" in str(row.get("package") or row.get("package_id") or "")
        for row in registry.excluded_launch_critical_packages
    )
    loaded_dhea = [
        key for key in registry._signals_by_activation_key if "dhea" in key.lower()
    ]
    record(
        10,
        "Provenance-blocked packages unreachable",
        bool(registry.excluded_launch_critical_packages) and not loaded_dhea,
        f"excluded={len(registry.excluded_launch_critical_packages)} dhea_loaded={loaded_dhea}",
    )
    del blocked_present


def scenario_11() -> None:
    key = "signal_vitamin_d_low::inv_vitamin_d_low_deficiency"
    root = _compile([_row("signal_vitamin_d_low", "inv_vitamin_d_low_deficiency", "vitamin_d")], {"vitamin_d": {"value": 32.0}})
    finding = next((f for f in (root.findings if root else []) if f.activation_key == key), None)
    ok = (
        finding is not None
        and finding.authority_scope == "frame_specific"
        and "25-hydroxyvitamin D" in finding.hypotheses[0].summary
    )
    record(11, "Vitamin D compiled, legacy retired", ok, "compiled summary_template wording present" if ok else "compiled path not selected")


def scenario_12() -> None:
    from core.knowledge.why_authority_v1 import resolve_frame_why_authority

    mode, _ = resolve_frame_why_authority(signal_id="signal_homocysteine_high", activation_key="")
    fail_closed = False
    try:
        _compile(
            [
                {
                    "signal_id": "signal_homocysteine_high",
                    "signal_state": "at_risk",
                    "confidence": 0.7,
                    "primary_metric": "homocysteine",
                }
            ],
            {"homocysteine": {"value": 18.0}},
        )
    except ValueError:
        fail_closed = True
    record(12, "Ambiguous bare multi-frame hcy fails closed", mode == "fail_closed" and fail_closed, f"mode={mode} raised={fail_closed}")


def scenario_13() -> None:
    from core.knowledge.why_authority_v1 import resolve_frame_why_authority

    mode, row = resolve_frame_why_authority(signal_id="signal_vitamin_d_low", activation_key="")
    record(13, "Single-frame vitamin D empty-key compatibility", mode == "compiled" and bool(row), f"mode={mode}")


def main() -> int:
    for scenario in (
        scenario_1,
        scenario_2,
        scenario_3,
        scenario_4,
        scenario_5,
        scenario_6,
        scenario_7,
        scenario_8,
        scenario_9,
        scenario_10,
        scenario_11,
        scenario_12,
        scenario_13,
    ):
        try:
            scenario()
        except Exception as exc:  # noqa: BLE001 — a raising scenario is a scenario failure
            RESULTS.append((int(scenario.__name__.split("_")[-1]), scenario.__name__, "FAIL", f"raised {exc!r}"))

    failures = [r for r in RESULTS if r[2] != "PASS"]
    for number, name, status, detail in sorted(RESULTS):
        print(f"{number:>2}. [{status}] {name} — {detail}")
    print("")
    print(f"score: {len(RESULTS) - len(failures)}/{len(RESULTS)} PASS")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
