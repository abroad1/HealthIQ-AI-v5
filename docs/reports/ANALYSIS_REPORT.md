# Sprint 16 Baseline Verification – Functional HealthIQ-AI Audit

Tag: Sprint 16 Baseline Verification – Functional HealthIQ-AI Audit

## Summary Table

- Pass (✅): 2
- Partial (⚠️): 1
- Fail (❌): 1

| Area | Path | Check | Result | Notes |
|------|------|-------|--------|-------|
| Backend | `backend/app/routes/health.py` → `/api/health` | FastAPI TestClient GET | ✅ | Returned 200 and JSON `{status:"ok"}` |
| Backend | `backend/app/routes/upload.py` → `/api/upload/parse` | POST JSON body `{text:"Glucose 5.2 mmol/L"}` | ❌ | 400 with `{detail}`; endpoint expects multipart or form for text. |
| Backend | `backend/app/routes/upload.py` → `/api/upload/parse` | POST form `text_content=...` | ✅ | 200 with keys `[success, message, parsed_data, analysis_id, timestamp]` |
| Backend | `backend/app/routes/analysis.py` → `/api/analysis/result` | GET without `analysis_id` | ⚠️ | 422 (missing query param). Route exists; needs `analysis_id` to return data. |
| Backend | `backend/app/routes/analysis.py` → `/api/analysis/fixture` | GET | ❌ | 404 currently; fixture file `tests/fixtures/sample_analysis.py` was deleted. |
| Frontend | `frontend/app/upload/page.tsx` | Build/import check | ⚠️ | No `build` script in package.json; TypeScript previously compiled. Manual flow likely OK but not verified with dev server. |

## Core Backend Functionality

### /api/health
- File: `backend/app/routes/health.py`
- Function: health root (router)
- Execution: ✅ 200 OK using TestClient
- Notes: Healthy

### /api/upload/parse (Gemini parser)
- File: `backend/app/routes/upload.py`
- Function: `parse_upload`
- Execution:
  - JSON body `{text:"..."}`: ❌ 400 (expects form/multipart)
  - Form field `text_content=...`: ✅ 200 with parsed structure
- Suggested fix: Optionally accept JSON `{text: str}` payload for convenience, or update client to send `text_content` form field.

### /api/analysis/result
- File: `backend/app/routes/analysis.py`
- Function: `get_analysis_result` (query param `analysis_id` required)
- Execution: ⚠️ Returns 422 when missing `analysis_id`; functional by design when provided.
- Suggested fix: None required; client must pass `analysis_id`.

### /api/analysis/fixture (excluded from scoring but referenced)
- File: `backend/app/routes/analysis.py`
- Function: `load_fixture_analysis`
- Execution: ❌ 404 because `backend/tests/fixtures/sample_analysis.py` is deleted
- Suggested fix: Restore fixture file or guard route when fixture missing.

## Frontend Functionality

### Upload → Results flow
- Files: `frontend/app/upload/page.tsx`, `frontend/app/results/page.tsx`
- Build: ⚠️ No `npm run build` script available; cannot perform production build check. Type-level compile previously passed in this session.
- Fixture Mode: Implemented via `fetchFixtureAnalysis()` with `NEXT_PUBLIC_API_BASE`.
- Manual Mode: Dual-path logic present; manual handlers (`handleFileUpload`, `handleConfirmAll`) remain intact.
- Suggested fix: Add/restore `build` script to `frontend/package.json` to validate production build.

### Questionnaire functionality
- Backend mapper and models present under `backend/core/pipeline/questionnaire_mapper.py` and `backend/core/models/questionnaire.py`.
- Import checks: ✅ Modules importable (by main app startup earlier).
- Suggested fix: None.

## Obsolete or Missing Tests
- Fixture dataset missing: `backend/tests/fixtures/sample_analysis.py` deleted → `/api/analysis/fixture` fails.
- Frontend build script missing → cannot validate production build.

## Suggested Priorities for Repair
1. Restore fixture dataset or remove the fixture route from navigation (low impact if focusing on production pipeline).
2. Add `"build": "next build"` to `frontend/package.json` to enable production build validation.
3. Optionally allow `/api/upload/parse` to accept JSON `{text}` payloads in addition to form field `text_content` for developer experience.

## Detailed Checks (Evidence)

- Health route:
  - Status: 200; JSON body `{status:"ok"}`.
- Upload parse:
  - JSON: 400 with `{detail}` (expected given current signature)
  - Form `text_content`: 200; keys present `[success, message, parsed_data, analysis_id, timestamp]`.
- Analysis result:
  - 422 without `analysis_id` (by design).
- Fixture:
  - 404; missing fixture file.
- Frontend build:
  - `npm run build` missing; unable to verify production artifacts.

---

Prepared by: Sprint 16 Baseline Verification – Functional HealthIQ-AI Audit
