# LAUNCH-CORE-5 — Results Page Narrative Hierarchy and Score Rationalisation Report

**Work package:** `LAUNCH-CORE-5_results_page_narrative_hierarchy_and_score_rationalisation`  
**Generated:** 2026-05-30  
**Reference audit:** `docs/audit-papers/LAUNCH-CORE-4_results_page_narrative_hierarchy_and_score_rationalisation_audit.md`

## Issues addressed

| LC-4 finding | LC-5 change |
|--------------|-------------|
| Primary finding after Health Systems Cards | Reordered journey: primary finding → working well → health systems |
| Stale/incompatible banner missing for incompatible | `StaleResultBanner` renders for `stale` and `incompatible` |
| Marker `Scored X/100` noise | Hidden from default card via `feR6aRetailCopy`; shown in expanded detail |
| Mechanical labels | Consumer copy: Data quality, How confident is this read?, Needs attention, Most relevant area |
| Weak narrative bridge text | Updated journey preamble to match new order |

## Before / after section order

| # | Before | After |
|---|--------|-------|
| 1 | Hero + body overview | Hero + body overview |
| 2 | What's working well | **Primary finding and why** |
| 3 | Health Systems Cards | What's working well |
| 4 | Primary finding and why | Health Systems Cards |
| 5+ | Uncertainty → patterns → markers → next steps → collapsed | Same relative order (indices shifted) |

## Layer B vs Layer C

| Layer | Changes |
|-------|---------|
| **Layer B** | **None** — no clinical scoring, narrative compiler, or DTO assembly changes |
| **Layer C** | Section reorder, label renames, banner behaviour, marker score display policy, journey test IDs |

Frontend did **not** infer clinical priority from raw markers or scores.

## Files changed

| Path | Change |
|------|--------|
| `frontend/app/(app)/results/page.tsx` | Section reorder; journey test id indices |
| `frontend/app/lib/feR2ResultsJourneyOrder.ts` | LC-5 canonical order (+ health-systems anchor) |
| `frontend/app/components/results/StaleResultBanner.tsx` | Stale + incompatible banner |
| `frontend/app/lib/feR6aRetailCopy.ts` | Hide `Scored X/100` on default card |
| `frontend/app/lib/resultsPageLayout.ts` | Consumer severity + system context label |
| `frontend/app/components/biomarkers/BiomarkerDials.tsx` | Expand when numeric score in detail only |
| `frontend/app/components/pipeline/PipelineStatus.tsx` | Trust strip → Data quality |
| `frontend/app/components/results/WhyThisLeadWonSection.tsx` | Section title relabel |
| `frontend/app/components/results/InterpretationPatternsSection.tsx` | Shared severity label |
| `backend/tests/regression/test_fe_r2_results_journey_restructure.py` | Updated journey guards |
| `backend/tests/regression/test_launch_core5_results_page_hierarchy.py` | LC-5 regression |
| `frontend/tests/components/StaleResultBanner.test.tsx` | Stale + incompatible |
| `frontend/tests/lib/feR6aRetailCopy.lc5.test.ts` | Score hide/detail |
| `frontend/tests/lib/resultsHeroAlignment.test.ts` | System context label |

## Content preservation

No clinically meaningful analysis removed from DTOs or collapsed sections. Changes are **reorder**, **rename**, **suppress default view**, and **expand** only.

## Stale / incompatible banner

- Renders for `result_status === 'stale'` or `'incompatible'`
- Uses backend `user_message` when present
- **No** regenerate button (`regeneration_available` copy only when true)

## Score display

- Marker interpretation lines matching `Scored N/100` hidden on default card
- Visible in expanded marker detail via `biomarkerInterpretationForDetail`
- Wave1 card scores, completeness, reliability unchanged

## Tests run

```text
python backend/scripts/validate_day_one_architecture.py
python -m pytest backend/tests/architecture/test_day_one_architecture_guardrails.py -q
python -m pytest backend/tests/regression/test_fe_r2_results_journey_restructure.py -q
python -m pytest backend/tests/regression/test_launch_core5_results_page_hierarchy.py -q
cd frontend && npm test -- tests/components/StaleResultBanner.test.tsx tests/lib/feR6aRetailCopy.lc5.test.ts tests/lib/resultsHeroAlignment.test.ts
```

## Manual validation

Target: `http://localhost:3000/results?analysis_id=746f2b0a-b470-4d87-8ed8-e2c3d1e68c02` — **deferred to post-merge UAT** (requires running stack + test-user3 credentials).

## Remaining risks / carry-forwards

| Risk | Mitigation |
|------|------------|
| Hero/body overview still duplicate lead framing | Future sprint: collapse body overview or merge with hero |
| Regeneration UX | LC-3 follow-on when lineage schema exists |
| FE-R2 sentinel name `working_well_before_primary` | Test updated; name retained for history |

## ARCH-RT-6

Validator expected **PASS** — no core clinical logic touched.
