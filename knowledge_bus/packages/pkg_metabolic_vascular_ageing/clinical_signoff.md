# Clinical Sign-Off — KBP-0011 Metabolic-Driven Vascular Ageing

## Review Status

**Status: PENDING REVIEW**

This document must be completed by a named clinical reviewer and committed before this package
may be promoted to Layer B implementation. No code may be committed to `backend/core/` without
a completed sign-off.

---

## Package Information

| Field | Value |
|-------|-------|
| Package ID | KBP-0011 |
| Package directory | `knowledge_bus/packages/pkg_metabolic_vascular_ageing/` |
| Signal | `signal_metabolic_vascular_ageing` |
| Translation mode | Creation — new signal (MDVA; AIP-primary) |
| Primary metric | `aip` |
| Source document | `knowledge_bus/research/papers/7-Cardiovascular-Metabolic-Risk.md` |
| Translation date | 2026-03-10 |
| Translated by | Claude Translation Engine — Research-to-Knowledge Translation Specification v1 |

---

## CRITICAL: Four Decisions Required Before Implementation

### Decision 1 — AIP mmol/L Threshold Confirmation

AIP = log10(TG_mmol/HDL_mmol). The thresholds 0.11 (optimal/suboptimal boundary) and
0.21 (suboptimal/at_risk boundary) are sourced from Niroumand et al. 2015.

**AIP is unit-sensitive.** log10(TG_mg/HDL_mg) produces a systematically different
numerical value than log10(TG_mmol/HDL_mmol) by approximately log10(2.29) ≈ 0.36.
Some published papers compute AIP in mg/dL; others in mmol/L. The thresholds cited
differ accordingly:
- mmol/L-based literature: thresholds ~0.11/0.21 (Niroumand 2015; Dobiásová 2004)
- mg/dL-based literature: thresholds ~0.10/0.24 (some North American studies)

The platform computes tg_hdl_ratio in mmol/L (SSOT standard). AIP is therefore
log10(tg_hdl_ratio_mmol_per_mmol). The 0.11/0.21 thresholds are standard for mmol/L
and are used in this package.

**Decision required:**
- [ ] Accept 0.11/0.21 as mmol/L-confirmed canonical thresholds (proceed to KB-S9)
- [ ] Request formal confirmation from clinical reviewer that Niroumand 2015 used
      mmol/L before implementation
- [ ] Adjust thresholds if mg/dL-basis confirmed: optimal < -0.25, suboptimal -0.25–0.10,
      at_risk > 0.10 (Dobiásová mg/dL-based values, adjusted for platform units)

---

### Decision 2 — Evidence Quality Acceptance

The primary threshold source (Niroumand 2015) is:
- Cross-sectional design (no prospective outcome follow-up)
- Persian population (n=4,215) — multi-ethnic validation absent
- Evidence tier: Tier 2

AIP is widely cited in lipidology literature as a valid proxy for LDL particle size
distribution and is mechanistically well-supported. However, unlike TyG index
(backed by n=105,365 meta-analysis) or NLR (backed by NHANES prospective data),
the AIP thresholds 0.11/0.21 rest on a single cross-sectional cohort.

**Decision required:**
- [ ] Accept Tier 2 evidence — AIP is mechanistically validated and widely used;
      cross-sectional threshold derivation is sufficient for a monitoring/screening signal
- [ ] Require additional prospective validation before Layer B — defer KBP-0011 until
      a prospective cohort study anchoring 0.11/0.21 is identified
- [ ] Proceed with explicit "moderate confidence" labelling in user-facing output

---

### Decision 3 — Pulse Pressure Optimal Boundary

KBP-0007 (signal_vascular_cognitive_reserve) tracks pulse_pressure with:
- optimal: < 45 mmHg
- at_risk: > 60 mmHg

This package uses:
- optimal: < 50 mmHg
- at_risk: > 60 mmHg

The at_risk boundary (> 60 mmHg) is consistent across both packages. The optimal
boundary differs (45 vs 50 mmHg). Both values appear in published literature:
- < 40 mmHg is often cited as physiologically optimal (young healthy adults)
- < 50 mmHg is the common clinical "normal" range cutoff
- < 45 mmHg represents a more conservative intermediate

**Decision required:**
- [ ] Standardise pulse_pressure optimal boundary to < 45 mmHg across all packages
      (more conservative; consistent with KBP-0007)
- [ ] Standardise to < 50 mmHg (less conservative; broader "normal" clinical range)
- [ ] Allow package-specific boundaries — document rationale for each

---

### Decision 4 — Early Vascular Ageing (EVA) Age Flag

The source paper specifies: age < 30 AND pulse_pressure > 60 → at_risk (EVA flag).

`age` is not registered in the SSOT as a metric_id. `date_of_birth` is available in
questionnaire.json. Age is derivable at runtime (current_date − date_of_birth in years).
The signal schema cannot express an age-conditional override rule without age being
a registered derived metric.

**Decision required:**
- [ ] Implement as a runtime annotation in KB-S9: when derived_age < 30 AND
      pulse_pressure > 60, append `early_vascular_ageing_flag: true` to signal output
- [ ] Add `age_years` as a derived metric to ratio_registry.py (computed from
      date_of_birth at evaluation time) — then implement as a schema override rule
- [ ] Deprioritise — the pulse_pressure_at_risk override already captures pp > 60
      regardless of age; the EVA annotation is supplementary

---

## Derived Metrics Status

| Metric | Formula | Status | Notes |
|--------|---------|--------|-------|
| `aip` | log10(tg_hdl_ratio) = log10(TG_mmol/HDL_mmol) | ✗ NOT IN PLATFORM | Standard sprint — log10 wrapper on existing tg_hdl_ratio in ratio_registry |
| `pulse_pressure` | systolic_bp − diastolic_bp | ✗ NOT IN PLATFORM | Already tracked in SSOT_GAPS.md (KBP-0007) |

---

## Evidence Summary

### Primary evidence

**Niroumand et al. (BMC Cardiovascular Disorders, 2015; DOI: 10.1186/s12872-015-0117-x)**
- Cross-sectional; n=4,215; Persian population
- AIP = log10(TG/HDL-C) — strongest metabolic predictor of arterial stiffness and CAC
- Thresholds: < 0.11 optimal, 0.11–0.21 intermediate, > 0.21 high risk

### Supporting evidence

**Nilsson et al. (Journal of Hypertension, 2014; DOI: 10.1097/HJH.0000000000000060)**
- Expert consensus / review of longitudinal cohorts; up to 20 years
- Defines Early Vascular Ageing (EVA); no single blood threshold established

**Framingham Heart Study (Archives of Internal Medicine, 1999)**
- n=5,000+; follow-up up to 30 years
- Pulse pressure > 60 mmHg: excess CVD risk; validates PP as structural stiffness marker

---

## Known Limitations

1. **AIP thresholds are Tier 2 evidence.** Primary source is cross-sectional and
   Persian-population-specific. See Decision 2.

2. **CETP inhibitor caveat.** Drug-mediated AIP improvement (CETP inhibitors) has
   historically failed to reduce hard cardiovascular outcomes, confirming AIP as a
   metabolic *marker*, not a therapeutic target. AIP reduction via medication does not
   necessarily indicate resolved vascular risk.

3. **Athletes.** High-performance athletes may have naturally elevated pulse pressures
   due to high stroke volume (Athlete's Heart), not arterial stiffness. Runtime
   exclusion flag required.

4. **Pregnancy.** Haemodynamic changes significantly alter pulse pressure and lipid
   profiles — signal unreliable during pregnancy.

5. **Vasodilators.** ACE inhibitors and calcium channel blockers lower pulse pressure
   without reversing underlying glycative AGE cross-linking. Medication confounders
   must be flagged via long_term_medications questionnaire field.

6. **AIP unit sensitivity.** See Decision 1 — mmol/L vs mg/dL threshold
   disambiguation required before implementation.

7. **pulse_pressure threshold delta with KBP-0007.** See Decision 3 — optimal
   boundary reconciliation required before KB-S9 implementation.

---

## Clinical Reviewer Sign-Off

**Reviewer name:** [PENDING]

**Role / credentials:** [PENDING]

**Review date:** [PENDING]

### Decision checklist (all four required)

- [ ] **Decision 1** — AIP mmol/L threshold confirmation (0.11/0.21 basis)
- [ ] **Decision 2** — Evidence quality acceptance (Tier 2 cross-sectional source)
- [ ] **Decision 3** — Pulse pressure optimal boundary standardisation (45 vs 50 mmHg)
- [ ] **Decision 4** — EVA age flag implementation path

### Threshold acceptance

| Threshold | Value | Evidence source | Accepted |
|-----------|-------|----------------|---------|
| AIP optimal | < 0.11 | Niroumand 2015 (n=4,215; mmol/L basis) | [ ] |
| AIP suboptimal | 0.11 – 0.21 | Niroumand 2015 | [ ] |
| AIP at_risk | > 0.21 | Niroumand 2015 | [ ] |
| PP at_risk override | > 60 mmHg → at_risk | Framingham Study | [ ] |
| PP suboptimal override | 50–60 mmHg → suboptimal | Clinical practice / Framingham context | [ ] |
| Synergistic glycation | AIP > 0.21 AND glucose > 7.0 → at_risk | Niroumand; EVA framework | [ ] |

### Excluded populations

- [ ] High-performance athletes (elevated PP from stroke volume, not stiffness)
- [ ] Pregnant individuals (haemodynamic and lipid profile alterations)
- [ ] Patients on CETP inhibitors (AIP improvement may not reflect true risk reduction)
- [ ] Patients on vasodilators (ACE inhibitors, CCBs — PP artificially lowered)
- [ ] Patients with secondary dyslipidaemia (thyroid disease, nephrotic syndrome)

### Additional notes

```
[Reviewer to complete]
```

### Sign-off statement

I confirm that the signal thresholds, override logic, excluded populations, limitations,
and the four pending decisions documented in KBP-0011 have been reviewed against the
cited research evidence.

**Signed:** ___________________________

**Date:** ___________________________

---

*This document was generated by Claude Translation Engine under Research-to-Knowledge Translation
Specification v1. All four decisions must be completed before this package proceeds to
Layer B implementation.*
