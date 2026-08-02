# ARCH-CONV-I — Gate 1 / Gate 2 Decision Record

**Work ID:** `ARCH-CONV-I`  
**Date opened:** 2026-08-02  
**Gate 1 recorded:** 2026-08-02  
**Gate 2 recorded:** 2026-08-02  
**Hardening pack:** `docs/architecture/ARCH-CONV-I_hardening_pack.md`  
**Medical decision register:** `docs/architecture/ARCH-CONV-I_medical_decision_register.yaml`  
**Implementation status:** **AUTHORISED** — Gate 1 and Gate 2 recorded; runtime compiled-WHY implementation may proceed under the active Automation Bus work package

## Gate references

| Gate | Reference | Status |
|---|---|---|
| Gate 1 — Head of Medical Research | `ARCH-CONV-I-GATE1-HMR-2026-08-02` | `APPROVED_WITH_NARROWING` |
| Gate 2 — Anthony (project authority) | `ARCH-CONV-I-GATE2-ANTHONY-2026-08-02` | `APPROVED` |

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

## Gate 1 approved disposition (`ARCH-CONV-I-GATE1-HMR-2026-08-02`)

### Outcome

- **Approved outcome:** `MAP_AND_COMPILE` (Outcome A)

### Canonical authority

- **Approved activation key:** `signal_alt_high::inv_alt_high_r_value_hepatocellular_biochemical_pattern`
- **Approved `why_role`:** `morphology_context` (flat; no conditional branch)
- **Canonical package:** `pkg_kb52c_alt_high_hepatocellular_injury_pattern`

### WHY-only retirement

- **Retired activation key:** `signal_hepatic_alt_context::inv_alt_context`
- **Disposition:** `LEGACY_RETIRED_FOR_WHY_ONLY`
- Package-layer and PSI status unchanged; no package deletion

### CRP / inflammatory-coupling

- Legacy hypothesis `alt_inflammatory_coupling_context_v1`: **excluded** — no compile and no transfer

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

### Expected authority delta

- `+1 COMPILED_ACTIVE` (hepatocellular)
- `+1 LEGACY_RETIRED` (legacy WHY identity)
- Sibling skip-class rows required for live non-compiled `signal_alt_high` frames when piloted

## Gate 2 ratification (`ARCH-CONV-I-GATE2-ANTHONY-2026-08-02`)

```text
decision: APPROVED
ratifies: ARCH-CONV-I-GATE1-HMR-2026-08-02
approved_outcome: MAP_AND_COMPILE
approved_authority: signal_alt_high::inv_alt_high_r_value_hepatocellular_biochemical_pattern
approved_why_role: morphology_context
why_only_retirement: signal_hepatic_alt_context::inv_alt_context
crp: excluded_no_compile_no_transfer
hardcoded_thresholds: transfer_prohibited
preserve_e2_e3_package_psi_activation: true
prohibited_claims: unchanged_from_gate1
runtime_changes_authorised: true
```

## Non-claims

- Retrospective ratification is forbidden (both gates were recorded before implementation).
- Packages / PSI / adjacent E2/E3 frames remain unchanged at package layer.
- No runtime alias.

## Next action

Resume `ARCH-CONV-I` implementation under the active Automation Bus work package token, matching this disposition exactly.
