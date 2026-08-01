# ARCH-CONV-H — Gate 1 / Gate 2 Decision Record

**Work ID:** `ARCH-CONV-H`  
**Date opened:** 2026-08-01  
**Hardening pack:** `docs/architecture/ARCH-CONV-H_hardening_pack.md`  
**Medical decision register:** `docs/architecture/ARCH-CONV-H_medical_decision_register.yaml`  
**Implementation status:** **NONE** — Phase 0 mapping only; sprint is not implemented, complete, or merged

## Gate references

| Gate | Reference | Status |
|---|---|---|
| Gate 1 — Head of Medical Research | `ARCH-CONV-H-GATE1-HMR-PENDING` | `PENDING` |
| Gate 2 — Anthony (project authority) | `ARCH-CONV-H-GATE2-ANTHONY-PENDING` | `PENDING` |

## Decision authority split

- **Head of Medical Research (Gate 1)** decides medical disposition: `why_role`, claim boundary, diabetes-range wording, TG/HDL metabolic-context use, prohibited claims, retained key, retired competing key.
- **Head of Architecture** advises readiness for Anthony Gate 2 after Gate 1 is recorded.
- **Anthony (Gate 2)** is human project authority for proceed/hold. Anthony is **not** the source of medical judgement.

## Register state

```text
register_state: PHASE_0_MAPPED_AWAITING_GATE_1_AND_GATE_2
gate1_status: PENDING
gate2_status: PENDING
```

## Exact proposed decisions for Gate 1 / Gate 2

### Canonical activation

- **Activation key:** `signal_hba1c_high::inv_hba1c_high_glycaemia`
- **Canonical package:** `pkg_s24_hba1c_high_glycaemia`
- **Proposed `why_role`:** `morphology_context` (flat; no conditional branch)
- **Alternative (Gate 1 only):** narrowed `causal` limited to sustained glycaemic-exposure / persistent hyperglycaemia pattern

### Medical boundary (proposed)

- HbA1c reflects sustained glycaemic exposure over the preceding ~8–12 weeks, not an independently proven cause of diabetes-related pathology.
- Compiled WHY may identify a persistent hyperglycaemia / glycaemic-exposure pattern supported by the canonical source.
- Diabetes-range escalation only using governed `hba1c >= 48 mmol/mol` with cautious wording.
- A single HbA1c result must not be presented as an unqualified diabetes diagnosis where confirmation, repeat testing, symptoms, or clinical assessment are required.
- Triglyceride/HDL (and ALT if used) may modify context only to the extent Gate 1 authorises from the canonical research.
- No treatment recommendation, medication instruction, complication diagnosis, unsupported chronicity, or unsupported causal claim.

### Competing frame

| Package | Activation key | Proposed disposition |
|---|---|---|
| `pkg_s24_hba1c_high_glycaemia` | `signal_hba1c_high::inv_hba1c_high_glycaemia` | Retain / compile |
| `pkg_kb52c_hba1c_high_diabetes_range_hyperglycemia` | `signal_hba1c_high::inv_hba1c_high_diabetes_range_hyperglycemia` | `LEGACY_RETIRED_FOR_WHY_ONLY` (package + PSI unchanged) |

### Adjacent identities (must remain unchanged)

- `signal_hba1c_pct_high` (separate signal family)
- `signal_glucose_dysregulation_hba1c_context` (separate signal_id)
- `signal_hba1c_low` (out of scope)

### Expected authority delta (if Gate 1 confirms)

- `+1 COMPILED_ACTIVE`
- `+1 LEGACY_RETIRED`

### Gate 1 required recorded values

```text
APPROVED | APPROVED_WITH_NARROWING | BLOCKED
```

Decision record must state:

- approved `why_role`;
- approved summary/claim boundary;
- approved diabetes-range escalation wording;
- approved use or exclusion of TG/HDL metabolic context;
- prohibited claims;
- retained activation key;
- retired competing WHY activation key.

### Gate 2 required recorded values

```text
APPROVED | BLOCKED
```

## Non-claims

- This document does **not** authorise implementation.
- Gate recording (when later approved) still requires Automation Bus resume under a gate-consistent hardened prompt before runtime changes.
- Retrospective ratification is forbidden.
- Raw S24 `explanation.implications` directive wording must not be compiled verbatim without Gate 1 narrowing.

## Required next human actions

1. GPT / Head of Medical Research: record Gate 1 against this proposed disposition.
2. Anthony: record Gate 2 after Gate 1.
3. Commit both gate statuses on disk (replace `PENDING` references).
4. Resume `ARCH-CONV-H` for implementation only if disposition matches this pack, or revise prompt + re-harden if material change is required.
