# Clinical Sign-Off — KBP-0004 Hepatic Metabolic Stress

## Review Status

**Status: PENDING REVIEW**

This document must be completed by a named clinical reviewer and committed before this package
may be promoted to Layer B implementation. No code may be committed to `backend/core/` without
a completed sign-off.

---

## Package Information

| Field | Value |
|-------|-------|
| Package ID | KBP-0004 |
| Package directory | `knowledge_bus/packages/pkg_hepatic_metabolic_stress/` |
| Signal | `signal_hepatic_metabolic_stress` |
| Translation mode | Creation — new threshold basis and primary metric differ from KBP-0001 |
| Primary metric (interim) | `derived.tyg_index` (hepatic thresholds 8.21 / 8.97) |
| Primary metric (research-preferred) | `derived.tyg_bmi_index` — AVAILABLE (see below) |
| Source document | `knowledge_bus/research/study_03_hepatic_metabolic_stress.md` |
| Translation date | 2026-03-08 |
| Translated by | Claude Translation Engine — Research-to-Knowledge Translation Specification v1 |

---

## CRITICAL: Four Decisions Required Before Implementation

### Decision 1 — Primary Metric: TyG vs TyG-BMI

The research study (Malek et al. 2025; n=339,087; AUC 0.83) identifies **TyG-BMI** as the
superior primary metric for MASLD detection.

**CORRECTION (2026-03-08):** An earlier draft of this document flagged TyG-BMI as blocked due
to missing SSOT anthropometrics. This was incorrect. `weight_kg` and `height_cm` are confirmed
present in `backend/ssot/lifestyle_registry.yaml`, and `bmi` is already a computed derived metric
in that registry (`weight_kg / (height_cm/100)²`). TyG-BMI = TyG × BMI is therefore computable
without any SSOT extension.

**Decision required:**
- [ ] Upgrade primary metric to `derived.tyg_bmi_index` — implement TyG-BMI in KB-S9 alongside `derived.tyg_index`
- [ ] Retain `derived.tyg_index` as primary metric — use TyG-BMI as a supporting metric only
- [ ] Document preferred threshold: TyG-BMI ≥ 180.71 for at-risk (Liu et al., n=4,753)

Note: the signal library `primary_metric` field currently points to `derived.tyg_index`. If
TyG-BMI is selected, the signal library will need to be updated before KB-S9.

---

### Decision 2 — KBP-0001 Threshold Delta

KBP-0001 contains `signal_hepatic_metabolic_stress` with a **different design**:

| Aspect | KBP-0001 | KBP-0004 |
|--------|----------|----------|
| Primary metric | `derived.ast_alt_ratio` | `derived.tyg_index` |
| Optimal | AST/ALT ≥ 0.8 | TyG < 8.21 |
| Suboptimal | AST/ALT 0.6–0.79 | TyG 8.21–8.96 |
| At-risk | AST/ALT < 0.6 | TyG ≥ 8.97 |

The AST/ALT ratio in KBP-0001 reflects the **pattern of liver injury** (ratio < 0.6 suggests
heavy metabolic stress pattern). The TyG-based approach in KBP-0004 reflects **metabolic risk
for hepatic steatosis** (upstream insulin resistance driving fat accumulation).

Both are clinically valid but answer different questions. The research evidence supports the
TyG approach as a more sensitive early predictor of MASLD.

**Decision required:**
- [ ] Adopt KBP-0004 TyG-based thresholds — replace KBP-0001 design at implementation
- [ ] Retain both metrics — use TyG as primary, AST/ALT as supporting
- [ ] Defer pending further clinical review

---

### Decision 3 — Sex-Specific ALT Thresholds

AASLD (2023) recommends sex-specific ALT thresholds:
- Suboptimal / at-risk boundary: **>33 IU/L (male)**, **>25 IU/L (female)**

The signal library schema does not currently support sex-specific threshold values. However,
`biological_sex` is confirmed present in `backend/ssot/questionnaire.json` as a required
questionnaire field. Sex-specific logic is therefore implementable at runtime (KB-S9) even
though it cannot be expressed as a single signal library threshold.

This package uses:
- `alt_acute_override`: ALT ≥ 100 IU/L → at_risk (acute injury, sex-independent)
- `ald_pattern_override`: AST/ALT ≥ 2.0 AND ALT ≥ 33 → at_risk (ALD pattern)
- The TyG primary thresholds are sex-independent

**Design gap:** A female user with ALT 26–32 IU/L would be suboptimal per AASLD but not
captured by the current override rules (which use 100 IU/L and 33 IU/L respectively).

**Decision required:**
- [ ] Accept current design — document sex-specific ALT gap as a known limitation; handle in runtime KB-S9 using `biological_sex` from questionnaire
- [ ] Request schema enhancement to support sex-stratified thresholds natively

---

### Decision 4 — FIB-4 Implementation Path

FIB-4 = (age × AST) / (platelets × √ALT) — the gold-standard non-invasive fibrosis rule-out.

- `ast` ✓ in SSOT (biomarkers.yaml)
- `alt` ✓ in SSOT (biomarkers.yaml)
- `platelets` ✓ in SSOT (biomarkers.yaml)
- `age` — **derivable from `date_of_birth`** in `questionnaire.json` (confirmed present as required field)

FIB-4 is therefore computable if the runtime layer derives age from `date_of_birth`. This is
an engineering decision, not a data availability gap.

AASLD/EASL thresholds: FIB-4 < 1.30 rules out advanced fibrosis (NPV >90%).

**Decision required:**
- [ ] Implement age derivation from `date_of_birth` in KB-S9; implement FIB-4 at same time
- [ ] Deprioritise FIB-4 — TyG-based risk stratification is sufficient for current scope
- [ ] Document age derivation as a prerequisite for KB-S9 engineering spec

---

## Evidence Summary

### Primary evidence

**Zhang/Zheng et al. meta-analysis (Lipids in Health and Disease, 2018)**
- Systematic review and dose-response meta-analysis; n=105,365; 12 studies; median follow-up 6.5 years
- OR 2.84 (95% CI 2.01–4.01) per unit increase in TyG for NAFLD/MASLD risk
- Q4 TyG (>8.97) associated with highest incident risk
- Supports 8.21 (suboptimal boundary) and 8.97 (at-risk boundary)

**Malek et al. (PLOS ONE, 2025; doi:10.1371/journal.pone.0324483)**
- 35 studies; n=339,087
- TyG-BMI pooled AUC 0.83 (95% CI 0.81–0.86) for MASLD diagnosis
- Confirms TyG-BMI as the superior composite metric — blocked by SSOT gap

**Ding et al. UK Biobank (Cardiovascular Diabetology, 2025; doi:10.1186/s12933-024-02345-w)**
- n=97,331 MASLD patients; median follow-up 13.56 years
- TyG-BMI Q4 vs Q1: HR 1.35 (95% CI 1.28–1.42) CVD; HR 1.26 all-cause mortality
- Confirms clinical outcome relevance at population scale

### Guideline anchoring

**AASLD Practice Guidance (Hepatology, 2023)**
- MASLD nomenclature adopted; ALT >33 (M) / >25 (F) for MASLD screening
- FIB-4 <1.30 to rule out advanced fibrosis; basis for override rules

**EASL-EASD-EASO Guidelines (Journal of Hepatology, 2024)**
- FIB-4 thresholds 1.30 (rule-out) and 2.67 (rule-in) for advanced fibrosis
- Stepwise biomarker approach endorsed

---

## New Derived Metrics Required

| Metric | Formula | Status | Blocker |
|--------|---------|--------|---------|
| `derived.tyg_index` | ln((TG_mg × Glucose_mg) / 2) | NOT in ratio_registry.py | Required for KB-S9 |
| `derived.tyg_bmi_index` | TyG × BMI (kg/m²) | NOT in ratio_registry.py | BMI available in lifestyle_registry.yaml — implement in KB-S9 |
| `derived.fib_4` | (age × AST) / (platelets × √ALT) | NOT in ratio_registry.py | age derivable from date_of_birth in questionnaire.json |
| `derived.ast_alt_ratio` | AST / ALT | Already in ratio_registry.py | None |

Note: `derived.tyg_index` is also required by KBP-0002 (insulin resistance). KB-S9 should
implement it once for both signals.

---

## Known Limitations

1. **TyG-BMI upgrade pending KB-S9 decision.** `weight_kg`, `height_cm`, and `bmi` are
   confirmed available in `lifestyle_registry.yaml`. TyG-BMI is computable — see Decision 1
   above for the upgrade decision. Until upgraded, TyG alone may underestimate risk in lean
   individuals (~7% of MASLD cases).

2. **Sex-specific ALT thresholds not modelled.** AASLD recommends different cut-offs for
   males and females. This signal applies sex-independent TyG thresholds. The female-specific
   ALT gap (25–33 IU/L) is not captured.

3. **FIB-4 requires age derivation.** `date_of_birth` is a required field in `questionnaire.json`.
   Age is derivable at runtime. FIB-4 is unblocked pending an engineering decision to implement
   age calculation — see Decision 4 above.

4. **TyG thresholds derived from predominantly Asian cohorts.** Many underlying studies used
   East Asian populations where triglyceride metabolism may differ. Performance in African
   American populations (where TG is often paradoxically lower despite high IR) requires
   independent validation.

5. **Snapshot biomarkers miss dynamic MASLD.** Single-timepoint measurements miss individuals
   with "regressed MASLD" who retain elevated CVD risk compared to "never MASLD."

6. **Medication confounders.** ALT is elevated by acetaminophen, statins, and antibiotics
   (drug-induced liver injury). Triglycerides are elevated by beta-blockers, thiazides,
   oestrogen/HRT, and antipsychotics. Clinical interpretation must account for medications.

7. **Athletes and sarcopenia.** AST/ALT ratio and FIB-4 are unreliable in these populations
   due to muscle-derived AST contributions.

8. **Formula image gap.** The source research document embedded key formulas as images which
   could not be parsed. Standard published formulas have been used. The TyG-BMI threshold of
   180.71 is from Liu et al. (n=4,753) as quoted in the text.

---

## Clinical Reviewer Sign-Off

**Reviewer name:** [PENDING]

**Role / credentials:** [PENDING]

**Review date:** [PENDING]

### Decision checklist (all four required)

- [ ] **Decision 1** — Primary metric selection (TyG interim vs TyG-BMI upgrade path)
- [ ] **Decision 2** — KBP-0001 delta resolution (TyG vs AST/ALT primary metric)
- [ ] **Decision 3** — Sex-specific ALT threshold handling
- [ ] **Decision 4** — FIB-4 implementation path (age SSOT sprint priority)

### Threshold acceptance

| Threshold | Value | Evidence source | Accepted |
|-----------|-------|----------------|---------|
| TyG optimal | < 8.21 | Zhang/Zheng meta-analysis (n=105,365) | [ ] |
| TyG suboptimal | 8.21 – 8.96 | Zhang/Zheng hepatic steatosis quartiles | [ ] |
| TyG at-risk | ≥ 8.97 | Zhang/Zheng Q4 (OR 2.84 per unit) | [ ] |
| ALT acute override | ≥ 100 IU/L → at_risk | AASLD acute injury threshold | [ ] |
| ALD pattern override | AST/ALT ≥ 2.0 AND ALT ≥ 33 → at_risk | AASLD/EASL guideline | [ ] |
| TG pancreatitis override | TG ≥ 5.6 mmol/L → at_risk | ESC/EAS guideline | [ ] |

### Excluded populations

- [ ] Athletes and high-resistance-exercise users (elevated muscle AST)
- [ ] Sarcopenic patients (low muscle AST, underestimates ratio)
- [ ] Lean MASLD (TyG-BMI not available; TyG alone may miss lean phenotype)
- [ ] Children (adult thresholds inappropriate)
- [ ] Chronic alcohol use (ALD pattern override applies; MASLD vs ALD distinction required)
- [ ] Patients on statins, acetaminophen, or antipsychotics (enzyme confounders)

### Additional notes

```
[Reviewer to complete]
```

### Sign-off statement

I confirm that the signal thresholds, override logic, excluded populations, limitations, and
the four pending decisions documented in KBP-0004 have been reviewed against the cited research
evidence.

**Signed:** ___________________________

**Date:** ___________________________

---

*This document was generated by Claude Translation Engine under Research-to-Knowledge Translation
Specification v1. All four decisions must be completed before this package proceeds to
Layer B implementation.*
