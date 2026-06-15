# DHEA-DHEAS-CANONICALISATION-1 — Unit-Aware Marker Identity and Adrenal Androgen Resolution

---
work_id: DHEA-DHEAS-CANONICALISATION-1_unit_aware_marker_identity_and_adrenal_androgen_resolution
branch: work/DHEA-DHEAS-CANONICALISATION-1-unit-aware-marker-identity-and-adrenal-androgen-resolution
status: IMPLEMENTATION_COMPLETE_PENDING_REAUDIT
gpt_architectural_ruling: identity_and_canonicalisation_approved_activation_not_approved
---

## Executive verdict

**GPT architectural ruling (retry applied):** DHEA/DHEA-S identity remediation and unit-aware canonicalisation are approved. DHEA-S high runtime activation is **not** approved — external clinician sign-off is required and is not satisfied by deterministic gates or product-owner merge approval.

**Sprint outcome after retry:**

- Unit-aware canonicalisation resolves AB panel `DHEA (Venous)` + umol/L + 0.94–15.44 range → `dhea_s` with `HIGH_CONFIDENCE_UNIT_RANGE_MATCH`
- Label-only `DHEA` without unit/range fails closed
- `pkg_kb47_dhea_high_androgen_excess_context` identity remediated (`primary_metric: dhea_s`) but **remains inactive** (`inactive_pending_external_clinician_signoff`)
- DHEA low remains inactive
- No frontend, scoring, or report compiler changes

**Do not merge** until Claude re-audit and human approval.

---

## GPT architectural ruling (recorded)

| Item | Ruling |
|------|--------|
| DHEA/DHEA-S identity remediation | Approved |
| Unit-aware canonicalisation | Approved |
| Alias registry cleanup | Approved |
| DHEA-S high runtime activation | **Not approved** |
| DHEA low runtime activation | **Not approved** |

**Reason:** Medical research authority requires external clinician sign-off before DHEA high / DHEA-S high activation. Implementing deterministic gates does not satisfy that requirement.

---

## Files inspected

- `backend/ssot/biomarker_alias_registry.yaml`, `biomarkers.yaml`
- `backend/core/canonical/alias_registry_service.py`, `normalize.py`, `unit_aware_biomarker_identity_v1.py`
- `backend/tests/fixtures/panels/ab_full_panel_with_ranges.json`
- `knowledge_bus/packages/pkg_kb47_dhea_high_androgen_excess_context/`
- `knowledge_bus/packages/pkg_kb47_dhea_low_adrenal_androgen_reduction/`
- `knowledge_bus/research/medical_reviews/batch2_thyroid_androgen_context_authority_review_v1.md`
- Governance registers and medical frame identity index

---

## Files changed

- `knowledge_bus/governance/unit_aware_biomarker_canonicalisation_model_v1.yaml` — `runtime_consumed: false`; activation policy inactive pending sign-off
- `backend/core/canonical/unit_aware_biomarker_identity_v1.py`
- `backend/core/canonical/normalize.py`
- `backend/core/models/biomarker.py`
- `backend/ssot/biomarker_alias_registry.yaml`
- `knowledge_bus/packages/pkg_kb47_dhea_high_androgen_excess_context/` — identity remediated; `behavioural_impact: NONE`
- `knowledge_bus/governance/batch2_full_coverage_activation_execution_register_v1.yaml` — DHEA high in `kept_inactive_packages`
- `knowledge_bus/governance/medical_frame_identity_index_v1.yaml` — `runtime_authority_status: inactive`
- `knowledge_bus/governance/day_one_full_traceability_manifest_v1.yaml`
- `backend/scripts/validate_day_one_launch_estate_gate.py`
- Tests and carry-forward register

---

## DHEA / DHEA-S identity audit

| Finding | Result |
|---------|--------|
| Identity conclusion for AB panel | **DHEA_S_CONFIRMED** |
| DHEA and DHEA-S conflated in alias registry | **Yes — remediated** |
| Sample evidence | `ab_full_panel_with_ranges.json` — 5.12 umol/L, range 0.94–15.44 |

---

## Canonicalisation model summary

**Artefact:** `knowledge_bus/governance/unit_aware_biomarker_canonicalisation_model_v1.yaml`

- `runtime_consumed: false` — implementation authority in Python module, not YAML-driven runtime config
- `dhea_s_high_activation_policy: KEEP_INACTIVE_PENDING_EXTERNAL_CLINICIAN_SIGNOFF`
- `dhea_low_activation_policy: DHEA_LOW_DO_NOT_ACTIVATE_EVIDENCE_INSUFFICIENT`

---

## DHEA-S high package outcome (retry)

**Outcome:** `RENAME_TO_DHEA_S_HIGH_KEEP_INACTIVE_PENDING_GATES`

- `primary_metric: dhea_s` (identity remediated)
- `governance_runtime_activation_status: inactive_pending_external_clinician_signoff`
- `behavioural_impact: NONE`
- Not in `activated_packages`; recorded in `kept_inactive_packages` with `IDENTITY_RESOLVED_PRIMARY_METRIC_DHEA_S`

---

## DHEA / DHEA-S low package outcome

**Outcome:** `DHEA_LOW_DO_NOT_ACTIVATE_EVIDENCE_INSUFFICIENT` — remains inactive

---

## Confirmations

- Raw label/unit/range preserved where supported
- No label-only DHEA → DHEA-S remap
- No DHEA-S high runtime activation
- No DHEA low activation
- No frontend, scoring, or report compiler changes
- No diagnosis or treatment wording introduced

---

## Validator output (full)

```
validation_status: PASS
errors: 0
index_path: .../medical_frame_identity_index_v1.yaml
validation_status: PASS
errors: 0
catalogue_path: .../context_modifier_catalogue_draft_v1.yaml
day_one_architecture_validation: PASS
day_one_launch_estate_gate: PASS
medical_intelligence_architecture_validation: PASS
.......s..                                                               [100%]
SKIPPED [1] test_medical_intelligence_architecture_sentinels.py:67
.....................                                                    [100%]
[architecture-gate] validate_medical_frame_identity_index
[architecture-gate] validate_context_modifier_catalogue
[architecture-gate] validate_day_one_architecture
[architecture-gate] validate_day_one_launch_estate_gate
[architecture-gate] validate_medical_intelligence_architecture
[architecture-gate] pytest_architecture_guardrails
[architecture-gate] pytest_governance_regression
architecture_validation_gate: PASS
day_one_launch_estate_gate: PASS
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
collected 84 items

backend\tests\regression\test_runtime_context_evaluation.py ............ [ 14%]
................                                                         [ 33%]
backend\tests\regression\test_context_threading.py .........             [ 44%]
backend\tests\regression\test_batch2_full_coverage_activation.py ....... [ 52%]
.............                                                            [ 67%]
backend\tests\regression\test_output_authority_provenance.py ........... [ 80%]
..                                                                       [ 83%]
backend\tests\regression\test_dhea_dheas_canonicalisation.py ...         [ 86%]
backend\tests\regression\test_dhea_s_high_remains_inactive.py ..         [ 89%]
backend\tests\governance\test_dhea_dheas_canonicalisation_governance.py . [ 90%]
..                                                                       [ 92%]
backend\tests\unit\test_unit_aware_biomarker_identity_v1.py ......       [100%]

============================= 84 passed in 10.16s =============================
```

---

## Carry-forward impact

- **CF-DHEA-IDENTITY-001**: Resolved
- **CF-DHEA-S-ACTIVATION-001** (new): Open — external clinician sign-off required before DHEA-S high activation
- **CF-BATCH2-010**: Open — 5 androgen packages remain inactive

---

## Rollback path

Revert governance model, identity resolver, alias registry, normalize/BiomarkerValue changes, package metadata, registers, tests, and audit paper.

---

## Recommended next action

Claude re-audit → human approval → merge (only after re-audit passes)
