# ARCH-CONV-F — Gate 1 / Gate 2 Decision Record

**Work ID:** `ARCH-CONV-F`  
**Date:** 2026-08-01  
**Hardening pack:** `docs/architecture/ARCH-CONV-F_hardening_pack.md`  
**Implementation status:** **NONE** — gates recorded only; sprint is not implemented, complete, or merged

## Gate references

| Gate | Reference | Status |
|---|---|---|
| Gate 1 — Head of Medical Research | `ARCH-CONV-F-GATE1-HMR-2026-08-01` | `APPROVED_WITH_NARROWING` |
| Gate 2 — Anthony (project authority) | `ARCH-CONV-F-GATE2-ANTHONY-2026-08-01` | `APPROVED` |

## Decision authority split

- **Head of Medical Research (Gate 1)** is the source of the medical judgement and narrowing for the two haematology WHY frames below.
- **Head of Architecture** advised readiness for Anthony Gate 2 on the hardened Phase 0 design.
- **Anthony (Gate 2)** approved ARCH-CONV-F to proceed on the recommendation of the Head of Medical Research and Head of Architecture. Anthony is the human project authority and is **not** treated as the source of the medical judgement.

## Register state

```text
register_state: GATE_1_AND_GATE_2_RECORDED_AWAITING_PROMPT_HARDENING
gate1_status: APPROVED_WITH_NARROWING
gate2_status: APPROVED
```

## Approved medical dispositions

### 1. `signal_hemoglobin_low::inv_hgb_low_anemia`

- `why_role: causal`
- Causal scope limited to anaemia / reduced oxygen-carrying capacity
- MCV and RDW are non-owning morphology/context only
- No independent underproduction aetiology claim
- Hemoglobin `<80 g/L` retained as concern escalation only
- Not a universal severe-anaemia definition
- Not an automatic transfusion threshold
- Not a treatment recommendation
- `pkg_kb52c_hgb_low_normocytic_underproduction_context` retired for WHY ownership only
- Separate oxygen-carrying PSI research gap remains open

### 2. `signal_ferritin_high::inv_ferritin_high_overload`

- `why_role: morphology_context`
- Flat and non-causal under every data state
- No haemochromatosis diagnosis
- No causal iron-overload claim
- CRP, ALT, serum iron and transferrin saturation may enrich context only
- Transferrin saturation is additional non-causal context enrichment only
- Missing corroboration fails closed to bare ferritin-elevation context
- Ferritin `>1000 µg/L` retained as concern escalation only
- `pkg_kb52c_ferritin_high_inflammatory_hyperferritinemia` retired for WHY ownership only
- `pkg_kb52c_ferritin_high_iron_overload_context` retired for WHY ownership only
- Package-layer and PSI status unchanged

## Explicit exclusions

- Do not compile or activate `signal_ferritin_low`, `signal_transferrin_high`, `signal_transferrin_low`, or `signal_iron_deficiency_context` as independent WHY owners under this work
- Do not compile `signal_iron_overload_context` as an independently owning frame
- Do not compile `signal_oxygen_transport_capacity`
- Do not touch `signal_urate_high`, `signal_hba1c_high`, or any ALT `signal_id`
- Do not resolve or promote the primary oxygen-carrying PSI research gap
- Do not add biomarkers, derived metrics, thresholds, rankings, or medical rules beyond the cited canonical / Pass 3 research already scoped in the hardening pack
- Do not alter frontend behaviour
- Do not permit any data state to upgrade ferritin-high to a causal `why_role`
- Do not revoke existing PSI activations or delete packages (WHY-ownership retirement only where recorded)

## Implementation boundary (explicit non-claims)

This record does **not** authorise or claim:

- that ARCH-CONV-F is implemented;
- that ARCH-CONV-F is complete;
- that ARCH-CONV-F is merged;
- any runtime, package, test, signal-library, PSI, or frontend change;
- Automation Bus kernel start.

**Mandatory before implementation:** Claude Code must produce final prompt `HARDENED` status, and Automation Bus start must succeed. Gate 1 / Gate 2 recording alone is insufficient to begin Core Engine implementation.
