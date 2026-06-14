# ARCH-COMPLETION-2 — Compiled Card and Root-Cause Authority Completion

---
work_id: ARCH-COMPLETION-2_compiled_card_and_root_cause_authority_completion
branch: work/ARCH-COMPLETION-2-compiled-card-and-root-cause-authority-completion
status: IMPLEMENTATION_COMPLETE
---

## Executive verdict

Day-one compiled analytical output authority chain is now governed end-to-end from activated signals through ReportV1 signal cards and root-cause findings. Three governance artefacts define allowed output element types, root-cause authority, and card authority. Runtime provenance metadata is attached additively to `ReportV1.output_authority_provenance_v1`. Untraceable `why_engine_fallback_v1` hypotheses are quarantined from clinician-facing output. No signal packages activated/deactivated; no SSOT, scoring, or frontend changes.

---

## Files inspected

- `backend/core/pipeline/orchestrator.py`, `orchestrator_phases_v1.py`
- `backend/core/analytics/signal_evaluator.py`, `report_compiler_v1.py`, `root_cause_compiler_v1.py`
- `backend/core/analytics/domain_score_assembler.py`, `interpretation_display_layer_publish_v1.py`
- `backend/core/analytics/insight_graph_builder.py` (Layer C heuristics)
- `backend/core/knowledge/root_cause_registry_v1.py`, `compiled_hypothesis_registry_v1.py`
- `backend/core/dto/builders.py`, `frontend_contract_v1.py`
- Prior audit papers: ARCH-COMPLETION-1, BATCH2-FULL-COVERAGE-ACTIVATION-1, DAY-ONE-ARCHITECTURE-CLOSURE-REVIEW

---

## Files changed

- `knowledge_bus/governance/compiled_output_authority_model_v1.yaml` (new)
- `knowledge_bus/governance/root_cause_authority_register_v1.yaml` (new)
- `knowledge_bus/governance/card_authority_register_v1.yaml` (new)
- `backend/core/contracts/output_authority_provenance_v1.py` (new)
- `backend/core/knowledge/compiled_output_authority_v1.py` (new)
- `backend/core/analytics/output_authority_provenance_builder_v1.py` (new)
- `backend/core/contracts/report_v1.py` — additive `output_authority_provenance_v1`
- `backend/core/analytics/report_compiler_v1.py` — provenance attach + quarantine why fallback from clinician path
- `backend/tests/regression/test_output_authority_provenance.py` (new)
- `backend/tests/governance/test_arch_completion_2_output_authority.py` (new)
- `backend/tests/unit/test_report_compiler_v1.py` — quarantine expectations
- `docs/sprints/launch_core_carry_forward_register.md`

**Not changed:** frontend, SSOT, scoring, signal package activation, clinical thresholds.

---

## Output-authority estate map (summary)

| Path | Authority status | Notes |
|------|------------------|-------|
| `SignalEvaluator` → `SignalResult` | GOVERNED_RUNTIME_AUTHORITY | Package gates + collision policy |
| `compile_report_v1` → `top_findings` | GOVERNED_RUNTIME_AUTHORITY | Signal cards with provenance |
| `compile_root_cause_v1` → legacy YAML | GOVERNED_MAPPING_AUTHORITY | LC-S18 41-target registry |
| `compile_root_cause_v1` → compiled hypothesis | GOVERNED_RUNTIME_AUTHORITY | Vitamin D promoted path |
| `why_engine_fallback_v1` | ROOT_CAUSE_UNTRACEABLE_BLOCKED | Quarantined from clinician output |
| `assemble_consumer_domain_scores_v1` | GOVERNED_RUNTIME_AUTHORITY | Compiled card evidence |
| `publish_interpretation_display_layer_v1` | GOVERNED_RUNTIME_AUTHORITY | IDL YAML + fired signals |
| `_build_layer_c_features` | CARD_LEGACY_QUARANTINED | Inline heuristics, non-primary |
| `assemble_layer3_insights` | CARD_LEGACY_QUARANTINED | Tooling/tests only |

---

## Compiled output authority model summary

Defines nine output element types (`signal_card`, `root_cause_card`, `system_summary`, …), forbidden runtime inputs (raw Pass 3 JSON, investigation specs, LLM clinical reasoning), fail-closed default, and frontend render-only boundary.

---

## Root-cause authority audit result

- 41 LC-S18 YAML targets: `ROOT_CAUSE_GOVERNED_ACTIVE`
- 1 compiled promoted signal (vitamin D): `ROOT_CAUSE_GOVERNED_ACTIVE`
- `why_engine_fallback_v1`: `ROOT_CAUSE_UNTRACEABLE_BLOCKED` — quarantined
- Batch 2 activated thyroid/androgen signals: `ROOT_CAUSE_REQUIRES_FUTURE_MAPPING` (signal cards only)
- Batch 2 inactive DHEA/FAI-low/pct: `ROOT_CAUSE_GOVERNED_INACTIVE`

---

## Card authority audit result

- `signal_card`, `consumer_domain_card`, `interpretation_display_layer_card`: `CARD_GOVERNED_ACTIVE`
- `layer3_insight_card`, `layer_c_feature_card`: `CARD_LEGACY_QUARANTINED`

---

## Legacy path remediation

- `why_engine_fallback_v1` filtered from `compile_clinician_report_v1` hypothesis normalisation
- Provenance bundle lists quarantined vs governed elements explicitly
- Layer C / Layer 3 paths classified quarantined in card register (no runtime emission change beyond documentation + tests)

---

## Provenance implementation details

`ReportV1.output_authority_provenance_v1` contains:
- `governed_elements[]` — traceable signal cards and root-cause cards
- `quarantined_elements[]` — inactive signal cards, blocked root-cause fallbacks
- Per-element: `output_element_id`, `output_element_type`, `source_signal_ids`, `source_package_ids`, `authority_status`, `generated_by`

Additive only — existing DTO root keys unchanged.

---

## Active signal estate integration

- FT3 low / FAI high / FT high / FT low: signal cards traceable when gates pass; suppressed when gates fail (regression suite unchanged)
- DHEA inactive: no signal emission, no signal cards
- Inactive packages do not produce analytical conclusions

---

## Confirmations

- No signal packages activated or deactivated
- No SSOT changes
- No scoring changes
- No frontend changes
- No raw Pass 3 runtime reads introduced
- No diagnosis wording introduced
- No treatment/supplement recommendations introduced

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

### check_no_secret_files.py

```
OK: no secret env files are git-tracked.
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
collected 80 items

backend\tests\regression\test_output_authority_provenance.py .......     [  8%]
backend\tests\regression\test_runtime_context_evaluation.py ............ [ 23%]
................                                                         [ 43%]
backend\tests\regression\test_context_threading.py .........             [ 55%]
backend\tests\regression\test_batch2_full_coverage_activation.py ....... [ 63%]
.............                                                            [ 80%]
backend\tests\governance\test_arch_completion_2_output_authority.py .... [ 85%]
.                                                                        [ 86%]
backend\tests\unit\test_report_compiler_v1.py ...........                [100%]

============================= 80 passed in 8.62s ==============================
```

---

## Rollback path

Revert governance YAML files, provenance contracts/builder, `ReportV1.output_authority_provenance_v1` field, compiler quarantine filter, tests, audit paper, and carry-forward updates.

---

## Carry-forward impact

- **CF-ARCHLEG1-001**: Partially addressed — authority model + registers classify dual root-cause path; full YAML→compiled migration still deferred to ARCH-RT-4+
- **CF-ARCH-COMPLETION-2-RC-1** (new): Batch 2 activated signals lack root-cause YAML registration — signal cards only until mapping sprint

---

## Recommended next action

Claude audit → GPT architectural review → human approval → merge → ARCH-COMPLETION-3 full traceability manifest and launch estate gate.
