# Clinical Sign-Off — KBP-0010 Metabolic Inflammation

## Review Status

**Status: PENDING REVIEW**

This document must be completed by a named clinical reviewer and committed before this package
may be promoted to Layer B implementation. No code may be committed to `backend/core/` without
a completed sign-off.

---

## Package Information

| Field | Value |
|-------|-------|
| Package ID | KBP-0010 |
| Package directory | `knowledge_bus/packages/pkg_metabolic_inflammation/` |
| Signal | `signal_metabolic_inflammation` |
| Translation mode | Creation — new signal (cellular inflammation; NLR-primary) |
| Primary metric | `nlr` |
| Source document | `knowledge_bus/research/papers/4-Chronic-Inflammation-Metabolism-Crosstalk.md` |
| Translation date | 2026-03-10 |
| Translated by | Claude Translation Engine — Research-to-Knowledge Translation Specification v1 |

---

## CRITICAL: Three Decisions Required Before Implementation

### Decision 1 — Relationship with KBP-0005 (signal_systemic_inflammation)

KBP-0005 and KBP-0010 address the same biological domain (metaflammation) from
different angles:

| Aspect | KBP-0005 | KBP-0010 |
|--------|----------|----------|
| Signal | `signal_systemic_inflammation` | `signal_metabolic_inflammation` |
| Primary | `crp` (humoral; cytokine load) | `nlr` (cellular; innate immune) |
| Thresholds | CRP < 1.0 / 1.0–2.0 / ≥ 2.0 | NLR < 2.0 / 2.0–3.0 / > 3.0 |

Both are clinically valid but answer different questions. hs-CRP captures IL-6-driven
hepatic response; NLR captures neutrophil mobilisation and lymphocyte suppression.
They are complementary — a user could have elevated NLR with normal CRP (early
cellular activation before cytokine cascade) or elevated CRP with normal NLR
(e.g., acute vs chronic patterns).

**Decision required:**
- [ ] Retain both signals — expose `signal_systemic_inflammation` (KBP-0005) and
      `signal_metabolic_inflammation` (KBP-0010) as distinct outputs in the platform
- [ ] Merge into a single composite inflammation signal — select dominant primary metric
- [ ] Defer KBP-0010 until clinical review of KBP-0005 is complete first

---

### Decision 2 — METS-IR Implementation Priority

METS-IR = ln[(2 × FBG_mg_dL) + TG_mg_dL] × BMI / ln(HDL_mg_dL)

All inputs are available (glucose, triglycerides, hdl_cholesterol in biomarkers.yaml;
BMI in lifestyle_registry.yaml — same pattern as tyg_bmi_index). Implementation is a
standard sprint item in ratio_registry.py — NOT an architecture gap.

When available, METS-IR activates as an at_risk override rule (> 40.56) providing
an integrative insulin resistance dimension alongside NLR.

**Decision required:**
- [ ] Prioritise mets_ir in the SSOT extension sprint — implement alongside other
      ratio_registry additions (e.g., lactate from KBP-0008)
- [ ] Deprioritise mets_ir — NLR and hs-CRP overrides are sufficient for current scope
- [ ] Document mets_ir as a required element of the KB-S9 implementation spec

---

### Decision 3 — Residual Inflammatory Risk (RIR) Output Flag

ESC/EAS 2025 defines residual inflammatory risk (RIR) as: patients achieving
LDL-C < 70 mg/dL (< 1.81 mmol/L) who retain hs-CRP ≥ 2.0 mg/L. These patients
remain at elevated MACE risk despite lipid control — colchicine is recommended.

The current signal schema cannot express a treatment-conditional threshold
(outcome depends on whether a separate lipid target has been met). Options:

**Decision required:**
- [ ] Implement RIR as a runtime output annotation — when ldl_cholesterol < 1.81 mmol/L
      AND crp ≥ 2.0 mg/L, append a "residual_inflammatory_risk: true" flag to the
      signal output (engineering decision for KB-S9)
- [ ] Defer RIR detection — document as a known limitation; handle in clinical report
      layer rather than signal layer
- [ ] Request schema enhancement to support multi-condition output flags natively

---

## Derived Metrics Status

| Metric | Formula | Status | Notes |
|--------|---------|--------|-------|
| `nlr` | neutrophils / lymphocytes | ✓ IN PLATFORM | Confirmed in ratio_registry.py DERIVED_IDS |
| `sii` | (platelets × neutrophils) / lymphocytes | ✓ IN PLATFORM | Confirmed in ratio_registry.py DERIVED_IDS |
| `mets_ir` | ln[(2×FBG_mg) + TG_mg] × BMI / ln(HDL_mg) | ✗ NOT IN PLATFORM | Standard sprint item — tracked in SSOT_GAPS.md |

---

## Evidence Summary

### Primary evidence

**Dong et al. (Cardiovascular Diabetology, 2023; DOI: 10.1186/s12933-023-01998-y)**
- Prospective cohort (NHANES 2003–2016); n=3,251; median follow-up 91 months
- NLR > 3.48: HR 2.03 all-cause mortality, HR 2.76 CVD mortality in diabetes
- Supports NLR > 3.0 as at_risk tier boundary

**Kailuan Cohort / Wang et al. (JAPI, 2025)**
- n=94,841; follow-up 13.1 years
- MetS + hs-CRP > 3.0 mg/L → HR 1.85 heart failure
- Supports hs-CRP as a clinically important override marker

**Zhang et al. (Cardiovascular Diabetology, 2025; DOI: 10.1186/s12933-024-02220-z)**
- Meta-analysis; multiple cohorts
- METS-IR inflection point 40.56 for CVD risk acceleration

**MELANY Cohort / Twig et al. (Diabetes Care, 2013; DOI: 10.2337/dc12-1143)**
- n=24,897 young males; follow-up 7.5 years
- WBC > 6,900 cells/µL → 52% increased diabetes risk
- Supports WBC > 11.0 ×10⁹/L leukocytosis override

### Guideline anchoring

**ESC/EAS 2025 Focused Update**
- Universal hs-CRP screening; RIR defined as hs-CRP ≥ 2.0 with controlled LDL

---

## Known Limitations

1. **METS-IR not yet in platform.** mets_ir override rule is schema-documented but
   inactive until ratio_registry.py is extended. Tracked in SSOT_GAPS.md.

2. **Residual Inflammatory Risk requires treatment data.** RIR detection needs LDL-C
   target status — not expressible in current signal schema. See Decision 3.

3. **NLR is sex-independent in current implementation.** NLR may vary with pregnancy,
   menstrual cycle phase, and hormonal treatments. Age stratification (adult 0.78–3.53;
   elderly >75: 0.89–8.80) not implemented — the 2.0/3.0 boundaries are validated for
   adults 18–75.

4. **Excluded populations must be flagged at runtime:**
   - Acute infections, recent major trauma/surgery (hs-CRP and NLR will be elevated acutely)
   - Pregnant individuals (WBC and NLR naturally trend higher)
   - Primary haematologic malignancies (CML, CLL — NLR unreliable)
   - Patients on corticosteroids (induced neutrophilia/lymphopenia artificially inflates NLR)
   - SGLT2 inhibitors and GLP-1 RAs reduce NLR and hs-CRP — may mask risk

5. **Asian vs Western cohort gap.** NLR threshold effects in North American populations
   are smaller than in Asian cohorts (NHANES data suggests some attenuation). Primary
   evidence (Dong et al.) is NHANES (US population) — applies broadly.

6. **Overlap with KBP-0005.** Both packages reference hs-CRP. The crp_acute_response
   override in this package (> 10.0) is consistent with KBP-0005's crp_acute_override.
   At implementation, the runtime layer should deduplicate acute-CRP flagging.

---

## Clinical Reviewer Sign-Off

**Reviewer name:** [PENDING]

**Role / credentials:** [PENDING]

**Review date:** [PENDING]

### Decision checklist (all three required)

- [ ] **Decision 1** — Signal architecture (dual signals vs merged vs deferred)
- [ ] **Decision 2** — METS-IR implementation priority
- [ ] **Decision 3** — Residual Inflammatory Risk output flag approach

### Threshold acceptance

| Threshold | Value | Evidence source | Accepted |
|-----------|-------|----------------|---------|
| NLR optimal | < 2.0 | Leucuța et al.; NHANES cross-sectional | [ ] |
| NLR suboptimal | 2.0 – 3.0 | Dose-response meta-analysis (26 studies; n=70,937) | [ ] |
| NLR at_risk | > 3.0 | Dong et al. 2023 (n=3,251; NLR > 3.48 = 2.03× mortality) | [ ] |
| CRP acute override | > 10.0 → at_risk | ACC/AHA 2025; standard clinical practice | [ ] |
| WBC leukocytosis override | > 11.0 → at_risk | Standard clinical threshold | [ ] |
| METS-IR override | > 40.56 → at_risk | Zhang et al. 2025 meta-analysis | [ ] |

### Excluded populations

- [ ] Patients with acute infections, trauma, or recent surgery
- [ ] Pregnant individuals
- [ ] Haematologic malignancy (CML, CLL, or similar)
- [ ] Patients on corticosteroids (artificial NLR elevation)
- [ ] Patients on SGLT2 inhibitors / GLP-1 RAs (NLR and CRP may be suppressed)
- [ ] Elderly > 75 years (NLR reference range shifts — 0.89–8.80 vs adult 0.78–3.53)

### Additional notes

```
[Reviewer to complete]
```

### Sign-off statement

I confirm that the signal thresholds, override logic, excluded populations, limitations,
and the three pending decisions documented in KBP-0010 have been reviewed against the
cited research evidence.

**Signed:** ___________________________

**Date:** ___________________________

---

*This document was generated by Claude Translation Engine under Research-to-Knowledge Translation
Specification v1. All three decisions must be completed before this package proceeds to
Layer B implementation.*
