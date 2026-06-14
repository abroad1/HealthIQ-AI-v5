# BATCH2-FULL-COVERAGE-ACTIVATION-1 — Activate Research-Supported Thyroid and Androgen Signals

---
work_id: BATCH2-FULL-COVERAGE-ACTIVATION-1_activate_research_supported_thyroid_and_androgen_signals
branch: work/BATCH2-FULL-COVERAGE-ACTIVATION-1-activate-research-supported-thyroid-and-androgen-signals
status: IMPLEMENTATION_COMPLETE
---

## Executive verdict

Four research-supported Batch 2 packages are runtime-activated with fail-closed disclosure-state gates. Five packages remain inactive (DHEA identity remediation, modifier-only futures, insufficient evidence). Medical research authority consumed from `docs/Medical Research Documents/Batch_2_Thyroid_Androgen_Context_Authority_Review.md`. All architecture validators and targeted regression/governance tests pass.

---

## Gate remediation (post-activation)

Additional fail-closed gates applied per medical research authority review:

| Signal | Change |
|--------|--------|
| `signal_free_testosterone_low` | `demographic.is_adult`: `present` → `disclosed` (requires confirmed adult; minors fail closed) |
| `signal_free_t3_low` | Pregnancy exclusion: `clinical_context.pregnancy_status` must be `answered_no` |
| `signal_fai_high` | Pregnancy exclusion + DHEA supplementation exclusion via `supplement.dhea_supplementation_status` |
| `signal_free_testosterone_high` | Pregnancy exclusion + DHEA supplementation exclusion |

Runtime evaluator additions:
- `supplement.dhea_supplementation_status` disclosure-state primitive (`answered_yes` / `answered_no` / `not_answered`)
- Pregnancy snapshot fix: `pregnancy_status: false` no longer treated as unanswered (removed `or`-chain falsy bug)

Schema: `package_manifest_schema.yaml` — added `SIGNAL_RUNTIME_ACTIVATION` to `behavioural_impact` enum.

---

## Activated packages (4)

| Package | Signal | Scope |
|---------|--------|-------|
| `pkg_kb47_free_t3_low_low_t3_syndrome` | `signal_free_t3_low` | `enable_lower_bound: true`; TSH/FT4 companion; illness, thyroid medication, calorie restriction, fasting, **pregnancy exclusion** gates |
| `pkg_kb47_fai_high_biochemical_hyperandrogenism` | `signal_fai_high` | Female-only; testosterone/SHBG present; therapy/AAS exclusion; symptoms disclosure; **pregnancy + DHEA supplement exclusion** |
| `pkg_kb47_free_testosterone_high_androgen_excess_context` | `signal_free_testosterone_high` | Testosterone/SHBG present; therapy/AAS exclusion; symptoms disclosure; **pregnancy + DHEA supplement exclusion** |
| `pkg_kb47_free_testosterone_low_androgen_deficiency_context` | `signal_free_testosterone_low` | Adult male only (`is_adult` **disclosed**); `enable_lower_bound: true`; symptom/illness/calorie gates; therapy/AAS exclusion |

---

## Kept inactive (5)

| Package | Outcome |
|---------|---------|
| `pkg_kb47_dhea_high_androgen_excess_context` | `KEEP_INACTIVE_PENDING_DHEA_DHEAS_IDENTITY_REMEDIATION` — approval phrase absent |
| `pkg_kb47_dhea_low_adrenal_androgen_reduction` | `DO_NOT_ACTIVATE` — insufficient evidence per medical research authority |
| `pkg_kb47_fai_low_reduced_free_androgen_availability` | Modifier-only future |
| `pkg_kb47_free_testosterone_pct_high_elevated_free_androgen_fraction` | Modifier-only future |
| `pkg_kb47_free_testosterone_pct_low_reduced_free_androgen_fraction` | Modifier-only future |

---

## Runtime changes

`runtime_context_evaluator.py` (additive):
- `demographic.is_adult` (age >= 18; `disclosed` requirement requires boolean `True`)
- `clinical_context.pregnancy_status` disclosure when answered (boolean-false safe)
- `supplement.dhea_supplementation` keyword detection
- `supplement.dhea_supplementation_status` disclosure-state enum

Package `signal_library.yaml` and `package_manifest.yaml` updated for four activated packages only. Inactive package signal libraries unchanged beyond prior governance metadata.

---

## Governance registers updated

- `batch2_full_coverage_activation_execution_register_v1.yaml` (new)
- `batch2_full_coverage_activation_readiness_register_v1.yaml`
- `context_runtime_execution_register_v1.yaml`
- `medical_frame_identity_index_v1.yaml` (4 frames → `runtime_active_canonical`)

Historical clearance/minimum-coverage registers retained as pre-activation snapshots; execution register is authoritative for activation state.

---

## Known omissions (documented)

- Free testosterone high: method/assay gate not fully encoded; fail-closed via missing method primitive if required upstream.
- DHEA packages: no activation without explicit `APPROVE DHEA-S ACTIVATION IN BATCH2-FULL-COVERAGE-ACTIVATION-1` phrase.

---

## Validator output (full)

### run_architecture_validation_gate.py

```
validation_status: PASS
errors: 0
index_path: C:\Users\abroa\HealthIQ-AI-v5\knowledge_bus\governance\medical_frame_identity_index_v1.yaml
validation_status: PASS
errors: 0
catalogue_path: C:\Users\abroa\HealthIQ-AI-v5\knowledge_bus\governance\context_modifier_catalogue_draft_v1.yaml
day_one_architecture_validation: PASS
medical_intelligence_architecture_validation: PASS
.......s..                                                               [100%]
=========================== short test summary info ===========================
SKIPPED [1] backend\tests\architecture\test_medical_intelligence_architecture_sentinels.py:67: full gate already executed by run_architecture_validation_gate.py
.....................                                                    [100%]
[architecture-gate] validate_medical_frame_identity_index
[architecture-gate] validate_context_modifier_catalogue
[architecture-gate] validate_day_one_architecture
[architecture-gate] validate_medical_intelligence_architecture
[architecture-gate] pytest_architecture_guardrails
[architecture-gate] pytest_governance_regression
architecture_validation_gate: PASS
```

### validate_knowledge_package.py (9 packages)

```

=== validate pkg_kb47_free_t3_low_low_t3_syndrome ===
validation_status: PASS
errors: 0
audit_path: C:\Users\abroa\HealthIQ-AI-v5\backend\artifacts\package_manifest_audit.md
validation_status: PASS
errors: 0
validated_biomarkers: 3
validated_metrics: 0
audit_path: C:\Users\abroa\HealthIQ-AI-v5\backend\artifacts\research_audit.md
validation_status: PASS
audit_path: C:\Users\abroa\HealthIQ-AI-v5\backend\artifacts\promoted_signal_intelligence_audit.md
manifest_validation: PASS
research_validation: PASS
signal_validation: PASS
intelligence_validation: SKIP
promoted_signal_intelligence_validation: PASS
ready_for_implementation: True
manifest_audit_path: C:\Users\abroa\HealthIQ-AI-v5\backend\artifacts\package_manifest_audit.md
research_audit_path: C:\Users\abroa\HealthIQ-AI-v5\backend\artifacts\research_audit.md
architecture_audit_path: C:\Users\abroa\HealthIQ-AI-v5\backend\artifacts\architecture_audit.md
aggregated_status_path: C:\Users\abroa\HealthIQ-AI-v5\backend\artifacts\knowledge_status.json
=== validate pkg_kb47_fai_high_biochemical_hyperandrogenism ===
validation_status: PASS
errors: 0
audit_path: C:\Users\abroa\HealthIQ-AI-v5\backend\artifacts\package_manifest_audit.md
validation_status: PASS
errors: 0
validated_biomarkers: 3
validated_metrics: 0
audit_path: C:\Users\abroa\HealthIQ-AI-v5\backend\artifacts\research_audit.md
validation_status: PASS
audit_path: C:\Users\abroa\HealthIQ-AI-v5\backend\artifacts\promoted_signal_intelligence_audit.md
manifest_validation: PASS
research_validation: PASS
signal_validation: PASS
intelligence_validation: SKIP
promoted_signal_intelligence_validation: PASS
ready_for_implementation: True
manifest_audit_path: C:\Users\abroa\HealthIQ-AI-v5\backend\artifacts\package_manifest_audit.md
research_audit_path: C:\Users\abroa\HealthIQ-AI-v5\backend\artifacts\research_audit.md
architecture_audit_path: C:\Users\abroa\HealthIQ-AI-v5\backend\artifacts\architecture_audit.md
aggregated_status_path: C:\Users\abroa\HealthIQ-AI-v5\backend\artifacts\knowledge_status.json
=== validate pkg_kb47_free_testosterone_high_androgen_excess_context ===
validation_status: PASS
errors: 0
audit_path: C:\Users\abroa\HealthIQ-AI-v5\backend\artifacts\package_manifest_audit.md
validation_status: PASS
errors: 0
validated_biomarkers: 3
validated_metrics: 0
audit_path: C:\Users\abroa\HealthIQ-AI-v5\backend\artifacts\research_audit.md
validation_status: PASS
audit_path: C:\Users\abroa\HealthIQ-AI-v5\backend\artifacts\promoted_signal_intelligence_audit.md
manifest_validation: PASS
research_validation: PASS
signal_validation: PASS
intelligence_validation: SKIP
promoted_signal_intelligence_validation: PASS
ready_for_implementation: True
manifest_audit_path: C:\Users\abroa\HealthIQ-AI-v5\backend\artifacts\package_manifest_audit.md
research_audit_path: C:\Users\abroa\HealthIQ-AI-v5\backend\artifacts\research_audit.md
architecture_audit_path: C:\Users\abroa\HealthIQ-AI-v5\backend\artifacts\architecture_audit.md
aggregated_status_path: C:\Users\abroa\HealthIQ-AI-v5\backend\artifacts\knowledge_status.json
=== validate pkg_kb47_free_testosterone_low_androgen_deficiency_context ===
validation_status: PASS
errors: 0
audit_path: C:\Users\abroa\HealthIQ-AI-v5\backend\artifacts\package_manifest_audit.md
validation_status: PASS
errors: 0
validated_biomarkers: 3
validated_metrics: 0
audit_path: C:\Users\abroa\HealthIQ-AI-v5\backend\artifacts\research_audit.md
validation_status: PASS
audit_path: C:\Users\abroa\HealthIQ-AI-v5\backend\artifacts\promoted_signal_intelligence_audit.md
manifest_validation: PASS
research_validation: PASS
signal_validation: PASS
intelligence_validation: SKIP
promoted_signal_intelligence_validation: PASS
ready_for_implementation: True
manifest_audit_path: C:\Users\abroa\HealthIQ-AI-v5\backend\artifacts\package_manifest_audit.md
research_audit_path: C:\Users\abroa\HealthIQ-AI-v5\backend\artifacts\research_audit.md
architecture_audit_path: C:\Users\abroa\HealthIQ-AI-v5\backend\artifacts\architecture_audit.md
aggregated_status_path: C:\Users\abroa\HealthIQ-AI-v5\backend\artifacts\knowledge_status.json
=== validate pkg_kb47_dhea_high_androgen_excess_context ===
validation_status: PASS
errors: 0
audit_path: C:\Users\abroa\HealthIQ-AI-v5\backend\artifacts\package_manifest_audit.md
validation_status: PASS
errors: 0
validated_biomarkers: 3
validated_metrics: 0
audit_path: C:\Users\abroa\HealthIQ-AI-v5\backend\artifacts\research_audit.md
validation_status: PASS
audit_path: C:\Users\abroa\HealthIQ-AI-v5\backend\artifacts\promoted_signal_intelligence_audit.md
manifest_validation: PASS
research_validation: PASS
signal_validation: PASS
intelligence_validation: SKIP
promoted_signal_intelligence_validation: PASS
ready_for_implementation: True
manifest_audit_path: C:\Users\abroa\HealthIQ-AI-v5\backend\artifacts\package_manifest_audit.md
research_audit_path: C:\Users\abroa\HealthIQ-AI-v5\backend\artifacts\research_audit.md
architecture_audit_path: C:\Users\abroa\HealthIQ-AI-v5\backend\artifacts\architecture_audit.md
aggregated_status_path: C:\Users\abroa\HealthIQ-AI-v5\backend\artifacts\knowledge_status.json
=== validate pkg_kb47_dhea_low_adrenal_androgen_reduction ===
validation_status: PASS
errors: 0
audit_path: C:\Users\abroa\HealthIQ-AI-v5\backend\artifacts\package_manifest_audit.md
validation_status: PASS
errors: 0
validated_biomarkers: 3
validated_metrics: 0
audit_path: C:\Users\abroa\HealthIQ-AI-v5\backend\artifacts\research_audit.md
validation_status: PASS
audit_path: C:\Users\abroa\HealthIQ-AI-v5\backend\artifacts\promoted_signal_intelligence_audit.md
manifest_validation: PASS
research_validation: PASS
signal_validation: PASS
intelligence_validation: SKIP
promoted_signal_intelligence_validation: PASS
ready_for_implementation: True
manifest_audit_path: C:\Users\abroa\HealthIQ-AI-v5\backend\artifacts\package_manifest_audit.md
research_audit_path: C:\Users\abroa\HealthIQ-AI-v5\backend\artifacts\research_audit.md
architecture_audit_path: C:\Users\abroa\HealthIQ-AI-v5\backend\artifacts\architecture_audit.md
aggregated_status_path: C:\Users\abroa\HealthIQ-AI-v5\backend\artifacts\knowledge_status.json
=== validate pkg_kb47_fai_low_reduced_free_androgen_availability ===
validation_status: PASS
errors: 0
audit_path: C:\Users\abroa\HealthIQ-AI-v5\backend\artifacts\package_manifest_audit.md
validation_status: PASS
errors: 0
validated_biomarkers: 4
validated_metrics: 0
audit_path: C:\Users\abroa\HealthIQ-AI-v5\backend\artifacts\research_audit.md
validation_status: PASS
audit_path: C:\Users\abroa\HealthIQ-AI-v5\backend\artifacts\promoted_signal_intelligence_audit.md
manifest_validation: PASS
research_validation: PASS
signal_validation: PASS
intelligence_validation: SKIP
promoted_signal_intelligence_validation: PASS
ready_for_implementation: True
manifest_audit_path: C:\Users\abroa\HealthIQ-AI-v5\backend\artifacts\package_manifest_audit.md
research_audit_path: C:\Users\abroa\HealthIQ-AI-v5\backend\artifacts\research_audit.md
architecture_audit_path: C:\Users\abroa\HealthIQ-AI-v5\backend\artifacts\architecture_audit.md
aggregated_status_path: C:\Users\abroa\HealthIQ-AI-v5\backend\artifacts\knowledge_status.json
=== validate pkg_kb47_free_testosterone_pct_high_elevated_free_androgen_fraction ===
validation_status: PASS
errors: 0
audit_path: C:\Users\abroa\HealthIQ-AI-v5\backend\artifacts\package_manifest_audit.md
validation_status: PASS
errors: 0
validated_biomarkers: 3
validated_metrics: 0
audit_path: C:\Users\abroa\HealthIQ-AI-v5\backend\artifacts\research_audit.md
validation_status: PASS
audit_path: C:\Users\abroa\HealthIQ-AI-v5\backend\artifacts\promoted_signal_intelligence_audit.md
manifest_validation: PASS
research_validation: PASS
signal_validation: PASS
intelligence_validation: SKIP
promoted_signal_intelligence_validation: PASS
ready_for_implementation: True
manifest_audit_path: C:\Users\abroa\HealthIQ-AI-v5\backend\artifacts\package_manifest_audit.md
research_audit_path: C:\Users\abroa\HealthIQ-AI-v5\backend\artifacts\research_audit.md
architecture_audit_path: C:\Users\abroa\HealthIQ-AI-v5\backend\artifacts\architecture_audit.md
aggregated_status_path: C:\Users\abroa\HealthIQ-AI-v5\backend\artifacts\knowledge_status.json
=== validate pkg_kb47_free_testosterone_pct_low_reduced_free_androgen_fraction ===
validation_status: PASS
errors: 0
audit_path: C:\Users\abroa\HealthIQ-AI-v5\backend\artifacts\package_manifest_audit.md
validation_status: PASS
errors: 0
validated_biomarkers: 3
validated_metrics: 0
audit_path: C:\Users\abroa\HealthIQ-AI-v5\backend\artifacts\research_audit.md
validation_status: PASS
audit_path: C:\Users\abroa\HealthIQ-AI-v5\backend\artifacts\promoted_signal_intelligence_audit.md
manifest_validation: PASS
research_validation: PASS
signal_validation: PASS
intelligence_validation: SKIP
promoted_signal_intelligence_validation: PASS
ready_for_implementation: True
manifest_audit_path: C:\Users\abroa\HealthIQ-AI-v5\backend\artifacts\package_manifest_audit.md
research_audit_path: C:\Users\abroa\HealthIQ-AI-v5\backend\artifacts\research_audit.md
architecture_audit_path: C:\Users\abroa\HealthIQ-AI-v5\backend\artifacts\architecture_audit.md
aggregated_status_path: C:\Users\abroa\HealthIQ-AI-v5\backend\artifacts\knowledge_status.json

```

---

## Test output (full)

```
============================= test session starts =============================
platform win32 -- Python 3.13.3, pytest-8.4.1, pluggy-1.6.0
rootdir: C:\Users\abroa\HealthIQ-AI-v5\backend
configfile: pyproject.toml
plugins: anyio-4.9.0, asyncio-1.2.0, cov-7.0.0, html-4.2.0, json-report-1.5.0, metadata-3.1.1
asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collected 91 items

backend\tests\regression\test_batch2_full_coverage_activation.py ....... [  7%]
.............                                                            [ 21%]
backend\tests\regression\test_runtime_context_evaluation.py ............ [ 35%]
................                                                         [ 52%]
backend\tests\regression\test_context_threading.py .........             [ 62%]
backend\tests\regression\test_batch2_thyroid_tsh_gating.py ...........   [ 74%]
backend\tests\governance\test_batch2_context_clearance_register.py ..... [ 80%]
..                                                                       [ 82%]
backend\tests\governance\test_batch2_full_coverage_build_governance.py . [ 83%]
....                                                                     [ 87%]
backend\tests\governance\test_batch2_minimum_coverage_decision_register.py . [ 89%]
......                                                                   [ 95%]
backend\tests\governance\test_runtime_context_semantics_model.py ....    [100%]

============================= 91 passed in 9.89s ==============================
```

Activation regression suite: 20 tests (includes pregnancy/DHEA exclusion cases).

---

## Rollback path

Revert signal_library gates and `enable_lower_bound` flags, package manifests, frame index entries, governance registers, runtime evaluator additions, tests, and this audit paper per `batch2_full_coverage_activation_execution_register_v1.yaml` rollback_path.

---

## Carry-forward impact

- **CF-BATCH2-FULL-COV-1**: Resolved — activation sprint complete for research-supported subset.
- **CF-BATCH2-010**: Partially addressed — three androgen packages activated under medical research authority; DHEA/FAI-low/pct packages still require external clinical sign-off.
- **New**: DHEA/DHEA-S identity remediation remains blocked pending dedicated sprint and approval phrase.
