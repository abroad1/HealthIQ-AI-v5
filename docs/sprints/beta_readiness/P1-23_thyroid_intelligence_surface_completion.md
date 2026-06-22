# P1-23 — Thyroid Intelligence Surface Completion

**Work ID:** P1-23  
**Date closed:** 2026-06-22

## 1. Start state

P1-22 activated `wave1_thyroid` with TSH lab-range-only scoring. TSH signal intelligence deferred; `wave1_thyroid` routed with empty subsystem tuple; no compiled thyroid card.

## 2. Phase 1 Knowledge Bus outcome

- Medical Review gate PASS (Pass 3 v3.0.0 supplemental authority).
- `pkg_kb52c_tsh_high_primary_hypothyroid_pattern` and `pkg_kb52c_tsh_low_thyrotoxic_pattern` authored from Batch_4 Pass 3.
- Legacy s24 TSH packages deprecated in-place.
- Package and PSI validation PASS for both candidates.
- Production PSI opt-in count increased by 2.

## 3. Phase 2 Core Engine outcome

- `signal_tsh_high` and `signal_tsh_low` added to thyroid launch allowlist.
- `wave1_thy_hormonal_axis` compiled card created and registered.
- `wave1_thyroid` subsystem order updated to `("wave1_thy_hormonal_axis",)`.
- Card uses `scored_subsystem` visibility; registered in MED-REV-1 scored-visible set for runtime emission.

## 4. Authority decisions

- ADR-THYROID-TSH-SIGNAL-INTELLIGENCE-ACTIVATION-1 records kb52c replacement and allowlist extension.
- `signal_free_t3_low` and `signal_thyroid_tsh_context` remain excluded.
- No changes to `signal_evaluator.py`, `domain_narrative_wave1.py`, or `scoring_policy.yaml`.

## 5. Validation results

- Package validation: PASS (both kb52c TSH packages).
- PSI validation: PASS (both).
- `validate_day_one_architecture.py`: PASS.
- Unit tests: PASS (`test_p1_22_thyroid_activation_pack.py`).

## 6. Carry-forwards

- FT3 low activation control (p1_22_cf_002).
- Thyroid antibody packages (p1_22_cf_003).

## 7. Recommended next sprint

- P1-24 bio-oxygen card depth or thyroid narrative enrichment sprint (deferred narrative work).
