# ARCH-CONV-H — Gate 1 / Gate 2 Decision Record

**Work ID:** `ARCH-CONV-H`  
**Date opened:** 2026-08-01  
**Gate 1 recorded:** 2026-08-01  
**Hardening pack:** `docs/architecture/ARCH-CONV-H_hardening_pack.md`  
**Medical decision register:** `docs/architecture/ARCH-CONV-H_medical_decision_register.yaml`  
**Implementation status:** **BLOCKED PENDING GATE 2** — Gate 1 recorded; no compiled-WHY implementation until Anthony Gate 2 ratification is on disk

## Gate references

| Gate | Reference | Status |
|---|---|---|
| Gate 1 — Head of Medical Research | `ARCH-CONV-H-GATE1-HMR-2026-08-01` | `APPROVED_WITH_NARROWING` |
| Gate 2 — Anthony (project authority) | `ARCH-CONV-H-GATE2-ANTHONY-PENDING` | `PENDING` |

## Decision authority split

- **Head of Medical Research (Gate 1)** is the source of the medical judgement and narrowing recorded below.
- **Head of Architecture** advises readiness for Anthony Gate 2 after Gate 1.
- **Anthony (Gate 2)** is human project authority for proceed/hold. Anthony is **not** the source of medical judgement.

## Register state

```text
register_state: GATE_1_RECORDED_AWAITING_GATE_2
gate1_status: APPROVED_WITH_NARROWING
gate2_status: PENDING
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
- Chronicity inference beyond the marker’s supported exposure window wording if separately authorised later
- Diabetes subtype
- Complications
- Causal attribution
- Diagnosis from HbA1c alone

### Adjacent identities unchanged

- `signal_hba1c_pct_high`
- `signal_glucose_dysregulation_hba1c_context`
- `signal_hba1c_low` (out of scope)

### Expected authority delta (subject to Gate 2)

- `+1 COMPILED_ACTIVE`
- `+1 LEGACY_RETIRED`

## Gate 2 status

```text
ARCH-CONV-H-GATE2-ANTHONY-PENDING
status: PENDING
required_values: APPROVED | BLOCKED
```

No implementation may begin until Gate 2 is repository-recorded as `APPROVED` and matches this Gate 1 disposition.

## Non-claims

- Gate 1 recording alone does **not** authorise implementation.
- Retrospective ratification is forbidden.
- Raw S24 directive implications wording must not be compiled verbatim.

## Required next human action

1. Anthony: record Gate 2 (`APPROVED` or `BLOCKED`) on disk.
2. Only after Gate 2 `APPROVED`, resume `ARCH-CONV-H` implementation under the active Automation Bus work package.
