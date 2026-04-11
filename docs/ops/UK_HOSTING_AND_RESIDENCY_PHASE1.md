# UK hosting and residency — Phase 1 evidence position

**Status:** Internal launch-governance document  
**Audience:** Engineering, operations, privacy  
**Related:** `docs/HealthIQ_Phase1_Launch_Posture.md` (UK-hosted by default — strategic decision)

---

## 1. Purpose

Record a **reviewable, honest** position on where HealthIQ Phase 1 data is hosted and processed, distinguishing:

- what the **repository** can prove (configuration patterns, env-driven wiring),
- what the **agreed launch posture** states as direction,
- what **production operations** must still verify and document outside this repo.

This document does **not** certify UK-only processing. It explains how residency is determined and what remains to be evidenced for launch.

---

## 2. Strategic posture (non-technical)

Per `docs/HealthIQ_Phase1_Launch_Posture.md`, Phase 1 targets **UK-first** launch with **UK data residency by default** as the **direction of travel**. That is a **business and compliance intent**, not an automatic property of the codebase.

---

## 3. What the repository demonstrates

| Finding | Evidence | Implication |
|--------|----------|-------------|
| No UK region is enforced in application code | Database URL and Supabase settings are read from environment variables (`backend/config/settings.py`: `DatabaseConfig.from_env`, `SupabaseConfig.from_env`). | **Hosting region is entirely determined by** the chosen Supabase project, database provider region, object storage region, and deployment environment — **not** by a hard-coded UK flag in-repo. |
| Same for AI vendor | Gemini configuration uses `GEMINI_API_KEY` and related env (`GeminiConfig` in `backend/config/settings.py`). | **Inference region and data routing** follow **Google’s** service terms and the account/project configuration — must be confirmed for production. |
| Frontend | Next.js app uses `NEXT_PUBLIC_SUPABASE_URL` / `NEXT_PUBLIC_SUPABASE_ANON_KEY` (`frontend/app/lib/supabase.ts`). | **Client-side** talks to whatever Supabase URL is configured; **no** residency logic in frontend code. |

**Conclusion:** The repo shows **vendor-mediated, env-driven** hosting. **UK residency for production** requires **explicit** alignment of:

- Supabase project region(s) (auth, DB, storage),
- optional separate DB if used,
- deployment region for the FastAPI backend and Next.js hosting,
- Google Cloud / Gemini data processing settings relevant to health-adjacent prompts,

…documented in runbooks and vendor consoles, **not** inferable from code alone.

---

## 4. Classification table (launch honesty)

| Item | Status for Phase 1 artefact |
|------|-----------------------------|
| “We intend UK-first / UK residency by default” | **Posture / strategy** — documented in launch posture doc. |
| “Production is provably UK-only today” | **Not claimed here.** Requires ops-verified Supabase + hosting + AI routing evidence. |
| “Repo enforces UK boundaries” | **False** — not a repo capability; must not be claimed. |

---

## 5. Minimum operational follow-up (outside repo)

Before asserting UK residency in **external** marketing or regulatory contexts beyond this internal pack, operations should complete at least:

1. Document **actual** primary region(s) for: Supabase project, Postgres (if not fully via Supabase), file export bucket, application hosting, Gemini API usage.
2. Record any **non-UK** subprocessors or regions and the **lawful mechanism** (e.g. IDTA, SCCs, UK Addendum) if applicable — typically with legal/privacy ownership.
3. Reconcile with user-facing Privacy notice (`frontend` OPS-S1A surfaces) so public copy does not overstate what is technically true.

---

## 6. Revision

Update this document when production regions are fixed or when major vendors change.
