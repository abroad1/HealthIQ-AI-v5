# ARCH-RT-2 Identity Runtime Pilot Report

**Work package:** ARCH-RT-2_identity_runtime_pilot  
**Date:** 2026-05-28  
**Status:** Complete (pilot scope)

## Pilot selected

| Field | Value |
|-------|-------|
| Signal family | `signal_alt_high` |
| Rationale | ADR-RT-002 preferred multi-frame pilot; ARCH-RT-0 documented 4-package collision |

## Package paths involved

| Package | Inferred `source_spec_id` | `activation_key` |
|---------|---------------------------|------------------|
| `pkg_kb52c_alt_high_hepatocellular_injury_pattern` | `inv_alt_high_hepatocellular_injury_pattern` | `signal_alt_high::inv_alt_high_hepatocellular_injury_pattern` |
| `pkg_kb52c_alt_high_metabolic_steatotic_liver_pattern` | `inv_alt_high_metabolic_steatotic_liver_pattern` | `signal_alt_high::inv_alt_high_metabolic_steatotic_liver_pattern` |
| `pkg_kb52c_alt_high_muscle_source_or_exertional_pattern` | `inv_alt_high_muscle_source_or_exertional_pattern` | `signal_alt_high::inv_alt_high_muscle_source_or_exertional_pattern` |
| `pkg_s24_alt_high_hepatocellular_injury` | `inv_alt_high_hepatocellular_injury` | `signal_alt_high::inv_alt_high_hepatocellular_injury` |

## Previous runtime behaviour

- `SignalRegistry` keyed by `signal_id` only.
- Duplicate `signal_id` → **lexicographic path overwrite** (silent collapse).
- **Winner:** `pkg_s24_alt_high_hepatocellular_injury` (path sorts last among ALT packages).
- **Discarded:** all three `pkg_kb52c_alt_high_*` frames.

## New runtime behaviour

- Registry keyed by **`activation_key`** (`signal_id::source_spec_id`).
- All **4** ALT frames loaded; **no overwrite**.
- Duplicate **`activation_key`** → `ValueError` (fail closed).
- `SignalEvaluator` evaluates **every** loaded frame; results sorted by `(signal_id, activation_key)`.
- `SignalResult` carries `activation_key`, `source_spec_id`, `package_id` plus existing `signal_id`.

## Activation key format

```text
{signal_id}::{source_spec_id}
```

Example: `signal_alt_high::inv_alt_high_metabolic_steatotic_liver_pattern`

**Provenance inference (no package file mutation):** `source_spec_id` from manifest `source_spec_id` if present, else `source_document` inv YAML stem, else `inv_{package_body}` from `package_id`.

## SignalResult provenance fields

| Field | Status |
|-------|--------|
| `signal_id` | Retained (family) |
| `activation_key` | **Added** (required) |
| `source_spec_id` | **Added** (required) |
| `package_id` | **Added** (required) |

Serialized through `model_dump()` into InsightGraph `signal_results`.

## Files changed

| File | Change |
|------|--------|
| `backend/core/knowledge/signal_activation_identity_v1.py` | **New** — activation_key resolution |
| `backend/core/analytics/signal_evaluator.py` | Multi-frame registry; provenance on results |
| `backend/core/models/signal.py` | SignalResult provenance fields |
| `backend/tests/unit/test_signal_evaluator.py` | ALT pilot + multi-frame / collision tests; s24 loader preference |
| `backend/tests/unit/test_signal_activation_identity_v1.py` | **New** — identity helper tests |
| `backend/tests/unit/test_orchestrator_unit_normalisation.py` | Expected payload fields |
| `backend/tests/unit/test_golden_panel_runner.py` | Stub SignalResult fields |

## Tests added/updated

- `test_signal_registry_alt_high_multi_frame_pilot`
- `test_signal_registry_multi_frame_preserves_distinct_signal_ids`
- `test_signal_registry_duplicate_activation_key_fails_closed`
- `test_signal_activation_identity_v1.py` (3 tests)
- Updated `_load_signal_definition` to prefer `pkg_s24_*` for KB-S24 harness

## Test commands

```powershell
cd backend
python -m pytest tests/unit/test_signal_evaluator.py -k "registry or duplicate or alt_high or override_loading" -q
python -m pytest tests/unit/test_signal_activation_identity_v1.py -q
python -m pytest tests/unit/test_orchestrator_unit_normalisation.py -q
```

## Test results

- ARCH-RT-2 focused signal registry tests: **PASS**
- Identity helper tests: **PASS**
- Orchestrator normalisation: **PASS** (after payload expectation update)

## Downstream impact assessment

| Consumer | Impact |
|----------|--------|
| **InsightGraph `signal_results`** | Additional fields per row; `signal_id` unchanged |
| **Root-cause compiler** | Still matches **first** row by `signal_id` only — **unchanged code**; multiple ALT frames may fire but WHY still keys on family id — **documented remaining risk** for ARCH-RT-3+ |
| **Report compiler / top findings** | May list multiple rows per `signal_id` if multiple frames fire — deterministic sort |
| **Interaction / phenotype maps** | Still family-level keys — **no code change** |
| **Domain score assembler** | Uses `signal_id` from results — family-level behaviour preserved |
| **Frontend** | Receives extra JSON fields; render-only — **not modified** |

## Remaining risks

1. `source_spec_id` inferred from manifests until packages regenerated with explicit fields.  
2. Root-cause registry not yet keyed by `activation_key`.  
3. Full estate may emit many more fired results when multiple frames activate.  
4. Golden panel / kbs23 catalogue tests not re-baselined in this sprint (pre-existing fixture issues).

## Compile manifest carry-forward

ARCH-RT-1 conditions **observed, not modified**:

- `compile_manifest_schema_v1.yaml` untouched  
- `validate_compile_manifest.py` untouched  
- No `compile_run_id` / `compile_id` logic added in this sprint

## Confirmations

- No package, investigation spec, PSI, root-cause YAML, card, or frontend files modified.  
- No helper scripts committed.  
- Activation compile vs PSI separation unchanged.
