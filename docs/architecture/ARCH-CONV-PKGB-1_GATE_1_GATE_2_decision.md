# ARCH-CONV-PKGB-1 — Gate 1 / Gate 2 Decision Record

**Work ID:** `ARCH-CONV-PKGB-1`  
**Date opened:** 2026-08-02  
**Gate 1 recorded:** 2026-08-02  
**Gate 2 recorded:** 2026-08-02  
**Hardening pack:** `docs/architecture/ARCH-CONV-PKGB-1_hardening_pack.md`  
**Medical decision register:** `docs/architecture/ARCH-CONV-PKGB-1_medical_decision_register.yaml`  
**Implementation status:** **AUTHORISED** — Gate 1 and Gate 2 recorded; runtime Phase 1 may proceed under the active Automation Bus work package

## Gate references

| Gate | Reference | Status |
|---|---|---|
| Gate 1 — Head of Medical Research | `ARCH-CONV-PKGB-1-GATE1-HMR-2026-08-02` | `APPROVED_WITH_NARROWING` |
| Gate 2 — Anthony (project authority) | `ARCH-CONV-PKGB-1-GATE2-ANTHONY-2026-08-02` | `APPROVED` |

## Decision authority split

- **Head of Medical Research (Gate 1)** is the source of the medical judgement confirming FOLD_SUPPRESS implementation boundaries.
- **Anthony (Gate 2)** ratifies proceed/hold for project authority; Anthony is **not** the source of medical judgement.

## Register state

```text
register_state: GATES_APPROVED_RUNTIME_AUTHORISED
gate1_status: APPROVED_WITH_NARROWING
gate2_status: APPROVED
runtime_changes_authorised: true
```

---

## Gate 1 approved disposition (`ARCH-CONV-PKGB-1-GATE1-HMR-2026-08-02`)

### Decision

- **Decision ID:** `ARCH-CONV-PKGB-1-GATE1-HMR-2026-08-02`
- **Decision:** `APPROVED_WITH_NARROWING`

### Q1–Q7 answers

| Question | Answer |
|---|---|
| Q1 — FOLD_SUPPRESS retention | `CONFIRMED` — `signal_homocysteine_elevation_context` remains `FOLD_SUPPRESS` |
| Q2 — Independent WHY ownership/emission | `CONFIRMED` — **prohibited** |
| Q3 — New hypothesis / replacement narrative | `CONFIRMED` — **prohibited** |
| Q4 — `signal_homocysteine_high` compiled content | `CONFIRMED` — **unchanged** |
| Q5 — Bare-key resolver correction | `CONFIRMED` — **mechanical authority handling only** |
| Q6 — HbA1c / urate changes | `CONFIRMED` — **assertion alignment only** |
| Q7 — L-04 / L-05 / L-06 product-policy | `CONFIRMED` — **out of scope** |

### Narrowing (resolver)

- **Resolver scope:** the five Phase 0-confirmed all-`LEGACY_RETIRED`, zero-`COMPILED_ACTIVE` pilot families:
  - `signal_ldl_high`
  - `signal_hdl_low`
  - `signal_total_cholesterol_high`
  - `signal_hgb_low`
  - `signal_hepatic_alt_context`
- **Governed skip** permitted only where all relevant authority rows are unambiguously retired/non-owning.
- **Genuine ambiguity or missing governance** must continue to **fail closed**.
- **No** new compiled authority or medical content for LDL, HDL, total cholesterol, haemoglobin-low, or hepatic ALT context.

### Homocysteine exclusivity boundary

- Elevation-context: `FOLD_SUPPRESS`
- Independent WHY ownership/emission: prohibited
- New hypothesis or replacement narrative: prohibited
- `signal_homocysteine_high` compiled content: unchanged

### Assertion alignment only

- HbA1c → `hyp_hba1c_elevated_glycaemia_context`
- Urate → `hyp_urate_elevated_non_causal_context`
- No runtime content change to satisfy old tests

### Explicitly out of scope

- L-04 `why_engine_fallback_v1`
- L-05 `_why_template`
- L-06 family aggregation product-policy

### Mechanism preference

Deferred to implementation under the medical boundary above (Phase 0 Options A/B/C), provided exclusivity and narrowing are satisfied.

### Gate 1 decision block (recorded)

```text
gate1_reference: ARCH-CONV-PKGB-1-GATE1-HMR-2026-08-02
decision: APPROVED_WITH_NARROWING
q1_fold_suppress: CONFIRMED
q2_no_independent_why_emit: CONFIRMED
q3_no_new_hypothesis_or_narrative: CONFIRMED
q4_hcy_high_compiled_unchanged: CONFIRMED
q5_resolver_mechanical_only: CONFIRMED
q6_assertion_alignment_only: CONFIRMED
q7_no_l04_l05_l06_policy: CONFIRMED
resolver_scope: five_phase0_all_legacy_retired_zero_compiled_active_pilots
governed_skip_only_when_all_rows_unambiguously_retired_or_non_owning: true
genuine_ambiguity_or_missing_governance: fail_closed
no_new_compiled_authority_or_medical_content_for_ldl_hdl_tc_hgb_hepatic_alt: true
mechanism_preference: DEFER_TO_IMPLEMENTATION
```

---

## Gate 2 ratification (`ARCH-CONV-PKGB-1-GATE2-ANTHONY-2026-08-02`)

```text
gate2_reference: ARCH-CONV-PKGB-1-GATE2-ANTHONY-2026-08-02
decision: APPROVED
ratifies: ARCH-CONV-PKGB-1-GATE1-HMR-2026-08-02
signal_homocysteine_elevation_context: FOLD_SUPPRESS
independent_why_ownership_emission: prohibited
new_hypothesis_or_replacement_narrative: prohibited
signal_homocysteine_high_compiled_content: unchanged
bare_key_resolver_correction: mechanical_authority_handling_only
resolver_scope: five_phase0_all_legacy_retired_zero_compiled_active_pilots
governed_skip_only_when_all_rows_unambiguously_retired_or_non_owning: true
genuine_ambiguity_or_missing_governance: fail_closed
no_new_compiled_authority_or_medical_content_for_ldl_hdl_tc_hgb_hepatic_alt: true
hba1c_urate_changes: assertion_alignment_only
l04_l05_l06_product_policy: out_of_scope
runtime_changes_authorised: true
```

Gate 2 ratifies Gate 1 **exactly**. No medical disposition change.

---

## Authorised runtime Phase 1

Runtime Phase 1 is authorised:

1. Gate 1 answers Q1–Q7 on disk (**satisfied** — `ARCH-CONV-PKGB-1-GATE1-HMR-2026-08-02`); and  
2. Gate 2 records `APPROVED` ratifying that exact Gate 1 (**satisfied** — `ARCH-CONV-PKGB-1-GATE2-ANTHONY-2026-08-02`); and  
3. `runtime_changes_authorised: true` is written into this file and the medical decision register (**satisfied**).

### Still prohibited

- Changing `signal_homocysteine_high` compiled medical content
- Creating independent WHY for elevation-context
- Creating new compiled authority / medical content for the five zero-compiled pilots
- L-04 / L-05 / L-06 product-policy decisions
- Package C replay/versioning
- Package / PSI / scoring / frontend activation changes beyond WHY exclusivity
