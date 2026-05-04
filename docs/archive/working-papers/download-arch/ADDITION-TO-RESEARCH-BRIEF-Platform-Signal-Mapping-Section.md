## HEALTHIQ PLATFORM SIGNAL MAPPING

**MANDATORY SECTION FOR EVERY BUNDLE**

In this section you must translate the clinical research model into signals that can be consumed by the HealthIQ platform.

HealthIQ uses a layered architecture:
- **Layer A** – Biomarker ingestion (raw lab values, normalization)
- **Layer B** – Derived analytics (ratios, indices, calculations, status classification)
- **Layer C** – Insight bundles (pattern recognition, clinical interpretation)

Your task is to identify which signals from the research model map to HealthIQ platform inputs.

### SIGNAL MAPPING FORMAT (REQUIRED)

For each biological signal in your bundle, provide:

#### Biological Signal
What physiological signal does the research model detect?
(One sentence, user language)

#### Required Biomarkers (Layer A inputs)
Which raw biomarkers must be present in the blood panel?

Format:
```
- biomarker_canonical_id (unit) - Why needed in model
- biomarker_canonical_id (unit) - Why needed in model
```

#### Derived Metrics (Layer B computation)
Which ratios, indices, or calculations must be computed?

For each derived metric provide:
- **Metric name**: Standard clinical name
- **Formula**: Exact calculation (with units)
- **Evidence source**: Study validating this metric (DOI)
- **Status thresholds**: How Layer B classifies this metric
  - Example: `<8.31: "low_risk" | 8.31-8.51: "moderate_risk" | ≥8.52: "high_risk"`

#### HealthIQ Signal Output (Layer C consumption)
Define the internal platform signals that the bundle will consume.

Format:
```
Layer B signals consumed:
- derived_markers.{metric_id}.status
- biomarker_nodes.{biomarker_id}.status
- clusters.{cluster_id}.status (if applicable)

Layer C output:
- bundle_features.{bundle_id}.{signal_name}
```

### EXAMPLE: Insulin Resistance Risk Bundle

#### Biological Signal
Early detection of insulin resistance before dysglycemia appears

#### Required Biomarkers (Layer A inputs)
```
- glucose (mg/dL) - Core component of TyG index, gauges glycemic baseline
- triglycerides (mg/dL) - Core component of TyG index, reflects hepatic insulin resistance
- hba1c (%) - Glycemic guardrail to detect prediabetes/diabetes thresholds
- hdl_cholesterol (mg/dL) - Optional: enhances lipid transport assessment
```

#### Derived Metrics (Layer B computation)

**TyG Index (Triglyceride-Glucose Index)**
- **Formula**: `ln[TG (mg/dL) × FPG (mg/dL) / 2]`
- **Evidence**: Navarro-González et al. 2016 (doi:10.1016/j.ypmed.2016.01.022)
  - Prospective cohort n=4,820, 8.84 year follow-up
  - HR 6.87 for incident diabetes in normoglycemic population
- **Status thresholds**:
  - `<8.31: "low_risk"` (reference quartile)
  - `8.31-8.51: "moderate_risk"` (incident diabetes signal)
  - `≥8.52: "high_risk"` (incident metabolic syndrome threshold)

**TG/HDL Ratio (optional enhancement)**
- **Formula**: `TG (mg/dL) / HDL (mg/dL)`
- **Evidence**: McLaughlin et al. 2005 (doi:10.2337/diacare.28.7.1626)
- **Status thresholds**:
  - `<3.0: "normal" | ≥3.0: "high"`

#### HealthIQ Signal Output (Layer C consumption)
```
Layer B signals consumed:
- derived_markers.tyg_index.status ("low_risk" | "moderate_risk" | "high_risk")
- derived_markers.tyg_index.value (float, for evidence tracking)
- biomarker_nodes.hba1c.status ("normal" | "high")
- biomarker_nodes.glucose.status ("normal" | "high")
- derived_markers.tg_hdl_ratio.status (optional)

Layer C output:
- bundle_features.insulin_resistance_risk_v1.risk_tier ("optimal" | "suboptimal" | "at_risk")
- bundle_features.insulin_resistance_risk_v1.tyg_signal ("low_risk" | "moderate_risk" | "high_risk")
- bundle_features.insulin_resistance_risk_v1.glycemic_guardrail_triggered (boolean)
- bundle_features.insulin_resistance_risk_v1.confidence (0.0-1.0)
```

### CRITICAL REQUIREMENTS

1. **All derived metrics MUST be computed in Layer B**
   - Layer C bundles consume Layer B outputs only
   - No raw biomarker value calculations in Layer C

2. **Status vocabulary must be finite and explicit**
   - Define exact strings Layer B will produce
   - Layer C logic must handle all possible status values

3. **Evidence citations required for all thresholds**
   - Every status boundary must have a research citation
   - Thresholds without evidence are not acceptable

4. **Unknown/missing data handling**
   - Specify what happens if biomarkers are missing
   - Define fallback logic or "insufficient_data" states

5. **Platform contract compliance**
   - All signal IDs must follow HealthIQ naming conventions
   - Use canonical biomarker IDs (as defined in alias registry)

---

## INTEGRATION WITH BUNDLE SPECIFICATION

This Platform Signal Mapping section should appear **immediately after Section 5 (Required Biomarkers)** and **before Section 6 (Calculation Method)** in your bundle specification.

The mapping ensures:
- ✅ Research findings are directly implementable
- ✅ No ambiguity about what Layer B must compute
- ✅ Clear contract between layers
- ✅ Deterministic, testable logic