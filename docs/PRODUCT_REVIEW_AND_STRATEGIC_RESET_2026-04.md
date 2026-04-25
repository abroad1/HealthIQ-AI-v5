# HealthIQ AI v5 — Product Review & Strategic Reset
**Date:** April 2026  
**Scope:** Full codebase, documentation, architecture, and product strategy  
**Status:** Unvarnished — nothing withheld

---

## Executive Summary

You have built something genuinely rare: a deterministic, clinician-grade metabolic reasoning engine with 50+ sub-engines, 103 canonical biomarkers, 187 knowledge packages, and a reproducibility story most health startups will never have. That is not hyperbole — it is a legitimate technical asset.

You have not yet built a product.

The delta between the engine and the product the user experiences is enormous, and that gap is what has been making you feel lost. After months of sprints the results page is impressive, the rest is near-empty. No PDF export. No trend view. No action hub. No pricing. No sharing. No onboarding. Dashboard and Reports are the same history list rendered twice. Profile is read-only. Settings is a theme toggle. The commercial surface is zero.

The core strategic risk is that the engine's momentum could run out before the product shell catches up. Everything below is oriented around preventing that.

---

## Part 1 — What You Have Built (the honest ledger)

### 1.1 The Engine (approximately 8/10 complete for Phase 1)

This is the product's genuine asset and it is real:

- **Pipeline:** A 2,200-line orchestrator runs canonicalisation → unit normalisation → derived metrics → signal evaluation → clustering → burden/capacity scaling → influence propagation → precedence/calibration/causal/conflict/arbitration → insight graph → explainability → IDL → narrative compilation → clinician report → DTO. Every step writes versioned hashes to a replay manifest. This is not vapourware.
- **Analytics module:** 45+ dedicated sub-engines (`signal_evaluator`, `root_cause_compiler_v1`, `insight_graph_builder`, `interpretation_display_layer_publish_v1`, `narrative_report_compiler_v1`, `arbitration`, `calibration`, `causal`, `conflict`, `precedence`, `burden`, `capacity_scaling`, `explainability_report`). Each has a defined contract.
- **SSOT:** 4,600 lines across biomarkers, ranges, units, labs, clusters, scoring policy, and registries for arbitration/precedence/conflict/calibration/evidence/causal. 103 canonical biomarker definitions.
- **Knowledge Bus:** 187 signal packages, 6 root-cause hypothesis YAMLs, pathway explainer libraries, phenotype definitions, interaction maps. Loaded at runtime by `SignalRegistry`.
- **Governed LLM usage:** LLMs are double-opt-in gated, confined to upload parsing and Layer C narrative translation. The analytical core is deterministic. That architectural boundary is correctly held and is a meaningful differentiation.

**Bottom line:** The engine is the moat. It is also roughly the only thing that works end-to-end.

### 1.2 The Product Shell (approximately 2/10 complete for Phase 1)

| Surface | Reality |
|---|---|
| Landing page | Exists. Positioning is reasonable. No pricing. |
| Upload flow | Works. LLM parse + deterministic fallback + questionnaire. Real. |
| Results page | 826 lines. 10+ sections. Deep. Probably overwhelming for new users. |
| Dashboard | 131 lines. 5 most recent analyses. Two CTA cards. Placeholder. |
| Reports | 109 lines. Paginated list. Same data as dashboard. `reports.ts` service is disabled (`API_BASE_URL = 'about:blank'`). |
| Profile | Read-only echo of auth metadata. "Editing profile is not available yet." |
| Settings | Light/dark theme toggle. 96 lines. "Settings are not synced." |
| PDF export | Not built. |
| Trend/longitudinal view | Not built. |
| Action hub / recommendations | Not built. |
| Sharing / clinician handoff | Not built. |
| Pricing / paywall | Not built. |
| Onboarding | Not built. |
| Retest reminders | Not built. |
| Email verification / password reset / account deletion | Not built. |

The PRD lists all of the above as deliverables. Nearly none are implemented.

---

## Part 2 — What Is Actually Wrong

### 2.1 The Engine Has Real Correctness Bugs

This is the most important finding because the "deterministic moat" claim is the strategy's core bet. Two confirmed bugs undermine it:

**Bug 1: Contradictory signals fire simultaneously (`signal_evaluator.py`)**  
`_evaluate_lab_range_activation_state` ignores `enable_upper_bound` / `enable_lower_bound` flags. On the same panel value, both `signal_total_cholesterol_high` and `signal_total_cholesterol_low` can be marked active simultaneously. A user whose report says they are simultaneously too high and too low on cholesterol will — correctly — not trust the product.

**Bug 2: One-sided lab ranges produce "Not scored — insufficient numeric bounds" (`orchestrator.py`)**  
`_has_valid_numeric_bounds` requires both min AND max to be numeric. Commercial blood panels commonly report LDL with only an upper bound and HDL with only a lower bound. The engine silently skips scoring these and surfaces the error message. This affects a significant proportion of real-world panels.

**Bug 3: WHY reasoning covers 6 of 137 runtime signals (`root_cause_compiler_v1.py`)**  
The root cause compiler is wired for exactly: `hcy`, `hba1c_high`, `hepatic_alt_context`, `thyroid_tsh_context`, `insulin_resistance`, `systemic_inflammation`. The other ~131 signals produce no governed WHY output. The clinician summary keys off `top_findings[0]`, which silently omits root-cause content when the lead signal is not one of the six. This was acknowledged in `docs/METABOLIC_PATHWAY_COVERAGE_AUDIT_2026-03-20.md` and `docs/investigations/PRODUCT_REALITY_AND_DIRECTION_AUDIT.md` — it is known, and it has not been fixed.

These three bugs should be fixed before any new feature is built. They sit directly in the product's claimed strength.

### 2.2 The Results Page is Doing Everything and Users Are Likely Lost

The results page renders, in a single scroll:
- Retail narrative summary
- Body overview / balanced systems summary
- Primary finding + WHY
- Why-this-lead-won
- System understanding
- Layer C insights
- Interpretation patterns
- Investigation spine
- Longitudinal narrative
- Next steps
- Clinician report (advanced)
- Biomarker dials
- Cluster summary

For a first-time user who uploaded their blood test hoping for clarity, this is a wall. The strategy document itself flags this risk ("a product built for clinicians masquerading as retail") but the UI has not been edited to address it. More analysis is not more clarity. The product needs a primary view that leads with one thing and gates depth behind deliberate exploration.

### 2.3 The Governance System is Consuming Delivery Bandwidth

The Automation Bus / Knowledge Bus / Gate control-plane is a multi-role, four-stage governance system with detailed SOPs, prompt hardening rituals, audit schemas, and execution tokens. It was designed for a future where this product is regulated software in a clinical workflow. 

For a pre-launch B2C consumer product where the most valuable information in the world is "what do real users say when they try to use this," the governance system is doing work that should be done by shipping to users and reading feedback. The SOPs are excellent documents. They are also the reason every sprint has a Stage 0, 1A, 1B, 1C, 1D, 2, 2A, 2B, 2C, 3, 4, 4A, and 5 before anything changes in the codebase.

This is a judgment call, not a condemnation. If Phase 3 is regulated software, you want these habits embedded early. But right now the governance overhead is a meaningful fraction of your total sprint cost, and the product shell is 2/10 complete.

**Recommendation:** Preserve the governance gates for Intelligence Core changes (engine correctness matters). For product shell work — UI pages, export flows, pricing, onboarding — use a lighter review model. The risk profile is different.

### 2.4 The Doc Estate is Ungoverned and Self-Contradicting

You have 228+ markdown files. Many of them contradict each other:

- `docs/DOCUMENTATION_HIERARCHY.md` declares `ARCHITECTURE_REVIEW_REPORT.md` as "Level 1 PRIMARY SSOT."
- `docs/README_V5.2_BASELINE.md` re-declares itself as the top authority.
- `docs/context/PROJECT_STRUCTURE.md` declares itself "Level 2 CANONICAL SPECIFICATION."
- `docs/DEPRECATED_ARCHITECTURE_NOTICE.md` deprecates two docs while simultaneously claiming `ARCHITECTURE_REVIEW_REPORT.md` reflects "actual implementation status" — that document is from Sprint 14 (October 2025).
- There are five versions of the strategy plan (v1.4, v1.5 draft, v1.5 FINAL, v1.5 FINAL Addendum, v1.5 FINAL amended).

There are also ~40 root-level firefighting fix-report markdown files (`ALIAS_NORMALIZATION_INSTRUMENTATION.md`, `BIOMARKER_PERSISTENCE_FIX.md`, `COMPLETE_FLOW_FIX_FINAL.md`, `EVENTSOURCE_DUPLICATION_FIX.md`, etc.) totalling ~293KB. These tell the real history of the project: months of debugging cycles on issues that should have been settled earlier.

A new contributor — or you, six months from now — cannot use this doc estate to understand the product. The most honest docs in the repo are the ones that say so: `docs/investigations/PRODUCT_REALITY_AND_DIRECTION_AUDIT.md` and `docs/METABOLIC_PATHWAY_COVERAGE_AUDIT_2026-03-20.md`. Read those before any others.

### 2.5 Repo Hygiene Is Actively Slowing You Down

The repository has accumulated significant structural debt:

- `_archived_app_root_20251012/` — full archived copy of the old frontend at the root.
- `_cursor_backup_stabilize_upload/` — another working-state backup at the root.
- Root-level `components/`, `queries/`, `state/`, `tests/`, `tests_archive/`, `stories/` — leftovers from the pre-restoration Vite/React layout, some with real code, some empty, all competing with the canonical `frontend/app/` tree.
- Root-level `vite.config.js`, `tsconfig.app.json`, `tsconfig.stories.json`, `postcss.config.js`, `tailwind.config.js`, `tailwind.config.ts` (both), `index.html`, `jest.config.js`, `jest.setup.ts`, `next.config.js`, `next-env.d.ts`, `playwright.config.ts`, `package.json`, `package-lock.json`, `bun.lockb` — all duplicating configs that also exist under `frontend/`.
- `venv/` committed to the repo.
- `.next/` build output committed to the root.
- `backend/frontend/package.json` — a two-line accidental file from running `npm install` in the wrong directory.
- Two test databases (`backend/test.db`, `backend/healthiq_test.db`).
- Multiple artifact directories: `backend/artifacts/`, `backend/reports/`, `backend/sprint10_test_report_*.txt`, `reports/`, `playwright-report/`, `test-results/`, `coverage/`, `.pytest_cache/`.
- Malformed filenames that look like PowerShell commands accidentally piped into filenames.

None of this is catastrophic individually. Together it means every new contributor spends time figuring out which config files are live, which source tree is real, and why there are two package.jsons at different levels. It is a constant low-grade drag on velocity.

### 2.6 The Orchestrator Is a 2,200-Line God Function

`backend/core/pipeline/orchestrator.py` is 2,212 lines with a single `run()` method that connects every Layer A and Layer B step in sequence. The sub-engines each have clean contracts. The method that wires them together does not. Any regression to pipeline step ordering requires reading 2,000 lines of sequential code. This is a testability and maintainability risk that grows with every sprint.

### 2.7 SSE Progress Reporting Is Fake

`GET /api/analysis/events` sleeps one second, emits a fake "completed" event, and closes. The frontend `PipelineStatus` component and pipeline phase display are driven by fabricated events. The backend pipeline runs synchronously in the POST handler with no real progress reporting. For a pipeline that takes real time, this is visible to users as a black box with a spinner followed by sudden completion.

### 2.8 Frontend-Backend Contract Drifts Without Enforcement

Frontend types in `frontend/app/types/analysis.ts` are not generated from backend Pydantic schemas. An OpenAPI spec exists in `docs/openapi.yaml` but there is no build-time sync or type generation. The symptom is `as any` casts on the results page and in the upload page. The `Insight.id` vs `insight_id` naming inconsistency (documented in a root-level fix report) was this class of problem in practice. Without automatic contract enforcement, this will keep happening.

### 2.9 The Questionnaire Has No Visible Payoff

The questionnaire is 59 questions. The orchestrator uses many of them through `QuestionnaireMapper` and `LifestyleModifierEngine`. However, the results page shows no feedback loop: nothing explicitly tells the user "your sleep of 5 hours modified this interpretation" or "your waist circumference was factored into this assessment." The user fills in 59 questions and experiences the results as if they did not.

### 2.10 Privacy Disclosure Gap on LLM Parsing

Upload goes through Gemini (a third-party LLM) before falling back to deterministic parsing. The landing page and upload flow make no mention of this. For a privacy-forward UK-first health product handling raw blood test data, this is both a GDPR risk and a trust gap. Users who care about their health data generally also care about who processes it.

---

## Part 3 — Why the Sprints Have Felt Underwhelming

The honest answer is that the sprint cadence has been optimised for engine depth rather than product completeness, and the governance model has made product-shell work as expensive as engine work.

The pattern you are in:
1. A complex analytical sprint is designed with full governance (Stages 0–5, prompt hardening, audit, gate).
2. The sprint succeeds — a new sub-engine, signal package, or pipeline stage is added or improved.
3. The product looks exactly the same to a user because none of the sprint's output is visible in the product shell.
4. Repeat.

The engine has grown. The product has not. After enough cycles of this the disconnect between effort and perceived progress becomes demoralising — even though the underlying asset is real and valuable.

There is also a secondary pattern: each time the product shell has been attempted, it has uncovered integration issues (the upload fix sprints, the DTO alignment report, the SSE duplication fix, the results state sync, the enum fix) that pulled the team back into firefighting. This suggests the integration layer between engine and product is not stable enough to build product shell features confidently on top of — and fixing that is prerequisite work, not a distraction.

---

## Part 4 — What to Do About It

### 4.1 Immediate: Fix the Engine Correctness Bugs (1–2 weeks)

Before any new feature work, fix:
1. `signal_evaluator.py` — honour `enable_upper_bound` / `enable_lower_bound` flags. Contradictory signal activation is a trust-destroying user experience.
2. `orchestrator.py` `_has_valid_numeric_bounds` — allow one-sided ranges. One-sided bounds are common in real commercial panels.
3. `root_cause_compiler_v1.py` — either expand WHY coverage to the top 20–30 signals by prevalence, or gracefully surface "WHY analysis not yet available for this marker" rather than silently returning nothing.

These bugs live in the moat. Fix them first.

### 4.2 Stabilise the Integration Layer (1–2 weeks)

Before building any new product shell features:
1. Generate frontend types from Pydantic schemas (use `datamodel-code-generator` or equivalent) — eliminate the `as any` casts.
2. Replace the fake SSE endpoint with real pipeline phase reporting, or remove it and replace with a simple polling mechanism. The fake progress report is worse than no progress report.
3. Make the `reports.ts` service either real or removed — a service file set to `'about:blank'` is a trap.

### 4.3 Product Shell Sprint: Close the User Journey (4–6 weeks)

The user journey currently is: upload → results → (dead end). Every user who completes that journey and wants to do anything else hits a wall. Close the journey with:

1. **PDF export.** The PRD named this. The clinician report and results DTO are already structured for it. Render to PDF server-side and offer a download. This is also the first shareable artefact.
2. **Actions hub.** A simple page that distils the top 3–5 actionable recommendations from the results DTO into a card format. Not a wall of text — cards with a heading, one paragraph, and a source citation. The intervention annotation engine already produces structured output for this.
3. **Trend view.** A simple biomarker chart with history across analyses. The history endpoint exists. Plot it. Even a table with delta arrows is meaningful longitudinal data.
4. **Pricing and account tier.** Decide: first analysis free, paid after. Add Stripe. Without this, you have no commercial product.

### 4.4 Results Page: Lead With One Thing

The results page needs an editorial pass, not an engineering pass. The user's first view should answer: "What is my most important finding and what does it mean?" Everything else — systems breakdown, clinician report, biomarker dials, cluster summary — should require a deliberate click to expand. 

Suggested hierarchy:
1. **Primary finding card** (phenotype-level name + 2-sentence plain-English why + severity indicator)
2. **Top 3 signals that drove it** (with expandable detail)
3. **Your system health overview** (balanced systems summary — the simplest version)
4. **Go deeper** (everything else behind a tab or accordion)

The content is already in the DTO. This is a frontend-only change that requires no engine work.

### 4.5 Clean the Repository

Do this once as a dedicated cleanup sprint, not incrementally. Specifically:
- Delete `_archived_app_root_20251012/`, `_cursor_backup_stabilize_upload/`
- Delete root-level `components/`, `queries/`, `state/`, `tests/`, `tests_archive/`, `stories/`
- Delete root-level duplicate config files (`vite.config.js`, old `tailwind.config.js`, old `postcss.config.js`, `tsconfig.app.json`, `tsconfig.stories.json`, `index.html`, root `jest.config.js`)
- Remove `venv/` from git (add to `.gitignore`)
- Remove `.next/` from git (add to `.gitignore`)
- Delete `backend/frontend/package.json`
- Move the 40 root-level fix-report markdowns to `docs/archived_fix_reports/` or delete them
- Delete the malformed filenames at root

This is not glamorous but it will make every subsequent sprint faster.

### 4.6 Rationalise the Documentation

One pass, one afternoon:
1. Delete all superseded strategy doc versions. Keep only `HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.5_FINAL_ADOPTED.md`.
2. Create a single `docs/README.md` that acts as the true index with two sentences per document describing what it is and whether it is current.
3. Archive `docs/ARCHITECTURE_REVIEW_REPORT.md` — it is from Sprint 14 and no longer reflects reality.
4. The two most honest documents in the repo are `docs/investigations/PRODUCT_REALITY_AND_DIRECTION_AUDIT.md` and `docs/METABOLIC_PATHWAY_COVERAGE_AUDIT_2026-03-20.md`. Treat those as ground truth and link to them from the README.

### 4.7 Recalibrate Governance for Phase 1 Reality

The Automation Bus governance is appropriate for Intelligence Core changes. Apply it there.

For product shell work (UI pages, export, pricing, onboarding, trend view, action hub), adopt a lighter model:
- Branch → implement → PR review → merge
- No Stage 0–5 ceremony
- Reserve the full gate process for backend engine changes where correctness matters deterministically

The risk profile of adding a PDF download button is categorically different from modifying `signal_evaluator.py`. Treat them differently.

### 4.8 Expand WHY Reasoning to the High-Prevalence Signals

The engine's credibility rests on WHY. Six signals is not enough for real-world panels which will almost always return a signal that falls outside those six. Prioritise by prevalence in real blood panels:
- Lipid signals (LDL, HDL, triglycerides, total cholesterol) — extremely common
- Iron panel (ferritin, transferrin saturation) — very common
- Vitamin D — extremely common
- Full thyroid beyond TSH alone
- Inflammatory markers (CRP, WBC) beyond `systemic_inflammation`
- Renal markers — currently has zero active interaction-map edges

This is engine depth work that actually changes what users experience.

### 4.9 Add Privacy Disclosure to the Upload Flow

Before the user submits their blood test data, add a one-sentence disclosure: "Your report is parsed using a third-party AI service (Google Gemini). Raw data is not stored by the parsing service." This is both the right thing to do and a UK GDPR requirement.

---

## Part 5 — What This Product Could Be

The strategy document (v1.5) is right. The engine you have built is the hardest part. Deterministic metabolic interpretation with governed WHY reasoning, phenotype mapping, structured causal chains, and reproducible analytics — most health startups trying to do this use LLMs all the way down and will not have a defensible answer when clinicians ask "how did you get this result?"

You have that answer. The engine gives it.

What is needed now is to close the distance between "we have a remarkable engine" and "a person uploads their blood test and understands their health better than they did before, takes an action because of it, and pays for the privilege."

That distance is almost entirely in the product shell, the results presentation, and the commercial infrastructure. None of it requires more analytical depth. It requires design and product engineering focus for a fixed period — 6 to 8 weeks of deliberate product-shell work — with the governance overhead dialled back for that scope.

After that window:
- A user can upload → read a clear primary finding → understand why → see their top actions → export a summary for their GP → track their markers over time → pay for access.
- That is a product. Not a remarkable engine. A product.

The engine you have built deserves one.

---

## Summary Table

| Area | Status | Priority |
|---|---|---|
| Engine correctness bugs (signal activation, one-sided ranges, WHY coverage) | Broken | **Fix now** |
| Frontend-backend type contract | Drifting | **Fix now** |
| Fake SSE progress reporting | Misleading | **Fix now** |
| Results page hierarchy / UX | Overwhelming | **High** |
| PDF export | Missing | **High** |
| Actions hub | Missing | **High** |
| Trend / longitudinal view | Missing | **High** |
| Pricing / paywall | Missing | **High** |
| Repo hygiene | Poor | **Medium** |
| Doc rationalisation | Conflicted | **Medium** |
| Privacy disclosure on upload | Missing | **Medium** |
| WHY reasoning coverage expansion | Thin (6/137 signals) | **Medium** |
| Governance calibration for Phase 1 | Miscalibrated | **Medium** |
| Questionnaire feedback loop visibility | Invisible to user | **Low** |
| Orchestrator decomposition | Fragile | **Low (Phase 2)** |
| Phenotype display in UI | Not surfaced | **Low (Phase 2)** |

---

*This review was produced by reading the full codebase and documentation. The most truthful pre-existing documents in the repository are `docs/investigations/PRODUCT_REALITY_AND_DIRECTION_AUDIT.md` and `docs/METABOLIC_PATHWAY_COVERAGE_AUDIT_2026-03-20.md` — they align closely with the findings above and should be treated as ground truth alongside this report.*
