# ADR-009 — KB-S46 Root-cause WHY: insulin resistance + systemic inflammation

## Status

Accepted.

## Decision

- Governed hypothesis assets: `knowledge_bus/root_cause/hypotheses/insulin_resistance_hypotheses_v1.yaml` and `systemic_inflammation_hypotheses_v1.yaml` (schema_version `v1`, same structural pattern as existing KB-S33b assets).
- Registry: `test_fasting_glucose_insulin_context_v1` and `test_ty_g_component_markers_panel_v1` added to `knowledge_bus/registries/confirmatory_tests_v1.yaml`; `test_liver_ggt_alt_ast_v1` also lists `signal_insulin_resistance` for related-signal traceability.
- Runtime: `compile_root_cause_v1` registers `signal_insulin_resistance` and `signal_systemic_inflammation` via `load_insulin_resistance_hypotheses_v1` / `load_systemic_inflammation_hypotheses_v1` in `root_cause_compiler_v1.py`.

## Backward compatibility

- Signals without a matching entry in `_ROOT_CAUSE_TARGETS` are unchanged (no finding emitted).
- Existing targets (homocysteine, HbA1c, ALT, TSH) behave as before; panels may now include **additional** findings when `signal_insulin_resistance` or `signal_systemic_inflammation` fire with suboptimal/at_risk state.
- No signal thresholds, activation evaluator, intervention registry, or promoted signal-intelligence schema changes.

## Related

- `backend/core/knowledge/load_root_cause_hypotheses.py`
- KB-S47d promoted signal intelligence (not consumed in this sprint beyond architectural coexistence).
