# FE-LAUNCH-INTEGRATION-A — Stage 1C Launch Coherence Record

**Date:** 2026-04-10  
**work_id:** FE-LAUNCH-INTEGRATION-A  
**Governing preflight:** `docs/investigations/FE_LAUNCH_INTEGRATION_PREFLIGHT.md`

## 1. Repo reality verified (pre-implementation)

| Item | Status |
|------|--------|
| `(app)` routes use Header + AppSidebar + Footer | Confirmed (`frontend/app/(app)/layout.tsx`) |
| `/upload` and `/results` were outside `(app)` | Confirmed before change |
| `POST /api/analysis/start` requires authenticated submitter | Confirmed (`backend/app/routes/analysis.py` `require_analysis_submitter`) |
| `/analysis/[id]` was a stub | Confirmed |
| `/results?analysis_id=` was the effective reopen path | Confirmed |
| `GET /api/analysis/result` with DB requires auth when `auth_user` absent | Confirmed (`_raw_result_payload_for_analysis_id`) |

## 2. Runtime auth paths verified

| Operation | Requirement |
|-----------|----------------|
| Start analysis | JWT (Bearer + cookie) via `require_analysis_submitter` |
| View persisted result (DB on) | JWT; owner-scoped row check |
| History list | JWT (`GET /api/analysis/history`) |

## 3. User paths verified

| Path | Behaviour (before change) |
|------|-----------------------------|
| Landing → upload | Direct `/upload` without sign-in — **rejected by API** on start |
| Dashboard/reports → result | `/results?analysis_id=` with auth cookie |

## 4. Shell split verified

Authenticated routes used `(app)` layout; `/upload` and `/results` used root layout only (no sidebar).

## 5. Decisions taken (implementation)

### Shell strategy

- **Move** `upload` and `results` **into** the `(app)` route group so URLs stay `/upload` and `/results` but they render inside the same Header / AppSidebar / Footer shell as dashboard and reports.

### Auth / journey model

- **Middleware:** Add `/upload` and `/results` to protected prefixes so unauthenticated users are redirected to `/login?next=…`.
- **Landing CTAs:** Primary actions go to **`/login?next=/upload`** or **`/register?next=/upload`**, not directly to `/upload`.
- **Upload payload:** `user.user_id` is taken from the signed-in session (`useAuthStore`) or questionnaire override — **no hardcoded UUID**.

### Canonical saved-analysis model

- **Bookmarkable entry:** `/analysis/[id]` **redirects** (HTTP redirect via Next.js `redirect()`) to **`/results?analysis_id=[id]`**.
- **Full interpretation UI** remains on **`/results`** (deterministic hierarchy unchanged).
- **Dashboard and reports** link to **`/analysis/{id}`** for cleaner URLs; users land on results after one redirect.

### Persisted-result continuity

- **Results fetch errors:** When TanStack Query cannot load a result for a known `analysis_id`, show a dedicated card explaining account-scoped access with **Sign in to retry** (preserves `next`) and **New analysis**, instead of a generic empty state.

## 6. Sprint non-goals confirmed

No FE-LAUNCH-INTEGRATION-B polish sweep, no OPS-S1 compliance copy changes, no backend reasoning changes, no deprecated-tab removal on upload (explicitly Phase B / out of scope in hardening).
