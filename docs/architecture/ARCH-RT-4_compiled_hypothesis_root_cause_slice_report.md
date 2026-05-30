# ARCH-RT-4 Compiled Hypothesis / Root-Cause Slice Report

**Work package:** `ARCH-RT-4_compiled_hypothesis_root_cause_slice`  
**Branch:** `work/ARCH-RT-4-compiled-hypothesis-root-cause-slice`  
**Generated:** 2026-05-30

## Pilot selected

| Field | Value |
|-------|-------|
| Signal | `signal_vitamin_d_low` |
| activation_key | `signal_vitamin_d_low::inv_vitamin_d_low_deficiency` |
| Legacy YAML | `vitamin_d_low_hypotheses_v1.yaml` |
| Compile source | `inv_vitamin_d_low_deficiency_v1.yaml` (manual translation) |

### Rationale

- Single-frame (no STOP #7 multi-frame ambiguity).
- Registered in `ROOT_CAUSE_TARGET_SPECS` today.
- Existing legacy YAML for divergence comparison.
- Empty confirmatory tests (STOP #5 N/A).
- Lowest blast radius vs hba1c/lipid families.

### Alternatives rejected

| Candidate | Reason |
|-----------|--------|
| `signal_hba1c_high` | Broader metabolic coupling; more marker interactions. |
| Multi-frame signals | Would require frame-selection policy not yet in root-cause compiler. |

## Deliverables

| Item | Path |
|------|------|
| Schema | `knowledge_bus/schema/compiled_hypothesis_schema_v1.yaml` |
| Contract | `docs/architecture/compiled_hypothesis_contract.md` |
| Pilot artefact | `knowledge_bus/compiled/hypotheses/signal_vitamin_d_low.yaml` |
| Divergence report | `docs/architecture/ARCH-RT-4_root_cause_divergence_report.md` |

## Internal checkpoint

1. **Schema + artefact validation:** PASS (`validate_compiled_hypothesis_payload`, unit tests) — completed before shadow registry wiring.
2. **Divergence review:** PASS — recommendation `acceptable_with_carry_forward`; does **not** block shadow pilot.

## Implementation

| Component | Path |
|-----------|------|
| Validator + loader | `backend/core/knowledge/compiled_hypothesis.py` |
| Shadow registry (separate) | `backend/core/knowledge/compiled_hypothesis_registry_v1.py` |
| Divergence compare | `backend/core/knowledge/root_cause_divergence_v1.py` |

**Not modified:** `root_cause_registry_v1.py`, `root_cause_compiler_v1.py`, `load_root_cause_hypotheses.py` (legacy loaders), SignalRegistry, SignalEvaluator, PSI, card evidence, frontend, packages, investigation specs.

## Confirmatory test mapping

Pilot uses empty `confirmatory_tests` in both legacy and compiled artefact — mapping N/A. Contract documents registry validation when non-empty.

## Tests

```powershell
cd backend
python -m pytest tests/unit/test_compiled_hypothesis_arch_rt4.py -q
```

**Result:** 9 passed (2026-05-30).

## Confirmations

- Legacy YAML path remains available (`load_vitamin_d_low_hypotheses_v1`, 41 registry entries unchanged).
- No full root-cause estate migration.
- Shadow registry is pilot-only; production `get_root_cause_targets()` unchanged.
- Root-cause compiler multi-frame limitation documented in contract + divergence notes.
- No SignalRegistry / SignalEvaluator / PSI / card / frontend changes.
- No helper scripts committed.

## Remaining risks / carry-forwards

- Compiled artefact is not yet wired into `compile_root_cause_v1` output (shadow only).
- `compile_manifest_ref` is pilot manual string.
- `source_spec_provenance: source_document_derived` — not canonical explicit provenance.
- Multi-frame root-cause compiler policy still required before estate migration.
