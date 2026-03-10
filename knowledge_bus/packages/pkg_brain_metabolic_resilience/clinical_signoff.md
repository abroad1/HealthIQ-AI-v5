# Clinical Sign-off — pkg_brain_metabolic_resilience (KBP-0007)

## Status: PENDING IMPLEMENTATION PREREQUISITES

The signal logic, thresholds, and override rules are evidence-anchored and ready.
The package cannot activate in the pipeline until two derived metrics are implemented.

---

## Implementation Prerequisites (Blocking)

### 1. `ghr_index` — Not yet computed

`ghr_index` is not in `ratio_registry.py` DERIVED_IDS. Required before signal activates.

Formula (platform canonical, mmol/L inputs):
```
ghr_index = glucose_mmol_l / hdl_cholesterol_mmol_l
```

Unit conversion from paper (Farnier et al. 2021 uses mg/dL ratio):
- glucose: mmol/L × 18.02 = mg/dL
- HDL: mmol/L × 38.67 = mg/dL
- Conversion factor: 18.02 / 38.67 = 0.4659 (mg/dL ratio → mmol/L ratio: × 2.146)

Canonical thresholds:
| mg/dL threshold | Platform canonical | Derivation |
|----------------|-------------------|------------|
| < 2.5 (optimal) | < 5.37 | 2.5 × 2.146 |
| > 4.0 (at_risk) | > 8.59 | 4.0 × 2.146 |

Verification: glucose 5.0 mmol/L ÷ HDL 1.3 mmol/L = 3.85 → × 0.4659 = 1.79 mg/dL (optimal < 2.5 ✓)

Both `glucose` and `hdl_cholesterol` are confirmed in `backend/ssot/biomarkers.yaml`.

### 2. `pulse_pressure` — Not yet computed

`pulse_pressure` is not in `ratio_registry.py` DERIVED_IDS. Required before override rules activate.

Formula:
```
pulse_pressure = systolic_bp - diastolic_bp
```

Inputs: `systolic_bp` and `diastolic_bp` are in `backend/ssot/lifestyle_registry.yaml` (mmHg).
No new SSOT biomarker additions required — inputs already registered.

---

## Resolved Decisions

### ghr_index canonical unit conversion — RESOLVED

Platform computes: `glucose (mmol/L) / hdl_cholesterol (mmol/L)` = dimensionless ratio.
Paper thresholds (Farnier 2021) in mg/dL ratio converted using factor 2.146.

| Clinical interpretation | mg/dL threshold | Platform canonical |
|------------------------|----------------|-------------------|
| Optimal | < 2.5 | < 5.37 |
| At risk | > 4.0 | > 8.59 |

No suboptimal band: Farnier et al. derives only optimal and at_risk cut-offs.
The 5.37–8.59 range has no validated intermediate tier — confirmed by addendum evidence review.

### pulse_pressure suboptimal tier — RESOLVED (not supported)

Rotterdam Study (Mattace-Raso et al., 2004) explicitly does not define 45–60 mmHg as
a distinct risk tier. Treated as transition zone. Suboptimal tier omitted by design.

### Signal system classification — RESOLVED

Schema allowed values do not include `neurological`. System set to `vascular` — correct
for this signal's Two-Hit Hypothesis mechanism (cerebrovascular stiffness and pulsatility).

### Age-gated override rule — RESOLVED (engineering deferred)

Rotterdam Study strongest risk correlation is in adults aged >50. Original override rule
`age > 50 AND pulse_pressure > 60 → at_risk` is clinically valid but requires runtime
age derivation from `date_of_birth` (questionnaire SSOT) — same pattern as `fib_4` and
`egfr`. Implementation deferred: the standalone `pulse_pressure > 60 → at_risk` override
fires for all ages and is the conservative safe implementation. The age-gated version
can be added as a future enhancement once questionnaire integration is confirmed for
signal evaluation context.

---

## Open Clinical Decisions

### 1. ghr_index evidence extrapolation — communication
Thresholds (Farnier 2021) are validated in peripheral microvasculature (retinal, renal),
not cerebral vessels. User-facing narrative must note this signal is an indirect
surrogate, not a direct brain scan finding. Engineering/narrative team to confirm messaging.

### 2. ACCORD-MIND framing
Signal must be communicated as prognostic, not prescriptive. Intensive glucose lowering
alone did not improve cognitive outcomes. Narrative must not imply that lowering
ghr_index via medication will reduce dementia risk.

### 3. Aortic regurgitation exclusion
Artificially elevated pulse_pressure in aortic regurgitation makes pulse_pressure
override rules invalid for this population. No runtime flag currently handles this.
Options:
- (a) Accept limitation; document in signal metadata
- (b) Add questionnaire-driven exclusion flag
Decision deferred to implementation sprint.

---

## Future Signal

`signal_brain_metabolic_health` is parked pending prospective validation of TyG index
cut-offs against dementia/cognitive decline endpoints. Research source:
`10-Brain-Metabolic-Health-(Future-Expansion).md`. The TyG index is already in the
platform (ratio_registry.py). Re-commission trigger: prospective cohort study
establishing numeric TyG thresholds against hard cognitive outcome endpoints
(MCI diagnosis, dementia incidence, MMSE trajectory).

Override rule of interest when signal_brain_metabolic_health activates:
T2D (HbA1c ≥ 6.5% or confirmed diabetes diagnosis) → at_risk. Evidence:
diabetics have ~2–2.5× higher dementia risk (established consensus).
