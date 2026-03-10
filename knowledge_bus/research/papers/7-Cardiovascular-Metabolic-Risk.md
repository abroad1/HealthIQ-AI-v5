### HealthIQ Deep Research Dossier: Cardiovascular Metabolic Risk - Metabolic-Driven Vascular Ageing (MDVA)

### 1. Executive Summary

The Metabolic-Driven Vascular Ageing (MDVA) signal quantifies the accelerated structural and functional degradation of the arterial wall caused by chronic metabolic dysregulation. Unlike chronological age, MDVA identifies "Early Vascular Ageing" (EVA) by measuring the interplay between glycative stress (Advanced Glycation End-products), oxidative lipid damage, and arterial stiffness.

The primary recommended metric is the **AIP (Atherogenic Index of Plasma)**, which serves as a proxy for lipoprotein particle size and arterial wall penetration potential. This is integrated with blood pressure and glucose variability markers. The evidence quality is Tier 1, anchored in longitudinal cohorts such as the **Framingham Heart Study** and **MESA (Multi-Ethnic Study of Atherosclerosis)**, which demonstrate that metabolic health is a more potent predictor of arterial "stiffness" than birth year.

---

### 2. Biological Question

> "Based on my blood tests and vitals, is my metabolism causing my arteries to age faster than my actual years, increasing my risk of 'stiff' arteries?"

---

### 3. Clinical Rationale

* **Dysfunction Predicted:** Early Vascular Ageing (EVA), arterial stiffness, and isolated systolic hypertension.
* **Pathophysiological Mechanism:** High circulating glucose and insulin levels drive the formation of Advanced Glycation End-products (AGEs). These AGEs cross-link collagen in the vascular media, making arteries rigid. Simultaneously, the preponderance of small dense LDL (measured by a high AIP) allows for easier sub-endothelial infiltration, triggering a chronic calcification cycle that mirrors the ageing process but at an accelerated rate.
* **Disease Stage:** Subclinical. This signal identifies individuals who have high "vascular age" despite low traditional 10-year risk scores.
* **Outcome Impact:** Early intervention with insulin-sensitizing protocols (High-Intensity Interval Training, autophagy-inducing fasting cycles) can halt or partially reverse arterial stiffening, preventing downstream heart failure with preserved ejection fraction (HFpEF).

---

### 4. Evidence Base

**Primary Evidence**
| Field | Content |
|-------|---------|
| Study name / first author | Niroumand, S., et al. |
| Journal | BMC Cardiovascular Disorders |
| Year | 2015 |
| DOI | 10.1186/s12872-015-0117-x |
| Design | Prospective cross-sectional analysis |
| Sample size | n=4,215 |
| Follow-up | N/A |
| Key finding | AIP (log(TG/HDL-C)) is the strongest metabolic predictor of arterial stiffness and coronary artery calcification. |
| Threshold derived | AIP > 0.21 (High Risk of accelerated ageing) |
| Limitations | Focuses on Persian population; requires multi-ethnic validation. |

**Supporting Evidence**
| Field | Content |
|-------|---------|
| Study name / first author | Nilsson, P. M., et al. |
| Journal | Journal of Hypertension |
| Year | 2014 |
| DOI | 10.1097/HJH.0000000000000060 |
| Design | Expert Consensus / Review of Longitudinal Cohorts |
| Sample size | Meta-analysis scale |
| Follow-up | Up to 20 years |
| Key finding | Defines "Early Vascular Aging" (EVA) as a mismatch between chronological age and biological vascular stiffness driven by glucose/lipids. |
| Threshold derived | Threshold evidence inconclusive for this condition — additional validation required. |
| Limitations | Identifies the syndrome but lacks a single "golden" blood threshold. |

---

### 5. Required Biomarkers

* **triglycerides** (lipid_transport): Core component of AIP. (Fasting: Yes; SSOT: `mmol/L`)
* **hdl_cholesterol** (lipid_transport): Core component of AIP. (Fasting: Yes; SSOT: `mmol/L`)
* **glucose** (metabolic): Marker of glycative stress. (Fasting: Yes; SSOT: `mmol/L`)
* **systolic_bp** (lifestyle_registry): Clinical manifestation of arterial stiffness. (SSOT: `mmHg`)

**Optional Biomarkers**

* `hb_a1c`: Long-term glycative stress marker.
* `albuminuria` (uACR): Early sign of microvascular ageing/damage.

---

### 6. Derived Metrics and Formulas

* **Metric name:** `aip` (Atherogenic Index of Plasma)
* **Formula:** `log10(triglycerides_mmol_L / hdl_cholesterol_mmol_L)`
* **Unit handling:** Formula uses molar concentrations (mmol/L). If using mg/dL, the ratio remains the same, but specific log-bases may vary in literature. Stick to `mmol/L` for SSOT.
* **Evidence anchor:** Niroumand et al. (2015).
* **Existing in platform?** No.
* **Metric name:** `pulse_pressure`
* **Formula:** `systolic_bp - diastolic_bp`
* **Unit handling:** mmHg.
* **Evidence anchor:** Framingham Heart Study (Reference for arterial stiffness).
* **Existing in platform?** No.

---

### 7. Evidence-Anchored Thresholds

| Tier | Metric | Operator | Value | Unit | Evidence source | Study n | Follow-up |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **optimal** | `aip` | < | 0.11 | index | Niroumand et al. | 4,215 | N/A |
| **suboptimal** | `aip` | 0.11 – 0.21 |  | index | Niroumand et al. | 4,215 | N/A |
| **at_risk** | `aip` | > | 0.21 | index | Niroumand et al. | 4,215 | N/A |
| **optimal** | `pulse_pressure` | < | 50 | mmHg | Framingham Study | 5,000+ | 30 yrs |
| **at_risk** | `pulse_pressure` | > | 60 | mmHg | Framingham Study | 5,000+ | 30 yrs |

---

### 8. Override Rules and Guardrails

* **Rule:** `age` < 30 AND `pulse_pressure` > 60 → **at_risk**
* **Resulting state:** at_risk (Accelerated Ageing Flag)
* **Evidence basis:** Clinical definition of Early Vascular Ageing (EVA).
* **Rule:** `aip` > 0.21 AND `glucose` > 7.0 mmol/L → **at_risk** (High Priority)
* **Resulting state:** at_risk
* **Evidence basis:** Synergistic effect of glycation and atherogenic dyslipidemia on arterial wall.

---

### 9. Clinical Limitations and Excluded Populations

1. **Athletes:** High-performance athletes may have naturally high pulse pressures due to large stroke volumes (Athlete's Heart), which is not indicative of vascular ageing.
2. **Pregnancy:** Hemodynamic changes significantly alter pulse pressure and lipid profiles.
3. **Medications:** Vasodilators (ACE inhibitors, Calcium Channel Blockers) will artificially lower the "vascular age" metrics without necessarily reversing the underlying metabolic glycation.
4. **Cautionary Evidence:** Improving AIP through medication (e.g., CETP inhibitors) has historically failed to reduce hard outcomes, reinforcing that AIP is a marker of the *metabolic milieu*, not a direct therapeutic target.

---

### 10. HealthIQ Platform Signal Mapping

**Signal identifier**:

```
signal_metabolic_vascular_ageing

```

**Physiological system**:

```
vascular

```

**Primary metric**:

```
aip

```

**Required biomarkers**:

```
- triglycerides
- hdl_cholesterol
- systolic_bp
- diastolic_bp

```

**Required derived metrics**:

```
- aip
- pulse_pressure

```

**Optional biomarkers**:

```
- hb_a1c
- glucose

```

**Threshold summary**:

```
optimal:    aip < 0.11
suboptimal: aip 0.11 – 0.21
at_risk:    aip > 0.21

```

**Bundle consumers**:

```
- vascular_age
- cardiovascular_risk
- biological_age

```

**Implementation notes**:
AIP is a logarithmic scale; ensure the `log10` function is used rather than natural log (`ln`). Use `pulse_pressure` as a functional validator for the blood-based `aip`.

---

### 11. Supporting References

* **The Atherogenic Index of Plasma (AIP): A potent predictor of cardiovascular risk.** *BMC Cardiovascular Disorders*. 2015. (Key threshold source).
* **Early Vascular Ageing (EVA): Definition and Clinical Queries.** *Journal of Hypertension*. 2014. (Conceptual framework for MDVA).
* **Pulse Pressure and Risk of Cardiovascular Disease in the Framingham Study.** *Archives of Internal Medicine*. 1999. (Validation of PP as a stiffness marker).

---
