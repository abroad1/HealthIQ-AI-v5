# ARCH-CONV-C — Gate 2 Human Ratification

**Reference:** `ARCH-CONV-C-GATE2-ANTHONY-2026-07-30`  
**Work ID:** `ARCH-CONV-C`  
**Ratifier:** Anthony  
**Date:** 2026-07-30  
**Status:** RATIFIED — PHASE 2 AUTHORISED

Anthony explicitly ratifies the Head of Medical Research Gate 1 decisions recorded under:

```text
ARCH-CONV-C-GATE1-HMR-2026-07-30
```

## Ratified decisions

1. `signal_alp_high::inv_alp_high_bone_biliary`
   - `APPROVE_WITH_NARROWING`
   - ALP may support a possible cholestatic/hepatobiliary biochemical pattern only when GGT is also high.
   - Isolated ALP, normal GGT or missing GGT must not emit hepatobiliary causal WHY.

2. `signal_ggt_high::inv_ggt_high_hepatic`
   - `APPROVE_WITH_NARROWING`
   - `CONTEXT_ONLY_NON_CAUSAL`
   - GGT may support hepatic-source attribution when ALP is high but must not generate causal liver, alcohol, medication or metabolic-disease claims.

3. `liver_injury_axis`
   - `APPROVE_WITH_NARROWING`
   - Medical concept narrowed to `cholestatic_source_axis`.
   - ALP is primary only when ALP and GGT are both high.
   - GGT remains supporting and non-causal.
   - Concordant and discordant behaviour must follow the ratified deterministic policy.

4. All four Pass 3 candidates
   - `DEFER_EVIDENCE_INSUFFICIENT`
   - No separate compile or authority promotion.

5. Bilirubin
   - Supporting severity/excretory context only.
   - No WHY authority granted in ARCH-CONV-C.

6. ALT, AST, bilirubin/hyperbilirubinemia and ALP-low
   - Remain excluded and unchanged.

## Authorisation boundary

Phase 2 implementation is authorised only within the ratified medical decisions, collision-policy decisions, safeguards, legacy-disposition conditions, STOP C requirements and explicit non-goals of the ARCH-CONV-C prompt.

This ratification does not authorise:

- ALT identity resolution or migration;
- AST WHY creation;
- bilirubin/hyperbilirubinemia migration;
- ALP-low migration;
- frontend medical logic;
- physical deletion of legacy assets;
- merge without successful STOP C, Automation Bus finish, independent audit and explicit human merge authority.
