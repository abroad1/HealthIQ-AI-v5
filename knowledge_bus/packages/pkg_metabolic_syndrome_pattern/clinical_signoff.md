# Clinical Sign-off — pkg_metabolic_syndrome_pattern (KBP-0009)

## Status: PENDING ARCHITECTURE IMPLEMENTATION

The signal logic, thresholds, and component definitions are evidence-anchored and ready.
The package cannot activate until three new derived metrics are implemented AND
questionnaire SSOT is expanded. This is more complex than standard SSOT gap resolution —
it requires a new computation module.

---

## Implementation Prerequisites (Blocking — Architecture)

### 1. `mets_component_count` — New computation module required

Cannot be implemented in `ratio_registry.py` as a simple ratio formula. Requires:

**Inputs (multi-registry)**:
- Blood panel: `triglycerides`, `hdl_cholesterol`, `glucose` (mmol/L)
- Lifestyle registry: `waist_circumference_cm` (cm), `systolic_bp` (mmHg), `diastolic_bp` (mmHg)
- Questionnaire: `biological_sex`, `ethnicity`, `chronic_conditions`, `long_term_medications`

**Computation logic (pseudocode)**:
```
score = 0

# Component 1: Triglycerides
if triglycerides >= 1.7 OR fibrate_niacin_flag:
    score += 1

# Component 2: HDL
if (biological_sex == "female" AND hdl_cholesterol < 1.3) OR \
   (biological_sex == "male" AND hdl_cholesterol < 1.0) OR hdl_raising_flag:
    score += 1

# Component 3: Fasting glucose
if glucose >= 5.6 OR antidiabetic_flag OR \
   "Diabetes Type 2" in chronic_conditions OR "Diabetes Type 1" in chronic_conditions:
    score += 1

# Component 4: Blood pressure
if systolic_bp >= 130 OR diastolic_bp >= 85 OR antihypertensive_flag OR \
   "High blood pressure" in chronic_conditions:
    score += 1

# Component 5: Waist circumference (ethnic threshold lookup)
waist_threshold = lookup(ethnicity, biological_sex)  # See table below
if waist_circumference_cm >= waist_threshold:
    score += 1

return score  # integer 0–5
```

**Ethnic waist threshold lookup table**:
| Population group | Male (cm) | Female (cm) |
|-----------------|-----------|-------------|
| European / USA European-descent | ≥ 102 | ≥ 88 |
| South Asian, Chinese, Japanese, South/Central American | ≥ 90 | ≥ 80 |
| Sub-Saharan African, Eastern Mediterranean, Middle Eastern | ≥ 94 | ≥ 80 |
| Unknown / unmapped | ≥ 102 (default) | ≥ 88 (default) |

Source: Alberti et al. 2009 (harmonised guideline).

**Questionnaire controlled vocabulary requirement**:
The `ethnicity` field in questionnaire.json must use controlled vocabulary that maps
to one of the 3 IDF population groups. Free-text input requires engineering mapping logic.

### 2. `mets_bp_flag` — Binary flag, multi-input

Formula:
```
mets_bp_flag = 1 if (systolic_bp >= 130 OR diastolic_bp >= 85 OR antihypertensive_flag)
             else 0
```

Simpler than mets_component_count. Requires lifestyle_registry integration in
ratio_registry or a parallel computation module. Can serve as standalone override
indicator beyond MetS component scoring.

### 3. `mets_waist_flag` — Binary flag, ethnicity/sex lookup

Formula:
```
mets_waist_flag = 1 if waist_circumference_cm >= ethnic_sex_threshold else 0
```

Requires the same lookup table as mets_component_count above.

---

## Implementation Prerequisites (Blocking — Questionnaire SSOT)

### 4. `long_term_medications` — Expansion needed for guideline compliance

The 2009 harmonised guideline requires medication-adjusted component scoring.
Current `long_term_medications` options: None, Corticosteroids, Atypical antipsychotics,
HIV/AIDS treatments — does NOT include cardiovascular/metabolic medications.

| Missing option | Component it adjusts | Notes |
|---------------|---------------------|-------|
| Antihypertensive medication | BP component → criterion met | ACE inhibitors, ARBs, beta-blockers, CCBs, diuretics |
| Fibrate or niacin | TG component → criterion met | TG-lowering agents; niacin also raises HDL |
| Antidiabetic medication | Glucose component → criterion met | Metformin, insulin, GLP-1 agonists, SGLT2i, etc. |

**Interim mitigation**: `chronic_conditions` provides proxy signals:
- "Diabetes Type 2" or "Diabetes Type 1" → glucose component proxy (not equivalent to medication status)
- "High blood pressure" → BP component proxy (not equivalent to medication status)

The proxy approach (diagnosis → criterion met) is slightly more conservative than the
guideline (treatment → criterion met) but is clinically defensible. Label in UX as
"based on reported diagnosis" when medication status is unavailable.

---

## Resolved Decisions

### Harmonised definition vs. IDF-first definition — RESOLVED

The 2009 IDF/NHLBI/AHA harmonised definition (Alberti et al.) is used. The older IDF-first
definition required waist circumference as a mandatory criterion. The harmonised definition
allows any 3 of 5 without waist being mandatory — broader applicability. Used here.

### Suboptimal tier (2 components) — RESOLVED as HealthIQ extension

The 2009 guideline is binary (MetS present at ≥3 / absent below). The platform extends
this with a 2-component "suboptimal" tier anchored in Gami et al. 2007 intermediate CVD
risk data. UX MUST clearly label this as "pre-MetS pattern, not formal metabolic syndrome."
Engineering to add this label to the signal output for the suboptimal state.

### TG/HDL ratio canonical thresholds — RESOLVED

Source paper incorrectly equates McLaughlin 2003 (3.0 mg/dL) with Li 2008 (0.87 mmol/L).
These are different thresholds from different studies. Platform uses Li 2008 direct
mmol/L values (0.87/1.74) as they are in SSOT canonical units. McLaughlin 2003 correct
canonical equivalent is 1.31 mmol/L (not 0.87 mmol/L). Li 2008 values retained.

### `uric_acid` naming — RESOLVED

SSOT canonical name is `urate` (µmol/L). Paper uses `uric_acid` — corrected in package.

### Kahn 2005 critique acknowledged — RESOLVED as communication note

The construct of MetS is criticised (Kahn et al., Lancet 2005) for not providing superior
predictive power over individual components. The signal is retained as a pattern detection
and risk communication tool — not a diagnostic label. Clinical narrative must avoid
implying MetS diagnosis adds independent information beyond its components.

---

## Open Clinical Decisions

### 1. Sex-specific HDL thresholds — engineering implementation note

HDL component thresholds: Female < 1.3 mmol/L, Male < 1.0 mmol/L. These must be
implemented inside the `mets_component_count` computation logic (not in signal_library
thresholds). The signal_library schema does not support sex-stratified threshold values.
The derived metric itself must handle the sex-specific logic.

### 2. Partial panel — incomplete component count

If waist_circumference_cm is not available, component 4 (waist) cannot be scored.
Options:
- (a) Report component count as partial (e.g., "2 of 4 measurable components")
- (b) Suppress signal if waist unavailable
- (c) Apply conservative imputation (assume component met if other adiposity markers elevated)
Decision deferred to engineering sprint.

### 3. Older adults (>75 years) — evidence attenuation note

Evidence for MetS predicting CVD attenuates at advanced age (>75 years). Signal output
for users ≥75 should include a communication note that MetS risk associations are less
validated in this age group. Option to add age-gated confidence modifier.

### 4. Paediatric exclusion — age gate

Signal not validated for users under 18. `age < 18 → signal_suppressed` rule required.
Age derivable from `date_of_birth` in questionnaire SSOT (same pattern as egfr, fib_4).
Implement as a suppression flag in the signal evaluation context.

---

## Signal Architecture Note

The `mets_component_count` derived metric is paradigmatically different from all other
derived metrics currently in the platform. Key differences:
1. Multi-registry inputs (blood + lifestyle + questionnaire)
2. Conditional logic (sex-specific HDL, ethnicity waist lookup)
3. Integer output (count 0–5), not a continuous ratio
4. Medication override inputs modify component scores before counting

Recommended implementation path: New Python module `backend/core/analytics/mets_engine.py`
(or equivalent) separate from `ratio_registry.py`. This touches `backend/core/analytics/` —
HIGH risk under SOP §7. Requires HIGH risk work package: Claude audit + GPT architectural
review + dual approval before merge.

---

_Clinical sign-off complete. Signal architecture is evidence-locked and ready for implementation sprint once HIGH risk work package is authorised._
