# ARCH-CONV-A — Wave 1 Thyroid Gate 1 / Gate 2 Decision

**Work ID:** `ARCH-CONV-A`  
**Wave:** 1 — Thyroid axis  
**Date (UTC):** 2026-07-28  
**Gate 1 reference:** `GPT-GATE1-ARCH-CONV-A-W1-THYROID-2026-07-28-v1`  
**Gate 2 reference:** `ANTHONY-GATE2-ARCH-CONV-A-W1-THYROID-2026-07-28-v1`

This artefact records the ratified medical boundaries for the five approved Wave 1
thyroid frames. It is durable decision authority for Package A implementation.

## Decision Summary

All five approved Wave 1 thyroid frames are ratified as:

```text
APPROVE_WITH_NARROWING
```

Approved frames:

```text
signal_tsh_high::inv_tsh_high_hypothyroidism
signal_tsh_low::inv_tsh_low_hyperthyroidism
signal_free_t3_high::inv_free_t3_high_t3_predominant_thyrotoxicosis
signal_free_t4_high::inv_free_t4_high_thyrotoxicosis_context
signal_free_t4_low::inv_free_t4_low_thyroid_hormone_deficiency
```

## Global Ratified Rules

These rules apply across the full Wave 1 thyroid set:

- One coherent thyroid-axis interpretation per panel.
- No duplicate causal prose from TSH and FT4/FT3 co-service.
- No simultaneous hypothyroid and thyrotoxic causal WHY.
- No simultaneous overt and subclinical classification.
- No diagnosis of hypothyroidism, hyperthyroidism, Graves' disease, Hashimoto's disease, or pituitary disease.
- No treatment or medication-adjustment recommendation.
- Preserve explicit caveats for medication, thyroid-hormone use, antithyroid treatment, recent illness, pregnancy, biotin, and assay interference where data are available.
- Consumer and clinician outputs must remain aligned.
- Layer C must not reconstruct thyroid medical meaning.

## Frame Boundaries

### 1. `signal_tsh_high::inv_tsh_high_hypothyroidism`

**Disposition:** `APPROVE_WITH_NARROWING`

Ratified boundary:

```text
TSH high + FT4 low
  -> primary thyroid-hormone-deficiency pattern

TSH high + FT4 normal
  -> raised-TSH / subclinical thyroid-dysfunction context only

TSH high + FT4 high
  -> fail closed for ordinary hypothyroid WHY
```

Implementation boundary:

- Preserve high-TSH axis context without broadening into diagnosis.
- Do not emit an ordinary hypothyroid causal WHY when FT4 is not low.
- Preserve medication, illness, pregnancy, biotin, and assay-interference caveats where available.

### 2. `signal_tsh_low::inv_tsh_low_hyperthyroidism`

**Disposition:** `APPROVE_WITH_NARROWING`

Ratified boundary:

```text
TSH low + FT4 high and/or FT3 high
  -> thyrotoxicosis-compatible pattern

TSH low + FT4 normal + FT3 normal
  -> low-TSH / subclinical thyroid-dysfunction context only

TSH low + FT4 low
  -> fail closed for ordinary hyperthyroid WHY
```

Implementation boundary:

- Preserve low-TSH context without broadening into disease attribution.
- Do not emit an ordinary hyperthyroid causal WHY when the broader hormone pattern is absent.
- Preserve caveats for medication, thyroid-hormone use, antithyroid treatment, recent illness, pregnancy, biotin, and assay interference where available.

### 3. `signal_free_t3_high::inv_free_t3_high_t3_predominant_thyrotoxicosis`

**Disposition:** `APPROVE_WITH_NARROWING`

Ratified boundary:

```text
FT3 high + TSH low/suppressed + FT4 not elevated
  -> T3-predominant thyroid-hormone excess pattern

FT3 high + non-suppressed TSH
  -> fail closed for T3-predominant thyrotoxicosis WHY

FT3 high + FT4 high
  -> broader thyrotoxicosis pattern, not a competing T3-specific causal explanation
```

Implementation boundary:

- Use this frame only for the T3-predominant lane.
- Suppress it when FT4 is also elevated so it does not compete with the broader FT4-high thyrotoxicosis interpretation.
- Do not imply Graves' disease or any other specific cause.

### 4. `signal_free_t4_high::inv_free_t4_high_thyrotoxicosis_context`

**Disposition:** `APPROVE_WITH_NARROWING`

Ratified boundary:

```text
FT4 high + TSH low/suppressed
  -> thyrotoxicosis-compatible pattern

FT4 high + TSH normal/high
  -> discordant-axis context; fail closed for ordinary thyrotoxicosis WHY
```

Implementation boundary:

- This is the broader thyrotoxicosis-compatible lane.
- Do not emit ordinary thyrotoxicosis WHY when TSH is not suppressed.
- Preserve medication, pregnancy, illness, biotin, and assay-interference caveats where available.

### 5. `signal_free_t4_low::inv_free_t4_low_thyroid_hormone_deficiency`

**Disposition:** `APPROVE_WITH_NARROWING`

Ratified boundary:

```text
FT4 low + TSH high
  -> primary thyroid-hormone-deficiency pattern

FT4 low + TSH low or inappropriately normal
  -> discordant-axis context; fail closed for ordinary primary-deficiency WHY
```

Implementation boundary:

- This is the ordinary primary thyroid-hormone-deficiency lane.
- Do not emit ordinary primary-deficiency WHY when the TSH response is not high.
- Preserve medication, pregnancy, illness, biotin, and assay-interference caveats where available.

## Explicit Non-Authorisations

- No compilation or activation of `signal_thyroid_tsh_context`.
- No compilation or activation of `signal_tgab_high`.
- No compilation or activation of bilirubin frames.
- No broadening of already compiled `signal_free_t3_low` or `signal_tpo_ab_high` beyond tested compatibility.
- No legacy retirement or disconnection under this decision.

## Implementation Note

The ratified narrowing must be encoded using the smallest governed runtime surface that
preserves:

- the approved axis gates;
- fail-closed behaviour for rejected or gate-unmet panels;
- aligned consumer and clinician wording;
- non-causal context where context-only interpretation is required.
