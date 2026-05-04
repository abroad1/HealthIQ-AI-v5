# F-1 — Frontend re-entry: deterministic narrative surfacing

**Work ID:** F-1  
**SOP:** Automation Bus v1.3.1 (`TWO_PHASE_START_FINISH`, `HIGH`, `MIXED`)

## What was blocking the journey

`narrative_report_v1` was produced on `AnalysisDTO` but **omitted** from the HTTP client snapshot in `analysis.py` (`stored` dict), so `build_analysis_result_dto` never forwarded it to the frontend.

## What changed

| Area | Change |
|------|--------|
| `backend/app/routes/analysis.py` | Persist `narrative_report_v1` in the in-memory/DB client result shape (`model_dump()`). |
| `backend/core/dto/builders.py` | Pass `narrative_report_v1` through on `build_analysis_result_dto`. |
| Frontend types / normalizer / store | `NarrativeReportV1` + `narrative_report_v1` on `AnalysisResult`. |
| Results journey | **Retail summary** and **body overview** (compiler) near the top; **lead / secondary / other systems** after balanced systems; **longitudinal + next steps** after “why this lead won”; **clinician synthesis** at top of Advanced → Clinician report tab. |
| Legacy surfaces | `insights[]` / Narrative tab framed as optional legacy summaries; deterministic blocks are on the main path. |

## UAT focus

- Confirm `GET /api/analysis/result` includes `narrative_report_v1` for new completes.
- Verify section order: summary → body overview → stable systems → compiler “what this means” → structured primary finding → trends/next steps → patterns.
- Older DB snapshots without `narrative_report_v1` should still render (fallback body overview heuristics unchanged).

## Files touched (implementation)

- `backend/app/routes/analysis.py`
- `backend/core/dto/builders.py`
- `backend/tests/unit/test_balanced_systems_presentation_v1.py`
- `frontend/app/types/analysis.ts`
- `frontend/app/services/analysis.ts`
- `frontend/app/state/analysisStore.ts`
- `frontend/app/components/results/DeterministicNarrativeSurface.tsx` (new)
- `frontend/app/components/results/ResultsBodyOverview.tsx`
- `frontend/app/components/results/ClinicianReportRenderer.tsx`
- `frontend/app/(app)/results/page.tsx`
