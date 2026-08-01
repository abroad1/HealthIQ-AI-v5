# ARCH-CONV-H — Gate 1 / Gate 2 Decision Record

**Work ID:** `ARCH-CONV-H`  
**Date opened:** 2026-08-01  
**Gate 1 recorded:** 2026-08-01  
**Gate 2 recorded:** 2026-08-01  
**Hardening pack:** `docs/architecture/ARCH-CONV-H_hardening_pack.md`  
**Medical decision register:** `docs/architecture/ARCH-CONV-H_medical_decision_register.yaml`  
**Implementation status:** **AUTHORISED** — Gate 1 and Gate 2 recorded; runtime compiled-WHY implementation may proceed under the active Automation Bus work package

## Gate references

| Gate | Reference | Status |
|---|---|---|
| Gate 1 — Head of Medical Research | `ARCH-CONV-H-GATE1-HMR-2026-08-01` | `APPROVED_WITH_NARROWING` |
| Gate 2 — Anthony (project authority) | `ARCH-CONV-H-GATE2-ANTHONY-2026-08-01` | `APPROVED` |

## Decision authority split

- **Head of Medical Research (Gate 1)** is the source of the medical judgement and narrowing.
- **Anthony (Gate 2)** ratifies proceed/hold for project authority; Anthony is **not** the source of medical judgement.

## Register state

```text
register_state: GATES_APPROVED_RUNTIME_AUTHORISED
gate1_status: APPROVED_WITH_NARROWING
gate2_status: APPROVED
runtime_changes_authorised: true
```

## Gate 1 approved disposition (`ARCH-CONV-H-GATE1-HMR-2026-08-01`)

### Canonical authority

- **Approved activation key:** `signal_hba1c_high::inv_hba1c_high_glycaemia`
- **Approved `why_role`:** `morphology_context` (flat; no conditional branch)
- **Canonical package:** `pkg_s24_hba1c_high_glycaemia`

### WHY-only retirement

- **Retired competing activation key:** `signal_hba1c_high::inv_hba1c_high_diabetes_range_hyperglycemia`
- **Disposition:** `LEGACY_RETIRED_FOR_WHY_ONLY`
- Package-layer and PSI status unchanged; no package deletion

### Diabetes-range escalation

- HbA1c `>= 48 mmol/mol`: **diabetes-range concern requiring clinical confirmation only**
- Not an unqualified diabetes diagnosis from HbA1c alone

### TG/HDL metabolic context

- Subordinate metabolic-pattern context only
- **No metabolic-syndrome diagnosis**

### Prohibited claims

- Treatment directives
- Chronicity inference
- Diabetes subtype
- Complications
- Causal attribution
- Diagnosis from HbA1c alone

### Adjacent identities unchanged

- `signal_hba1c_pct_high`
- `signal_glucose_dysregulation_hba1c_context`
- `signal_hba1c_low` (out of scope)

### Expected authority delta

- `+1 COMPILED_ACTIVE`
- `+1 LEGACY_RETIRED`

## Gate 2 ratification (`ARCH-CONV-H-GATE2-ANTHONY-2026-08-01`)

```text
decision: APPROVED
ratifies: ARCH-CONV-H-GATE1-HMR-2026-08-01
approved_authority: signal_hba1c_high::inv_hba1c_high_glycaemia
approved_why_role: morphology_context
why_only_retirement: signal_hba1c_high::inv_hba1c_high_diabetes_range_hyperglycemia
hba1c_gte_48: diabetes_range_concern_requiring_clinical_confirmation_only
tg_hdl: subordinate_metabolic_pattern_context_only
prohibited_claims_and_adjacent_identities: unchanged_from_gate1
runtime_changes_authorised: true
```

## Non-claims

- Retrospective ratification is forbidden (both gates were recorded before implementation).
- Raw S24 directive implications wording must not be compiled verbatim.
- Packages / PSI / adjacent identities remain unchanged.

## Next action

Resume `ARCH-CONV-H` implementation under the active Automation Bus work package token, matching this disposition exactly.
