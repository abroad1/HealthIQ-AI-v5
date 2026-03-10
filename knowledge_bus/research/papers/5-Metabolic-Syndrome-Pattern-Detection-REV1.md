# 5 — Metabolic Syndrome Pattern Detection — REV1

**REV1 Status: CANONICAL REVIEW COMPLETE**
All naming corrections, unit resolution decisions, and architecture gaps documented below.
Package-ready for KBP-0009 (pkg_metabolic_syndrome_pattern).

Source document: `knowledge_bus/research/papers/5-Metabolic-Syndrome-Pattern-Detection.md`

---

## CANONICAL RESOLUTIONS

### 1. `uric_acid` → `urate` (SSOT canonical name)

Paper uses `uric_acid` (optional biomarker). SSOT canonical name is `urate` (unit: µmol/L).
Corrected in package.

### 2. tg_hdl_ratio mmol/L equivalence — DISCREPANCY FLAGGED

Paper states: "TG/HDL ≥3.0 mg/dL ≡ ≥0.87 mmol/L (equivalent)"

**This conversion is mathematically incorrect.**
| Metric | Conversion factor | Result |
|--------|-----------------|--------|
| TG/HDL ratio unit conversion | × (38.67 / 88.57) = × 0.437 | 3.0 mg/dL ratio → 1.31 mmol/L ratio |

The correct mmol/L equivalent of 3.0 mg/dL is **1.31 mmol/L**, NOT 0.87 mmol/L.

**Resolution**: 0.87 mmol/L is the DIRECT threshold from Li et al. 2008 (NHANES, SI units),
not a conversion from McLaughlin 2003. These are two different thresholds from two different
studies — Li 2008 reports mmol/L directly; McLaughlin 2003 reports in mg/dL. They are NOT
equivalent. This is an error in the source document.

**Canonical values retained for package (from Li 2008, direct mmol/L)**:
| State | Threshold |
|-------|-----------|
| Optimal | < 0.87 mmol/L ratio |
| Suboptimal | 0.87 – 1.74 mmol/L ratio |
| At risk | ≥ 1.74 mmol/L ratio |

**McLaughlin 2003 canonical value** (for reference, NOT used as package threshold):
TG/HDL ≥ 3.0 mg/dL = ≥ 1.31 mmol/L ratio (correct conversion).

Note: These thresholds are SUPPORTING SUB-SIGNAL values only. The primary signal tier
is `mets_component_count`. The tg_hdl_ratio thresholds follow Translation Rule 2
(threshold belongs to the signal) — different values than other KBP packages using
tg_hdl_ratio are valid.

### 3. Biomarkers confirmed in SSOT

| Biomarker | SSOT status | Unit |
|-----------|------------|------|
| `triglycerides` | ✓ | mmol/L |
| `hdl_cholesterol` | ✓ | mmol/L |
| `glucose` | ✓ | mmol/L |
| `insulin` | ✓ | pmol/L |
| `hba1c` | ✓ | mmol/mol |
| `crp` | ✓ (aliases: hs_crp) | mg/L |
| `alt` | ✓ | IU/L |
| `urate` | ✓ (NOT `uric_acid`) | µmol/L |

### 4. Lifestyle and questionnaire inputs — confirmed

| Input | Registry | Status |
|-------|---------|--------|
| `waist_circumference_cm` | lifestyle_registry | ✓ |
| `systolic_bp` | lifestyle_registry | ✓ |
| `diastolic_bp` | lifestyle_registry | ✓ |
| `biological_sex` | questionnaire | ✓ |
| `ethnicity` | questionnaire | ✓ |
| `chronic_conditions` | questionnaire | ✓ (includes Diabetes Type 2, High blood pressure) |
| `antihypertensive_medication` | questionnaire | ✗ NOT in long_term_medications — SSOT gap |
| `fibrate_or_niacin` | questionnaire | ✗ NOT in long_term_medications — SSOT gap |
| `antidiabetic_medication` | questionnaire | ✗ NOT in long_term_medications — SSOT gap |

### 5. Component criteria — canonical units confirmed

All thresholds already in platform canonical units:
| Component | Criterion | Canonical value |
|-----------|-----------|----------------|
| Triglycerides | ≥ 1.7 mmol/L | ✓ (paper uses mmol/L) |
| Glucose | ≥ 5.6 mmol/L | ✓ (paper uses mmol/L) |
| Systolic BP | ≥ 130 mmHg | ✓ |
| Diastolic BP | ≥ 85 mmHg | ✓ |
| HDL — Female | < 1.3 mmol/L | ✓ |
| HDL — Male | < 1.0 mmol/L | ✓ |
| Waist — European Male | ≥ 102 cm | ✓ |
| Waist — European Female | ≥ 88 cm | ✓ |
| Waist — South/East Asian, SA, CA Male | ≥ 90 cm | ✓ |
| Waist — South/East Asian, SA, CA Female | ≥ 80 cm | ✓ |
| Waist — Sub-Saharan/Eastern Med/Middle East Male | ≥ 94 cm | ✓ |
| Waist — Sub-Saharan/Eastern Med/Middle East Female | ≥ 80 cm | ✓ |

---

## ARCHITECTURE GAPS (blocking implementation)

### A. `mets_component_count` — requires new computation module

Not expressible as a simple ratio in `ratio_registry.py`. Requires:
- Multi-registry inputs: blood panel (TG, HDL, glucose) + lifestyle_registry (waist_cm, BP) + questionnaire (sex, ethnicity, medication flags)
- Sex-specific HDL threshold lookup
- Ethnicity-specific waist circumference lookup table (6 population groups × 2 sexes = 12 thresholds)
- Medication flag overrides (antihypertensive, fibrate/niacin, antidiabetic — if component SSOT gap is resolved)
- Integer output (0–5)

This is a HIGH-complexity derived metric requiring a new computation module. Cannot be added to ratio_registry.py without significant refactoring. Flagged for engineering sprint.

### B. `mets_bp_flag` — binary flag, multi-input

`(systolic_bp ≥ 130 OR diastolic_bp ≥ 85 OR antihypertensive_medication = true) → 1, else 0`

Simpler than mets_component_count but still multi-registry. Could be added to ratio_registry as a binary derived metric using lifestyle_registry inputs once that pattern is supported.

### C. `mets_waist_flag` — ethnicity/sex lookup

`waist_circumference_cm ≥ ethnicity_sex_threshold → 1, else 0`

Requires lookup table as a platform asset. Controlled vocabulary for `ethnicity` questionnaire field needed to map free-text responses to IDF categories.

### D. `activation_logic: "component_count"` — schema gap

The `deterministic_threshold` activation logic is not suitable for a component-count signal.
The signal tier is derived from the integer value of `mets_component_count` (≤1 / =2 / ≥3).
Once `mets_component_count` is implemented as a derived metric, the threshold comparison
itself IS expressible in the current schema (the signal simply compares an integer to threshold
values). The `deterministic_threshold` activation logic can be used — the architecture gap
is in computing `mets_component_count`, not in evaluating its threshold.

---

## QUESTIONNAIRE SSOT GAPS

| Missing field | Notes |
|--------------|-------|
| `antihypertensive_medication` (boolean) | Needed for guideline-compliant BP component scoring. Partial proxy: `chronic_conditions` includes "High blood pressure" but does not confirm whether medicated. |
| `fibrate_or_niacin` (boolean) | Needed for TG component scoring. Not in long_term_medications. |
| `antidiabetic_medication` (boolean) | Needed for glucose component scoring. Partial proxy: chronic_conditions includes Diabetes Type 1/2 but does not confirm medication status. |

Interim mitigation: `chronic_conditions` proxies are available for type_2_diabetes and
hypertension diagnosis (but not medication status). Implementation note: the 2009 guideline
requires treatment status — not just diagnosis — for components. The proxy approach
(diagnosis → component met) is slightly more conservative than the guideline (medication →
component met) but is clinically defensible.

---

## SIGNAL DEFINITION CONFIRMED

**Signal ID**: `signal_metabolic_syndrome_pattern`
**System**: `metabolic`
**Primary metric**: `mets_component_count` (integer 0–5; ARCHITECTURE GAP — see above)

### Signal tiers

| Tier | Threshold | Evidence |
|------|-----------|---------|
| Optimal | mets_component_count ≤ 1 | Mottillo 2010 (baseline CVD risk reference) |
| Suboptimal | mets_component_count = 2 | Gami 2007 (intermediate CVD risk, 2-component) |
| At risk | mets_component_count ≥ 3 | Alberti 2009; Mottillo 2010; Lorenzo 2003 |

Note: the suboptimal tier (2 components) is a HealthIQ-specific extension to the
harmonised guideline (which is binary: MetS present at ≥3 or absent). Anchored in
Gami 2007 showing intermediate CVD risk elevation with 2 components. UX must
clearly label this as "pre-MetS pattern, not formal metabolic syndrome."

### TG/HDL ratio supporting thresholds (Li 2008, direct mmol/L)

| Tier | Threshold | Unit |
|------|-----------|------|
| Optimal | < 0.87 | mmol/L ratio |
| Suboptimal | 0.87 – 1.74 | mmol/L ratio |
| At risk | ≥ 1.74 | mmol/L ratio |

These thresholds are from Li 2008 (NHANES, SI units). McLaughlin 2003 3.0 mg/dL =
1.31 mmol/L (correct conversion) is a DIFFERENT study threshold; the paper's "equivalence"
claim is incorrect. Li 2008 values used as they are in mmol/L and directly applicable.

---

_REV1 completed 2026-03-10. Package KBP-0009 ready for creation._
