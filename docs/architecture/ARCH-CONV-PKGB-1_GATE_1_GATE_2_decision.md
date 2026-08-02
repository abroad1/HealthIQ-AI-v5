# ARCH-CONV-PKGB-1 — Gate 1 / Gate 2 Decision Record

**Work ID:** `ARCH-CONV-PKGB-1`  
**Date opened:** 2026-08-02  
**Gate 1 recorded:** *pending*  
**Gate 2 recorded:** *pending*  
**Hardening pack:** `docs/architecture/ARCH-CONV-PKGB-1_hardening_pack.md`  
**Medical decision register:** `docs/architecture/ARCH-CONV-PKGB-1_medical_decision_register.yaml`  
**Implementation status:** **NOT AUTHORISED** — awaiting Gate 1 and Gate 2

## Gate references

| Gate | Reference | Status |
|---|---|---|
| Gate 1 — Head of Medical Research | *pending* | `PENDING` |
| Gate 2 — Anthony (project authority) | *pending* | `PENDING` |

## Decision authority split

- **Head of Medical Research (Gate 1)** is the source of the medical judgement confirming FOLD_SUPPRESS implementation boundaries.
- **Anthony (Gate 2)** ratifies proceed/hold for project authority; Anthony is **not** the source of medical judgement.

## Register state

```text
register_state: AWAITING_GATE_1_GATE_2
gate1_status: PENDING
gate2_status: PENDING
runtime_changes_authorised: false
```

---

## Exact Gate 1 decision required

Head of Medical Research must confirm **all seven** of the following. Any disagreement with the Phase 0 pack must be recorded explicitly; silent omission is not approval.

### Q1 — FOLD_SUPPRESS retention

Confirm that `signal_homocysteine_elevation_context` remains **`FOLD_SUPPRESS`** as previously ratified under ARCH-CONV-A Wave 0 / STOP A (`ARCH-CONV-A_wave0_suppression_closure.md`).

- Required answer form: `CONFIRMED` or `REVISED` (with replacement disposition).

### Q2 — No independent WHY ownership / emission

Confirm that elevation-context **must not** independently own or emit WHY content after this sprint’s exclusivity implementation.

- Required answer form: `CONFIRMED` or `REVISED`.

### Q3 — No new medical hypothesis / replacement narrative

Confirm that **no** new medical hypothesis and **no** replacement narrative is required for `signal_homocysteine_elevation_context`.

- Required answer form: `CONFIRMED` or `REVISED` (with required content scope).

### Q4 — Homocysteine-high compiled content unchanged

Confirm that `signal_homocysteine_high` compiled WHY content remains **unchanged** (B-vitamin and renal `COMPILED_ACTIVE` artefacts; metabolic remains `REJECTED`).

- Required answer form: `CONFIRMED` or `REVISED`.

### Q5 — Total-cholesterol / bare-key resolver is mechanical only

Confirm that the bare-key resolver correction for pilot families with zero `COMPILED_ACTIVE` rows (including `signal_total_cholesterol_high`, and the uniform class `signal_ldl_high`, `signal_hdl_low`, `signal_hgb_low`, `signal_hepatic_alt_context`) is **mechanical authority handling only** and must **not** create new medical content.

- Required answer form: `CONFIRMED` or `REVISED`.

### Q6 — HbA1c / urate assertion alignment only

Confirm that correcting stale tests to:

- HbA1c: `hyp_hba1c_elevated_glycaemia_context`
- Urate: `hyp_urate_elevated_non_causal_context`

is **assertion alignment only** and must **not** alter runtime content.

- Required answer form: `CONFIRMED` or `REVISED`.

### Q7 — No L-04 / L-05 / L-06 product-policy decision

Confirm that this sprint does **not** make or imply any L-04 (`why_engine_fallback_v1`), L-05 (`_why_template`), or L-06 (family aggregation) product-policy decision.

- Required answer form: `CONFIRMED` or `REVISED`.

### Optional Gate 1 mechanism preference (within Q1–Q2 boundary)

Phase 0 proposes three architectural options (A register WHY-only retirement; B selector disconnect; C other existing skip). Gate 1 may:

- leave mechanism choice to implementation under the medical boundary above; or
- name a preferred option.

Mechanism preference is **not** a substitute for Q1–Q7 answers.

---

## Gate 1 decision block (to be completed by Head of Medical Research)

```text
gate1_reference: ARCH-CONV-PKGB-1-GATE1-HMR-YYYY-MM-DD
decision: PENDING
q1_fold_suppress: PENDING
q2_no_independent_why_emit: PENDING
q3_no_new_hypothesis_or_narrative: PENDING
q4_hcy_high_compiled_unchanged: PENDING
q5_resolver_mechanical_only: PENDING
q6_assertion_alignment_only: PENDING
q7_no_l04_l05_l06_policy: PENDING
mechanism_preference: PENDING_OR_DEFER_TO_IMPLEMENTATION
notes: 
```

---

## Gate 2 ratification block (to be completed by Anthony)

Gate 2 must ratify Gate 1 **exactly**. If Gate 1 is revised, Gate 2 must ratify the revised text, not a different disposition.

```text
gate2_reference: ARCH-CONV-PKGB-1-GATE2-ANTHONY-YYYY-MM-DD
decision: PENDING
ratifies: PENDING
runtime_changes_authorised: false
notes:
```

---

## Non-claims until gates are recorded

- Cursor must not alter resolver behaviour.
- Cursor must not disconnect or split the shared homocysteine asset.
- Cursor must not change authority registers.
- Cursor must not modify test expectations.
- Cursor must not touch L-04, L-05, L-06, or Package C.
- Retrospective ratification after runtime change is forbidden.

## Resume condition

Runtime Phase 1 is authorised only when:

1. Gate 1 answers Q1–Q7 on disk; and  
2. Gate 2 records `APPROVED` ratifying that exact Gate 1; and  
3. `runtime_changes_authorised: true` is written into this file and the medical decision register.
