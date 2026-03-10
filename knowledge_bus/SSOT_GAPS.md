# SSOT Gaps — Knowledge Bus Ingestion Batch 1

Tracked during batch ingestion. All items here require a dedicated HIGH risk sprint
(SOP §7: touches `backend/ssot/` and/or `backend/core/analytics/`).

---

## Biomarkers missing from `backend/ssot/biomarkers.yaml`

| Biomarker | Unit | Required by | Notes |
|-----------|------|-------------|-------|
| `albumin_urine` | mg/L | KBP-0006 (pkg_ckd_risk) | Urine albumin; input to uACR |
| `creatinine_urine` | g/L | KBP-0006 (pkg_ckd_risk) | Urine creatinine; input to uACR. If lab reports mmol/L, convert: g/L = mmol/L × 0.1131 |

---

## Derived metrics missing from `ratio_registry.py` DERIVED_IDS

| Metric | Formula | Required by | Notes |
|--------|---------|-------------|-------|
| `uacr` | `albumin_urine_mg_l / creatinine_urine_g_l` | KBP-0006 (pkg_ckd_risk) | Result in mg/g; primary metric for signal_ckd_risk |
| `egfr` | CKD-EPI 2021 (without race coefficient) | KBP-0006 (pkg_ckd_risk) | `142 × min(scr/κ,1)^α × max(scr/κ,1)^-1.200 × 0.9938^age`; scr = creatinine_umol_l ÷ 88.4; κ=0.7(F)/0.9(M); α=-0.241(F)/-0.302(M); age from `date_of_birth`; sex from `biological_sex` |
| `ghr_index` | `glucose_mmol_l / hdl_cholesterol_mmol_l` | KBP-0007 (pkg_brain_metabolic_resilience) | mmol/L ratio; canonical thresholds: < 5.37 optimal, > 8.59 at_risk (converted from Farnier 2021 mg/dL values × 2.146) |
| `pulse_pressure` | `systolic_bp - diastolic_bp` | KBP-0007 (pkg_brain_metabolic_resilience) | mmHg; inputs from lifestyle_registry (no new SSOT biomarker entries needed); thresholds: < 45 optimal, > 60 at_risk |

---

## Optional / future biomarkers (not blocking)

| Biomarker | Unit | Required by | Notes |
|-----------|------|-------------|-------|
| `cystatin_c` | mg/L | KBP-0006 optional | Confounded by inflammation, thyroid disease, steroids |
| `ngal_urine` | ng/mL | KBP-0006 optional | False-positive in sepsis and malignancy |
| `tmao` | µmol/L | KBP-0006 optional | Parked — signal_kidney_metabolic_stress pending prospective outcome data |

---

## Packages processed

| Package | Status | Validator result | SSOT gaps logged |
|---------|--------|-----------------|-----------------|
| KBP-0006 pkg_ckd_risk | Committed | manifest ✓ signal ✓ research ✗ (2 missing SSOT entries) | albumin_urine, creatinine_urine, uacr, egfr |
| KBP-0007 pkg_brain_metabolic_resilience | Committed | manifest ✓ signal ✓ research ✓ (full PASS) | ghr_index, pulse_pressure (no new biomarkers — lifestyle_registry inputs already registered) |

---

_Update this file after each package is validated. Sprint to resolve all gaps once batch is complete._
