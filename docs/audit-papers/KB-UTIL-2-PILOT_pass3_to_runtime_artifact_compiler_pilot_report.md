# KB-UTIL-2-PILOT — Pass 3 to Runtime Artefact Compiler Pilot Report

**Work ID:** `KB-UTIL-2-PILOT_pass3_to_runtime_artifact_compiler_pilot`  
**Date:** 2026-06-01  
**Risk:** HIGH (compiler + generated artefacts; no runtime wiring)  
**Compiler:** `backend/scripts/compile_pass3_pilot_artifacts.py` (`kb_util2_pass3_pilot_compiler_v1.0.0`)

---

## Executive verdict

The first **deterministic** Pass 3 → pilot package compiler path is implemented and validated for **two ROUTE_A** packages. Generated artefacts live under `knowledge_bus/generated_pilot/kb_util_2_pilot/` and are **not runtime-active**. No manual LLM extraction was used. No runtime packages were overwritten.

**Pilot proves** that Pass 3 JSON can be parsed, mapped, compiled, structurally validated, and source-field audited. Sufficient to plan a broader ROUTE_A compile wave after promotion-pilot hardening.

---

## Pilot package selection

| package_id | Pass 3 spec_id | Pass 3 file | Frames | Route |
|---|---|---|---|---|
| `pkg_s24_creatinine_high_renal` | `inv_creatinine_high_reduced_glomerular_filtration` | `Batch_4_Pass_3.json` | 1 (exact signal) | ROUTE_A |
| `pkg_s24_ferritin_low_iron_deficiency` | `inv_ferritin_low_iron_store_depletion` | `Batch_4_Pass_3.json` | 1 (exact signal) | ROUTE_A |

Comparison-only (not compiled): `pkg_lipid_transport`, `pkg_chronic_inflammation` per sprint scope.

---

## Generated artefacts (per pilot)

Under `knowledge_bus/generated_pilot/kb_util_2_pilot/<package_id>/`:

- `research_brief.yaml`
- `signal_library.yaml`
- `package_manifest.yaml`
- `promoted_signal_intelligence.yaml`
- `compile_manifest.yaml`
- `source_field_preservation_audit.yaml`

Governance index: `knowledge_bus/governance/pass3_pilot_compile_manifest_index_v1.yaml`

---

## Source-field preservation summary

All Pass 3 top-level fields are accounted for in `source_field_preservation_audit.yaml`:

| Field | Disposition |
|---|---|
| `primary_marker`, `activation`, `states`, `supporting_markers`, `override_rules`, `confirmatory_tests`, `evidence` | Preserved → package / PSI |
| `narrative` | Partially preserved → `signal_library.explanation` |
| `hypotheses`, `hypothesis_ranking` | Deferred → `ROOT_CAUSE_FUTURE` (contradiction markers extracted to PSI) |

Rich content explicitly not silently dropped: supporting marker roles/rationale, ranked hypotheses (deferred), contradiction markers (PSI), confirmatory tests, override rules, evidence sources.

---

## Validation results

| Check | Result |
|---|---|
| `validate_knowledge_package.py` (creatinine pilot) | PASS — `ready_for_implementation: True` |
| `validate_knowledge_package.py` (ferritin pilot) | PASS — `ready_for_implementation: True` |
| `validate_day_one_architecture.py` | PASS |
| `test_day_one_architecture_guardrails.py` | 4 passed |
| `test_kb_util2_pass3_pilot_compiler.py` | All passed |

---

## Deterministic output evidence

Re-running `compile_pass3_pilot_artifacts.py` produces **identical** `compile_manifest.yaml` SHA-256 hashes (regression test `test_compiler_deterministic_hashes`).

---

## Behavioural parity / divergence (pilot vs legacy runtime)

Classification only — **not resolved** in this sprint.

### `pkg_s24_creatinine_high_renal`

| Dimension | Legacy runtime | Pilot generated | Classification |
|---|---|---|---|
| `signal_id` | `signal_creatinine_high` | Match | Aligned |
| Primary biomarker | `creatinine` | Match | Aligned |
| `activation_logic` | `lab_range_exceeded` | Match | Aligned |
| Supporting biomarkers | `egfr`, `urea`, `potassium` | `egfr`, `uacr`, `cystatin_c` | **Divergence** — Pass 3 spec markers differ from s24 translation |
| Override rules | eGFR & potassium numeric thresholds | UACR lab-range boundary | **Divergence** — Pass 3 uses lab-range comparator; legacy uses fixed values |
| Rich PSI | N/A (legacy package has no PSI file) | Full PSI from Pass 3 | **Enhancement** — not runtime-wired |

### `pkg_s24_ferritin_low_iron_deficiency`

| Dimension | Legacy runtime | Pilot generated | Classification |
|---|---|---|---|
| `signal_id` | `signal_ferritin_low` | Match | Aligned |
| Primary biomarker | `ferritin` | Match | Aligned |
| Supporting biomarkers | includes `mcv`, `mch`, `transferrin` | `iron`, `hemoglobin`, `crp` | **Divergence** — Pass 3 vs s24 cohort |
| Override rules | Hb/MCV/ferritin numeric thresholds | Hb lab-range boundary per Pass 3 | **Divergence** — promotion requires adjudication |
| Rich PSI | N/A | Generated | **Enhancement** |

**Promotion safety:** Generated pilots are structurally valid but **not safe for blind runtime replacement** without semantic review of supporting-marker and override-rule divergence.

---

## Confirmations

- No runtime wiring (`SignalEvaluator`, loaders, `knowledge_bus/current/latest_knowledge_status.json` unchanged).
- No manual LLM extraction — compiler-only path.
- No overwrite of `knowledge_bus/packages/*` runtime packages.
- Generated outputs marked `pilot_status: generated_non_runtime`, `runtime_active: false`.

---

## Recommended next sprint

**KB-UTIL-2-PROMOTE-PILOT** (or continuation): wire promotion gate for one ROUTE_A package after clinical sign-off on divergence table; extend compiler to additional ROUTE_A s24 packages; keep ROUTE_C adjudication packages out of bulk compile.

**CF-KBUTIL1-001** remains open — this pilot replaces ad-hoc manual enrichment for two packages only; estate-wide automated pipeline still required.

---

## ROUTE_A bulk wave judgement

**Conditional go:** Two-package pilot validates deterministic compile + validation + preservation audit. **Do not** bulk-promote 13 ROUTE_A packages until override/supporting-marker divergence policy is defined and promotion harness exists.
