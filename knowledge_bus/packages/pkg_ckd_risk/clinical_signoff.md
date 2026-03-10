# Clinical Sign-off — pkg_ckd_risk (KBP-0006)

## Status: PENDING IMPLEMENTATION PREREQUISITES

The signal logic, thresholds, and override rules are evidence-anchored and ready.
The package cannot activate in the pipeline until two derived metrics are implemented.

---

## Implementation Prerequisites (Blocking)

### 1. `uacr` — Not yet computed

`uacr` is not in `ratio_registry.py` DERIVED_IDS. Required before signal activates.

Formula: `uacr = albumin_urine_mg_l / creatinine_urine_g_l` → result in mg/g

Unit handling:
- `albumin_urine` input: mg/L
- `creatinine_urine` input: g/L (if stored as mmol/L, convert: g/L = mmol/L × 0.1131)

SSOT action required: confirm whether `albumin_urine` and `creatinine_urine` are
urine biomarkers that need adding to `backend/ssot/biomarkers.yaml`.

### 2. `egfr` — Not yet computed

`egfr` is not in `ratio_registry.py` DERIVED_IDS. Required before eGFR override rules activate.

Formula: CKD-EPI 2021 (without race coefficient):
```
egfr = 142 × min(scr / kappa, 1)^alpha × max(scr / kappa, 1)^(-1.200) × 0.9938^age
```
Where:
- `scr` = creatinine in mg/dL (convert from µmol/L: scr = creatinine_umol_l / 88.4)
- `kappa` = 0.7 (female), 0.9 (male)
- `alpha` = -0.241 (female), -0.302 (male)
- `age` = derived from `date_of_birth` (questionnaire SSOT)
- `sex` = from `biological_sex` (questionnaire SSOT)

Note: `urea_creatinine_ratio` IS already computed and override rules using it
will function once uacr is available as the primary metric.

---

## Resolved Decisions

### urea_creatinine_ratio canonical unit conversion — RESOLVED

Platform computes: `urea (mmol/L) / creatinine (µmol/L)` = small decimal ratio.
US clinical thresholds (10/20/30:1) converted using factor 247.6:

| Clinical interpretation | US threshold | Platform canonical |
|------------------------|-------------|-------------------|
| Liver disease / low production | < 10:1 | < 0.040 |
| Normal / intrinsic renal | 10–20:1 | 0.040–0.081 |
| Pre-renal azotaemia | > 20:1 | > 0.081 |
| GI bleed | > 30:1 | > 0.121 |

Verified: urea 5.0 mmol/L ÷ creatinine 88 µmol/L = 0.057 (normal band ✓)

### eGFR 60–89 without albuminuria — RESOLVED

KDIGO 2024 and UKKIDNEY 2023 explicitly state eGFR 60–89 without concurrent
albuminuria is NOT CKD and must not be flagged as suboptimal. Handled by signal
design: no threshold or override rule independently triggers suboptimal for
eGFR 60–89. Only fires suboptimal if uACR ≥30 mg/g (primary threshold) OR
eGFR 45–59 (egfr_moderate_risk override).

---

## Open Clinical Decisions

### 1. GI bleed override — clinical communication
The `gi_bleed_flag` (urea_creatinine_ratio > 0.121 → at_risk) is a differential
diagnostic flag, not a primary kidney disease finding. The user-facing narrative
must clearly distinguish "possible GI bleed" from "kidney disease" when this
rule fires. Engineering/narrative team to confirm messaging.

### 2. Diabetic hyperfiltration handling
Early diabetes can produce eGFR >90 (hyperfiltration), making the signal classify
as optimal when early nephropathy is progressing. No runtime logic currently
adjusts for this. Options:
- (a) Accept limitation; document in signal metadata
- (b) Add override: if chronic_conditions includes diabetes AND uacr >= 30 → flag
      (requires questionnaire SSOT integration at signal evaluation time)
Decision deferred to implementation sprint.

### 3. Age-stratified eGFR messaging
eGFR 60–89 without albuminuria is common in adults over 65 and within normal
variation. Consider age-stratified messaging at runtime (not threshold adjustment —
thresholds remain KDIGO-anchored). Narrative layer decision.

---

## Future Signal

`signal_kidney_metabolic_stress` is parked pending prospective metabolomics
outcome data. Markers (TMAO, myo-inositol, pyruvate) have AUC >0.7 in early
CKD cross-sectional studies but lack hard outcome thresholds as of 2026.
Re-commission trigger: prospective cohort study with ESRD/progression endpoints
establishing cut-off values for any metabolic marker in a human population.
