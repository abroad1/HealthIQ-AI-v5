# ARCH-CONV-I — Gate 1 / Gate 2 Decision Record

**Work ID:** `ARCH-CONV-I`  
**Date opened:** 2026-08-02  
**Hardening pack:** `docs/architecture/ARCH-CONV-I_hardening_pack.md`  
**Medical decision register:** `docs/architecture/ARCH-CONV-I_medical_decision_register.yaml`  
**Implementation status:** **NONE** — Phase 0 mapping only; sprint is not implemented, complete, or merged

## Gate references

| Gate | Reference | Status |
|---|---|---|
| Gate 1 — Head of Medical Research | `ARCH-CONV-I-GATE1-HMR-PENDING` | `PENDING` |
| Gate 2 — Anthony (project authority) | `ARCH-CONV-I-GATE2-ANTHONY-PENDING` | `PENDING` |

## Decision authority split

- **Head of Medical Research (Gate 1)** decides medical disposition: Outcome A vs B, exact activation key if A, `why_role`, wording boundaries, CRP disposition, threshold-transfer prohibition, prohibited claims.
- **Head of Architecture** advises readiness for Anthony Gate 2 after Gate 1 is recorded (including Outcome A multi-frame / registry-target hazards).
- **Anthony (Gate 2)** is human project authority for proceed/hold. Anthony is **not** the source of medical judgement.

## Register state

```text
register_state: PHASE_0_MAPPED_AWAITING_GATE_1_AND_GATE_2
gate1_status: PENDING
gate2_status: PENDING
```

## Exact proposed decisions for Gate 1 / Gate 2

### Choice 1 — Outcome A or Outcome B

Gate 1 must select exactly one:

| Outcome | Name | Expected delta |
|---|---|---|
| **A** | Narrow `MAP_AND_COMPILE` | `+1 COMPILED_ACTIVE` / `+1 LEGACY_RETIRED` (minimum; sibling rows may be required) |
| **B** | `RETIRE_WITHOUT_SUCCESSOR` | `+0 COMPILED_ACTIVE` / `+1 LEGACY_RETIRED` |

No other disposition is authorised without re-scoping.

### Choice 2 — If Outcome A: exact activation key

Phase 0 presents two hepatocellular identities; Gate 1 must name one:

| Candidate | Status | Phase 0 note |
|---|---|---|
| `signal_alt_high::inv_alt_high_r_value_hepatocellular_biochemical_pattern` | **Live activated** (E2 Pass 3 successor) | **Recommended compile target** |
| `signal_alt_high::inv_alt_high_hepatocellular_injury` | **SUPERSEDED** | Must not be compiled / must not be reactivated |

### Choice 3 — If Outcome A: `why_role`

Proposed: `morphology_context` (flat).  
Alternative for Gate 1 only: narrowed `causal` limited to hepatocellular enzyme-leakage / cell-stress pattern with identical prohibitions.

### Choice 4 — CRP / inflammatory-coupling disposition

Legacy hypothesis `alt_inflammatory_coupling_context_v1` has **no** canonical `signal_alt_high` counterpart.

Gate 1 must record one of:

- **Exclude / do not transfer** (required under Outcome A as written in the sprint prompt); or  
- **Block pending new canonical research** (still no compile).

Compiling CRP content without new canonical research is prohibited.

### Choice 5 — Threshold transfer

Confirm: legacy hard-coded AST>45 / GGT>60 / ALP>130 / bilirubin>20 **must not transfer** into compiled WHY or retained WHY behaviour.

### Choice 6 — Prohibited claims (must confirm)

- No consumer Hy’s Law / DILI diagnosis  
- No MASLD / steatosis / fibrosis diagnosis from ALT alone  
- No treatment directives  
- No chronicity inference  
- No disease-specific cause attribution beyond ratified contextual limits  
- No runtime alias between `signal_hepatic_alt_context` and `signal_alt_high`

### Choice 7 — WHY-only retirement key (both outcomes)

Retire for WHY ownership only:

`signal_hepatic_alt_context::inv_alt_context`

Package-layer activation and PSI unchanged; no package deletion.

### Adjacent frames unchanged

- Mixed / cholestatic / muscle / metabolic `signal_alt_high` frames  
- Bilirubin-severity override-only posture  
- ALP / GGT compiled-WHY authority  
- R-value formula and bands  

### Gate 1 required recorded values

```text
OUTCOME_A_MAP_AND_COMPILE | OUTCOME_B_RETIRE_WITHOUT_SUCCESSOR | BLOCKED
```

If Outcome A, decision record must also state:

- approved activation key;
- approved `why_role`;
- approved claim / wording boundary;
- CRP disposition;
- confirmation that hard-coded thresholds do not transfer;
- prohibited claims;
- acknowledgment of Outcome A implementation hazards (registry target / sibling fail-closed) or explicit narrowing that removes them;
- retired WHY activation key.

### Gate 2 required recorded values

```text
APPROVED | BLOCKED
```

Gate 2 must ratify Gate 1 exactly.

## Non-claims

- This document does **not** authorise implementation.
- Gate recording (when later approved) still requires Automation Bus resume under a gate-consistent hardened prompt before runtime changes.
- Retrospective ratification is forbidden.
- No compiled artefact, authority-register edit, legacy WHY retirement, or runtime behaviour change may occur while gates are PENDING.

## Required next human actions

1. GPT / Head of Medical Research: record Gate 1 against Outcome A or Outcome B with the required fields above.
2. Anthony: record Gate 2 after Gate 1.
3. Commit both gate statuses on disk (replace `PENDING` references).
4. Resume `ARCH-CONV-I` for implementation only if disposition matches this pack, or revise prompt + re-harden if material change is required.
