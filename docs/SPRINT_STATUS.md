# HealthIQ AI — Sprint Status Register

**Last updated:** 2026-05-04  
**Status:** LIVE — update this document when sprint status changes  
**Maintainer:** Whoever completes or starts a sprint

This is the source of truth for what has been done, what is in progress, and what is next. Do not rely on git log archaeology for this information — update this file instead.

---

## Reset Sprints (April 2026 — all complete)

These are the 8 sprints defined in `docs/strategy/RESET_SPRINT_PLAN_2026-04.md`. All are now complete and merged to main.

| Sprint | Name | Type | Status | Branch / Commit |
|---|---|---|---|---|
| R-1 | Engine Trust Bugs | BEHAVIOUR / HIGH (Intelligence Core) | **COMPLETE** | `fix/R-1`: `7f48cb6`, `54d96b4` |
| R-1B | Unscored Marker Trust Gaps | BEHAVIOUR / HIGH (Intelligence Core) | **COMPLETE** | Branch `fix/unscored-marker-trust-gaps`: `7679f89` |
| R-2A | Backend SSE Removal | BEHAVIOUR (route layer) | **COMPLETE** | Branch `fix/integration-stability-backend`: `f74e5af` |
| Sprint 2 (FE) | Integration Stability — OpenAPI types, remove dead reports service | Frontend / Light | **COMPLETE** | `6d567c7` |
| Sprint 3 | Results Page Restructure | Frontend / Light | **COMPLETE** | `284d188` |
| Sprint 4 | PDF Export | Product Shell / Light | **COMPLETE** | `36a4f9f` |
| Sprint 5 | Actions Hub | Product Shell / Light | **COMPLETE** | `4887087` |
| Sprint 6 | Longitudinal Trend View | Product Shell / Light | **COMPLETE** | `4381984` |
| Sprint 7 | Pricing & Stripe Paywall | Commercial / Light | **COMPLETE** | `898d14c` |
| R-8 | WHY Coverage Wave 1 | BEHAVIOUR / HIGH (Intelligence Core) | **COMPLETE** | Branch `feature/why-coverage-expansion-wave-1`: `2f0b346` |

---

## Wave 1 Domain Card Work (post-reset — all complete)

Domain card sprints implementing the D-series wave 1 consumer domain narrative.

| Sprint | Name | Status | Commit |
|---|---|---|---|
| D-1 | Wave 1 consumer domain score assembler and DTO | **COMPLETE** | `449b854` |
| D-2 | Wave 1 consumer domain narrative assembly (IDL + D-1) | **COMPLETE** | `ec4a6a7` |
| D-3 | Wave 1 per-domain next steps and consumer domain cards | **COMPLETE** | `f0e13fc` (gate) / `8d897c5` (bus) |
| D-4 | Wave 1 domain card headline coherence, safe caveats, evidence anchors | **COMPLETE** | `2d3c3d2` |
| D-5 | Wave 1 runtime diagnosis (snapshot persistence, UAT id) | **COMPLETE** | `68b95b6` |
| D-6 | Wave 1 single-authority cards, driver meta, governed backfill helpers | **COMPLETE** | `f1e52cd` |
| D-7 | Wave 1 liver consequence coherence and confidence-marker UI labels | **COMPLETE** | `4e65556` |

---

## Alias / Hardening Fixes (post-reset — complete)

| Fix | Status | Commit |
|---|---|---|
| GGT trace alias, bilirubin venous alias, Wave 1 missing-marker coherence | **COMPLETE** | `43e181f` |

---

## Questionnaire UX Redesign

| Sprint | Name | Status | Commit |
|---|---|---|---|
| Q-1 | Guided section-by-section questionnaire flow | **COMPLETE** | `d096833` |
| Q-2 | Premium visual layer (intent, shell, pills, upload framing) | **COMPLETE** | `4d8517d` |

---

## Sentinel Quality Layer

| Phase | Status | Report |
|---|---|---|
| Phase 1 — changed-file classifier, alias sweep, escaped-defect pack, slug leakage guard, structured reports | **COMPLETE** (merged to main) | `docs/testing/healthiq_sentinel_phase1_implementation_report.md` |
| Phase 2 — Wave 1 narrative coherence guard, DTO schema comparison, Playwright rendering checks | **NOT STARTED** | Deferred — requires Playwright orchestration |

---

## Active / Upcoming Work (as of 2026-05-04)

| Area | Status | Notes |
|---|---|---|
| WHY Wave 2 — iron, inflammatory, renal, expanded thyroid | **NOT STARTED** | Defined in `docs/strategy/RESET_SPRINT_PLAN_2026-04.md` Sprint 8 Wave 2 targets. Requires full SOP. |
| Renal interaction-map edges | **NOT STARTED** | Zero edges currently. Flagged in pathway coverage audit. |
| Sentinel Phase 2 | **NOT STARTED** | Deferred per brief. Requires Playwright. |
| Privacy disclosure on LLM parsing at upload | **UNCERTAIN** | GDPR gap identified in April 2026 review. Verify whether addressed in current upload flow. |
| Frontend design system documentation | **MISSING** | No single documented source of truth. Recommend authoring. |
| Release confidence model | **MISSING** | No formal definition. Recommend authoring before first paying user launch. |

---

## How to Update This Document

When a sprint starts:
1. Change status to **IN PROGRESS**
2. Add the branch name

When a sprint completes and is merged:
1. Change status to **COMPLETE**
2. Add the merge commit hash

When something is blocked or a decision is pending:
1. Change status to **BLOCKED — [reason]**
2. Add a link to the blocking issue or decision

This document is owned by whoever is running the programme. It should reflect real state, not aspirational state.
