# D-5 — Wave 1 runtime verification and stale-path diagnosis

**Work ID:** D-5  
**Branch:** `feature/wave1-runtime-diagnosis`  
**SOP:** 1.3.1 (kernel start / finish)  
**Date:** 2026-04-26  

This document is **diagnosis only** (no product fix in D-5). It answers why a specific live UAT recheck can still look “pre–D-4” even when the repo on disk contains D-4.

---

## Target (from prompt)

| Item | Value |
|------|--------|
| UAT analysis URL | `http://localhost:3000/results?analysis_id=c1c061ab-4691-4a47-80b8-2938ae1460e4` |
| Login (local) | `test-user3@example.com` (credentials per bus prompt) |

**Note:** This investigation did not call your local API or browser from CI; findings below are from **code-path tracing** and define how to verify on your machine.

---

## 1) Backend: where the result comes from

`GET /api/analysis/result?analysis_id=…` does **not** recompute domain cards.

Flow:

1. `get_analysis_result` → `_raw_result_payload_for_analysis_id` (`backend/app/routes/analysis.py`).
2. With DB: loads `AnalysisResult` for the owner, then reads  
   `processing_metadata["client_result_shape_v1"]` as the **entire** stored client snapshot.
3. `build_analysis_result_dto` passes `consumer_domain_scores` through **as stored** (no assembly on read).

Code references:

- Snapshot read: `backend/app/routes/analysis.py` — see `_raw_result_payload_for_analysis_id` (in-process cache else DB `processing_metadata[CLIENT_RESULT_SHAPE_V1]`).
- DTO pass-through: `backend/core/dto/builders.py` — `"consumer_domain_scores": result.get("consumer_domain_scores")`.
- Write path: `backend/services/storage/persistence_service.py` — `save_live_analysis_after_run` stores `client_result` under `CLIENT_RESULT_SHAPE_V1` in `processing_metadata` at **analysis completion** (`save_analysis` + `upsert_by_analysis_id`).

**Conclusion:** `consumer_domain_scores` (including `headline_sentence`, `confidence_sentence`, `caveat_flags`, `evidence_anchor_sentence`) is **computed during the analysis pipeline** and **persisted**. It is **not** rebuilt on each GET.

So for any fixed `analysis_id` (including `c1c061ab-4691-4a47-80b8-2938ae1460e4`):

- If the run **completed before** D-4 was deployed, the DB snapshot will still contain **pre–D-4** strings and may omit D-4 keys (e.g. no `evidence_anchor_sentence`), **even if the server code is now D-4**.

That single fact explains “looks like pre-D-4” without any frontend or logic bug.

---

## 2) How to verify payload for the target `analysis_id` (local)

1. Log in and obtain a **Bearer** token (same session the app uses).
2. `GET` e.g.  
   `{API_BASE}/api/analysis/result?analysis_id=c1c061ab-4691-4a47-80b8-2938ae1460e4`  
   with `Authorization: Bearer <token>`.
3. Inspect JSON:
   - `consumer_domain_scores` (array, three Wave 1 rows).
   - For each of `wave1_cardiovascular`, `wave1_blood_sugar`, `wave1_liver`, check:
     - `headline_sentence` (still say “broadly stable” if pre-D-4 and band stable?)
     - `caveat_flags` (slugs like `enzyme_limited_assessment` vs D-4 user sentences)
     - `evidence_anchor_sentence` **present and non-empty** (D-4) vs **absent** (old snapshot / older code path)

**Expected if snapshot is pre–D-4:** old headlines, slug-like liver caveats, **no** `evidence_anchor_sentence` (or not rendered).

**Expected after a fresh run with D-4 code:** D-4 headlines (when heuristics apply), user-safe liver caveats, `evidence_anchor_sentence` populated per `core/analytics/domain_narrative_wave1.py`.

---

## 3) Frontend: `Wave1DomainCards` wiring (post–D-4 `main`)

`frontend/app/components/results/Wave1DomainCards.tsx` (current tree):

| UI area | Source field |
|---------|----------------|
| Card subtitle (collapsed) | `contributor_sentence` (truncated) else `clinical_label` |
| Evidence anchor (collapsed) | `evidence_anchor_sentence` (only if truthy) |
| Band | `band_label` |
| Tier | `confidence_tier` |
| Main narrative line | `headline_sentence` |
| Expand: “Why / Confidence / Consequence / Next” | `contributor_sentence`, `confidence_sentence`, `consequence_sentence`, `next_step_sentence` |
| Expand: missing markers | `missing_marker_ids` (canonical ids) |
| Expand: caveats | `caveat_flags` joined with ` · ` |

**Conclusion:** The component **does** render D-4 fields. If the API omits `evidence_anchor_sentence`, the anchor block **correctly** does not show (no bug). If the API still has slug `caveat_flags`, the UI will show them as-is (backend should send D-4 user phrases).

There is no alternate code path in this component that would “hide” a correct D-4 payload.

---

## 4) D-4 logic “not firing”

For a **given stored** `analysis_id`, the assembler (`assemble_consumer_domain_scores_v1`) is **not** invoked on GET. So “D-4 not firing” for that id usually means: **it was never executed for that id at save time** (old pipeline output), not that D-4 code is dead on the server.

---

## 5) Runtime / build (cannot assert remotely)

| Check | What to do locally |
|-------|-------------------|
| Backend on D-4 | `git log -1` in repo used to start uvicorn; ensure commit includes D-4; restart server after pull. |
| Frontend on D-4 | `git log -1` in `frontend/`; `next build` or dev server from same tree; hard refresh; clear `.next` if suspicious. |
| Stale data | For UAT, prefer a **new** `analysis_id` after D-4 merge. |

---

## 6) Root cause (primary)

**Stale persisted analysis snapshot** for the `analysis_id` under review:  
`GET /result` returns the **frozen** `client_result_shape_v1` written at completion time, not a live recompute. An analysis completed before D-4 will still present pre–D-4 (or D-3-only) `consumer_domain_scores` in the API and therefore in the UI.

Secondary causes *only if* a **new** post–D-4 run still shows old copy *then* investigate: wrong git checkout, old server process, or frontend build cache.

---

## 7) Smallest safe next step

1. **Run a new analysis** (same user, same panel if desired) **after** D-4 is deployed and both servers restarted.  
2. Open **results** for the **new** `analysis_id` and compare Wave 1 cards.  
3. Optionally `GET /api/analysis/result` for the **old** id and the **new** id side-by-side to confirm the snapshot diff.

**Do not** expect changing server code alone to retroactively change an existing `analysis_id` in the database.

---

## 8) Scope compliance

- No scoring change, no Phase 2, no PDF, no speculative fix — documentation and code-path analysis only.
- This file + bus commits live on `feature/wave1-runtime-diagnosis` until merged by maintainers.
