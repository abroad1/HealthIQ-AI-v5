# ADR-THYROID-TSH-SIGNAL-INTELLIGENCE-ACTIVATION-1 — TSH Signal Intelligence Activation

## Status

Accepted — P1-23 Phase 1 authority decision.

## Date

2026-06-22

## Context

P1-22 activated `wave1_thyroid` with TSH in `lab_range_only` scoring only. TSH directional signal intelligence (`signal_tsh_high`, `signal_tsh_low`) remained excluded from the domain allowlist. Legacy s24 TSH packages held stale signal authority. Governed Pass 3 v3.0.0 specs exist in Batch_4 for kb52c replacement.

## Medical Review authority

Existing FT3/FT4 clinical signoff (`thyroid_blood_marker_interpretation_clinical_signoff.md`) establishes TSH as mandatory first-line discriminator for FT3/FT4 patterns but does not explicitly sign off standalone TSH high/low narrative patterns.

**Decision:** PASS — TSH directional activation authorised via governed Pass 3 v3.0.0 specs (`inv_tsh_high_primary_hypothyroid_pattern`, `inv_tsh_low_thyrotoxic_pattern`) with consensus evidence. Activation class is `lab_range_exceeded` on the primary TSH marker — distinct from FT3/FT4 narrative patterns requiring mandatory pre-emission gates. FT4/FT3 context is captured in PSI supporting_markers and override_rules.

## Decision

1. Author kb52c replacement packages from Pass 3 Batch_4 specs; deprecate legacy s24 TSH packages in-place (not revalidated).
2. Move exactly `signal_tsh_high` and `signal_tsh_low` into `_THYROID_LAUNCH_SIGNAL_IDS`.
3. Keep excluded: `signal_free_t3_low`, `signal_thyroid_tsh_context`.
4. No changes to `signal_evaluator.py`, `domain_narrative_wave1.py`, or `scoring_policy.yaml`.
5. Phase 2 Core Engine allowlist and compiled card work proceeds because Phase 1 gates passed.

## Consequences

- cf_001 (TSH signal intelligence deferred) and cf_005 (legacy s24 revalidation) closed by kb52c replacement path.
- cf_004 (compiled subsystem card missing) closed by `wave1_thy_hormonal_axis` registration.

## References

- `docs/architecture/ADR-THYROID-TSH-LAUNCH-SCORING-ONLY-1.md`
- `docs/architecture/ADR-THYROID-FT3-AUTHORITY-RECONCILIATION-1.md`
- `knowledge_bus/research/investigation_specs/multi_llm_research/Batch_4_Pass_3.json`
