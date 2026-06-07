# BATCH2-EGFR-AUTHORITY-1 — Renal Signal Authority and Reusable Collision Model

**Work ID:** `BATCH2-EGFR-AUTHORITY-1_renal_signal_authority_and_reusable_collision_model`  
**Date:** 2026-06-07  
**SOP:** AUTOMATION_BUS_SOP_v1.3.1

---

## Executive verdict

**AUTHORITY ADJUDICATED — RUNTIME INACTIVE (Outcome B).** Reusable `signal_authority_collision_model_v1.yaml` created with adjudicated `renal_filtration_axis`. Both Batch 2 eGFR packages authority-classified but **not activated**. **No runtime code changes.** **No clinical wording or threshold changes.** Activation blocked until **CF-AUTHORITY-RUNTIME-1** implements evaluator wiring. **No human STOP gate required** — activation not recommended.

---

## Artefacts inspected

| Artefact | Status |
|----------|--------|
| `batch2_remainder_resolution_register_v1.yaml` | Read — eGFR packages REQUIRES_ARCHITECTURE_AUTHORITY_DECISION |
| `batch2_remaining_blockers_execution_register_v1.yaml` | Read — egfr KEEP_BLOCKED |
| `creatinine_multiframe_authority_decision_v1.yaml` | Read — eGFR corroborator not replacement; legacy s24 active |
| `medical_frame_identity_index_v1.yaml` | Read/updated — collision_status + notes for 2 eGFR frames |
| `batch2_final_promotion_decision_register_v1.yaml` | Read — eGFR excluded from BATCH2-PROMOTE-1 |
| Both eGFR package directories | Inspected read-only |
| `pkg_kb52c_creatinine_high_reduced_glomerular_filtration` | Inspected — canonical creatinine active |
| `pkg_s24_creatinine_high_renal` | Inspected — legacy eGFR/potassium overrides |
| `backend/core/analytics/signal_evaluator.py` | Read — no collision/suppression mechanism |

---

## Creatinine / eGFR relationship summary

| Entity | Role | Runtime state |
|--------|------|---------------|
| `signal_egfr_low` (kb47 chronic + hemodynamic) | Pass 3 distinct filtration family | Inactive |
| `signal_creatinine_high` / `frame_creatinine_reduced_glomerular_filtration` | Canonical Pass 3 reduced GFR | Active |
| `frame_creatinine_legacy_s24_egfr_escalation` | Legacy eGFR CKD-stage override on creatinine signal | Active (legacy) |
| `frame_creatinine_legacy_s24_potassium_escalation` | Distinct acute electrolyte layer | Active (legacy) |

**Risk:** Activating `signal_egfr_low` without anti-double-counting would present low eGFR + high creatinine as two independent renal-filtration problems alongside legacy s24 eGFR escalation.

---

## Renal authority decision (8 questions)

| # | Question | Decision |
|---|----------|----------|
| 1 | Is eGFR-low its own signal family? | **Yes** — `signal_egfr_low` indexed separately |
| 2 | Is eGFR-low stronger renal-filtration evidence than creatinine-high? | **Yes, when present** — primary filtration authority |
| 3 | Should creatinine-high remain active as a separate signal? | **Yes** — supporting evidence or separate biochemical abnormality |
| 4 | Should eGFR-low suppress duplicate filtration framing from creatinine-high? | **Yes** — when both present at user-facing surface |
| 5 | Can creatinine still contribute as supporting evidence? | **Yes** — when not duplicate filtration framing |
| 6 | Does potassium / acute risk remain a separate complication layer? | **Yes** — `hyperkalemia_or_electrolyte_complication` distinct layer |
| 7 | Can the two Batch 2 eGFR packages activate safely now? | **No** |
| 8 | What is missing? | Runtime consumption of authority/collision model in SignalEvaluator |

---

## Reusable authority / collision model

**Created:** `knowledge_bus/governance/signal_authority_collision_model_v1.yaml`

- `runtime_consumed: false`
- Adjudicated group: `renal_filtration_axis`
- Placeholder groups (not adjudicated): metabolic_glycaemic_axis, thyroid_axis, androgen_axis, liver_injury_axis, iron_inflammation_axis

---

## Phase 3 activation outcome

**Outcome B:** Governance authority-classified; runtime inactive pending reusable runtime support.

| Package | Activated | Final state |
|---------|:---------:|-------------|
| pkg_kb47_egfr_low_chronic_kidney_function_reduction | No | compiled_not_promoted / inactive |
| pkg_kb47_egfr_low_hemodynamic_filtration_drop | No | compiled_not_promoted / inactive |

---

## Anti-double-counting decision

| Item | Status |
|------|--------|
| Governance pattern defined | Yes — declarative `authority_resolution` under `renal_filtration_axis` |
| Runtime mechanism in SignalEvaluator | **No** |
| Safe to activate now | **No** |
| Next action | CF-AUTHORITY-RUNTIME-1 |

---

## Runtime behaviour changed

**None.** Governance-only sprint.

---

## Tests added / not added

**Not added** — no runtime or signal_library changes. Existing architecture and governance regression tests cover frame index updates.

---

## STOP gate outcome

**Activation not recommended** — human STOP gate (`APPROVE BATCH2 EGFR AUTHORITY ACTIVATION`) **not invoked**.

If runtime support is implemented under CF-AUTHORITY-RUNTIME-1, a future sprint must STOP before metadata activation.

---

## Rollback path

1. Revert `signal_authority_collision_model_v1.yaml`
2. Revert `batch2_egfr_authority_execution_register_v1.yaml`
3. Revert eGFR frame index collision_status/notes to `requires_adjudication`
4. Revert carry-forward register (remove CF-AUTHORITY-RUNTIME-1; restore CF-BATCH2-007 prior note)

---

## Carry-forward updates

| ID | Action |
|----|--------|
| CF-BATCH2-007 | **Resolved** — authority adjudicated via reusable collision model |
| CF-AUTHORITY-RUNTIME-1 | **Open (new)** — runtime consumption of collision model |

---

## Confirmations

- No clinical wording changes
- No threshold or reference range changes
- No signal_library / research_brief changes
- No frontend / SSOT / scoring / report compiler changes
- Creatinine packages untouched
- Androgen packages untouched

---

## Validation output

**Architecture gate:** PASS

```text
architecture_validation_gate: PASS
medical_frame_identity_index: PASS (errors: 0)
context_modifier_catalogue: PASS (errors: 0)
day_one_architecture_validation: PASS
medical_intelligence_architecture_validation: PASS
pytest_architecture_guardrails: PASS
pytest_governance_regression: PASS
```

**Frame index validator:** PASS (errors: 0)

**Context modifier catalogue validator:** PASS (errors: 0)

**eGFR package validators (2):** all PASS — `validation_status: PASS`, `errors: 0`, `manifest_validation: PASS`

---

## Files changed

```text
knowledge_bus/governance/signal_authority_collision_model_v1.yaml (new)
knowledge_bus/governance/batch2_egfr_authority_execution_register_v1.yaml (new)
knowledge_bus/governance/medical_frame_identity_index_v1.yaml (eGFR frames only)
docs/audit-papers/BATCH2-EGFR-AUTHORITY-1_renal_signal_authority_and_reusable_collision_model.md (new)
docs/sprints/launch_core_carry_forward_register.md (updated)
```
