# INTERNAL-UAT-RESULTS-TRUST-HARDENING-1 — High-Trust Results Page Coherence

---
work_id: INTERNAL-UAT-RESULTS-TRUST-HARDENING-1_high_trust_results_page_coherence
branch: work/INTERNAL-UAT-RESULTS-TRUST-HARDENING-1-high-trust-results-page-coherence
status: GPT_CORRECTION_COMPLETE_PENDING_REVIEW
head_sha: (see latest commit on branch)
---

## Executive verdict

Resolved all six **HIGH** internal UAT trust/coherence defects on the working results page (`analysis_id: 6bcbf1de-d97f-4a1c-9556-e3a6e0625fd1`) without changing parser, intelligence, signal activation, scoring, lab ranges, or result-versioning logic.

**GPT architectural review (initial): FAIL** — duplicate frontend B12 title rewrite removed; TypeScript build fixed.

**Do not merge** until re-review passes and human approval.

---

## GPT correction (post-review)

| Ruling | Action |
|--------|--------|
| Backend IUAT-001 / IUAT-004 producer fixes | **Kept** — `report_compiler_v1.py`, `lifestyle_consumer_surface_v1.py` |
| Duplicate frontend B12 neutralisation | **Removed** — deleted `hypothesisDisplayCopy.ts`; `PrimaryFindingAndWhy.tsx` renders backend title with generic retail scrub only |
| TypeScript build | **Fixed** — `result_versioning` added to store `AnalysisResult`; normalised in `analysis.ts` service |
| IUAT-002–006 | **Preserved** |
| IUAT-006 critical fallback | **Confirmed** — below-range interpretation → "Below range"; no interpretation → "Needs review" |

---

## Baseline UAT summary

| Check | Baseline |
|-------|----------|
| `GET /api/analysis/result` | HTTP 200 |
| `result_versioning.compatible` | `true` |
| `result_status` | `current` |
| `render_blockers` | `[]` |
| `stale_reasons` | `[]` |
| `clinician_report_v1` | present |
| Stale/incompatible banner | absent |
| Clusters | 3 |
| Biomarkers | 79 |

Source: `docs/testing/INTERNAL_UAT_RESULTS_PAGE_FULL_AUDIT_6bcbf1de_2026-06-16.md`

---

## Issue-by-issue tracing and fixes

### IUAT-001 — B12-associated heading mismatch

| Layer | Detail |
|-------|--------|
| Visible text | "B12-associated pattern" |
| API field | `clinician_report_v1.sections.root_cause.hypotheses[0].title` |
| Producer | `report_compiler_v1._normalise_root_cause_finding` |
| Fix | `_neutralise_hypothesis_title_for_counter_evidence` when B12 counter-evidence present → "Homocysteine-related pattern" |
| Frontend | Render-only: `scrubConsumerRetailNarrative(hyp0.title)` — **no** counter-evidence rewrite |
| Counter-evidence | Unchanged and still visible |

### IUAT-002 — Pattern-groups placeholder

| Layer | Detail |
|-------|--------|
| Condition | `clusters.length > 0` && `showPatternGroupBuckets=false` |
| Component | `ResultsBodyOverview.tsx` |
| Fix | "Detailed pattern groups are hidden in this view…" |

### IUAT-003 — 79 markers vs 9/9 expected

| Layer | Detail |
|-------|--------|
| Toolbar | `page.tsx` → "79 uploaded markers" |
| Data quality | `PipelineStatus.tsx` → "9 of 9 key markers available for this headline interpretation" |

### IUAT-004 — Markdown / internal wording in body overview

| Layer | Detail |
|-------|--------|
| Producer | `lifestyle_consumer_surface_v1._metabolic_modifier_paragraph` |
| Scrubber | `retailNarrativeSanitize.ts` — `Cardiovascular N Biomarkers` mapping |

### IUAT-005 — Homocysteine vs vascular hierarchy

| Layer | Detail |
|-------|--------|
| Subline | "Broader system context:" (was "Most relevant area:") |

### IUAT-006 — Transferrin "Critical" in driver band

| Fix | `formatConsumerDriverBandStatusLabel` — driver band only |
| Below-range + interpretation | "Below range" |
| `critical` without directional interpretation | "Needs review" |
| Backend severity mapping | Unchanged |

---

## Files changed (including GPT correction)

| File | Change |
|------|--------|
| `backend/core/analytics/report_compiler_v1.py` | IUAT-001 hypothesis title neutralisation (producer) |
| `backend/core/analytics/lifestyle_consumer_surface_v1.py` | IUAT-004 consumer metabolic paragraph |
| `backend/tests/regression/test_internal_uat_results_trust_hardening.py` | 5 regression tests incl. `_normalise_root_cause_finding` |
| `frontend/app/lib/resultsPageLayout.ts` | IUAT-005 hero subline; IUAT-006 driver status |
| `frontend/app/lib/retailNarrativeSanitize.ts` | IUAT-004 Cardiovascular label scrub |
| `frontend/app/components/results/ResultsBodyOverview.tsx` | IUAT-002 |
| `frontend/app/components/results/ResultsHeroBlocks.tsx` | IUAT-006 |
| `frontend/app/components/results/PrimaryFindingAndWhy.tsx` | Render backend title only (GPT correction) |
| `frontend/app/components/pipeline/PipelineStatus.tsx` | IUAT-003 |
| `frontend/app/(app)/results/page.tsx` | IUAT-003 |
| `frontend/app/state/analysisStore.ts` | `result_versioning` on store type (build fix) |
| `frontend/app/services/analysis.ts` | Pass through `result_versioning` from API |
| `frontend/tests/lib/resultsTrustHardening.test.ts` | 7 tests |
| `frontend/tests/lib/resultsHeroAlignment.test.ts` | IUAT-005 expectation |
| `docs/sprints/launch_core_carry_forward_register.md` | Carry-forward updates |

**Removed (GPT correction):** `frontend/app/lib/hypothesisDisplayCopy.ts`

---

## Boundary confirmations

- Frontend remains **render-only** — hypothesis titles come from backend compiler; no duplicate clinical-title rewrite
- Parser, intelligence, signal activation, scoring, lab reference ranges, and result versioning **unchanged**
- No dummy/fallback `clinician_report_v1`
- Stale/incompatible warnings **not** hidden or bypassed

---

## Test output (post-correction)

### Backend trust-hardening

```
python -m pytest backend/tests/regression/test_internal_uat_results_trust_hardening.py -q
.....                                                                    [100%]
5 passed
```

### Frontend trust-hardening

```
npm test -- tests/lib/resultsTrustHardening.test.ts
7 passed
```

### Frontend build

```
npm run build
✓ Compiled successfully
✓ Generating static pages (20/20)
(exit 0)
```

TypeScript fix: `analysisStore.AnalysisResult.result_versioning` + service normalisation.

### Frontend lint

```
npm run lint
Failed to load config "next/core-web-vitals" to extend from.
Referenced from: C:\Users\abroa\HealthIQ-AI-v5\.eslintrc.json
```

Pre-existing monorepo ESLint config resolution issue (repo-root `.eslintrc.json` vs `frontend/` dependency tree). **Not introduced by this sprint.** `npm run build` type-check phase passes.

### Architecture gate

```
architecture_validation_gate: PASS
day_one_architecture_validation: PASS
day_one_launch_estate_gate: PASS
validation_status: PASS
medical_intelligence_architecture_validation: PASS
```

### Required regressions

```
test_internal_uat_result_versioning_dto_contract.py  → 7 passed
test_active_signal_context_gate_reachability.py      → 21 passed
test_dhea_s_high_activation.py                       → 37 passed
```

---

## Carry-forward register

- **Resolved:** CF-RESULTS-COPY-PATTERN-GROUPS-1 (IUAT-002)
- **Opened:** CF-IUAT-DEFER-001 through CF-IUAT-DEFER-006

---

## Review route

```
Cursor implementation + GPT correction
→ GPT re-review
→ Claude audit
→ Human approval before merge
```
