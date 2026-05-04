# HealthIQ AI — Insight Specification (Developer Hand-off)

Scope: implementation-ready specification for the 3 headline insights, 7 supporting insights, and QRISK3. Includes inputs, derived values, required questionnaire fields, decision rules at a high level, DTO contracts, confidence logic, and test cases. All thresholds are **lab-first**; do not hard-code “global” ranges except where noted for derived ratios.

---

## Global conventions

* **Lab-first ranges:** Always use ranges from the user’s lab report for min/max and flagging.
* **Units:** Canonicalise to SI units in the pipeline before scoring.
* **Missing data:** Never block an insight unless core inputs are missing; degrade confidence instead.
* **LLM boundary:** Engines calculate; LLM narrates only.
* **Severity levels:** `normal | borderline | high | very_high | low | very_low`.
* **Confidence:** `0–1` float; composition described per insight.
* **DTO keys:** snake_case for backend; frontend mapping handled separately.

### Common derived values

| Name                    | Formula (canonical units)                  | Notes                         |
| ----------------------- | ------------------------------------------ | ----------------------------- |
| `tg_hdl_ratio`          | triglycerides / HDL-C                      | mmol/L ÷ mmol/L               |
| `tc_hdl_ratio`          | total_cholesterol / HDL-C                  | mmol/L ÷ mmol/L               |
| `homa_ir`               | (fasting_glucose * fasting_insulin) / 22.5 | glucose mmol/L; insulin mIU/L |
| `alt_ast_ratio`         | ALT / AST                                  | unitless                      |
| `urea_creatinine_ratio` | urea / creatinine                          | use SI; report unitless       |
| `nlr`                   | neutrophils / lymphocytes                  | dimensionless                 |
| `non_hdl_cholesterol`   | total_cholesterol − HDL-C                  | mmol/L                        |

---

## DTO contracts (applies to all insights)

```json
{
  "insight_id": "string",                 // e.g. "metabolic_age"
  "title": "string",
  "score": {                              // optional for some insights
    "value": 0.0,                         // 0–100 where applicable
    "severity": "normal|borderline|high|very_high|low|very_low"
  },
  "drivers": [                            // ranked contributors
    {"name": "string", "direction": "high|low", "weight": 0.0}
  ],
  "components": [                         // normalised sub-scores if relevant
    {"id": "string", "label": "string", "value": 0.0}
  ],
  "biomarkers_used": ["canonical_biomarker_id"],
  "derived_used": ["tg_hdl_ratio", "homa_ir"],
  "questionnaire_used": ["field_key"],
  "confidence": 0.0,                      // 0–1
  "flags": [ {"code":"string","level":"info|warn|critical","message":"string"} ],
  "recommendations_ref": ["id"],          // keys into recs library
  "narrative_inputs": {                   // structured bundle for LLM
    "key": "value"
  }
}
```

---

## Questionnaire schema (shared)

Collect once and reuse:

```json
{
  "age": 58,
  "sex": "male|female",
  "ethnicity": "standardised_coding",
  "height_cm": 178,
  "weight_kg": 84,
  "waist_cm": 96,
  "alcohol_units_per_week": 18,
  "smoking_status": "never|former|current",
  "exercise_level": "low|moderate|high",
  "sleep_hours": 7,
  "stress_level": "low|moderate|high",
  "medications": ["statin","steroids", "thyroxine"],
  "family_history_premature_chd": true,
  "diagnoses": ["type2_diabetes","ckd","af","ra","smi","migraine"],
  "postcode": "SW1A 1AA"                  // for deprivation index if enabled
}
```

---

# Headline insights (3)

## 1) Metabolic Age

**Purpose:** Estimate “metabolic age” proxy from insulin/glycaemic control, lipid interaction, and hepatic strain.

**Inputs**

* Biomarkers (core): `fasting_glucose`, `hba1c`, `fasting_insulin`, `triglycerides`, `hdl_c`, `alt`.
* Helpful: `ast`, `urate`.
* Derived: `homa_ir`, `tg_hdl_ratio`.
* Questionnaire: `age`, `sex`, `waist_cm`, `alcohol_units_per_week`, `exercise_level`.

**Logic (outline)**

1. Compute `homa_ir` and `tg_hdl_ratio`.
2. Score sub-domains 0–100:

   * Glycaemic control: `hba1c`, `fasting_glucose`, `homa_ir`.
   * Lipid interaction: `tg_hdl_ratio`.
   * Hepatic load: `alt` (± `alt_ast_ratio`).
3. Weighted composite → **metabolic age delta** (years):

   * Positive delta = metabolism “older” than chronological.
   * Clamp ±20y for UX.
4. Severity bands by delta:

   * `≤−5`: very_low (youthful), `−5..+5`: normal, `+5..+10`: borderline, `>+10`: high.

**Confidence**

* Start at 1.0; subtract 0.2 for each missing core domain (glycaemic, lipid, hepatic), min 0.2.

**DTO special fields**

* `score.value`: scaled 0–100 from delta (map −20..+20 to 100..0).
* `narrative_inputs`: deltas, domain scores, lifestyle modifiers.

**Tests**

* All-normal panel → delta ≈ 0, severity normal.
* High insulin + high TG/low HDL + raised ALT → delta > +10.
* Missing insulin → compute without `homa_ir`, confidence ≤ 0.8.

---

## 2) Cardiovascular / Heart

**Purpose:** Cardiometabolic resilience based on lipids and inflammatory context.

**Inputs**

* Core biomarkers: `total_cholesterol`, `ldl_c`, `hdl_c`, `triglycerides`, `hs_crp`.
* Derived: `tc_hdl_ratio`, `tg_hdl_ratio`, `non_hdl_cholesterol`.
* Questionnaire: `age`, `sex`, `exercise_level`, `smoking_status`, `medications` (statin).

**Logic (outline)**

1. Lipid quality sub-score from `tc_hdl_ratio`, `tg_hdl_ratio`, `non_hdl_cholesterol`.
2. Inflammation penalty from `hs_crp` banding (low-grade ≥3 mg/L).
3. Optional adjustment if `statin` present (mark as medication context; do not “normalise”).
4. Composite 0–100; higher is better.

**Confidence**

* Missing CRP → −0.1; missing HDL or TG → −0.2 each; min 0.4.

**DTO**

* `components`: `lipids`, `inflammation`.
* `drivers`: e.g., `{"name":"tg_hdl_ratio","direction":"high","weight":0.3}`.

**Tests**

* High TG:HDL and high CRP → low resilience (≤40).
* Ideal lipids, low CRP → ≥80.

---

## 3) Inflammation

**Purpose:** Identify systemic inflammatory load and pattern tendency.

**Inputs**

* Core biomarkers: `hs_crp` (or `crp`), `neutrophils`, `lymphocytes`, `ferritin`, `albumin`.
* Derived: `nlr`.
* Helpful: `wbc`, `alt`, `ggt`, `vitamin_d`.

**Logic (outline)**

1. Base from `hs_crp` band.
2. Immune tone from `nlr` (1–3 normal; >5 abnormal).
3. Ferritin/albumin interaction (high ferritin with normal CRP → iron overload tendency flag; high ferritin + high CRP → acute-phase).
4. Composite severity.

**Confidence**

* Missing CRP or differential → −0.2 each; min 0.4.

**DTO**

* `flags`: `FERRITIN_ACUTE_PHASE`, `LOW_ALBUMIN_INFLAMMATORY_PATTERN`.

**Tests**

* CRP 0.5 mg/L + NLR 2.0 → normal.
* CRP 5 mg/L + NLR 4.5 + low albumin → high.

---

# Supporting insights (7)

## 4) Fatigue Root Cause

**Purpose:** Attribute low energy to physiological drivers.

**Inputs**

* Iron/oxygen: `haemoglobin`, `ferritin`, `serum_iron`, `transferrin_saturation`, `tibc`.
* Methylation: `vitamin_b12`, `folate`, `mcv`.
* Thyroid: `tsh`, `free_t4`, `free_t3`.
* Inflammatory: `crp/hs_crp`, `nlr`, `albumin`.
* Metabolic: `hba1c`, `fasting_glucose`, `triglycerides`, `alt`.
* Helpful: `vitamin_d`, `magnesium`, morning `cortisol`.
* Questionnaire: `sleep_hours`, `stress_level`, `exercise_level`, `alcohol_units_per_week`, `diagnoses` (depression, etc.).

**Logic**

* Produce per-cluster flags (true/false + severity):
  `iron_oxygen`, `methylation`, `thyroid_drag`, `inflammatory_fatigue`, `metabolic_inflexibility`, `lifestyle_sleep_stress`.
* Rank top two drivers by evidence score.

**Confidence**

* Weighted by number of contributing abnormal markers; min 0.3 if only lifestyle present.

**DTO**

* `components`: list of cluster evidence scores (0–1).
* `drivers`: ranked.

**Tests**

* Low ferritin + low Hb → iron driver top.
* TSH high-normal + low-normal fT3 → thyroid_drag present.

---

## 5) Detox & Filtration (Liver + Kidney)

**Purpose:** Detect hepatic strain and kidney filtration issues.

**Inputs**

* Liver: `alt`, `ast`, `ggt`, `alp`, `bilirubin`, `albumin` (± `inr` if present).
* Kidney: `creatinine`, `egfr`, `urea`, `sodium`, `potassium`, `bicarbonate`, `chloride`.
* Derived: `alt_ast_ratio`, `urea_creatinine_ratio`.
* Helpful: urine `acr`.
* Questionnaire: `alcohol_units_per_week`, `medications` (e.g., paracetamol, statins), `exercise_level` (for transient ALT).

**Logic**

* Compute liver sub-score (ALT-weighted; AST pattern with ratio; GGT as load).
* Compute kidney sub-score (eGFR band; urea:creatinine dehydration signal).
* Composite; independent flags per organ.

**Confidence**

* Penalise missing ALT or eGFR (−0.3 each).

**DTO**

* `components`: `liver`, `kidney`.
* `flags`: `DEHYDRATION_PATTERN`, `HEPATIC_LOAD_ALCOHOL_SUSPECTED` (if alcohol high + GGT raised).

**Tests**

* Raised GGT + ALT → hepatic load high.
* Low eGFR → kidney severity high irrespective of liver normal.

---

## 6) Thyroid Regulation

**Purpose:** Hypothyroid trend, conversion issues, or euthyroid.

**Inputs**

* Core: `tsh`, `free_t4`, `free_t3`.
* Helpful: `reverse_t3`, `anti_tpo`, `anti_tg`, `ferritin`, `b12`, `sodium`.
* Questionnaire: `sex`, `age`, `medications` (thyroxine), symptoms (optional later).

**Logic**

* Classify:

  * **Primary hypothyroid trend:** `tsh` elevated vs lab ref ± low `free_t4`.
  * **Conversion issue:** `tsh` normal/mildly high, `free_t4` normal, `free_t3` low-normal.
  * **Autoimmune suspicion:** antibodies high.
* Severity from distance to lab limits.

**Confidence**

* Full with TSH+fT4+fT3; −0.3 if any missing.

**DTO**

* `flags`: `AUTOIMMUNE_THYROID_SUSPECTED`, `CONVERSION_DRAG`.

**Tests**

* TSH 5.0 with low fT4 → primary hypothyroid pattern.
* TSH 2.8, normal fT4, low fT3 → conversion.

---

## 7) Nutritional Sufficiency

**Purpose:** Identify key nutrient deficits impacting systems.

**Inputs**

* Core: `vitamin_d`, `ferritin` (+ iron studies), `vitamin_b12`, `folate`.
* Helpful: `magnesium`, `zinc`, `calcium`, `albumin`.
* Questionnaire: diet patterns (optional next phase).

**Logic**

* Per-nutrient status vs lab range; co-interpret ferritin with CRP if available.
* Rank top 1–3 deficits.

**Confidence**

* Based on count of nutrients tested.

**DTO**

* `components`: entries per nutrient with `status`.

**Tests**

* Low vitamin D alone → single deficit; ferritin high with high CRP → do not conclude iron overload.

---

## 8) Metabolic Instability Pattern (pre-diabetes early warning)

**Purpose:** Early risk for metabolic syndrome/insulin resistance.

**Inputs**

* Core: `fasting_insulin`, `fasting_glucose`, `hba1c`, `triglycerides`, `hdl_c`, `alt`.
* Helpful: `urate`.
* Derived: `homa_ir`, `tg_hdl_ratio`.
* Questionnaire: `waist_cm`, `exercise_level`.

**Logic**

* Evidence scoring from `homa_ir`, `tg_hdl_ratio`, `alt`, `waist_cm`.
* Pattern present if ≥2 strong signals.

**Confidence**

* High if insulin + TG/HDL present; else moderate.

**DTO**

* `flags`: `INSULIN_RESISTANCE_PATTERN`.

**Tests**

* HOMA-IR high + TG/HDL > 2.5 → pattern positive.

---

## 9) Silent Inflammation Load

**Purpose:** Low-grade chronic inflammation signature.

**Inputs**

* Core: `hs_crp`, `neutrophils`, `lymphocytes`, `ferritin`, `albumin`.
* Derived: `nlr`.
* Helpful: `alt`, `ggt`, `esr`.

**Logic**

* Composite from CRP band + NLR + low albumin; ferritin interaction as above.

**Confidence**

* Penalise if CRP or differential missing.

**DTO**

* As per Inflammation, with `signature:true`.

**Tests**

* CRP 2–5 + NLR 3–5 + low-normal albumin → signature present.

---

# Additional insight

## 10) QRISK3 — 10-year cardiovascular event probability

**Purpose:** Deterministic replication of QRISK3 to estimate 10-year risk.

**Inputs**

* Biomarkers: `total_cholesterol`, `hdl_c`, `systolic_bp`.
* Questionnaire/record: `age`, `sex`, `ethnicity`, `smoking_status`, `bmi`, `type1_or_type2_diabetes`, `ckd`, `af`, `ra`, `corticosteroid_use`, `severe_mental_illness`, `migraine`, `family_history_premature_chd`, `postcode` (deprivation index) and medications (antihypertensives).

**Logic**

* Implement published QRISK3 equations (sex-specific, with interaction terms).
* Output absolute risk `%` with banding: `<5% low`, `5–10% moderate`, `>10% high` (UK conventions).

**Confidence**

* 1.0 if all mandatory fields present; else do not compute (return `not_applicable` with a structured `missing_inputs` list).

**DTO (specific)**

```json
{
  "insight_id": "qrisk3",
  "title": "10-year Cardiovascular Event Risk",
  "risk_percent": 7.8,
  "risk_band": "moderate",
  "inputs_present": ["age","sex","tc","hdl","sbp","smoking_status", "..."],
  "missing_inputs": [],
  "confidence": 1.0,
  "biomarkers_used": ["total_cholesterol","hdl_c","systolic_bp"],
  "questionnaire_used": ["age","sex","ethnicity","bmi","smoking_status","..."],
  "flags": [],
  "narrative_inputs": { "comparators": { "population_band":"moderate" } }
}
```

**Tests**

* Known QRISK3 sample cases to validate parity (golden tests).
* Missing SBP → return `not_applicable`, no risk computed.

---

# Confidence & completeness model (shared helper)

```python
def completeness_confidence(required_sets: list[list[str]], present: set[str]) -> float:
    """
    required_sets: list of logical groups (e.g., ["hba1c","glucose"], ["hdl_c","triglycerides"])
    present: set of available inputs (biomarkers + questionnaire keys)
    Returns: confidence in 0..1, starting at 1.0 and penalising each missing group by equal weight.
    """
```

Use per insight to ensure consistent degradation.

---

# LLM narrative hand-off (shared)

**Input to LLM:** strictly the `narrative_inputs` plus a small, fixed context:

* Insight name
* Severity band(s)
* Top drivers
* Confidence statement
* Non-diagnostic language requirement

**Validation:** Pydantic schema ensuring:

* No thresholds invented
* No diagnoses
* All numbers exist in engine outputs

---

# Frontend presentation requirements (per insight card)

* Title, severity or risk band, numeric score/value if applicable.
* Top 2–3 drivers with small chips (↑ or ↓).
* Confidence chip (e.g., High / Medium / Low).
* “What this means” (LLM narrative).
* “Next steps” (recommendation keys).

---

# Minimum test set (per insight)

1. **Happy path**: all inputs present, returns stable score/band.
2. **Partial data**: one domain missing, returns degraded confidence but valid output.
3. **Edge values**: near lab cut-offs to verify banding.
4. **Invalid input**: wrong units rejected by earlier pipeline; here, ensure safe handling if surfaced.
5. **Snapshot**: DTO shape stable across runs (no key drift).

---

# Implementation notes

* Engines register via a simple registry (string `insight_id` → callable).
* Each engine exposes `required_inputs()`, `optional_inputs()`, `compute(payload) -> dto`.
* Ratios pre-computed by a `derived_values` stage; engines do not re-implement formulas.
* Confidence helper shared.
* Recommendations selected by deterministic mapping from drivers/severity to a library key (no generation).

---

# Deliverables for the team

1. Implement each engine per the above (inputs, logic outline, DTO).
2. Add unit tests and golden tests (QRISK3).
3. Wire into orchestrator (execute engines with available data; collate DTOs).
4. Map DTOs to frontend cards.
5. Validate LLM narratives against schema.

This document is sufficient to begin implementation.
