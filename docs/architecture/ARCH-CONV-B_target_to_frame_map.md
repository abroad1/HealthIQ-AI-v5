# ARCH-CONV-B — Target-to-Frame and Canonical-Source Map

**Work ID:** `ARCH-CONV-B`  
**Date (UTC):** 2026-07-30  
**Purpose:** STOP A identity/source map only; no medical decision, compile, activation, or legacy disconnection.

Identity model:

```text
signal_id      = signal-family identity
source_spec_id = embedded canonical investigation identity
activation_key = signal_id::source_spec_id
```

## Scope summary

| Category | Count | Identities |
|---|---:|---|
| Migration targets | 2 | creatinine high; urea high |
| Cross-signal authority boundary | 1 signal / 2 frames | eGFR low chronic; eGFR low hemodynamic |
| Explicitly excluded | 1 | urate high |
| Compiled renal WHY frames active | 0 | none |
| Active legacy WHY targets in migration scope | 2 | creatinine high; urea high |

## Frame map

| Scope role | signal_id | source_spec_id | activation_key | source type | current causal-WHY state | readiness / disposition |
|---|---|---|---|---|---|---|
| Migration target | `signal_creatinine_high` | `inv_creatinine_high_renal` | `signal_creatinine_high::inv_creatinine_high_renal` | Canonical investigation spec | Legacy WHY active | `CANONICAL_RESEARCH_AVAILABLE_COMPILE_INCOMPLETE`; medical disposition pending |
| Parallel candidate | `signal_creatinine_high` | `inv_creatinine_high_reduced_glomerular_filtration` | `signal_creatinine_high::inv_creatinine_high_reduced_glomerular_filtration` | Package-only Pass 3 | No compiled WHY | `PACKAGE_ONLY_MEDICAL_DISPOSITION_REQUIRED` |
| Boundary only | `signal_egfr_low` | `inv_egfr_low_chronic_kidney_function_reduction` | `signal_egfr_low::inv_egfr_low_chronic_kidney_function_reduction` | Canonical investigation spec + active signal package | No causal-WHY registry entry | `ADJACENT_PRESERVE_NOT_COMPILE` |
| Boundary only | `signal_egfr_low` | `inv_egfr_low_hemodynamic_filtration_drop` | `signal_egfr_low::inv_egfr_low_hemodynamic_filtration_drop` | Canonical investigation spec + active signal package | No causal-WHY registry entry | `ADJACENT_PRESERVE_NOT_COMPILE` |
| Migration target | `signal_urea_high` | `inv_urea_high_renal` | `signal_urea_high::inv_urea_high_renal` | Canonical investigation spec | Legacy WHY active | `CANONICAL_RESEARCH_AVAILABLE_COMPILE_INCOMPLETE`; medical disposition pending |
| Parallel candidate | `signal_urea_high` | `inv_urea_high_prerenal_volume_depletion_or_catabolic_load` | `signal_urea_high::inv_urea_high_prerenal_volume_depletion_or_catabolic_load` | Package-only Pass 3 | No compiled WHY | `PACKAGE_ONLY_MEDICAL_DISPOSITION_REQUIRED` |
| Excluded | `signal_urate_high` | `inv_uric_acid_high_metabolic` | `signal_urate_high::inv_uric_acid_high_metabolic` | Canonical investigation spec, metabolic domain | Legacy WHY active | `OUT_OF_SCOPE_DEFERRED` |
| Excluded parallel | `signal_urate_high` | `inv_urate_high_gout_crystal_deposition_risk` | `signal_urate_high::inv_urate_high_gout_crystal_deposition_risk` | Package-only Pass 3 | No compiled WHY | `OUT_OF_SCOPE_DEFERRED` |

## Source map

### Canonical investigation specs

| activation_key | Path | Embedded identity evidence |
|---|---|---|
| `signal_creatinine_high::inv_creatinine_high_renal` | `knowledge_bus/research/investigation_specs/inv_creatinine_high_renal_v1.yaml` | lines 1-2 |
| `signal_urea_high::inv_urea_high_renal` | `knowledge_bus/research/investigation_specs/inv_urea_high_renal.yaml` | lines 1-2 |
| `signal_egfr_low::inv_egfr_low_chronic_kidney_function_reduction` | `knowledge_bus/research/investigation_specs/inv_egfr_low_chronic_kidney_function_reduction.yaml` | lines 2-3 |
| `signal_egfr_low::inv_egfr_low_hemodynamic_filtration_drop` | `knowledge_bus/research/investigation_specs/inv_egfr_low_hemodynamic_filtration_drop.yaml` | lines 2-3 |
| `signal_urate_high::inv_uric_acid_high_metabolic` | `knowledge_bus/research/investigation_specs/inv_uric_acid_high_metabolic.yaml` | lines 1-2 |

### Legacy WHY

| signal_id | Registry | Loader | Asset |
|---|---|---|---|
| `signal_creatinine_high` | `backend/core/knowledge/root_cause_registry_v1.py:89` | `load_root_cause_hypotheses.py:171-172` | `knowledge_bus/root_cause/hypotheses/creatinine_high_hypotheses_v1.yaml` |
| `signal_urea_high` | `backend/core/knowledge/root_cause_registry_v1.py:90` | `load_root_cause_hypotheses.py:175-176` | `knowledge_bus/root_cause/hypotheses/urea_high_hypotheses_v1.yaml` |
| `signal_urate_high` | `backend/core/knowledge/root_cause_registry_v1.py:91` | `load_root_cause_hypotheses.py:179-180` | `knowledge_bus/root_cause/hypotheses/urate_high_hypotheses_v1.yaml` |

`signal_egfr_low` has no row in that registry. None of these four signal families has a row in `knowledge_bus/governance/compiled_why_authority_register_v1.yaml`.

### Package records

| Frame | Package |
|---|---|
| Creatinine S24 | `knowledge_bus/packages/pkg_s24_creatinine_high_renal/` |
| Creatinine Pass 3 parallel | `knowledge_bus/packages/pkg_kb52c_creatinine_high_reduced_glomerular_filtration/` |
| Creatinine non-runtime promoted duplicate | `knowledge_bus/generated_pilot/kb_util_2_pilot/promoted_candidates/pkg_creatinine_high_renal_pass3_v1/` |
| Urea S24 | `knowledge_bus/packages/pkg_s24_urea_high_renal/` |
| Urea Pass 3 parallel | `knowledge_bus/packages/pkg_kb52c_urea_high_prerenal_volume_depletion_or_catabolic_load/` |
| eGFR chronic | `knowledge_bus/packages/pkg_kb47_egfr_low_chronic_kidney_function_reduction/` |
| eGFR hemodynamic | `knowledge_bus/packages/pkg_kb47_egfr_low_hemodynamic_filtration_drop/` |
| Urate S24, excluded | `knowledge_bus/packages/pkg_s24_urate_high_metabolic/` |
| Urate gout/crystal parallel, excluded | `knowledge_bus/packages/pkg_kb52c_urate_high_gout_crystal_deposition_risk/` |

The Pass 3 creatinine, urea, and urate parallel identities have no standalone peer investigation-spec YAML. Package or filename identity must not be promoted to canonical source authority by inference.

## Creatinine/eGFR boundary contract

1. `signal_creatinine_high` and `signal_egfr_low` are distinct signal families.
2. The two eGFR frames are not duplicates of the creatinine activation key.
3. eGFR signal authority is already runtime active under `renal_filtration_axis`.
4. eGFR primacy may suppress duplicate user-facing creatinine filtration signal presentation.
5. That signal collision policy does not create eGFR causal-WHY authority.
6. A future creatinine compiled WHY frame may consume only medically ratified eGFR supporting/severity context.
7. Creatinine must never emit `signal_egfr_low` causal WHY or prevent future standalone eGFR WHY migration.
8. ARCH-CONV-B Phase 0 changes none of the existing collision behaviour.

## Evidence-gap map

| Frame | Confirmed evidence | Gap / ambiguity | Gate implication |
|---|---|---|---|
| Creatinine S24 | eGFR/urea/potassium support; muscle mass, creatine, dehydration confounders | No structured UACR; no chronicity/serial input; overlap with reduced-GFR Pass 3 | Narrow/context/defer/cause decision required |
| Creatinine Pass 3 | Reduced-GFR package framing | Package-only; no peer canonical inv YAML | Cannot become causal authority by package inference |
| eGFR chronic | UACR/cystatin C and chronicity safeguards | Not a B compile target | Preserve as distinct future WHY candidate |
| eGFR hemodynamic | Creatinine/cystatin C, trajectory, illness/medication safeguards | Not a B compile target | Preserve as distinct future WHY candidate |
| Urea S24 | Creatinine concordance, Hb differential, protein/dehydration confounders | Thin source; catabolic/steroid context not structured | Narrow/context/defer/cause decision required |
| Urea Pass 3 | Prerenal volume-depletion/catabolic framing | Package-only; no peer canonical inv YAML | Cannot be silently merged or activated |
| Urate | Metabolic canonical source plus gout/crystal parallel | Mixed domain and wider rollback boundary | Entire family deferred out of B |

## Canonical test and validation map

| Concern | Existing authority/pattern |
|---|---|
| Legacy WHY reachability | `backend/tests/unit/test_root_cause_v1_homocysteine.py` renal legacy assertions |
| Signal collision / eGFR primacy | `backend/tests/regression/test_signal_authority_collision_enforcement.py` |
| Activation identity | `backend/tests/unit/test_signal_activation_identity_v1.py` |
| Named duplicate authority / fail closed | `backend/tests/unit/test_duplicate_authority_resolution_v1.py` |
| WHY selection / legacy disconnection pattern | `backend/tests/unit/test_why_authority_pkg3.py` |
| Context-only causal prohibition | `backend/tests/unit/test_arch_conv_a_wave1_thyroid_stop_c.py` and Wave 2 STOP C tests |
| Frame identity/provenance | `backend/tests/unit/test_arch_conv_pkg1_frame_identity.py`; `test_arch_conv_pkg2_provenance_reachability.py` |
| Kidney signal/domain behaviour | `backend/tests/unit/test_p1_2_kidney_domain_card.py`; `test_signal_evaluator.py` |
| Compiled WHY validation | `backend/scripts/validate_compiled_why_authority_gate.py` |
| Knowledge package validation | `backend/scripts/validate_knowledge_package.py`; `validate_promoted_signal_intelligence.py` |

No parallel test authority is created during STOP A. Renal compile/runtime tests are a later post-ratification requirement.

## STOP A disposition

| Identity | Current disposition |
|---|---|
| Creatinine canonical | `PENDING_INDEPENDENT_STOP_A_AND_MEDICAL_GATE` |
| Creatinine Pass 3 parallel | `PENDING_MEDICAL_ROLE_DECISION` |
| eGFR chronic | `ADJACENT_PRESERVE_NOT_COMPILE` |
| eGFR hemodynamic | `ADJACENT_PRESERVE_NOT_COMPILE` |
| Urea canonical | `PENDING_INDEPENDENT_STOP_A_AND_MEDICAL_GATE` |
| Urea Pass 3 parallel | `PENDING_MEDICAL_ROLE_DECISION` |
| Urate canonical and parallel | `OUT_OF_SCOPE_DEFERRED` |

No row in this map constitutes medical approval or runtime authority.
