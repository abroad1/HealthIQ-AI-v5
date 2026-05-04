# FE-ACCOUNT-A — Stage 1C Account Shell Preflight (mandatory)

**work_id:** FE-ACCOUNT-A  
**date:** 2026-04-08  
**SOP:** Automation Bus v1.3.1

## 1. Baseline verification

| Check | Result |
|--------|--------|
| `docs/investigations/FE_ACCOUNT_PREFLIGHT.md` exists | **Yes** (committed on this branch) |
| `/profile` placeholder, `/settings` placeholder | **Yes** — `frontend/app/(app)/profile/page.tsx`, `settings/page.tsx` |
| Auth identity from `/api/auth/me` | **Yes** — `backend/app/routes/auth.py`, `AuthService.getCurrentUserFromServer` |
| DB-backed customer profile CRUD API | **Not exposed** — ORM `Profile` exists; no dedicated FE profile PATCH |
| `uiStore` preferences | **Out of scope** for FE-ACCOUNT-A (FE-ACCOUNT-B) |

## 2. Sprint boundaries

This sprint **will not**: implement settings UX, editable profile without contract, broad backend profile APIs, auth redesign, FE-PAGES/clinician/commercial drift.

## 3. Account-page role decision (§4)

**Decision:** **`/profile` is the single effective “My Account” / account shell.**  
**No `/account` route** is introduced. Sidebar label updated to **“My account”** pointing to `/profile` to reduce “Profile vs My Account” ambiguity without creating a second page.

## 4. Backend delta

**None required** — truthful identity is available from existing `GET /api/auth/me`. Frontend adds **`AuthService.fetchMe()`** to read full `MeResponse` (including Supabase metadata) for display without widening persisted `User` shape.
