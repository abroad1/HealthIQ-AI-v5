# Clinical Sign-Off — KBP-0005 Chronic Systemic Inflammation

## Review Status

**Status: PENDING REVIEW**

This document must be completed by a named clinical reviewer and committed before this package
may be promoted to Layer B implementation. No code may be committed to `backend/core/` without
a completed sign-off.

---

## Package Information

| Field | Value |
|-------|-------|
| Package ID | KBP-0005 |
| Package directory | `knowledge_bus/packages/pkg_chronic_inflammation/` |
| Signal | `signal_systemic_inflammation` |
| Translation mode | Creation — materially different thresholds and supporting marker framework from KBP-0001 |
| Primary metric | `crp` (hs-CRP) |
| Thresholds | optimal <1.0 / suboptimal 1.0–3.0 / at_risk ≥3.0 mg/L |
| Source document | `knowledge_bus/research/study_04_chronic_inflammation.md` |
| Translation date | 2026-03-08 |
| Translated by | Claude Translation Engine — Research-to-Knowledge Translation Specification v1 |

---

## CRITICAL: Four Decisions Required Before Implementation

### Decision 1 — KBP-0001 Threshold Delta

KBP-0001 contains `signal_systemic_inflammation` with a **materially different design**:

| Aspect | KBP-0001 | KBP-0005 |
|--------|----------|----------|
| Primary metric | `crp` | `crp` |
| Optimal | CRP < 3.0 mg/L | CRP < 1.0 mg/L |
| Suboptimal | CRP 3.0–9.99 mg/L | CRP 1.0–3.0 mg/L |
| At-risk | CRP ≥ 10.0 mg/L | CRP ≥ 3.0 mg/L |
| Override | None | Acute override: CRP ≥ 10.0 → at_risk + repeat flag |

KBP-0001 thresholds appear to be based on the standard CRP clinical ranges (where <10 mg/L
is "non-elevated" for acute disease purposes). KBP-0005 uses the hs-CRP cardiovascular
risk stratification model from ACC/AHA 2025 and ESC guidelines, which is the appropriate
framework for metabolic health monitoring (hs-CRP specifically targets the 0–10 mg/L range
with clinical significance at 1.0 and 3.0 mg/L boundaries).

The KBP-0001 design would classify a patient with CRP = 2.5 mg/L (elevated residual
inflammatory risk) as "optimal". The KBP-0005 design correctly classifies this as
"suboptimal".

**Decision required:**
- [ ] Adopt KBP-0005 thresholds — replace KBP-0001 design at implementation
- [ ] Investigate KBP-0001 threshold origin — confirm whether 3.0/10.0 was intentional
- [ ] Defer pending further clinical review

---

### Decision 2 — Primary Threshold Boundary: 2.0 mg/L vs 3.0 mg/L

The evidence supports two defensible suboptimal/at-risk boundary positions:

**Option A — 3.0 mg/L** (implemented in this package):
- Traditional ACC/AHA three-tier: low (<1.0) / intermediate (1.0–3.0) / high (>3.0)
- ESC/EAS 2025 and AHA guidelines use >3.0 as the "high risk" entry point
- Clinically conservative — only flags the highest-risk chronic inflammation cases

**Option B — 2.0 mg/L**:
- ACC/AHA 2025 Scientific Statement: hs-CRP ≥2.0 mg/L = "risk-enhancing factor"
- Residual inflammatory risk (RIR): patients on statins with LDL-C <70 mg/dL but
  hs-CRP ≥2.0 mg/L remain at significantly elevated MACE risk (JUPITER trial)
- More sensitive for secondary prevention population
- Would reclassify the range 2.0–3.0 mg/L from suboptimal → at_risk

The current signal library schema expresses a single suboptimal/at_risk boundary.
The RIR concept (2.0 mg/L specifically for statin-treated patients) cannot be natively
expressed — it would require medication context from `long_term_medications` in
`questionnaire.json`. This is implementable at runtime (KB-S9) using questionnaire data.

**Decision required:**
- [ ] Use 3.0 mg/L as the at-risk boundary (current implementation) — document RIR as a runtime logic note for KB-S9
- [ ] Use 2.0 mg/L as the at-risk boundary — more conservative; will increase at_risk classifications across the platform
- [ ] Implement runtime RIR logic in KB-S9 using `long_term_medications` from questionnaire

---

### Decision 3 — NLR as Supporting Metric: Threshold Documentation

`derived.nlr` is already computed in `ratio_registry.py`. The research supports an NLR
cutoff of **1.67** for metabolic syndrome detection (sensitivity 74.3%, specificity 62.3%;
meta-analysis n=70,937).

The signal library currently lists `derived.nlr` as an **optional** supporting metric
with no associated threshold. The NLR 1.67 threshold is not enforced in the signal tier
classification (CRP alone determines the tier). This is consistent with NLR functioning
as contextual enrichment rather than a co-primary.

However, a patient with optimal CRP (<1.0 mg/L) but NLR >2.45 (linked to HR 2.217 for
diabetic retinopathy) may represent undetected inflammatory risk that hs-CRP alone misses.

**Design gap:** The current schema cannot express compound logic (e.g., "if NLR >1.67,
escalate from optimal to suboptimal even if CRP <1.0").

**Decision required:**
- [ ] Retain current design — NLR as supporting context only; document threshold gap as a known limitation
- [ ] Request schema enhancement to support compound primary/secondary threshold logic
- [ ] Implement NLR as a co-primary with its own override rule (NLR ≥2.45 → at_risk)

---

### Decision 4 — SII as New Derived Metric (KB-S9 Sprint Priority)

SII = (Platelet Count × Neutrophil Count) / Lymphocyte Count

All three input biomarkers are confirmed in `backend/ssot/biomarkers.yaml`:
- `platelets` ✓
- `neutrophils` ✓ (or `neutrophils_abs`)
- `lymphocytes` ✓ (or `lymphocytes_abs`)

SII is currently listed as an optional derived metric in the signal library.
It is **not implemented** in `ratio_registry.py`.

Evidence: meta-analysis n=85,796 — SII predicts diabetic nephropathy (OR 1.94),
retinopathy (SMD 2.70), CVD mortality (OR 1.55) — superior to NLR alone.

**Decision required:**
- [ ] Implement `derived.sii` in `ratio_registry.py` during KB-S9 — high clinical value
- [ ] Deprioritise SII — NLR coverage is sufficient for current scope
- [ ] Document age-stratified NLR interpretation as a KB-S9 engineering note (adult 1.67 cutoff; elderly >75 reference range shifts to 0.89–8.80)

---

## Evidence Summary

### Primary evidence — hs-CRP

**ACC Scientific Statement (2025)**
- Universal hs-CRP screening recommended for primary and secondary prevention
- hs-CRP ≥2.0 mg/L classified as a risk-enhancing factor
- hs-CRP reclassifies 12–14% of intermediate-risk patients
- Exercise reduces hs-CRP by 0.59 mg/L; weight loss 0.13 mg/L per kg; vegan diet 0.54 mg/L

**JUPITER and A-to-Z Trials (Ridker et al.)**
- Patients achieving LDL-C <70 mg/dL but with hs-CRP ≥2.0 mg/L: persistently elevated MACE risk
- Best outcomes: both LDL-C <70 mg/dL AND hs-CRP <2.0 mg/L achieved
- Establishes residual inflammatory risk (RIR) as an independent treatment target

**NeLSA / MetS longitudinal data**
- Each log-unit increase in hs-CRP: 18% higher T2DM risk, 34% higher ASCVD risk in MetS patients
- hs-CRP correlates with Framingham Risk Scores (r=0.684, p<0.001) in T2DM patients

### Primary evidence — NLR

**Meta-analysis of 26 studies (n=70,937)**
- NLR significantly higher in MetS patients (mean difference 0.40)
- 2.23-fold increase in MetS incidence for high NLR
- NLR cutoff 1.67: sensitivity 74.3%, specificity 62.3% for MetS (US adults, NHANES 1999–2018)

**Prospective cohort (9.4-year follow-up)**
- Highest NLR tertile: HR 2.7 for major adverse vascular events (MAVE)
- HR 1.55 for diabetic kidney disease progression
- NLR >2.45: HR 2.217 for diabetic retinopathy (independent of HbA1c and diabetes duration)

### Primary evidence — SII

**Meta-analysis of 22 studies (n=85,796; Frontiers in Endocrinology, 2025)**
- Diabetic Nephropathy: OR 1.94
- Diabetic Retinopathy: SMD 2.70
- All-cause mortality in T2DM: OR 1.38
- Cardiovascular mortality: OR 1.55
- SII outperforms NLR for predicting microvascular diabetic complications

### Guideline anchoring

**ACC/AHA 2025 Scientific Statement on hs-CRP**
- Three-tier: <1.0 (low) / 1.0–3.0 (intermediate) / >3.0 (high) for CVD risk
- Acute inflammation exclusion: repeat high values (>10 mg/L) after 2 weeks

**ESC/EAS 2025 Focused Update**
- hs-CRP as a risk modifier for cardiovascular prevention
- Colchicine for residual inflammatory risk in stable CAD

**ADA 2025 Standards of Care**
- Universal screening from age 35; anti-inflammatory therapies (GLP-1 RA, SGLT2i)
- Role of sleep and chrono-nutrition in metabolic inflammation management

---

## New Derived Metrics Required

| Metric | Formula | Status | Blocker |
|--------|---------|--------|---------|
| `derived.nlr` | Neutrophils / Lymphocytes | Already in ratio_registry.py | None |
| `derived.sii` | (Platelets × Neutrophils) / Lymphocytes | NOT in ratio_registry.py | Implement in KB-S9; all inputs in SSOT |
| `derived.siri` | (Neutrophils × Monocytes) / Lymphocytes | NOT in ratio_registry.py | Optional; implement in KB-S9 if Decision 4 selects SII |

Note: `monocytes_abs` biomarker is confirmed in `biomarkers.yaml` for SIRI computation.

---

## Known Limitations

1. **Threshold delta with KBP-0001.** KBP-0001 uses 3.0/10.0 mg/L for systemic inflammation.
   KBP-0005 uses 1.0/3.0 mg/L per ACC/AHA 2025. The designs are mutually exclusive —
   both cannot be active simultaneously for `signal_systemic_inflammation`. Clinical sign-off
   Decision 1 must resolve this before KB-S9.

2. **Residual inflammatory risk (RIR) not expressible in current schema.** The 2.0 mg/L
   threshold applies specifically to patients on statins with controlled LDL-C. The signal
   library cannot encode medication context — this requires runtime logic in KB-S9 using
   `long_term_medications` from `questionnaire.json`.

3. **NLR compound logic not supported.** The schema cannot express "if NLR >1.67, escalate
   tier even when CRP is optimal." NLR functions as supporting context only in current design.

4. **Age-stratified NLR interpretation.** The 1.67 cutoff is validated for adults 18–75.
   Elderly patients (>75) have physiologically higher NLR (up to 8.80) due to immunosenescence.
   Age derivation from `date_of_birth` in `questionnaire.json` enables runtime stratification
   in KB-S9 — document as engineering requirement.

5. **Acute CRP override.** CRP ≥10.0 mg/L is classified as at_risk but likely reflects
   acute infection or tissue injury, not chronic metabolic inflammation. The platform cannot
   currently flag a result for "repeat in 2 weeks" — this is a UX/output layer concern for KB-S10.

6. **SII reference thresholds context-dependent.** The 626.51 cutoff cited in the study is
   for perimenopausal populations. General population SII thresholds are not yet established
   with the same precision as hs-CRP. SII is currently optional until broader reference ranges
   are validated.

7. **Sex-specific CRP considerations.** Oral contraceptives and HRT elevate hs-CRP
   independently of metabolic inflammation. Female sex also has higher baseline CRP.
   `biological_sex` is available in `questionnaire.json` for runtime interpretation — flag
   for KB-S9 implementation note.

8. **Statin effect on hs-CRP.** Statins reduce hs-CRP independently of LDL-C lowering.
   A patient on statins with CRP 1.5 mg/L may have had untreated CRP of 3+ mg/L.
   Medication context required for full interpretation — `long_term_medications` in
   questionnaire.json is the SSOT source.

---

## Clinical Reviewer Sign-Off

**Reviewer name:** [PENDING]

**Role / credentials:** [PENDING]

**Review date:** [PENDING]

### Decision checklist (all four required)

- [ ] **Decision 1** — KBP-0001 threshold delta resolution (1.0/3.0 vs 3.0/10.0 mg/L)
- [ ] **Decision 2** — Primary at-risk boundary: 2.0 mg/L (RIR) vs 3.0 mg/L (ACC/AHA high-risk)
- [ ] **Decision 3** — NLR: supporting context only vs compound override logic
- [ ] **Decision 4** — SII implementation in KB-S9 (priority vs deprioritise)

### Threshold acceptance

| Threshold | Value | Evidence source | Accepted |
|-----------|-------|----------------|---------|
| hs-CRP optimal | < 1.0 mg/L | ACC/AHA 2025 three-tier low-risk | [ ] |
| hs-CRP suboptimal | 1.0–3.0 mg/L | ACC/AHA 2025 intermediate risk | [ ] |
| hs-CRP at-risk | ≥ 3.0 mg/L | ACC/AHA 2025 high-risk; 18% T2DM, 34% ASCVD risk per log-unit (NeLSA) | [ ] |
| Acute override | CRP ≥ 10.0 mg/L → at_risk + repeat flag | ACC/AHA 2025 stability guidance | [ ] |
| NLR MetS cutoff (supporting) | 1.67 | NHANES 26-study meta-analysis n=70,937 (sensitivity 74.3%) | [ ] |
| NLR vascular events (supporting) | > 2.45 | Prospective cohort HR 2.217 for diabetic retinopathy | [ ] |

### Excluded populations

- [ ] Patients with acute infection, trauma, or autoimmune flare (CRP >10 mg/L — acute override applies)
- [ ] Patients on oral contraceptives or HRT (artificially elevated CRP; sex documented in questionnaire.json)
- [ ] Patients on statins (CRP suppressed; medication context required from long_term_medications)
- [ ] Children and adolescents (adult thresholds inappropriate; NLR reference ranges differ)
- [ ] Elderly >75 (NLR reference range shifts to 0.89–8.80; age derivable from date_of_birth)
- [ ] Patients with chronic autoimmune conditions (rheumatoid arthritis, lupus, IBD) — CRP chronically elevated for non-metabolic reasons; `chronic_conditions` in questionnaire.json

### Additional notes

```
[Reviewer to complete]
```

### Sign-off statement

I confirm that the signal thresholds, override logic, excluded populations, limitations, and
the four pending decisions documented in KBP-0005 have been reviewed against the cited research
evidence.

**Signed:** ___________________________

**Date:** ___________________________

---

*This document was generated by Claude Translation Engine under Research-to-Knowledge Translation
Specification v1. All four decisions must be completed before this package proceeds to
Layer B implementation.*
