# INTERNAL-UAT-RESULTS-TRUST-HARDENING-1 — High-Trust Results Page Coherence

---
work_id: INTERNAL-UAT-RESULTS-TRUST-HARDENING-1_high_trust_results_page_coherence
branch: work/INTERNAL-UAT-RESULTS-TRUST-HARDENING-1-high-trust-results-page-coherence
status: IMPLEMENTATION_COMPLETE_PENDING_REVIEW
head_sha: b55e6e7
---

## Executive verdict

Resolved all six **HIGH** internal UAT trust/coherence defects on the working results page (`analysis_id: 6bcbf1de-d97f-4a1c-9556-e3a6e0625fd1`) without changing parser, intelligence, signal activation, scoring, lab ranges, or result-versioning logic. Fixes combine backend compiler copy hardening (hypothesis titles, lifestyle paragraph) with frontend render-only labelling, scrubbing, and hierarchy alignment.

**Do not merge** until Claude audit, GPT architectural review, and human approval.

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
| Frontend belt | `hypothesisDisplayCopy.neutraliseHypothesisTitleForDisplay` in `PrimaryFindingAndWhy` (render-only from existing counter-evidence) |
| Counter-evidence | Unchanged and still visible |

### IUAT-002 — Pattern-groups placeholder

| Layer | Detail |
|-------|--------|
| Visible text | "Pattern groups are not available…" |
| Condition | `clusters.length > 0` && `showPatternGroupBuckets=false` |
| Component | `ResultsBodyOverview.tsx` |
| Fix | When clusters exist but buckets hidden: "Detailed pattern groups are hidden in this view…" |

### IUAT-003 — 79 markers vs 9/9 expected

| Layer | Detail |
|-------|--------|
| Toolbar | `page.tsx` → "79 uploaded markers" / "Uploaded markers" |
| Data quality | `PipelineStatus.tsx` → "9 of 9 key markers available for this headline interpretation" |
| Calculation | Unchanged — copy only |

### IUAT-004 — Markdown / internal wording in body overview

| Layer | Detail |
|-------|--------|
| Examples | `**Cardiovascular 4 Biomarkers**`, "analytical model" |
| Producer | `lifestyle_consumer_surface_v1._metabolic_modifier_paragraph` |
| Scrubber | `retailNarrativeSanitize.ts` — `Cardiovascular N Biomarkers` mapping |
| Fix | Consumer lifestyle paragraph; markdown strip + token replacement at render |

### IUAT-005 — Homocysteine vs vascular hierarchy

| Layer | Detail |
|-------|--------|
| Hero lead | `resolveHeroPrimaryStory` — page1 concern lead (homocysteine) |
| Subline | Changed from "Most relevant area:" → "Broader system context:" |
| Scoring / IDL ranking | Unchanged |

### IUAT-006 — Transferrin "Critical" in driver band

| Investigation | `critical` status from backend biomarker DTO; `humanizeStatus` capitalised to "Critical" |
| Fix | `formatConsumerDriverBandStatusLabel` in driver band only — uses backend `interpretation` text when present; maps scoring-tier `critical` to "Needs review" when no interpretation cue |
| Transferrin scenario | interpretation "below the lab reference range" → "Below range" |
| Lab ranges / scoring | Unchanged |

---

## Files changed

| File | Change |
|------|--------|
| `backend/core/analytics/report_compiler_v1.py` | IUAT-001 hypothesis title neutralisation |
| `backend/core/analytics/lifestyle_consumer_surface_v1.py` | IUAT-004 consumer metabolic paragraph |
| `backend/tests/regression/test_internal_uat_results_trust_hardening.py` | Regression tests |
| `frontend/app/lib/hypothesisDisplayCopy.ts` | IUAT-001 render-only title helper |
| `frontend/app/lib/resultsPageLayout.ts` | IUAT-005 hero subline; IUAT-006 driver status |
| `frontend/app/lib/retailNarrativeSanitize.ts` | IUAT-004 Cardiovascular label scrub |
| `frontend/app/components/results/ResultsBodyOverview.tsx` | IUAT-002 hidden-buckets copy |
| `frontend/app/components/results/ResultsHeroBlocks.tsx` | IUAT-006 driver band labels |
| `frontend/app/components/results/PrimaryFindingAndWhy.tsx` | IUAT-001 hypothesis display |
| `frontend/app/components/pipeline/PipelineStatus.tsx` | IUAT-003 key-marker wording |
| `frontend/app/(app)/results/page.tsx` | IUAT-003 uploaded-marker wording |
| `frontend/tests/lib/resultsTrustHardening.test.ts` | IUAT-001–006 tests |
| `frontend/tests/lib/resultsHeroAlignment.test.ts` | IUAT-005 expectation update |
| `docs/sprints/launch_core_carry_forward_register.md` | CF-RESULTS-COPY-PATTERN-GROUPS-1 resolved; deferred IUAT items |

---

## Boundary confirmations

- Frontend remains **render-only** — no clinical inference, no abnormality calculation, no severity invention
- Parser, intelligence, signal activation, scoring, lab reference ranges, and result versioning **unchanged**
- No dummy/fallback `clinician_report_v1`
- Stale/incompatible warnings **not** hidden or bypassed
- Lab-provided ranges remain authoritative; no global/default ranges introduced
- MEDIUM/LOW UAT items deferred to carry-forward register (CF-IUAT-DEFER-001–006)

---

## Test output

### Backend (new)

```
python -m pytest backend/tests/regression/test_internal_uat_results_trust_hardening.py -q
...                                                                      [100%]
3 passed
```

### Frontend (new)

```
npm test -- tests/lib/resultsTrustHardening.test.ts
6 passed
```

### Architecture gate

```
architecture_validation_gate: PASS
day_one_architecture_validation: PASS
day_one_launch_estate_gate: PASS
validation_status: PASS (medical_frame_identity_index, context_modifier_catalogue, active_signal_context_gate_reachability)
medical_intelligence_architecture_validation: PASS
```

### Regression suite (required)

```
python -m pytest backend/tests/regression/test_internal_uat_result_versioning_dto_contract.py -q  → 7 passed
python -m pytest backend/tests/regression/test_active_signal_context_gate_reachability.py -q     → 21 passed
python -m pytest backend/tests/regression/test_dhea_s_high_activation.py -q                      → 37 passed
```

### Frontend build note

`npm run build` fails on a **pre-existing** TypeScript error (`result_versioning` vs `result_version` on `AnalysisResult` in `page.tsx:665`) unrelated to this sprint. Jest unit tests for changed modules pass.

---

## Carry-forward register

- **Resolved:** CF-RESULTS-COPY-PATTERN-GROUPS-1 (IUAT-002)
- **Opened:** CF-IUAT-DEFER-001 through CF-IUAT-DEFER-006 for deferred MEDIUM/LOW polish

---

## Review route

```
Cursor implementation (this sprint)
→ Claude audit
→ GPT architectural review
→ Human approval before merge
```
