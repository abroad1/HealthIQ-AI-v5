# BATCH2-REMAINDER-RESOLUTION-1 — Remaining Batch 2 Package Resolution Investigation

**Work ID:** `BATCH2-REMAINDER-RESOLUTION-1_remaining_batch2_package_resolution_investigation`  
**Date:** 2026-06-07  
**SOP:** AUTOMATION_BUS_SOP_v1.3.1

---

## Executive verdict

**INVESTIGATION COMPLETE.** All **14** remaining Batch 2 packages classified with evidence-grounded blockers. **No promotion, activation, or runtime changes performed.** Package validators **14/14 PASS**. Architecture gate **PASS**. Primary finding: the **three TSH-only thyroid patterns** (FT3 high, FT4 high, FT4 low) are the only cohort ready for a **single bounded execution sprint** after mandatory TSH activation gating is implemented; **FT3 low**, **all 8 androgen**, and **both eGFR** packages remain formally blocked pending distinct prerequisites.

---

## Artefacts inspected

| Artefact | Status |
|----------|--------|
| `batch2_runtime_activation_execution_register_v1.yaml` | Read — 6 active, 4 thyroid deferred, 10 excluded |
| `batch2_final_promotion_decision_register_v1.yaml` | Read — 20 total, 10 cleared, 10 excluded |
| `batch2_promote_1_execution_register_v1.yaml` | Read |
| `batch2_promotion_readiness_register_v1.yaml` | Read |
| `batch2_androgen_panel_medical_review_v1.yaml` | Read |
| `batch2_androgen_context_modifier_binding_v1.yaml` | Read |
| `pass3_batch2_research_asset_register_v1.yaml` | Present |
| `pass3_batch2_kb47_manifest_realign_register_v1.yaml` | Present |
| `medical_frame_identity_index_v1.yaml` | Read (not modified) |
| `context_modifier_catalogue_draft_v1.yaml` | Read — all modifiers `runtime_active: false` |
| `thyroid_blood_marker_interpretation_clinical_signoff.md` | Read — APPROVE_SUBSET |
| `knowledge_bus/current/latest_knowledge_status.json` | **Absent** — activation state taken from activation register |
| All 14 package directories | Inspected (manifest/signal_library read-only) |
| `backend/core/analytics/signal_evaluator.py` | Read — lab_range_exceeded fires before override escalation |

---

## Current Batch 2 state summary

| Cohort | Count | State |
|--------|------:|-------|
| Runtime active (CK + eosinophil) | 6 | `runtime_active_canonical` |
| Governance-promoted, runtime-deferred (thyroid) | 4 | `compiled_not_promoted` / inactive |
| Never promoted — androgen | 8 | EXCLUDED; indexed, validate PASS |
| Never promoted — eGFR | 2 | EXCLUDED; indexed, collision requires_adjudication |

---

## All 14 remaining packages — summary table

| package_id | Gov promoted | Runtime active | Validates | Blocker type | Final recommendation |
|------------|:------------:|:--------------:|:---------:|--------------|----------------------|
| pkg_kb47_free_t3_high_t3_predominant_thyrotoxicosis | Yes | No | PASS | thyroid_tsh_gating_required | READY_IF_RUNTIME_GATE_IMPLEMENTED |
| pkg_kb47_free_t3_low_low_t3_syndrome | Yes | No | PASS | thyroid_tsh_ft4_context_required | FORMALLY_BLOCKED_KEEP_INACTIVE |
| pkg_kb47_free_t4_high_thyrotoxicosis_context | Yes | No | PASS | thyroid_tsh_gating_required | READY_IF_RUNTIME_GATE_IMPLEMENTED |
| pkg_kb47_free_t4_low_thyroid_hormone_deficiency | Yes | No | PASS | thyroid_tsh_gating_required | READY_IF_RUNTIME_GATE_IMPLEMENTED |
| pkg_kb47_dhea_high_androgen_excess_context | No | No | PASS | androgen_clinical_signoff_required | FORMALLY_BLOCKED_KEEP_INACTIVE |
| pkg_kb47_dhea_low_adrenal_androgen_reduction | No | No | PASS | androgen_context_runtime_required | FORMALLY_BLOCKED_KEEP_INACTIVE |
| pkg_kb47_fai_high_biochemical_hyperandrogenism | No | No | PASS | androgen_context_runtime_required | FORMALLY_BLOCKED_KEEP_INACTIVE |
| pkg_kb47_fai_low_reduced_free_androgen_availability | No | No | PASS | androgen_context_runtime_required | FORMALLY_BLOCKED_KEEP_INACTIVE |
| pkg_kb47_free_testosterone_high_androgen_excess_context | No | No | PASS | androgen_clinical_signoff_required | FORMALLY_BLOCKED_KEEP_INACTIVE |
| pkg_kb47_free_testosterone_low_androgen_deficiency_context | No | No | PASS | androgen_context_runtime_required | FORMALLY_BLOCKED_KEEP_INACTIVE |
| pkg_kb47_free_testosterone_pct_high_elevated_free_androgen_fraction | No | No | PASS | androgen_context_runtime_required | FORMALLY_BLOCKED_KEEP_INACTIVE |
| pkg_kb47_free_testosterone_pct_low_reduced_free_androgen_fraction | No | No | PASS | androgen_context_runtime_required | FORMALLY_BLOCKED_KEEP_INACTIVE |
| pkg_kb47_egfr_low_chronic_kidney_function_reduction | No | No | PASS | renal_authority_adjudication_required | REQUIRES_ARCHITECTURE_AUTHORITY_DECISION |
| pkg_kb47_egfr_low_hemodynamic_filtration_drop | No | No | PASS | anti_double_counting_required | REQUIRES_ARCHITECTURE_AUTHORITY_DECISION |

Full per-package records: `knowledge_bus/governance/batch2_remainder_resolution_register_v1.yaml`

---

## Thyroid resolution assessment

**Clinical sign-off:** APPROVE_SUBSET — TSH mandatory for all four; FT3 low additionally requires TSH + FT4 + illness/medication context.

**TSH at runtime:** TSH is available as a biomarker input to `SignalEvaluator` when present in lab panel. Existing kb47 thyroid packages list TSH in `dependencies` and `override_rules`.

**Critical architectural finding:** `SignalEvaluator` evaluates `lab_range_exceeded` on the primary metric **first**, emitting a signal before override rules apply. Override rules (e.g. `or_free_t3_high_with_tsh_low`) **escalate** state when TSH is suppressed but **do not block** isolated FT3/FT4 activation. Clinical sign-off explicitly prohibits activating from isolated FT3 high.

**Conclusion:** Metadata-only runtime activation (BATCH2-ACTIVATION-1 pattern) is **insufficient** for thyroid. Mandatory TSH gating requires **signal_library and/or SignalEvaluator changes** plus regression proof before metadata activation.

| Pattern | Safe after TSH-only gate? |
|---------|---------------------------|
| FT3 high | Yes — with mandatory suppression gate |
| FT4 high | Yes — with mandatory suppression gate |
| FT4 low | Yes — with mandatory TSH interpretation gate |
| FT3 low | **No** — requires TSH + FT4 + illness/medication context (Layer B gap) |

---

## Androgen resolution assessment

**Governance state:** All 8 packages **EXCLUDED** from BATCH2-PROMOTE-1 — not governance-promoted.

**Medical review:** 4 frames MEDICALLY_COHERENT_BUT_CONTEXT_DEPENDENT; 4 BLOCKED_PENDING_CONTEXT_MODIFIER_BINDING. All 8 require clinical sign-off (CF-BATCH2-010).

**Context modifiers:** BATCH2-CONTEXT-MOD-1 bound catalogue links for all 8 frames. **Every catalogue modifier has `runtime_active: false`.** No Layer B context evaluation consumes modifiers (CF-CONTEXT-MOD-3).

**Runtime context availability:**

| Context | Governance catalogue | Runtime consumed |
|---------|---------------------|------------------|
| Sex | mod_demo_sex linked | No |
| Age | mod_demo_age linked | No |
| SHBG | mod_androgen_ctx_shbg_governance linked | No |
| Hormone medication | mod_med_testosterone_hormone linked | No |
| AAS/steroid exposure | mod_androgen_ctx_aas_exposure linked | No |

**Conclusion:** Androgen packages **cannot** be safely activated without Layer B context evaluation. No subset is safe for context-gated metadata activation today. All 8 remain **FORMALLY_BLOCKED** until CF-CONTEXT-MOD-3, CF-BATCH2-010, and a **re-promotion sprint**.

---

## eGFR resolution assessment

**Governance state:** Both packages **EXCLUDED** from BATCH2-PROMOTE-1.

**Frame index:** `signal_egfr_low` is a distinct family with two ROUTE_C frames; both carry `collision_status: requires_adjudication`. Notes reference creatinine legacy eGFR override (`frame_creatinine_legacy_s24_egfr_escalation`) and CF-CREATININE-001 adjacency.

**Authority overlap:** `creatinine_multiframe_authority_decision_v1.yaml` documents pkg_kb52c as canonical creatinine authority; legacy s24 retains eGFR escalation override. Independent `signal_egfr_low` runtime activation would risk **duplicate renal dysfunction signalling** without anti-double-counting rules.

**Medical research vs architecture:** Package medical content validates; blocker is **architectural authority** (CF-BATCH2-007), not missing Pass 3 research.

**Conclusion:** Both eGFR packages require **BATCH2-EGFR-AUTHORITY-1** architecture adjudication before promotion or activation.

---

## Medical research gaps

| Area | Research needed? |
|------|------------------|
| Thyroid TSH gating | **No** — sign-off ingested; implementation gap is runtime gate |
| Thyroid FT3 low illness context | **Partially** — context modifiers exist in catalogue but not runtime |
| Androgen panel | **Yes** — clinical sign-off artefact absent (CF-BATCH2-010) |
| eGFR dual-frame | **No new research required** — architecture authority decision primary |

---

## Runtime / context architecture gaps

1. **Mandatory cross-biomarker activation gate** for thyroid (SignalEvaluator / signal_library)
2. **Layer B context modifier evaluation** (CF-CONTEXT-MOD-3) for androgen and FT3 low illness context
3. **Renal signal family authority model** for independent `signal_egfr_low` vs `signal_creatinine_high`

---

## Package validation evidence

Command: `python backend/scripts/validate_knowledge_package.py --package-dir <package_dir>`

**Result: 14/14 PASS** (`ready_for_implementation: True` for all)

---

## Architecture gate output

```text
validation_status: PASS (frame index)
validation_status: PASS (context modifier catalogue)
day_one_architecture_validation: PASS
medical_intelligence_architecture_validation: PASS
architecture_validation_gate: PASS
```

---

## Carry-forward updates

| ID | Update |
|----|--------|
| CF-BATCH2-013 | Investigation complete — implement mandatory TSH activation gate in SignalEvaluator/signal_library; then metadata activation for 3 TSH-only patterns; FT3 low remains blocked for TSH+FT4+context |
| CF-BATCH2-010 | Androgen clinical sign-off still absent; blocks all 8 packages before any re-promotion |
| CF-CONTEXT-MOD-3 | Blocks **all 8 androgen packages** and **FT3 low** illness/medication context; catalogue links are governance-only |
| CF-BATCH2-007 | Requires architecture authority decision for signal_egfr_low vs creatinine/eGFR escalation; document collision rules before promotion |

---

## Recommended next execution package

```text
Recommended next execution package:
BATCH2-THYROID-GATE-1_mandatory_tsh_gating_and_runtime_activation

Scope:
- packages to activate (after gate proof + STOP approval):
  - pkg_kb47_free_t3_high_t3_predominant_thyrotoxicosis
  - pkg_kb47_free_t4_high_thyrotoxicosis_context
  - pkg_kb47_free_t4_low_thyroid_hormone_deficiency
- packages to keep blocked in same programme:
  - pkg_kb47_free_t3_low_low_t3_syndrome (TSH+FT4+illness context — separate follow-on)
- packages to keep blocked entirely (out of scope):
  - all 8 androgen packages
  - both eGFR packages

gates to implement:
- Mandatory TSH-suppression/interpretation activation gate preventing isolated FT3/FT4 firing
- Regression tests proving gate enforcement

STOP gates required:
- Human STOP gate before metadata runtime activation (APPROVE phrase pattern)

validations required:
- validate_knowledge_package.py × 3 thyroid packages pre/post gate
- validate_medical_frame_identity_index.py
- run_architecture_validation_gate.py

Follow-on execution packages (do not combine):
- BATCH2-EGFR-AUTHORITY-1_renal_signal_family_authority_adjudication
- BATCH2-ANDROGEN-EXECUTION-1_androgen_panel_promotion_after_context_and_signoff
- BATCH2-THYROID-FT3LOW-1_ft3_low_context_gated_activation (after CONTEXT-MOD-3)
```

---

## Confirmations

- **No** package file modifications
- **No** frame index or context catalogue modifications
- **No** runtime/frontend/evaluator code changes
- **No** promotion or activation performed
