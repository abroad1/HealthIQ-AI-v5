# BATCH2-MINIMUM-COVERAGE-1 — Androgen and FT3 Low Clinical / Runtime Completion

---
work_id: BATCH2-MINIMUM-COVERAGE-1_androgen_ft3_low_clinical_and_runtime_completion
branch: work/BATCH2-MINIMUM-COVERAGE-1-androgen-ft3-low-clinical-and-runtime-completion
status: CLASSIFICATION_COMPLETE_NO_ACTIVATION
---

## Executive verdict

All 9 remaining Batch 2 context-dependent packages receive formal minimum-coverage decisions. **Zero packages were activated.** The exact approval phrase `APPROVE BATCH2 MINIMUM COVERAGE ACTIVATION` was **not present**. CF-BATCH2-010 remains **Open**. Eight androgen packages receive `DEFER_PENDING_EXTERNAL_CLINICAL_AUTHORITY`. FT3 low receives `EXCLUDE_FROM_MINIMUM_COVERAGE`. Validators and regression tests pass. No Intelligence Core, SSOT, scoring, report compiler, or frontend files were changed.

---

## Files inspected

- `docs/audit-papers/ARCH-COMPLETION-1_final_runtime_context_and_orchestrator_restructure.md`
- `docs/audit-papers/BATCH2-CONTEXT-COMPLETION-1_runtime_semantics_and_stop_gated_activation.md`
- `docs/audit-papers/CONTEXT-CLEARANCE-1_context_semantics_and_batch2_clearance.md`
- `docs/sprints/launch_core_carry_forward_register.md`
- `knowledge_bus/governance/batch2_context_clearance_register_v1.yaml`
- `knowledge_bus/governance/batch2_remaining_blockers_execution_register_v1.yaml`
- `knowledge_bus/governance/batch2_remainder_resolution_register_v1.yaml`
- `knowledge_bus/governance/batch2_androgen_panel_medical_review_v1.yaml`
- `knowledge_bus/governance/batch2_androgen_context_modifier_binding_v1.yaml`
- `knowledge_bus/governance/context_runtime_execution_register_v1.yaml`
- `knowledge_bus/governance/runtime_context_requirements_model_v1.yaml`
- `knowledge_bus/governance/runtime_context_semantics_model_v1.yaml`
- `knowledge_bus/governance/medical_frame_identity_index_v1.yaml`
- All 9 package directories (`package_manifest.yaml`, `signal_library.yaml`, `research_brief.yaml` where present)
- `backend/core/pipeline/orchestrator.py` (read-only)
- `backend/core/analytics/runtime_context_evaluator.py` (read-only)
- `backend/core/analytics/signal_evaluator.py` (read-only)

---

## Files changed

- `knowledge_bus/governance/batch2_minimum_coverage_decision_register_v1.yaml` (new)
- `knowledge_bus/governance/batch2_context_clearance_register_v1.yaml`
- `knowledge_bus/governance/context_runtime_execution_register_v1.yaml`
- `backend/tests/governance/test_batch2_minimum_coverage_decision_register.py` (new)
- `backend/tests/governance/test_batch2_context_clearance_register.py`
- `docs/sprints/launch_core_carry_forward_register.md`
- `docs/audit-papers/BATCH2-MINIMUM-COVERAGE-1_androgen_ft3_low_clinical_and_runtime_completion.md`

**Not changed:** package metadata, Intelligence Core, SSOT, scoring, report compiler, frontend.

---

## Authority preflight

| Check | Result |
|-------|--------|
| Branch matches work package | PASS — `work/BATCH2-MINIMUM-COVERAGE-1-androgen-ft3-low-clinical-and-runtime-completion` |
| ARCH-COMPLETION-1 merged | PASS — orchestrator imports `build_runtime_context_snapshot_from_analysis_context` |
| AnalysisContext precedes signal evaluation | PASS |
| All 8 androgen packages inactive | PASS |
| FT3 low inactive | PASS |
| No activation approval exists | PASS — `approval_received=false` |
| CF-BATCH2-010 open | PASS |
| Exact approval phrase present | **NO** |

---

## Phase 1 — 9-package classification table

| Package | Biomarker / signal | Activation state | Clinical authority | Activation blockers | Runtime blockers | Governance blockers | Recommendation |
|---------|-------------------|------------------|-------------------|---------------------|------------------|---------------------|----------------|
| pkg_kb47_dhea_high_androgen_excess_context | dhea / signal_dhea_high (high) | inactive | NO | CF-BATCH2-010 | disclosed context gates | not_in_repo signoff | DEFER_PENDING_EXTERNAL_CLINICAL_AUTHORITY |
| pkg_kb47_dhea_low_adrenal_androgen_reduction | dhea / signal_dhea_low (low) | inactive | NO | CF-BATCH2-010 | medication/stress disclosed gates | not_in_repo signoff | DEFER_PENDING_EXTERNAL_CLINICAL_AUTHORITY |
| pkg_kb47_fai_high_biochemical_hyperandrogenism | fai / signal_fai_high (high) | inactive | NO | CF-BATCH2-010 | SHBG/testosterone companions | BLOCKED_PENDING_CONTEXT_MODIFIER_BINDING | DEFER_PENDING_EXTERNAL_CLINICAL_AUTHORITY |
| pkg_kb47_fai_low_reduced_free_androgen_availability | fai / signal_fai_low (low) | inactive | NO | CF-BATCH2-010 | sex-specific FAI + companions | not_in_repo signoff | DEFER_PENDING_EXTERNAL_CLINICAL_AUTHORITY |
| pkg_kb47_free_testosterone_high_androgen_excess_context | free_testosterone / signal_free_testosterone_high | inactive | NO | CF-BATCH2-010 | cluster overlap risk | EXCLUDED from BATCH2-PROMOTE-1 | DEFER_PENDING_EXTERNAL_CLINICAL_AUTHORITY |
| pkg_kb47_free_testosterone_low_androgen_deficiency_context | free_testosterone / signal_free_testosterone_low | inactive | NO | CF-BATCH2-010 | LH/sex/medication context | not_in_repo signoff | DEFER_PENDING_EXTERNAL_CLINICAL_AUTHORITY |
| pkg_kb47_free_testosterone_pct_high_elevated_free_androgen_fraction | free_testosterone_pct / signal_free_testosterone_pct_high | inactive | NO | CF-BATCH2-010 | SHBG fraction context | BLOCKED_PENDING_CONTEXT_MODIFIER_BINDING | DEFER_PENDING_EXTERNAL_CLINICAL_AUTHORITY |
| pkg_kb47_free_testosterone_pct_low_reduced_free_androgen_fraction | free_testosterone_pct / signal_free_testosterone_pct_low | inactive | NO | CF-BATCH2-010 | SHBG/sex context gap | not_in_repo signoff | DEFER_PENDING_EXTERNAL_CLINICAL_AUTHORITY |
| pkg_kb47_free_t3_low_low_t3_syndrome | free_t3 / signal_free_t3_low (low) | inactive | PARTIAL (thyroid signoff exists; FT3 low deferred) | enable_lower_bound: false | illness/medication disclosed context | DEFERRED_NON_LAUNCH_CRITICAL | EXCLUDE_FROM_MINIMUM_COVERAGE |

---

## Phase 2 — Clinical authority assessment

### Androgen packages (8)

Governed medical review (`batch2_androgen_panel_medical_review_v1.yaml`) confirms frames are medically coherent but context-dependent. Context modifier binding exists (`batch2_androgen_context_modifier_binding_v1.yaml`) with `remains_blocked_for_promotion=true` for all 8 frames. **No androgen clinical sign-off artefact exists in the repository.** CF-BATCH2-010 remains Open.

**Question answered:** Is there enough governed clinical authority to activate safely in deterministic runtime? **NO** for all 8 packages.

### FT3 low

Thyroid panel sign-off exists at estate level but explicitly defers FT3 low. Package `signal_library.yaml` confirms `enable_lower_bound: false`. Required disclosed context (`illness_or_recovery_status_disclosed`, `thyroid_medication_disclosed`) cannot be satisfied for safe activation without activation-layer changes and explicit approval. Active thyroid trio (FT3 high, FT4 high/low) already provides minimum credible pre-beta thyroid coverage.

---

## Phase 3 — Minimum coverage decision

| Decision | Count | Packages |
|----------|-------|----------|
| ACTIVATE_WITH_GATES | 0 | — |
| EXCLUDE_FROM_MINIMUM_COVERAGE | 1 | pkg_kb47_free_t3_low_low_t3_syndrome |
| DEFER_PENDING_EXTERNAL_CLINICAL_AUTHORITY | 8 | all androgen packages |
| DO_NOT_ACTIVATE | 0 | — |

Authoritative register: `knowledge_bus/governance/batch2_minimum_coverage_decision_register_v1.yaml`

---

## Phase 4 — STOP gate table

| Package | Current state | Clinical authority | Runtime context complete? | Companion biomarkers complete? | Bounds correct? | Blockers resolved? | Recommended action | Evidence |
|---------|---------------|-------------------|----------------------------|-------------------------------|-----------------|-------------------|-------------------|----------|
| All 8 androgen | inactive | NO | partial | YES (where declared) | YES | NO — CF-BATCH2-010 | DEFER | No sign-off artefact; approval phrase absent |
| FT3 low | inactive | PARTIAL | partial | YES (TSH+FT4) | NO — enable_lower_bound false | NO | EXCLUDE | enable_lower_bound false; illness/medication blockers |

**CF-BATCH2-010 resolution:** NOT resolved. All androgen packages remain inactive.

**FT3 low blockers:** NOT resolved (`enable_lower_bound: false`; thyroid_medication_disclosed incomplete; illness context risk).

**Approval phrase:** `APPROVE BATCH2 MINIMUM COVERAGE ACTIVATION` — **NOT PRESENT**.

---

## Activation decision summary

| Package | Activated? |
|---------|------------|
| All 9 packages | **NO** |

---

## Confirmations

- No unauthorised activation occurred
- No package metadata changed
- No SSOT changed
- No scoring changed
- No report compiler changed
- No frontend changed
- No raw research runtime reads introduced
- No Intelligence Core code changed

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

### validate_day_one_architecture.py

```
day_one_architecture_validation: PASS
```

### validate_medical_frame_identity_index.py

```
validation_status: PASS
errors: 0
index_path: C:\Users\abroa\HealthIQ-AI-v5\knowledge_bus\governance\medical_frame_identity_index_v1.yaml
```

### validate_context_modifier_catalogue.py

```
validation_status: PASS
errors: 0
catalogue_path: C:\Users\abroa\HealthIQ-AI-v5\knowledge_bus\governance\context_modifier_catalogue_draft_v1.yaml
```

### check_no_secret_files.py

```
OK: no secret env files are git-tracked.
```

### Package validators (9/9 PASS)

All 9 packages validated with `validate_knowledge_package.py --package-dir`; each returned `manifest_validation: PASS`, `research_validation: PASS`, `signal_validation: PASS`, `ready_for_implementation: True`.

---

## Test output (full)

```
python -m pytest backend/tests/regression/test_runtime_context_evaluation.py backend/tests/regression/test_context_threading.py backend/tests/governance/test_batch2_context_clearance_register.py backend/tests/governance/test_batch2_minimum_coverage_decision_register.py -q

..........................................                               [100%]
42 passed
```

---

## Rollback path

Revert `batch2_minimum_coverage_decision_register_v1.yaml`, updates to `batch2_context_clearance_register_v1.yaml`, `context_runtime_execution_register_v1.yaml`, governance tests, carry-forward register, and this audit paper.

---

## Carry-forward impact

- **CF-BATCH2-010:** Remains **Open**. Notes updated with BATCH2-MINIMUM-COVERAGE-1 formal DEFER decisions.
- **FT3 low:** Explicitly **excluded from minimum pre-beta coverage**; remains inactive.
- **Androgen panel:** Deferred pending external clinical authority workflow.

---

## Recommended next action

Proceed to **ARCH-COMPLETION-2** with minimum biomarker estate explicitly defined (active thyroid trio + previously activated Batch 2 packages; excluding FT3 low and androgen panel until external sign-off). Run focused external medical authority/sign-off workflow before **BATCH2-ANDROGEN-EXECUTION-1**.
