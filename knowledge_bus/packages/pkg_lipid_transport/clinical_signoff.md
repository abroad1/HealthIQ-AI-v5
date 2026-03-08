# Clinical Sign-Off — KBP-0003 Lipid Transport Dysfunction

## Review Status

**Status: PENDING REVIEW**

This document must be completed by a named clinical reviewer and committed before this package may be
promoted to Layer B implementation (KB-S9). No code implementing derived metrics or signal logic from
this package may be committed to `backend/core/` without a completed sign-off.

---

## Package Information

| Field | Value |
|-------|-------|
| Package ID | KBP-0003 |
| Package directory | `knowledge_bus/packages/pkg_lipid_transport/` |
| Signal | `signal_lipid_transport_dysfunction` |
| Translation mode | Creation — evidence-anchored thresholds; threshold delta from KBP-0001 |
| Primary metric | `derived.non_hdl_cholesterol` |
| Source document | `knowledge_bus/research/study_02_lipid_transport_dysfunction.md` |
| Translation date | 2026-03-08 |
| Translated by | Claude Translation Engine — Research-to-Knowledge Translation Specification v1 |

---

## CRITICAL: Threshold Delta — KBP-0001 vs KBP-0003

**A decision is required before implementation.**

`signal_lipid_transport_dysfunction` already exists in KBP-0001. KBP-0003 proposes different thresholds
based on primary outcome evidence. The two sets are not compatible.

| Tier | KBP-0001 (existing design) | KBP-0003 (research-anchored) | Delta |
|------|---------------------------|------------------------------|-------|
| Optimal boundary | < 3.4 mmol/L | < 3.7 mmol/L | +0.3 mmol/L |
| Suboptimal range | 3.4 – 4.09 mmol/L | 3.7 – 5.69 mmol/L | Materially wider |
| At-risk boundary | ≥ 4.1 mmol/L | ≥ 5.7 mmol/L | +1.6 mmol/L |

**Why the delta exists:**

The KBP-0001 thresholds were derived from general clinical guidelines (ESC/EAS treatment targets and
European guideline LDL/non-HDL secondary goals). These are clinically reasonable reference points.

The KBP-0003 thresholds are derived from the **Multinational Cardiovascular Risk Consortium**
(Lancet 2019; n=398,846; 54,542 cardiovascular endpoints; median follow-up 13.5 years). This is a
large pooled prospective cohort study with hard cardiovascular outcomes. The non-HDL-C risk gradient
in this study places the at-risk inflection at approximately 5.7 mmol/L — 1.6 mmol/L above the KBP-0001
value of 4.1 mmol/L.

**Practical consequence:**

Using KBP-0001 thresholds will classify more users as "at risk" than the long-term outcome data supports.
Using KBP-0003 thresholds more closely reflects the population-level risk gradient from prospective data.
Neither set is "wrong" — they reflect different evidence bases and different clinical use cases
(treatment target vs population risk stratification).

**Decision required from clinical reviewer:**

- [ ] Adopt KBP-0003 thresholds (3.7 / 5.7 mmol/L) — research-outcome-anchored
- [ ] Retain KBP-0001 thresholds (3.4 / 4.1 mmol/L) — existing design
- [ ] Hybrid approach — document rationale below
- [ ] Defer pending additional review

---

## Known Design Limitation: Two-Axis TG Signal

The research model specifies a two-axis detection system:

- **Primary axis**: non-HDL-C (thresholds 3.7 / 5.7 mmol/L)
- **Secondary axis**: TG (1.7 mmol/L and 5.6 mmol/L boundaries)

The full intended logic is:
- If non-HDL-C is optimal AND TG ≥ 1.7 mmol/L → promote to suboptimal
- If TG ≥ 5.6 mmol/L → at-risk regardless of non-HDL-C

The current signal schema supports unconditional override rules (which always set a resulting state
regardless of the primary metric classification). A `tg_borderline_override` (TG ≥ 1.7 → suboptimal)
as an unconditional rule would downgrade users who are already `at_risk` from the non-HDL-C axis.

**Current implementation in this package:**
- `tg_severe_override` (TG ≥ 5.6 → at_risk) is included — this is always an upgrade, never a downgrade
- The TG 1.7 mmol/L conditional upgrade is **not modelled as an override rule**

**Required resolution:**
Option 1: Add conditional override support to the signal library schema (future schema enhancement)
Option 2: Handle the TG 1.7 upgrade as runtime logic during KB-S9 implementation, outside the signal schema
Option 3: Accept the conservative model — TG 1.7-5.5 cases are suboptimal via non-HDL-C thresholds anyway
in the majority of affected users, and the rare case (non-HDL optimal, TG mildly elevated) is caught
by the clinical notes in the user interface

Clinical reviewer decision required below.

---

## Evidence Summary

### Primary evidence

**Multinational Cardiovascular Risk Consortium (Lancet 2019)**
- n = 398,846 participants; 54,542 cardiovascular endpoints; median follow-up 13.5 years
- Pooled prospective cohorts; derivation and validation arms
- Non-HDL-C shows stepwise long-term ASCVD event-rate increases above 3.7 mmol/L
- Non-HDL-C ≥ 5.7 mmol/L identifies highest long-term ASCVD risk category
- Basis for KBP-0003 optimal and at-risk threshold values

### Supporting evidence

**ApoB vs LDL-C vs non-HDL-C meta-analysis (Circulation 2011; n=233,455)**
- ApoB is the strongest lipid cardiovascular risk marker
- Non-HDL-C outperforms LDL-C; best available standard-panel proxy for atherogenic burden
- Justifies non-HDL-C as primary metric when apoB is not available

**Copenhagen General Population Study (Clinical Chemistry 2018; n=106,216)**
- Remnant cholesterol ≥ 1.5 mmol/L associated with ~2-fold MI risk across BMI strata
- Follow-up up to 11 years; Cox models; prospective design
- Basis for the optional `derived.remnant_cholesterol` flag at 1.5 mmol/L

**ESC/EAS Dyslipidaemia Guidelines (European Heart Journal 2019)**
- Non-HDL-C endorsed as secondary treatment target
- TG ≥ 1.7 mmol/L indicated as risk-enhancement boundary
- TG ≥ 5.6 mmol/L defined as severe hypertriglyceridaemia threshold; basis for `tg_severe_override`

**EAS TRL/Remnant Consensus Statement (European Heart Journal 2021)**
- TRL/remnants confirmed as causal contributors to MI and ischaemic stroke
- Genetic, epidemiological, and mechanistic evidence synthesis
- Supports TG override rules as clinically defensible

**PROMINENT trial — cautionary evidence (NEJM 2022; n=10,497)**
- Pemafibrate lowered TG and remnants but did not reduce cardiovascular events
- ApoB and LDL-C increased slightly during TG lowering
- Demonstrates TG lowering ≠ CV risk reduction without apoB/non-HDL improvement
- Signal design reflects this: TG is a modifier and override trigger, not the primary outcome-anchored axis

---

## New Derived Metric: derived.remnant_cholesterol

This package introduces `derived.remnant_cholesterol` as an optional signal dependency.

**Formula:** `remnant_cholesterol = total_cholesterol − ldl_cholesterol − hdl_cholesterol`

**Units:** mmol/L (all inputs in mmol/L)

**Clinical flag threshold:** RC ≥ 1.5 mmol/L (~2-fold MI risk; Copenhagen General Population Study)

**Current implementation status:** NOT present in `backend/core/analytics/ratio_registry.py`

A separate implementation sprint is required before this metric can activate. It is listed under
`optional_dependencies` in the signal library. The signal will function without it — the remnant
cholesterol flag will simply not activate until the metric is registered.

**LDL-C accuracy caveat:** Calculated LDL-C (Friedewald-type) degrades at TG > 4.5 mmol/L.
At high TG, skip remnant calculation and rely on non-HDL-C + TG axis only.

---

## Known Limitations

1. **ApoB not in standard panel.** ApoB is consistently the strongest lipid risk marker in
   discordance analyses (Circulation 2011 meta-analysis) but requires a separate assay not included
   in standard fasting lipid panels. Non-HDL-C is the best available proxy. If apoB becomes available
   for a user, signal upgrade to apoB-based classification is warranted. This is not currently
   supported by the signal schema.

2. **Remnant cholesterol depends on LDL-C accuracy.** Calculated remnant cholesterol inherits
   LDL-C estimation error, particularly at TG > 4.5 mmol/L (Friedewald formula degrades). The
   Sampson equation (JAMA Cardiology 2020) improves accuracy up to TG ≈ 800 mg/dL but implementation
   is not universal. The signal treats remnant_cholesterol as conditional and optional.

3. **TG 1.7 mmol/L conditional upgrade not modelled.** See design limitation section above. The
   TG 1.7 mmol/L risk-enhancement boundary is clinically defensible but cannot be implemented as
   an unconditional override without introducing possible state downgrade for at-risk users.

4. **Non-fasting samples.** This signal is designed for fasting lipid panels. Non-fasting TG can be
   substantially elevated (postprandial lipaemia). If fasting status is unknown, TG override rules
   should be applied conservatively.

5. **Population calibration.** The Multinational Cardiovascular Risk Consortium thresholds reflect
   predominantly European population cohorts with long follow-up. Calibration against the specific
   HealthIQ user population may be warranted before thresholds are treated as final.

6. **HDL-C is a substrate, not a protective target.** HDL-C is used only for non-HDL-C calculation.
   The signal does not treat HDL-C as an independent protective marker. Very high HDL-C can associate
   with increased mortality in some subgroups. HDL quantity is not equivalent to HDL function
   (cholesterol efflux capacity).

7. **TG lowering requires apoB/non-HDL validation.** PROMINENT (2022) established that TG reduction
   without non-HDL-C/apoB improvement does not reduce CV events. If a user reports TG improvements,
   this signal should check whether non-HDL-C and/or apoB have also improved before classifying the
   change as a risk reduction. This nuance is not captured in the current static signal design.

---

## Clinical Reviewer Sign-Off

**Reviewer name:** [PENDING]

**Role / credentials:** [PENDING]

**Review date:** [PENDING]

### Acknowledgement checklist

- [ ] I have reviewed the research evidence summary and source document
- [ ] I have reviewed the KBP-0001 vs KBP-0003 threshold delta and made a decision (document below)
- [ ] I accept the evidence-anchored non-HDL-C thresholds for product use, OR document my decision below
- [ ] I have reviewed and accept the TG override rules (5.6 mmol/L severe threshold)
- [ ] I have reviewed and accept the TG 1.7 mmol/L design limitation and proposed resolution
- [ ] I have reviewed and accept the derived.remnant_cholesterol optional flag and its status
- [ ] I acknowledge the signal limitations listed above
- [ ] I have documented excluded populations and clinical guardrails below

### Threshold decision (required)

```
[Reviewer to complete:
 - Select: KBP-0001 thresholds (3.4 / 4.1) | KBP-0003 thresholds (3.7 / 5.7) | Hybrid | Defer
 - Provide rationale for chosen threshold set
 - Note any modifications to the evidence-anchored values]
```

### TG design limitation resolution (required)

```
[Reviewer to complete:
 - Select preferred resolution: Schema enhancement | Runtime KB-S9 logic | Accept conservative model
 - Any other guidance on TG axis handling]
```

### Excluded populations and clinical guardrails

```
[Reviewer to complete. Examples to consider:
 - Secondary hyperlipidaemia (hypothyroidism, nephrotic syndrome, cholestasis)
 - Medication confounders (corticosteroids, antipsychotics, HIV therapy)
 - Pregnancy (lipid profile changes substantially)
 - Familial hypercholesterolaemia (may require different threshold calibration)
 - Paediatric populations]
```

### Additional notes

```
[Reviewer to complete]
```

---

*This document was generated by Claude Translation Engine under Research-to-Knowledge Translation
Specification v1. The acknowledgement and decision sections require human completion before this
package may proceed to Layer B implementation.*
