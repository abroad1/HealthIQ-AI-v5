# P1-22 — Thyroid Activation Pack

**Work ID:** P1-22  
**Branch:** `sprint/P1-22-thyroid-activation-pack`  
**Date:** 2026-06-22  
**Status:** IMPLEMENTATION_COMPLETE  
**Change type:** BEHAVIOUR

## 1. Start state

- Hormonal scoring rail inert (`system_weight: 0.0`, empty biomarkers).
- P1-4 stopped at authority gate; no `wave1_thyroid` domain.
- P1-8 `lab_range_only` engine ready; first production use in this sprint.
- ADR-THYROID-FT3-AUTHORITY-RECONCILIATION-1 governs FT3/FT4/TSH boundaries.

**pipeline_advisory_trigger:** true  
**pipeline_advisory_reason:** P1-21 audit close identified thyroid domain as the last missing launch-core domain; Stage B scope advisory (2026-06-22) confirmed single outcome-based P1-22 pack.

## 2. Phase 1 — Scoring and authority

- Verified `lab_range_only` schema from `scoring_policy_registry.py` and `rules.py` before edits.
- Populated hormonal rail: `tsh`, `free_t4`, `free_t3` with `lab_range_only` (no hardcoded bands).
- Decisions: `system_weight: 0.1`, `min_biomarkers_required: 1` (recorded in activation manifest).
- ADR: `ADR-THYROID-TSH-LAUNCH-SCORING-ONLY-1` — TSH scoring only; signal intelligence deferred.

## 3. Phase 2 — Runtime activation

- `wave1_thyroid` sixth launch-core domain in `domain_score_assembler.py`.
- Launch allowlist: `signal_free_t3_high`, `signal_free_t4_high`, `signal_free_t4_low`.
- Excluded: TSH signal IDs, `signal_free_t3_low`, `signal_thyroid_tsh_context`.
- Subsystem routing registered with empty tuple pending compiled card evidence.
- Non-diagnostic narrative helpers in `domain_narrative_wave1.py`.
- Replay contract updated.

## 4. Marker boundaries

| Marker | Scoring | Domain signals |
|--------|---------|----------------|
| TSH | lab_range_only | Not in allowlist (scoring only) |
| FT4 | lab_range_only | high/low when active |
| FT3 high | lab_range_only | high only; TSH-suppressed gate enforced by SignalEvaluator |
| FT3 low | — | Excluded |

## 5. Validation

```powershell
python -m pytest backend/tests/unit/test_p1_22_thyroid_activation_pack.py backend/tests/unit/test_scoring_lab_range_only_rules.py backend/tests/unit/test_scoring_policy_registry.py backend/tests/unit/test_domain_score_assembler_v1.py backend/tests/regression/test_batch2_thyroid_tsh_gating.py backend/tests/unit/test_p1_2_kidney_domain_card.py backend/tests/unit/test_p1_3_blood_iron_oxygen_domain_card.py -q
```

## 6. Carry-forwards

See `P1-22_pass3_carry_forward.yaml` — TSH kb52c promotion, FT3 low activation control, antibody packages, compiled subsystem card.

## 7. Recommended next sprint

**P1-TSH-KB52C-PROMOTION-1** (Knowledge Bus) after medical review, plus **P1-22B-THYROID-SUBSYSTEM-CARD-1** for compiled subsystem evidence.
