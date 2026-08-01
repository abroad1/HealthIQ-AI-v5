# ARCH-CONV-E3 — Gate 2 Human Ratification

**Reference:** `ARCH-CONV-E3-GATE2-ANTHONY-2026-08-01`  
**Work ID:** `ARCH-CONV-E3`  
**Ratifier:** Anthony  
**Date:** 2026-08-01  
**Status:** RATIFIED

Anthony explicitly ratifies the Head of Medical Research Gate 1 decisions recorded under:

```text
ARCH-CONV-E3-GATE1-HMR-2026-08-01
```

See `docs/architecture/ARCH-CONV-E3_medical_decision_register.yaml`.

## Ratified decisions

1. Activate cholestatic R≤2 as subordinate ALT biochemical-pattern context.
2. Do **not** add `signal_alt_high` as `liver_injury_axis` supporting family (contract-safe subordination).
3. Activate muscle lab-only (`creatine_kinase` above lab max gate).
4. Activate metabolic lab-only (compound any_of metabolic lab corroboration).
5. Represent bilirubin severity as override/escalation only; keep package withheld.
6. Leave user-context corroboration and very-high-ALT numeric suppress as unresolved blockers.
7. Preserve E2 hepatocellular/mixed behaviour and ALP/GGT `liver_injury_axis`.
8. No consumer Hy’s Law diagnosis wording.

## Authorisation boundary

This ratification authorises governed merge and closure of ARCH-CONV-E3 within the already-implemented runtime authority. It does not authorise:

- inventing a very-high-ALT numeric threshold;
- inventing a runtime user-context contract;
- independent activation of the bilirubin severity package as a competing primary;
- reactivating S24 or former Batch 5 inferred ALT keys;
- frontend medical inference;
- reading raw Pass 3 research at runtime;
- changes to medical rules, package content, or unresolved blocker dispositions beyond the ratified Gate 1 design already implemented.
