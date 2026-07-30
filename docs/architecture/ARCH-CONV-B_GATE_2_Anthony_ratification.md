# ARCH-CONV-B — Gate 2 Human Ratification

**Reference:** `ARCH-CONV-B-GATE2-ANTHONY-2026-07-30`  
**Work ID:** `ARCH-CONV-B`  
**Ratifier:** Anthony  
**Date:** 2026-07-30  
**Status:** RATIFIED — PHASE 2 AUTHORISED

Anthony explicitly ratifies the Head of Medical Research Gate 1 decisions recorded under:

```text
ARCH-CONV-B-GATE1-HMR-2026-07-30
```

## Ratified decisions

1. `signal_creatinine_high::inv_creatinine_high_renal`
   - `APPROVE_WITH_NARROWING`
   - bounded possible reduced renal-clearance / filtration-marker interpretation;
   - no CKD or AKI diagnosis from isolated creatinine;
   - no absorption or displacement of separate `signal_egfr_low` authority.

2. `signal_urea_high::inv_urea_high_renal`
   - `APPROVE_WITH_NARROWING`
   - `CONTEXT_ONLY_NON_CAUSAL`;
   - no standalone causal renal-impairment WHY from isolated urea.

3. Pass 3 package-only creatinine reduced-GFR candidate
   - `DEFER_EVIDENCE_INSUFFICIENT`;
   - no compile or authority promotion.

4. Pass 3 package-only urea prerenal/catabolic candidate
   - `DEFER_EVIDENCE_INSUFFICIENT`;
   - no compile or authority promotion.

5. eGFR boundary
   - separate future WHY authority preserved;
   - ARCH-CONV-B must not compile, alias, displace or retire eGFR WHY authority.

6. Urate
   - remains excluded from ARCH-CONV-B.

## Authorisation boundary

Phase 2 implementation is authorised only within the approved medical decisions, safeguards, legacy-disposition conditions, STOP C requirements and explicit non-goals of the ARCH-CONV-B prompt.

This ratification does not authorise:

- scope expansion;
- standalone eGFR WHY migration;
- urate migration;
- physical deletion of legacy assets;
- merge without successful STOP C, Automation Bus finish, independent audit and explicit human merge authority.
