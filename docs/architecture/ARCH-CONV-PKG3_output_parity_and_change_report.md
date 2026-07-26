# ARCH-CONV-PKG3 — Output Parity and Change Report

**Work ID:** `ARCH-CONV-PKG3`  
**Status:** **COMPLETE for Gate C continuation (Phases 4–5)**  
**Authority:** Anthony-ratified medical-review pack (2026-07-26)

Every output change below is classified as:

```text
intended | required revision | regression | unresolved
```

| Frame | Authority before | Authority after | Output delta | Classification | Aligned to ratified pack? |
|---|---|---|---|---|---|
| Vit D deficiency | Compiled (signal-promoted) + legacy YAML reachable via registry | Compiled sole runtime authority; legacy on disk / non-selected | Same compiled hypothesis id retained; summary_template path unchanged | intended | Yes — RETIREMENT_CONFIRMATION_ONLY |
| Hcy B-vitamin | Shared legacy `hcy_hypotheses_v1.yaml` family | Per-key compiled artefact (2 approved hyps) | Legacy inflammation/renal hyps excluded from this frame; consumer boundary applied | required revision | Yes |
| Hcy metabolic | Would have shared legacy / catch-all risk | **REJECTED — inactive** | No WHY finding; no WHY-engine fallback | intended | Yes — REJECT |
| Hcy renal | Shared legacy family | Per-key compiled artefact (2 approved hyps) | Renal + combined hyps only; CKD inference constrained in caveats | required revision | Yes |
| MCV macrocytosis anchor | Shared legacy family | Per-key compiled anchor | Morphology-only; no duplicate causal ranking with Frames 6/7 | required revision | Yes |
| MCV megaloblastic | Shared legacy family | Per-key compiled (2 hyps) | Nutrient/B12–folate pattern only | required revision | Yes |
| MCV non-megaloblastic | Shared legacy family | Per-key compiled (2 hyps) | Alcohol/hepatic + constrained other differential; marrow wording clinician-facing | required revision | Yes |
| Free T3 low | Legacy `free_t3_low_hypotheses_v1.yaml` | Per-key compiled (2 hyps) | NTI / conversion pattern with no-treatment caveats | required revision | Yes |
| TPO autoimmune hypothyroid | Shared TPO legacy | Per-key compiled (2 hyps) | Overt vs subclinical split preserved | required revision | Yes |
| TPO euthyroid risk | Shared TPO legacy / previously unwired richness | Per-key compiled (2 hyps) | Euthyroid risk wording; no current-hypothyroid implication | required revision | Yes |

## Unexplained clinical drift

None identified for the pilot cohort under the ratified dispositions.

## STOP assessment (parity)

| Trigger | Result |
|---|---|
| Unexplained regression vs ratified pack | Not triggered |
| Rejected frame emitting causal WHY | Not triggered (gate + unit covered) |
| Dual compiled+legacy for same activation_key | Not triggered |
