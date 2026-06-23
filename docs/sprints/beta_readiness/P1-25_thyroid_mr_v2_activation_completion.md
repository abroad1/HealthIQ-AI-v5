# P1-25 — Thyroid MR-v2 Activation Completion

**Work ID:** P1-25  
**Date closed:** 2026-06-23

## 1. Start state

P1-23 activated TSH directional signals and the thyroid compiled card. FT3-low remained excluded; kb59 thyroid antibody packages inactive.

## 2. MR-v2 authority outcome

MR-v2 (2026-06-23) cleared FT3-low and TPOAb hypothyroid-context activation with strict deterministic gates. TPOAb euthyroid and TgAb remain deferred.

## 3. Knowledge Bus outcome

- FT3-low signal library hardened with `mandatory_pre_emission_gates` (TSH not below min).
- TPOAb hypothyroid package hardened with runtime context requirements and TSH above-max gate.
- TPOAb PSI authored (`promoted_signal_intelligence.yaml`).
- kb59 manifest updated (`SIGNAL_RUNTIME_ACTIVATION`, PSI ref).
- Medical frame index updated for FT3-low and TPOAb hypothyroid frames.

## 4. Core Engine outcome

- `signal_free_t3_low` and `signal_tpo_ab_high` added to thyroid launch allowlist.
- `signal_thyroid_tsh_context` remains excluded.
- ADR-THYROID-MR-V2-ACTIVATION-1 created.

## 5. Compiled card outcome

- `wave1_thy_hormonal_axis` enriched with FT3-low and TPOAb source specs and TPOAb contextual marker.
- P1-25 compile manifest created; estate index updated.

## 6. Validation results

- Package and PSI validation: PASS (both candidates).
- Thyroid unit and regression tests: PASS.
- `validate_day_one_architecture.py`: PASS (closure).

## 7. Carry-forwards

- Questionnaire alignment for FT3-low context fields (fail-closed preserved).
- Biotin/assay-interference disclosure schema follow-on (optional).
- TPOAb euthyroid and TgAb deferred.

## 8. Recommended next sprint

- Questionnaire thyroid context alignment or deferred antibody tranche per programme priority.
