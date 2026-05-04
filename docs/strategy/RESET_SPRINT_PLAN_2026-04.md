# HealthIQ AI v5 — Reset Sprint Plan
**Date:** April 2026  
**Horizon:** 6–8 weeks  
**Source:** Product Review & Strategic Reset (docs/PRODUCT_REVIEW_AND_STRATEGIC_RESET_2026-04.md)  
**Purpose:** Give GPT the concrete specification to author work package prompts in the correct order.

---

## Governing Principles for This Reset

1. **Order is non-negotiable.** Engine trust bugs before product shell. Integration stability before new features. Do not reorder.
2. **Governance tier matters.** Sprints touching Intelligence Core (`backend/core/`, `backend/ssot/`, `backend/scripts/`) use full Automation Bus SOP. Sprints touching only frontend, services, or commercial surfaces use a lightweight PR-based model — branch → implement → review → merge.
3. **No new engine depth until Sprint 5.** Expanded WHY coverage is engine work and is valuable, but it comes after the product shell closes.
4. **Done means shipped, not merged.** Each sprint has explicit user-visible success criteria, not just code-change criteria.

---

## Sprint Overview

| # | Name | Type | Governance | Estimated Duration |
|---|---|---|---|---|
| 1 | Engine Trust Bugs | BEHAVIOUR (Intelligence Core) | Full SOP | 1–2 weeks |
| 2 | Integration Layer Stabilisation | MIXED | Full SOP (backend) / Light (frontend) | 1 week |
| 3 | Results Page Restructure | Frontend | Light PR model | 1 week |
| 4 | PDF Export | Product Shell | Light PR model | 1 week |
| 5 | Actions Hub | Product Shell | Light PR model | 1 week |
| 6 | Trend / Longitudinal View | Product Shell | Light PR model | 1 week |
| 7 | Pricing & Paywall | Commercial | Light PR model | 1–2 weeks |
| 8 | WHY Coverage Expansion | BEHAVIOUR (Intelligence Core) | Full SOP | 2 weeks |
| — | Repo & Doc Hygiene | Housekeeping | None | 1 day (do alongside Sprint 1) |

---

## Sprint 1 — Engine Trust Bugs

**Goal:** Eliminate the three correctness failures that directly undermine the deterministic moat claim.  
**Governance:** Full Automation Bus SOP. These are `BEHAVIOUR` / HIGH risk changes to Intelligence Core.  
**Branch naming:** `fix/engine-trust-bugs`

### Bug 1: Contradictory Signal Activation

**File:** `backend/core/analytics/signal_evaluator.py`  
**Function:** `_evaluate_lab_range_activation_state` (or equivalent activation evaluation function)  
**Problem:** `enable_upper_bound` and `enable_lower_bound` flags on signal definitions are not being honoured. A value can simultaneously activate both `signal_total_cholesterol_high` and `signal_total_cholesterol_low` on the same panel. Any signal pair with asymmetric bound gating is affected.  
**Required fix:**
- Before marking a signal active, check the signal definition's `enable_upper_bound` / `enable_lower_bound` flags.
- If `enable_upper_bound = false`, do not activate signals whose condition depends on the value being above a threshold.
- If `enable_lower_bound = false`, do not activate signals whose condition depends on the value being below a threshold.
- If both activation conditions would fire simultaneously after fixing, that is a signal definition error, not a code error — surface it as a configuration warning, not a runtime result.

**Regression target:** A test panel with a mid-range cholesterol value must not produce both `signal_total_cholesterol_high` and `signal_total_cholesterol_low` as active simultaneously.

### Bug 2: One-Sided Lab Range Scoring Failure

**File:** `backend/core/pipeline/orchestrator.py`  
**Function:** `_has_valid_numeric_bounds` (or the function used to determine whether a biomarker can be scored)  
**Problem:** The function requires both `min` AND `max` to be numeric. Commercial blood panels commonly report:
- LDL with only an upper bound (no lower bound — you cannot have too-low LDL clinically in most reporting conventions)
- HDL with only a lower bound (no upper bound)
- Many vitamin/mineral markers with only a lower bound

These produce "Not scored — insufficient numeric bounds for scoring" in the output, which surfaces to the user and destroys confidence in the result.  
**Required fix:**
- Allow a range to be valid if EITHER `min` or `max` is a valid numeric (not requiring both).
- For a max-only range: a value above max is out-of-range high; below max is in-range. No lower comparison is possible.
- For a min-only range: a value below min is out-of-range low; above min is in-range. No upper comparison is possible.
- The scoring function should handle one-sided ranges without error and without producing the "insufficient numeric bounds" message.

**Regression target:** A test panel including LDL with max-only and HDL with min-only range definitions must produce scored results for those markers, not the "insufficient bounds" error message.

### Bug 3: WHY Reasoning — Graceful Fallback for Non-Covered Signals

**Files:** `backend/core/analytics/root_cause_compiler_v1.py`, contracts and DTO  
**Problem:** WHY reasoning is governed for exactly 6 signal IDs: `hcy`, `hba1c_high`, `hepatic_alt_context`, `thyroid_tsh_context`, `insulin_resistance`, `systemic_inflammation`. When the lead signal is outside these six, the clinician summary silently contains no root-cause content. The user receives a primary finding with no WHY explanation — the engine's most claimed feature is invisible for the majority of real panels.  
**Required fix (minimum viable — full expansion is Sprint 8):**
- When `root_cause_compiler_v1` is asked for WHY reasoning on a signal ID it does not have a hypothesis for, it must return a structured fallback object rather than empty/null.
- The fallback should include: the signal name, its activation state, its lab range classification, and a standard phrase indicating that deep hypothesis analysis is not yet available for this marker.
- This fallback must be surfaced visibly in the results DTO and results page — not silently omitted.
- The clinician report must not key off `top_findings[0]` as if it always has WHY content. Add a null-guard that degrades gracefully when WHY is absent.

**Regression target:** A test panel whose lead signal is outside the six governed signals must produce a results DTO that includes a non-null, non-empty WHY section (even if it is the fallback phrase). The clinician summary must not be empty.

### Sprint 1 Success Criteria
- [ ] Contradictory signal activation is impossible for a single panel value — confirmed by test
- [ ] One-sided range biomarkers score without error on a real commercial panel structure
- [ ] Any lead signal produces a visible WHY output — either governed hypothesis or explicit fallback
- [ ] All existing golden panel tests continue to pass
- [ ] No change to output structure contracts (fallback is a value in an existing WHY field, not a new field)

---

## Sprint 2 — Integration Layer Stabilisation

**Goal:** Close the gap between backend and frontend so product shell work in Sprints 3–7 does not introduce new drift bugs.  
**Governance:** Backend changes (if any) use full SOP. Frontend/service changes use light PR model.  
**Branch naming:** `fix/integration-stability`

### Task 2A: Frontend Type Generation from Backend Pydantic

**Problem:** `frontend/app/types/analysis.ts` is hand-maintained and has drifted from backend Pydantic models. Evidence: `as any` casts in `results/page.tsx` (line ~149) and `upload/page.tsx` (line ~90). The `Insight.id` vs `insight_id` naming bug was this problem in practice.  
**Required fix:**
- Evaluate and adopt a type-generation approach: `datamodel-code-generator` (Python → JSON Schema → TypeScript), or FastAPI's built-in OpenAPI export piped to `openapi-typescript`.
- The goal is a `npm run generate-types` (or equivalent) command that regenerates `frontend/app/types/analysis.ts` from the backend schema.
- Add this as a step in local development setup docs. It does not need to be in CI yet — it needs to exist.
- Remove all `as any` casts in `results/page.tsx` and `upload/page.tsx`. If removing them reveals genuine mismatches, fix the mismatch — do not widen the type.

### Task 2B: Replace Fake SSE with Honest Progress Model

**File:** `backend/app/routes/analysis.py` (the `/events` endpoint, lines ~403–429)  
**Problem:** The SSE endpoint sleeps 1 second, emits a fake "completed" event, and closes. The pipeline runs synchronously in the POST handler. The frontend pipeline phase display is driven by fabricated events.  
**Required fix — choose one of:**

Option A (preferred if pipeline is fast enough): Remove SSE entirely. The POST `/start` endpoint runs the pipeline synchronously and returns when done. Replace the frontend's SSE listener with a simple polling call to `GET /result/{id}` every 2 seconds until status is COMPLETE or FAILED. Remove the `PipelineStatus` fabricated-phase display — replace with a simple spinner and elapsed time.

Option B (if pipeline latency makes polling painful): Keep SSE but emit real events from the orchestrator. The orchestrator must call a progress callback at each named phase boundary (canonicalisation complete, signal evaluation complete, etc.). The SSE endpoint streams these. This is more work but gives real progress to the user.

Either option eliminates the fake event. The fake event is worse than no event because it makes the system look faster than it is and breaks trust when the UI claims "completed" while the user can see the page is still loading.

### Task 2C: Remove Dead Service Paths

**File:** `frontend/app/services/reports.ts`  
**Problem:** `API_BASE_URL = 'about:blank'` — the reports service is disabled but still imported. Any code path that calls it silently fails or navigates to `about:blank`.  
**Required fix:** Delete `reports.ts` and remove all imports of it. If the Reports page uses it, replace with a direct call to the analysis history endpoint (which works) or remove the call and render from the already-loaded store state.

### Sprint 2 Success Criteria
- [ ] `npm run generate-types` (or equivalent) produces TypeScript types that match the backend Pydantic models
- [ ] No `as any` casts remain in results or upload pages
- [ ] SSE endpoint is either replaced with polling or replaced with real events — the fake 1-second sleep-and-complete is gone
- [ ] `reports.ts` is deleted and nothing imports it
- [ ] Results page and upload page load and function correctly end-to-end after these changes

---

## Sprint 3 — Results Page Restructure

**Goal:** The results page leads with one clear primary finding. Everything else is progressively disclosed.  
**Governance:** Light PR model. Frontend-only. No backend changes.  
**Branch naming:** `feature/results-ux-restructure`

### Specification

**Current problem:** The results page renders 10+ sections simultaneously. A first-time user has no clear answer to "what does this mean for me?"

**Target structure (top to bottom):**

**Section 1 — Primary Finding (always visible, above the fold)**
- Phenotype-level label (e.g. "Early Metabolic Stress Pattern" — not a signal ID)
- 2–3 sentence plain-English summary of what was found and why it matters
- Severity indicator (visual — colour or icon, not a number)
- "Download Report" button (Sprint 4)

**Section 2 — What's Driving This (always visible)**
- Top 3 signals: marker name, value, range status (low/normal/high/optimal), one-sentence interpretation
- "See all markers" link that expands the full biomarker dial section

**Section 3 — Your System Health (always visible)**
- Balanced systems summary: one row per body system, simple status indicator
- Maximum 6 systems shown; rest collapsed behind "show more"

**Section 4 — What This Means (expandable, collapsed by default)**
- Interpretation patterns
- WHY reasoning (if governed; fallback text if not)
- Investigation spine

**Section 5 — Actions (expandable, collapsed by default)**
- Top 3–5 intervention annotations as action cards
- Each card: heading, one paragraph, evidence level indicator

**Section 6 — Advanced / Clinician Report (expandable, collapsed by default, visually separated)**
- Full clinician report
- Layer C insights
- Cluster summary
- All biomarker dials

**What to remove or hide by default:**
- `WhyThisLeadWonSection` — move inside Section 4, collapsed
- `DeterministicNarrativeSurface` — if it duplicates the primary finding, remove it from the default view
- `LayerCInsightSection` — move to Section 6
- `InterpretationPatternsSection` — move to Section 4

**Constraint:** No backend changes. All data needed for this restructure is already in the DTO. This is a layout and information-architecture change only.

### Sprint 3 Success Criteria
- [ ] Primary finding is the first thing a user sees, above the fold on a standard laptop viewport
- [ ] A user can understand "what is my main finding" without scrolling
- [ ] Sections 4, 5, 6 are collapsed by default and expand on click
- [ ] All existing DTO content is still accessible — nothing is removed, only reorganised
- [ ] The full biomarker dial list is still reachable but not the default view
- [ ] The page renders without error on a completed analysis

---

## Sprint 4 — PDF Export

**Goal:** A user can download a PDF summary of their results. This is the first shareable artefact and the most-requested PRD feature.  
**Governance:** Light PR model. No Intelligence Core changes.  
**Branch naming:** `feature/pdf-export`

### Specification

**What the PDF must contain (minimum viable):**
1. User name + analysis date + test panel name
2. Primary finding (phenotype label + 2-sentence plain-English summary)
3. Top 3 driving signals with lab values and range status
4. System health overview (balanced systems summary — one sentence per system)
5. Top 3 recommended actions (from intervention annotation output)
6. Standard footer: "This report is for informational use only and is not a medical diagnosis. Please discuss findings with a qualified clinician."

**What the PDF must NOT contain:**
- The full clinician report (that is a separate export if it ever exists)
- Raw engine metadata, JSON keys, or internal scoring terminology
- Any content that is not already in the results DTO

**Implementation approach:**
- Server-side rendering is preferred: a `GET /api/analysis/{id}/export/pdf` endpoint that generates and streams a PDF using a Python library (WeasyPrint, ReportLab, or equivalent).
- The PDF template should be simple: HealthIQ logo/wordmark at top, clean typography, no charts in v1.
- The frontend adds a "Download Report" button on the results page that calls this endpoint and triggers a file download. The button placeholder was wired in Sprint 3 — this sprint makes it functional.

**Alternative (frontend-only, faster to ship):**
- Use a React-to-PDF library (e.g. `react-pdf`, `html2canvas` + `jsPDF`) to render a print-styled version of the results page primary finding section.
- Simpler to implement, lower quality output, no server endpoint needed.
- Acceptable for v1 if server-side approach takes more than 2 days.

### Sprint 4 Success Criteria
- [ ] "Download Report" button on the results page is functional (was placeholder in Sprint 3)
- [ ] Clicking it downloads a PDF file (not opens a new tab, not navigates away)
- [ ] PDF contains the six minimum sections listed above
- [ ] PDF is readable and presentable — not a JSON dump or raw text file
- [ ] PDF contains the non-diagnostic disclaimer footer
- [ ] Works for any completed analysis in the user's history (accessible from the history list too)

---

## Sprint 5 — Actions Hub

**Goal:** A dedicated page (and results section) showing the user's top actionable recommendations with enough context to act on them.  
**Governance:** Light PR model. Backend may need a lightweight endpoint; if so, full SOP applies only if it touches Intelligence Core.  
**Branch naming:** `feature/actions-hub`

### Specification

**What the actions hub is:**
- A page at `/actions` (or `/recommendations`) that shows the user's top 5–8 recommended actions from their most recent analysis
- Each action is a card: title, category (diet / supplement / lifestyle / medical referral), 1–2 sentence explanation, strength-of-evidence indicator, "source: [signal name]"
- Actions are sourced from `intervention_annotation` output already in the DTO — this is not new engine work

**What it is not:**
- A full supplement database browser
- A personalised treatment plan
- Medical advice (standard disclaimer applies)

**Integration with results page:**
- Section 5 of the restructured results page (Sprint 3) links to this hub
- The hub also appears as a nav item in the main navigation

**Data source:**
- Intervention annotation data is already in the DTO. If it is not surfaced in the API response, add it — that is a backend change and requires SOP review for the specific field.
- Do not add new engine logic. Use what the orchestrator already produces.

### Sprint 5 Success Criteria
- [ ] `/actions` page exists and renders for a logged-in user with at least one completed analysis
- [ ] Page shows at minimum 3 action cards
- [ ] Each card has: title, category label, explanation paragraph, evidence level, source signal
- [ ] Non-diagnostic disclaimer is present on the page
- [ ] Page is linked from main navigation and from the results page
- [ ] Page renders gracefully (empty state message) if no analysis exists

---

## Sprint 6 — Trend / Longitudinal View

**Goal:** A user who uploads a second blood test can see how their markers have changed.  
**Governance:** Light PR model. No Intelligence Core changes. Backend: a new API endpoint for history data (SOP applies only if it touches analytical logic — a history read endpoint does not).  
**Branch naming:** `feature/trend-view`

### Specification

**Minimum viable longitudinal view:**
- A page at `/trends` (or accessible from dashboard/reports)
- Shows a table of: biomarker name | most recent value | previous value | delta | trend arrow | range status
- Sorted by: markers with the largest absolute change first
- For users with only one analysis: shows "Upload another blood test to see your trends" empty state

**Chart (v1 — optional):**
- A simple line chart for a single selected biomarker across all analyses
- X-axis: analysis date; Y-axis: marker value with reference range band
- If charting library is not already in the frontend dependencies, use a simple table with delta values for v1 rather than adding a charting dependency

**Data source:**
- The history endpoint (`GET /api/analysis/history`) already returns past analyses
- The trend view reads from this + the most recent result DTO
- No new backend logic required for v1 — compute delta on the frontend from existing data

**Dashboard integration:**
- The dashboard page (currently a thin history list) should show a "Your trends at a glance" mini-section: top 3 markers with the largest positive or negative movement since last test, with arrows. This replaces or supplements the current empty CTA cards.

### Sprint 6 Success Criteria
- [ ] `/trends` page exists and renders for a logged-in user
- [ ] User with 2+ analyses sees a delta table with trend arrows
- [ ] User with 1 analysis sees a clear empty state message prompting a second upload
- [ ] Dashboard shows at least a "markers moved most" summary if 2+ analyses exist
- [ ] No backend engine changes; reads only from existing history endpoint data

---

## Sprint 7 — Pricing & Paywall

**Goal:** First-time users can pay for access. Without this, there is no commercial product.  
**Governance:** Light PR model. No Intelligence Core changes. This is infrastructure work.  
**Branch naming:** `feature/pricing-paywall`

### Specification

**Recommended model (decide before authoring this sprint):**
- Option A: First analysis free, £X/month for unlimited analyses + PDF export + trend view
- Option B: Free trial (3 analyses), then subscription
- Option C: Pay-per-analysis (£X per upload)

This document does not pick the model — that is a commercial decision. The sprint assumes a model has been chosen before work begins.

**Technical implementation:**
- Stripe integration (Stripe Checkout or Stripe Elements)
- A `/pricing` page with plan comparison and CTA
- Webhook handler for subscription events (`checkout.session.completed`, `customer.subscription.deleted`)
- User table in Supabase gains a `subscription_status` field (free / active / cancelled / trial)
- API middleware enforces plan limits: if user is on free tier and has already used their free analyses, `POST /api/analysis/start` returns 402 with a "upgrade required" response
- Frontend handles 402 gracefully — redirects to pricing page with a message

**What does NOT need to be gated behind paywall in v1:**
- The upload page (file parsing is not the premium service)
- Historical results already generated (users should always see results they already paid for or generated in trial)

**Compliance note:**
- Stripe's standard checkout handles PCI compliance
- UK consumer regulations require a cancellation flow — Stripe's customer portal handles this

### Sprint 7 Success Criteria
- [ ] `/pricing` page exists with plan details and a working "Subscribe" / "Buy" CTA
- [ ] Stripe checkout flow works end-to-end in test mode
- [ ] Subscribing updates user's `subscription_status` in the database
- [ ] A user on the free tier who has exhausted their free analyses is blocked from starting a new one and redirected to pricing
- [ ] A subscribed user can start analyses without restriction
- [ ] Cancellation is possible via Stripe customer portal link in settings

---

## Sprint 8 — WHY Coverage Expansion

**Goal:** Expand governed WHY reasoning to cover the highest-prevalence signals in real commercial blood panels.  
**Governance:** Full Automation Bus SOP. This is BEHAVIOUR / HIGH risk Intelligence Core work.  
**Branch naming:** `feature/why-coverage-expansion-wave-1`

**Note:** This sprint comes after the product shell closes (Sprints 3–7). It is high-value engine work, but it does not unlock any commercial milestone. Do not bring this forward.

**Wave 1 priority (mandatory starting point):** Lipid panel and Vitamin D first. These two groups cover the majority of UK commercial blood panel findings by prevalence. Delivering governed WHY for these two groups alone will produce a step-change in result quality for most real users. All other groups are Wave 2 and must not be included in this sprint's scope unless Lipid + Vitamin D are completed with time to spare.

### Target signals for Wave 1 (by prevalence in UK commercial panels)

| Signal Group | Specific Signals | Priority | Notes |
|---|---|---|---|
| Lipid panel | `signal_ldl_high`, `signal_hdl_low`, `signal_triglycerides_high`, `signal_total_cholesterol_high` | **Wave 1 — required** | Extremely common; currently WHY-silent |
| Vitamin D | `signal_vitamin_d_low` | **Wave 1 — required** | Among the most common single-marker findings in UK panels |
| Iron panel | `signal_ferritin_low`, `signal_ferritin_high`, `signal_transferrin_saturation_low` | Wave 2 | Iron deficiency and overload both common |
| Inflammatory | `signal_crp_high`, `signal_wbc_high` | Wave 2 | Beyond the existing `systemic_inflammation` signal |
| Renal | `signal_creatinine_high`, `signal_egfr_low`, `signal_urea_high` | Wave 2 | Currently zero active interaction-map edges |
| Thyroid (expanded) | `signal_ft4_low`, `signal_ft3_low` | Wave 2 | Beyond existing `thyroid_tsh_context` |

### What WHY expansion requires per signal group

For each group, the sprint must produce:
1. A root-cause hypothesis YAML in `knowledge_bus/root_cause/hypotheses/` following the existing schema
2. Wiring in `root_cause_compiler_v1.py` to load and apply the hypothesis for the relevant signal IDs
3. A governed test: a fixture panel that activates the target signal must produce a non-fallback WHY output in the results DTO
4. The existing 6-signal WHY coverage must be unaffected (regression)

### Sprint 8 Success Criteria
- [ ] Lipid panel and Vitamin D both have governed WHY reasoning (not fallback) — mandatory
- [ ] At minimum 1 additional Wave 2 group has governed WHY reasoning if capacity allows
- [ ] All existing golden panel tests pass
- [ ] A panel dominated by lipid findings produces a governed WHY output, not the fallback phrase
- [ ] A panel dominated by vitamin D deficiency produces a governed WHY output
- [ ] No new contradictory signal behaviour introduced
- [ ] The fallback mechanism from Sprint 1 Bug 3 continues to work correctly for signals outside the now-larger governed set

---

## Repo & Doc Hygiene (Parallel with Sprint 1 — 1 day, one person)

Do this as a separate branch (`chore/repo-hygiene`) while Sprint 1 engine work is in progress. It is not blocked by Sprint 1 and does not touch the engine.

### Delete from root
- `_archived_app_root_20251012/` — old frontend archive
- `_cursor_backup_stabilize_upload/` — working-state backup
- Root-level `components/`, `queries/`, `state/`, `tests/`, `tests_archive/`, `stories/` (verify each is not imported by anything live before deleting)
- Root-level duplicate configs: `vite.config.js`, `tsconfig.app.json`, `tsconfig.stories.json`, `postcss.config.js`, old `tailwind.config.js`, `index.html` (verify not used by Next.js build)
- Malformed filenames at root (the ones that look like PowerShell commands)
- `backend/frontend/package.json`

### Add to `.gitignore`
- `venv/`
- `.next/`
- `backend/test.db`
- `backend/healthiq_test.db`
- `backend/artifacts/`
- `playwright-report/`
- `test-results/`
- `coverage/`
- `.pytest_cache/`

### Move to `docs/archived/`
- The ~40 root-level fix-report markdown files (`ALIAS_NORMALIZATION_INSTRUMENTATION.md`, `BIOMARKER_PERSISTENCE_FIX.md`, etc.)
- `TEST_LEDGER.md`

### Doc rationalisation
- Delete all superseded strategy versions. Keep only `docs/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.5_FINAL_ADOPTED.md`.
- Create `docs/README.md` as the single entry point: a two-sentence description of each current doc with a link.
- Archive `docs/ARCHITECTURE_REVIEW_REPORT.md` — it is from Sprint 14 (October 2025) and no longer reflects implementation.
- The two most truthful documents remain: `docs/investigations/PRODUCT_REALITY_AND_DIRECTION_AUDIT.md` and `docs/PRODUCT_REVIEW_AND_STRATEGIC_RESET_2026-04.md`. Link to both from `docs/README.md`.

---

## Governance Calibration — Standing Rule for This Reset

| Work type | Governance model |
|---|---|
| `backend/core/` (any analytics, pipeline, signal evaluation, orchestration, root cause) | Full Automation Bus SOP (Stages 0–5) |
| `backend/ssot/` | Full Automation Bus SOP |
| `backend/scripts/run_work_package.py`, `golden_gate_local.py`, `update_cursor_status.py` | Full Automation Bus SOP |
| `knowledge_bus/` hypothesis or signal YAMLs consumed by Intelligence Core | Full Automation Bus SOP (MIXED or BEHAVIOUR) |
| `backend/app/routes/` (API endpoints, not analytical logic) | SOP Stage 0 branch check + PR review; no full gate required |
| `frontend/` (all) | Branch → implement → PR review → merge. No SOP ceremony. |
| `docs/`, `*.md`, config files, `.gitignore` | Direct commit or PR at discretion. No SOP. |
| Stripe integration, Supabase schema additions | Branch → implement → PR review → merge. No SOP ceremony. |

---

## What GPT Should Do With This Document

1. Author work package prompts for Sprints 1 and 2 first. Do not author Sprints 3–8 until Sprint 1 is in GATE_PASSED state.
2. Sprint 1 prompts must follow full SOP (Stage 0 branch alignment, Stage 1A–1D, BEHAVIOUR classification, HIGH risk, Intelligence Core declared).
3. Sprint 2 prompts: the backend tasks (SSE replacement if it touches route logic) use full SOP for the backend endpoint only. The frontend tasks (type generation, `as any` removal, `reports.ts` deletion) use the light PR model — no SOP ceremony required.
4. For Sprints 3–7, author implementation prompts as standard engineering tasks, not work packages. No Stage 0–5 overhead.
5. Do not add new analytical depth to any sprint except Sprint 8. If a sprint's implementation surfaces an engine issue, open a new sprint for it — do not scope-creep an existing sprint.
6. Sprint 8 should not be authored until at least Sprints 3–6 are complete.
