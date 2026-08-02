# ARCH-CONV-I — Gate 1 / Gate 2 Decision Record

**Work ID:** `ARCH-CONV-I`  
**Date opened:** 2026-08-02  
**Gate 1 recorded:** 2026-08-02  
**Hardening pack:** `docs/architecture/ARCH-CONV-I_hardening_pack.md`  
**Medical decision register:** `docs/architecture/ARCH-CONV-I_medical_decision_register.yaml`  
**Implementation status:** **BLOCKED PENDING GATE 2** — Gate 1 recorded; no compiled-WHY implementation until Anthony Gate 2 ratification is on disk

## Gate references

| Gate | Reference | Status |
|---|---|---|
| Gate 1 — Head of Medical Research | `ARCH-CONV-I-GATE1-HMR-2026-08-02` | `APPROVED_WITH_NARROWING` |
| Gate 2 — Anthony (project authority) | `ARCH-CONV-I-GATE2-ANTHONY-PENDING` | `PENDING` |

## Decision authority split

- **Head of Medical Research (Gate 1)** is the source of the medical judgement and narrowing recorded below.
- **Head of Architecture** advises readiness for Anthony Gate 2 after Gate 1 (including Outcome A multi-frame / registry-target hazards).
- **Anthony (Gate 2)** is human project authority for proceed/hold. Anthony is **not** the source of medical judgement.

## Register state

```text
register_state: GATE_1_RECORDED_AWAITING_GATE_2
gate1_status: APPROVED_WITH_NARROWING
gate2_status: PENDING
runtime_changes_authorised: false
```

## Gate 1 approved disposition (`ARCH-CONV-I-GATE1-HMR-2026-08-02`)

### Outcome

- **Approved outcome:** `MAP_AND_COMPILE` (Outcome A)
- Outcome B withdrawn for this decision

### Canonical authority

- **Approved activation key:** `signal_alt_high::inv_alt_high_r_value_hepatocellular_biochemical_pattern`
- **Approved `why_role`:** `morphology_context` (flat; no conditional branch)
- **Canonical package:** `pkg_kb52c_alt_high_hepatocellular_injury_pattern`
- Superseded S24 key `signal_alt_high::inv_alt_high_hepatocellular_injury` must not be compiled or reactivated

### WHY-only retirement

- **Retired activation key:** `signal_hepatic_alt_context::inv_alt_context`
- **Disposition:** `LEGACY_RETIRED_FOR_WHY_ONLY`
- Package-layer and PSI status unchanged; no package deletion

### CRP / inflammatory-coupling

- Legacy hypothesis `alt_inflammatory_coupling_context_v1`: **excluded**
- No compile and no transfer

### Threshold transfer

- Legacy hard-coded AST/GGT/ALP/bilirubin thresholds: **prohibited from transfer**

### Preserve unchanged

- E2/E3 R-value behaviour
- Contextual-frame authority
- Package / PSI / activation behaviour

### Prohibited claims

- Runtime alias between `signal_hepatic_alt_context` and `signal_alt_high`
- Consumer Hy’s Law / DILI diagnosis
- MASLD / steatosis / fibrosis diagnosis from ALT alone
- Treatment directives
- Chronicity inference
- Unsupported causal claims

### Expected authority delta (subject to Gate 2)

- `+1 COMPILED_ACTIVE` (minimum)
- `+1 LEGACY_RETIRED` (legacy WHY identity)
- Sibling skip-class rows may still be required if `signal_alt_high` is piloted (implementation hazard remains for Gate 2 / implementation resume)

## Gate 2 status

```text
ARCH-CONV-I-GATE2-ANTHONY-PENDING
status: PENDING
required_values: APPROVED | BLOCKED
```

No implementation may begin until Gate 2 is repository-recorded as `APPROVED` and matches this Gate 1 disposition.

## Non-claims

- Gate 1 recording alone does **not** authorise implementation (`runtime_changes_authorised: false`).
- Retrospective ratification is forbidden.
- No compiled artefact, authority-register edit, legacy WHY retirement, or runtime behaviour change may occur while Gate 2 is PENDING.

## Required next human action

1. Anthony: record Gate 2 (`APPROVED` or `BLOCKED`) on disk.
2. Only after Gate 2 `APPROVED`, resume `ARCH-CONV-I` implementation under the active Automation Bus work package.
