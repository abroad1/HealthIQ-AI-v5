# BETA-READINESS-SPRINT-2 — Runtime Gate Consistency and Active Signal Reachability

---
work_id: BETA-READINESS-SPRINT-2_runtime_gate_consistency_and_active_signal_reachability
branch: work/BETA-READINESS-SPRINT-2-runtime-gate-consistency-and-active-signal-reachability
status: IMPLEMENTATION_COMPLETE
---

## Executive verdict

Resolved pregnancy_status gate consistency for FAI high, FT3 low and free testosterone high by aligning allowed values with the DHEA-S high model (`answered_no`, `not_answered`, `not_applicable`). Added deterministic active-signal context gate reachability validator promoted to the architecture validation gate. Added real-user reachability regression tests. DHEA-S high remains active; DHEA-S low and unsulfated DHEA remain inactive; no new activations or deactivations.

---

## Active signal reachability audit (pre-change)

| Package | Signal | pregnancy gate (before) | Questionnaire captures pregnancy? | Evaluator produces not_answered? | Unintentional suppress risk |
|---------|--------|-------------------------|-----------------------------------|----------------------------------|----------------------------|
| pkg_kb47_fai_high_biochemical_hyperandrogenism | signal_fai_high | answered_no only | No | Yes (since DHEA-S sprint) | **Yes** |
| pkg_kb47_free_t3_low_low_t3_syndrome | signal_free_t3_low | answered_no only | No | Yes | **Yes** |
| pkg_kb47_free_testosterone_high_androgen_excess_context | signal_free_testosterone_high | answered_no only | No | Yes | **Yes** |
| pkg_kb47_free_testosterone_low_androgen_deficiency_context | signal_free_testosterone_low | none | No | N/A | No pregnancy gate |
| pkg_kb47_dhea_high_androgen_excess_context | signal_dhea_high | answered_no, not_answered, not_applicable | No | Yes | **No** (fixed prior sprint) |

---

## Pregnancy-gate consistency decisions

| Package | Decision | Rationale |
|---------|----------|-----------|
| FAI high | **A** — expand allowed_values | Non-pregnancy-specific biochemical signal; pregnancy answered_yes remains suppressive via exclusion from allowed set |
| FT3 low | **A** — expand allowed_values | Contextual low T3 education signal; pregnancy-specific interpretation unavailable |
| FT high | **A** — expand allowed_values | Same model as FAI high / DHEA-S high |
| DHEA-S high | **No change** | Already corrected in DHEA-S-HIGH-ACTIVATION-1 |
| FT low | **No change** | No pregnancy_status gate |

---

## Gate changes made

```yaml
pregnancy_status:
  allowed_values:
    - answered_no
    - not_answered
    - not_applicable
```

Applied to: `pkg_kb47_fai_high_biochemical_hyperandrogenism`, `pkg_kb47_free_t3_low_low_t3_syndrome`, `pkg_kb47_free_testosterone_high_androgen_excess_context`.

---

## Gates deliberately not changed

| Gate | Package | Reason |
|------|---------|--------|
| symptoms_status | FAI high, FT high, FT low | Suppress-until-answered per Batch 2 medical authority; registered in policy |
| calorie_restriction_status, fasting_status | FT3 low, FT low | Lifestyle-sourced; suppress-until-answered with medical justification |
| dhea_supplementation_status (answered_no only) | FAI high, FT high | Deferred to CF-BETA-READINESS-2 |
| hormone_therapy / AAS disclosed presence | FAI high, FT high | Existing Batch 2 gates unchanged |

---

## Runtime context evaluator review

- `pregnancy_status`: defaults to `not_answered` when field absent (DHEA-S-HIGH-ACTIVATION-1); **no change this sprint**
- Other disclosure keys reviewed; no broad rewrite required
- Lifestyle-sourced keys remain set only when lifestyle_factors answered

---

## Validator design

**Script:** `backend/scripts/validate_active_signal_context_gate_reachability.py`  
**Policy:** `knowledge_bus/governance/active_signal_context_gate_reachability_policy_v1.yaml`  
**Promoted to:** `run_architecture_validation_gate.py`

Checks all 5 active Batch 2 packages for pregnancy gate safety, questionnaire-absent key handling, and suppress-until-answered registry entries.

---

## Confirmations

- DHEA-S high remains **runtime_active_canonical**
- DHEA-S low remains **inactive**
- Unsulfated DHEA high/low remain **inactive**
- Batch 2 active package count: **5**
- No new signal activation
- No signal deactivation
- No frontend, scoring, or report compiler changes
- No raw research runtime reads introduced
- No diagnosis or treatment wording introduced

---

## Validator output (full)

```
validation_status: PASS
errors: 0
index_path: knowledge_bus/governance/medical_frame_identity_index_v1.yaml
validation_status: PASS
errors: 0
catalogue_path: knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml
day_one_architecture_validation: PASS
day_one_launch_estate_gate: PASS
active_package_count: 5
[active] pkg_kb47_free_t3_low_low_t3_syndrome :: signal_free_t3_low (7 gates)
[active] pkg_kb47_fai_high_biochemical_hyperandrogenism :: signal_fai_high (11 gates)
[active] pkg_kb47_free_testosterone_high_androgen_excess_context :: signal_free_testosterone_high (11 gates)
[active] pkg_kb47_free_testosterone_low_androgen_deficiency_context :: signal_free_testosterone_low (11 gates)
[active] pkg_kb47_dhea_high_androgen_excess_context :: signal_dhea_high (6 gates)
validation_status: PASS
errors: 0
active_packages_checked: 5
medical_intelligence_architecture_validation: PASS
.......s..
SKIPPED [1] backend\tests\architecture\test_medical_intelligence_architecture_sentinels.py:67
.....................                                                    [100%]
[architecture-gate] validate_medical_frame_identity_index
[architecture-gate] validate_context_modifier_catalogue
[architecture-gate] validate_day_one_architecture
[architecture-gate] validate_day_one_launch_estate_gate
[architecture-gate] validate_active_signal_context_gate_reachability
[architecture-gate] validate_medical_intelligence_architecture
[architecture-gate] pytest_architecture_guardrails
[architecture-gate] pytest_governance_regression
architecture_validation_gate: PASS
OK: no secret env files are git-tracked.
```

---

## Test output (full)

```
============================= test session starts =============================
platform win32 -- Python 3.13.3, pytest-8.4.1, pluggy-1.6.0
collected 99 items

backend\tests\regression\test_runtime_context_evaluation.py ............ [ 12%]
................                                                         [ 28%]
backend\tests\regression\test_context_threading.py .........             [ 37%]
backend\tests\regression\test_batch2_full_coverage_activation.py ....... [ 44%]
.............                                                            [ 57%]
backend\tests\regression\test_dhea_s_high_activation.py .............    [ 70%]
backend\tests\regression\test_output_authority_provenance.py ........... [ 81%]
..                                                                       [ 83%]
backend\tests\regression\test_active_signal_context_gate_reachability.py . [ 84%]
........                                                                 [ 92%]
backend\tests\governance\test_active_signal_context_gate_reachability_governance.py . [ 93%]
...                                                                      [ 96%]
backend\tests\governance\test_dhea_s_high_activation_governance.py ...   [100%]

============================= 99 passed in 10.68s =============================
```

---

## Rollback path

Revert signal_library pregnancy gate changes, reachability validator, policy YAML, architecture gate wiring, tests, carry-forward register, estate gate doc, and audit paper.

---

## Recommended next action

Claude audit → GPT architectural review → human approval → merge
