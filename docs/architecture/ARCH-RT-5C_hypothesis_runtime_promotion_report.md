# ARCH-RT-5C — Hypothesis Runtime Promotion Report

**Generated:** 2026-05-30  
**Work package:** ARCH-RT-5C_hypothesis_runtime_promotion

## Pilot selected

**`signal_vitamin_d_low`** — single-frame, compiled artefact and manifest exist, divergence documented, legacy YAML retained.

## Artefact and manifest

| Item | Path |
|------|------|
| Artefact | `knowledge_bus/compiled/hypotheses/signal_vitamin_d_low.yaml` |
| Manifest | `knowledge_bus/compiled/manifests/arch_rt4_vitamin_d_hypothesis.yaml` |

## Runtime promotion mechanism

`compile_root_cause_v1()` detects `is_runtime_promoted_compiled_signal()` for the pilot and calls `_compile_compiled_hypothesis_finding()` instead of `_compile_finding()` + legacy YAML loader.

The bridge maps:

- `summary_template` → `RootCauseHypothesisV1.summary` via `runtime_summary_for_hypothesis(promoted=True)`
- Pre-evaluated `evidence_for` / `evidence_against` strings → `RootCauseEvidenceItemV1`
- No rule re-evaluation; no investigation-spec runtime reads

## summary_template policy

- Schema `runtime_promotion` block documents promoted signal ids and required fields.
- Validator requires `summary_template` for rows under `RUNTIME_PROMOTED_COMPILED_SIGNAL_IDS`.
- Missing template raises `CompiledHypothesisValidationError` on promoted path.

## physiological_claim boundary

Not emitted as runtime summary. Shadow path may still use fail-open fallback for comparison only.

## Compiler / registry changes

| File | Change |
|------|--------|
| `compiled_hypothesis.py` | `RUNTIME_PROMOTED_COMPILED_SIGNAL_IDS`, fail-closed summary, `validate_runtime_promoted_artefact()` |
| `compiled_hypothesis_registry_v1.py` | `is_runtime_promoted_compiled_signal()` |
| `root_cause_compiler_v1.py` | `_compile_compiled_hypothesis_finding()`, pilot-gated routing |
| `estate_index_v1.yaml` | Vitamin D `runtime_authority: runtime_promoted_compiled` |

## Legacy YAML preservation

`load_vitamin_d_low_hypotheses_v1()` and asset file unchanged. Runtime compiler skips legacy loader for promoted signal only.

## Tests

| Module | Coverage |
|--------|----------|
| `test_compiled_hypothesis_arch_rt5c.py` | Promotion gate, summary enforcement, compiler output, non-pilot stability, cross-load |
| `test_compiled_hypothesis_arch_rt4.py` | Existing shadow/legacy tests (unchanged behaviour) |
| `test_root_cause_v1_homocysteine.py` | Vitamin D + homocysteine regression |

**Command:** `pytest backend/tests/unit/test_compiled_hypothesis_arch_rt5c.py backend/tests/unit/test_compiled_hypothesis_arch_rt4.py backend/tests/unit/test_root_cause_v1_homocysteine.py -q`

## Remaining risks / carry-forwards

- Full root-cause estate migration deferred.
- `missing_data_policy` text not yet structured into `missing_data[]` at promotion (empty list for pilot).
- ARCH-RT-5D: explicit provenance backfill.
- ARCH-RT-5E: PSI runtime if mandated.
