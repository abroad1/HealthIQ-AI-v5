# KB-UTIL-2-PROMOTE-PILOT — ROUTE_A Single Package Promotion Report

**Work ID:** `KB-UTIL-2-PROMOTE-PILOT_route_a_single_package_promotion`  
**Date:** 2026-06-02  
**Selected package:** `pkg_s24_creatinine_high_renal`  
**Promoted package path:** `knowledge_bus/packages/pkg_creatinine_high_renal_pass3_v1`

---

## Executive verdict

One ROUTE_A package was promoted into a **new immutable package directory** (legacy package preserved). Advisory 1 and Advisory 2 from KB-UTIL-2-PILOT were resolved. Validators pass for the promoted package and promoted signal intelligence. No runtime evaluator/frontend code changes were made and no manual LLM extraction was used.

Runtime activation is deferred in this sprint (`compiled_not_promoted`) to avoid unintended behavioural change without promotion harness hardening.

---

## Selected package and source mapping

| Item | Value |
|---|---|
| Selected legacy package | `pkg_s24_creatinine_high_renal` |
| Legacy package path | `knowledge_bus/packages/pkg_s24_creatinine_high_renal` |
| Generated pilot path | `knowledge_bus/generated_pilot/kb_util_2_pilot/pkg_s24_creatinine_high_renal` |
| Source Pass_3 path | `knowledge_bus/research/investigation_specs/multi_llm_research/Batch_4_Pass_3.json` |
| Source spec_id | `inv_creatinine_high_reduced_glomerular_filtration` |
| Source signal_id | `signal_creatinine_high` |
| Source primary biomarker | `creatinine` |
| Exact signal_id match | yes |
| Single Pass_3 frame | yes |

---

## Advisory resolutions

### Advisory 1 — preservation audit path discrepancy

- **Issue:** preservation audit pointed to `compile_manifest.yaml#source_contract_version` but field was previously absent.
- **Fix:** compiler now writes `source_contract_version` into `compile_manifest.yaml`.
- **Result:** audit pointer is now accurate and test-covered.

### Advisory 2 — generated signal_library schema version

- **Issue:** generated signal_library used `schema_version: "2.0.0"` without approved schema migration.
- **Decision:** use `schema_version: "1.0.0"` for promoted artefacts in this sprint.
- **Rationale:** avoid unapproved schema advancement; maintain current governed compatibility.
- **Result:** compiler updated and test-covered.

---

## Validation results

| Command | Result |
|---|---|
| `python backend/scripts/validate_knowledge_package.py --package-dir knowledge_bus/packages/pkg_creatinine_high_renal_pass3_v1` | PASS (`ready_for_implementation: True`) |
| `python backend/scripts/validate_promoted_signal_intelligence.py --model knowledge_bus/packages/pkg_creatinine_high_renal_pass3_v1/promoted_signal_intelligence.yaml` | PASS |
| `python backend/scripts/validate_day_one_architecture.py` | PASS |
| `python -m pytest backend/tests/architecture/test_day_one_architecture_guardrails.py -q` | PASS |
| `python -m pytest backend/tests/regression/test_kb_util2_pass3_pilot_compiler.py -q` | PASS |

---

## Behavioural parity / divergence classification

| Dimension | Classification | Notes |
|---|---|---|
| signal_id | NO_DIFFERENCE | `signal_creatinine_high` retained |
| primary biomarker | NO_DIFFERENCE | `creatinine` retained |
| activation logic | NO_DIFFERENCE | `lab_range_exceeded` retained |
| thresholds | STRUCTURAL_ONLY | placeholder remains lab-range driven |
| supporting markers | RICHNESS_GAIN_ONLY | Pass_3 set differs from s24 translation but retained in richer PSI structure |
| override rules | RICHNESS_GAIN_ONLY | Pass_3 rule logic preserved with boundary comparator semantics |
| Overall | RICHNESS_GAIN_ONLY | accepted with rationale for pilot promotion mechanics |

No `BEHAVIOURAL_DIFFERENCE_HIGH` or `CLINICAL_ADJUDICATION_REQUIRED` classification in this selected package path.

---

## Legacy package treatment

- Legacy package kept unchanged: `knowledge_bus/packages/pkg_s24_creatinine_high_renal`
- New promoted package created: `knowledge_bus/packages/pkg_creatinine_high_renal_pass3_v1`
- Governance classification for legacy: `superseded_by_pass3_package` (traceability retained)

---

## Source-field preservation summary

`source_field_preservation_audit.yaml` exists for promoted source and accounts for all required Pass_3 top-level fields.

- Preserved: activation/states/supporting_markers/override_rules/evidence/confirmatory_tests
- Partially preserved: narrative → signal_library explanation
- Deferred with reason: hypotheses and hypothesis_ranking (`ROOT_CAUSE_FUTURE`)

---

## Runtime status

- `knowledge_bus/current/latest_knowledge_status.json`: **not updated**
- Sprint classification: **compiled_not_promoted**
- No runtime code wiring performed.

---

## Confirmations

- No manual LLM extraction was used for artefact generation or promotion.
- No changes to `SignalEvaluator`, `SignalRegistry`, loaders, frontend, SSOT, scoring thresholds, or unit conversion.
- No legacy package overwrite.

---

## Recommended next sprint

`KB-UTIL-2-PROMOTE-WIRE-1` (or equivalent): promotion harness wiring + controlled activation gate for one promoted package, with explicit runtime authority switch controls and rollback path.

