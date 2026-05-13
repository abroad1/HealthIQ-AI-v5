# LC-S6 — Results retail hardening (completion)

**Work ID:** `LC-S6-RESULTS-RETAIL-HARDENING`  
**Branch:** `sprint6/results-retail-hardening`  
**Date:** 2026-05-13  
**Evidence:** `docs/testing/UAT_results_page_analysis_b2dfa0c4_2026-05-12.md`

## UAT blockers addressed

- Internal architecture vocabulary (Layer B/C, deterministic compiler/arbitration, slugs, chain IDs) removed or gated from default retail paths; retail narrative blocks run through a presentation-only sanitiser.
- Raw markdown (`**…**`) stripped for Summary, lead stack, direction/next steps, body overview primary line, and clinician synthesis (advanced).
- Hero vs ranked-lead mismatch: when IDL retail label and page-1 primary concern disagree, the hero title uses the primary-concern lead sentence and a `Main system context:` line carries the IDL label; otherwise a softer bridge line is shown.
- Summary and “What this means” card subtitles rewritten to consumer-safe copy (no compiler / deterministic wording).
- Domain section heading no longer shows “Wave 1”.
- Advanced teaser no longer references “Layer C” in the default disclosure description.
- Actions hub: when cluster/panel recommendation lines are empty, cards are derived from governed `narrative_report_v1.next_steps_narrative` (frontend-only wiring); Actions page uses the same fallback; empty-state copy de-emphasised engineering language.
- Mock-mode honesty banner uses approved verbatim copy with “structured clinical rules”.
- “What’s driving this” uses humanised marker names instead of raw snake_case keys.

## Markdown rendering

- Implemented `stripSimpleMarkdownDecorators` + `scrubConsumerRetailNarrative` in `frontend/app/lib/retailNarrativeSanitize.ts` and applied via `DeterministicNarrativeSurface` narrative prose, `ResultsBodyOverview`, `PrimaryFindingAndWhy`, hero summary lines, and narrative-derived action paragraphs.

## Hero / summary alignment decision

- **Decision:** Prefer the page-1 primary concern first sentence as the hero title when it materially differs from the IDL retail display label, and show `Main system context: <IDL label>` beneath the title. Ranking logic and backend fields are unchanged.

## Actions hub decision

- **Decision:** Extend `buildActionCardModels` with optional `narrativeNextStepsNarrative`, used only when no cards were produced from clusters, panel recommendations, or filtered insights — avoids replacing structured recs and does not reintroduce `legacy_v1` `insights[]`.

## Tests run

```text
npx jest tests/lib/resultsHeroAlignment.test.ts tests/lib/retailNarrativeSanitize.test.ts tests/lib/resultsPageLayout.lc-s6.test.ts tests/lib/lcS4ResultsCopy.test.ts tests/components/DeterministicNarrativeSurface.lc-s4.test.tsx tests/components/ResultsBodyOverview.lc-s4.test.tsx
```

Result: **6 suites, 18 tests passed.**

```text
npm run type-check
```

Result: **passed.**

Full `npm test` was not used as the suite includes unrelated failing store/persistence tests in this workspace; LC-S6 scoped tests and `tsc` were used as the sprint validation minimum.

## Known limitations

- Long internal slugs use a heuristic (length + underscore segments) plus explicit token map; novel internal codes could still surface until mapped.
- `scrubInternalArchitecturePhrases` replaces some generic words (e.g. “runtime”) wherever they appear as whole words in narrative text — trade-off for blocking pipeline jargon.
- Evidence ranking blocks and chains remain available only inside a collapsed `<details>` in “Primary finding and why”; advanced clinician report still shows technical tables for power users.

## Files changed (implementation)

- `frontend/app/lib/retailNarrativeSanitize.ts` (new)
- `frontend/app/lib/resultsPageLayout.ts`
- `frontend/app/lib/lcS4ResultsCopy.ts`
- `frontend/app/components/results/DeterministicNarrativeSurface.tsx`
- `frontend/app/components/results/ResultsHeroBlocks.tsx`
- `frontend/app/components/results/ResultsBodyOverview.tsx`
- `frontend/app/components/results/PrimaryFindingAndWhy.tsx`
- `frontend/app/components/results/ClinicianReportRenderer.tsx`
- `frontend/app/components/results/Wave1DomainCards.tsx`
- `frontend/app/(app)/results/page.tsx`
- `frontend/app/(app)/actions/page.tsx`
- `frontend/tests/lib/resultsHeroAlignment.test.ts`
- `frontend/tests/lib/lcS4ResultsCopy.test.ts`
- `frontend/tests/lib/retailNarrativeSanitize.test.ts` (new)
- `frontend/tests/lib/resultsPageLayout.lc-s6.test.ts` (new)
- `frontend/tests/components/DeterministicNarrativeSurface.lc-s4.test.tsx`
- `frontend/tests/components/ResultsBodyOverview.lc-s4.test.tsx`
- `docs/sprints/LC-S6_results_retail_hardening_completion_2026-05.md` (this file)

## Confirmation — out-of-scope paths not modified

No changes to: `backend/ssot/`, `knowledge_bus/`, `backend/core/analytics/`, `backend/core/pipeline/`, `backend/core/contracts/`, questionnaire assets, narrative compiler (LC-S3) Python, Automation Bus control-plane scripts (`run_work_package.py`, etc.), or Sentinel files.
