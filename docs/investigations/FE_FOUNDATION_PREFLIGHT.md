# FE-FOUNDATION Preflight — Authentication and Product Access Foundation

**Mode:** Read-only investigation (this artifact only). No implementation, prompts, or sprint execution.  
**Date:** 2026-04-04  
**Work ID:** FE-FOUNDATION-PREFLIGHT  
**Basis:** `docs/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.5_FINAL_ADOPTED.md` (lines 607–618), live repo inspection across frontend, backend, config, and database surfaces.

---

## 1. Executive Summary

**Auth/product-access maturity: LOW — intentionally deferred, mostly stubbed**

The repo has structural foundations for authentication scattered across frontend and backend, but the entire auth path has been deliberately disabled pending a proper implementation sprint. The strategy document (line 615) names this explicitly: "resolution of the current 'auth is effectively disabled' state."

**Critical finding:** Both `@supabase/supabase-js` (v2.58.0) on the frontend and `supabase>=2.4.0` on the backend are already installed. The Supabase client is already configured on the frontend with full auth options (`autoRefreshToken`, `persistSession`, `detectSessionInUrl`). This means the auth provider decision is already made by the existing dependencies — **Supabase Auth is the natural and pre-chosen path.** No new libraries are required for the core implementation.

**Key gaps:**
- No backend auth endpoints exist (`/auth/login`, `/auth/register`, `/auth/me`)
- No JWT verification in any backend route
- Frontend auth service is fully stubbed with `API_BASE_URL = 'about:blank'`
- No `middleware.ts` exists — all routes are unprotected
- No login or register pages exist
- All analysis runs are anonymous and unscoped to any user

**First practical unlock:** A two-sprint SPLIT sequence delivers the minimum viable product auth shell: backend JWT verification + auth endpoints (FE-FOUNDATION-A) followed by frontend login/register pages + route gating (FE-FOUNDATION-B).

---

## 2. FE-FOUNDATION Definition

**Source:** `docs/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.5_FINAL_ADOPTED.md` lines 607–618

> FE-FOUNDATION — Authentication and product access foundation  
> Purpose: begin the product-shell thread no later than Wave 2.
>
> Minimum intent:
> - backend auth foundation and session model
> - frontend login / register entry points
> - route/session gating for authenticated product surfaces
> - explicit scoping of persistence and account boundaries
> - resolution of the current "auth is effectively disabled" state
>
> Strategic note: this thread runs in parallel with engine work and is not dependent on full engine completion.

**What this thread is building:**

A real authentication layer on top of the existing anonymous analysis pipeline. After FE-FOUNDATION:
- Users must sign in to access the product shell
- The `(app)` route group (dashboard, analysis, profile, reports, settings) is protected
- Login and register pages exist and function
- The backend can verify who is making a request
- The current disabled/stubbed state is resolved

**What FE-FOUNDATION does NOT include:**
- Saving analysis results per user (FE-PERSISTENCE, Wave 3)
- Dashboard or history UI that consumes persisted data (FE-PAGES, Wave 4)
- Account management surfaces (FE-ACCOUNT, Wave 4)
- Email verification, OAuth providers, or rate limiting (post-MVP hardening)

---

## 3. Current-State Audit

### 3.1 Backend Auth

| Component | Status | Evidence |
|-----------|--------|---------|
| Auth routes (`/auth/login`, `/auth/register`, `/auth/me`, `/auth/refresh`) | **ABSENT** | `backend/app/main.py:21–25` — 5 registered routers, none auth-related |
| JWT generation / verification | **ABSENT** | No `PyJWT`, `python-jose`, or equivalent in `backend/requirements.txt` |
| Password hashing | **ABSENT** | No `bcrypt`, `passlib`, or equivalent in `backend/requirements.txt` |
| `get_current_user` FastAPI dependency | **ABSENT** | Not present in any backend route file |
| Supabase Python SDK | **REAL** | `supabase>=2.4.0` in `backend/requirements.txt` — includes `supabase.auth` |
| Security config (`SECRET_KEY`, `algorithm`, token expiry) | **PLACEHOLDER** | `backend/config/settings.py:100–116` — structure present, `SECRET_KEY` validated as required (line 211) but defaults to empty string |
| CORS middleware | **REAL** | `backend/app/main.py:8–14` |

**Summary:** Backend has the Supabase SDK and a security config scaffold, but no working auth code of any kind.

### 3.2 Session Handling

| Component | Status | Evidence |
|-----------|--------|---------|
| Session table / model | **ABSENT** | No session or auth_tokens table in any migration |
| Refresh token storage | **ABSENT** | SecurityConfig defines `refresh_token_expire_days` but no storage mechanism |
| Supabase manages sessions natively | **AVAILABLE** | Supabase Auth handles session persistence and refresh token rotation in managed infrastructure — no custom session table required for FE-FOUNDATION |

**Summary:** For the Supabase Auth path, session management is handled by Supabase infrastructure. No custom session table is needed for FE-FOUNDATION.

### 3.3 User / Account Model

| Component | Status | Evidence |
|-----------|--------|---------|
| `Profile` (SQLAlchemy) | **REAL** | `backend/core/models/database.py:23–60` — user_id, email, demographics, GDPR consent |
| `ProfilePII` | **REAL** | Encrypted PII fields (name, DOB, phone, address) |
| Auth credentials (password_hash, OAuth tokens) | **ABSENT** | Not in any database model |
| Supabase `auth.users` table | **AVAILABLE** | Supabase manages its own `auth.users` table — this is the canonical user record for the Supabase Auth path |
| Frontend `User` type | **PLACEHOLDER** | `frontend/app/types/user.ts` — basic interface, not wired to real auth |

**Summary:** The backend has a Profile model for storing user attributes, but credentials live in Supabase's managed `auth.users`. The two are linked by `user_id` (UUID).

### 3.4 Frontend Login / Register

| Component | Status | Evidence |
|-----------|--------|---------|
| Login page | **ABSENT** | No `(auth)/login/page.tsx` or equivalent |
| Register page | **ABSENT** | No `(auth)/register/page.tsx` or equivalent |
| Auth forms (React Hook Form + Zod) | **REAL (unused for auth)** | `react-hook-form` v7.61.1 and `zod` v3.25.76 are installed — no auth forms yet |
| Auth service methods | **STUBBED** | `frontend/app/services/auth.ts:11` — `API_BASE_URL = 'about:blank'`; all API calls are disabled but method signatures are complete |
| Supabase auth client | **REAL (not used for auth yet)** | `frontend/app/lib/supabase.ts:19–25` — client created with `autoRefreshToken: true, persistSession: true, detectSessionInUrl: true` |

### 3.5 Route Gating

| Component | Status | Evidence |
|-----------|--------|---------|
| `middleware.ts` | **ABSENT** | Not present at `frontend/middleware.ts` or `frontend/app/middleware.ts` |
| `(app)` layout auth check | **ABSENT** | `frontend/app/(app)/layout.tsx:1–23` — layout renders sidebar/header unconditionally, no session check |
| Protected route component | **ABSENT** | No `ProtectedRoute` or equivalent component |
| All routes effectively public | **CONFIRMED** | Entire app is accessible without authentication |

### 3.6 Current Anonymous Flow

```
/ (landing)
├─ /upload       → PDF or text input → POST /api/upload or /api/analysis → SSE stream
├─ /results      → Displays transient analysis results
└─ /demo         → Demo page (public)

/(app) — app shell layout with sidebar/header/footer
├─ /dashboard    → STUB (empty, no data)
├─ /analysis     → STUB (empty)
├─ /analysis/[id]→ STUB (empty)
├─ /profile      → STUB (empty)
├─ /reports      → STUB (empty)
└─ /settings     → STUB (empty)
```

All routes are public. The `(app)` group exists as a cosmetic layout grouping only.

---

## 4. Persistence Boundary

### What belongs in FE-FOUNDATION

| Item | Reason |
|------|--------|
| Backend JWT verification (Supabase JWT tokens) | Required to know who is calling the API |
| FastAPI `get_current_user` dependency | Required to protect any route |
| Backend auth endpoints calling Supabase Auth SDK | Required for server-side session operations |
| Frontend Supabase Auth integration (signIn, signUp, getSession, onAuthStateChange) | Required to obtain and hold a session |
| Login and register pages | Required entry points |
| `middleware.ts` route guard | Required to protect the `(app)` group |
| Auth Zustand store | Required to hold user/session state in frontend |
| Remove `about:blank` from auth service | Required to re-enable auth API calls |

### What belongs in FE-PERSISTENCE (Wave 3 — not this sprint)

| Item | Reason |
|------|--------|
| Scoping analysis runs to `user_id` | Requires integration between auth session and analysis pipeline — higher risk, Wave 3 |
| Saving analysis results per user | FE-PERSISTENCE sprint explicitly owns this |
| Analysis history retrieval | Depends on persisted analyses — Wave 3 |
| `supabaseHelpers` implementation (`saveAnalysisResult`, `getAnalysisHistory`) | Explicitly marked TODO Sprint 9b (FE-PERSISTENCE) in `frontend/app/lib/supabase.ts:129–152` |
| Row-level security policy review for analysis/results tables | Should happen alongside persistence wiring |

**Key decision:** FE-FOUNDATION gates the product shell behind authentication but does **not** wire `user_id` into the analysis pipeline. The upload/analysis/results flow may continue to work anonymously during FE-FOUNDATION, or it may be moved behind auth gating as a product decision — but it must not attempt to store results per-user in this sprint.

---

## 5. Likely Implementation Surfaces

### 5.1 Backend (FE-FOUNDATION-A)

| Surface | File | Action |
|---------|------|--------|
| Anon-key Supabase client (auth only) | `backend/core/supabase_anon.py` | **GPT-authorised** — bounded auth support; uses `SUPABASE_ANON_KEY` only; separates auth from service-role storage client (`backend/services/storage/supabase_client.py`) |
| New auth router | `backend/app/routes/auth.py` | Create — Supabase Auth proxy endpoints |
| Register endpoint | `POST /api/auth/register` | New — calls `supabase.auth.sign_up()` |
| Login endpoint | `POST /api/auth/login` | New — calls `supabase.auth.sign_in_with_password()` |
| Me endpoint | `GET /api/auth/me` | New — returns current user from verified JWT |
| Logout endpoint | `POST /api/auth/logout` | New — calls `supabase.auth.sign_out()` |
| JWT verification dependency | `backend/core/dependencies/auth.py` | Create — `get_current_user(token: str = Depends(oauth2_scheme))` using Supabase JWT secret |
| Router registration | `backend/app/main.py` | Modify — add auth router `include_router` |
| Security config | `backend/config/settings.py` | Modify — confirm `SECRET_KEY` / `SUPABASE_JWT_SECRET` usage |
| **No new packages required** | — | Supabase Python SDK already installed; `python-jose` may be needed for JWT decode if not using Supabase SDK directly |

### 5.2 Frontend (FE-FOUNDATION-B)

| Surface | File | Action |
|---------|------|--------|
| Route middleware | `frontend/middleware.ts` | Create — redirects unauthenticated requests to `/login` |
| Auth route group | `frontend/app/(auth)/layout.tsx` | Create — minimal layout for login/register pages |
| Login page | `frontend/app/(auth)/login/page.tsx` | Create — email/password form via Supabase Auth |
| Register page | `frontend/app/(auth)/register/page.tsx` | Create — email/password registration form |
| Auth Zustand store | `frontend/app/state/authStore.ts` | Create — user, session, loading, login/logout actions |
| Auth provider/initialiser | `frontend/app/providers.tsx` | Modify — add session initialisation on app mount |
| Auth service re-enable | `frontend/app/services/auth.ts` | Modify — replace `'about:blank'` with real API base; wire to Supabase Auth SDK |
| App layout session indicator | `frontend/app/(app)/layout.tsx` | Modify (optional) — add user display or logout button to Header |

### 5.3 Database

| Surface | Status |
|---------|--------|
| `auth.users` (Supabase managed) | **No migration needed** — Supabase creates this automatically |
| `Profile` table (existing) | **Already exists** — created by `873438dcca41_initial_persistence_schema.py` |
| Profile creation on first login | **New logic** — trigger or API call to create a Profile row for new Supabase Auth users |

No new Alembic migration is needed for FE-FOUNDATION if Supabase Auth manages user records natively. A Profile row is created on first sign-in (not a schema change — application logic only).

---

## 6. Recommendation

### Auth provider decision: Supabase Auth

This decision is already made by the existing repo. Both `@supabase/supabase-js` (frontend) and `supabase>=2.4.0` (backend) are installed. The Supabase client in `frontend/app/lib/supabase.ts` is configured with auth options. No alternative provider (NextAuth, Clerk, Auth0, Firebase) is installed or referenced anywhere. The comment in `supabase.ts` explicitly defers Supabase integration to "Sprint 9b" (now FE-FOUNDATION).

**Use Supabase Auth. Do not re-open this decision.**

### Sprint shape: SPLIT

**Recommended sequence:**

#### FE-FOUNDATION-A — Backend auth foundation
**Risk level:** STANDARD  
**change_type:** CONTENT (new endpoints and dependencies; does not modify Intelligence Core or analysis pipeline behaviour)

Deliverables:
- `backend/core/supabase_anon.py` — **GPT-authorised** anon-key Supabase client for auth (not service role); audit basis recorded in `automation_bus/latest_cursor_prompt.md` (Implementation constraints → GPT re-authorisation)
- `backend/app/routes/auth.py` — auth endpoints proxying Supabase Auth SDK
- `backend/core/dependencies/auth.py` — `get_current_user` FastAPI dependency using Supabase JWT verification
- Register auth router in `backend/app/main.py`
- Verify `SUPABASE_JWT_SECRET` (or equivalent) is in env config and used for token verification
- Confirm existing analysis routes remain functional (no auth requirement added in this sprint)

Does NOT include:
- Protecting analysis routes with `get_current_user` (FE-FOUNDATION-B confirms frontend can reach backend first; analysis auth gating can be a sub-item of FE-PERSISTENCE or a third sprint)
- Database schema changes

#### FE-FOUNDATION-B — Frontend auth + route gating
**Risk level:** STANDARD  
**change_type:** CONTENT (new frontend pages and middleware; no backend Intelligence Core interaction)

Deliverables:
- `frontend/middleware.ts` — route guard redirecting unauthenticated users from `(app)` to `/login`
- `frontend/app/(auth)/login/page.tsx` — login form
- `frontend/app/(auth)/register/page.tsx` — register form
- `frontend/app/state/authStore.ts` — Zustand auth store (user, session, login/logout)
- Update `frontend/app/providers.tsx` — initialise auth session on mount
- Update `frontend/app/services/auth.ts` — replace `about:blank` with real API base, wire to Supabase Auth SDK

**Why SPLIT, not COMBINED:**

1. **Testability:** Backend auth can be verified independently (Postman/curl) before frontend is wired. Combined sprint cannot confirm backend correctness until both halves are complete.
2. **Risk separation:** Backend changes touch `main.py` (a governed boundary file) and introduce a new dependency pattern (`get_current_user`) that will propagate to future routes. Isolating this allows clean audit.
3. **Failure isolation:** If FE-FOUNDATION-A reveals an unexpected Supabase configuration issue (JWT secret, RLS policy conflict, project setup), it does not stall frontend page work.
4. **Sequential dependency is clean:** FE-FOUNDATION-B meaningfully depends on FE-FOUNDATION-A completing — the login form must call a real backend endpoint. This natural sequencing maps cleanly to a two-sprint chain.

---

## 7. Structural Integrity Check

| Dependency | Required for FE-FOUNDATION? | Assessment |
|------------|----------------------------|------------|
| FE-PERSISTENCE | No | FE-FOUNDATION explicitly excludes result persistence; analysis flow stays anonymous |
| FE-PAGES | No | Dashboard/history stubs remain stubs; FE-FOUNDATION only gates them behind login |
| FE-ACCOUNT | No | Profile/settings stubs remain stubs |
| Major backend redesign | No | Supabase Auth path requires only new endpoints + dependency injection, not restructuring existing routes |
| Auth provider decision | Resolved | Supabase Auth — both SDKs installed, client configured |
| New Python packages | Potentially one | `python-jose[cryptography]` for JWT decode if the supabase Python SDK does not expose a verify-token helper directly; otherwise no new packages needed |
| New frontend packages | No | `@supabase/supabase-js` already installed with full auth capability |

**No blocking dependencies identified.** FE-FOUNDATION-A and FE-FOUNDATION-B can proceed in order without any prerequisite sprint.

**One open decision for prompt author to resolve before authoring:**

> How does the backend verify a Supabase-issued JWT?  
> Option A: Use `python-jose` to decode the JWT with the Supabase JWT secret (available from Supabase project settings as `JWT_SECRET`).  
> Option B: Call the Supabase Admin API (`supabase.auth.get_user(token)`) to validate the token server-side.  
> Option A is faster and stateless (no round-trip). Option B is simpler to code but adds a network call per request.  
> This decision belongs in the sprint prompt, not this preflight. Either path is viable.

---

## 8. Source Pointers (Verification)

| Artifact | Role |
|----------|------|
| `docs/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.5_FINAL_ADOPTED.md:607–618` | FE-FOUNDATION definition |
| `backend/app/main.py:21–25` | Registered backend routes (no auth) |
| `backend/config/settings.py:100–116` | Security config scaffold |
| `backend/requirements.txt` | `supabase>=2.4.0` — only auth-relevant package |
| `backend/core/models/database.py:23–60` | Profile / PII models |
| `backend/migrations/versions/` | 8 migrations, none for auth credentials |
| `frontend/app/services/auth.ts:11` | `API_BASE_URL = 'about:blank'` — auth disabled |
| `frontend/app/lib/supabase.ts:19–25` | Supabase client with auth configured |
| `frontend/app/(app)/layout.tsx:1–23` | App shell — no session check |
| `frontend/package.json` | `@supabase/supabase-js` v2.58.0 only auth SDK |
| `frontend/app/types/user.ts` | User type interface (placeholder) |

---

**Artifact path:** `docs/investigations/FE_FOUNDATION_PREFLIGHT.md`
