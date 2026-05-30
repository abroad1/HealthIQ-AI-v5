# LAUNCH-CORE-5 — Results Page Narrative Hierarchy and Score Rationalisation Report

**Work package:** `LAUNCH-CORE-5_results_page_narrative_hierarchy_and_score_rationalisation`  
**Generated:** 2026-05-30  
**Updated:** 2026-05-30 (closure evidence — validator output + manual UAT)  
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

### ARCH-RT-6 validator (closure re-run — 2026-05-30)

```text
> python backend/scripts/validate_day_one_architecture.py
day_one_architecture_validation: PASS

> python -m pytest backend/tests/architecture/test_day_one_architecture_guardrails.py -q
....                                                                     [100%]
4 passed in 7.40s
```

### Sprint regression (implementation commit)

```text
python -m pytest backend/tests/regression/test_fe_r2_results_journey_restructure.py -q
python -m pytest backend/tests/regression/test_launch_core5_results_page_hierarchy.py -q
cd frontend && npm test -- tests/components/StaleResultBanner.test.tsx tests/lib/feR6aRetailCopy.lc5.test.ts tests/lib/resultsHeroAlignment.test.ts
```

(All passed at implementation time; not re-run for this doc-only closure patch.)

## Manual validation

**Target:** `http://localhost:3000/results?analysis_id=746f2b0a-b470-4d87-8ed8-e2c3d1e68c02`  
**Account:** `test-user3@example.com`  
**Date:** 2026-05-30  
**Stack:** backend `uvicorn` @ `:8000`, frontend `next dev` @ `:3000`, sprint branch `work/LAUNCH-CORE-5-results-page-narrative-hierarchy-and-score-rationalisation`

### API pre-check (authenticated)

```text
POST /api/auth/login → 200
GET /api/analysis/result?analysis_id=746f2b0a-b470-4d87-8ed8-e2c3d1e68c02 → 200
result_versioning.result_status: incompatible
result_versioning.regeneration_available: false
result_versioning.user_message: "This saved result cannot be displayed with the current results page contract."
```

### Browser inspection checklist

| Criterion | Result | Evidence |
|-----------|--------|----------|
| Main story clearer within first 30s | **Pass (improved)** | Hero shows “Raised homocysteine pattern…” + “Needs attention” + “Most relevant area: …” above fold; primary finding section follows hero before system cards |
| Primary finding before Health Systems Cards | **Pass** | DOM `data-testid` order: `fe-r2-journey-primary-finding` (top ≈1817px) before `fe-r2-journey-health-systems` (top ≈2837px) |
| Repeated lead-pattern copy reduced | **Partial** | Reorder + relabels reduce competing urgency signals; hero + body overview still share homocysteine framing (known carry-forward — see risks) |
| Stale/incompatible banner correct | **Pass** | `stale-result-banner` visible; title “This saved result uses an older format”; body shows API `user_message`; matches `result_status: incompatible` |
| No regenerate button | **Pass** | No button/link matching `/regenerat/i` in page controls |
| Marker numeric scores not noisy by default | **Pass** | Zero `Scored N/100` matches in default page text / marker section; after Expand on a marker card, detail shows `Scored 100.0/100` in `biomarker-detail-interpretation` |
| Technical detail remains available | **Pass** | “Show technical detail” control present; `section-advanced` disclosure present (collapsed) |
| No internal IDs/traces visible | **Pass** | Page text scan: no `wave1_subsystem`, `source_trace`, `health_system_card_evidence`, `pkg_`, or `signal_` substrings |
| Consumer label renames | **Pass** | “Data quality” present; “How confident is this read?” present; “Needs attention” present; “Strong Signal” / “Trust strip” / “Why this lead won” absent from retail surface |

### Representative retail copy observed

```text
This saved result uses an older format
… PRIMARY FINDING … Raised homocysteine pattern …
Most relevant area: Vascular Inflammation Risk
Needs attention
… Primary finding and why … (before Health Systems Cards)
… Data quality … How confident is this read? …
```

## Remaining risks / carry-forwards

| Risk | Mitigation |
|------|------------|
| Hero/body overview still duplicate lead framing | Future sprint: collapse body overview or merge with hero |
| Regeneration UX | LC-3 follow-on when lineage schema exists |
| FE-R2 sentinel name `working_well_before_primary` | Test updated; name retained for history |

## ARCH-RT-6

Validator **PASS** (see closure re-run output above) — no core clinical logic touched.
