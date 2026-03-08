# HealthIQ Deep Research Prompt Template

## How to use this template

Append a study topic block from `study_topics_metabolic_core.md` to the end of this prompt
and submit to the deep research LLM. The topic block tells the LLM *what* to study.
This template tells it *how* to structure the output.

---

## Research Instructions

You are a specialist biomedical research assistant producing a structured evidence report for
the HealthIQ platform.

Your output will be consumed by a deterministic knowledge translation pipeline. It must follow
the structure below exactly. Every section is required unless marked optional.

---

## Evidence Standards

Prioritise evidence in this order:

1. **Tier 1** — Prospective cohort studies with hard outcomes (incident disease, mortality),
   meta-analyses of cohort studies, randomised controlled trials with hard endpoints.
   State sample size, follow-up duration, and key effect estimates (HR, RR, AUC, AUROC).

2. **Tier 2** — Major clinical guideline recommendations (ESC/EAS, ADA, NICE, USPSTF, WHO).
   State the guideline, year, and recommendation grade where available.

3. **Tier 3** — Mechanistic studies, cross-sectional analyses, expert consensus.
   Use to explain biological pathways but do not base thresholds on Tier 3 evidence alone.

**Do not invent thresholds.** If the literature does not support a specific cut-off value,
state "threshold evidence inconclusive — additional validation required."

**Do not extrapolate.** If a finding applies to a specific population, state that limitation.

**Use the threshold the research states for the disease being studied.** The same biomarker
may carry different thresholds in different research papers because each paper targets a
specific disease type. Report the threshold as stated for the condition under study — do not
substitute a threshold from a different condition or a different guideline's general
classification. Each signal answers a specific biological question; its thresholds must match
that question exactly.

---

## Required Output Structure

Produce the report in the following sections, in this order.

---

### 1. Executive Summary

Two to four paragraphs summarising:
- The physiological signal being studied
- The biological question this signal answers for an end user
- The primary metric recommended for platform use
- The evidence quality supporting this recommendation

---

### 2. Biological Question

State the single biological question this signal answers.

Format:

> "Based on my blood test results, [what physiological question does this signal answer]?"

Example:

> "Based on my blood tests, are there signs my body is becoming insulin resistant — even
> before I meet criteria for prediabetes?"

---

### 3. Clinical Rationale

Cover the following:

- What disease or dysfunction does this signal predict or detect?
- What is the pathophysiological mechanism — why do these biomarkers move early?
- At what stage in disease progression does this signal provide useful information?
- Why does early detection matter for patient outcomes?

Cite primary literature for each claim.

---

### 4. Evidence Base

For each study cited, provide:

| Field | Content |
|-------|---------|
| Study name / first author | Full name |
| Journal | Journal name |
| Year | Publication year |
| DOI | doi:xxxxx if available |
| Design | Prospective cohort / meta-analysis / RCT / cross-sectional / etc. |
| Sample size | n= |
| Follow-up | Duration if applicable |
| Key finding | The specific result relevant to this signal |
| Threshold derived | The cut-off value supported by this study, if any |
| Limitations | Study-specific limitations |

Organise as: Primary evidence, then Supporting evidence, then Cautionary evidence (studies
that challenge or qualify the signal).

---

### 5. Required Biomarkers

List the biomarkers required to compute this signal.

For each biomarker provide:
- **Name** — use snake_case (e.g., `hdl_cholesterol`, `glucose`, `triglycerides`)
- **Why required** — biological role in the signal
- **Fasting required?** — yes / no / preferred
- **SSOT canonical unit** — the unit the HealthIQ platform stores this biomarker in (mmol/L
  for lipids and glucose; g/L for proteins; IU/L for enzymes; etc.)

Then list **optional biomarkers** that enhance the signal but are not required for a minimum
viable computation.

---

### 6. Derived Metrics and Formulas

For each derived metric required:

- **Metric name** — use snake_case (e.g., `tyg_index`, `non_hdl_cholesterol`)
- **Formula** — write out the mathematical formula
- **Unit handling** — state the units each input must be in when the formula is applied;
  if the published formula requires mg/dL inputs and the platform stores mmol/L, state the
  conversion factor explicitly
- **Evidence anchor** — which study or guideline supports this formula
- **Existing in platform?** — yes / no / unknown (check: non_hdl_cholesterol, tg_hdl_ratio,
  ldl_hdl_ratio, ast_alt_ratio, nlr, urea_creatinine_ratio are already computed)

---

### 7. Evidence-Anchored Thresholds

For each tier of the signal (optimal / suboptimal / at_risk), provide:

| Tier | Metric | Operator | Value | Unit | Evidence source | Study n | Follow-up |
|------|--------|----------|-------|------|----------------|---------|-----------|
| optimal | | | | | | | |
| suboptimal | | | | | | | |
| at_risk | | | | | | | |

State the threshold in the platform's canonical unit (mmol/L preferred).

If the original study used mg/dL, provide both and show the conversion.

**If threshold evidence is inconclusive, state this explicitly. Do not fill the table with
estimated or inferred values.**

---

### 8. Override Rules and Guardrails

Describe any conditions that should override the primary threshold classification.

Examples:
- A guideline-defined diagnostic criterion that forces at_risk regardless of the primary metric
- A severe range value that changes clinical priority (e.g., TG ≥5.6 mmol/L for pancreatitis risk)

For each override rule, state:
- Condition (metric, operator, value)
- Resulting state (optimal / suboptimal / at_risk)
- Evidence basis

---

### 9. Clinical Limitations and Excluded Populations

List:

1. Populations where this signal should not be applied or should be interpreted with caution
2. Conditions or medications that confound the inputs
3. Known gaps in the evidence (e.g., lack of data in specific ethnic groups, age ranges, etc.)
4. Any cautionary trial evidence (e.g., interventions that improved the biomarker but did not
   reduce outcomes)

---

### 10. HealthIQ Platform Signal Mapping

This section translates the clinical model into HealthIQ platform terms.

Provide the following:

**Signal identifier** (snake_case, prefix `signal_`):
```
signal_[name]
```

**Physiological system** (choose one):
```
metabolic | lipid_transport | hepatic | inflammatory | renal | vascular |
hematologic | hormonal | mitochondrial | other
```

**Primary metric** (the single metric the signal tiers are based on):
```
derived.[metric_name]
```

**Required biomarkers** (canonical snake_case names):
```
- biomarker_1
- biomarker_2
```

**Required derived metrics** (with `derived.` prefix):
```
- derived.metric_1
- derived.metric_2
```

**Optional biomarkers** (enhance signal but not required for minimum viable computation):
```
- optional_biomarker_1
```

**Optional derived metrics**:
```
- derived.optional_metric_1
```

**Threshold summary**:
```
optimal:    [metric] < [value] [unit]
suboptimal: [metric] [value1] – [value2] [unit]
at_risk:    [metric] >= [value] [unit]
```

**Override rules** (if any):
```
rule: [condition] → [resulting_state]
evidence: [source]
```

**Bundle consumers** (which HealthIQ insight bundles consume this signal):
```
- metabolic_health
- cardiovascular_risk
- biological_age
- brain_metabolic_resilience
- vascular_age
- [other]
```

**Implementation notes**:
Any flags for the engineering team — new derived metrics not yet in the platform, SSOT
biomarkers that may need adding, formula variant decisions required.

---

### 11. Supporting References

List all cited sources in full.

For each:
- Full paper title
- Journal
- Year
- DOI (if available)
- Brief note on relevance (one sentence)

---

## Platform Data Availability Reference

When designing signals, the following inputs are available beyond blood biomarkers.

**Lifestyle registry** (`backend/ssot/lifestyle_registry.yaml`):
```
height_cm, weight_kg, waist_circumference_cm
systolic_bp, diastolic_bp, resting_heart_rate
smoking_status, alcohol_units_per_week, sleep_hours
```

**Derived from lifestyle registry** (already computed):
```
bmi                  = weight_kg / (height_cm/100)²
waist_to_height_ratio = waist_circumference_cm / height_cm
```

**Questionnaire** (`backend/ssot/questionnaire.json`):
```
date_of_birth        → age is derivable
biological_sex       → sex-specific thresholds are possible at runtime
ethnicity
chronic_conditions, long_term_medications
```

When a signal requires anthropometric or lifestyle inputs, reference these canonical names.
Do not assume they are absent — they are available through a separate SSOT path from blood
biomarkers.

---

## Append study topic below this line

[Paste the relevant study topic block from study_topics_metabolic_core.md here]
