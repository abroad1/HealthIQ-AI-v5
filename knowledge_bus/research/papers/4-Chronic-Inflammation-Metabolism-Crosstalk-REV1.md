# 4 — Chronic Inflammation & Metabolism Crosstalk — REV1

**REV1 Status: CANONICAL REVIEW COMPLETE**
All naming corrections and canonical decisions documented below.
Formula images in source document are UNREADABLE — NLR, METS-IR, SII formulas
confirmed from ratio_registry.py (NLR, SII) and published source (METS-IR).
Package-ready for KBP-0010.

Source document: `knowledge_bus/research/papers/4-Chronic-Inflammation-Metabolism-Crosstalk.md`

---

## CANONICAL RESOLUTIONS

### 1. Biomarker naming corrections

| Paper name | SSOT canonical | Unit | Notes |
|-----------|---------------|------|-------|
| `hs_crp` | `crp` | mg/L | `hs_crp` is an alias in biomarkers.yaml |
| `neutrophils_abs` | `neutrophils` | ×10⁹/L | ratio_registry nlr/sii inputs use `neutrophils` |
| `lymphocytes_abs` | `lymphocytes` | ×10⁹/L | ratio_registry nlr/sii inputs use `lymphocytes` |
| `wbc_count` | `white_blood_cells` | ×10⁹/L | `wbc` is alias; canonical is `white_blood_cells` |

### 2. Derived metric platform status corrections

Paper Section 6 states "Existing in platform? No" for SII.
**SII IS already in the platform (ratio_registry.py DERIVED_IDS):**

| Derived metric | Platform status | Formula confirmed |
|---------------|----------------|------------------|
| `nlr` | ✓ IN PLATFORM | `neutrophils / lymphocytes` |
| `sii` | ✓ IN PLATFORM | `(platelets × neutrophils) / lymphocytes` |
| `mets_ir` | ✗ NOT IN PLATFORM | `ln[(2×FBG_mg) + TG_mg] × BMI / ln(HDL_mg)` — SSOT gap |

### 3. METS-IR formula recovery

Paper formula is an image (unreadable). Formula recovered from:
- Bello-Chavolla et al. (Endocrine, 2018) — original validation paper
- Zhang et al. 2025 (DOI: 10.1186/s12933-024-02220-z) — cited as threshold source

**Canonical formula:**
```
METS-IR = ln[(2 × glucose_mg_dL) + TG_mg_dL] × BMI / ln(HDL_mg_dL)
```

**Platform unit conversions (from SSOT mmol/L):**
```
glucose_mg_dL = glucose_mmol × 18.018
TG_mg_dL     = triglycerides_mmol × 88.57
HDL_mg_dL    = hdl_cholesterol_mmol × 38.67
BMI          = bmi (from lifestyle_registry)
```

**Implementation note:** Like tyg_bmi_index, METS-IR requires bmi from lifestyle_registry.
Can be added to ratio_registry.py (same integration pattern as tyg_bmi_index).
This is a STANDARD risk item (not ARCHITECTURE gap).

Threshold source: Zhang et al. 2025 meta-analysis. Inflection point 40.56 for CVD risk.
- optimal: METS-IR < 38.0
- suboptimal: METS-IR 38.0 – 40.56
- at_risk: METS-IR > 40.56 (rounded to 40.5 in paper table — using 40.56 from text)

### 4. Signal design decision — PRIMARY METRIC

Paper Section 10 designates `derived.nlr` as the primary metric with
`derived.mets_ir` as a required secondary. KBP-0005 uses `crp` as primary for
`signal_systemic_inflammation`. Paper 4 describes a DISTINCT signal:
`signal_metabolic_inflammation` — NLR as primary (cellular inflammation),
hs-CRP as override/supporting metric. These are complementary signals:

| Signal | Package | Primary | Focus |
|--------|---------|---------|-------|
| `signal_systemic_inflammation` | KBP-0005 | `crp` | Humoral / cytokine load |
| `signal_metabolic_inflammation` | KBP-0010 (new) | `nlr` | Cellular / innate immune activation |

Both are clinically valid. NLR captures neutrophil mobilisation and lymphocyte
suppression — the cellular hallmark of insulin resistance. hs-CRP captures IL-6-
driven hepatic acute phase response. Paper 4 is creating a NEW package.

### 5. NLR formula image — confirmed from platform

NLR formula in Section 6 is an image (unreadable). Confirmed from ratio_registry.py:
```
NLR = neutrophils / lymphocytes
```
Inputs: `neutrophils` and `lymphocytes` (×10⁹/L, same units → dimensionless ratio).

### 6. SII formula image — confirmed from platform

SII formula in Section 6 is an image (unreadable). Confirmed from ratio_registry.py:
```
SII = (platelets × neutrophils) / lymphocytes
```
Inputs: all ×10⁹/L → dimensionless ratio.

### 7. METS-IR thresholds — canonical units

METS-IR is dimensionless (log-transformed index). Zhang et al. 2025 inflection
point 40.56 is in standard METS-IR index units. Paper threshold table uses 40.5
(rounded); official paper text states 40.56. Platform uses 40.56 (exact source value).
Suboptimal lower boundary 38.0 is from paper threshold table — Zhang et al. 2025.

### 8. Residual Inflammatory Risk (RIR) override rule

Paper Section 8 states: "achieved LDL-C target AND hs_crp ≥ 2.0 mg/L → suboptimal".
This multi-condition override references LDL-C (which may or may not be available).
Schema `condition_type: "all_of"` with two conditions can express this IF ldl_cholesterol
is in scope. However, the LDL target condition is a continuous threshold ("< 70 mg/dL")
and making this override depend on treatment target achievement adds clinical complexity.
**Resolution**: Document RIR as a clinical narrative flag (annotate signal output when
ldl_cholesterol < 1.81 mmol/L AND crp >= 2.0 mg/L) rather than a schema override rule.
This is a schema limitation — documented in clinical_signoff.md. The crp acute_override
(≥ 10.0 → at_risk) and wbc leukocytosis override (> 11.0 → at_risk) ARE implemented.

### 9. System field

Paper states `inflammatory`. Schema valid value confirmed.

---

## SSOT STATUS

| Biomarker | SSOT canonical | Status |
|-----------|---------------|--------|
| `crp` | `crp` | ✓ mg/L |
| `neutrophils` | `neutrophils` | ✓ ×10⁹/L |
| `lymphocytes` | `lymphocytes` | ✓ ×10⁹/L |
| `glucose` | `glucose` | ✓ mmol/L |
| `triglycerides` | `triglycerides` | ✓ mmol/L |
| `hdl_cholesterol` | `hdl_cholesterol` | ✓ mmol/L |
| `white_blood_cells` | `white_blood_cells` | ✓ ×10⁹/L |

Optional: `platelets` ✓, `monocytes_abs` ✓, `hba1c` ✓ (all in SSOT).

**SSOT gap**: `mets_ir` not in ratio_registry.py — requires standard sprint
(not architecture gap; formula is a ratio with BMI from lifestyle_registry).

---

## SIGNAL DEFINITION (CANONICAL)

**Signal ID**: `signal_metabolic_inflammation`
**System**: `inflammatory`
**Primary metric**: `nlr`

### Primary thresholds (Leucuța et al. 2024; Dong et al. 2023)

| Tier | Threshold |
|------|-----------|
| Optimal | nlr < 2.0 |
| Suboptimal | nlr 2.0 – 3.0 |
| At risk | nlr > 3.0 |

### METS-IR thresholds (Zhang et al. 2025) — treated as supporting multi-metric

Since `mets_ir` is not yet in platform, these thresholds are documented here for
future implementation. When mets_ir is available, worst-state wins semantics apply
(same pattern as KBP-0008 dual-metric activation).

| Tier | Threshold |
|------|-----------|
| Optimal | mets_ir < 38.0 |
| Suboptimal | mets_ir 38.0 – 40.56 |
| At risk | mets_ir > 40.56 |

### Override rules

| Rule | Condition | State | Evidence |
|------|-----------|-------|---------|
| `crp_acute_inflammation` | crp > 10.0 | at_risk | Standard clinical; acute infection/trauma |
| `wbc_leukocytosis` | white_blood_cells > 11.0 | at_risk | Standard clinical leukocytosis threshold |
| `mets_ir_at_risk` | mets_ir > 40.56 | at_risk | Zhang et al. 2025 (meta-analysis, multiple cohorts) |

**Note**: mets_ir_at_risk override is included as documentation; will be active once
mets_ir is added to ratio_registry.py. validator will flag mets_ir as missing SSOT
entry — expected.

---

_REV1 completed 2026-03-10. Package KBP-0010 ready for creation._
