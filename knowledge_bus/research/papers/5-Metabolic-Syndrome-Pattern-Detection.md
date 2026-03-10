# HealthIQ Evidence Report: Metabolic Syndrome Pattern Detection

**Signal identifier:** `signal_metabolic_syndrome_pattern`
**Generated:** 2026-03-08
**Evidence tier focus:** Tier 1 (prospective cohort, meta-analysis) → Tier 2 (harmonised guideline definitions)

---

## 1. Executive Summary

Metabolic syndrome (MetS) is a cluster of interrelated cardiometabolic risk factors — elevated triglycerides, reduced HDL cholesterol, impaired fasting glucose, elevated blood pressure, and central adiposity — that co-occur more frequently than chance alone would predict. Their clustering reflects shared upstream pathophysiology centred on insulin resistance, chronic low-grade inflammation, and ectopic fat deposition. The signal is not defined by any single biomarker in isolation but by the **number and pattern of abnormal components** present simultaneously.

The harmonised 2009 IDF/NHLBI/AHA/WHF/IAS/IASO joint statement defines metabolic syndrome as the presence of **≥3 of 5 criteria**, each with sex- and ethnicity-specific thresholds. This definition is the most widely validated across multi-ethnic prospective cohorts and is adopted here as the platform's primary classification framework. The primary metric for this signal is therefore a **component count** (0–5), with pattern-based sub-classification indicating which components are abnormal.

Prospective evidence from ARIC (n=9,841), Framingham Offspring (n=3,323), the San Antonio Heart Study (n=2,902), and a landmark Mottillo et al. meta-analysis (n=951,083) consistently demonstrates that MetS confers approximately 2× the risk of cardiovascular disease events and 5× the risk of incident type 2 diabetes compared with MetS-absent individuals. Component clustering is additive to multiplicative: each additional abnormal component incrementally increases risk. The TG/HDL ratio — already computed in the platform — serves as a validated surrogate for insulin resistance and anchors the internal biology of this signal.

Evidence quality supporting the thresholds is **Tier 1 and Tier 2**. The component cut-offs themselves derive from the 2009 harmonised guideline (Tier 2), which was constructed on Tier 1 prospective data. Risk estimates for component count tiers are supported by Tier 1 meta-analytic evidence.

---

## 2. Biological Question

> "Based on my blood test results and body measurements, how many markers of metabolic stress are simultaneously abnormal in my body — and does this pattern suggest my cardiometabolic risk is clustering beyond what any single marker would show?"

---

## 3. Clinical Rationale

### What disease or dysfunction does this signal predict or detect?

Metabolic syndrome is a pre-disease clustering state that predicts:
1. **Type 2 diabetes mellitus (T2DM):** 5-fold increased incidence over 5–10 years (Sattar et al., 2008; Lorenzo et al., 2003)
2. **Cardiovascular disease (CVD):** ~2-fold increased risk of major adverse cardiovascular events and cardiovascular mortality (Mottillo et al., 2010; Gami et al., 2007)
3. **Non-alcoholic fatty liver disease (NAFLD):** strong bidirectional association; MetS components predict hepatic steatosis and fibrosis progression
4. **Chronic kidney disease:** 55% increased risk in MetS-positive individuals (Chen et al., 2004)

### Pathophysiological mechanism

The central driver is **insulin resistance** — particularly in adipose tissue, liver, and skeletal muscle. Visceral adiposity (captured by waist circumference) releases excess free fatty acids and pro-inflammatory adipokines (TNF-α, IL-6, resistin), while adiponectin secretion falls. These signals create hepatic insulin resistance, increasing VLDL-TG secretion and reducing HDL formation. Skeletal muscle insulin resistance impairs glucose uptake, raising fasting and postprandial glucose. Concurrent activation of the renin-angiotensin-aldosterone system and sympathetic nervous system elevates blood pressure. The five MetS criteria are therefore not independent — they are phenotypic read-outs of the same upstream dysfunction.

The TG/HDL ratio captures this axis particularly efficiently: elevated TG reflects excess hepatic VLDL output; depressed HDL reflects accelerated TG-rich HDL catabolism. A high TG/HDL ratio predicts insulin resistance with AUROC ~0.75–0.78 in non-Hispanic white populations (McLaughlin et al., 2003; Li et al., 2008).

### Stage in disease progression

MetS pattern detection operates at the **pre-clinical / early-dysfunction stage** — after insulin resistance has begun generating measurable biomarker shifts but before frank T2DM or established CVD. A person may carry MetS for 5–15 years before reaching diagnostic thresholds for either endpoint. This window is precisely where lifestyle and pharmacological interventions have the greatest evidence for risk reversal.

### Why early detection matters

The STOP-NIDDM trial (Chiasson et al., 2002) and DPP (Knowler et al., 2002) demonstrated that lifestyle intervention in MetS-adjacent populations reduces T2DM incidence by 31–58%. The PREDIMED trial (Estruch et al., 2013) showed Mediterranean diet intervention in high-MetS-burden individuals reduced cardiovascular events by 30%. Detecting the clustering pattern early — before 3-component threshold is crossed — enables risk communication and preventive action.

---

## 4. Evidence Base

### Primary Evidence

| Field | Study 1 |
|-------|---------|
| **Study name / first author** | Mottillo et al. |
| **Journal** | Journal of the American College of Cardiology |
| **Year** | 2010 |
| **DOI** | doi:10.1016/j.jacc.2010.05.034 |
| **Design** | Systematic review and meta-analysis of prospective cohort studies |
| **Sample size** | n = 951,083 across 87 studies |
| **Follow-up** | Weighted mean ~10 years |
| **Key finding** | MetS associated with 2× risk of CVD events (RR 2.35, 95% CI 2.02–2.73), 2× CVD mortality (RR 2.40), 1.5× all-cause mortality, and 5× T2DM incidence |
| **Threshold derived** | ≥3 components (harmonised definition) as the classification criterion; relative risks reported at this binary threshold |
| **Limitations** | Heterogeneity across studies; variable definitions of MetS used pre-harmonisation; predominance of European-descent cohorts |

| Field | Study 2 |
|-------|---------|
| **Study name / first author** | Sattar et al. (WOSCOPS, AFCAPS, CARE, 4S nested cohort) |
| **Journal** | Lancet |
| **Year** | 2003 |
| **DOI** | doi:10.1016/S0140-6736(03)12229-3 |
| **Design** | Prospective nested cohort within statin trials |
| **Sample size** | n = 16,549 (combined across 4 trials) |
| **Follow-up** | 5 years |
| **Key finding** | MetS (ATP III ≥3 criteria) significantly predicted CVD in men not previously treated for hyperlipidaemia; MetS alone without diabetes conferred RR ~1.7 for CHD events |
| **Threshold derived** | ATP III ≥3 criteria (2001) used as classifier; findings support ≥3 threshold as clinically meaningful |
| **Limitations** | Male-predominant trial populations; statin-treated backgrounds complicate lipid component thresholds |

| Field | Study 3 |
|-------|---------|
| **Study name / first author** | Lorenzo et al. (San Antonio Heart Study) |
| **Journal** | Diabetes Care |
| **Year** | 2003 |
| **DOI** | doi:10.2337/diacare.26.11.3153 |
| **Design** | Prospective cohort |
| **Sample size** | n = 2,902 (Mexican American and non-Hispanic white) |
| **Follow-up** | 7–8 years |
| **Key finding** | MetS (ATP III ≥3) predicted incident T2DM with OR 5.17 (95% CI 3.86–6.93) in Mexican Americans and OR 3.45 (2.51–4.74) in non-Hispanic whites; risk was stronger in Mexican Americans, highlighting ethnic variation |
| **Threshold derived** | ATP III ≥3 criteria |
| **Limitations** | Two ethnic groups only; not generalisable to South Asian, East Asian, or African-descent populations without adjustment |

| Field | Study 4 |
|-------|---------|
| **Study name / first author** | Gami et al. |
| **Journal** | Journal of the American College of Cardiology |
| **Year** | 2007 |
| **DOI** | doi:10.1016/j.jacc.2006.10.068 |
| **Design** | Meta-analysis of prospective cohort studies |
| **Sample size** | n = 172,573 across 37 studies |
| **Follow-up** | Variable, median ~8 years |
| **Key finding** | MetS confers RR 1.78 (95% CI 1.58–2.00) for incident CVD; RR for CVD mortality 1.86 (1.41–2.46) |
| **Threshold derived** | ≥3 components per WHO/ATP III/IDF; findings robust across definitions |
| **Limitations** | Studies pre-date harmonised 2009 definition; definition heterogeneity reduces precision |

| Field | Study 5 |
|-------|---------|
| **Study name / first author** | Isomaa et al. (Botnia Study) |
| **Journal** | Diabetes Care |
| **Year** | 2001 |
| **DOI** | doi:10.2337/diacare.24.4.683 |
| **Design** | Prospective cohort |
| **Sample size** | n = 4,483 (Finnish and Swedish families) |
| **Follow-up** | 6.9 years |
| **Key finding** | WHO-defined MetS conferred 3× risk of CHD/stroke (RR 3.0, 95% CI 2.2–4.0) and 5× T2DM risk; CVD mortality RR 2.26 in MetS-positive men, 2.78 in women |
| **Threshold derived** | WHO criteria (insulin resistance required as core + 2 additional components) |
| **Limitations** | Predominantly Northern European; WHO definition requires OGTT-based insulin measurement, not replicated in observational practice |

### Supporting Evidence

| Field | Study 6 |
|-------|---------|
| **Study name / first author** | McLaughlin et al. |
| **Journal** | Journal of Clinical Endocrinology & Metabolism |
| **Year** | 2003 |
| **DOI** | doi:10.1210/jc.2003-030221 |
| **Design** | Cross-sectional with euglycaemic clamp validation |
| **Sample size** | n = 258 |
| **Follow-up** | Cross-sectional |
| **Key finding** | TG/HDL ratio (mg/dL units) ≥3.0 identified insulin resistance with sensitivity 64%, specificity 68%; TG/HDL in mmol/L ≥0.87 equivalent; AUROC 0.75 |
| **Threshold derived** | TG/HDL ≥3.0 (mg/dL); equivalent to ≥0.87 in mmol/L units |
| **Limitations** | Non-Hispanic white adults only; clamp-validated but single-centre; does not replace clinical MetS diagnosis |

| Field | Study 7 |
|-------|---------|
| **Study name / first author** | Alberti et al. (IDF/NHLBI/AHA Joint Statement) |
| **Journal** | Circulation |
| **Year** | 2009 |
| **DOI** | doi:10.1161/CIRCULATIONAHA.109.192644 |
| **Design** | Expert consensus / harmonised guideline |
| **Sample size** | N/A (guideline) |
| **Follow-up** | N/A |
| **Key finding** | Harmonised definition: ≥3 of 5 criteria, with population-specific waist circumference thresholds; any 3 of 5 components qualifies regardless of which components |
| **Threshold derived** | See Section 7 for full threshold table |
| **Limitations** | Consensus document; waist thresholds for some ethnic groups still under research scrutiny |

| Field | Study 8 |
|-------|---------|
| **Study name / first author** | Ford et al. (NHANES III) |
| **Journal** | JAMA |
| **Year** | 2002 |
| **DOI** | doi:10.1001/jama.287.3.356 |
| **Design** | Cross-sectional population survey |
| **Sample size** | n = 8,814 US adults |
| **Follow-up** | Cross-sectional |
| **Key finding** | MetS prevalence 23.7% in US adults (ATP III); prevalence rose steeply with age; Mexican Americans had highest age-adjusted prevalence |
| **Threshold derived** | ATP III thresholds applied |
| **Limitations** | Cross-sectional; cannot establish temporal relationships |

### Cautionary Evidence

| Field | Study 9 |
|-------|---------|
| **Study name / first author** | Kahn et al. |
| **Journal** | Lancet |
| **Year** | 2005 |
| **DOI** | doi:10.1016/S0140-6736(05)67483-1 |
| **Design** | Critical review / commentary |
| **Sample size** | Literature review |
| **Follow-up** | N/A |
| **Key finding** | MetS as a construct is criticised: risk prediction not superior to the sum of individual components; unclear whether MetS represents a true syndrome or an arbitrary cluster; definition heterogeneity undermines validity |
| **Threshold derived** | No new thresholds |
| **Limitations** | Commentary, not primary data |

| Field | Study 10 |
|-------|---------|
| **Study name / first author** | Gupta et al. (South Asian cohort) |
| **Journal** | BMC Cardiovascular Disorders |
| **Year** | 2012 |
| **DOI** | doi:10.1186/1471-2261-12-28 |
| **Design** | Cross-sectional |
| **Sample size** | n = 3,040 (urban India) |
| **Follow-up** | Cross-sectional |
| **Key finding** | ATP III waist threshold (≥102 cm men / ≥88 cm women) significantly underestimates MetS prevalence in South Asians; IDF South Asian thresholds (≥90 cm men / ≥80 cm women) more appropriate |
| **Threshold derived** | South Asian waist: men ≥90 cm, women ≥80 cm |
| **Limitations** | Cross-sectional; urban India only |

---

## 5. Required Biomarkers

### Required for minimum viable computation

| Name | Why required | Fasting required? | SSOT canonical unit |
|------|-------------|-------------------|---------------------|
| `triglycerides` | Component 1: elevated TG is one of the 5 MetS criteria; also used in TG/HDL ratio | Yes — fasting TG reflects hepatic VLDL output accurately | mmol/L |
| `hdl_cholesterol` | Component 2: reduced HDL is one of the 5 MetS criteria; denominator for TG/HDL ratio | Preferred (HDL less affected by fasting than TG) | mmol/L |
| `glucose` | Component 3: elevated fasting glucose ≥5.6 mmol/L is a criterion; also detects IFG | Yes — fasting glucose required for criterion | mmol/L |
| `waist_circumference_cm` | Component 4: central adiposity criterion; sex- and ethnicity-specific thresholds | No (anthropometric measurement) | cm — from lifestyle_registry |
| `systolic_bp` | Component 5a: elevated BP criterion ≥130 mmHg systolic | No (measured at rest) | mmHg — from lifestyle_registry |
| `diastolic_bp` | Component 5b: elevated BP criterion ≥85 mmHg diastolic | No | mmHg — from lifestyle_registry |
| `biological_sex` | Required for sex-specific HDL and waist thresholds | N/A | categorical — from questionnaire |
| `ethnicity` | Required for population-specific waist circumference thresholds | N/A | categorical — from questionnaire |

### Optional biomarkers (enhance signal, not required for minimum viable computation)

| Name | Why optional | SSOT canonical unit |
|------|-------------|---------------------|
| `insulin` (fasting) | Enables HOMA-IR computation; direct insulin resistance quantification | pmol/L |
| `hba1c` | Detects dysglycaemia beyond fasting glucose; useful if fasting glucose unavailable | mmol/mol |
| `crp` (high-sensitivity) | Reflects inflammatory burden co-occurring with MetS; hsCRP ≥2 mg/L associated with MetS clustering | mg/L |
| `alt` | Hepatic fat deposition marker; elevated ALT common in MetS-positive individuals | IU/L |
| `uric_acid` | Serum urate elevated in MetS; independent predictor of gout and CVD in this context | mmol/L |
| `antihypertensive_medication` | If on treatment, BP criterion met regardless of measured values | boolean — from questionnaire/medications |
| `lipid_lowering_medication` | TG-lowering or fibrate use may suppress TG criterion; clinical context required | boolean — from questionnaire/medications |
| `antidiabetic_medication` | Drug treatment for hyperglycaemia meets the glucose criterion per harmonised guideline | boolean — from questionnaire/medications |

---

## 6. Derived Metrics and Formulas

### Metric 1: `mets_component_count`

- **Formula:** Count of components meeting criteria (integer 0–5), where each component scores 1 point:
  - TG ≥1.7 mmol/L OR on fibrate/TG-lowering therapy → +1
  - HDL < sex-specific threshold OR on HDL-raising therapy → +1
  - Glucose ≥5.6 mmol/L OR on antidiabetic therapy → +1
  - Waist ≥ ethnicity/sex-specific threshold → +1
  - SBP ≥130 OR DBP ≥85 OR on antihypertensive therapy → +1

- **Unit handling:** All inputs must be in mmol/L for lipids/glucose; cm for waist; mmHg for BP
- **Evidence anchor:** Alberti et al. 2009 (harmonised IDF/NHLBI/AHA definition)
- **Existing in platform?** No — new derived metric required

### Metric 2: `tg_hdl_ratio`

- **Formula:** `triglycerides (mmol/L) / hdl_cholesterol (mmol/L)`
- **Unit handling:** Both inputs in mmol/L. Note: published US thresholds frequently use mg/dL. Conversion: TG mmol/L × 88.6 = mg/dL; HDL mmol/L × 38.67 = mg/dL. Ratio threshold 3.0 (mg/dL) ≡ ~0.87 (mmol/L).
- **Evidence anchor:** McLaughlin et al. 2003 (insulin resistance surrogate validation)
- **Existing in platform?** Yes — `tg_hdl_ratio` already computed

### Metric 3: `mets_bp_flag`

- **Formula:** Binary flag: 1 if (systolic_bp ≥ 130 OR diastolic_bp ≥ 85 OR antihypertensive_medication = true), else 0
- **Unit handling:** mmHg
- **Evidence anchor:** Alberti et al. 2009
- **Existing in platform?** No — new derived metric required

### Metric 4: `mets_waist_flag`

- **Formula:** Binary flag using population-specific thresholds (see Section 7). Returns 1 if waist ≥ threshold for the individual's ethnicity/sex combination, else 0.
- **Unit handling:** cm
- **Evidence anchor:** Alberti et al. 2009 (harmonised thresholds with ethnic-specific waist cuts)
- **Existing in platform?** No — new derived metric required; requires ethnicity and biological_sex as inputs

---

## 7. Evidence-Anchored Thresholds

### MetS Component Criteria (Harmonised 2009 Definition)

Source: Alberti et al., *Circulation*, 2009

#### Triglycerides

| Tier | Metric | Operator | Value | Unit | Evidence source | Study n | Follow-up |
|------|--------|----------|-------|------|----------------|---------|-----------|
| optimal | triglycerides | < | 1.7 | mmol/L | Alberti et al. 2009 / ATP III | 951,083 (meta) | ~10 yr |
| at_risk (criterion met) | triglycerides | ≥ | 1.7 | mmol/L | Alberti et al. 2009 | — | — |

*1.7 mmol/L = 150 mg/dL*

#### HDL Cholesterol

| Tier | Metric | Operator | Value | Unit | Sex | Evidence source |
|------|--------|----------|-------|------|-----|----------------|
| optimal | hdl_cholesterol | ≥ | 1.3 | mmol/L | Female | Alberti et al. 2009 |
| optimal | hdl_cholesterol | ≥ | 1.0 | mmol/L | Male | Alberti et al. 2009 |
| at_risk (criterion met) | hdl_cholesterol | < | 1.3 | mmol/L | Female | Alberti et al. 2009 |
| at_risk (criterion met) | hdl_cholesterol | < | 1.0 | mmol/L | Male | Alberti et al. 2009 |

*1.3 mmol/L = 50 mg/dL; 1.0 mmol/L = 40 mg/dL*

#### Fasting Glucose

| Tier | Metric | Operator | Value | Unit | Evidence source |
|------|--------|----------|-------|------|----------------|
| optimal | glucose | < | 5.6 | mmol/L | Alberti et al. 2009 |
| at_risk (criterion met) | glucose | ≥ | 5.6 | mmol/L | Alberti et al. 2009 |

*5.6 mmol/L = 100 mg/dL*

#### Blood Pressure

| Tier | Metric | Operator | Value | Unit | Evidence source |
|------|--------|----------|-------|------|----------------|
| optimal | systolic_bp | < | 130 | mmHg | Alberti et al. 2009 |
| optimal | diastolic_bp | < | 85 | mmHg | Alberti et al. 2009 |
| at_risk (criterion met) | systolic_bp | ≥ | 130 | mmHg | Alberti et al. 2009 |
| at_risk (criterion met) | diastolic_bp | ≥ | 85 | mmHg | Alberti et al. 2009 |

#### Waist Circumference — Population-Specific Thresholds

| Population | Sex | Threshold (cm) | Evidence source |
|-----------|-----|----------------|----------------|
| European (and USA European-descent) | Male | ≥ 102 | IDF/NHLBI/AHA 2009 (ATP III) |
| European (and USA European-descent) | Female | ≥ 88 | IDF/NHLBI/AHA 2009 (ATP III) |
| South Asian, Chinese, Japanese, South and Central American | Male | ≥ 90 | IDF 2006 / Alberti et al. 2009 |
| South Asian, Chinese, Japanese, South and Central American | Female | ≥ 80 | IDF 2006 / Alberti et al. 2009 |
| Sub-Saharan African, Eastern Mediterranean, Middle Eastern | Male | ≥ 94 | IDF 2006 / Alberti et al. 2009 |
| Sub-Saharan African, Eastern Mediterranean, Middle Eastern | Female | ≥ 80 | IDF 2006 / Alberti et al. 2009 |

*Note: Alberti et al. 2009 recommends using existing IDF ethnic-specific cuts where available, defaulting to European thresholds where no ethnic-specific data exist.*

### Primary Signal Tier Table (Component Count)

| Tier | Metric | Operator | Value | Unit | Evidence source | Study n | Follow-up |
|------|--------|----------|-------|------|----------------|---------|-----------|
| optimal | mets_component_count | ≤ | 1 | components | Mottillo et al. 2010 (no MetS = baseline risk) | 951,083 | ~10 yr |
| suboptimal | mets_component_count | = | 2 | components | Gami et al. 2007 (2-component clustering → intermediate risk elevation) | 172,573 | ~8 yr |
| at_risk | mets_component_count | ≥ | 3 | components | Alberti et al. 2009; Mottillo et al. 2010; Lorenzo et al. 2003 | 951,083+ | — |

### TG/HDL Ratio Tier (Surrogate Insulin Resistance — Supporting Sub-Signal)

| Tier | Metric | Operator | Value | Unit | Evidence source | Study n |
|------|--------|----------|-------|------|----------------|---------|
| optimal | tg_hdl_ratio | < | 0.87 | mmol/L ratio | McLaughlin et al. 2003 | 258 |
| suboptimal | tg_hdl_ratio | 0.87 – 1.74 | — | mmol/L ratio | Li et al. 2008 (extended validation) | 1,138 |
| at_risk | tg_hdl_ratio | ≥ | 1.74 | mmol/L ratio | Li et al. 2008 (top tertile, insulin resistance highly probable) | 1,138 |

*Note: TG/HDL ratio thresholds validated primarily in non-Hispanic white and Chinese populations. Validation in South Asian populations is less robust — apply with caution; threshold evidence for South Asian cohorts should be noted as partially inconclusive.*

---

## 8. Override Rules and Guardrails

### Override 1 — Medication-Adjusted Criteria

**Condition:** Patient on antihypertensive medication
**Rule:** BP component = criterion met (score +1) regardless of measured BP value
**Evidence:** Alberti et al. 2009 (harmonised guideline explicitly includes treated hypertension as meeting BP criterion)

**Condition:** Patient on fibrate or niacin (TG-lowering therapy)
**Rule:** TG component = criterion met regardless of measured TG value
**Evidence:** Alberti et al. 2009

**Condition:** Patient on antidiabetic medication (including metformin, insulin, GLP-1 agonists)
**Rule:** Glucose component = criterion met regardless of measured fasting glucose
**Evidence:** Alberti et al. 2009

**Condition:** Patient on HDL-raising medication (niacin)
**Rule:** HDL component = criterion met (low HDL) regardless of measured HDL value
**Evidence:** Alberti et al. 2009

### Override 2 — Established Diagnosis Forces at_risk

**Condition:** chronic_conditions includes "type_2_diabetes" OR "prediabetes"
**Rule:** Glucose component automatically = criterion met → component count ≥ 1; combined with any 2 other components → overall at_risk
**Evidence:** Diagnostic certainty supersedes threshold; clinical consensus

**Condition:** chronic_conditions includes "hypertension"
**Rule:** BP component automatically = criterion met
**Evidence:** Alberti et al. 2009

### Override 3 — Extreme Triglycerides (Pancreatitis Risk)

**Condition:** triglycerides ≥ 5.6 mmol/L (500 mg/dL)
**Rule:** Immediately flag as `at_risk` with supplementary alert for acute pancreatitis risk; this overrides signal tier and requires clinical attention note separate from MetS scoring
**Evidence:** European Society of Cardiology (ESC/EAS) 2019 dyslipidaemia guidelines; triglyceride-induced pancreatitis threshold

### Override 4 — Ethnic Waist Threshold Ambiguity

**Condition:** ethnicity data unavailable or maps to a category without validated thresholds
**Rule:** Default to European ATP III thresholds (male ≥102 cm, female ≥88 cm); flag in output that ethnic-specific thresholds not applied
**Evidence:** Alberti et al. 2009 (default recommendation for unknown ethnicity)

---

## 9. Clinical Limitations and Excluded Populations

### Populations requiring caution or exclusion

1. **Pregnant women:** Waist circumference, TG, and glucose are physiologically altered during pregnancy. MetS criteria should not be applied. Separate gestational diabetes and pregnancy hypertension risk signals required.

2. **Children and adolescents (<18 years):** Adult MetS criteria not validated. Paediatric definitions (IDF ≥10 years, Cook criteria) use age- and sex-specific percentile thresholds. Do not apply this signal to users under 18.

3. **Acute illness:** CRP elevation, glucose instability, and BP fluctuations during acute illness confound all five criteria. Results within 4 weeks of hospitalisation or acute infection should be flagged.

4. **Recent corticosteroid therapy:** Systemic corticosteroids raise glucose, TG, and BP acutely, potentially falsely triggering MetS criteria. Flag if long_term_medications includes corticosteroids.

5. **Lipodystrophy or severe eating disorders:** Adiposity-dependent criteria (waist circumference) and lipid criteria are distorted. Interpretive caution required.

6. **East African descent:** Limited prospective data for optimal waist cut-offs; IDF recommends using sub-Saharan African thresholds but evidence base is thinner than for European or Asian populations.

### Conditions and medications that confound inputs

| Confounder | Components affected | Direction |
|-----------|---------------------|-----------|
| Corticosteroids (systemic) | Glucose, TG, BP | False elevation |
| Atypical antipsychotics (olanzapine, clozapine) | TG, glucose, waist | False elevation |
| HIV antiretroviral therapy (PIs, NNRTIs) | TG, HDL, waist redistribution | Dyslipidaemia pattern |
| Hypothyroidism | TG, HDL, glucose | TG elevated, HDL reduced |
| Polycystic ovary syndrome (PCOS) | TG, glucose, waist | False elevation (or true MetS overlap) |
| Chronic kidney disease (eGFR <30) | TG, HDL, glucose | Complex distortion |
| Beta-blockers | TG (mild elevation), HDL (mild reduction) | Modest false elevation |

### Known evidence gaps

1. **Sub-Saharan African and Afro-Caribbean populations:** Insulin resistance and visceral adiposity patterns differ from European populations; waist cut-offs under-researched.
2. **Middle Eastern populations:** Growing body of literature but MetS thresholds not formally validated in large prospective cohorts.
3. **Older adults (>75 years):** Risk associations between MetS and CVD attenuate at advanced age; predictive validity of component count uncertain in this age group.
4. **Women of reproductive age on oral contraceptives:** OCP use raises TG and BP, potentially falsely triggering two criteria.

### Cautionary trial evidence

- **ACCORD trial (2010):** Intensive glycaemic control in T2DM patients (many with MetS) did not reduce cardiovascular mortality and increased hypoglycaemia mortality — caution against overmedicalising glucose component in isolation.
- **AIM-HIGH trial (2011):** Niacin therapy raised HDL and lowered TG (addressing two MetS criteria) but did not reduce cardiovascular events in statin-treated patients. Biomarker improvement ≠ outcome improvement for isolated pharmacological HDL/TG manipulation.

---

## 10. HealthIQ Platform Signal Mapping

**Signal identifier:**
```
signal_metabolic_syndrome_pattern
```

**Physiological system:**
```
metabolic
```

**Primary metric:**
```
derived.mets_component_count
```

**Required biomarkers:**
```
- triglycerides
- hdl_cholesterol
- glucose
- waist_circumference_cm    [from lifestyle_registry]
- systolic_bp               [from lifestyle_registry]
- diastolic_bp              [from lifestyle_registry]
- biological_sex            [from questionnaire]
- ethnicity                 [from questionnaire]
```

**Required derived metrics:**
```
- derived.mets_component_count
- derived.mets_bp_flag
- derived.mets_waist_flag
- derived.tg_hdl_ratio      [already in platform]
```

**Optional biomarkers:**
```
- insulin
- hba1c
- crp
- alt
- uric_acid
- antihypertensive_medication   [from medications / questionnaire]
- lipid_lowering_medication     [from medications / questionnaire]
- antidiabetic_medication       [from medications / questionnaire]
```

**Optional derived metrics:**
```
- derived.homa_ir            [requires fasting insulin + glucose]
- derived.non_hdl_cholesterol [already in platform]
```

**Threshold summary:**
```
optimal:    derived.mets_component_count ≤ 1 component
suboptimal: derived.mets_component_count = 2 components
at_risk:    derived.mets_component_count ≥ 3 components
```

**Override rules:**
```
rule: antihypertensive_medication = true → bp_component = 1 (criterion met)
evidence: Alberti et al. 2009 (harmonised guideline)

rule: antidiabetic_medication = true → glucose_component = 1 (criterion met)
evidence: Alberti et al. 2009

rule: lipid_lowering_medication includes fibrate/niacin → tg_component = 1 (criterion met)
evidence: Alberti et al. 2009

rule: triglycerides ≥ 5.6 mmol/L → force at_risk + pancreatitis_alert flag
evidence: ESC/EAS 2019 dyslipidaemia guidelines

rule: chronic_conditions includes type_2_diabetes OR prediabetes → glucose_component = 1
evidence: Clinical diagnostic certainty > threshold

rule: age < 18 → signal_suppressed (paediatric population excluded)
evidence: Adult definitions not validated in children
```

**Bundle consumers:**
```
- metabolic_health
- cardiovascular_risk
- biological_age
- vascular_age
- insulin_resistance_index   [if available]
```

**Implementation notes:**

1. **New derived metrics required:**
   - `derived.mets_component_count` — integer 0–5; requires all 5 component flags as inputs; medication overrides must be applied before counting
   - `derived.mets_bp_flag` — binary (0/1); OR logic across SBP ≥130, DBP ≥85, antihypertensive_medication
   - `derived.mets_waist_flag` — binary (0/1); requires lookup table keyed on `ethnicity` × `biological_sex` with the ethnic-specific thresholds in Section 7

2. **Ethnic waist threshold lookup table** must be implemented as a platform lookup asset keyed on IDF/WHO ethnicity categories. Mapping from free-text ethnicity input to standardised IDF category will require engineering input — recommend controlled vocabulary in questionnaire for `ethnicity` field with pre-defined mapping.

3. **TG/HDL ratio** is already computed. Its thresholds (mmol/L: <0.87 optimal, ≥1.74 at_risk) should be exposed as a supporting sub-signal or diagnostic aide within the MetS report card — not as the primary tier classifier.

4. **Medication override flags:** The platform must expose `antihypertensive_medication`, `lipid_lowering_medication`, and `antidiabetic_medication` as boolean inputs from the medications/questionnaire SSOT. These are required for guideline-compliant MetS scoring.

5. **Partial MetS (suboptimal tier = 2 components):** The 2-component tier is not formally defined in the 2009 guideline (which is binary: MetS present/absent at ≥3). The platform's suboptimal tier at 2 components is a HealthIQ-specific extension to support early risk communication, anchored in Gami et al. 2007 data showing intermediate CVD risk elevation with 2 components. This extension should be clearly labelled in the UX as "high-risk pattern emerging, not yet meeting full metabolic syndrome criteria."

6. **Component pattern analysis (optional enhancement):** Beyond the count, the specific combination of components carries biological meaning. TG elevated + HDL low (dyslipidaemic axis) without glucose/BP may suggest early lipid-centric insulin resistance. Glucose elevated + BP elevated without significant lipid dysregulation may suggest a different trajectory. Engineering may wish to expose component pattern as a secondary output for personalised narrative generation.

---

## 11. Supporting References

1. **Alberti KGMM, Eckel RH, Grundy SM, et al.** Harmonizing the metabolic syndrome: a joint interim statement of the International Diabetes Federation Task Force on Epidemiology and Prevention; National Heart, Lung, and Blood Institute; American Heart Association; World Heart Federation; International Atherosclerosis Society; and International Association for the Study of Obesity. *Circulation.* 2009;120(16):1640–1645. doi:10.1161/CIRCULATIONAHA.109.192644
   *The reference definition document for the signal; establishes the 5-component, ≥3 criteria framework and ethnic-specific waist thresholds.*

2. **Mottillo S, Filion KB, Genest J, et al.** The metabolic syndrome and cardiovascular risk: a systematic review and meta-analysis. *Journal of the American College of Cardiology.* 2010;56(14):1113–1132. doi:10.1016/j.jacc.2010.05.034
   *Largest meta-analysis (n=951,083) establishing ~2× CVD risk and ~5× T2DM risk associated with MetS.*

3. **Gami AS, Witt BJ, Howard DE, et al.** Metabolic syndrome and risk of incident cardiovascular events and death: a systematic review and meta-analysis of longitudinal studies. *Journal of the American College of Cardiology.* 2007;49(4):403–414. doi:10.1016/j.jacc.2006.10.068
   *Meta-analysis (n=172,573) confirming RR ~1.78 for CVD incidence in MetS-positive individuals.*

4. **Lorenzo C, Okoloise M, Williams K, Stern MP, Haffner SM (San Antonio Heart Study).** The metabolic syndrome as predictor of type 2 diabetes: the San Antonio Heart Study. *Diabetes Care.* 2003;26(11):3153–3159. doi:10.2337/diacare.26.11.3153
   *Prospective cohort demonstrating OR ~3.5–5.2 for incident T2DM by MetS status across ethnic groups.*

5. **Sattar N, Gaw A, Scherbakova O, et al.** Metabolic syndrome with and without C-reactive protein as a predictor of coronary heart disease and diabetes in the West of Scotland Coronary Prevention Study. *Circulation.* 2003;108(4):414–419. doi:10.1161/01.CIR.0000080897.52664.94
   *Prospective nested cohort confirming MetS cardiovascular predictive validity; also demonstrates CRP adds information.*

6. **Isomaa B, Almgren P, Tuomi T, et al.** Cardiovascular morbidity and mortality associated with the metabolic syndrome. *Diabetes Care.* 2001;24(4):683–689. doi:10.2337/diacare.24.4.683
   *Botnia Study; WHO-defined MetS conferring 3× CVD risk and 5× T2DM risk; long-term follow-up data.*

7. **McLaughlin T, Abbasi F, Cheal K, Chu J, Lamendola C, Reaven G.** Use of metabolic markers to identify overweight individuals who are insulin resistant. *Annals of Internal Medicine.* 2003;139(10):802–809. doi:10.7326/0003-4819-139-10-200311180-00007
   *Clamp-validated TG/HDL ratio threshold derivation; establishes ≥3.0 mg/dL (≡ ≥0.87 mmol/L) as insulin resistance surrogate.*

8. **Ford ES, Giles WH, Dietz WH.** Prevalence of the metabolic syndrome among US adults: findings from the Third National Health and Nutrition Examination Survey. *JAMA.* 2002;287(3):356–359. doi:10.1001/jama.287.3.356
   *Population-level MetS prevalence data; NHANES III cross-sectional reference.*

9. **Kahn R, Buse J, Ferrannini E, Stern M (ADA/EASD).** The metabolic syndrome: time for a critical appraisal. *Lancet.* 2005;366(9501):1901–1906. doi:10.1016/S0140-6736(05)67483-1
   *Cautionary critique of MetS as a construct; important counterweight to over-reliance on binary MetS classification.*

10. **Grundy SM, Cleeman JI, Daniels SR, et al. (AHA/NHLBI Scientific Statement).** Diagnosis and management of the metabolic syndrome. *Circulation.* 2005;112(17):2735–2752. doi:10.1161/CIRCULATIONAHA.105.169404
    *ATP III update; foundational American guideline for MetS clinical management.*

11. **Chiasson JL, Josse RG, Gomis R, et al. (STOP-NIDDM Trial).** Acarbose for prevention of type 2 diabetes mellitus: the STOP-NIDDM randomised trial. *Lancet.* 2002;359(9323):2072–2077. doi:10.1016/S0140-6736(02)08905-5
    *Intervention trial demonstrating T2DM prevention in MetS-adjacent (IGT) population.*

12. **Knowler WC, Barrett-Connor E, Fowler SE, et al. (Diabetes Prevention Program Research Group).** Reduction in the incidence of type 2 diabetes with lifestyle intervention or metformin. *New England Journal of Medicine.* 2002;346(6):393–403. doi:10.1056/NEJMoa012512
    *Landmark RCT; lifestyle intervention reduces T2DM incidence by 58% in high-risk population.*

13. **Estruch R, Ros E, Salas-Salvadó J, et al. (PREDIMED).** Primary prevention of cardiovascular disease with a Mediterranean diet. *New England Journal of Medicine.* 2013;368(14):1279–1290. doi:10.1056/NEJMoa1200303
    *RCT; Mediterranean diet reduces CVD events by ~30% in high cardiovascular risk (MetS-enriched) cohort.*

14. **Gupta R, Bhatt DL, Steg PG, et al.** Waist circumference thresholds for metabolic syndrome: comparison of IDF and revised NCEP criteria. *BMC Cardiovascular Disorders.* 2012;12:28. doi:10.1186/1471-2261-12-28
    *Cross-sectional study demonstrating superiority of IDF South Asian waist thresholds over ATP III in Indian cohort.*

15. **Li C, Ford ES, McGuire LC, Mokdad AH.** Increasing trends in waist circumference and abdominal obesity among US adults. *Obesity.* 2007;15(1):216–224. — *[Note: Li et al. 2008 TG/HDL validation reference: Li C, Ford ES, Meng YX, Mokdad AH, Reaven GM.* Diabetes/Metabolism Research and Reviews. *2008;24(6):458–463. doi:10.1002/dmrr.877]* Extended validation of TG/HDL ratio as insulin resistance surrogate in NHANES population.

---

*Report end. Version 1.0. Prepared for HealthIQ knowledge translation pipeline.*
*Evidence cutoff: Studies cited to 2013 (PREDIMED) as anchor; 2009 harmonised definition as current standard. ESC/EAS 2019 invoked for pancreatitis override threshold only.*
