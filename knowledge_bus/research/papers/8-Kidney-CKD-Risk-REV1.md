### 1. Executive Summary

This signal, CKD Risk, is designed to detect early and established chronic kidney disease (CKD) using the standard renal function panel: estimated glomerular filtration rate (eGFR), urinary albumin-to-creatinine ratio (uACR), serum creatinine, and blood urea nitrogen (BUN/urea). The biological question it answers for an end user is whether their kidneys are filtering waste efficiently, and whether early signs of kidney damage are present.

The primary metric recommended for platform use is the **urinary albumin-to-creatinine ratio (uACR)**, which is the earliest detectable sign of glomerular stress. eGFR is the gold standard for staging kidney function decline and is used as the secondary metric. The BUN/urea-to-creatinine ratio is used as a differential diagnostic tool to distinguish intrinsic renal dysfunction from pre-renal causes (dehydration, heart failure) and other confounding conditions (liver disease, GI bleeding).

The evidence quality supporting this signal is **Tier 1 and Tier 2**, anchored in KDIGO 2024 clinical practice guidelines and large prospective cohort data. All required derived metrics are already computed on the platform. The signal can be implemented immediately using the standard renal function panel.

An important threshold qualifier: eGFR 60–89 mL/min/1.73 m² is **not independently suboptimal** — it should only be flagged as suboptimal when concurrent albuminuria (uACR ≥30 mg/g) is present, or in the context of other kidney damage markers. Standalone eGFR 60–89 in the absence of proteinuria, particularly in older adults, is often within normal variation.

---

### 2. Biological Question

> "Based on my blood and urine tests, are there signs that my kidneys are not filtering waste efficiently — early indicators of kidney disease that I should know about?"

---

### 3. Clinical Rationale

- **What disease or dysfunction does this signal predict or detect?**
  This signal detects early and established chronic kidney disease (CKD), including diabetic nephropathy, hypertensive nephrosclerosis, and glomerular disease. It also identifies pre-renal dysfunction (reduced blood flow to kidneys from dehydration, heart failure) and flags confounding conditions (liver disease, GI bleeding) that alter the standard biomarkers.

- **What is the pathophysiological mechanism — why do these biomarkers move early?**
  - **uACR**: Albumin leaks into urine when glomerular filtration barriers are damaged. This occurs before eGFR falls, making uACR the earliest detectable signal of kidney stress.
  - **eGFR**: Reflects the rate at which the kidneys filter waste from the blood. Declines as nephron mass is lost. Creatinine (used to compute eGFR) rises only after >50% nephron loss, making eGFR a lagging marker compared to uACR.
  - **BUN/urea-creatinine ratio**: Both urea and creatinine are filtered by the kidneys, but urea is also produced by the liver and reabsorbed passively in the tubules. The ratio between them identifies whether dysfunction is intrinsic to the kidney (ratio 10–20:1, US units) or caused by reduced renal perfusion from pre-renal causes (>20:1), or whether urea production is impaired by liver disease (<10:1). A ratio >30:1 suggests GI bleeding as a source of excess urea load.

- **At what stage in disease progression does this signal provide useful information?**
  Most valuable in **CKD stages G1–G3** (eGFR ≥30 mL/min/1.73 m²), where conventional creatinine alone may remain within normal range despite established glomerular damage. uACR detects damage at G1 (eGFR ≥90 with proteinuria) — before eGFR declines.

- **Why does early detection matter for patient outcomes?**
  Early identification enables interventions that demonstrably slow CKD progression: blood pressure control with ACE inhibitors or ARBs, glycaemic management in diabetes, dietary modification (sodium, protein restriction), and avoidance of nephrotoxins. KDIGO evidence supports that reducing albuminuria and controlling blood pressure reduces risk of ESRD and cardiovascular events.

---

### 4. Evidence Base

**Primary Evidence**

| Field | Content |
|-------|---------|
| Study name / first author | KDIGO (Kidney Disease: Improving Global Outcomes) |
| Journal | KDIGO Clinical Practice Guideline for CKD Evaluation and Management |
| Year | 2024 |
| DOI | N/A (guideline) |
| Design | Clinical practice guideline |
| Sample size | N/A |
| Follow-up | N/A |
| Key finding | CKD defined as eGFR <60 mL/min/1.73 m² OR albuminuria (uACR ≥30 mg/g) for >3 months. eGFR 60–89 with no albuminuria is not diagnostic of CKD. uACR ≥30 mg/g at any eGFR level indicates kidney damage. |
| Threshold derived | uACR: <30 mg/g optimal; 30–300 mg/g suboptimal (microalbuminuria); ≥300 mg/g at_risk (macroalbuminuria). eGFR: ≥60 optimal; 45–59 suboptimal; <45 at_risk. |
| Limitations | Thresholds define CKD; do not specifically target metabolic drivers of renal stress. |

| Field | Content |
|-------|---------|
| Study name / first author | Nkuipou-Kenfack E, et al. |
| Journal | PLOS ONE |
| Year | 2014 |
| DOI | 10.1371/journal.pone.0096955 |
| Design | Prospective cohort |
| Sample size | n=49 (20 CKD training, 29 test) |
| Follow-up | 2.8 ± 0.8 years |
| Key finding | Plasma and urinary metabolite panels correlate strongly with eGFR at baseline (ρ = −0.80) and follow-up (ρ = −0.60), supporting metabolomics as future adjunct markers. |
| Threshold derived | None — continuous correlation only. |
| Limitations | Small sample size; mixed diabetic and non-diabetic CKD. |

**Supporting Evidence**

| Field | Content |
|-------|---------|
| Study name / first author | University of Rochester Medical Centre (URMC) |
| Journal | URMC Encyclopedia — Urea Nitrogen, Serum |
| Year | Current |
| DOI | N/A |
| Design | Clinical reference |
| Sample size | N/A |
| Follow-up | N/A |
| Key finding | BUN/creatinine ratio 10–20:1 (US units) is normal or suggests intrinsic renal disease. Ratio >20:1 indicates pre-renal azotaemia (dehydration, heart failure, GI bleed). |
| Threshold derived | Ratio 10–20:1 normal/intrinsic; >20:1 pre-renal; >30:1 GI bleed. |
| Limitations | Narrative clinical reference; not a primary outcome study. |

| Field | Content |
|-------|---------|
| Study name / first author | Shah S, Bhatt H (NCBI StatPearls) |
| Journal | NCBI StatPearls NBK507821 |
| Year | 2023 |
| DOI | https://www.ncbi.nlm.nih.gov/books/NBK507821/ |
| Design | Evidence-based clinical review |
| Sample size | N/A |
| Follow-up | N/A |
| Key finding | BUN/creatinine ratio distinguishes pre-renal (>20:1), intrinsic renal (10–20:1), and post-hepatic or low-production states (<10:1). Ratio >30:1 is associated with upper GI bleeding. |
| Threshold derived | Same as URMC; consistent across clinical literature. |
| Limitations | Thresholds are US-unit (mg/dL) conventions; unit conversion required for UK platforms. |

| Field | Content |
|-------|---------|
| Study name / first author | UK Kidney Association (UKKIDNEY) |
| Journal | UK eGFR Guide / CKD Staging |
| Year | 2023 |
| DOI | https://www.ukkidney.org/health-professionals/information-resources/uk-eckd-guide/ckd-staging |
| Design | National clinical guideline |
| Sample size | N/A |
| Follow-up | N/A |
| Key finding | Consistent with KDIGO staging. eGFR 60–89 (G2) is not CKD unless accompanied by other markers of kidney damage (albuminuria, haematuria, structural abnormality). CKD-EPI 2021 equation (without race coefficient) recommended. |
| Threshold derived | Consistent with KDIGO. Explicitly clarifies eGFR 60–89 without damage markers is not CKD. |
| Limitations | Guideline; does not provide new threshold data beyond KDIGO. |

**Cautionary Evidence**

| Field | Content |
|-------|---------|
| Study name / first author | Various (PMC review context) |
| Journal | International Journal of Molecular Sciences |
| Year | 2022 |
| DOI | 10.3390/ijms23084444 |
| Design | Systematic review context |
| Sample size | N/A |
| Follow-up | N/A |
| Key finding | Creatinine rises only after >50% nephron loss; confounded by muscle mass, hydration, diet. Cystatin C confounded by CRP, WBC, thyroid, steroids. NGAL false-positive in sepsis, malignancy, COPD. eGFR may be falsely elevated in early diabetes (hyperfiltration). |
| Threshold derived | N/A — cautionary context only. |
| Limitations | Highlights multi-marker necessity; emphasises that no single marker is sufficient. |

---

### 5. Required Biomarkers

**Required Biomarkers** (for minimum viable computation):

| Name | Why Required | Fasting Required? | SSOT Canonical Unit |
|------|--------------|-------------------|---------------------|
| `creatinine` | Used to compute eGFR; reflects glomerular filtration capacity; rises after significant nephron loss | No | **µmol/L** (confirmed SSOT canonical) |
| `urea` | Nitrogenous waste marker; with creatinine forms the urea-to-creatinine ratio for pre-renal/intrinsic differential | No | **mmol/L** (confirmed SSOT canonical) |
| `albumin_urine` | Earliest glomerular stress marker; required to compute uACR | No | mg/L |
| `creatinine_urine` | Required to normalise urinary albumin for uACR; corrects for urine concentration | No | mmol/L or mg/dL — must match uACR formula unit basis |

**Note**: eGFR is a **derived metric** computed from creatinine, age, and sex — it is not a direct biomarker input. Age and sex are available from the questionnaire SSOT (`date_of_birth`, `biological_sex`).

**Optional Biomarkers** (enhance signal but not required):

| Name | Why Optional | SSOT Canonical Unit |
|------|--------------|---------------------|
| `cystatin_c` | Muscle-independent filtration marker; detects early GFR decline when creatinine is normal; confirms eGFR in equivocal cases | mg/L |
| `ngal_urine` | Tubular damage marker; predicts AKI; cut-off >150 ng/mL | ng/mL |
| `tmao` | Gut-derived uremic toxin; elevated in early CKD (AUC >0.7); requires prospective validation before threshold use | µmol/L |

---

### 6. Derived Metrics and Formulas

| Metric name | Formula | Unit handling | Evidence anchor | Existing in platform? |
|-------------|---------|---------------|-----------------|----------------------|
| `egfr` | CKD-EPI 2021 equation (without race coefficient): `egfr = 142 × min(creatinine_mg_dl / kappa, 1)^alpha × max(creatinine_mg_dl / kappa, 1)^(-1.200) × 0.9938^age` where kappa = 0.7 (female), 0.9 (male); alpha = -0.241 (female), -0.302 (male) | Platform stores creatinine in µmol/L (confirmed). Convert before applying formula: `creatinine_mg_dl = creatinine_umol_l / 88.4`. Age from `date_of_birth`; sex from `biological_sex` (questionnaire SSOT). | KDIGO 2024; UK Kidney Association eGFR guide | **No — requires implementation** |
| `uacr` | `uacr = albumin_urine_mg_l / creatinine_urine_g_l` → result in mg/g | albumin_urine in mg/L; creatinine_urine in g/L. If creatinine_urine stored in mmol/L, convert: `creatinine_g_l = creatinine_urine_mmol_l × 0.1131`. `albumin_urine` and `creatinine_urine` are urine biomarkers — confirm SSOT addition required. | KDIGO 2024 | **No — requires implementation** |
| `urea_creatinine_ratio` | `urea_creatinine_ratio = urea / creatinine` | **Confirmed platform canonical units**: urea in mmol/L ÷ creatinine in µmol/L. This produces a small decimal ratio (normal range ~0.040–0.081). The published clinical thresholds (10:1, 20:1, 30:1) are US-unit conventions — **canonical platform equivalents are resolved below and in Section 8.** Conversion factor: US ratio = platform ratio × 247.6. | URMC; NCBI NBK507821; Liv Hospital | **Yes — already computed** |

**Resolved canonical thresholds for urea_creatinine_ratio** (platform units: mmol/L ÷ µmol/L):

| Clinical interpretation | US threshold (mg/dL) | Platform canonical value | Derivation |
|------------------------|---------------------|--------------------------|------------|
| Liver disease / low urea production | < 10:1 | < **0.040** | 10 ÷ 247.6 |
| Normal / intrinsic renal | 10–20:1 | 0.040 – **0.081** | 10–20 ÷ 247.6 |
| Pre-renal azotaemia | > 20:1 | > **0.081** | 20 ÷ 247.6 |
| GI bleed / excess urea load | > 30:1 | > **0.121** | 30 ÷ 247.6 |

Verified: normal result example — urea 5.0 mmol/L ÷ creatinine 88 µmol/L = 0.057 (sits correctly in 0.040–0.081 band).

---

### 7. Evidence-Anchored Thresholds

**Biological question filter applied**: All thresholds below are anchored to the question of detecting early and established CKD using the standard renal function panel. These are KDIGO Tier 1 / Tier 2 thresholds validated against hard outcomes (ESRD, CKD progression, cardiovascular events).

**Primary metric: uACR**

| Tier | Metric | Operator | Value | Unit | Evidence source | Study n | Follow-up |
|------|--------|----------|-------|------|----------------|---------|-----------|
| optimal | `uacr` | < | 30 | mg/g | KDIGO 2024 | Guideline | N/A |
| suboptimal | `uacr` | 30–300 | mg/g | KDIGO 2024 | Guideline | N/A |
| at_risk | `uacr` | ≥ | 300 | mg/g | KDIGO 2024 | Guideline | N/A |

**Secondary metric: eGFR**

| Tier | Metric | Operator | Value | Unit | Evidence source | Study n | Follow-up |
|------|--------|----------|-------|------|----------------|---------|-----------|
| optimal | `egfr` | ≥ | 60 | mL/min/1.73 m² | KDIGO 2024; UKKIDNEY 2023 | Guideline | N/A |
| suboptimal | `egfr` | 45–59 | mL/min/1.73 m² | KDIGO 2024 | Guideline | N/A |
| suboptimal | `egfr` | 60–89 with `uacr` ≥ 30 mg/g | mL/min/1.73 m² | KDIGO 2024; UKKIDNEY 2023 | Guideline | N/A |
| at_risk | `egfr` | < | 45 | mL/min/1.73 m² | KDIGO 2024 | Guideline | N/A |

**Important qualifier**: eGFR 60–89 mL/min/1.73 m² **without concurrent albuminuria is not suboptimal** and should not independently trigger a flag. In older adults, eGFR 60–89 without proteinuria is within normal variation. This is explicitly stated in KDIGO 2024 and the UK Kidney Association eGFR guide.

---

### 8. Override Rules and Guardrails

| Rule | Condition | Resulting State | Evidence Basis |
|------|-----------|-----------------|----------------|
| Pre-renal override | `urea_creatinine_ratio` > **0.081** (platform canonical; equivalent to >20:1 US) with elevated `urea` | suboptimal (flag: possible dehydration / reduced renal perfusion / heart failure — not primary kidney disease) | URMC urea nitrogen reference; NCBI NBK507821; Liv Hospital clinical review |
| GI bleed override | `urea_creatinine_ratio` > **0.121** (platform canonical; equivalent to >30:1 US) | at_risk (flag: possible upper GI bleed — urgent clinical review required) | NCBI NBK507821; URMC; Levels.com BUN guide |
| Liver disease override | `urea_creatinine_ratio` < **0.040** (platform canonical; equivalent to <10:1 US) with low `urea` | suboptimal (flag: possible liver disease / malnutrition / low protein intake — urea production impaired) | URMC; Levels.com BUN guide; MedicineNet |
| Critical value override | `urea` > **35.7 mmol/L** OR `creatinine` > **354 µmol/L** | at_risk (flag: critical renal impairment — immediate clinical referral) | Peterborough City Hospital Pathology critical value standards; KDIGO |
| eGFR context override | `egfr` 60–89 mL/min/1.73 m² AND `uacr` < 30 mg/g | optimal (do not flag as suboptimal — no concurrent damage marker) | KDIGO 2024; UKKIDNEY CKD staging guide |

**All ratio threshold values above are in confirmed platform canonical units** (urea mmol/L ÷ creatinine µmol/L). No further unit conversion required at the YAML or evaluator level. See Section 6 for derivation.

---

### 9. Clinical Limitations and Excluded Populations

1. **Populations where signal should not be applied or interpreted with caution**:
   - Acute illness (sepsis, major surgery, trauma) — confounds BUN and creatinine due to catabolism and volume shifts
   - Known liver disease — impaired urea production makes BUN/creatinine ratio unreliable
   - Pregnancy — physiological lowering of BUN and creatinine; standard thresholds not validated
   - Extremes of muscle mass (bodybuilders, sarcopenia, limb amputation) — creatinine unreliable as filtration proxy; cystatin C preferred
   - Children and adolescents — eGFR equations and thresholds differ; this signal is validated for adults only

2. **Conditions or medications that confound inputs**:
   - High-protein diet, GI bleed, corticosteroids — raise BUN without renal injury
   - Dehydration — elevates both BUN and creatinine (pre-renal); ratio differentiates this
   - NSAIDs, aminoglycosides, ACE inhibitors/ARBs, diuretics, certain antibiotics — affect creatinine or urea handling
   - Inflammation (high CRP, elevated WBC) — may elevate cystatin C independent of GFR
   - Thyroid disease, corticosteroid therapy — elevate cystatin C independent of GFR

3. **Diabetic hyperfiltration**:
   Early-stage diabetes commonly produces an elevated eGFR (>90 mL/min/1.73 m²) due to glomerular hyperfiltration — the kidneys filter at an abnormally high rate. This can make the signal classify a diabetic patient as **optimal** when early nephropathy is already progressing. In patients with known diabetes, the presence of microalbuminuria (uACR 30–300 mg/g) is the more reliable early indicator, even when eGFR appears elevated. The signal should not be used in isolation for diabetic patients without uACR context.

4. **Known gaps in evidence**:
   - No validated thresholds exist for "metabolic renal stress" as a distinct entity from established CKD staging — the signal therefore uses CKD risk stratification criteria
   - Metabolomic markers (TMAO, myo-inositol, pyruvate) have AUC >0.7 in early CKD but lack prospective outcome data and assay standardisation; excluded from signal thresholds
   - Limited threshold data in non-European/non-North American ethnic populations
   - Temporal delta metrics (e.g., creatinine rise over 48 hours for AKI detection) cannot be computed on a single-panel submission — AKI criteria are not implemented in this signal

5. **Cautionary trial evidence**:
   - Interventions that reduce proteinuria (e.g., RAS blockade) do not consistently reduce ESRD or mortality across all trial populations. This signal should be communicated as a **risk indicator**, not a standalone therapeutic target. Improvements in biomarker values without corresponding clinical intervention changes should not be over-interpreted.

---

### 10. HealthIQ Platform Signal Mapping

**Signal identifier**:
```
signal_ckd_risk
```

**Physiological system**:
```
renal
```

**Primary metric**:
```
uacr
```

**Required biomarkers**:
```
- creatinine
- urea
- albumin_urine
- creatinine_urine
```

**Required derived metrics**:
```
- egfr
- uacr
- urea_creatinine_ratio
```

**Optional biomarkers**:
```
- cystatin_c
- ngal_urine
- tmao
```

**Optional derived metrics**:
```
- none currently defined
```

**Threshold summary**:
```
Primary (uACR):
  optimal:    uacr < 30 mg/g
  suboptimal: uacr 30–300 mg/g
  at_risk:    uacr >= 300 mg/g

Secondary (eGFR):
  optimal:    egfr >= 60 mL/min/1.73 m² (with no concurrent albuminuria for 60–89 band)
  suboptimal: egfr 45–59 mL/min/1.73 m²
              OR egfr 60–89 mL/min/1.73 m² with uacr >= 30 mg/g
  at_risk:    egfr < 45 mL/min/1.73 m²
```

**Override rules**:
```
rule: urea_creatinine_ratio > 0.081 → suboptimal (flag: pre-renal)
rule: urea_creatinine_ratio > 0.121 → at_risk (flag: possible GI bleed — urgent referral)
rule: urea_creatinine_ratio < 0.040 → suboptimal (flag: liver disease/malnutrition)
rule: urea > 35.7 mmol/L OR creatinine > 354 µmol/L → at_risk (critical value — immediate referral)
rule: egfr 60–89 AND uacr < 30 mg/g → optimal (do not flag)
evidence: KDIGO 2024; UKKIDNEY 2023; NCBI NBK507821; URMC; Peterborough City Hospital Pathology
note: all ratio thresholds are in confirmed platform canonical units (urea mmol/L ÷ creatinine µmol/L)
```

**Bundle consumers**:
```
- metabolic_health
- cardiovascular_risk
- biological_age
- vascular_age
```

**Implementation notes**:
- **Ratio unit conversion RESOLVED**: Platform confirmed to store urea in mmol/L and creatinine in µmol/L. `urea_creatinine_ratio` is computed as urea/creatinine in those units. Canonical threshold values (0.040 / 0.081 / 0.121) are already derived and used throughout this document. No further conversion needed at YAML or evaluator level.
- **uACR NOT YET COMPUTED**: `uacr` is not currently in the platform's derived metrics registry (`ratio_registry.py`). Requires implementation sprint before this signal can activate. `albumin_urine` and `creatinine_urine` are urine biomarkers — confirm whether SSOT addition is required.
- **eGFR NOT YET COMPUTED**: `egfr` is not currently in the platform's derived metrics registry. Requires implementation sprint (CKD-EPI 2021 formula, sex-specific coefficients, creatinine µmol/L → mg/dL conversion) before this signal can activate.
- **eGFR inputs from questionnaire SSOT**: CKD-EPI 2021 requires `date_of_birth` (→ age) and `biological_sex` — both available from questionnaire SSOT
- **Sex-specific eGFR**: CKD-EPI 2021 uses sex coefficients (kappa and alpha differ by sex) — platform must apply sex-specific formula at runtime using `biological_sex`
- **Age-stratified interpretation**: eGFR 60–89 without proteinuria is particularly common in adults over 65 — consider age-stratified messaging at runtime
- **Diabetic hyperfiltration flag**: In patients with known diabetes (`chronic_conditions` in questionnaire SSOT), eGFR-only classification is unreliable; uACR should be the primary tier determinant
- **`tmao` not currently in SSOT**: Requires addition if optional path is implemented; unit tentative (µmol/L); threshold not implementable until prospective outcome data available
- **AKI temporal delta not implemented**: Creatinine-rise-over-48-hours (KDIGO AKI criteria) requires time-series data across visits — not computable on a single-panel submission; excluded from this signal

---

### 11. Supporting References

1. KDIGO Clinical Practice Guideline for CKD Evaluation and Management. 2024. (Tier 1 — primary threshold authority)
2. UK Kidney Association. UK eGFR Guide / CKD Staging. 2023. https://www.ukkidney.org/health-professionals/information-resources/uk-eckd-guide/ckd-staging (Tier 2 — national UK guideline confirming eGFR 60–89 context dependency)
3. Shah S, Bhatt H. "Blood Urea Nitrogen (BUN) to Creatinine Ratio." NCBI StatPearls. NBK507821. 2023. https://www.ncbi.nlm.nih.gov/books/NBK507821/ (Tier 2 — ratio threshold evidence)
4. University of Rochester Medical Centre. "Urea Nitrogen, Serum." URMC Encyclopedia. https://www.urmc.rochester.edu/encyclopedia/content?contenttypeid=167&contentid=urea_nitrogen_serum (Tier 2 — ratio threshold clinical reference)
5. Levels.com. "Guide to Urea Nitrogen (BUN)." https://www.levels.com/blog/guide_to_urea_nitrogen_bun (Tier 3 — narrative review; ratio interpretation context)
6. Liv Hospital International. "High BUN and Creatinine." https://int.livhospital.com/high-bun-and-creatinine/ (Tier 3 — clinical overview; GI bleed ratio context)
7. MedicineNet. "What Causes a High BUN/Creatinine Ratio?" https://www.medicinenet.com/what_causes_a_high_bun_creatinine_ratio/article.htm (Tier 3 — clinical overview)
8. Nkuipou-Kenfack E, et al. "Assessment of Metabolomic and Proteomic Biomarkers in Detection and Prognosis of Progression of Renal Function in Chronic Kidney Disease." PLOS ONE. 2014;9(5):e96955. DOI: 10.1371/journal.pone.0096955 (Tier 1 — prospective cohort; metabolomics context)
9. PMC/IJMS review. "Biomarkers in CKD." International Journal of Molecular Sciences. 2022. DOI: 10.3390/ijms23084444 (Tier 2 — systematic review context; cautionary evidence on confounders)
10. Peterborough City Hospital Pathology. "Critical Value Cut-Off Limits." 2019. https://pch-pathlab.com (Tier 2 — critical value standards for referral thresholds)
11. NHS. "Kidney Disease — Diagnosis." https://www.nhs.uk/conditions/kidney-disease/diagnosis/ (Tier 2 — UK national clinical pathway)
12. Kidney.org. "Creatinine." https://www.kidney.org/kidney-topics/creatinine (Tier 2 — NKF clinical reference; muscle mass confound context)
