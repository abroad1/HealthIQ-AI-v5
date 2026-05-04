# FE-LAUNCH-INTEGRATION-B — Stage 1C Launch Polish Preflight

**Date:** 2026-04-10  
**work_id:** FE-LAUNCH-INTEGRATION-B  
**Governing preflight:** `docs/investigations/FE_LAUNCH_INTEGRATION_PREFLIGHT.md`  
**Phase A reference:** FE-LAUNCH-INTEGRATION-A complete (shell, auth, canonical `/analysis/[id]` → results).

## 1. Repo reality verified

| Check | Status |
|--------|--------|
| Upload/results in authenticated shell | Yes (`frontend/app/(app)/upload`, `(app)/results`) |
| Canonical reopen route | `/analysis/[id]` → `/results?analysis_id=` |
| Remaining gaps are polish/consistency | Yes per preflight §6–7 (upload debt, copy, empty/error states) |

## 2. Launch-facing rough edges classified

| Issue | Class | In scope? |
|-------|-------|-----------|
| Four-tab upload UI with deprecated Manual/Questionnaire/Combined paths | Deprecated / misleading UI debt | **Yes** — remove from launch path |
| Heavy `console.log` / debug `useEffect` on upload | Deprecated / developer-facing debt | **Yes** — strip from production path |
| Dashboard/reports raw API error strings | Empty/error state weakness | **Yes** |
| Reports list full UUID monospace | Copy / small nav rough edge | **Yes** — align with dashboard short label |
| Dashboard “enter biomarkers” copy | Copy inconsistency | **Yes** — upload flow is parse-first |
| Landing HIPAA / compliance bullets | OPS-S1 | **No** — untouched |
| Results hero/trust/clinician/narrative order | Hierarchy | **No change** — out of scope |

## 3. Deferred (would widen scope)

- Full marketing rewrite of `page.tsx`
- Questionnaire copy overhaul inside `QuestionnaireForm`
- New global error boundary system

## 4. STOP check

Work is bounded to copy cleanup, upload tab removal, console stripping, and improved list/history errors — **no structural auth or route changes**.
