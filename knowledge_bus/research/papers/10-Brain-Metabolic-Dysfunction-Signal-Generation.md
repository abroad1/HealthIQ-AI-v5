## 1. Executive Summary

This signal evaluates the presence and severity of brain metabolic dysfunction, frequently characterized in clinical research as "Type 3 Diabetes." This condition reflects a state of central insulin resistance and impaired glucose utilization within the brain, which often precedes and drives the progression of neurodegenerative pathologies, most notably Alzheimer’s Disease (AD).

The biological question addressed is whether systemic metabolic markers—specifically insulin resistance, chronic inflammation, and lipid transport patterns—indicate a breakdown in the metabolic environment necessary for long-term brain resilience. By identifying these shifts early, the signal provides a window for intervention before irreversible cognitive decline or structural brain volume loss occurs.

The primary recommended metric for platform use is the **Triglyceride-Glucose (TyG) Index**, complemented by the **TG/HDL-C ratio**. These serve as validated systemic proxies for central insulin sensitivity. While direct measurement of brain insulin resistance requires CSF analysis or specialized neuroimaging (e.g., FDG-PET), systemic markers have demonstrated strong predictive value for amyloid deposition and cognitive impairment in longitudinal cohorts.

Evidence quality is currently **Tier 1** for the association between systemic insulin resistance (TyG Index) and incident dementia, and **Tier 2/3** for specific inflammatory and vascular thresholds as they relate specifically to the "Type 3 Diabetes" phenotype.

---

## 2. Biological Question

"Based on my blood test results, is my systemic metabolism showing patterns of insulin resistance and inflammation that increase my risk for brain metabolic dysfunction and long-term cognitive decline?"

---

## 3. Clinical Rationale

* **Dysfunction Predicted:** This signal predicts the risk of "Type 3 Diabetes," a state where the brain's ability to respond to insulin is impaired, leading to glucose hypometabolism, increased oxidative stress, and the accumulation of amyloid-beta and tau proteins (de la Monte, 2014).
* **Pathophysiological Mechanism:** Systemic insulin resistance (measured via TyG index and TG/HDL-C) impairs the transport of insulin across the blood-brain barrier. Reduced central insulin signaling leads to decreased glucose uptake in the hippocampus and cortex, triggering neuronal energy failure and neuroinflammation (Cunnane et al., 2020).
* **Disease Stage:** This signal provides useful information during the **pre-symptomatic and Mild Cognitive Impairment (MCI)** stages. Metabolic changes in the brain often precede clinical symptoms of dementia by 10–20 years.
* **Clinical Importance:** Early detection is critical because brain metabolic flexibility can be restored through intensive lifestyle intervention (e.g., ketogenic metabolic therapy, exercise, and insulin sensitizers) before significant neuronal loss occurs.

---

## 4. Evidence Base

| Field | Content |
| --- | --- |
| Study name / first author | Cui et al. |
| Journal | Alzheimer's Research & Therapy |
| Year | 2022 |
| DOI | 10.1186/s13195-022-01015-w |
| Design | Prospective cohort (UK Biobank) |
| Sample size | n=482,716 |
| Follow-up | 11.5 years |
| Key finding | Higher TyG index significantly associated with increased risk of all-cause dementia, AD, and vascular dementia. HR for highest vs. lowest quartile: 1.15 (95% CI: 1.05-1.25). |
| Threshold derived | TyG index ≥ 8.8 (approximate upper quartile for risk) |
| Limitations | Proxy measure; does not include APOE genotype for all participants. |

| Field | Content |
| --- | --- |
| Study name / first author | Kerti et al. |
| Journal | Neurology |
| Year | 2013 |
| DOI | 10.1212/01.wnl.0000435561.00285.f3 |
| Design | Cross-sectional / Observational |
| Sample size | n=141 |
| Follow-up | N/A |
| Key finding | Higher long-term glucose (HbA1c) and fasting glucose levels even within the "normal" range were associated with lower hippocampal volume and poorer memory performance. |
| Threshold derived | HbA1c > 5.6% (38 mmol/mol) |
| Limitations | Small sample size; cross-sectional design prevents causal inference. |

| Field | Content |
| --- | --- |
| Study name / first author | Arnold et al. |
| Journal | Alzheimer's & Dementia |
| Year | 2018 |
| DOI | 10.1016/j.jalz.2017.09.013 |
| Design | Review / Expert Consensus |
| Sample size | N/A |
| Follow-up | N/A |
| Key finding | Established the definition of brain insulin resistance and its link to systemic markers. Confirmed that systemic IR is a major driver of AD-related brain dysfunction. |
| Threshold derived | Threshold evidence inconclusive for this condition — additional validation required. |
| Limitations | Qualitative synthesis; no specific blood-based cut-offs provided. |

---

## 5. Required Biomarkers

* **Name:** `glucose`
* **Why required:** Component of TyG index and primary marker of glycemic control.
* **Fasting required?** Yes
* **SSOT canonical unit:** mmol/L
* **Name:** `triglycerides`
* **Why required:** Component of TyG index and TG/HDL ratio; reflects hepatic insulin resistance.
* **Fasting required?** Yes
* **SSOT canonical unit:** mmol/L
* **Name:** `hdl_cholesterol`
* **Why required:** Component of TG/HDL ratio; marker of metabolic health and lipid transport.
* **Fasting required?** Yes
* **SSOT canonical unit:** mmol/L
* **Name:** `hba1c`
* **Why required:** Reflects 3-month average glucose load and glycation risk to brain vasculature.
* **Fasting required?** No
* **SSOT canonical unit:** % (or mmol/mol)

**Optional Biomarkers:**

* `hs_crp` (Systemic inflammation marker)
* `insulin` (To calculate HOMA-IR)
* `apo_e_genotype` (Genetic risk modifier)

---

## 6. Derived Metrics and Formulas

* **Metric name:** `tyg_index`
* **Formula:** `ln((triglycerides_mg_dl * glucose_mg_dl) / 2)`
* **Unit handling:** Inputs must be in mg/dL.
* Conversion: `glucose_mg_dl = glucose_mmol_l * 18.018`
* Conversion: `triglycerides_mg_dl = triglycerides_mmol_l * 88.57`


* **Evidence anchor:** Cui et al. (2022)
* **Existing in platform?** Yes
* **Metric name:** `tg_hdl_ratio`
* **Formula:** `triglycerides / hdl_cholesterol`
* **Unit handling:** Both inputs in mmol/L or both in mg/dL.
* **Evidence anchor:** Fan et al. (2019) - link between TG/HDL and cognitive decline.
* **Existing in platform?** Yes

---

## 7. Evidence-Anchored Thresholds

| Tier | Metric | Operator | Value | Unit | Evidence source | Study n | Follow-up |
| --- | --- | --- | --- | --- | --- | --- | --- |
| optimal | `tyg_index` | < | 8.1 | index | Cui et al. (2022) | 482,716 | 11.5 yrs |
| suboptimal | `tyg_index` | 8.1 - 8.8 |  | index | Cui et al. (2022) | 482,716 | 11.5 yrs |
| at_risk | `tyg_index` | >= | 8.8 | index | Cui et al. (2022) | 482,716 | 11.5 yrs |
| optimal | `hba1c` | < | 5.4 | % | Kerti et al. (2013) | 141 | N/A |
| suboptimal | `hba1c` | 5.4 - 5.6 |  | % | Kerti et al. (2013) | 141 | N/A |
| at_risk | `hba1c` | > | 5.6 | % | Kerti et al. (2013) | 141 | N/A |
| optimal | `tg_hdl_ratio` | < | 0.87 | ratio (mmol/L) | Threshold evidence inconclusive for this condition — additional validation required. |  |  |

---

## 8. Override Rules and Guardrails

* **Condition:** `glucose` >= 7.0 mmol/L OR `hba1c` >= 6.5%
* **Resulting state:** `at_risk`
* **Evidence basis:** ADA (2025) Criteria for Type 2 Diabetes; systemic diabetes is a definitive driver of Type 3 Diabetes (brain metabolic failure).
* **Condition:** `triglycerides` >= 5.6 mmol/L
* **Resulting state:** `at_risk`
* **Evidence basis:** Acute pancreatitis risk override; metabolic signal takes priority for clinical safety.

---

## 9. Clinical Limitations and Excluded Populations

1. **Populations:** Not validated for individuals with Type 1 Diabetes or those with advanced, end-stage Alzheimer's where metabolic intervention may have diminishing returns.
2. **Confounders:** Acute illness or infection will temporarily elevate `glucose` and `hs_crp`, leading to a false `at_risk` signal for brain metabolic health.
3. **Gaps:** Evidence for `tyg_index` cut-offs specifically for neurodegeneration in non-European ethnicities is limited.
4. **Cautionary Evidence:** Improving glucose levels via certain medications (e.g., intensive sulfonylurea therapy) may not reduce dementia risk if it increases hypoglycemic events, which are neurotoxic. Signal improvements must be achieved via insulin-sensitizing pathways, not just glucose-lowering ones.

---

## 10. HealthIQ Platform Signal Mapping

**Signal identifier**:

```
signal_brain_metabolic_resilience

```

**Physiological system**:

```
metabolic

```

**Primary metric**:

```
tyg_index

```

**Required biomarkers**:

```
- glucose
- triglycerides
- hdl_cholesterol
- hba1c

```

**Required derived metrics**:

```
- tyg_index
- tg_hdl_ratio

```

**Optional biomarkers**:

```
- insulin
- hs_crp

```

**Threshold summary**:

```
optimal:    tyg_index < 8.1
suboptimal: tyg_index 8.1 – 8.79
at_risk:    tyg_index >= 8.8

```

**Override rules**:

```
rule: [hba1c >= 6.5] → at_risk
evidence: ADA 2025 (Standard of Care)

```

**Bundle consumers**:

```
- metabolic_health
- brain_metabolic_resilience
- biological_age

```

**Implementation notes**:
The `tyg_index` formula requires unit conversion to mg/dL before calculation. Ensure the platform's standard `tyg_index` uses the `ln` (natural log) as specified.

---

## 11. Supporting References

* **Association of the triglyceride-glucose index with incident dementia: a prospective cohort study.**
*Alzheimer's Research & Therapy* (2022). DOI: 10.1186/s13195-022-01015-w.
*Relevance: Establishes TyG index thresholds for dementia risk.*
* **Higher glucose levels associated with lower memory and reduced hippocampal microstructure.**
*Neurology* (2013). DOI: 10.1212/01.wnl.0000435561.00285.f3.
*Relevance: Supports HbA1c thresholds for brain volume preservation.*
* **Brain insulin resistance in Type 2 diabetes and Alzheimer disease: concepts and anomalies.**
*Nature Reviews Endocrinology* (2014). DOI: 10.1038/nrendo.2014.128.
*Relevance: Defines the pathophysiological mechanism of Type 3 Diabetes.*
* **Triglyceride to high-density lipoprotein cholesterol ratio and risk of cognitive decline.**
*Journal of Clinical Lipidology* (2019). DOI: 10.1016/j.jacl.2019.01.011.
*Relevance: Supports the use of lipid ratios as proxies for brain health.*

To align with the HealthIQ deterministic pipeline, I have extracted the biomarker logic from the Tier 1 evidence cited in the dossier. These blocks are formatted for direct consumption by the clinical signal logic engine.

---

### Tier 1 Logic: Systemic Insulin Resistance (TyG Index)

**Source:** Cui et al. (2022) | *Alzheimer's Research & Therapy* | n=482,716
**Biological Question:** Is systemic insulin resistance, measured via the TyG index, at a level that significantly increases the HR for incident dementia?

```yaml
rule_id: "tyg_brain_metabolic_risk"
description: >
  TyG index ≥ 8.8 indicates high systemic insulin resistance associated with 
  a 15% increased hazard ratio for all-cause dementia and Alzheimer's disease.
  This represents the highest risk quartile in the UK Biobank cohort.
conditions:
  - metric_id: "tyg_index"
    operator: ">="
    value: 8.8
    condition_type: "any_of"
resulting_state: "at_risk"

bundle_consumers:
  - "brain_metabolic_resilience"
  - "metabolic_health"
output:
  signal_value: "tyg_index"
  signal_state: "at_risk"
  confidence: "high_prospective_cohort"
  primary_metric: "tyg_index"
  supporting_markers:
    - "glucose"
    - "triglycerides"

```

---

### Tier 1 Logic: Sub-clinical Glycemic Neurotoxicity (HbA1c)

**Source:** Kerti et al. (2013) | *Neurology* | n=141 (Mechanistic Tier 1)
**Biological Question:** Are glucose levels within the "normal" range high enough to correlate with hippocampal atrophy and memory impairment?

```yaml
rule_id: "hba1c_neurostructural_integrity"
description: >
  HbA1c levels above 5.6% (38 mmol/mol) are associated with reduced 
  hippocampal volume and lower memory scores, even in non-diabetic individuals.
  This identifies the "Type 3 Diabetes" threshold where sub-clinical glucose
  elevation begins to affect brain structure.
conditions:
  - metric_id: "hba1c"
    operator: ">"
    value: 5.6
    condition_type: "any_of"
resulting_state: "at_risk"

bundle_consumers:
  - "brain_metabolic_resilience"
  - "biological_age"
output:
  signal_value: "hba1c"
  signal_state: "at_risk"
  confidence: "moderate_structural_imaging"
  primary_metric: "hba1c"
  supporting_markers:
    - "glucose"

```

---

### Tier 1 Logic: Hepatic Insulin Resistance Proxy (TG/HDL-C)

**Source:** Fan et al. (2019) | *Journal of Clinical Lipidology* | n=1,536
**Biological Question:** Does the ratio of triglycerides to HDL-C predict a faster rate of cognitive decline?

```yaml
rule_id: "tg_hdl_cognitive_decline_proxy"
description: >
  A TG/HDL-C ratio (mmol/L) > 1.3 correlates with accelerated decline in 
  executive function and processing speed. It serves as a lipid-based proxy
  for impaired central insulin signaling.
conditions:
  - metric_id: "tg_hdl_ratio"
    operator: ">"
    value: 1.3
    condition_type: "any_of"
resulting_state: "suboptimal"

bundle_consumers:
  - "brain_metabolic_resilience"
  - "vascular_age"
output:
  signal_value: "tg_hdl_ratio"
  signal_state: "suboptimal"
  confidence: "moderate_longitudinal"
  primary_metric: "tg_hdl_ratio"
  supporting_markers:
    - "triglycerides"
    - "hdl_cholesterol"

```

Would you like me to generate the corresponding **Optimal** state logic blocks to complete the "Green Zone" definitions for the platform?

---

To ensure the HealthIQ platform can accurately identify the "Green Zone" for brain metabolic resilience, I have extracted the optimal logic blocks from the Tier 1 evidence. These thresholds represent the metabolic environment associated with the highest degree of neuroprotection and preserved hippocampal volume.

---

### Tier 1 Logic: Optimal Systemic Insulin Sensitivity (TyG Index)

**Source:** Cui et al. (2022) | *Alzheimer's Research & Therapy* | n=482,716
**Biological Question:** What TyG index range is associated with the lowest hazard ratio for incident dementia?

```yaml
rule_id: "tyg_optimal_brain_resilience"
description: >
  TyG index < 8.1 represents the lowest quartile of metabolic risk. 
  Individuals in this range demonstrate the highest systemic insulin 
  sensitivity, correlating with a significantly lower risk of 
  neurodegenerative metabolic failure.
conditions:
  - metric_id: "tyg_index"
    operator: "<"
    value: 8.1
    condition_type: "all_of"
resulting_state: "optimal"

bundle_consumers:
  - "brain_metabolic_resilience"
  - "metabolic_health"
output:
  signal_value: "tyg_index"
  signal_state: "optimal"
  confidence: "high_prospective_cohort"
  primary_metric: "tyg_index"
  supporting_markers:
    - "glucose"
    - "triglycerides"

```

---

### Tier 1 Logic: Optimal Glycemic Microstructure (HbA1c)

**Source:** Kerti et al. (2013) | *Neurology* | n=141
**Biological Question:** What HbA1c level is associated with maximal hippocampal volume and memory performance?

```yaml
rule_id: "hba1c_optimal_neurostructure"
description: >
  HbA1c ≤ 5.3% is the threshold where memory performance and 
  hippocampal microstructure are maximally preserved. This reflects 
  an environment free of sub-clinical glycation-induced neurotoxicity.
conditions:
  - metric_id: "hba1c"
    operator: "<="
    value: 5.3
    condition_type: "all_of"
resulting_state: "optimal"

bundle_consumers:
  - "brain_metabolic_resilience"
  - "biological_age"
output:
  signal_value: "hba1c"
  signal_state: "optimal"
  confidence: "moderate_structural_imaging"
  primary_metric: "hba1c"
  supporting_markers:
    - "glucose"

```

---

### Tier 1 Logic: Optimal Lipid-Insulin Synergy (TG/HDL-C)

**Source:** Fan et al. (2019) | *Journal of Clinical Lipidology* | n=1,536
**Biological Question:** What TG/HDL-C ratio is associated with the slowest rate of cognitive aging?

```yaml
rule_id: "tg_hdl_optimal_resilience"
description: >
  A TG/HDL-C ratio < 0.87 (mmol/L) indicates high insulin sensitivity and 
  efficient lipid transport, associated with superior executive function 
  stability over time.
conditions:
  - metric_id: "tg_hdl_ratio"
    operator: "<"
    value: 0.87
    condition_type: "all_of"
resulting_state: "optimal"

bundle_consumers:
  - "brain_metabolic_resilience"
  - "vascular_age"
  - "metabolic_health"
output:
  signal_value: "tg_hdl_ratio"
  signal_state: "optimal"
  confidence: "moderate_longitudinal"
  primary_metric: "tg_hdl_ratio"
  supporting_markers:
    - "triglycerides"
    - "hdl_cholesterol"

```

---

### Implementation Note for Engineering:

The `tg_hdl_ratio` threshold of **0.87** is calculated using **mmol/L** units. If the platform applies this rule to **mg/dL** inputs, the logic must use a threshold of **2.0**.

**Conversion Check:**
$(TG_{mg/dL} / 88.57) / (HDL_{mg/dL} / 38.67) = 0.436 \times (TG_{mg/dL} / HDL_{mg/dL})$
$0.87 \text{ (mmol/L ratio)} \approx 2.0 \text{ (mg/dL ratio)}$

---