# SSOT Gaps — Knowledge Bus Ingestion Batch 1

Tracked during batch ingestion. All items here require a dedicated HIGH risk sprint
(SOP §7: touches `backend/ssot/` and/or `backend/core/analytics/`).

---

## Biomarkers missing from `backend/ssot/biomarkers.yaml`

| Biomarker | Unit | Required by | Notes |
|-----------|------|-------------|-------|
| `albumin_urine` | mg/L | KBP-0006 (pkg_ckd_risk) | Urine albumin; input to uACR |
| `creatinine_urine` | g/L | KBP-0006 (pkg_ckd_risk) | Urine creatinine; input to uACR. If lab reports mmol/L, convert: g/L = mmol/L × 0.1131 |
| `lactate` | mmol/L | KBP-0008 (pkg_mitochondrial_efficiency) | Fasting plasma lactate; primary co-metric for signal_mitochondrial_efficiency |

---

## Questionnaire SSOT gaps (missing options in `long_term_medications`)

| Missing option | Required by | Notes |
|---------------|-------------|-------|
| Antihypertensive medication (boolean) | KBP-0009 (pkg_metabolic_syndrome_pattern) | Required for guideline-compliant BP component scoring; interim proxy: chronic_conditions "High blood pressure" |
| Fibrate or niacin (boolean) | KBP-0009 (pkg_metabolic_syndrome_pattern) | Required for TG component scoring (treatment → criterion met per Alberti 2009) |
| Antidiabetic medication (boolean) | KBP-0009 (pkg_metabolic_syndrome_pattern) | Required for glucose component scoring; interim proxy: chronic_conditions "Diabetes Type 1/2" |

---

## Derived metrics missing from `ratio_registry.py` DERIVED_IDS

| Metric | Formula | Required by | Notes |
|--------|---------|-------------|-------|
| `uacr` | `albumin_urine_mg_l / creatinine_urine_g_l` | KBP-0006 (pkg_ckd_risk) | Result in mg/g; primary metric for signal_ckd_risk |
| `egfr` | CKD-EPI 2021 (without race coefficient) | KBP-0006 (pkg_ckd_risk) | `142 × min(scr/κ,1)^α × max(scr/κ,1)^-1.200 × 0.9938^age`; scr = creatinine_umol_l ÷ 88.4; κ=0.7(F)/0.9(M); α=-0.241(F)/-0.302(M); age from `date_of_birth`; sex from `biological_sex` |
| `ghr_index` | `glucose_mmol_l / hdl_cholesterol_mmol_l` | KBP-0007 (pkg_brain_metabolic_resilience) | mmol/L ratio; canonical thresholds: < 5.37 optimal, > 8.59 at_risk (converted from Farnier 2021 mg/dL values × 2.146) |
| `pulse_pressure` | `systolic_bp - diastolic_bp` | KBP-0007 (pkg_brain_metabolic_resilience) | mmHg; inputs from lifestyle_registry (no new SSOT biomarker entries needed); thresholds: < 45 optimal, > 60 at_risk |
| `mets_ir` | `ln[(2×FBG_mg) + TG_mg] × BMI / ln(HDL_mg)` | KBP-0010 (pkg_metabolic_inflammation) | STANDARD SPRINT — same BMI integration pattern as tyg_bmi_index; inputs: glucose, triglycerides, hdl_cholesterol (biomarkers.yaml), bmi (lifestyle_registry) |
| `mets_component_count` | COUNT of 5 MetS criteria met (0–5) | KBP-0009 (pkg_metabolic_syndrome_pattern) | ARCHITECTURE GAP — multi-registry computation; requires new module in backend/core/analytics/ (HIGH risk); sex-specific HDL + ethnicity waist lookup table |
| `mets_bp_flag` | `(systolic_bp >= 130 OR diastolic_bp >= 85) → 1, else 0` | KBP-0009 (pkg_metabolic_syndrome_pattern) | Binary flag from lifestyle_registry inputs; simpler than mets_component_count |
| `mets_waist_flag` | `waist_circumference_cm >= ethnic_sex_threshold → 1, else 0` | KBP-0009 (pkg_metabolic_syndrome_pattern) | Requires ethnicity × sex lookup table (see clinical_signoff.md for full table) |

---

## Optional / future biomarkers (not blocking)

| Biomarker | Unit | Required by | Notes |
|-----------|------|-------------|-------|
| `cystatin_c` | mg/L | KBP-0006 optional | Confounded by inflammation, thyroid disease, steroids |
| `ngal_urine` | ng/mL | KBP-0006 optional | False-positive in sepsis and malignancy |
| `tmao` | µmol/L | KBP-0006 optional | Parked — signal_kidney_metabolic_stress pending prospective outcome data |
| `acetylcarnitine_c2` | µmol/L | KBP-0008 optional | Acylcarnitine panel; not routinely available; future c14_c2_ratio |
| `tetradecanoylcarnitine_c14` | µmol/L | KBP-0008 optional | Acylcarnitine panel; not routinely available; future c14_c2_ratio |

---

## Packages processed

| Package | Status | Validator result | SSOT gaps logged |
|---------|--------|-----------------|-----------------|
| KBP-0004 pkg_hepatic_metabolic_stress | Updated | manifest ✓ signal ✓ research ✓ (full PASS) | None — all derived metrics confirmed in platform (2026-03-10 correction) |
| KBP-0006 pkg_ckd_risk | Committed | manifest ✓ signal ✓ research ✗ (2 missing SSOT entries) | albumin_urine, creatinine_urine, uacr, egfr |
| KBP-0007 pkg_brain_metabolic_resilience | Committed | manifest ✓ signal ✓ research ✓ (full PASS) | ghr_index, pulse_pressure (no new biomarkers — lifestyle_registry inputs already registered) |
| KBP-0008 pkg_mitochondrial_efficiency | Committed | manifest ✓ signal ✓ research ✗ (1 missing SSOT entry) | lactate (blocking); acetylcarnitine_c2, tetradecanoylcarnitine_c14 (optional) |
| KBP-0009 pkg_metabolic_syndrome_pattern | Committed | manifest ✓ signal ✓ research ✓ (full PASS) | mets_component_count, mets_bp_flag, mets_waist_flag (ARCHITECTURE GAP — HIGH risk sprint); questionnaire long_term_medications expansion |
| KBP-0010 pkg_metabolic_inflammation | Committed | manifest ✓ signal ✓ research ✓ (full PASS) | mets_ir (standard sprint — ratio_registry extension); nlr, sii confirmed in platform |

---

_Update this file after each package is validated. Sprint to resolve all gaps once batch is complete._
