# FE-ACCOUNT Preflight — Profile, Settings, and My Account Management

**work_id:** FE-ACCOUNT-PREFLIGHT  
**mode:** READ_ONLY investigation  
**date:** 2026-04-08  
**evidence:** Repository paths cited below.

---

## 1. Executive summary

### What already exists

- **Authenticated shell and navigation:** `(app)` layout with sidebar **Account** group linking to **`/profile`** and **`/settings`** (`frontend/app/components/layout/AppSidebar.tsx`). **Middleware** protects those routes via auth cookie (`frontend/middleware.ts`).
- **Auth identity (end-to-end):** FastAPI **`/api/auth/login`**, **`/api/auth/register`**, **`/api/auth/me`**, **`/api/auth/logout`** (`backend/app/routes/auth.py`). Frontend **`AuthService`** + **`useAuthStore`** persist session (`access_token`, minimal `User` in `localStorage` + cookie) and refresh identity from **`GET /api/me`** (`frontend/app/services/auth.ts`, `frontend/app/state/authStore.ts`).
- **Header session UX:** Shows **`user.email`** (or id) and **Log out** (`frontend/app/components/layout/Header.tsx`).
- **Backend persistence “profile” (app database):** SQLAlchemy **`Profile`** and **`ProfilePII`** models with `user_id`, `email`, `demographics`, consent fields, and optional PII columns (`backend/core/models/database.py`). These rows are created via **`ensure_profile_for_auth_user`** for analysis FK integrity (`backend/core/profile_bridge.py`) — **not** exposed as a customer-facing read/update HTTP API in `backend/app/routes/`.

### What is still missing

- **Product pages:** **`/profile`** and **`/settings`** are **placeholders only** (title + one muted sentence) — `frontend/app/(app)/profile/page.tsx`, `frontend/app/(app)/settings/page.tsx`.
- **No dedicated “My Account” landing route** (e.g. `/account`); account entry is only via sidebar **Profile** / **Settings** labels.
- **No server-backed profile/settings update path for the SPA:** `AuthService.updateProfile` and **`changePassword`** are **explicit stubs** that always fail with “out of scope” / “not exposed” messages (`frontend/app/services/auth.ts` lines 218–235).
- **FE `User` / `MeResponse` contract** is intentionally minimal: **`id`** + **`email`** (+ raw `app_metadata` / `user_metadata` on wire but **not** mapped into product UI) (`frontend/app/types/auth.ts`, `identityToUser` in `auth.ts`).
- **Rich `UserPreferences` in `useUIStore`** (theme, language, notifications, accessibility) is **persisted locally** (`zustand` `persist`) but **not wired** to `/settings` and **not synced** to any backend account-preferences model (`frontend/app/state/uiStore.ts`).

### Is FE-ACCOUNT justified now?

**Yes.** The roadmap treats **account/profile/settings** as part of the **product and launch gate** (strategy doc §4.2) and lists **FE-ACCOUNT** under Wave 4 as the line item that **implements account/profile/settings capability** for **minimum account-management experience required for launch** (`docs/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.5_FINAL_ADOPTED.md` §705–708). Repo reality: **auth works**, but **account surfaces and editable/readable product profile are largely absent**, so the next implementation sprint can be authored **truthfully** as ** filling placeholders + contracts**, not assuming features already exist.

---

## 2. Strategy interpretation

### Sources

- `docs/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.5_FINAL_ADOPTED.md`:
  - **§193–194 (Product and launch gate):** “persistent account capability”, “report history, analysis continuity, and **account/profile surfaces**”.
  - **§280:** “authentication, persistence, **account management**, and customer-history surfaces are not yet complete enough to support a commercial launch”.
  - **§699–708 (Wave 4):** **FE-PAGES** (product pages / history) and **FE-ACCOUNT** separately:
    - **FE-ACCOUNT purpose:** “implement **account/profile/settings capability**” and “support the **minimum account-management experience required for launch**”.

### What FE-ACCOUNT is supposed to do (roadmap context)

In context, **“profile, settings, and My Account management”** means:

- **Product-visible** ways for a signed-in customer to see **who they are**, manage **basic account-related information and preferences**, and complete **routine account actions** (e.g. sign out, and **eventually** password/profile updates where the stack allows) — **without** collapsing into FE-PAGES (dashboard/history/detail) or replacing upload/results/clinician surfaces.

**Capability unlocked:** A **coherent account layer** so the app is not only “authenticated shell + analyses” but a **launch-credible** logged-in product with **named account surfaces** aligned to privacy/compliance expectations (consent, visibility of identity, path to settings).

### One wave vs multiple phases (roadmap)

The adopted roadmap states **FE-ACCOUNT** as **one named line item** under Wave 4 — it does **not** prescribe internal sub-phases inside the markdown table. **Repo reality** (large gap between GoTrue identity, ORM `Profile`, and zero public profile API) **strongly suggests** **governed sub-phases** for implementation even if the roadmap label stays singular (see §6).

---

## 3. Current account audit

### 3.1 Pages and routes

| Surface | Path | Status | Evidence |
|--------|------|--------|----------|
| Profile | `/profile` | **Placeholder** — heading + “Your profile information will appear here.” | `frontend/app/(app)/profile/page.tsx` |
| Settings | `/settings` | **Placeholder** — heading + “Your settings will appear here.” | `frontend/app/(app)/settings/page.tsx` |
| My Account (named) | — | **Missing** — no `/account` (or similar) route located | `frontend/app/(app)/` tree |
| Subscription / billing | — | **Not found** in audited app routes | — |
| Auth | `/login`, `/register` | **Substantive** | `(auth)/` pages |

**Navigation:**

- **Sidebar:** **Profile**, **Settings** under **Account** (`AppSidebar.tsx`).
- **Header:** identity snippet + **Log out**; **theme toggle** uses **`next-themes`** (`Header.tsx`) — **not** the same channel as `uiStore` preferences UI (settings page unused).

**classification summary**

- **Present (substantive):** auth pages, header logout, protected routes.
- **Present (stub only):** `/profile`, `/settings`.
- **Missing:** dedicated My Account hub, any profile/settings forms, billing, password-change UI wired to a real API.

### 3.2 Data and contracts

| Layer | What exists | Read | Update | Notes |
|--------|-------------|------|--------|------|
| **Auth identity (Supabase via FastAPI)** | `UserIdentity` / `MeResponse`: `user.id`, `user.email`, `app_metadata`, `user_metadata` | **Yes** — `GET /api/auth/me` | **No** product endpoint for profile patch on this router | `backend/app/routes/auth.py` |
| **Frontend session user** | `User`: `id`, `email`, optional `name`, `role`, timestamps in **type** only | **Yes** — from `/me` + localStorage | **N/A** — `updateProfile` stub | `frontend/app/types/user.ts`, `frontend/app/services/auth.ts` |
| **DB `profiles` row** | `email`, `demographics`, `consent_*`, etc. | **Indirect** — created for analysis saves; **no** audited customer **GET profile** route | **No** generic customer-facing PATCH located | `backend/core/models/database.py`, `profile_bridge.py` |
| **DB `profiles_pii`** | name, DOB, phone, address | **No** FE API found in `backend/app/routes/` | **No** | ORM only |
| **Analysis-scoped “user profile”** | `UserProfile` in analysis types + `analysisStore.setUserProfile` | Used for **analysis payload**, not account CRUD | Local store only | `frontend/app/state/analysisStore.ts` |
| **UI preferences** | `useUIStore` `UserPreferences` | **Yes** — local persisted state | **Yes** — locally only | `frontend/app/state/uiStore.ts` |

**Distinction (required):**

- **Auth/session identity:** GoTrue-backed **id + email** — **real** and **read** in the app.
- **Product “profile” page:** **not implemented**; ORM **Profile** is **persistence/supporting**, not yet a **declared REST contract** for the FE account sprint without new routes.
- **User preferences/settings:** **local-only** infrastructure exists in **`uiStore`**; **settings page does not surface it**.
- **Account-management actions:** **Logout** is real; **password change / profile update** explicitly **not** on current auth API surface.

---

## 4. Product-role audit — what FE-ACCOUNT should include next (repo-grounded)

**Reasonable next responsibilities** (without redesigning the whole app):

1. **Replace stubs** with a **truthful account summary** using existing **`/api/auth/me`** (and optionally display raw metadata only if product/legal warrants).
2. **Optional “My Account” hub** or **profile-as-hub**: links to **Dashboard**, **Reports**, **Upload** — **no** duplication of FE-PAGES history implementation.
3. **Settings page (bounded):** wire **existing** client preferences (`useUIStore`) and/or **next-themes** into one coherent **in-app settings** experience (still may remain **device-local** until a server model exists).
4. **Consent / account metadata (if required for launch):** only if product/legal demands — would need **thin, owner-scoped** **`GET/PATCH`** (or dedicated resource) against **`profiles`** — **currently missing**; size as a **separate governed decision** (not assumed in this preflight).
5. **Password / email change:** typically **Supabase-hosted flows** or **new backend endpoints** — **not** present; **document as follow-on** unless sprint explicitly includes Supabase dashboard links or API expansion.
6. **Out of scope for FE-ACCOUNT:** re-implement **FE-PAGES** dashboard/reports/analysis detail; **clinician** workspace; **commercial batch** interfaces; **billing**.

---

## 5. Dependency / blocker audit

| Item | Ready? | Blocker detail |
|------|--------|----------------|
| Read identity in FE | **Yes** | `/api/auth/me` |
| Protected `/profile`, `/settings` | **Yes** | `middleware.ts` |
| Customer profile **read** from app DB (`profiles`) | **Partial** | Data exists; **no** dedicated safe **JSON** route audited under `app/routes/` |
| Profile **update** | **No** | No contract; `AuthService.updateProfile` is stub |
| Password change | **No** | Stub; Supabase may offer flows outside current FastAPI contract |
| Server-side user preferences | **No** | Only `uiStore` local persistence |
| Strategy doc vs repo (auth) | **Note** | Baseline table §6.1 still says authentication “Disabled/unfinished”; **repo has** FE-FOUNDATION auth routes — **treat roadmap narrative as partially stale** for auth **completeness**; **account surfaces** remain incomplete per §280 |

**Honest assessment:** FE-ACCOUNT is **not** blocked from **starting** with **read-only account summary + settings UI bound to local preferences**. It **is** blocked from **truthful server-backed profile editing** until **thin backend** (or Supabase-only) contracts are added — unless the sprint scope is explicitly **identity-only**.

---

## 6. Boundary check (out of scope for FE-ACCOUNT)

Keep **out of scope** (unless a future sprint explicitly expands):

- **FE-PAGES** work already delivered: **dashboard, `/reports`, `/analysis/[id]` gateway, `/results`** — **link only**, do not rebuild.
- **Upload / results UX redesign**, retail explainer work, **clinician** workspace features, **enterprise/commercial** surfaces.
- **Broad auth/provider redesign** (replacing FastAPI `/api/auth` contract) — **out of scope** unless a dedicated governance sprint says otherwise.
- **Billing/subscription** — **not present** in audited routes; **out of scope** for initial FE-ACCOUNT unless product adds it explicitly.

---

## 7. Delivery-shape recommendation

### Final recommendation

**`SPLIT_INTO_PROFILE_AND_SETTINGS_PHASES`**

### Rationale

- **Roadmap** names a **single** FE-ACCOUNT item, but **repo reality** couples **three different depths**: (1) **GoTrue identity** (ready), (2) **app DB Profile** (exists, **no** customer API), (3) **rich local preferences** (`uiStore`, **no** settings page).
- A **single monolithic sprint** risks **mixing** “display `/me`” with **new backend contracts** and **password flows** without clean gates.
- **Split (governed):**
  - **Phase A — Account / profile shell (read-mostly):** Replace stubs; **My Account or Profile** shows **truthful** identity from **`/me`**; deep links to history/dashboard; **logout** already in header (may duplicate affordance on page).
  - **Phase B — Settings:** Surface **`useUIStore`** preferences + theme alignment; document **local-only** vs future server sync.
  - **Phase C (optional / later):** **Thin backend** (or Supabase) for **`profiles` consent/demographics** read/write and/or **password** handoff — **only** with explicit security review.

### If forced to one bounded sprint (alternative)

A **single** sprint is only coherent if scope is **explicitly** capped to: **stub replacement + `/me` display + settings UX for local `uiStore` + no new persistence**. Name that cap in the sprint prompt to avoid scope creep.

---

## 8. If proceeding — likely touched surfaces (indicative, not a sprint charter)

- `frontend/app/(app)/profile/page.tsx`, `frontend/app/(app)/settings/page.tsx`
- `frontend/app/components/layout/AppSidebar.tsx` / `Header.tsx` (IA labels, optional `/account`)
- `frontend/app/services/auth.ts` (only if expanding beyond stubs with real endpoints)
- `frontend/app/state/uiStore.ts` (consumers from settings UI)
- **Backend (only for Phase C):** new **`routes/profile.py`** or extend **`auth.py`** — **owner-scoped**, **bounded**; align with `Profile` / consent model

---

## 9. Mandatory recommendation enum (required one-liner)

**`SPLIT_INTO_PROFILE_AND_SETTINGS_PHASES`**

---

## 10. Evidence index (key files)

| Area | Path |
|------|------|
| Roadmap FE-ACCOUNT | `docs/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.5_FINAL_ADOPTED.md` §705–708, §193–194, §280 |
| Profile page (stub) | `frontend/app/(app)/profile/page.tsx` |
| Settings page (stub) | `frontend/app/(app)/settings/page.tsx` |
| Sidebar account links | `frontend/app/components/layout/AppSidebar.tsx` |
| Header session | `frontend/app/components/layout/Header.tsx` |
| Auth API | `backend/app/routes/auth.py` |
| Auth client | `frontend/app/services/auth.ts` |
| Auth store | `frontend/app/state/authStore.ts` |
| Me / identity types | `frontend/app/types/auth.ts` |
| ORM Profile | `backend/core/models/database.py` (`Profile`, `ProfilePII`) |
| Profile bridge (analysis) | `backend/core/profile_bridge.py` |
| Local preferences | `frontend/app/state/uiStore.ts` |
| Route protection | `frontend/middleware.ts` |
