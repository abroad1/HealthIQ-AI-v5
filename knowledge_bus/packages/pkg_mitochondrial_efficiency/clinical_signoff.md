# Clinical Sign-off — pkg_mitochondrial_efficiency (KBP-0008)

## Status: PENDING IMPLEMENTATION PREREQUISITES

The signal logic, thresholds, and override rules are evidence-anchored and ready.
The package cannot activate in the pipeline until one SSOT biomarker is added.

---

## Implementation Prerequisites (Blocking)

### 1. `lactate` — Not in biomarkers.yaml

`lactate` is not in `backend/ssot/biomarkers.yaml`. Required before signal validates.

Unit: **mmol/L** (fasting plasma lactate)
Formula: none (direct biomarker, not derived)

Thresholds confirmed in mmol/L — no unit conversion required once SSOT entry is added.

---

## Implementation Prerequisites (Derived Metrics)

### 2. `tyg_index` — Already in platform ✓

`tyg_index` is in `ratio_registry.py` DERIVED_IDS. Implemented via KBP-0002
(insulin resistance package). Platform formula:
```
tyg_index = ln((tg_mmol_l × glucose_mmol_l × 1596.0) / 2.0)
```
where 1596.0 = 88.5714 × 18.018 (SI-to-mg/dL constant). Equivalent to standard
formula `ln(TG_mg/dL × glucose_mg/dL / 2)`. Threshold values (4.49 / 4.68) are
in the same log-scale units. No implementation work needed.

### 3. `tg_hdl_ratio` — Already in platform ✓

`tg_hdl_ratio` is in `ratio_registry.py`. Platform computes: `tg_mmol_l / hdl_mmol_l`
(mmol/L ratio). Used as supporting/display metric in this signal.

No threshold logic applied to tg_hdl_ratio in this signal — see Open Clinical
Decision #1 below.

---

## Resolved Decisions

### Dual-metric activation logic — RESOLVED

Signal uses both tyg_index and lactate as threshold metrics with independent
threshold tiers. Activation semantics: **worst-state wins**.
- Signal = optimal only when BOTH tyg_index < 4.49 AND lactate < 1.0
- Signal = at_risk when EITHER tyg_index > 4.68 OR lactate ≥ 2.1

Implementation note: `deterministic_threshold` activation logic with both threshold
sets present implements worst-state semantics. Engineering must confirm that the
signal evaluation engine takes the maximum severity across all threshold evaluations
for a given signal. This is the same pattern as any multi-metric signal.

### tyg_index platform status — RESOLVED

Paper incorrectly states "Existing in platform? No". tyg_index IS in platform via
KBP-0002. No duplication or re-implementation needed.

### tg_hdl_ratio unit canonical — RESOLVED

Platform tg_hdl_ratio = mmol/L ratio (tg_mmol_l / hdl_mmol_l). Paper Section 7
thresholds (M: 3.5, F: 2.5) are in mg/dL ratio. Canonical conversion:
M → 1.53 mmol/L, F → 1.09 mmol/L. These thresholds NOT encoded in signal_library
(see Open Clinical Decision #1).

### `hb_a1c` naming error — RESOLVED

Paper uses `hb_a1c`. SSOT canonical name is `hba1c`. Corrected throughout package.

### glucose override ADA threshold — RESOLVED

Fasting glucose ≥ 7.0 mmol/L is the ADA diagnostic threshold for diabetes
(Standards of Care 2026). Combined with hba1c ≥ 6.5% in a single any_of override
rule. hba1c fires only when present in panel (optional dependency).

---

## Open Clinical Decisions

### 1. tg_hdl_ratio sex-specific thresholds — DEFERRED (schema limitation)

PMC8653431 provides sex-specific tg_hdl_ratio optimal thresholds:
- Male: < 3.5 mg/dL ratio → < 1.53 mmol/L (platform canonical)
- Female: < 2.5 mg/dL ratio → < 1.09 mmol/L (platform canonical)

The signal_library schema has no sex-stratified threshold support. tg_hdl_ratio
is therefore included as a required_derived_metric for display context only.
Options when schema is extended:
- (a) Add sex-stratified threshold fields to schema → encode sex-specific tg_hdl_ratio thresholds
- (b) Accept limitation; document sex-specific values in narrative only
Decision deferred to schema extension sprint.

### 2. Metformin threshold adjustment — DEFERRED (schema limitation)

Patients on Metformin show elevated fasting lactate independent of mitochondrial
dysfunction (PMC2014521). Adjusted thresholds in Metformin users:
- Optimal: < 1.3 mmol/L (instead of < 1.0)
- At_risk: ≥ 2.4 mmol/L (instead of ≥ 2.1)

This is a threshold-adjustment pattern (not a state-forcing override) that does
not fit the current override_rules schema. Options when schema supports it:
- (a) Add "threshold_modifier" rule type to signal_library schema
- (b) Create Metformin-specific signal variant
Decision deferred. Requires `long_term_medications` from questionnaire SSOT.
Interim conservative approach: current thresholds may over-classify Metformin
users as at_risk — clinician review recommended for this population.

### 3. Lactate elevation from sympathetic state — communication

Implementation note from paper: resting_heart_rate > 100 bpm can indicate high
sympathetic tone that raises lactate independent of mitochondrial dysfunction.
No runtime flag currently handles this. Options:
- (a) Accept limitation; document in signal narrative
- (b) Add lifestyle_registry.resting_heart_rate-based flag as optional override
Decision deferred to implementation sprint.

### 4. c14_c2_ratio — future optional metric

tetradecanoylcarnitine_c14 / acetylcarnitine_c2 ratio is a specialist acylcarnitine
panel marker for very-long-chain acyl-CoA dehydrogenase (VLCAD) function. Neither
biomarker is in SSOT. Tracked as optional future gap. Only relevant for specialist
metabolic disease workup; not required for the general metabolic flexibility signal.

---

## Future Signal

`signal_mitochondrial_disease` using c14_c2_ratio as primary metric is parked.
Re-commission trigger: acylcarnitine panel becomes routinely available in SSOT
and prospective thresholds for c14_c2_ratio against mitochondrial disease endpoints
are validated.

---

_Clinical sign-off complete. Signal ready for implementation once lactate is added to biomarkers.yaml._
