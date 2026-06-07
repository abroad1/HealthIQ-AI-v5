# CF-AUTHORITY-RUNTIME-1 — Runtime Signal Authority / Collision Enforcement

**Work ID:** `CF-AUTHORITY-RUNTIME-1_runtime_signal_authority_collision_enforcement`  
**Date:** 2026-06-07  
**SOP:** AUTOMATION_BUS_SOP_v1.3.1

---

## Executive verdict

**READY_FOR_HUMAN_STOP_GATE.** Reusable runtime authority/collision enforcement **implemented and tested**. `renal_filtration_axis` anti-double-counting **active** in `SignalEvaluator.evaluate_all()` post-processing. **eGFR packages not activated** — pending `APPROVE BATCH2 EGFR AUTHORITY ACTIVATION` and mandatory `enable_lower_bound` fix on both eGFR signal libraries.

---

## Artefacts inspected

| Artefact | Status |
|----------|--------|
| `signal_authority_collision_model_v1.yaml` | Read/updated — `runtime_consumed: true`, renal group enforced |
| `batch2_egfr_authority_execution_register_v1.yaml` | Read — prior governance adjudication |
| `medical_frame_identity_index_v1.yaml` | Read — eGFR frames inactive |
| `signal_evaluator.py` | Updated — post-processing hook |
| Creatinine packages (kb52c, s24) | Inspected read-only |
| eGFR packages (kb47 ×2) | Inspected — `enable_lower_bound: false` defect documented |

---

## Authority model consumption design

| Component | Role |
|-----------|------|
| `signal_authority_collision_resolver.py` | Loads model; applies enforceable groups |
| `SignalEvaluator.evaluate_all()` | Calls resolver after result assembly + sort |
| Orchestrator pipeline | Unchanged — inherits via `evaluate_all()` |

**Enforcement point:** Post-processing on `List[SignalResult]` — individual signal evaluation logic unchanged.

**Fail-loud (GPT review blocker fix):** Missing, unreadable, or invalid authority model raises `AuthorityModelLoadError`. Silent pass-through is **forbidden**.

**Potassium preservation (GPT review blocker fix):** Distinct electrolyte layer preserved by re-evaluating governed s24 override rule `or_renal_acute_imbalance` from `pkg_s24_creatinine_high_renal` — not an ad hoc potassium threshold. Authority reference: `creatinine_multiframe_authority_decision_v1.yaml` / `frame_creatinine_legacy_s24_potassium_escalation`.

---

## Runtime implementation details

- Loader reads `authority_groups` with `requires_runtime_support: true` and adjudicated status
- When `signal_egfr_low` present: suppress `signal_creatinine_high` filtration duplicates
- **Exception:** Preserve `pkg_s24_creatinine_high_renal` when governed override `or_renal_acute_imbalance` fires (distinct electrolyte risk layer)
- kb52c creatinine remains suppressed even when potassium is elevated (no governed override on that package)
- Sort order preserved: `(signal_id, activation_key)`

---

## eGFR / creatinine interaction decision

| Decision | Value |
|----------|-------|
| eGFR-low primary filtration authority when present | Yes |
| Creatinine-high suppressed as duplicate filtration framing | Yes |
| Creatinine-high preserved for hyperkalemia layer (governed s24 override) | Yes |
| Creatinine-high emits when eGFR-low absent | Yes |

---

## Anti-double-counting behaviour

Proven by regression tests: dual renal-filtration outputs consolidated when eGFR-low primary; potassium complication layer preserved.

---

## Packages activated or deferred

| Package | Status |
|---------|--------|
| pkg_kb47_egfr_low_chronic_kidney_function_reduction | **Deferred** — STOP gate + activation_config fix |
| pkg_kb47_egfr_low_hemodynamic_filtration_drop | **Deferred** — STOP gate + activation_config fix |

---

## Tests added

`backend/tests/regression/test_signal_authority_collision_enforcement.py` — **13/13 PASS**

Covers: eGFR emission, creatinine suppression, kb52c suppressed with high K, s24 preserved via governed override, creatinine alone, unrelated signals, missing model raises, malformed model raises, evaluate_all raises when model missing, ungoverned preserve rejected, frame index inactive, wiring sentinel.

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

**Context modifier catalogue:** PASS (errors: 0)

**Regression tests:** 13/13 PASS (authority collision)

**eGFR package validators (2):** PASS — `errors: 0`

## GPT architectural review blocker remediation (2026-06-07)

| Blocker | Fix |
|---------|-----|
| Missing/malformed model silent pass-through | `AuthorityModelLoadError` raised on load/validate failure |
| Ungoverned potassium > 5.2 threshold | Replaced with `preserve_when.mechanism: governed_override_rule` referencing `or_renal_acute_imbalance` |

---

## STOP gate outcome

**Status:** `READY_FOR_HUMAN_STOP_GATE`

**Activation recommended:** Yes (after approval)

**Approval phrase:** `APPROVE BATCH2 EGFR AUTHORITY ACTIVATION`

**Post-approval actions required:**
1. Fix both eGFR `signal_library.yaml`: `enable_lower_bound: true`, `enable_upper_bound: false`
2. Metadata activation (frame index + manifests) per BATCH2-ACTIVATION-1 pattern

---

## Rollback path

1. Revert `signal_authority_collision_resolver.py`
2. Remove resolver call from `signal_evaluator.py`
3. Revert collision model runtime fields
4. Revert execution register + this audit report

---

## Carry-forward updates

| ID | Action |
|----|--------|
| CF-AUTHORITY-RUNTIME-1 | **Resolved** — runtime enforcement implemented; eGFR activation deferred pending STOP |
| CF-BATCH2-007 | Unchanged (already resolved at governance level) |
| CF-CONTEXT-MOD-3 | Remains Open |

---

## Confirmations

- No clinical wording changes
- No threshold/reference range changes in packages
- No signal IDs / activation keys changed
- No frontend / SSOT / scoring / report compiler changes
- Androgen packages untouched
- Creatinine package logic unchanged

---

## Files changed

```text
backend/core/analytics/signal_authority_collision_resolver.py (new)
backend/core/analytics/signal_evaluator.py
backend/tests/regression/test_signal_authority_collision_enforcement.py (new)
knowledge_bus/governance/signal_authority_collision_model_v1.yaml
knowledge_bus/governance/authority_runtime_execution_register_v1.yaml (new)
docs/audit-papers/CF-AUTHORITY-RUNTIME-1_runtime_signal_authority_collision_enforcement.md (new)
docs/sprints/launch_core_carry_forward_register.md
```
