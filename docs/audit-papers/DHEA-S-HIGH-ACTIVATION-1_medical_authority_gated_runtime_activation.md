# DHEA-S-HIGH-ACTIVATION-1 — Medical Authority Gated Runtime Activation

---
work_id: DHEA-S-HIGH-ACTIVATION-1_medical_authority_gated_runtime_activation
branch: work/DHEA-S-HIGH-ACTIVATION-1-medical-authority-gated-runtime-activation
status: IMPLEMENTATION_COMPLETE
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
5. DHEA supplementation disclosed; suppress if answered_yes
6. Testosterone therapy / AAS / HRT disclosed (answered_yes allows basic signal; broader wording limited)
7. Pregnancy disclosed; suppress if answered_yes
8. Supplements disclosed

**Not required for basic signal:** testosterone, SHBG, FAI, symptoms (required only for broader androgen-excess wording).

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

## Validator output (full)

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

## Test output (full)

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

Claude audit → GPT architectural review → human approval → merge
