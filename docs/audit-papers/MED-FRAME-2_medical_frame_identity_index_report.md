# MED-FRAME-2 — Medical Frame Identity Index Report

**Work ID:** `MED-FRAME-2_medical_frame_identity_index`  
**Date:** 2026-06-02

---

## Executive verdict

The first governed, **non-runtime** medical frame identity index is implemented and passing validation. Creatinine-high is modelled as one signal family with four distinct frames, preventing flat-signal collapse while blocking duplicate active `activation_key` authority.

No runtime, package, frontend, or SignalRegistry changes were made.

---

## Files created/changed

| Path | Role |
|---|---|
| `knowledge_bus/governance/medical_frame_identity_index_v1.yaml` | Governed index (`runtime_consumed: false`) |
| `knowledge_bus/schema/medical_frame_identity_index_schema_v1.yaml` | Schema contract |
| `backend/scripts/validate_medical_frame_identity_index.py` | Standalone validator |
| `backend/tests/regression/test_med_frame_identity_index.py` | Regression tests |
| `docs/audit-papers/MED-FRAME-2_medical_frame_identity_index_report.md` | This report |
| `docs/sprints/launch_core_carry_forward_register.md` | CF-MEDFRAME1-001 resolved |

---

## Identity model implemented

- **Signal family:** `signal_creatinine_high` / biomarker `creatinine`
- **Frame identity:** `medical_frame_id` + `research_spec_id` + `activation_key`
- **Runtime authority:** at most one `runtime_authority_status: active` per `activation_key`
- **Non-runtime collisions:** `compiled_not_promoted` entries may share an activation key when `collision_status: allowed_non_runtime_collision`

---

## Creatinine family / frame entries

| medical_frame_id | promotion_state | runtime_authority | collision_status |
|---|---|---|---|
| frame_creatinine_reduced_glomerular_filtration | runtime_active_canonical | active | none |
| frame_creatinine_legacy_s24_egfr_escalation | runtime_active_legacy_unadjudicated | active | requires_adjudication |
| frame_creatinine_legacy_s24_potassium_escalation | runtime_active_legacy_unadjudicated | inactive | requires_adjudication |
| frame_creatinine_pass3_promoted_candidate | compiled_not_promoted | inactive | allowed_non_runtime_collision |

---

## Validator behaviour

`validate_medical_frame_identity_index.py` enforces:

1. Top-level index metadata and `runtime_consumed: false`
2. Required frame fields per schema
3. Unique `medical_frame_id`
4. No duplicate active `activation_key`
5. Enum validation for promotion, collision, and adjudication states
6. Rejection of `runtime_active_canonical` + `real_collision_active_blocker`
7. Package path existence for referenced entries

The validator does **not** import runtime modules.

---

## Regression test coverage

- Valid index passes via CLI subprocess
- Four creatinine frames present
- kb52c vs promoted candidate collision classification
- Duplicate active activation key failure (mutated fixture)
- Missing field / unknown enum / `runtime_consumed` failures
- Legacy eGFR and potassium frames preserved

---

## Runtime boundary confirmation

No changes to: SignalEvaluator, SignalRegistry, loaders, packages, frontend, SSOT, or `latest_knowledge_status.json`.

---

## Carry-forward updates

- **CF-MEDFRAME1-001:** Resolved (index + validator created)
- **CF-MEDFRAME1-002:** Remains open → CONTEXT-MOD-1
- **CF-MEDFRAME1-003:** Remains open → creatinine authority adjudication

---

## Remaining limitations

- Index covers creatinine family only (not estate-wide)
- Questionnaire and medication modifiers flagged unsupported at frame level (CONTEXT-MOD-1)
- Legacy s24 eGFR/potassium divergence not adjudicated
- Index not wired to runtime (by design)

---

## Recommended next sprint

**CONTEXT-MOD-1** — questionnaire and drug-category modifier governance bound to frame IDs.

**KB-UTIL-2-CREATININE-AUTHORITY-ADJUDICATION** — clinical adjudication for legacy eGFR/potassium vs Pass_3 UACR before any authority convergence.

---

## Creatinine architecture narrative (business terms)

**Why creatinine_high is not one flat meaning:** High creatinine can indicate reduced filtration, albuminuric damage, electrolyte risk, creatinine distortion, or medication-associated strain. Collapsing these into one signal would mislead users and clinicians.

**Evidence roles:** eGFR corroborates filtration; UACR supports kidney disease context in Pass_3 frame; potassium supports acute imbalance in legacy frame; cystatin C supports differential interpretation.

**Why Pass_3 candidate was not activated:** It duplicates the kb52c Pass_3 frame activation identity. WIRE-1 correctly refused runtime activation.

**Why pkg_kb52c remains canonical:** It is the governed Pass_3 runtime package for `inv_creatinine_high_reduced_glomerular_filtration`.

**Why legacy s24 logic is retained:** eGFR and potassium override rules remain medically relevant but unadjudicated relative to Pass_3 UACR escalation—they are indexed, not deleted.

**How the index prevents collapse and duplicate authority:** Multiple `medical_frame_id` entries under one family, with validator-enforced single active authority per `activation_key`.
