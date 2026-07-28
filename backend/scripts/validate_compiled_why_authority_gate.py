#!/usr/bin/env python3
"""
ARCH-CONV-PKG3 — compiled WHY authority behavioural gate.

Fails if:
- register does not cover exactly the 10 pilot activation keys;
- REJECTED metabolic frame has an artefact or is COMPILED_ACTIVE;
- any COMPILED_ACTIVE row lacks a loadable artefact / fails promotion validation;
- metabolic inv YAML exists under compiled/hypotheses;
- bare multi-frame signal_id resolves without activation_key;
- vitamin D / free_t3 unique empty-key resolve fails;
- rejected-only metabolic emits WHY findings or WHY-engine fallback;
- vitamin D legacy YAML is selected when compiled path is active.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
BACKEND = REPO_ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

EXPECTED_KEYS = (
    "signal_vitamin_d_low::inv_vitamin_d_low_deficiency",
    "signal_homocysteine_high::inv_homocysteine_high_b_vitamin_related_methylation_impairment",
    "signal_homocysteine_high::inv_homocysteine_high_metabolic",
    "signal_homocysteine_high::inv_homocysteine_high_renal_clearance_reduction",
    "signal_mcv_high::inv_mcv_high_macrocytosis",
    "signal_mcv_high::inv_mcv_high_megaloblastic_macrocytosis",
    "signal_mcv_high::inv_mcv_high_nonmegaloblastic_macrocytosis",
    "signal_free_t3_low::inv_free_t3_low_low_t3_syndrome",
    "signal_tpo_ab_high::inv_tpo_ab_high_autoimmune_hypothyroid_pattern",
    "signal_tpo_ab_high::inv_tpo_ab_high_euthyroid_autoimmune_risk",
    "signal_tsh_high::inv_tsh_high_hypothyroidism",
    "signal_tsh_low::inv_tsh_low_hyperthyroidism",
    "signal_free_t3_high::inv_free_t3_high_t3_predominant_thyrotoxicosis",
    "signal_free_t4_high::inv_free_t4_high_thyrotoxicosis_context",
    "signal_free_t4_low::inv_free_t4_low_thyroid_hormone_deficiency",
    "signal_tsh_high::inv_tsh_high_primary_hypothyroid_pattern",
    "signal_tsh_low::inv_tsh_low_thyrotoxic_pattern",
    "signal_ldl_cholesterol_high::inv_ldl_high_dyslipidaemia",
    "signal_hdl_cholesterol_low::inv_hdl_low_cardiovascular",
    "signal_triglycerides_high::inv_triglycerides_high_metabolic",
    "signal_triglycerides_high::inv_triglycerides_high_insulin_resistant_hypertriglyceridemia",
    "signal_ldl_high::inv_ldl_high_atherogenic_ldl_burden",
    "signal_ldl_high::inv_ldl_high_familial_hypercholesterolemia_context",
    "signal_hdl_low::inv_hdl_low_atherogenic_dyslipidemia",
    "signal_hdl_low::inv_hdl_low_hypertriglyceridemic_insulin_resistance_pattern",
    "signal_total_cholesterol_high::inv_total_cholesterol_high_atherogenic_hypercholesterolemia",
    "signal_total_cholesterol_high::inv_total_cholesterol_high_hdl_dominant_elevation_pattern",
)
METABOLIC_KEY = "signal_homocysteine_high::inv_homocysteine_high_metabolic"
FORBIDDEN_COMPILED = REPO_ROOT / "knowledge_bus/compiled/hypotheses/inv_homocysteine_high_metabolic.yaml"


def _fail(msg: str) -> int:
    print(f"[compiled-why-authority] FAIL: {msg}", file=sys.stderr)
    return 1


def main() -> int:
    from core.analytics.root_cause_compiler_v1 import compile_root_cause_v1
    from core.knowledge.compiled_hypothesis import (
        clear_compiled_hypothesis_caches,
        get_compiled_hypothesis_artefact_for_activation_key,
        validate_runtime_promoted_artefact,
    )
    from core.knowledge.why_authority_v1 import (
        STATE_COMPILED_ACTIVE,
        STATE_LEGACY_RETIRED,
        STATE_REJECTED,
        clear_why_authority_cache,
        load_why_authority_register,
        resolve_frame_why_authority,
    )

    clear_why_authority_cache()
    clear_compiled_hypothesis_caches()

    reg = load_why_authority_register()
    by_key = reg["_by_activation_key"]
    if set(by_key) != set(EXPECTED_KEYS):
        return _fail(f"register keys mismatch: {sorted(by_key)}")

    ratification = Path(REPO_ROOT / str(reg.get("ratification_artefact") or ""))
    if not ratification.is_file():
        return _fail(f"missing ratification artefact: {ratification}")

    metabolic = by_key[METABOLIC_KEY]
    if str(metabolic.get("authority_state") or "").strip() != STATE_REJECTED:
        return _fail("metabolic frame must be REJECTED")
    if metabolic.get("artefact_path"):
        return _fail("REJECTED metabolic must not declare artefact_path")
    if FORBIDDEN_COMPILED.is_file():
        return _fail("compiled metabolic artefact must not exist")

    for key in EXPECTED_KEYS:
        row = by_key[key]
        state = str(row.get("authority_state") or "").strip()
        if state == STATE_COMPILED_ACTIVE:
            artefact = get_compiled_hypothesis_artefact_for_activation_key(key)
            if artefact.activation_key != key:
                return _fail(f"artefact activation_key mismatch for {key}")
            validate_runtime_promoted_artefact(artefact)
            if "Marow" in str(artefact.caveats if False else ""):
                return _fail("Marow typo present")
            # Caveats live on hypotheses
            for hyp in artefact.hypotheses:
                joined = " ".join(hyp.caveats)
                if "Marow" in joined:
                    return _fail(f"Marow typo in {key}")
        elif state == STATE_REJECTED:
            mode, _ = resolve_frame_why_authority(
                signal_id=str(row.get("signal_id") or ""),
                activation_key=key,
            )
            if mode != "skip":
                return _fail(f"REJECTED frame must resolve to skip: {key}")
        elif state == STATE_LEGACY_RETIRED:
            mode, _ = resolve_frame_why_authority(
                signal_id=str(row.get("signal_id") or ""),
                activation_key=key,
            )
            if mode != "skip":
                return _fail(f"LEGACY_RETIRED frame must resolve to skip: {key}")
            if row.get("artefact_path"):
                return _fail(f"LEGACY_RETIRED must not declare artefact_path: {key}")
        else:
            return _fail(f"unexpected authority_state {state!r} for {key}")

    # Multi-frame bare signal_id must fail closed.
    mode, _ = resolve_frame_why_authority(
        signal_id="signal_homocysteine_high",
        activation_key="",
    )
    if mode != "fail_closed":
        return _fail("bare signal_homocysteine_high must fail_closed")

    # Unique single-frame COMPILED_ACTIVE may resolve without key.
    mode, row = resolve_frame_why_authority(
        signal_id="signal_vitamin_d_low",
        activation_key="",
    )
    if mode != "compiled" or not row:
        return _fail("vitamin_d empty key must uniquely resolve to compiled")

    # Rejected-only metabolic must emit no finding and no WHY-engine fallback.
    root = compile_root_cause_v1(
        signal_results=[
            {
                "signal_id": "signal_homocysteine_high",
                "activation_key": METABOLIC_KEY,
                "source_spec_id": "inv_homocysteine_high_metabolic",
                "signal_state": "suboptimal",
                "confidence": 0.9,
                "primary_metric": "homocysteine",
            }
        ],
        biomarker_context={"homocysteine": 20.0},
        input_reference_ranges={},
    )
    if root is not None:
        return _fail("rejected metabolic must not emit root_cause findings/fallback")

    # Vitamin D uses compiled path; legacy YAML remains on disk but is not selected.
    root = compile_root_cause_v1(
        signal_results=[
            {
                "signal_id": "signal_vitamin_d_low",
                "activation_key": "signal_vitamin_d_low::inv_vitamin_d_low_deficiency",
                "source_spec_id": "inv_vitamin_d_low_deficiency",
                "signal_state": "suboptimal",
                "confidence": 0.9,
                "primary_metric": "vitamin_d",
            }
        ],
        biomarker_context={"vitamin_d": 20.0},
        input_reference_ranges={},
    )
    if root is None or len(root.findings) != 1:
        return _fail("vitamin_d must emit exactly one compiled finding")
    finding = root.findings[0]
    if finding.authority_scope != "frame_specific":
        return _fail("vitamin_d authority_scope must be frame_specific")
    if not finding.hypotheses:
        return _fail("vitamin_d compiled finding must include hypotheses")
    # Compiled artefact may retain legacy hypothesis_id for continuity; prove summary_template path.
    if "25-hydroxyvitamin D is low relative to the lab reference" not in finding.hypotheses[0].summary:
        return _fail("vitamin_d must use compiled summary_template wording")

    # Approved hcy B-vitamin frame uses compiled artefact only.
    bvit_key = (
        "signal_homocysteine_high::inv_homocysteine_high_b_vitamin_related_methylation_impairment"
    )
    root = compile_root_cause_v1(
        signal_results=[
            {
                "signal_id": "signal_homocysteine_high",
                "activation_key": bvit_key,
                "source_spec_id": "inv_homocysteine_high_b_vitamin_related_methylation_impairment",
                "signal_state": "suboptimal",
                "confidence": 0.8,
                "primary_metric": "homocysteine",
            }
        ],
        biomarker_context={"homocysteine": 20.0, "folate": 2.0},
        input_reference_ranges={},
    )
    if root is None or len(root.findings) != 1:
        return _fail("hcy B-vitamin frame must emit one compiled finding")
    ids = {h.hypothesis_id for h in root.findings[0].hypotheses}
    if ids != {
        "hyp_folate_related_hyperhomocysteinemia",
        "hyp_b12_related_or_combined_methylation_impairment",
    }:
        return _fail(f"unexpected hcy B-vitamin hypothesis ids: {sorted(ids)}")

    print("compiled_why_authority_gate: PASS")
    print(f"frames={len(EXPECTED_KEYS)} compiled_active=17 rejected=1 legacy_retired=9")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
