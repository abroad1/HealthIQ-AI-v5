# BATCH2-FULL-COVERAGE-ACTIVATION-1 — Activate Research-Supported Thyroid and Androgen Signals

---
work_id: BATCH2-FULL-COVERAGE-ACTIVATION-1_activate_research_supported_thyroid_and_androgen_signals
branch: work/BATCH2-FULL-COVERAGE-ACTIVATION-1-activate-research-supported-thyroid-and-androgen-signals
status: IMPLEMENTATION_COMPLETE
---

## Executive verdict

Four research-supported Batch 2 packages are runtime-activated with fail-closed disclosure-state gates. Five packages remain inactive (DHEA identity remediation, modifier-only futures, insufficient evidence). Medical research authority consumed from `docs/Medical Research Documents/Batch_2_Thyroid_Androgen_Context_Authority_Review.md`. All architecture validators and targeted regression/governance tests pass.

---

## Activated packages (4)

| Package | Signal | Scope |
|---------|--------|-------|
| `pkg_kb47_free_t3_low_low_t3_syndrome` | `signal_free_t3_low` | `enable_lower_bound: true`; TSH/FT4 companion; illness, thyroid medication, calorie restriction, fasting gates |
| `pkg_kb47_fai_high_biochemical_hyperandrogenism` | `signal_fai_high` | Female-only; testosterone/SHBG present; therapy/AAS exclusion; symptoms disclosure |
| `pkg_kb47_free_testosterone_high_androgen_excess_context` | `signal_free_testosterone_high` | Testosterone/SHBG present; therapy/AAS exclusion; symptoms disclosure |
| `pkg_kb47_free_testosterone_low_androgen_deficiency_context` | `signal_free_testosterone_low` | Adult male only; `enable_lower_bound: true`; symptom/illness/calorie gates; therapy/AAS exclusion |

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
- `demographic.is_adult` (age >= 18)
- `clinical_context.pregnancy_status` disclosure when answered
- `supplement.dhea_supplementation` keyword detection

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

## Validator output

### run_architecture_validation_gate.py

```
architecture_validation_gate: PASS
```

### validate_knowledge_package.py (9 packages)

All nine context-dependent Batch 2 packages: PASS.

---

## Test output

```
python -m pytest backend/tests/regression/test_batch2_full_coverage_activation.py \
  backend/tests/regression/test_runtime_context_evaluation.py \
  backend/tests/regression/test_context_threading.py \
  backend/tests/regression/test_batch2_thyroid_tsh_gating.py \
  backend/tests/governance/ -q

86 passed
```

Activation regression suite: 15 tests covering FT3 low, FAI high, free testosterone high/low, inactive pct/DHEA packages.

---

## Rollback path

Revert signal_library gates and `enable_lower_bound` flags, package manifests, frame index entries, governance registers, runtime evaluator additions, tests, and this audit paper per `batch2_full_coverage_activation_execution_register_v1.yaml` rollback_path.

---

## Carry-forward impact

- **CF-BATCH2-FULL-COV-1**: Resolved — activation sprint complete for research-supported subset.
- **CF-BATCH2-010**: Partially addressed — three androgen packages activated under medical research authority; DHEA/FAI-low/pct packages still require external clinical sign-off.
- **New**: DHEA/DHEA-S identity remediation remains blocked pending dedicated sprint and approval phrase.
