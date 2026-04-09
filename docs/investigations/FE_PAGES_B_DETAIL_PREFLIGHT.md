# FE-PAGES-B — Analysis Detail Preflight (Stage 1C)

**work_id:** FE-PAGES-B  
**date:** 2026-04-08  
**SOP:** Automation Bus v1.3.1 — Stage 1C mandatory verification before implementation.

---

## 1. Baseline verification

| Check | Status |
|--------|--------|
| FE-PAGES preflight doc exists at `docs/investigations/FE_PAGES_PREFLIGHT.md` | **Yes** |
| FE-PAGES-A reality: `/reports` canonical list; `/results` rich UX; `/analysis` → `/reports`; history + hardened `GET /analysis/result` | **Yes** (confirmed on current `main`) |
| `/analysis/[id]` was stub only (placeholder copy) | **Yes** — `frontend/app/(app)/analysis/[id]/page.tsx` |

---

## 2. Sprint boundaries (this sprint will **not**)

- Redesign the locked `/results` UX package
- Duplicate full results UI under `/analysis/[id]`
- FE-ACCOUNT, upload redesign, public/auth redesign
- Broad backend persistence redesign

**Confirmed:** Implementation stays a thin FE entry + optional minimal read-path only if missing (not required — `AnalysisService.getAnalysisResult` + auth already exist).

---

## 3. Route role decision (Stage 1C §4)

**Chosen role for `/analysis/[id]`:** **Canonical authenticated gateway** into the existing results experience.

- **Behaviour:** After auth (middleware-enforced for `/analysis/*`), the page performs a **truthful** `GET` of the saved result for the id (owner-safe API). On success, it **replaces** history to `/results?analysis_id=<id>` so all interpretation and retail chrome remain in the **single** governed `/results` surface.
- **Not chosen:** A second full “detail results” implementation; a third ambiguous role competing with `/results`.

This matches the strategic intent in `automation_bus/latest_cursor_prompt.md` (FE-PAGES-B).

---

## 4. Backend delta

**None required for truthful open** on environments with DB + auth: `GET /api/analysis/result` already enforces ownership and DB snapshot fallback per FE-PAGES-A.

---

## 5. Closure cross-reference

After implementation, confirm:

- Approach: gateway + `router.replace` to `/results?analysis_id=…`
- Dashboard + `/reports` links target `/analysis/[id]`
- Loading / not-found / forbidden / auth error UI on the gateway
