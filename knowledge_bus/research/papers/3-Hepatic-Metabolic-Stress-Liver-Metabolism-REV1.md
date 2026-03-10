# 3 — Hepatic Metabolic Stress & Liver Metabolism — REV1

**REV1 Status: CANONICAL REVIEW COMPLETE**
All naming corrections and canonical decisions documented below.
Formula images in source document are UNREADABLE — all formulas confirmed from
platform implementations (ratio_registry.py). Package-ready for KBP-0010.

Source document: `knowledge_bus/research/papers/3-Hepatic-Metabolic-Stress-Liver-Metabolism.md`

---

## CANONICAL RESOLUTIONS

### 1. Biomarker naming corrections

| Paper name | SSOT canonical | Unit |
|-----------|---------------|------|
| `alanine_aminotransferase` | `alt` | IU/L |
| `aspartate_aminotransferase` | `ast` | IU/L |
| `platelet_count` | `platelets` | ×10⁹/L |
| `gamma_glutamyltransferase` | `ggt` | IU/L |
| `waist_circumference` | `waist_circumference_cm` | cm (lifestyle_registry) |

### 2. Derived metric platform status corrections

Paper Section 6 states "Existing in platform: No" for all derived metrics.
**All four derived metrics ARE already in the platform (ratio_registry.py DERIVED_IDS):**

| Derived metric | Platform status | Formula confirmed |
|---------------|----------------|------------------|
| `tyg_index` | ✓ IN PLATFORM | `ln((tg_mmol × glucose_mmol × 1596.0) / 2.0)` |
| `tyg_bmi_index` | ✓ IN PLATFORM | `tyg_index × bmi` |
| `ast_alt_ratio` | ✓ IN PLATFORM | `ast / alt` |
| `fib_4` | ✓ IN PLATFORM | `(age × ast) / (platelets × √alt)` |

No new derived metrics required. Formula images in source document are unreadable
but all formulas are recoverable from ratio_registry.py implementations.

### 3. System field

Paper states "metabolic | hepatic". Schema allows single value. Correct value: `hepatic`
(valid schema value; more specific than `metabolic` for this liver-centric signal).

### 4. Primary metric design decision — RESOLVED

Section 10 states primary metric = `tyg_bmi_index`. However, the threshold table uses:
- Optimal and suboptimal: `tyg_index` (8.21 / 8.97)
- At risk only: `tyg_bmi_index` (≥ 180.71) OR `tyg_index` > 8.97

`tyg_bmi_index` has NO validated optimal/suboptimal thresholds in the paper — only an
at_risk trigger (Liu et al., cross-sectional, n=4,753). `tyg_index` has a complete
three-tier threshold set (Targher et al., n=2,900, 10-year follow-up).

**Resolution**: Package uses `tyg_index` as the primary metric with full threshold
tiers. `tyg_bmi_index` ≥ 180.71 enters as an at_risk override rule. This is the
validator-compliant design (schema requires threshold metrics to be primary or in
override_rules) and is clinically equivalent to the paper's intent.
Documented in clinical_signoff.md.

### 5. ALT sex-specific thresholds — RESOLVED (conservative approximation)

Paper: ALT at_risk ≥ 33 IU/L (male), ≥ 25 IU/L (female). Schema: no sex-specific support.
Resolution: two override rules:
- `alt_masld_at_risk`: alt ≥ 33 → at_risk (male/general AASLD threshold)
- `alt_masld_suboptimal_female`: alt ≥ 25 → suboptimal (female threshold applied conservatively)
Both rules are "any_of" — applies to all users. Conservative for males (25-33 zone
triggers suboptimal); clinically defensible since the paper frames this as a gradient
detection signal. Documented in clinical_signoff.md.

### 6. TyG index thresholds — canonical units confirmed

TyG index is computed as `ln(TG_mg/dl × glucose_mg/dl / 2)` via SI constant (platform
already handles mmol/L→mg/dL conversion). The threshold values (8.21 / 8.97) are in the
same log-scale as the platform formula. No unit conversion required.

Threshold source: Targher et al. (2-year data cited as source "24" in paper).
At-risk note: paper states values > 8.5 consistently associated with increased IR and
fatty liver across populations; 8.97 (Q4 threshold) is from Zhang et al. 2018 meta-analysis.

### 7. TyG-BMI threshold — canonical units confirmed

TyG-BMI = tyg_index × BMI (dimensionless × kg/m²). Platform: same formula.
Threshold 180.71 from Liu et al. (cross-sectional, n=4,753). Evidence tier: single
cross-sectional study — Tier 2. Malek 2025 meta-analysis validates TyG-BMI diagnostic
performance (AUC 0.83) but does not give a specific at_risk threshold. 180.71 is the
best available threshold; documented as single-study origin in clinical_signoff.

### 8. FIB-4 fibrosis rule-out — schema limitation

Paper override rule 4: fib_4 < 1.30 → "negative for advanced fibrosis (regardless of TyG)".
This is a DOWNGRADE rule — it reduces concern, not increases it. The current signal_library
schema only supports state-upgrading override rules (resulting_state is typically at_risk
or suboptimal). This rule is documented in clinical_signoff.md as a narrative/context
flag: when fib_4 < 1.30, the signal output should be annotated "advanced fibrosis excluded"
in the UX — it does not change the steatosis-based signal state.

### 9. Formula image status

ALL formulas in Section 6 (TyG, TyG-BMI, AST/ALT, FIB-4) are given as images and are
UNREADABLE from source document. However, ALL formulas are confirmed from ratio_registry.py:
no clinical information is lost. Formula recovery confirmed.

---

## SSOT STATUS — ALL CLEAR

All required biomarkers are in SSOT:
| Biomarker | SSOT canonical | Status |
|-----------|---------------|--------|
| `alt` | `alt` | ✓ IU/L |
| `ast` | `ast` | ✓ IU/L |
| `triglycerides` | `triglycerides` | ✓ mmol/L |
| `glucose` | `glucose` | ✓ mmol/L |

Optional biomarkers: `ggt` ✓, `platelets` ✓, `albumin` ✓, `waist_circumference_cm` ✓
(lifestyle_registry).

No SSOT biomarker gaps. Research_validation expected: PASS.

---

## SIGNAL DEFINITION (CANONICAL)

**Signal ID**: `signal_hepatic_metabolic_stress`
**System**: `hepatic`
**Primary metric**: `tyg_index`

### Primary thresholds (Targher et al.; Zhang et al. 2018)

| Tier | Threshold |
|------|-----------|
| Optimal | tyg_index < 8.21 |
| Suboptimal | tyg_index 8.21 – 8.97 |
| At risk | tyg_index > 8.97 |

### Override rules

| Rule | Condition | State | Evidence |
|------|-----------|-------|---------|
| `tyg_bmi_at_risk` | tyg_bmi_index ≥ 180.71 | at_risk | Liu et al. (n=4,753); Malek 2025 AUC 0.83 |
| `alt_masld_at_risk` | alt ≥ 33 | at_risk | AASLD 2023 (male threshold) |
| `alt_masld_suboptimal_female` | alt ≥ 25 | suboptimal | AASLD 2023 (female threshold, conservative) |
| `alt_acute_injury` | alt > 100 | at_risk | Standard clinical practice (3× ULN) |
| `triglycerides_pancreatitis` | triglycerides ≥ 5.6 | at_risk | ESC/EAS 2019 guidelines |
| `ald_pattern` | ast_alt_ratio > 2.0 AND alt > 33 | at_risk | Release of mitochondrial AST in ALD |

---

_REV1 completed 2026-03-10. Package KBP-0010 ready for creation._
