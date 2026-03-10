# Clinical Sign-Off — KBP-0012 Brain Metabolic Health

## Review Status

**Status: PENDING REVIEW**

---

## Package Information

| Field | Value |
|-------|-------|
| Package ID | KBP-0012 |
| Package directory | `knowledge_bus/packages/pkg_brain_metabolic_health/` |
| Signal | `signal_brain_metabolic_health` |
| Translation mode | Creation — companion to KBP-0007 (unparked) |
| Primary metric | `tyg_index` |
| Source document | `knowledge_bus/research/papers/10-Brain-Metabolic-Dysfunction-Signal-Generation.md` |
| Translation date | 2026-03-10 |
| Translated by | Claude Translation Engine — Research-to-Knowledge Translation Specification v1 |

---

## CRITICAL: Three Decisions Required Before Implementation

### Decision 1 — TyG Threshold Context Separation

KBP-0012 uses tyg_index with dementia-endpoint thresholds (8.1 / 8.8) from Cui et al.
2022 UK Biobank. Other packages use tyg_index with different thresholds for different
endpoints:

| Package | Signal | TyG thresholds | Endpoint |
|---------|--------|---------------|---------|
| KBP-0002 | `signal_insulin_resistance` | 8.30 / 8.50 | T2DM / metabolic IR |
| KBP-0004 | `signal_hepatic_metabolic_stress` | 8.21 / 8.97 | MASLD/NAFLD |
| KBP-0008 | `signal_mitochondrial_efficiency` | 4.49 / 4.68 | Mitochondrial efficiency |
| KBP-0012 | `signal_brain_metabolic_health` | 8.1 / 8.8 | Dementia / cognitive decline |

This is correct per Translation Rule #2 ("threshold belongs to the signal, not the
biomarker"). The runtime layer must correctly route each signal's tyg_index evaluation
to its own threshold set. Confirm this is architecturally supported.

**Decision required:**
- [ ] Confirm runtime can evaluate tyg_index against multiple independent threshold
      sets (one per signal) without cross-contamination
- [ ] Document in KB-S9 engineering spec that tyg_index is a shared derived metric
      with signal-specific threshold contexts

---

### Decision 2 — HbA1c Threshold Tier Evidence Quality

The HbA1c tiers (< 5.4 optimal / 5.4–5.6 suboptimal / > 5.6 at_risk) are sourced
from Kerti et al. 2013 — a cross-sectional study of n=141. This is Tier 2 evidence
by standard hierarchy (the paper itself labels it "mechanistic Tier 1" referring to
plausibility, not study design).

These thresholds are below pre-diabetes diagnostic criteria (≥ 5.7% per ADA). A user
with HbA1c 5.7% would be at_risk for brain metabolic health via this signal but only
borderline (pre-diabetic) systemically. The signal is intentionally sensitive — brain
structural changes appear earlier than metabolic diagnostic thresholds.

**Decision required:**
- [ ] Accept Tier 2 evidence for HbA1c tiers — brain-specific sensitivity justified;
      proceed with 5.4/5.6 boundaries
- [ ] Raise optimal boundary to < 5.0% or < 5.3% for more conservative framing
- [ ] Add explicit user-facing caveat that these HbA1c boundaries are for brain
      health monitoring only, not metabolic disease diagnosis

---

### Decision 3 — Signal Framing: Prognostic vs Actionable

ACCORD-MIND (RCT; n=2,977) confirmed intensive glucose lowering alone does not improve
cognitive outcomes. This signal must be framed as prognostic — risk indicator —
not as a target for glucose-lowering medication.

The appropriate intervention pathway when signal is at_risk: insulin-sensitising
lifestyle protocols (exercise, dietary modification, weight management) rather than
pharmacological glucose reduction.

**Decision required:**
- [ ] Confirm user-facing output includes prognostic framing caveat (not "lower your
      glucose to improve brain health" but "reduce insulin resistance to protect
      brain health")
- [ ] Add ACCORD-MIND caveat to runtime output annotation for at_risk state

---

## Derived Metrics Status

| Metric | Formula | Status |
|--------|---------|--------|
| `tyg_index` | ln((TG_mg × glucose_mg) / 2) | ✓ IN PLATFORM |
| `tg_hdl_ratio` | TG_mmol / HDL_mmol | ✓ IN PLATFORM |
| `homa_ir` | (insulin × glucose) / 22.5 | ✓ IN PLATFORM (optional) |

No SSOT gaps.

---

## Evidence Summary

### Primary evidence

**Cui et al. (Alzheimer's Research & Therapy, 2022; DOI: 10.1186/s13195-022-01015-w)**
- UK Biobank prospective cohort; n=482,716; follow-up 11.5 years
- TyG ≥ 8.8 (Q4 vs Q1): HR 1.15 (95% CI 1.05–1.25) for all-cause dementia and AD
- Tier 1 evidence — primary threshold source

**Kerti et al. (Neurology, 2013; DOI: 10.1212/01.wnl.0000435561.00285.f3)**
- Cross-sectional; n=141
- HbA1c > 5.6% even within normal range → reduced hippocampal volume and memory
- Tier 2 evidence — small sample; mechanistic support

**Fan et al. (Journal of Clinical Lipidology, 2019; DOI: 10.1016/j.jacl.2019.01.011)**
- Observational; n=1,536
- TG/HDL > 1.3 (mmol/L) → accelerated cognitive decline
- Tier 2 — supporting override rule

### Cautionary evidence

**ACCORD-MIND (Lancet Neurology, 2011; DOI: 10.1016/S1474-4422(11)70188-0)**
- RCT; n=2,977. Intensive glycemic control (HbA1c < 6.0%) yielded no improvement
  in cognitive test scores. Signal is prognostic, not prescriptive.

---

## Known Limitations

1. **TyG proxy limitation.** TyG index is a systemic surrogate for brain insulin
   resistance. Direct measurement requires CSF analysis or FDG-PET neuroimaging.
   Systemic IR does not guarantee central IR in every individual.

2. **HbA1c evidence is Tier 2.** Kerti 2013 thresholds (5.4/5.6%) are from a small
   cross-sectional study. Prospective validation of these specific brain-health cut-offs
   is not yet available in large cohorts.

3. **APOE genotype not incorporated.** APOE ε4 is the strongest genetic risk modifier
   for AD and amplifies the effect of metabolic risk. Not expressible in current schema.

4. **Ethnic generalisability.** TyG cut-offs validated primarily in European (UK Biobank)
   population. Evidence for non-European ethnicities is limited (stated in Cui 2022).

5. **T1D exclusion.** Signal not validated in Type 1 Diabetes. Pathophysiology differs;
   insulin deficiency vs resistance.

6. **Advanced AD.** In end-stage Alzheimer's, metabolic intervention has diminishing
   returns — signal most useful in pre-symptomatic and MCI stages.

7. **Acute illness confounders.** Acute illness or infection temporarily elevates glucose
   and CRP — runtime layer should flag elevated glucose in acute context.

---

## Clinical Reviewer Sign-Off

**Reviewer name:** [PENDING]

**Role / credentials:** [PENDING]

**Review date:** [PENDING]

### Decision checklist (all three required)

- [ ] **Decision 1** — TyG multi-signal threshold routing (engineering confirmation)
- [ ] **Decision 2** — HbA1c Tier 2 evidence acceptance (5.4/5.6 boundaries)
- [ ] **Decision 3** — Prognostic framing and ACCORD-MIND caveat in output

### Threshold acceptance

| Threshold | Value | Evidence source | Accepted |
|-----------|-------|----------------|---------|
| TyG optimal | < 8.1 | Cui et al. 2022 (UK Biobank; n=482,716; Tier 1) | [ ] |
| TyG suboptimal | 8.1 – 8.8 | Cui et al. 2022 | [ ] |
| TyG at_risk | ≥ 8.8 | Cui et al. 2022 (HR 1.15 for dementia) | [ ] |
| HbA1c optimal | < 5.4% | Kerti et al. 2013 (n=141; Tier 2) | [ ] |
| HbA1c suboptimal | 5.4 – 5.6% | Kerti et al. 2013 | [ ] |
| HbA1c at_risk | > 5.6% | Kerti et al. 2013 (hippocampal volume reduction) | [ ] |
| Overt diabetes override | glucose ≥ 7.0 OR HbA1c ≥ 6.5% → at_risk | ADA 2025 | [ ] |
| TG/HDL cognitive decline | > 1.3 → suboptimal | Fan et al. 2019 (n=1,536) | [ ] |
| Pancreatitis safety | TG ≥ 5.6 → at_risk | ESC/EAS (consistent with other packages) | [ ] |

### Excluded populations

- [ ] Type 1 Diabetes (different pathophysiology — insulin deficiency, not resistance)
- [ ] End-stage Alzheimer's Disease (diminishing returns for metabolic intervention)
- [ ] Acute illness / infection (transient glucose/CRP elevation)
- [ ] Children (adult thresholds inappropriate)
- [ ] Patients on intensive sulphonylurea therapy (hypoglycaemic events are neurotoxic)

### Additional notes

```
[Reviewer to complete]
```

### Sign-off statement

I confirm that the signal thresholds, override logic, excluded populations, limitations,
and the three pending decisions documented in KBP-0012 have been reviewed against the
cited research evidence.

**Signed:** ___________________________

**Date:** ___________________________

---

*This document was generated by Claude Translation Engine under Research-to-Knowledge Translation
Specification v1. All three decisions must be completed before this package proceeds to
Layer B implementation.*
