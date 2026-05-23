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

| Marker | Direction class | In `biomarker_directionality.markers` | In `scoring_policy.yaml` `biomarkers` + system lists |
|--------|-----------------|--------------------------------------|------------------------------------------------------|
| ALT | `high_only_concern` | Yes | Yes (`liver` system) |
| AST | `high_only_concern` | Yes | Yes (`liver` system) |
| GGT | `high_only_concern` | **Yes** | **No** — directionality only |
| ALP | `high_only_concern` | **Yes** | **No** — directionality only |
| HDL cholesterol | `protective_high` | Yes | Yes (`cardiovascular` system) |
| ApoA1 | `protective_high` | **Yes** | **No** — directionality only |
| All others | `bidirectional_concern` (default) | — | Per existing enrolment |

### GGT, ALP, and ApoA1 — policy coverage vs system enrolment

LC-S14 **does** assign governed direction classes to **GGT**, **ALP**, and **ApoA1** in
`biomarker_directionality.markers`. `ScoringRules.calculate_biomarker_score()` honours those
classes whenever a lab reference range is supplied (covered by unit/regression tests).

They are **not** fully enrolled in system/domain aggregation via `scoring_policy.yaml`:

- **GGT** and **ALP** are absent from the top-level `biomarkers:` block and from
  `systems.*.biomarkers` lists (unlike ALT/AST under `liver`).
- **ApoA1** is absent from `biomarkers:` and system lists (unlike `hdl_cholesterol` under
  `cardiovascular`). The derived `apob_apoa1_ratio` remains enrolled separately.

**Accepted disposition (not an LC-S14 blocker):** this is a **deferred SSOT metadata / system
coverage enrolment** issue. LC-S14 scope was direction-aware **lab-range scoring behaviour**,
not expanding which markers participate in weighted health-system rollups. Track for a later
scaffold sprint (SSOT metadata + `systems`/`biomarkers` alignment), alongside clinical review
of ferritin, transferrin, CRP, TSH, and Free T4 directionality.

**Deferred (clinical directionality, not enrolment):** ferritin, transferrin, CRP, TSH,
Free T4 — context-dependent; no invented policy.

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
- **GGT / ALP / ApoA1 system enrolment** — directionality active at score time; rollup/domain weighting unchanged until SSOT lists are extended (see §5).
- Broader marker directionality (ferritin, TSH, etc.) deferred to LC-S15/Sprint 4.

---

## 13. Pre-merge proving harness (2026-05-23)

Re-ran `python backend/tools/launch_core_proving_harness.py` after LC-S14.

**Result:** No **material** fingerprint refresh required. All `runs.*` narrative, domain-row,
and intervention payloads are **byte-identical** to the prior commit; only harness metadata
(`git_short_sha`, `stamp`) advanced to the current branch HEAD. No proving-artefact commit
needed for LC-S14 pre-merge closure.

---

## 12. Recommendation for LC-S15 / Sprint 4

1. Extend directionality to deferred markers after clinical sign-off.  
2. Align burden/bio-stats asymmetry with scoring policy if audits show drift.  
3. Re-run proving harness if domain score bands shift materially.
