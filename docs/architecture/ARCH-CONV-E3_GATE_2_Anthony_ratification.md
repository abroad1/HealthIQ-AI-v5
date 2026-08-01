# ARCH-CONV-E3 — Gate 2 Human Ratification (PENDING)

**Reference:** `ARCH-CONV-E3-GATE2-ANTHONY-PENDING`  
**Work ID:** `ARCH-CONV-E3`  
**Ratifier:** Anthony  
**Date:** pending  
**Status:** PENDING

This document records that Gate 2 ratification is **required before merge** and has
**not** been executed. Cursor must not forge ratification.

Gate 1 decisions to be ratified are recorded under:

```text
ARCH-CONV-E3-GATE1-HMR-2026-08-01
```

See `docs/architecture/ARCH-CONV-E3_medical_decision_register.yaml`.

## Decisions awaiting ratification

1. Activate cholestatic R≤2 as subordinate ALT biochemical-pattern context.
2. Do **not** add `signal_alt_high` as `liver_injury_axis` supporting family (contract-safe subordination).
3. Activate muscle lab-only (`creatine_kinase` above lab max gate).
4. Activate metabolic lab-only (compound any_of metabolic lab corroboration).
5. Represent bilirubin severity as override/escalation only; keep package withheld.
6. Leave user-context corroboration and very-high-ALT numeric suppress as unresolved blockers.
7. Preserve E2 hepatocellular/mixed behaviour and ALP/GGT `liver_injury_axis`.

## Authorisation boundary when ratified

Ratification would authorise governed merge of ARCH-CONV-E3 within the implemented
runtime authority. It would not authorise:

- inventing a very-high-ALT numeric threshold;
- inventing a runtime user-context contract;
- independent activation of the bilirubin severity package as a competing primary;
- reactivating S24 or former Batch 5 inferred ALT keys;
- frontend medical inference;
- reading raw Pass 3 research at runtime.
