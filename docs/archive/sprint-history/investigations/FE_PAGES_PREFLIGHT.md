# FE-PAGES Preflight — Product Pages, Detail Surfaces, and Continuity

**work_id:** FE-PAGES-PREFLIGHT  
**mode:** READ_ONLY investigation (this document only)  
**date:** 2026-04-08  
**evidence:** Repository paths cited below.

---

## 1. Executive summary

### What already exists

- **Authenticated shell:** `(app)/layout.tsx` provides `Header`, `AppSidebar`, `Footer` for routes under the `(app)` group.
- **Route protection:** `frontend/middleware.ts` requires auth cookie for `/dashboard`, `/analysis`, `/analysis/*`, `/reports`, `/settings`, `/profile` (redirect to `/login?next=…`). **`/upload` and `/results` are not in `PROTECTED_PREFIXES` or the matcher** — they are **unprotected** at middleware level.
- **Rich results experience:** `frontend/app/results/page.tsx` implements the locked retail UX stack (hero, trust strip, system groups, biomarker dials, advanced/clinician panels, `?analysis_id=` hydration via `useAnalysisResult` + `useAnalysisStore`).
- **Analysis pipeline + persistence (backend):** `backend/app/routes/analysis.py` — `POST /analysis/start` runs synchronously, stores results in `_analysis_results`, and **when `DATABASE_URL` is set** calls `PersistenceService.save_live_analysis_after_run`. **`GET /analysis/result`** reads **only** `_analysis_results` (in-memory); **no DB fallback** on cache miss in the current handler (lines 241–254).

### What is still missing or weak

- **Product pages inside `(app)`:** `dashboard`, `reports`, `analysis` (list), `analysis/[id]`, `profile`, and `settings` are **placeholder copy only** (title + one muted paragraph each) — no lists, no data, no navigation into results.
- **Sidebar IA:** `AppSidebar.tsx` links to `/dashboard`, `/upload`, `/analysis`, `/reports` but **not** to `/results`; continuity from “saved item” → full results chrome is **not** implemented in navigation.
- **History/list surfaces:** `frontend/app/services/history.ts` is an explicit **mock** (empty history, TODO). `AnalysisService.getAnalysisHistory` targets **`GET /api/analysis/history`** — **no matching route** in `backend/app/routes/analysis.py` (only `start`, `result`, `events`, `fixture` per current file).
- **Session vs durable continuity:** `analysisStore` keeps `analysisHistory` in memory during the SPA session; **cold reload** or **new device** relies on **`GET /result`** which is **in-memory-only** — so **durable revisit** after persistence save is **not** end-to-end honest yet without backend read-path completion.
- **`/analysis/[id]`:** Route exists but is **stubbed**; it does **not** reuse results components or fetch by id.

### Whether FE-PAGES is justified now

**Yes** for **page-layer implementation** (dashboard, history/list, detail route, continuity). The roadmap explicitly places FE-PAGES in Wave 4 as the thread that “implement[s] the currently incomplete customer-facing product pages” and moves beyond upload/results-only (`docs/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.5_FINAL_ADOPTED.md`, §699–703).

**Caveat:** “Genuinely usable” **saved** analysis continuity (per strategy wording) **still depends** on **list + durable `result` read** contracts. Those are **partially missing** on the backend as of this audit; FE-PAGES should either **bundle a minimal BE read-path** as acceptance criteria or **phase** FE until those endpoints exist.

---

## 2. Strategy interpretation — what FE-PAGES is supposed to do

**Source:** adopted sprint plan Wave 4, **FE-PAGES** (§699–703).

| Roadmap phrase | Meaning |
|----------------|--------|
| “Currently incomplete customer-facing product pages” | Fill in **dashboard**, **reports/history**, **analysis detail** — not only polish `/results`. |
| “History, report retrieval, and detailed analysis genuinely usable” | Users can **find** past work and **open** a stable detail/summary path, not only the immediate post-upload flow. |
| “Move the app beyond upload/results into a persistent product” | **Navigation and mental model** of a logged-in product: home/history/detail/account-adjacent flows, aligned with persistence. |

**Capability unlocked:** A **coherent authenticated product** where upload → results is one path, and **return visits** and **browsing prior analyses** are first-class — not an orphan results URL.

**One wave vs multiple:** The roadmap lists FE-PAGES as **one Wave 4 line item** alongside FE-ACCOUNT (separate). It does **not** mandate micro-sprints; **phased delivery** is a **governance choice** based on **backend readiness** and **IA risk** (see §8).

---

## 3. Current page audit

### 3.1 Present (substantive)

| Route / area | Layout / notes |
|--------------|----------------|
| `/` | Marketing-style landing (`app/page.tsx`). |
| `/login`, `/register` | Auth routes; middleware redirects authed users to `/dashboard`. |
| `/upload` | Full upload/analysis orchestration UI; uses `AnalysisService.startAnalysis` (with auth headers on start). |
| `/results` | Full results / retail visualisation implementation; supports `?analysis_id=` + store sync. |

### 3.2 Present but placeholder only (in `(app)` group)

| Route | Evidence |
|-------|----------|
| `/dashboard` | `frontend/app/(app)/dashboard/page.tsx` — heading + “Your health overview will appear here.” |
| `/reports` | `frontend/app/(app)/reports/page.tsx` — “Your past reports will appear here.” |
| `/analysis` | `frontend/app/(app)/analysis/page.tsx` — “Your detailed analysis will appear here.” |
| `/analysis/[id]` | `frontend/app/(app)/analysis/[id]/page.tsx` — “Analysis {id}” + generic subtitle. |
| `/profile` | `frontend/app/(app)/profile/page.tsx` — stub. |
| `/settings` | `frontend/app/(app)/settings/page.tsx` — stub. |

### 3.3 Missing (as product-complete surfaces)

- **Functional dashboard** (recent analysis, CTAs, status).
- **Functional reports / history list** wired to a **real** history API (or agreed interim).
- **Functional analysis detail** that loads persisted analysis and presents or **routes to** the results experience.
- **Middleware + IA alignment:** optional hardening so **results** for authenticated users are only reachable when intended (policy choice; currently `/results` is public).

### 3.4 Route-role observations

- **`/results`** behaves as **canonical rich results chrome** for the implemented UX package; **locked docs** (`docs/architecture/Frontend/HealthIQ_Results_Page_UX_Design_Package.md`) describe **this** surface, not dashboard/history.
- **`/analysis/[id]`** is the **natural** stable URL for “saved analysis” per earlier planning, but today it is **not** wired.
- **Role split (recommended direction, not yet implemented):**  
  - **`/results`** — full interpretation view (same-session or `?analysis_id=`).  
  - **`/analysis/[id]`** — bookmarkable **entry** that ensures auth, fetches payload, then **renders or redirects** into the same results module to avoid duplicating layout logic.

---

## 4. Continuity / saved-result audit

### 4.1 Frontend behaviour

- **Post-upload:** Upload flow sets `currentAnalysisId`, prefetches via `useAnalysisResult`, navigates to results — **works in-session**.
- **Deep link:** `results/page.tsx` reads `analysis_id` from query, syncs `currentAnalysisId`, uses `useAnalysisResult(idToFetch)` — **works if API returns data**.
- **Empty state:** If no `currentAnalysis`, no in-flight analysis, and no `analysis_id` in URL, results page **redirects to `/upload`** (lines 143–147).
- **Store history:** `analysisStore` maintains `analysisHistory` and `getAnalysisById` from that list — **client-session** only unless repopulated from API.

### 4.2 Backend / contract

- **Persistence write:** Present on successful run when DB session available (`PersistenceService.save_live_analysis_after_run`).
- **Persistence read for `/result`:** **Not used** — handler uses `_analysis_results.get(analysis_id)` only.
- **History list API:** **Not implemented** on `analysis` router; frontend **mock** in `services/history.ts`.

### 4.3 Weak points

| Issue | Impact |
|-------|--------|
| In-memory-only `GET /result` | New session / server restart / cache eviction → **404** even if DB row exists. |
| No `GET /analysis/history` (in-repo route) | **Reports** and **Analysis list** pages cannot be truthful product surfaces without new contract or scope creep into backend. |
| `getAnalysisResult` without `Authorization` header | Matches current **unauthenticated** `get_analysis_result` — **ownership not enforced** on read path (product/compliance gap for launch). |
| Sidebar omits `/results` | Users in app shell must discover results via upload completion or manual URL. |

### 4.4 Likely canonical page roles (recommended)

1. **`/dashboard`** — entry after login; shortcuts to upload, **recent analyses** (when API exists).
2. **`/reports` or `/analysis`** — **list** of saved analyses (single responsibility; avoid duplicating two empty list pages long-term).
3. **`/analysis/[id]`** — **open saved analysis**; fetch result; navigate or embed results experience.
4. **`/results`** — **interpretation UX** (current implementation); keep as **primary rendering** for the design package.

---

## 5. Reports / saved-result surface audit

| Capability | FE | Backend (evidenced) |
|------------|----|---------------------|
| View saved result | **Partial** — `/results?analysis_id=` if API returns body | **Partial** — only if id still in memory dict |
| List history | **Missing** — mock returns `[]` | **Missing** — no `history` route on analysis router |
| Re-open stable URL | **Partial** — query param works; **`/analysis/[id]`** stub | Same read limitations |
| Export/share | **Present** on results (client JSON export, Web Share / clipboard) | `AnalysisService.exportAnalysis` posts to `/analysis/export` — **no route** in `analysis.py` |

---

## 6. Analysis detail page (`/analysis/[id]`)

- **Exists:** `frontend/app/(app)/analysis/[id]/page.tsx`
- **State:** **Stub only** — no `useAnalysisResult`, no redirect to `/results`, no shared layout with results package.
- **FE-PAGES should treat it as a primary target:** **Yes**, for **bookmarkable, authenticated** entry to a saved analysis — **provided** backend can **serve** the result for that id reliably.
- **Separation vs `/results`:** **Yes** — keep **one implementation** of the heavy results UI (`/results` module); use **`/analysis/[id]`** as **router/load gate** (fetch, error, auth) to avoid bifurcating the UX package.

---

## 7. Dependency / blocker audit

| Dependency | Severity | Notes |
|------------|----------|-------|
| **DB-backed `GET /analysis/result` (or cache miss → DB)** | **High** for durable continuity | Without this, “saved analysis” story is **fragile** across sessions. |
| **`GET /analysis/history` (or equivalent)** | **High** for real list UX | Frontend service already assumes this shape; router lacks it. |
| **Unify `history.ts` mock vs `AnalysisService.getAnalysisHistory`** | **Medium** | Split-brain noted in FE-PERSISTENCE preflight; still relevant until one path wins. |
| **Ownership on read** | **Medium–High** for launch | Start path uses auth; result path does not — FE-PAGES should not **assume** security is done. |
| **FE-ACCOUNT** | **Explicitly separate** | Profile/settings stubs exist; rich account work is **FE-ACCOUNT** per roadmap (§705–708). |

**UX ambiguity:** Two placeholders **`/reports`** and **`/analysis`** both claim “your stuff will appear here” without distinct roles — **IA cleanup** should be part of FE-PAGES scoping.

---

## 8. Delivery-shape recommendation

### Final recommendation label

**SPLIT_INTO_DASHBOARD_HISTORY_AND_DETAIL_PHASES**

### Rationale

1. **Phase A — Shell + list + continuity glue:** Implement **dashboard** with meaningful empty/loading states; implement **one** canonical **history list** (prefer **`/reports`** or **`/analysis`** — retire duplicate placeholder); wire to **`AnalysisService.getAnalysisHistory`** **after** (or in parallel with) **backend list endpoint**; align sidebar (e.g. Results / History).  
2. **Phase B — Analysis detail + results integration:** Implement **`/analysis/[id]`** as fetch + **redirect or shared render** with `/results`; ensure **DB-backed result read** is in acceptance criteria **somewhere** (minimal BE slice if not already done).

Trying to ship **dashboard + list + detail + auth-hard read path + IA cleanup** in one undisciplined sprint risks **hidden backend coupling**; splitting matches **actual** **half-ready persistence read** state.

**Alternative:** **PROCEED_AS_ONE_BOUNDED_PAGES_SPRINT** only if the charter **explicitly includes** a **named backend deliverable**: `history` list + `result` hydration from DB on miss, and **single sprint cap** on page count.

**Not chosen:** **DO_NOT_PROCEED_BLOCKED_BY_FOUNDATION_GAP** — incorrect **globally**: **FE work is actionable** on stubs and contracts; the gap is **partial**, not “no foundation.” Use **DO_NOT** only if org forbids any concurrent BE work.

---

## 9. Boundary check — out of scope for FE-PAGES

Per roadmap and prompt constraints, FE-PAGES sprints should **default exclude**:

- **FE-ACCOUNT** — full profile/settings/My Account (stubs may remain; depth is separate lineage §705–708).
- **Public marketing / auth page redesign** beyond **linking** into product shell.
- **Upload form redesign** as primary scope (touch only for **continuity links** if needed).
- **Retail explainer SSOT / B1 content** expansion.
- **Symptom relevance**, **clinician workspace**, **enterprise batch UI**.

**Backend:** FE-PAGES **should not** own “whole persistence redesign,” but **may need a thin, bounded** read API if product truth requires it — call that out in sprint charter.

---

## 10. Required chat outputs (summary)

| Item | Value |
|------|--------|
| **Artifact** | `docs/investigations/FE_PAGES_PREFLIGHT.md` |
| **Executive summary** | **Rich `/results`** + **auth shell** exist; **`(app)` pages are stubs**; **history/list APIs and DB `GET /result`** are incomplete for durable continuity; middleware leaves **`/results`/`/upload` public**. |
| **Final recommendation** | **SPLIT_INTO_DASHBOARD_HISTORY_AND_DETAIL_PHASES** (with parallel/thin BE read endpoints for list + result). |

---

*End of preflight — READ_ONLY; no repo mutations beyond this document.*
