# FE-LAUNCH-INTEGRATION Preflight — Product Coherence and Launch Readiness

**work_id:** FE-LAUNCH-INTEGRATION-PREFLIGHT  
**mode:** READ_ONLY investigation  
**date:** 2026-04-10  
**sources:** Adopted roadmap `docs/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.5_FINAL_ADOPTED.md`; frontend routes, middleware, stores, and services as cited; backend `backend/app/routes/analysis.py` and `backend/core/dependencies/analysis_auth.py` for auth semantics on analysis APIs.

---

## 1. Executive summary

### What launch integration capability already exists

- **Results (Layer C + B presentation):** `frontend/app/results/page.tsx` implements a coherent retail stack: hero interpretation (`InsightPanel`), trust/data-quality strip (`PipelineStatus`), system groups (`ClusterSummary`), biomarker evidence (`BiomarkerDials`), and **Advanced analysis** tabs for narrative (`InsightsPanel` + `narrativeRuntime` from `meta` via `extractNarrativeRuntimeMeta`) and clinician report (`ClinicianReportRenderer`). `useAnalysisResult` (`frontend/app/queries/analysisResult.ts`) is the single fetch path; the store is synced from TanStack Query.
- **Authenticated shell:** `(app)` layout (`frontend/app/(app)/layout.tsx`) provides `Header`, `AppSidebar`, and `Footer` for dashboard, reports, profile, and settings.
- **Dashboard and reports:** `frontend/app/(app)/dashboard/page.tsx` and `frontend/app/(app)/reports/page.tsx` list saved analyses via `useHistory` → `AnalysisService.getAnalysisHistory`, with links to `/results?analysis_id=…`.
- **Account surfaces:** Profile (`frontend/app/(app)/profile/page.tsx`) is a read-only identity shell (FE-ACCOUNT-A). Settings (`frontend/app/(app)/settings/page.tsx`) is local theme preference (FE-ACCOUNT-B), honestly labeled as not server-synced.
- **Auth plumbing:** `frontend/middleware.ts` protects `/dashboard`, `/reports`, `/profile`, `/settings`, `/analysis`, `/login` redirect when already authed; `frontend/app/state/authStore.ts` and `providers.tsx` initialize session; `Header` exposes sign-in / sign-out.
- **Narrative empty states:** `frontend/app/lib/narrativeRuntimePresentation.ts` and `InsightsPanel` align copy with backend policy reasons — product-honest when LLM narrative is off or empty.

### What is still missing or weak

- **Two product shells:** `/upload` and `/results` sit **outside** `(app)` and therefore **do not** use `AppSidebar` / the same chrome as dashboard and reports. Navigation and visual continuity between “analysis flow” and “logged-in product” are split.
- **Auth vs marketing funnel:** The landing page (`frontend/app/page.tsx`) drives visitors to `/upload` without requiring sign-in. **`POST /api/analysis/start` requires an authenticated submitter** (`require_analysis_submitter` in `backend/app/routes/analysis.py`). The upload UI does not gate on login. In any environment where the API enforces JWT, **signed-out upload cannot complete a run** unless something else supplies auth — a launch-critical journey mismatch.
- **Stable detail URL:** `/analysis/[id]` (`frontend/app/(app)/analysis/[id]/page.tsx`) remains a **stub** (“Detailed biomarker analysis will appear here”). Real deep linking uses `/results?analysis_id=…` (query-param pattern, not a resource route under the app shell). `/analysis` redirects to `/reports` (`frontend/app/(app)/analysis/page.tsx`).
- **Product copy inconsistency:** Marketing (`page.tsx`) emphasizes generic “AI” and compliance-style claims; results copy emphasizes deterministic structure, clinician report, and “interpretation first.” First-run and returning-user mental models are not unified end-to-end.
- **Upload surface debt:** `frontend/app/upload/page.tsx` still exposes deprecated tabs (alerts / combined flow), heavy console logging, and a **hardcoded fallback `user_id`** in the analysis payload — risky for coherence with authenticated identity.
- **Read path semantics (when DB is configured):** `_raw_result_payload_for_analysis_id` in `backend/app/routes/analysis.py` returns **401** if `auth_user is None` when a DB session exists. Middleware still allows unauthenticated access to `/results`. A bookmarked results URL without a session **will not** load persisted results in a DB-backed deployment, while the UI route remains reachable — another auth/product seam.

### Whether FE-LAUNCH-INTEGRATION is justified now

**Yes.** Enough FE-PAGES / FE-ACCOUNT / narrative presentation work exists in the tree that the remaining work is **integration and coherence**, not greenfield page building. The roadmap explicitly calls for a **dedicated scoping** pass before prompt authoring; this preflight confirms that **named gaps are real in repo** and are appropriate for a bounded FE-LAUNCH-INTEGRATION programme.

**OPS-S1** (launch readiness, privacy, compliance, CI/CD) remains **explicitly separate**: the adopted plan states OPS-S1 must not be authored until market, residency, operating model, and compliance inputs exist, and is **out of scope** for this preflight (`docs/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.5_FINAL_ADOPTED.md`, §764–770).

---

## 2. Strategy interpretation — what FE-LAUNCH-INTEGRATION is supposed to do

**Source:** Wave 6 — **FE-LAUNCH-INTEGRATION** (`docs/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.5_FINAL_ADOPTED.md`, §735–762).

| Roadmap intent | Meaning for this repo |
|----------------|------------------------|
| “Final product integration pass” | Wire **already-built** surfaces into **one** coherent authenticated experience and navigation model — not replace the engine or invent new reasoning. |
| “Ensure auth, persistence, dashboard/history/report pages, account surfaces, and narrative work as one coherent product” | Align **middleware**, **route groups**, **upload → persist → list → reopen** behaviour, and **results/narrative/clinician** so they match **Phase 1 product gate** language (§190–196). |
| “Resolve remaining product-shell integration issues before launch” | Close gaps like **shell split**, **sign-in funnel**, **canonical URLs**, and **truthful empty/error** when APIs require auth or DB. |

**Unlocks:** A user can understand **one** product: sign in → upload → see results → find the same run in history → reopen with correct auth — without contradictory routes, copy, or silent API failure.

**Relations (roadmap threads):**

| Thread | Relation to FE-LAUNCH-INTEGRATION |
|--------|-----------------------------------|
| **FE-PAGES** | Delivers dashboard/reports/detail **pages**; launch integration **ties them to upload/results** and navigation (including whether `/results` lives inside the app shell). |
| **FE-ACCOUNT** | Delivers profile/settings **shells**; integration ensures **account vs analysis** journeys and CTAs do not contradict each other. |
| **FE-S2** | Narrative **presentation**; much of it is already on `/results` — integration ensures narrative/clinician/hero **story** is consistent in nav and copy, not duplicated awkwardly elsewhere. |
| **Backend narrative enablement (BE-S1)** | Not reimplemented here; FE must **consume** `insights`, `meta.narrative_runtime`, and clinician report **as-is** without drift. |
| **Persistence / history** | Integration must match **owner-scoped history** (`GET /api/analysis/history`) and **authenticated result read** when DB is on — see `analysis.py` + `analysis_auth.py`. |

**What FE-LAUNCH-INTEGRATION is *not* (roadmap + boundaries):**

- Not the place to **build the whole product shell from scratch** (Wave 6 intro: that work should already be underway earlier — §738–743).
- Not **OPS-S1** (compliance, deployment, market-specific controls).
- Not a licence to move **reasoning into Layer C** (strategy §134–141, §334–336).
- Not **backend narrative logic changes** as a default scope item.

---

## 3. Current product-journey audit

Assessment labels: **Coherent** | **Partial** | **Missing / weak**

| Journey | Assessment | Evidence / notes |
|---------|--------------|------------------|
| Signed-out → auth → upload → results | **Partial / weak** | `/login`, `/register` exist; middleware protects app routes but **not** `/upload` or `/results`. Analysis **start** requires JWT (`analysis.py` `start_analysis`). Landing pushes `/upload` without login (`page.tsx`). |
| Results → narrative → clinician report → history | **Partial** | On `/results`, narrative and clinician sit in **Advanced analysis**; coherent on **one page**. Link-out to **Reports** is not in the results chrome; user relies on sidebar only when inside `(app)`. |
| Reports/history → saved analysis → results | **Coherent (FE)** | Dashboard and reports link to `/results?analysis_id=…` with `encodeURIComponent` (`dashboard/page.tsx`, `reports/page.tsx`). |
| Dashboard/home → upload / reports / profile / settings | **Coherent** | Sidebar (`AppSidebar.tsx`): Dashboard, Upload, Reports; Account: profile, settings. |
| Profile/settings vs results/history | **Partial** | Profile “Go to” includes Upload/Reports/Dashboard (`profile/page.tsx`). Settings is explicitly local-only — fine, but must be messaged consistently app-wide. |
| Empty-state / first-run | **Weak** | Landing and upload promise a smooth path; **auth requirement** for `start` is not reflected in landing CTA. Reports/dashboard empty states link to upload — **good**. |
| Returning user continuity | **Partial** | History lists work when API succeeds. **Bookmark `/results?analysis_id=`** without session risks **401** on fetch when DB requires auth — weak continuity. |

**Stub / duplicate / abrupt:**

- **`/analysis/[id]`** stub vs **`/results?analysis_id=`** real behaviour — **duplicate mental model**, one of them non-functional.
- **Upload** deprecated tabs and alerts — **product-disconnected** from the primary Upload & Parse path.

---

## 4. Cross-surface consistency audit

| Dimension | Finding |
|-----------|---------|
| **Naming** | “Reports” (sidebar) vs “Your results” (results H1) vs “Analysis history” (reports card) — related but not identical; acceptable if intentional, confusing if not. |
| **Navigation** | App routes use **sidebar + header**; upload/results use **standalone** pages — **inconsistent hierarchy**. |
| **Section hierarchy** | Results page follows locked retail structure (hero → trust → groups → biomarkers → advanced). Dashboard/reports are simpler — OK, but **no shared page header pattern** across shells. |
| **Empty / degraded** | Narrative empty states are **truthful** (`narrativeRuntimePresentation.ts`). API errors on history show a string line — **minimal**. |
| **Narrative vs deterministic** | Results copy repeatedly positions narrative as **complementary** to structured/clinician views — **aligned** with strategy. Landing “AI” copy is **not** aligned with that vocabulary. |
| **Account vs analysis** | Profile read-only disclaimer is clear. Upload payload still allows **hardcoded `user_id`** — **undermines** account-truth story. |

---

## 5. Data / contract continuity audit (frontend-focused)

| Topic | State |
|-------|--------|
| **Results payload** | `AnalysisService.getAnalysisResult` maps DTO fields including `clinician_report_v1` and `meta` (`frontend/app/services/analysis.ts` + `frontend/app/types/analysis.ts`). |
| **Narrative metadata** | `extractNarrativeRuntimeMeta` reads `meta.narrative_runtime` only — no invention. |
| **Clinician report** | Typed `ClinicianReportV1` and renderer — wired. |
| **Saved analysis retrieval** | `useHistory` + `getAnalysisHistory` with auth headers when token present (`analysis.ts` `analysisAuthHeaders`). |
| **Dashboard vs reports list** | Both use same hook pattern; **duplicate fetch** possible if user hits both in one session — acceptable; not a correctness bug. |
| **Routes** | Canonical “detail” for full UX is **`/results`** + query param, not `/analysis/[id]`. |
| **Brittle assumptions** | Hardcoded UUID in upload payload; reliance on query param for deep link; optional auth on GET result means **environment-dependent** behaviour when DB on/off. |

---

## 6. Launch-critical gap ranking (highest first)

1. **Auth-gated analysis start vs public marketing/upload funnel** — Risk of **failed runs** or confusing errors for signed-out users; contradicts “coherent product” and Phase 1 gate for authenticated experience.
2. **Dual shell (app layout vs bare upload/results)** — Breaks **one-product** feel; affects every journey and support/trust narrative.
3. **Persisted result viewing without session (bookmark `/results`)** — When DB + auth are enforced, **silent failure** or error handling must match product expectations.
4. **No real `/analysis/[id]` (stub) vs query-param results** — Hurts **bookmarking, sharing, and IA clarity**; shows incomplete integration from earlier FE-PAGES-era planning.
5. **Landing/marketing vs in-app deterministic copy** — Launch-quality **trust** risk if users feel baited by “instant AI” vs clinical structured positioning.
6. **Upload technical debt** — Deprecated tabs, console noise, hardcoded `user_id` — **maintenance and trust** risk at launch polish time.
7. **History error UX** — Single line error on dashboard/reports — acceptable for MVP, weak for “launch.”

---

## 7. Best-next-shape recommendation

### Recommendation: **SPLIT_INTO_COHERENCE_AND_POLISH_PHASES**

**Grounding:** Repo evidence shows **two classes** of work: (1) **structural** — route group / middleware / auth funnel / canonical detail entry / alignment with API auth rules; (2) **polish** — remove deprecated upload paths, align marketing copy, tighten empty/error states, reduce debug noise. They touch overlapping files but **different risk profiles**; splitting keeps governance auditable and matches roadmap §343–348 (split when rollback or audit scope warrants).

**Phase A — Coherence (journey + shell + auth alignment)**

- **Likely surfaces:** `frontend/middleware.ts`, `frontend/app/(app)/layout.tsx`, `frontend/app/upload/page.tsx`, `frontend/app/results/page.tsx`, `frontend/app/page.tsx`, `frontend/app/components/layout/AppSidebar.tsx`, `frontend/app/(app)/analysis/[id]/page.tsx` (implement redirect or shared layout strategy).
- **Named gaps:** Single shell or explicitly justified exception; sign-in before or as part of upload when API requires JWT; policy for `/results` + persisted IDs; replace or redirect stub detail route.

**Phase B — Launch polish**

- **Likely surfaces:** `frontend/app/upload/page.tsx` (remove deprecated tabs / dead paths), copy on `frontend/app/page.tsx`, consistent loading/error on `useHistory` consumers, minor `dashboard` / `reports` UX.

**Alternative (single sprint):** **PROCEED_AS_ONE_BOUNDED_LAUNCH_INTEGRATION_SPRINT** is defensible if programme governance prefers **one audit** and the team accepts a **larger single diff** — the work is still bounded to integration, not new engine features.

**Not recommended:** **DO_NOT_PROCEED_FRONTEND_LAUNCH_SCOPE_NOT_READY** — Prerequisites for *scoping* integration work are **present**; remaining issues are **specific and evidenced**, not unknown.

---

## 8. Boundary check — out of scope for FE-LAUNCH-INTEGRATION

Default **exclude** unless explicitly chartered:

| Area | Rationale |
|------|-----------|
| **OPS-S1** | Market/compliance/CI/CD/deployment controls; blocked on external inputs per roadmap. |
| **Backend narrative reasoning / BE-S1 core** | Translation and orchestration belong to backend sprints; FE consumes contracts. |
| **New analytical or reasoning logic** | Violates Layer B/C boundary. |
| **Full auth redesign / SSO / enterprise IdP** | Phase 1 scope is **minimum** viable account — integrate what exists. |
| **Full marketing site** | Landing tweaks for **honesty and CTA alignment** may appear; full site is not required. |
| **Clinician workspace / B2B workflow** | Out of Phase 1 shell scope unless roadmap explicitly adds. |
| **Enterprise/commercial workflow redesign** | Not integration of existing surfaces. |
| **Speculative launch-market requirements** | No invented compliance story — OPS-S1 when inputs exist. |

---

## 9. Required output mapping

| Section | Location |
|---------|----------|
| Executive summary | §1 |
| Strategy interpretation | §2 |
| Journey audit | §3 |
| Gap ranking | §6 |
| Recommendation | §7 |
| Boundaries | §8 |

---

**Document status:** Preflight complete — ready for **FE-LAUNCH-INTEGRATION** prompt authoring under Automation Bus governance (separate work package).
