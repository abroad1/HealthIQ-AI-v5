# 6 — Mitochondrial Energy Efficiency & Metabolic Flexibility — REV1

**REV1 Status: CANONICAL REVIEW COMPLETE**
All unit conversions, naming corrections, and schema decisions resolved below.
Package-ready for KBP-0008 (pkg_mitochondrial_efficiency).

Source document: `knowledge_bus/research/papers/6-Mitochondrial-Energy-Efficiency-Metabolic Flexibility.md`

---

## CANONICAL RESOLUTIONS

### 1. `hb_a1c` → `hba1c` (SSOT canonical name)

Paper uses `hb_a1c` in the diabetes override rule. SSOT canonical name is `hba1c`.
Corrected throughout.

### 2. tyg_index — platform status correction

Paper Section 6 states "Existing in platform? No". This is incorrect.
`tyg_index` IS in the platform via `ratio_registry.py` (DERIVED_IDS, line 30).
Platform formula: `ln((tg_mmol_l × glucose_mmol_l × 1596.0) / 2.0)` where
1596.0 = 88.5714 × 18.018 (SI-to-mg/dL conversion constants). This is identical
to the paper formula `ln((TG_mg/dL × glucose_mg/dL) / 2)`. No new implementation needed.

Threshold values (4.49 optimal / 4.68 at_risk) are in the same log-scale units as
the platform formula. No unit conversion required.

### 3. tg_hdl_ratio — platform formula and canonical unit clarification

Paper formula: `(triglycerides × 88.57) / (hdl_cholesterol × 38.67)` → mg/dL ratio.
Platform implementation (`ratio_registry.py`): `safe_ratio(tg, hdl)` = tg_mmol_l / hdl_mmol_l → mmol/L ratio.

Paper Section 7 thresholds for tg_hdl_ratio (M: < 3.5, F: < 2.5 mg/dL ratio) require conversion:
| Paper (mg/dL ratio) | Platform canonical (mmol/L ratio) | Derivation |
|---------------------|----------------------------------|------------|
| < 3.5 (Male optimal) | < 1.53 | 3.5 × (38.67 / 88.57) = 3.5 × 0.4367 |
| < 2.5 (Female optimal) | < 1.09 | 2.5 × 0.4367 |

**Signal implementation decision**: tg_hdl_ratio is listed as a REQUIRED DERIVED METRIC in
the Section 10 signal mapping but does NOT appear in the threshold summary. Its thresholds
(Section 7) are sex-stratified and the current signal_library schema has no sex-stratified
threshold support. The sex-specific tg_hdl_ratio thresholds are therefore NOT encoded in
the signal_library — tg_hdl_ratio is a supporting/display metric only. The schema gap is
noted in clinical_signoff.md.

### 4. lactate thresholds — no unit conversion needed

Paper thresholds are in mmol/L. SSOT will hold lactate in mmol/L. No conversion required.
| State | Threshold |
|-------|-----------|
| Optimal | < 1.0 mmol/L |
| Suboptimal | 1.0 – 2.0 mmol/L |
| At risk | ≥ 2.1 mmol/L |
| Critical override | ≥ 4.0 mmol/L (severe hyperlactatemia) |

### 5. Metformin threshold adjustment — deferred

Paper Section 8 describes a Metformin correction: lactate thresholds shift to
< 1.3 (optimal) / ≥ 2.4 (at_risk) in patients on Metformin. This is a
threshold-adjustment pattern (not a state-forcing override) that does not fit
the current signal_library override_rules schema. Deferred to future enhancement.
Tracked in clinical_signoff.md. Requires `long_term_medications` from questionnaire SSOT.

### 6. Override rule evidence citation — correction

Section 10 override rule for glucose override lists `evidence: ` (empty). Corrected to
reference ADA Standards of Care in Diabetes 2026 (reference [33] in paper).

### 7. SSOT gaps identified

| Biomarker | Unit | Notes |
|-----------|------|-------|
| `lactate` | mmol/L | BLOCKING — required biomarker for signal_mitochondrial_efficiency |
| `acetylcarnitine_c2` | µmol/L | Optional — acylcarnitine panel not in SSOT |
| `tetradecanoylcarnitine_c14` | µmol/L | Optional — acylcarnitine panel not in SSOT |

---

## SIGNAL DEFINITION (CANONICAL)

**Signal ID**: `signal_mitochondrial_efficiency`
**System**: `mitochondrial`
**Primary metric**: `tyg_index`
**Supporting metric**: `lactate`

### Primary thresholds

| Metric | Optimal | Suboptimal | At risk |
|--------|---------|-----------|---------|
| `tyg_index` | < 4.49 | 4.49 – 4.68 | > 4.68 |
| `lactate` | < 1.0 mmol/L | 1.0 – 2.0 mmol/L | ≥ 2.1 mmol/L |

Activation logic: worst-state wins across both metrics. Signal is `optimal` only when
BOTH metrics are optimal. Signal is `at_risk` when EITHER metric is at_risk.
This is correctly implemented by `deterministic_threshold` activation logic with both
threshold sets present (engine evaluates worst state).

### Override rules

| Rule | Condition | Resulting state | Evidence |
|------|-----------|-----------------|---------|
| `lactate_hyperlactatemia` | lactate ≥ 4.0 mmol/L | at_risk | Ampath clinical reference [29] |
| `hypertriglyceridemia` | triglycerides ≥ 5.6 mmol/L | at_risk | Endocrine Society Guideline [32] |
| `overt_diabetes` | glucose ≥ 7.0 mmol/L OR hba1c ≥ 6.5% | at_risk | ADA Standards 2026 [33] |

### Required derived metrics

- `tyg_index` (in platform: KBP-0002)
- `tg_hdl_ratio` (in platform — supporting/display context only)

### Optional derived metrics

- `homa_ir` (in platform: ratio_registry.py)
- `c14_c2_ratio` = tetradecanoylcarnitine_c14 / acetylcarnitine_c2 (NOT in platform — future)

---

## KEY EVIDENCE

| Source | Finding | Use |
|--------|---------|-----|
| PMC7142375 | Fasting lactate optimal < 1.0 mmol/L; metabolic health marker | Lactate thresholds |
| PMC11063788 | TyG < 4.49 insulin-sensitive; > 4.68 insulin-resistant | TyG thresholds |
| oval.care MetFlex White Paper | MetFlex index: fasting lactate scoring system | Lactate threshold validation |
| PMC8653431 | TG/HDL ratio as insulin resistance and atherosclerosis marker | tg_hdl_ratio evidence |
| PMC4765362 | Metabolic inflexibility: mitochondrial fuel switching failure | Physiological claim |
| PMC6093334 | Metabolic flexibility adaptation to energy resources | Conceptual framework |
| PMC2014521 | Metformin and fasting plasma lactate in T2D | Metformin correction (deferred) |

---

## FORMULA IMAGE STATUS

Paper contains formula images (image3–image7 in source document). All formulas
are recoverable from text descriptions in Sections 6–8. No unrecoverable content.

---

_REV1 completed 2026-03-10. Package KBP-0008 ready for creation._
