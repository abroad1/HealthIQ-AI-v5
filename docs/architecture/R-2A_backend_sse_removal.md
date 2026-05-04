# R-2A — Backend integration (fake SSE removal)

**Work package:** R-2A (Sprint 2 backend path, Option A)  
**Branch:** `fix/integration-stability-backend`

## What was removed

- `GET /api/analysis/events` previously returned a **fake** `text/event-stream` body: a fixed sleep, then `started` and `completed` events with no connection to the real `AnalysisOrchestrator` run.
- That handler is replaced with **HTTP 410 Gone** and a JSON `detail` object (`error: sse_progress_not_available`) so clients cannot treat the stream as real progress.

## What the frontend should use (follow-on, light model)

1. **Start:** `POST /api/analysis/start` — the pipeline still runs **synchronously** in this handler; a successful response includes `analysis_id` and `status: "completed"` when the run finishes.
2. **Result payload:** `GET /api/analysis/result?analysis_id={uuid}` — truth source for the full client result (poll if needed, e.g. every ~2s, until 200 or a definite error).
3. **Do not** rely on `GET /api/analysis/events` for progress; it is intentionally **gone (410)** with an explicit error code.

## Assumptions

- No new async job queue was introduced; polling is compatible with the current synchronous `POST /start` plus `GET /result` contract.
