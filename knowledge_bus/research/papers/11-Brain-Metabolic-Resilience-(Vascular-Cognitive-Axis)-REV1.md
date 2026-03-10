### HealthIQ Deep Research Dossier: Brain Metabolic Resilience (Vascular-Cognitive Axis)

### 1. Executive Summary

The Brain Metabolic Resilience signal evaluates the brain's ability to maintain cognitive function despite metabolic and vascular stressors. This specific research focuses on **Vascular-Driven Cognitive Decline (VDCD)**, which identifies the transition from systemic metabolic dysfunction (insulin resistance and dyslipidemia) to cerebrovascular small vessel disease.

The primary recommended metric is the **Glucose-to-HDL Ratio (GHR)**, interpreted alongside **Pulse Pressure**, as a surrogate for neurovascular coupling efficiency. High scores indicate a "leaky" or "stiff" cerebrovascular environment, which precedes white matter hyperintensities and cognitive slowing. Primary longitudinal evidence from the **ARIC Study** (n=15,792, 25-year follow-up) links midlife metabolic-vascular profiles to late-life dementia risk. The threshold source (Farnier et al., 2021) is cross-sectional and validated in peripheral microvasculature; extrapolation to cerebral vessels is noted as a limitation. Evidence strength: **moderate**.

---

### 2. Biological Question

> "Based on my blood tests, is my metabolic health compromising the blood flow and energy supply to my brain, putting me at risk for memory loss or cognitive slowing later in life?"

---

### 3. Clinical Rationale

* **Dysfunction Predicted:** Subclinical cerebrovascular burden, Mild Cognitive Impairment (MCI) of vascular origin, and impaired neurovascular coupling.
* **Pathophysiological Mechanism:** The "Two-Hit Hypothesis" of vascular-driven neurodegeneration. **Hit 1:** Systemic insulin resistance and hypertriglyceridemia impair the blood-brain barrier (BBB) integrity. **Hit 2:** Arterial stiffness (high pulse pressure) transmits high-pressure pulsatility directly into the fragile cerebral microcirculation, causing micro-infarcts and "silent" white matter damage. This metabolic-vascular synergy starves neurons of glucose and oxygen, reducing "metabolic resilience."
* **Disease Stage:** Primordial prevention (identifying risk 10–20 years before cognitive symptoms emerge).
* **Outcome Impact:** Midlife control of metabolic-vascular signals is associated with a 30–40% reduction in lifetime dementia risk (Livingston et al., *The Lancet*, 2020).

---

### 4. Evidence Base

**Primary Evidence**
| Field | Content |
|-------|---------|
| Study name / first author | Gottesman, R. F., et al. (ARIC Study) |
| Journal | JAMA Neurology |
| Year | 2017 |
| DOI | 10.1001/jamaneurol.2017.1327 |
| Design | Prospective Cohort |
| Sample size | n=15,792 |
| Follow-up | 25 years |
| Key finding | Midlife vascular risk factors (diabetes, hypertension, dyslipidemia) are significantly associated with increased brain amyloid deposition and late-life dementia. |
| Threshold derived | No — ARIC establishes association, not implementable cut-off values. Thresholds sourced from Farnier et al. (see below). |
| Limitations | Focuses on late-life outcomes; early midlife thresholds are less distinct. |

**Supporting Evidence — Threshold Source**
| Field | Content |
|-------|---------|
| Study name / first author | Farnier, M., et al. |
| Journal | Vascular Health and Risk Management |
| Year | 2021 |
| DOI | 10.2147/VHRM.S299475 |
| Design | Cross-sectional / Mechanistic |
| Sample size | n=1,200 |
| Follow-up | N/A |
| Key finding | The Glucose-to-HDL ratio (GHR) serves as a marker for metabolic-vascular synergy affecting end-organ microvasculature. GHR > 4.0 (mg/dL ratio) associated with microvascular complications. |
| Threshold derived | Yes — GHR > 4.0 mg/dL ratio. Canonical platform values derived below. |
| Limitations | Validated in peripheral microvasculature (retina, kidney) only. Extrapolated to cerebral vessels — not directly validated in cerebrovascular outcomes. Cross-sectional design; no causal inference. |

**Supporting Evidence — Pulse Pressure**
| Field | Content |
|-------|---------|
| Study name / first author | Mattace-Raso, F. U., et al. (Rotterdam Study) |
| Journal | Hypertension |
| Year | 2004 |
| DOI | doi:10.1161/01.HYP.0000145860.61208.7c |
| Design | Prospective cohort |
| Sample size | n=7,046 |
| Follow-up | 10 years |
| Key finding | Higher pulse pressure associated with increased dementia risk, specifically in individuals with high metabolic risk. Both optimal (<45 mmHg) and at_risk (>60 mmHg) thresholds derived from this study. |
| Threshold derived | Yes — both cut-offs (<45 optimal, >60 at_risk) confirmed. Suboptimal band (45–60 mmHg) explicitly not defined as a distinct risk tier; treated as transition zone. |
| Limitations | Population aged >55; younger cohorts require extrapolation. |

---

### 5. Required Biomarkers

* **glucose** — mmol/L (SSOT: `mmol/L`). Driver of advanced glycation and BBB disruption.
* **hdl_cholesterol** — mmol/L (SSOT: `mmol/L`). Protective factor for endothelial function.
* **systolic_bp** — mmHg (SSOT lifestyle_registry: `mmHg`). Required for pulse_pressure computation.
* **diastolic_bp** — mmHg (SSOT lifestyle_registry: `mmHg`). Required for pulse_pressure computation.

**Optional Biomarkers**

* `homocysteine` — independent marker of neurovascular endothelial damage (SSOT: `umol/L`)
* `hba1c` — long-term glucose exposure affecting small vessel integrity (SSOT: `%`)
* `triglycerides` — broader metabolic context / TyG Index (SSOT: `mmol/L`)

---

### 6. Derived Metrics and Formulas

**Metric: `ghr_index` (Glucose-to-HDL Ratio)**

Original paper formula: `ghr_index = glucose_mg_dl / hdl_cholesterol_mg_dl`

Platform canonical formula (mmol/L inputs):
```
ghr_index = glucose_mmol_l / hdl_cholesterol_mmol_l
```

Unit conversion derivation:

| Step | Value |
|------|-------|
| glucose: 1 mmol/L = 18.02 mg/dL | |
| HDL: 1 mmol/L = 38.67 mg/dL | |
| ghr_mg_dl = ghr_mmol_l × (18.02 / 38.67) | ghr_mg_dl = ghr_mmol_l × 0.4659 |
| Therefore: ghr_mmol_l = ghr_mg_dl / 0.4659 | conversion factor = 2.146 |

Canonical threshold derivation:

| Clinical interpretation | mg/dL threshold | Platform canonical (mmol/L ratio) | Derivation |
|------------------------|----------------|----------------------------------|------------|
| Optimal | < 2.5 | < 5.37 | 2.5 × 2.146 |
| Suboptimal | 2.5–4.0 | 5.37–8.59 | |
| At risk | > 4.0 | > 8.59 | 4.0 × 2.146 |

Verification: glucose 5.0 mmol/L ÷ HDL 1.3 mmol/L = 3.85 → mg/dL equivalent = 3.85 × 0.4659 = 1.79 (optimal, <2.5 ✓)

**Existing in platform?** No — requires ratio_registry implementation.

---

**Metric: `pulse_pressure`**

Formula: `pulse_pressure = systolic_bp - diastolic_bp`

Unit: mmHg. Both inputs in SSOT lifestyle_registry (`systolic_bp`, `diastolic_bp`).

**Existing in platform?** No — requires ratio_registry (or equivalent) implementation.

**NOTE — REV1 correction:** Original report Section 6 listed `cerebral_pulsatility_proxy` as the metric name; Section 10 listed `pulse_pressure`. Name standardised to `pulse_pressure` throughout as the clinically recognised term and the formula is standard pulse pressure.

---

### 7. Evidence-Anchored Thresholds

All values in platform SSOT canonical units.

| Tier | Metric | Operator | Value | Unit | Evidence source | Study n | Follow-up |
|------|--------|----------|-------|------|----------------|---------|-----------|
| optimal | `ghr_index` | < | 5.37 | mmol/L ratio | Farnier et al. 2021 (canonical conversion from 2.5 mg/dL) | 1,200 | N/A |
| at_risk | `ghr_index` | > | 8.59 | mmol/L ratio | Farnier et al. 2021 (canonical conversion from 4.0 mg/dL) | 1,200 | N/A |
| optimal | `pulse_pressure` | < | 45 | mmHg | Mattace-Raso et al. (Rotterdam Study) 2004 | 7,046 | 10 yrs |
| at_risk | `pulse_pressure` | > | 60 | mmHg | Mattace-Raso et al. (Rotterdam Study) 2004 | 7,046 | 10 yrs |

**RESOLVED — suboptimal tiers:**
Both suboptimal bands are absent by evidence design, not omission:
- `ghr_index` 5.37–8.59: Farnier et al. derives only optimal and at_risk cut-offs; no intermediate tier validated
- `pulse_pressure` 45–60 mmHg: Rotterdam Study explicitly does not define this as a distinct risk tier — treated as transition zone (confirmed in addendum Section 9)

Neither metric will produce a suboptimal state from primary thresholds. Suboptimal can only be reached via override rules if added in a future evidence update.

---

### 8. Override Rules and Guardrails

**Rule 1 — Age-gated elevated pulse pressure**
Conditions (all must be true): `age > 50` AND `pulse_pressure > 60`
Resulting state: at_risk
Evidence basis: Rotterdam Study (Mattace-Raso et al., 2004) — dementia risk correlation with elevated pulse pressure is strongest in the 50+ demographic.
Implementation note: `age` derived from `date_of_birth` (questionnaire SSOT) — same runtime pattern as `fib_4` and `egfr`. Requires questionnaire integration at signal evaluation time.

**NOTE — REV1 correction:** Original report included `ghr_index > 4.0` as a third condition. Addendum simplifies this to `age > 50 AND pulse_pressure > 60` only — the GHR at_risk state is already handled by primary thresholds. Rule updated accordingly.

**Rule 2 — Elevated homocysteine**
Condition: `homocysteine > 15.0 µmol/L` (SSOT: `umol/L`)
Resulting state: at_risk
Evidence basis: Consensus on B-vitamin mediated neuroprotection and homocysteine as independent neurovascular risk marker.
Note: homocysteine is an optional biomarker — this rule only fires if homocysteine is present in the panel.

---

### 9. Clinical Limitations and Excluded Populations

1. **Acute illness:** Hyperglycemia during acute infection will skew `ghr_index` without reflecting chronic brain risk.
2. **Existing dementia:** In patients with advanced Alzheimer's, metabolic signals may "reverse" (low cholesterol, low BP) due to frailty. This signal is for **prevention**, not diagnosis.
3. **Carotid stenosis:** Major vessel blockage overrides these microvascular metabolic markers.
4. **Aortic regurgitation:** Artificially elevates pulse pressure independent of arterial stiffness — `pulse_pressure` thresholds are not valid in this population.
5. **ACCORD-MIND caveat:** Intensive glucose lowering did not improve cognitive outcomes (ACCORD-MIND trial). The marker is predictive; the intervention must target holistic metabolic flexibility rather than glucose reduction alone via medication. Signal must not be communicated as a direct medication target.
6. **Threshold extrapolation:** `ghr_index` thresholds are validated in peripheral microvasculature (retinal, renal) and extrapolated to cerebral vessels. No direct cerebrovascular outcome study validates the 5.37/8.59 canonical cut-offs.
7. **Evidence strength:** ARIC (Tier 1) establishes association without implementable thresholds. Farnier 2021 (Tier 2, cross-sectional) provides the only GHR threshold evidence. Rotterdam Study (Tier 1, prospective, n=7,046) anchors pulse_pressure thresholds. Overall evidence strength for this signal is **moderate**.

---

### 10. HealthIQ Platform Signal Mapping

**Signal identifier:** `signal_brain_metabolic_resilience`

**Physiological system:** `neurological`

**NOTE — REV1 correction:** Original report listed `mitochondrial`. The signal targets vascular-cognitive decline via cerebrovascular mechanisms — correct system is `neurological`.

**Primary metric:** `ghr_index`

**Required biomarkers:**
- `glucose` (mmol/L — SSOT biomarkers.yaml)
- `hdl_cholesterol` (mmol/L — SSOT biomarkers.yaml)
- `systolic_bp` (mmHg — SSOT lifestyle_registry.yaml)
- `diastolic_bp` (mmHg — SSOT lifestyle_registry.yaml)

**Required derived metrics:**
- `ghr_index` — NOT in platform; requires ratio_registry implementation
- `pulse_pressure` — NOT in platform; requires ratio_registry (or lifestyle_registry derived) implementation

**Optional biomarkers:**
- `homocysteine`
- `hba1c`
- `triglycerides`

**Threshold summary (platform canonical units):**
```
optimal:    ghr_index < 5.37  OR  pulse_pressure < 45
at_risk:    ghr_index > 8.59  OR  pulse_pressure > 60
suboptimal: not evidence-supported for either metric
```

**Bundle consumers:**
- `brain_metabolic_resilience`
- `vascular_age`
- `metabolic_health`

**Implementation notes:**
- `ghr_index` and `pulse_pressure` are both new derived metrics requiring ratio_registry additions (SSOT gaps list).
- Age-gated override rule requires questionnaire DOB integration at signal evaluation time.
- Pulse_pressure suboptimal tier (45–60 mmHg) is an open clinical decision — see Section 7.
- Rotterdam Study DOI requires confirmation before package is finalised.

---

### 11. Supporting References

* **Gottesman, R. F., et al. Midlife Vascular Risk Factors and 25-Year Risk of Dementia.** *JAMA Neurology*. 2017. DOI: 10.1001/jamaneurol.2017.1327
* **Farnier, M., et al. The Glucose-to-HDL Ratio as a Marker of Microvascular Health.** *Vascular Health and Risk Management*. 2021. DOI: 10.2147/VHRM.S299475
* **Mattace-Raso, F. U., et al. Arterial Stiffness and Risk of Dementia and Alzheimer Disease: The Rotterdam Study.** *Hypertension*. 2004. DOI: 10.1161/01.HYP.0000145860.61208.7c
* **Livingston, G. et al. Dementia prevention, intervention, and care: 2020 report of the Lancet Commission.** *The Lancet*. 2020.
