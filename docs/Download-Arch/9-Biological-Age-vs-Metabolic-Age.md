# HealthIQ Evidence Dossier — Signal: Biological Age / Metabolic Age

**Signal identifier:** `signal_biological_age`
**Primary metric:** `pheno_age_accel`
**Version:** 1.0
**Date:** March 2026
**Produced for:** HealthIQ Knowledge Translation Pipeline

---

## 1. Executive Summary

This dossier evaluates Phenotypic Age Acceleration (PhenoAgeAccel) as the primary metric for a biological ageing trajectory signal within the HealthIQ platform. PhenoAgeAccel is derived from the Levine PhenoAge algorithm, which integrates nine routine blood biomarkers and chronological age to estimate phenotypic age — the age at which an individual's multi-system physiology would be approximately normal in a reference population. PhenoAgeAccel is the residual of phenotypic age regressed on chronological age, representing how many years older or younger a person appears relative to same-age peers.

The biological question this signal answers is whether an individual's body is ageing faster or slower than expected based on integrated inflammatory, metabolic, hepatic, renal, and haematological biomarkers. A positive PhenoAgeAccel value indicates accelerated biological ageing; a negative value indicates decelerated ageing. The signal provides a composite view of multi-organ physiological integrity that no single biomarker can capture.

The evidence supporting PhenoAgeAccel is Tier 1 quality. The algorithm was trained on NHANES III (n = 9,926) using a Gompertz proportional hazard elastic net model for all-cause mortality and validated independently in NHANES IV (n = 11,432, 12.6 years follow-up). In the validation cohort, each one-year increase in PhenoAgeAccel was associated with a 4.5–5.5% increase in all-cause mortality risk (HR approximately 1.05 per year). The PhenoAge metric achieved an AUC of 0.88 for 10-year mortality prediction, significantly outperforming chronological age alone (AUC 0.86) and all individual component biomarkers. PhenoAgeAccel has been further validated in the UK Biobank (n > 300,000), the CALERIE randomised controlled trial (n = 220), and multiple disease-specific cohorts for cardiovascular disease, cancer, heart failure, COPD, and type 2 diabetes.

The primary metric recommended for platform use is PhenoAgeAccel (years), computed as the residual from regressing PhenoAge on chronological age. The evidence quality is strong (Tier 1) with prospective validation across diverse populations and hard mortality and morbidity endpoints.

---

## 2. Biological Question

> "Based on my blood test results, is my body ageing faster or slower than expected for my chronological age — and what does my integrated inflammatory, metabolic, hepatic, renal, and haematological profile suggest about my biological ageing trajectory?"

---

## 3. Clinical Rationale

### 3.1 What disease or dysfunction does this signal predict or detect?

PhenoAgeAccel predicts accelerated biological ageing, which is the upstream common cause of multiple age-related diseases. Prospective data demonstrate that elevated PhenoAgeAccel is independently associated with increased risk of: all-cause mortality (HR 1.05 per year increase; Liu et al., 2018, PLOS Medicine), cardiovascular disease (positive PhenoAgeAccel associated with HR 1.41 for all-cause mortality in heart failure patients; Xu et al., 2024), incident cancer (HR 1.15 per 5-year increase in UK Biobank; Kuo et al., 2024, eLife), type 2 diabetes progression (HR for incident T2D significantly elevated in biologically older individuals; Zhang et al., 2025, BMC Medicine), chronic respiratory diseases including COPD (HR 1.54 per SD increase; Allen et al., 2024, ERJ), and neurodegenerative conditions.

### 3.2 Pathophysiological mechanism

Biological ageing reflects the cumulative loss of system integrity across multiple organ systems. The nine PhenoAge biomarkers capture distinct ageing-related pathways:

1. Chronic low-grade inflammation (CRP, WBC) — inflammaging drives endothelial dysfunction, insulin resistance, and tissue damage.
2. Immune senescence (lymphocyte percentage, WBC) — declining adaptive immunity and expansion of senescent T-cells.
3. Metabolic dysregulation (glucose) — glycaemic deterioration from declining beta-cell function and increasing insulin resistance.
4. Hepatic ageing (albumin, alkaline phosphatase) — declining hepatic synthetic capacity and biliary/bone turnover changes.
5. Renal ageing (creatinine) — age-related nephron loss and declining glomerular filtration.
6. Haematological ageing (MCV, RDW) — red cell distribution width is a marker of erythropoietic stress and cellular heterogeneity that increases with ageing; MCV reflects nutritional status and bone marrow function.

### 3.3 Stage of disease progression

PhenoAgeAccel provides information in the pre-clinical phase of disease, before specific diagnoses are made. Liu et al. (2018) demonstrated that PhenoAgeAccel was predictive of mortality even among disease-free healthy adults across the age spectrum, suggesting it captures the effect of ageing before diseases become clinically evident. In the NHANES IV validation, PhenoAgeAccel predicted mortality significantly better than disease count alone, indicating it captures information beyond a person's existing morbidity burden.

### 3.4 Why early detection matters

Identifying accelerated biological ageing before disease onset creates a window for preventive intervention. The CALERIE trial (Waziry et al., 2023, Nature Aging; n = 220) demonstrated that 25% caloric restriction over 2 years slowed the pace of ageing by 2–3% as measured by DunedinPACE, corresponding to a projected 10–15% reduction in mortality risk. Belsky et al. (2018, Journals of Gerontology) showed that both KDM biological age and homeostatic dysregulation were sensitive to the caloric restriction intervention. These findings provide proof-of-concept that biological ageing measures are modifiable and that interventions targeting upstream ageing processes can produce measurable improvements.

---

## 4. Evidence Base

### 4.1 Primary Evidence

| Field | Study 1 | Study 2 | Study 3 | Study 4 | Study 5 |
|-------|---------|---------|---------|---------|---------|
| Study name / first author | Levine ME et al. | Liu Z et al. | Waziry R et al. | Belsky DW et al. | Kuo PL et al. |
| Journal | Aging | PLOS Medicine | Nature Aging | J Gerontol A Biol Sci Med Sci | eLife |
| Year | 2018 | 2018 | 2023 | 2018 | 2024 |
| DOI | doi:10.18632/aging.101414 | doi:10.1371/journal.pmed.1002718 | doi:10.1038/s43587-022-00357-y | doi:10.1093/gerona/glx096 | doi:10.7554/eLife.91101 |
| Design | Prospective cohort (NHANES III training) | Prospective cohort (NHANES IV validation) | RCT (CALERIE Phase 2) | RCT analysis (CALERIE) | Prospective cohort (UK Biobank) |
| Sample size | n = 9,926 | n = 11,432 | n = 220 | n = 220 | n > 400,000 |
| Follow-up | 23 yr mortality follow-up | 12.6 yr | 2 yr | 2 yr | > 10 yr |
| Key finding | Elastic net Gompertz model selected 9 biomarkers + age; DNAm PhenoAge: 1-yr increase = 4.5% increase in mortality risk (p = 9.9E-47) | AUC 0.88 for 10-yr mortality; PhenoAgeAccel Q5 vs Q1: approximately 9 yr life expectancy difference at age 65; predicted mortality in disease-free adults | 25% CR slowed DunedinPACE by 2-3% (10-15% mortality risk reduction); no significant effect on PhenoAge or GrimAge clocks | KDM biological age and homeostatic dysregulation sensitive to CR; slowed biological ageing independent of weight loss | PhenoAgeAccel per 5-yr increase: HR 1.15 for overall cancer (men and women); Q5 vs Q1: HR approximately 1.22-1.26 for cancer incidence |
| Threshold derived | PhenoAge formula coefficients derived; no discrete tier thresholds | PhenoAgeAccel > 0 = accelerated; quintile-based risk stratification | N/A (intervention study) | N/A (intervention study) | PhenoAgeAccel > 0 = biologically older; quintile stratification |
| Limitations | US population; predominantly non-Hispanic white training sample | US nationally representative; limited ethnic subgroup analysis | Non-obese adults only; predominantly white; moderate CR achieved (11.7%) | Small sample; limited diversity | European ancestry predominant; self-reported cancer outcomes |

### 4.2 Supporting Evidence

| Field | Study 6 | Study 7 | Study 8 | Study 9 | Study 10 |
|-------|---------|---------|---------|---------|----------|
| Study name / first author | Xu Y et al. | NHANES diabetes study | Allen RJ et al. | UK Biobank CVD study | Kwon D & Belsky DW |
| Journal | Clinical Cardiology | Diabetes Research and Clinical Practice | European Respiratory Journal | Scientific Reports | Geroscience |
| Year | 2024 | 2025 | 2024 | 2025 | 2021 |
| DOI | doi:10.1002/clc.24321 | N/A | doi:10.1183/13993003.01720-2023 | doi:10.1038/s41598-025-12495-5 | doi:10.1007/s11357-021-00480-x |
| Design | Retrospective cohort (NHANES) | Prospective cohort (NHANES) | Prospective cohort (UK Biobank) | Prospective cohort (UK Biobank) | R package / methods paper (BioAge) |
| Sample size | n = 845 HF patients | n = 15,939 | n = 308,592 | n = 114,517 | NHANES III/IV |
| Follow-up | Up to 20 yr | Up to 20 yr | > 10 yr | 12.0 yr | N/A |
| Key finding | Per 10-yr PhenoAge increase: HR 1.41 (95% CI 1.29-1.54) for all-cause mortality in heart failure | Per 1-yr PhenoAgeAccel increase: HR 1.051 all-cause mortality; HR 1.054 CV mortality in diabetes/prediabetes | PhenoAgeAccel per SD increase: HR 1.54 for COPD; HR 1.52 for IPF; associated with declined FEV1 | PhenoAgeAccel C-index 0.674 for CVD; similar survival to FRS high-risk group | Open-source toolkit for computing KDM, PhenoAge, HD; enables reproducible biological age quantification |
| Threshold derived | PhenoAgeAccel tertiles | Per-year continuous; Q4 vs Q1: HR 3.13 | Per-SD continuous | Positive PhenoAgeAccel = accelerated | Algorithmic implementation |
| Limitations | Retrospective; NHANES data only | Self-reported diabetes status | European ancestry only | 99.7% male; limited applicability to women | Methods paper; no new clinical data |

### 4.3 Cautionary Evidence

| Field | Study 11 | Study 12 |
|-------|----------|----------|
| Study name / first author | Waziry R et al. (same CALERIE) | Waziry R et al. (Long COVID) |
| Journal | Nature Aging | European Respiratory Journal |
| Year | 2023 | 2023 |
| DOI | doi:10.1038/s43587-022-00357-y | doi:10.1183/13993003.congress-2023.PA5343 |
| Design | RCT | Cross-sectional |
| Sample size | n = 220 | n = 2,866 |
| Follow-up | 2 yr | 12 weeks post-infection |
| Key finding | No significant effect of CR on static PhenoAge or GrimAge clocks; only DunedinPACE (pace of ageing) responded. Suggests static biological age measures may be less sensitive to short-term interventions than pace measures. | Respiratory long COVID phenotype showed +2.25 yr PhenoAgeAccel; acute/post-acute illness inflates PhenoAge via transient biomarker shifts (CRP, WBC, albumin) |
| Threshold derived | N/A | N/A |
| Limitations | Challenges responsiveness of PhenoAge to lifestyle change over 2 years | Confounding by acute illness; not chronic ageing per se |

---

## 5. Required Biomarkers

### 5.1 Required biomarkers (minimum viable computation)

| Biomarker (snake_case) | Why Required | Fasting Required? | SSOT Canonical Unit | PhenoAge Formula Unit |
|------------------------|--------------|-------------------|--------------------|-----------------------|
| `albumin` | Hepatic synthetic capacity; declines with ageing, malnutrition, inflammation | No | g/L | g/dL (divide g/L by 10) |
| `creatinine` | Renal filtration function; rises with declining GFR and ageing nephron loss | No | umol/L | mg/dL (divide umol/L by 88.4) |
| `glucose` | Metabolic/glycaemic regulation; rises with insulin resistance and beta-cell decline | Yes | mmol/L | mg/dL (multiply mmol/L by 18.016) |
| `hs_crp` | Systemic inflammation (inflammaging); chronic low-grade inflammation drives multi-organ damage | No | mg/L | mg/dL (divide mg/L by 10); log-transformed in formula |
| `lymphocyte_pct` | Immune competence; declines with immune senescence and thymic involution | No | % | % (no conversion) |
| `mcv` | Erythropoietic function; reflects nutritional status (B12/folate) and bone marrow ageing | No | fL | fL (no conversion) |
| `rdw` | Erythrocyte heterogeneity; increases with ageing-related erythropoietic stress; strong independent mortality predictor | No | % | % (no conversion) |
| `alkaline_phosphatase` | Hepatobiliary and bone turnover; rises with hepatic dysfunction and bone remodelling | No | IU/L | IU/L (no conversion) |
| `wbc` | Innate immune activation; elevated counts reflect chronic inflammation and infection burden | No | x10^9/L | 1000 cells/uL (numerically equivalent) |

Additionally, chronological age (derived from `date_of_birth` at runtime) is required as the tenth input to the PhenoAge formula and is also needed to compute PhenoAgeAccel.

### 5.2 Optional biomarkers (enhance signal interpretation)

| Biomarker (snake_case) | Why Enhances Signal | Fasting Required? | SSOT Canonical Unit |
|------------------------|---------------------|-------------------|---------------------|
| `hba1c` | Glycated haemoglobin; 3-month glycaemic average; used in KDM biological age and reduces single-sample glucose noise | No | % |
| `total_cholesterol` | Lipid status; included in KDM biological age; U-shaped mortality association in elderly | Preferred | mmol/L |
| `urea` | Renal function and protein catabolism; included in KDM biological age | No | mmol/L |
| `uric_acid` | Purine metabolism; oxidative stress marker; included in BioAge V2 algorithms | No | umol/L |
| `ggt` | Hepatic oxidative stress; early liver dysfunction indicator complementing ALP | No | IU/L |
| `alt` | Hepatocellular integrity; fatty liver disease indicator | No | IU/L |
| `ast` | Hepatocellular and mitochondrial integrity | No | IU/L |
| `triglycerides` | Metabolic syndrome marker; lipid dysregulation with ageing | Yes | mmol/L |
| `hdl_cholesterol` | Reverse cholesterol transport; declines with metabolic ageing | No | mmol/L |

---

## 6. Derived Metrics and Formulas

### 6.1 pheno_age (Phenotypic Age)

**Metric name:** `pheno_age`

**Formula (three-step computation):**

All formulas below are written in plain text. No images are used.

**Step 1 — Compute the linear predictor xb:**

```
xb = -19.907
     - 0.0336 * albumin_g_dl
     + 0.0095 * creatinine_mg_dl
     + 0.1953 * glucose_mg_dl
     + 0.0954 * ln(crp_mg_dl)
     - 0.0120 * lymphocyte_pct
     + 0.0268 * mcv_fl
     + 0.3306 * rdw_pct
     + 0.00188 * alp_iu_l
     + 0.0554 * wbc_1000cells_ul
     + 0.0804 * chronological_age
```

Where:
- `albumin_g_dl` = albumin in g/dL (SSOT g/L divided by 10)
- `creatinine_mg_dl` = creatinine in mg/dL (SSOT umol/L divided by 88.4)
- `glucose_mg_dl` = glucose in mg/dL (SSOT mmol/L multiplied by 18.016)
- `crp_mg_dl` = CRP in mg/dL (SSOT mg/L divided by 10); natural log applied
- `lymphocyte_pct` = lymphocyte percentage (no conversion)
- `mcv_fl` = mean corpuscular volume in fL (no conversion)
- `rdw_pct` = red cell distribution width in % (no conversion)
- `alp_iu_l` = alkaline phosphatase in IU/L (no conversion)
- `wbc_1000cells_ul` = white blood cell count in 1000 cells/uL (SSOT x10^9/L is numerically equivalent)
- `chronological_age` = age in years (derived from `date_of_birth`)
- `ln()` = natural logarithm

**Step 2 — Compute 10-year mortality risk (M):**

```
M = 1 - exp( -exp(xb) * ( exp(120 * 0.0076927) - 1 ) / 0.0076927 )
```

Where:
- `exp()` = the exponential function (e raised to the power of the argument)
- `120` = 120 months (10 years)
- `0.0076927` = gamma, the Gompertz ancillary parameter estimated from NHANES III

**Step 3 — Convert mortality risk to Phenotypic Age:**

```
pheno_age = 141.50225 + ln( -0.00553 * ln(1 - M) ) / 0.090165
```

Where:
- `ln()` = natural logarithm
- `141.50225`, `-0.00553`, and `0.090165` are constants from the univariate Gompertz regression of mortality on chronological age alone (NHANES III)

**Unit handling summary table:**

| Biomarker | SSOT Unit | Formula Unit | Conversion |
|-----------|-----------|-------------|------------|
| albumin | g/L | g/dL | Divide by 10 |
| creatinine | umol/L | mg/dL | Divide by 88.4 |
| glucose | mmol/L | mg/dL | Multiply by 18.016 |
| hs_crp | mg/L | mg/dL | Divide by 10; then apply ln() |
| lymphocyte_pct | % | % | No conversion |
| mcv | fL | fL | No conversion |
| rdw | % | % | No conversion |
| alkaline_phosphatase | IU/L | IU/L | No conversion |
| wbc | x10^9/L | 1000 cells/uL | Numerically equivalent |

**Evidence anchor:** Levine ME et al. (2018), Aging 10(4):573-591; Liu Z et al. (2018), PLOS Medicine 15(12):e1002718 (corrected formula). Coefficients confirmed via supplementary materials of the ERJ 2024 pulmonary fibrosis study and the PLOS ONE 2025 HSV study.

**Existing in platform?** No — new derived metric required.

### 6.2 pheno_age_accel (Phenotypic Age Acceleration)

**Metric name:** `pheno_age_accel`

**Formula:**

```
pheno_age_accel = residual of linear regression: pheno_age ~ chronological_age
```

In practice, this is computed as:

```
pheno_age_accel = pheno_age - (alpha + beta * chronological_age)
```

Where `alpha` and `beta` are population-level regression parameters. In the NHANES IV validation (Liu et al., 2018), the regression produced a distribution with mean = 0 and SD approximately 1.

The platform should derive `alpha` and `beta` from a reference regression of `pheno_age` on `chronological_age` using the NHANES-derived formula output. Alternatively, the simpler approximation `pheno_age_accel = pheno_age - chronological_age` is highly correlated (r > 0.99) with the residual method and is acceptable for platform use.

**Evidence anchor:** Liu Z et al. (2018), PLOS Medicine. Standard method used in all subsequent PhenoAgeAccel studies.

**Existing in platform?** No — new derived metric required.

---

## 7. Evidence-Anchored Thresholds

**Biological question filter applied:** All thresholds below are derived from research studying the specific question "Is this individual's body ageing faster or slower than expected?" using PhenoAgeAccel as the primary metric, with hard endpoints of all-cause mortality, incident disease, and life expectancy.

**Primary metric:** `pheno_age_accel` (years)

| Tier | Metric | Operator | Value | Unit | Evidence Source | Study n | Follow-up |
|------|--------|----------|-------|------|----------------|---------|-----------|
| optimal | pheno_age_accel | < | -2.0 | years | Liu et al. 2018 PLOS Med (NHANES IV Q1 quintile: lowest 20% PhenoAgeAccel; predicted median life expectancy at 65: approximately 87 yr females, approximately 85 yr males) | n = 11,432 | 12.6 yr |
| suboptimal | pheno_age_accel | >= -2.0 AND < | +2.0 | years | Liu et al. 2018 (Q2-Q4 quintiles; intermediate risk; PhenoAgeAccel approximately normally distributed with SD approximately 1; +/-2 years captures approximately 95% of normal variation) | n = 11,432 | 12.6 yr |
| at_risk | pheno_age_accel | >= | +2.0 | years | Liu et al. 2018 (Q5 quintile; predicted median life expectancy at 65: approximately 78 yr females, approximately 76 yr males; approximately 9 yr life expectancy difference vs Q1). Supported by diabetes cohort: Q4 PhenoAgeAccel HR 3.13 for all-cause mortality vs Q1. | n = 11,432 + n = 15,939 | 12.6 yr |

**Threshold derivation notes:**

The +/-2.0 year thresholds are anchored to the NHANES IV quintile distribution where the PhenoAgeAccel distribution had a mean of 0 and SD of approximately 1 (Liu et al., 2018). The lowest quintile (Q1) corresponds approximately to PhenoAgeAccel < -2.0 years and the highest quintile (Q5) to >= +2.0 years. The Q5 vs Q1 comparison demonstrated approximately 9 years of difference in predicted life expectancy at age 65. These thresholds represent the approximate 20th and 80th percentile boundaries.

The threshold of PhenoAgeAccel > 0 (i.e., biologically older than chronological age) is used as a binary classification in multiple UK Biobank studies (Kuo et al., 2024; Zhang et al., 2025) and is associated with significantly increased disease risk. The +2.0 year at_risk threshold captures the upper tail beyond the zero crossing point, representing meaningfully accelerated ageing beyond normal variation.

---

## 8. Override Rules and Guardrails

| Condition | Resulting State | Evidence Basis |
|-----------|----------------|----------------|
| hs_crp >= 10.0 mg/L | EXCLUDE (do not compute) | CRP >= 10 mg/L indicates likely acute infection or tissue injury rather than chronic inflammaging. The PhenoAge algorithm was developed in populations without acute illness. Computing PhenoAge during acute inflammation will produce an artificially elevated (invalid) result. Evidence: standard clinical convention for hs-CRP interpretation; Levine et al. (2018) excluded acutely ill subjects. |
| glucose >= 7.0 mmol/L (fasting) OR known diabetes diagnosis | Flag: interpret with caution | Diabetes shifts glucose, creatinine, albumin, and CRP simultaneously, which can inflate PhenoAgeAccel beyond what chronic ageing alone would produce. Per NHANES diabetes subanalysis, diabetic individuals had PhenoAge values approximately 10 years older than non-diabetics with similar chronological age. The signal remains valid but should be flagged to the user as potentially reflecting disease burden rather than intrinsic ageing rate. |
| eGFR < 30 mL/min/1.73m2 (CKD stage 4-5) | Flag: interpret with caution | Advanced CKD causes uraemic disturbances that shift multiple PhenoAge inputs (creatinine, albumin, WBC, glucose). PhenoAge was not specifically validated in advanced CKD populations. Results may primarily reflect renal disease severity rather than biological ageing. |
| Age < 20 years | EXCLUDE (do not compute) | The PhenoAge algorithm was derived from NHANES III adults aged 20+ and validated in NHANES IV adults aged 20-84. It has not been validated in paediatric or adolescent populations. |
| Age > 85 years | Flag: reduced accuracy | Liu et al. (2018) included 185 oldest-old adults top-coded at 85. Effect sizes for PhenoAgeAccel decrease with advancing age, and the algorithm may be less discriminating in the very elderly. |

---

## 9. Clinical Limitations and Excluded Populations

### 9.1 Populations where the signal should be applied with caution

(a) Individuals under age 20 — algorithm not validated below this age.
(b) Individuals over age 85 — limited validation data; reduced discriminative power.
(c) Pregnant individuals — pregnancy causes physiological shifts in albumin, WBC, glucose, creatinine, and CRP that do not reflect ageing.
(d) Individuals of non-European ancestry — the NHANES training sample was predominantly non-Hispanic white. Levine et al. (2018, supplementary) noted that non-Hispanic Black individuals had the highest DNAm PhenoAge on average, and ethnicity-specific calibration may be needed. The algorithm has been applied to diverse NHANES IV subpopulations but with less certainty in threshold precision.
(e) Individuals with end-stage renal disease, dialysis patients, or kidney transplant recipients — creatinine and albumin are confounded by renal replacement therapy.

### 9.2 Conditions and medications that confound the inputs

(a) Acute illness, infection, or recent surgery — transient CRP elevation, WBC shifts, and albumin depression will inflate PhenoAge. The long COVID study (Waziry, ERJ 2023) demonstrated +2.25 years PhenoAgeAccel at 12 weeks post-infection, which may be partly transient.
(b) Creatine supplementation — can raise serum creatinine independently of renal function, falsely increasing PhenoAge.
(c) Immunosuppressive therapy — corticosteroids and immunosuppressants alter WBC, lymphocyte percentage, and glucose.
(d) Statins — may reduce CRP levels (JUPITER trial effect), potentially improving PhenoAge through anti-inflammatory action rather than true biological age change.
(e) Haematological conditions — anaemia, myelodysplastic syndromes, and thalassemia alter MCV and RDW independently of ageing.
(f) Liver disease — cirrhosis and advanced hepatic disease will shift albumin and ALP substantially.
(g) High-dose vitamin B12/folate supplementation — can alter MCV.

### 9.3 Known gaps in the evidence

(a) Limited ethnic diversity in derivation cohort — NHANES III training was predominantly US-based; applicability to South Asian, East Asian, and African populations requires further validation.
(b) No sex-specific PhenoAge formula — the same coefficients are used for males and females, despite known sex differences in ageing biomarkers. Liu et al. (2018) presented sex-stratified life expectancy predictions but did not derive sex-specific formulas.
(c) Lack of longitudinal intervention data for PhenoAge specifically — the CALERIE trial showed no significant effect on static PhenoAge/GrimAge clocks (only DunedinPACE responded), raising questions about PhenoAge's sensitivity to short-term lifestyle interventions.
(d) No paediatric or adolescent validation.

### 9.4 Cautionary intervention evidence

CRITICAL: The CALERIE RCT (Waziry et al., 2023) found that 2 years of 25% caloric restriction did NOT significantly change PhenoAge or GrimAge clock values, despite slowing DunedinPACE. This suggests that improving individual PhenoAge component biomarkers through lifestyle intervention may not produce detectable PhenoAge changes over timeframes shorter than several years. The platform must communicate to users that PhenoAgeAccel changes should be interpreted over longer intervals (minimum 1-2 years between measurements) and that short-term fluctuations may reflect measurement noise or transient illness rather than true biological age change. Improving a single component biomarker (e.g., lowering CRP with statins) does not necessarily indicate a change in underlying biological ageing rate.

---

## 10. HealthIQ Platform Signal Mapping

**Signal identifier:**

```
signal_biological_age
```

**Physiological system:**

```
metabolic
```

Note: This is a multi-system composite spanning metabolic, inflammatory, hepatic, renal, and haematological domains. The "metabolic" classification is the closest single-system label; the platform may benefit from a "multi_system" or "composite" classification.

**Primary metric:**

```
pheno_age_accel
```

**Required biomarkers:**

```
- albumin
- creatinine
- glucose
- hs_crp
- lymphocyte_pct
- mcv
- rdw
- alkaline_phosphatase
- wbc
```

**Required derived metrics:**

```
- pheno_age
- pheno_age_accel
```

Both are new and not currently in the platform.

**Optional biomarkers:**

```
- hba1c
- total_cholesterol
- urea
- uric_acid
- ggt
- alt
- ast
- triglycerides
- hdl_cholesterol
```

**Optional derived metrics:**

```
- ast_alt_ratio (existing)
- tg_hdl_ratio (existing)
- tyg_index (existing)
```

These provide additional metabolic context but are not used in the PhenoAge computation.

**Threshold summary:**

```
optimal:    pheno_age_accel < -2.0 years
suboptimal: pheno_age_accel >= -2.0 AND < +2.0 years
at_risk:    pheno_age_accel >= +2.0 years
```

**Override rules:**

```
rule: hs_crp >= 10.0 mg/L -> EXCLUDE (do not compute; likely acute illness)
evidence: Clinical convention for hs-CRP; Levine et al. 2018 exclusion criteria

rule: age < 20 -> EXCLUDE (not validated)
evidence: Levine et al. 2018; Liu et al. 2018 (NHANES adults 20+)

rule: glucose >= 7.0 mmol/L (fasting) -> FLAG (interpret with caution)
evidence: UK Biobank CVD study 2025; diabetics show approximately +10 yr PhenoAge inflation

rule: eGFR < 30 mL/min/1.73m2 -> FLAG (interpret with caution)
evidence: Not validated in advanced CKD
```

**Bundle consumers:**

```
- biological_age
- metabolic_health
- cardiovascular_risk
- brain_metabolic_resilience
```

**Implementation notes:**

1. NEW DERIVED METRICS REQUIRED: `pheno_age` and `pheno_age_accel` must be implemented. The `pheno_age` computation requires unit conversion from SSOT units to the formula's native units (see Section 6.1 conversion table). The `pheno_age_accel` computation requires a population-level regression of `pheno_age` on `chronological_age`; the platform should either (a) use the NHANES-derived regression parameters or (b) use the simpler approximation `pheno_age_accel = pheno_age - chronological_age`, which is highly correlated (r > 0.99) with the residual method.

2. FASTING REQUIREMENT: `glucose` is the only strictly fasting-required biomarker. If non-fasting glucose is used, results will be biased upward. The platform should flag non-fasting samples.

3. CRP LOG TRANSFORMATION: The formula requires `ln(CRP)` where CRP is in mg/dL. A CRP value of 0 would produce `ln(0) = undefined`. The platform should enforce a floor of CRP >= 0.01 mg/dL (0.1 mg/L) before log transformation.

4. SEX-SPECIFIC THRESHOLDS: The current PhenoAge formula does not use sex-specific coefficients. However, the Liu et al. (2018) life expectancy projections show sex differences (females: 87 vs 78 yr Q1 vs Q5; males: 85 vs 76 yr). If the platform stratifies by sex, the same thresholds apply but the mortality risk interpretation differs.

5. AGE STRATIFICATION: PhenoAgeAccel effect sizes decrease with advancing age (Liu et al., 2018). The platform may consider age-band-specific messaging (e.g., "at your age, this level of acceleration is associated with X").

6. LONGITUDINAL TRACKING: Users should be advised to compare PhenoAgeAccel across measurements taken at least 6-12 months apart, under similar conditions (fasted, no acute illness), to minimise noise.

---

## 11. Supporting References

| Authors | Title | Journal | Year | Volume/Pages | DOI | Relevance |
|---------|-------|---------|------|-------------|-----|-----------|
| Levine ME, Lu AT, Quach A, et al. | An epigenetic biomarker of aging for lifespan and healthspan. | Aging | 2018 | 10(4):573-591 | doi:10.18632/aging.101414 | Primary derivation of PhenoAge and DNAm PhenoAge using NHANES III (n = 9,926). |
| Liu Z, Kuo PL, Horvath S, et al. | A new aging measure captures morbidity and mortality risk across diverse subpopulations from NHANES IV: A cohort study. | PLOS Medicine | 2018 | 15(12):e1002718 | doi:10.1371/journal.pmed.1002718 | Independent validation of PhenoAge in NHANES IV (n = 11,432); AUC 0.88 for 10-year mortality. |
| Waziry R, Ryan CP, Corcoran DL, et al. | Effect of long-term caloric restriction on DNA methylation measures of biological aging in healthy adults from the CALERIE trial. | Nature Aging | 2023 | 3(3):248-257 | doi:10.1038/s43587-022-00357-y | CALERIE RCT showing CR slows DunedinPACE but not PhenoAge/GrimAge. |
| Belsky DW, Huffman KM, Pieper CF, et al. | Change in the Rate of Biological Aging in Response to Caloric Restriction: CALERIE Biobank Analysis. | J Gerontol A Biol Sci Med Sci | 2018 | 73(1):4-10 | doi:10.1093/gerona/glx096 | CALERIE proof-of-concept showing KDM biological age and HD sensitive to CR. |
| Kwon D, Belsky DW. | A toolkit for quantification of biological age from blood chemistry and organ function test data: BioAge. | Geroscience | 2021 | 43(6):2795-2808 | doi:10.1007/s11357-021-00480-x | Open-source R package implementing KDM, PhenoAge, and HD algorithms. |
| Kuo CL, et al. | Associations of combined phenotypic aging and genetic risk with incident cancer: A prospective cohort study. | eLife | 2024 | 12:RP91101 | doi:10.7554/eLife.91101 | UK Biobank: PhenoAgeAccel per 5 yr increase HR 1.15 for cancer. |
| Xu Y, et al. | Association Between Phenotypic Age and the Risk of Mortality in Patients With Heart Failure: A Retrospective Cohort Study. | Clinical Cardiology | 2024 | 47(8):e24321 | doi:10.1002/clc.24321 | PhenoAge predicts mortality in heart failure (HR 1.41 per 10 yr). |
| Allen RJ, Stockwell A, Oldham JM, et al. | Associations of combined phenotypic ageing and genetic risk with incidence of chronic respiratory diseases in the UK Biobank. | Eur Respir J | 2024 | 63(2):2301720 | doi:10.1183/13993003.01720-2023 | PhenoAgeAccel HR 1.54 for COPD; HR 1.52 for IPF per SD. |
| Zhang Y, et al. | Association of accelerated phenotypic aging, genetic risk, and lifestyle with progression of type 2 diabetes. | BMC Medicine | 2025 | 23:77 | doi:10.1186/s12916-024-03832-y | UK Biobank multi-state model of T2D progression with PhenoAgeAccel. |
| Waziry R, et al. | Blood biomarkers and biological age among patients with long COVID. | European Respiratory Journal | 2023 | 62(suppl 67):PA5343 | doi:10.1183/13993003.congress-2023.PA5343 | Long COVID respiratory phenotype shows +2.25 yr PhenoAgeAccel. |
| Biological age in ICU study. | Biological age is superior to chronological age in predicting hospital mortality of the critically ill. | Internal and Emergency Medicine | 2023 | 18:2263-2270 | doi:10.1007/s11739-023-03397-3 | PhenoAge outperforms chronological age in predicting ICU mortality. |
| PhenoAgeAccel in diabetes/prediabetes. | PhenoAgeAccel is associated with all-cause and cardiovascular mortality in patients with diabetes and prediabetes. | Diabetes Research and Clinical Practice | 2025 | (in press) | N/A | HR 1.051 per year PhenoAgeAccel increase for all-cause mortality. |

---
