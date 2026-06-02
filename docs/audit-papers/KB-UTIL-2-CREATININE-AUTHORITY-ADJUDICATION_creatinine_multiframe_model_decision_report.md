# KB-UTIL-2-CREATININE-AUTHORITY-ADJUDICATION — Creatinine Multi-Frame Model Decision Report

**Work ID:** `KB-UTIL-2-CREATININE-AUTHORITY-ADJUDICATION_creatinine_multiframe_model_decision`  
**Date:** 2026-06-02  
**SOP:** AUTOMATION_BUS_SOP_v1.3.1

---

## Executive verdict

**PASS (governance adjudication only).** Creatinine high is confirmed as a **multi-frame signal family**. `pkg_kb52c` remains the Pass_3 canonical authority for reduced glomerular filtration. The ROUTE_A promoted candidate is a **duplicate** of `pkg_kb52c` and must stay `compiled_not_promoted`. Legacy `pkg_s24` **eGFR and potassium override contexts are preserved** and must not be retired until Pass_3 enrichment and medical review. **No runtime activation, no package file changes.**

---

## Artefacts inspected

| Artefact | Path |
|----------|------|
| Medical frame identity index | `knowledge_bus/governance/medical_frame_identity_index_v1.yaml` |
| Context modifier catalogue | `knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml` |
| Pass_3 promotion register | `knowledge_bus/governance/pass3_promotion_decision_register_v1.yaml` |
| WIRE-1 report | `docs/audit-papers/KB-UTIL-2-PROMOTE-WIRE-1_creatinine_runtime_authority_switch_report.md` |
| Activation-readiness report | `docs/audit-papers/KB-UTIL-2-ACTIVATION-READINESS_creatinine_candidate_divergence_and_collision_resolution_report.md` |
| s24 package | `knowledge_bus/packages/pkg_s24_creatinine_high_renal/` |
| kb52c package | `knowledge_bus/packages/pkg_kb52c_creatinine_high_reduced_glomerular_filtration/` |
| Promoted candidate | `knowledge_bus/generated_pilot/kb_util_2_pilot/promoted_candidates/pkg_creatinine_high_renal_pass3_v1/` |

---

## Package comparison table

| Field | pkg_s24_creatinine_high_renal | pkg_kb52c_creatinine_high_reduced_glomerular_filtration | pkg_creatinine_high_renal_pass3_v1 (candidate) |
|-------|------------------------------|--------------------------------------------------------|-----------------------------------------------|
| Package path | `knowledge_bus/packages/pkg_s24_creatinine_high_renal/` | `knowledge_bus/packages/pkg_kb52c_creatinine_high_reduced_glomerular_filtration/` | `knowledge_bus/generated_pilot/.../pkg_creatinine_high_renal_pass3_v1/` |
| signal_id | `signal_creatinine_high` | `signal_creatinine_high` | `signal_creatinine_high` |
| activation_key | `signal_creatinine_high::inv_creatinine_high_renal` | `signal_creatinine_high::inv_creatinine_high_reduced_glomerular_filtration` | `signal_creatinine_high::inv_creatinine_high_reduced_glomerular_filtration` |
| Source spec / document | `inv_creatinine_high_renal_v1.yaml` | `Batch_4_Pass_3.json` / `inv_creatinine_high_reduced_glomerular_filtration` | `Batch_4_Pass_3.json` / same spec as kb52c |
| Primary biomarker | creatinine | creatinine | creatinine |
| Supporting markers | egfr, urea, potassium | egfr, uacr, cystatin_c (roles: corroborator, mechanism, differential) | egfr, uacr, cystatin_c (same as kb52c) |
| Override rules | `or_renal_ckd_stage_3` (eGFR < 60); `or_renal_acute_imbalance` (K+ > 5.2) | `or_creatinine_high_with_uacr_high` (UACR lab-range boundary) | Same UACR rule as kb52c |
| Thresholds | Lab-range placeholder | Lab-range placeholder | Lab-range placeholder |
| Evidence roles | eGFR/potassium escalation in single library | eGFR corroborator; UACR mechanism; cystatin C differential | Same as kb52c |
| Frame(s) represented | Legacy eGFR + potassium override frames (index split) | Reduced glomerular filtration (Pass_3 canonical) | Duplicate Pass_3 GFR frame |
| Runtime status | Runtime-loaded (`packages/`) | Runtime-loaded (`packages/`) | **Not** runtime-loaded |
| Promotion state | `runtime_active_legacy_unadjudicated` (index) | `runtime_active_canonical` | `compiled_not_promoted` |
| Clinical adjudication | `blocked_pending_medical_review` (legacy frames) | `not_required` (canonical GFR) | Duplicate — do not activate |
| Recommended action | **Retain** until Pass_3 enrichment | **Retain** canonical | **Retain** as duplicate non-runtime |

---

## Current runtime authority assessment

Two distinct activation keys coexist in runtime `knowledge_bus/packages/`:

1. **Pass_3 GFR frame** → `pkg_kb52c` (canonical).
2. **Legacy renal spec** → `pkg_s24` (eGFR + potassium overrides on one library).

No duplicate activation key for the same `research_spec_id` is active. WIRE-1 correctly refused candidate activation.

---

## Promoted candidate assessment

`pkg_creatinine_high_renal_pass3_v1` shares `activation_key`, spec, and UACR override logic with `pkg_kb52c`. **Adds nothing beyond kb52c** for runtime purposes. Status: **duplicate `compiled_not_promoted` candidate** — superseded by kb52c per identity index.

---

## s24 legacy frame assessment

`pkg_s24` encodes **two medically distinct override pathways** on one package:

| Override | Medical context | Covered by kb52c? |
|----------|-----------------|-----------------|
| eGFR < 60 | Filtration severity / CKD-stage escalation | Partially (eGFR as corroborator only; no eGFR threshold override) |
| Potassium > 5.2 | Acute electrolyte / safety-risk escalation | **No** — kb52c has no potassium override |

**Conclusion:** s24 must **not** be deleted or collapsed. Retirement requires Pass_3 enrichment or explicit medical adjudication.

---

## eGFR / potassium / UACR / cystatin-C roles

| Marker / rule | Architectural role | Frame relationship |
|---------------|-------------------|-------------------|
| eGFR low | Corroborator (kb52c); threshold override (s24) | Severity context vs legacy escalation frame |
| UACR high | Pass_3 override escalation (kb52c) | Albuminuria / kidney-damage context within GFR frame; distinct frame deferred |
| Potassium high | s24 override escalation only today | Acute electrolyte-risk frame (legacy index entry) |
| Cystatin C | Differential marker in kb52c | Supports distortion vs true filtration; not a standalone frame |

---

## Context modifier relevance

`context_modifier_catalogue_draft_v1.yaml` rows cover CKD, diabetes/hypertension, NSAIDs, ACE/ARB, diuretics, hydration, exercise, creatine, cystatin C availability, and potassium — aligned with frame decisions. **No modifier evaluation** in this sprint (CONTEXT-MOD-2).

---

## Medical / architecture decision

Governed decision file: `knowledge_bus/governance/creatinine_multiframe_authority_decision_v1.yaml`

**Cursor did not make independent clinical judgements.** Decisions are artefact-comparison and architecture-classification only.

### Core questions answered

1. **Is pkg_kb52c the correct Pass_3 canonical for reduced GFR?** — **Yes** (repo evidence: active canonical index + runtime package).
2. **Does promoted candidate add beyond kb52c?** — **No** (duplicate activation_key and override logic).
3. **What frames does pkg_s24 represent?** — Legacy eGFR CKD-stage escalation + potassium acute-imbalance escalation (one package, two index frames).
4. **What is covered by Pass_3/kb52c?** — Reduced GFR frame, UACR escalation, cystatin C differential role.
5. **What is not covered?** — eGFR threshold override path, potassium safety override, standalone albuminuric and distortion frames.
6. **eGFR/potassium treatment?** — **Separate legacy frames** + **defer** Pass_3 enrichment; not context-modifier-only substitutes for potassium safety.
7. **Before activation/supersession/retirement?** — Medical review + Pass_3 enrichment + no duplicate activation keys.
8. **Pass_3 enrichment needed?** — **Yes** for eGFR/potassium/albuminuria frame completeness before s24 retirement.

---

## What must not be collapsed

- eGFR severity vs UACR albuminuria vs potassium safety vs creatinine distortion
- Legacy s24 overrides into kb52c UACR-only model
- Promoted candidate into runtime while kb52c is canonical

---

## What must not be activated yet

- `pkg_creatinine_high_renal_pass3_v1` into `knowledge_bus/packages/`
- Any package retirement or supersession of s24
- `runtime_activation_allowed` remains **false**

---

## Updates made

| File | Change |
|------|--------|
| `knowledge_bus/governance/creatinine_multiframe_authority_decision_v1.yaml` | Created |
| `knowledge_bus/governance/medical_frame_identity_index_v1.yaml` | Notes + adjudication references |
| `knowledge_bus/governance/pass3_promotion_decision_register_v1.yaml` | Adjudication block added |
| `docs/sprints/launch_core_carry_forward_register.md` | CF-MEDFRAME1-003 resolved; CF-CREATININE-001 added |
| This report | Created |

---

## Validation results

All sprint validators and regression tests run at closure — see implementation evidence.

---

## Remaining blockers

- Medical review for legacy eGFR/potassium vs Pass_3 UACR paths
- Pass_3 specs/packages for albuminuric and electrolyte frames
- CONTEXT-MOD-2 Layer B modifier binding

---

## Recommended next sprint

**CREATININE-PASS3-ENRICH-1** — Pass_3 investigation enrichment and/or package regeneration for eGFR, potassium, and albuminuria frames before legacy s24 retirement.

---

## Runtime boundary confirmation

No changes to `knowledge_bus/packages/*`, SignalEvaluator, SignalRegistry, loaders, frontend, or SSOT.
