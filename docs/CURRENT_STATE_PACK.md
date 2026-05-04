# HealthIQ AI — Current-State Pack

**Last updated:** 2026-05-04  
**Audience:** Leadership, new contributors, anyone needing a fast orientation  
**Status:** LIVE — maintained alongside major product milestones

This is the compact leadership pack. Read these documents in order to understand what HealthIQ AI is, where it is today, and what is being built next.

---

## The Seven Documents

### 1. Product Review & Strategic Reset — April 2026
**Path:** `docs/PRODUCT_REVIEW_AND_STRATEGIC_RESET_2026-04.md`  
**Read time:** ~20 minutes

The most complete, honest, repo-grounded state-of-truth document in the project. Produced April 2026. Covers:
- What the engine actually is (the honest ledger)
- What the product shell was missing at reset time
- The three engine correctness bugs (now fixed)
- Why sprints were feeling unproductive
- The 8-sprint reset plan and its rationale
- Documentation and repo hygiene problems

**Read this first.**

---

### 2. Product Reality & Direction Audit — April 2026
**Path:** `docs/investigations/PRODUCT_REALITY_AND_DIRECTION_AUDIT.md`  
**Read time:** ~15 minutes

The technical companion to document 1. Produced by a repo-grounded code audit. Provides:
- Exact file paths and line numbers for the engine bugs
- Reproducible evidence for the contradictory signal activation issue
- Exact code for the one-sided bounds problem
- WHY coverage gap with signal-by-signal detail

**Read alongside document 1.**

---

### 3. Metabolic Pathway Coverage Audit — March 2026
**Path:** `docs/METABOLIC_PATHWAY_COVERAGE_AUDIT_2026-03-20.md`  
**Read time:** ~10 minutes

The definitive analytical coverage map. Shows, for every metabolic pathway:
- Which signals are registered
- Which have WHY hypothesis assets and which do not
- Which have phenotype fixtures
- Which have interaction map edges

**Key finding that remains partially unresolved:** WHY Wave 1 (lipid panel + Vitamin D) is now complete. Wave 2 (iron, inflammatory, renal, expanded thyroid) is not yet started. The renal pathway has zero interaction-map edges.

---

### 4. Reset Sprint Plan — April 2026
**Path:** `docs/RESET_SPRINT_PLAN_2026-04.md`  
**Read time:** ~10 minutes

The 8-sprint plan produced alongside the April review. All 8 sprints are now complete (see `docs/SPRINT_STATUS.md`). Read this to understand what was fixed, in what order, and why.

---

### 5. CLAUDE.md — Permanent Project Context
**Path:** `.claude/CLAUDE.md`  
**Read time:** ~5 minutes

The permanent context file. Kept current. Contains:
- What HealthIQ is and is not (non-negotiable)
- The three-layer architecture rule
- The multi-LLM governance model
- Current active focus (as of 2026-05)
- Standing lessons and branch discipline

**Read this to understand the non-negotiables.**

---

### 6. Strategic Vision v1.5 FINAL ADOPTED
**Path:** `docs/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.5_FINAL_ADOPTED.md`  
**Read time:** ~25 minutes

The master strategic record for Phase 1. Governs:
- What HealthIQ is being built as (long-term positioning)
- Phase 1 / Phase 2 / Phase 3 structure
- What must be true before Phase 1 is launchable
- Strategic bets and sequencing rationale

**Read to understand direction and phase structure.** The April 2026 reset operates within this strategy.

---

### 7. Sentinel Phase 1 Implementation Report — May 2026
**Path:** `docs/testing/healthiq_sentinel_phase1_implementation_report.md`  
**Read time:** ~10 minutes

The current quality layer truth. Produced 2026-05-03. Documents:
- What regression coverage exists (32/32 tests pass)
- Exactly what each test covers
- What is explicitly deferred to Phase 2+ (with gap disclosure)
- How the Sentinel runner works

**Read to understand what quality assurance is currently in place.**

---

## Current Product State Summary

Based on the above documents and git history as of 2026-05-04:

### Engine
- Three trust bugs from the April 2026 audit have been fixed (R-1: signal activation flags, one-sided bounds, WHY fallback; R-1B: unscored marker trust gaps, string bounds, HbA1c unit harmonisation)
- WHY reasoning Wave 1 complete: total cholesterol high, Vitamin D low (R-8)
- WHY Wave 2 (iron, inflammatory, renal, expanded thyroid) — not yet started

### Product Shell
- All 8 reset sprints complete: integration stability, results restructure, PDF export, actions hub, trend view, pricing/paywall, WHY Wave 1

### Active Work (as of 2026-05)
- Questionnaire UX redesign — Q-1 (guided flow) and Q-2 (premium visual layer): both committed
- Wave 1 domain card work — D-1 through D-7 all committed to main
- Liver/alias fix hardening — committed (GGT trace alias, bilirubin venous alias)
- Sentinel Phase 1 — complete and merged

### Remaining Gaps (from coverage audit + April review)
- WHY Wave 2 coverage (iron, inflammatory, renal, expanded thyroid)
- Renal pathway: zero interaction-map edges
- Privacy disclosure on LLM parsing at upload (GDPR gap — verify if addressed)
- Frontend design system: no single documented source of truth
- Release confidence model: not formally defined

---

## What This Pack Does Not Replace

This pack gives leadership the current state. It does not replace:
- `docs/SPRINT_STATUS.md` for day-to-day sprint tracking
- `docs/DECISION_REGISTER.md` for settled architectural/product decisions
- `architecture/ARCHITECTURE_INDEX.md` for binding architecture constraints
- `docs/AUTOMATION_BUS_SOP_v1.3.1.md` for sprint execution governance
