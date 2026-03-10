# 7 — Cardiovascular Metabolic Risk (MDVA) — REV1

**REV1 Status: CANONICAL REVIEW COMPLETE**
Package-ready for KBP-0011.

Source document: `knowledge_bus/research/papers/7-Cardiovascular-Metabolic-Risk.md`

---

## CANONICAL RESOLUTIONS

### 1. Biomarker naming corrections

| Paper name | SSOT canonical | Notes |
|-----------|---------------|-------|
| `hb_a1c` | `hba1c` | Standard alias correction |
| `systolic_bp` | `systolic_bp` | In lifestyle_registry.yaml — NOT a blood biomarker; exclude from research_brief.yaml biomarkers[] |
| `diastolic_bp` | `diastolic_bp` | In lifestyle_registry.yaml — NOT a blood biomarker; exclude from research_brief.yaml biomarkers[] |
| `albuminuria (uACR)` | `uacr` (derived) | uACR is a derived metric (albumin_urine / creatinine_urine); tracked as SSOT gap in KBP-0006; listed as optional derived_metric, not biomarker |

### 2. Derived metric platform status

| Metric | Platform status | Notes |
|--------|----------------|-------|
| `aip` | ✗ NOT IN PLATFORM | Not in ratio_registry.py DERIVED_IDS; SSOT gap (standard sprint) |
| `pulse_pressure` | ✗ NOT IN PLATFORM | Already tracked in SSOT_GAPS.md (KBP-0007); formula: systolic_bp − diastolic_bp; inputs in lifestyle_registry |

**AIP simplification:** AIP = log10(TG_mmol / HDL_mmol) = log10(tg_hdl_ratio), where
tg_hdl_ratio IS already in platform (ratio_registry.py DERIVED_IDS). AIP implementation
reduces to a single log10 wrapper around the existing tg_hdl_ratio.

**Important:** Paper notes "If using mg/dL, the ratio remains the same, but specific
log-bases may vary in literature." This is INCORRECT — the numerical value of AIP does
change between mmol/L and mg/dL because the ratios differ by a conversion factor
(TG×88.57 / HDL×38.67 = ratio × 2.29). The mmol/L and mg/dL versions of AIP are NOT
interchangeable. All SSOT thresholds are anchored to mmol/L. The Niroumand 2015
thresholds (0.11 / 0.21) must be confirmed as mmol/L-based — they are commonly cited
with mmol/L context and are used as canonical values here. Decision raised in
clinical_signoff.md.

### 3. Override rule — age-based EVA flag

Section 8 rule: `age < 30 AND pulse_pressure > 60 → at_risk (EVA flag)`

`age` is NOT registered in SSOT. Only `date_of_birth` is available (questionnaire.json).
Age is derivable at runtime but cannot be expressed as a signal_library threshold
metric_id. **Resolution**: Document as a clinical narrative flag for KB-S9 runtime
implementation — annotate signal output when derived_age < 30 AND pulse_pressure > 60.
Not implemented as a schema override rule.

### 4. Compound override — synergistic glycation

Section 8 rule: `aip > 0.21 AND glucose > 7.0 → at_risk (High Priority)`

Expressible in schema using condition_type "all_of". Note that aip > 0.21 already
triggers at_risk from the primary threshold tier, so this rule is redundant for state
classification but documents the synergistic mechanism. Implemented as override rule
`synergistic_glycation` for completeness and downstream annotation use.

### 5. pulse_pressure suboptimal tier

Paper provides two pulse_pressure tiers (optimal < 50, at_risk > 60) but no explicit
suboptimal. The 50–60 mmHg range is the standard gray zone in hypertension guidelines.
Added as suboptimal override rule (pp ≥ 50 AND pp ≤ 60 → suboptimal).

### 6. Threshold delta with KBP-0007

KBP-0007 (signal_vascular_cognitive_reserve) tracks pulse_pressure with thresholds
< 45 optimal, > 60 at_risk (from Farnier 2021 data context). Paper 7 uses < 50
optimal, > 60 at_risk. The > 60 at_risk boundary is consistent; the optimal
boundary differs (45 vs 50 mmHg). Flagged in clinical_signoff.md — Decision required
before KB-S9 to reconcile the pulse_pressure optimal boundary across packages.

### 7. Evidence quality note

**Primary source** (Niroumand 2015; n=4,215): cross-sectional design, Persian
population only — Tier 2 evidence (prospective endpoint validation absent).
**Nilsson 2014**: expert consensus / review — Tier 3 for threshold derivation.
AIP thresholds 0.11/0.21 are widely cited in lipidology literature but validated
primarily in cross-sectional and observational studies. Decision raised in clinical_signoff.md.

---

## SSOT STATUS

| Input | Source | Status |
|-------|--------|--------|
| `triglycerides` | biomarkers.yaml | ✓ mmol/L |
| `hdl_cholesterol` | biomarkers.yaml | ✓ mmol/L |
| `glucose` | biomarkers.yaml | ✓ mmol/L |
| `hba1c` | biomarkers.yaml | ✓ % |
| `systolic_bp` | lifestyle_registry.yaml | ✓ mmHg (not a blood biomarker) |
| `diastolic_bp` | lifestyle_registry.yaml | ✓ mmHg (not a blood biomarker) |
| `aip` | ratio_registry.py | ✗ SSOT gap — standard sprint |
| `pulse_pressure` | ratio_registry.py | ✗ SSOT gap — already in SSOT_GAPS.md (KBP-0007) |

---

## SIGNAL DEFINITION (CANONICAL)

**Signal ID**: `signal_metabolic_vascular_ageing`
**System**: `vascular`
**Primary metric**: `aip`

### Primary thresholds (Niroumand et al. 2015; n=4,215; mmol/L basis)

| Tier | Threshold | Note |
|------|-----------|------|
| Optimal | aip < 0.11 | log10(TG_mmol/HDL_mmol) — small, buoyant LDL predominant |
| Suboptimal | aip 0.11 – 0.21 | Borderline atherogenic particle distribution |
| At risk | aip > 0.21 | Small dense LDL predominant; highest sub-endothelial penetration risk |

### Override rules

| Rule | Conditions | State | Evidence |
|------|-----------|-------|---------|
| `pulse_pressure_at_risk` | pp > 60 | at_risk | Framingham; structural arterial stiffness |
| `pulse_pressure_suboptimal` | pp ≥ 50 AND pp ≤ 60 | suboptimal | Implied gray zone; Framingham threshold context |
| `synergistic_glycation` | aip > 0.21 AND glucose > 7.0 | at_risk | Niroumand 2015; glycation + atherogenic dyslipidaemia synergism |

EVA age-flag (age < 30 AND pp > 60): clinical narrative only — runtime annotation.

---

_REV1 completed 2026-03-10. Package KBP-0011 ready for creation._
