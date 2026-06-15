# DHEA-S-HIGH-ACTIVATION-1 — Medical Authority Gated Runtime Activation

---
work_id: DHEA-S-HIGH-ACTIVATION-1_medical_authority_gated_runtime_activation
branch: work/DHEA-S-HIGH-ACTIVATION-1-medical-authority-gated-runtime-activation
status: MECHANICAL_CORRECTIONS_COMPLETE
---

## Executive verdict

DHEA-S high is activated as a **standalone cautious biomarker-level signal** per `docs/Medical Research Documents/DHEA-S_High_Activation_Medical_Research_Review.md` (`DHEA_S_HIGH_ACTIVATE_NOW`, `standalone_signal_allowed: true`, `corroboration_required: false`). Activation uses lab-provided reference range, requires age and biological sex, suppresses DHEA supplementation and pregnancy, and does not require testosterone/SHBG/FAI for the basic signal. DHEA-S low, DHEA low, and unsulfated DHEA remain inactive. No frontend, scoring, or report compiler contract changes.

---

## Medical authority summary

| Directive | Value |
|-----------|-------|
| activation_recommendation | DHEA_S_HIGH_ACTIVATE_NOW |
| standalone_signal_allowed | true |
| corroboration_required | false |
| DHEA-S low | BIOMARKER_LEVEL_EXPLANATION_ONLY (inactive) |
| Unsulfated DHEA high/low | DO_NOT_ACTIVATE |

This report supersedes the prior DHEA-S high blocker (CF-DHEA-S-ACTIVATION-001 external clinician sign-off) for DHEA-S high activation only.

---

## Why this supersedes the prior blocker

`DHEA-DHEAS-CANONICALISATION-1` withheld activation pending external clinician sign-off. The new dedicated medical authority report provides explicit activation approval for DHEA-S high as a cautious standalone signal with defined gates and wording constraints.

---

## Activation gates

1. Canonical `dhea_s` (not unsulfated DHEA)
2. Above lab-provided reference range
3. Age present
4. Biological sex present
5. DHEA supplementation: suppress only when `answered_yes`; `not_answered` and `answered_no` allow cautious biomarker-level signal
6. Pregnancy: suppress only when `answered_yes`; `not_answered`, `not_applicable`, and `answered_no` allow signal
7. Hormone therapy / AAS: disclosure-state gates allow `not_answered`; `answered_yes` permits basic signal with limitation wording
8. Optional supplement-field presence is not a hard blocker

**Not required for basic signal:** testosterone, SHBG, FAI, symptoms (symptoms affect limitation wording only, not activation)

---

## Suppression gates

- DHEA supplementation answered_yes
- Pregnancy answered_yes
- Missing age or biological sex
- Ambiguous DHEA without unit/range (fail-closed canonicalisation)
- Unsulfated DHEA metric

---

## Downgrade / limitation rules

- Testosterone therapy answered_yes: basic signal may emit; broader androgen-excess wording limited
- AAS exposure answered_yes: same
- Missing testosterone/SHBG/FAI/symptoms: biomarker-level limitation note in signal metadata

---

## Wording safety review

Permitted: "may be consistent with increased adrenal androgen production", "not diagnostic on its own"

Forbidden in signal explanation: PCOS diagnosis, adrenal tumour, adrenal overactivity, treatment/supplement recommendations

---

## Package outcomes

| Package | Outcome |
|---------|---------|
| pkg_kb47_dhea_high_androgen_excess_context | **runtime_active_canonical** (DHEA-S high standalone) |
| pkg_kb47_dhea_low_adrenal_androgen_reduction | inactive |
| Unsulfated DHEA | not activated |

---

## Confirmations

- No frontend changes
- No scoring changes
- No report compiler contract changes
- No raw research runtime reads introduced
- DHEA/DHEA-S canonicalisation unchanged
- CF-DHEA-S-ACTIVATION-001 closed

---

---

## Mechanical corrections (Claude audit FAIL — MECHANICAL)

Applied targeted gate fixes per GPT routing; medical authority decision unchanged.

| # | Change | File |
|---|--------|------|
| 1 | Removed `symptoms_status` from `required_context` | `signal_library.yaml` |
| 2 | `pregnancy_status` allowed: `answered_no`, `not_answered`, `not_applicable` | `signal_library.yaml` |
| 3 | `dhea_supplementation_status` allowed: `answered_no`, `not_answered` | `signal_library.yaml` |
| 4 | Removed `supplements_disclosed`, `aas_exposure_status_disclosed`, `hormone_therapy_status_disclosed` presence gates; added `not_answered` to hormone/AAS disclosure gates | `signal_library.yaml` |
| 5 | Launch estate gate docs: five activated packages, four inactive androgen, DHEA-S high active | `day_one_launch_estate_gate_v1.yaml` |
| 6 | Removed duplicate `governance_runtime_activation_status` key | `batch2_full_coverage_activation_execution_register_v1.yaml` |
| 7–8 | Added minimal real-user context tests + suppression/inactive coverage | `test_dhea_s_high_activation.py`, `test_runtime_context_evaluation.py` |
| — | Set `pregnancy_status: not_answered` when pregnancy field absent (evaluator mechanical fix) | `runtime_context_evaluator.py` |

---

## Validator output (full — post mechanical correction)

```
validation_status: PASS
errors: 0
index_path: knowledge_bus/governance/medical_frame_identity_index_v1.yaml
validation_status: PASS
errors: 0
catalogue_path: knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml
day_one_architecture_validation: PASS
day_one_launch_estate_gate: PASS
medical_intelligence_architecture_validation: PASS
.......s..
SKIPPED [1] backend\tests\architecture\test_medical_intelligence_architecture_sentinels.py:67: full gate already executed by run_architecture_validation_gate.py
.....................                                                    [100%]
[architecture-gate] validate_medical_frame_identity_index
[architecture-gate] validate_context_modifier_catalogue
[architecture-gate] validate_day_one_architecture
[architecture-gate] validate_day_one_launch_estate_gate
[architecture-gate] validate_medical_intelligence_architecture
[architecture-gate] pytest_architecture_guardrails
[architecture-gate] pytest_governance_regression
architecture_validation_gate: PASS
OK: no secret env files are git-tracked.
```

---

## Test output (full — post mechanical correction)

```
============================= test session starts =============================
platform win32 -- Python 3.13.3, pytest-8.4.1, pluggy-1.6.0
collected 96 items

backend\tests\regression\test_dhea_dheas_canonicalisation.py ...         [  3%]
backend\tests\regression\test_dhea_s_high_activation.py .............    [ 16%]
backend\tests\regression\test_batch2_full_coverage_activation.py ....... [ 23%]
.............                                                            [ 37%]
backend\tests\regression\test_output_authority_provenance.py ........... [ 48%]
..                                                                       [ 51%]
backend\tests\regression\test_runtime_context_evaluation.py ............ [ 63%]
................                                                         [ 80%]
backend\tests\regression\test_context_threading.py .........             [ 89%]
backend\tests\governance\test_dhea_s_high_activation_governance.py ...   [ 92%]
backend\tests\governance\test_dhea_dheas_canonicalisation_governance.py . [ 93%]
backend\tests\unit\test_unit_aware_biomarker_identity_v1.py ......       [100%]

============================= 96 passed in 10.19s =============================
```

---

## Validator output (full — initial implementation)

```
validation_status: PASS
errors: 0
day_one_architecture_validation: PASS
day_one_launch_estate_gate: PASS
medical_intelligence_architecture_validation: PASS
architecture_validation_gate: PASS
OK: no secret env files are git-tracked.
```

---

## Test output (full — initial implementation)

```
============================= test session starts =============================
platform win32 -- Python 3.13.3, pytest-8.4.1, pluggy-1.6.0
collected 93 items

backend\tests\regression\test_dhea_dheas_canonicalisation.py ...         [  3%]
backend\tests\regression\test_dhea_s_high_activation.py ..........       [ 13%]
backend\tests\regression\test_batch2_full_coverage_activation.py ....... [ 21%]
.............                                                            [ 35%]
backend\tests\regression\test_output_authority_provenance.py ........... [ 47%]
..                                                                       [ 49%]
backend\tests\regression\test_runtime_context_evaluation.py ............ [ 62%]
................                                                         [ 79%]
backend\tests\regression\test_context_threading.py .........             [ 89%]
backend\tests\governance\test_dhea_s_high_activation_governance.py ...   [ 92%]
backend\tests\governance\test_dhea_dheas_canonicalisation_governance.py . [ 93%]
backend\tests\unit\test_unit_aware_biomarker_identity_v1.py ......       [100%]

============================= 93 passed in 10.18s =============================
```

---

## Rollback path

Revert package activation metadata, signal_library gates, governance registers, tests, and audit paper. Restore DHEA-S high to inactive_pending_external_clinician_signoff in batch2 register.

---

## Recommended next action

Claude re-audit (mechanical corrections applied) → GPT architectural review → human approval → merge
