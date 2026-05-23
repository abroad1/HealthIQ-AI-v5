# LC-S14 — Direction-Aware Scoring Framework

**Work package:** LC-S14  
**Branch:** `scaffold/lc-s14-direction-aware-scoring`  
**Status:** Implementation complete (awaiting human review; not merged)

---

## 1. Preflight results

| Check | Result |
|-------|--------|
| Branch | `scaffold/lc-s14-direction-aware-scoring` (from `main` @ `29d78f5`) |
| Stash | Empty |
| Work package token | `LC-S14` — kernel STARTED |
| Controlling docs | Present |
| Cross-sprint guards | LC-S8F/G/D, LC-S10B, LC-S11A, LC-S13 — pass |

---

## 2. Current scoring architecture summary

- **Lab biomarkers:** `ScoringRules.calculate_biomarker_score()` uses **only** `input_reference_range` (lab); no SSOT/global range substitution.
- **Position:** `position_in_range` → `map_position_to_status` → `score_curve` mapping (`_calculate_score_from_has_position`).
- **Derived ratios:** `derived_ratio_policy_bounds` in `scoring_policy.yaml` when lab did not supply a range.
- **Systems:** `ScoringEngine` aggregates biomarker scores into health-system scores; domain assembly is downstream.

---

## 3. ALT bypass (pre-LC-S14)

Hardcoded in `rules.py`:

```python
if biomarker_name == "alt" and value < float(min_val):
    score, score_range = self._calculate_score_from_has_position(0.05)
```

Mapped low ALT to informational HAS position `0.05` (~borderline 70), avoiding critical false alarm (LC-S11A).

---

## 4. Directionality policy design

New SSOT block `biomarker_directionality` in `backend/ssot/scoring_policy.yaml` (policy `1.2.0`):

| Class | Meaning |
|-------|---------|
| `bidirectional_concern` | Default — symmetric high/low scoring |
| `high_only_concern` | Below range informational; above range concerning |
| `low_only_concern` | Above range informational; below concerning |
| `protective_high` | Above range not penalised; below range symmetric |
| `protective_low` | Below range not penalised |
| `informational_low` / `informational_high` | Explicit informational deviation |

Runtime: `ScoringRules._directionality_position_override()` applies governed positions before symmetric range scoring.

---

## 5. Biomarkers covered

| Marker | Class |
|--------|--------|
| ALT, AST, GGT, ALP | `high_only_concern` |
| HDL cholesterol, ApoA1 | `protective_high` |
| All others | `bidirectional_concern` (default) |

**Deferred (documented):** ferritin, transferrin, CRP, TSH, Free T4 — context-dependent; no invented policy.

---

## 6. Files changed

| File | Change |
|------|--------|
| `backend/ssot/scoring_policy.yaml` | `biomarker_directionality` + version `1.2.0` |
| `backend/core/analytics/scoring_policy_registry.py` | Validator for directionality block |
| `backend/core/scoring/rules.py` | Policy-driven overrides; removed ALT hardcode |
| `backend/tests/regression/test_lc_s14_direction_aware_scoring.py` | New regression pack |
| `backend/tests/unit/test_scoring_rules.py` | Direction class unit test |
| `sentinel/packs/lc_s10b_launch_core_protection_v1.json` | LC-S14 defect classes |
| `docs/audit-papers/LC-S14_direction_aware_scoring_notes.md` | This note |

**Not touched:** `knowledge_bus/**`, units, narrative, frontend, signal libraries.

---

## 7. Tests

- `backend/tests/unit/test_scoring_rules.py` — direction class load
- `backend/tests/regression/test_lc_s14_direction_aware_scoring.py` — enzymes, protective-high, policy validation, no hardcoded ALT

---

## 8. Sentinel updates

Added to `lc_s10b_launch_core_protection_v1.json`: `direction_sensitive_marker_false_alarm`, `low_enzyme_false_alarm`, `protective_high_marker_penalised`, `hardcoded_biomarker_scoring_exception`, `scoring_signal_directionality_conflation`.

---

## 9. Lab-derived ranges authoritative

- Missing lab range → `missing_lab_reference_range` unscored (unchanged).
- Directionality only adjusts HAS **position** interpretation; min/max lab bounds unchanged.

---

## 10. Units / display fidelity

No changes to `units.yaml`, registry, or frontend. LC-S8F/G regressions pass.

---

## 11. Residual risks

- `bio_stats_engine` / burden vectors may still treat low enzymes symmetrically — out of LC-S14 scoring scope.
- Policy cache is process-global (`load_scoring_policy`); tests that mutate policy must clear `scoring_policy_registry._policy_cache`.
- Broader marker directionality (ferritin, TSH, etc.) deferred to LC-S15/Sprint 4.

---

## 12. Recommendation for LC-S15 / Sprint 4

1. Extend directionality to deferred markers after clinical sign-off.  
2. Align burden/bio-stats asymmetry with scoring policy if audits show drift.  
3. Re-run proving harness if domain score bands shift materially.
