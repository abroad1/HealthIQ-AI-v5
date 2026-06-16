# Investigation — `fdf9bc74` false `incompatible` / `render_blockers: ["clinician_report_v1"]`

**Date:** 2026-06-16  
**Mode:** Investigation only — no code changes  
**Analysis ID:** `fdf9bc74-70db-4d36-be8a-8c709c654df8`  
**Related UAT:** [`UAT_results_page_analysis_fdf9bc74_2026-06-16.md`](UAT_results_page_analysis_fdf9bc74_2026-06-16.md)  
**API evidence:** `automation_bus/_uat_fdf9bc74.json`

---

## Executive verdict

This is a **backend compatibility-check bug**, not a failed new analysis. The engine generates `clinician_report_v1` at read time; versioning checks the **wrong payload** (pre-DTO stored snapshot). **Regenerate would repeat the same false warning.**

---

## End-to-end path (new upload)

| Step | Route / function | What happens |
|------|------------------|--------------|
| 1. Parse | `POST /api/upload/parse` → `backend/app/routes/upload.py::parse_upload` | Returns parsed biomarkers only; **no analysis created** |
| 2. Validate | `POST /api/upload/validate` → `upload.py::validate_upload_format` | Format check only |
| 3. Start | `POST /api/analysis/start` → `backend/app/routes/analysis.py::start_analysis` | Normalise → `AnalysisOrchestrator.run()` → build `stored` dict → persist |
| 4. Execute | `backend/core/pipeline/orchestrator.py::AnalysisOrchestrator.run` | Current pipeline; produces DTO with `meta.insight_graph.report_v1`, `narrative_report_v1`, `consumer_domain_scores`, `clusters`, etc. |
| 5. Persist | `PersistenceService.save_live_analysis_after_run` | Writes `AnalysisResult.processing_metadata["client_result_shape_v1"]` = `stored` |
| 6. Result GET | `GET /api/analysis/result` → `get_analysis_result` | Load `raw` → `build_analysis_result_dto(raw)` → `build_result_versioning_metadata(raw)` |
| 7. Frontend | `frontend/app/(app)/results/page.tsx` | Renders DTO; `StaleResultBanner` reads `result_versioning.result_status` |

Upload/validate do not touch analysis persistence. The new run uses the **same** `start_analysis` path as any live analysis.

---

## 1. Where `clinician_report_v1` is expected

| Layer | Location | Expectation |
|-------|----------|-------------|
| **Persisted replay contract** | `backend/core/dto/persisted_replay_contract_v1.py` → `PERSISTED_RENDER_REQUIRED_KEYS` | `clinician_report_v1` is a **required key on the stored dict** |
| **Frontend contract** | `backend/core/dto/frontend_contract_v1.py` → `FRONTEND_CONSUMED_ROOT_KEYS` | Required on **API response** |
| **API DTO builder** | `backend/core/dto/builders.py::build_analysis_result_dto` | Compiles from `meta.insight_graph.report_v1` |
| **Compiler** | `backend/core/analytics/report_compiler_v1.py::compile_clinician_report_v1` | Source of truth for assembly |

---

## 2. Is `clinician_report_v1` generated on a new analysis?

**Yes — at DTO assembly, not at persistence.**

For `fdf9bc74`:

- `meta.insight_graph.report_v1` is present in stored payload
- `build_analysis_result_dto(stored)` produces a full `clinician_report_v1` (header, sections, page1 `primary_concern`, root_cause hypotheses, etc.)
- UAT API JSON includes `clinician_report_v1` as a populated dict

`compile_clinician_report_v1` only returns `None` when `report_v1_payload` is empty — not the case here.

---

## 3. Is it persisted?

**No — by current design.**

`start_analysis` stored shape (`analysis.py` ~218–282) and `build_client_result_shape_from_dto` (`analysis_regeneration.py` ~49–113) both **omit** `clinician_report_v1` (and `balanced_systems_v1`).

Persistence target:

```text
AnalysisResult.processing_metadata["client_result_shape_v1"]
```

via `PersistenceService.save_live_analysis_after_run` (`persistence_service.py` ~320–365).

`persistence_service.py` explicitly documents that Part B rebuilds the frontend DTO via `build_analysis_result_dto` — i.e. derived fields are expected at read time.

---

## 4. Is it dropped during DTO assembly?

**No.** DTO assembly **adds** it in `backend/core/dto/builders.py::build_analysis_result_dto` via `compile_clinician_report_v1`.

The GET response for `fdf9bc74` **has** `clinician_report_v1`. Nothing is dropped after compile.

---

## 5. Is the compatibility checker looking in the wrong place?

**Yes — root cause.**

In `backend/app/routes/analysis.py::get_analysis_result`:

```python
raw = _raw_result_payload_for_analysis_id(analysis_id, db, auth_user)
dto = build_analysis_result_dto(raw)
dto["result_versioning"] = build_result_versioning_metadata(
    raw,
    raw_biomarkers=raw_biomarkers,
)
```

`build_result_versioning_metadata` → `assess_persisted_result_compatibility(stored)` checks **`raw` (DB snapshot)**, not **`dto` (assembled API contract)**.

Reproduced on UAT artefact:

| Payload assessed | `compatible` | `render_blockers` |
|------------------|-------------|-------------------|
| DB-like stored (no `clinician_report_v1`) | `false` | `["clinician_report_v1"]` |
| Full API DTO (after `build_analysis_result_dto`) | `true` | `[]` |

In `persisted_replay_contract_v1.py`, missing required keys become render blockers:

```python
missing_required = tuple(sorted(k for k in PERSISTED_RENDER_REQUIRED_KEYS if k not in stored))
render_blockers: List[str] = list(missing_required)
```

So `clinician_report_v1` in `render_blockers` means **“key absent from stored JSON”**, not **“compiler failed”**.

Frontend (`StaleResultBanner.tsx`) correctly displays whatever the API returns — **not a frontend false positive**.

---

## 6. Old engine / old persistence / old compiler?

**No.**

| Check | `fdf9bc74` evidence |
|-------|---------------------|
| `result_version` | `1.0.0` (current) |
| `replay_manifest.manifest_version` | `1.0.0` (current) |
| `meta.completeness_policy_id` | `launch_core_1_subsystem_union_v1` (current) |
| `stale_reasons` | `[]` (no LC-1/LC-3 stale heuristics) |
| `report_v1` in meta | Present |
| Narrative / IDL / domain cards | Present and populated |
| Dashboard date | 6/16/2026 — new run |

This is **not** an old snapshot misclassified as new. It is a **contract mismatch** introduced when LAUNCH-CORE-3 required `clinician_report_v1` on the **persisted** dict while persistence still stores the **pre-compile orchestrator snapshot**. The LC-S20 fixture generator saves the **post-`build_analysis_result_dto`** shape to fixtures, masking the gap in tests.

---

## 7. Why `pattern_groups` appears empty

**There is no `pattern_groups` field in the API.** UAT `pattern_groups_count: 0` maps to UI copy, not backend data.

| Fact | Detail |
|------|--------|
| Clusters exist | **3** clusters in stored/API payload |
| UI control | `ResultsBodyOverview` `showPatternGroupBuckets={showDetails}` (`page.tsx` ~695) |
| Default retail | `showDetails` is `false` → buckets hidden **by design** (FE-R6A: avoid pattern-counter contradiction) |
| Fallback copy | When buckets hidden, component always shows *“Pattern groups are not available for this result yet…”* even when clusters exist |

Empty pattern groups on a new result is **misleading frontend copy + gating**, separate from the incompatible banner. Not caused by missing backend `pattern_groups` generation.

---

## 8. Is `compatible: false` correct or false?

**False positive (backend metadata bug).**

- Page renders hero, domains, narrative, markers, clinician sections — using compiled `clinician_report_v1` from DTO
- `result_status: "incompatible"` is driven only by missing key on **stored** shape
- `stale_reasons: []` confirms this is not a genuine stale/old-engine case

---

## 9. Would “Regenerate with latest engine” fix it?

**No — same false warning would recur.**

`POST /api/analysis/{id}/regenerate` → `run_pipeline_from_raw_biomarkers` → `build_client_result_shape_from_dto` → same persistence path **without** `clinician_report_v1` → same `build_result_versioning_metadata(raw)` → same `incompatible`.

Regeneration re-runs the **current** engine but does not change the stored/assessed shape mismatch.

---

## Confirmed root cause

**LAUNCH-CORE-3 compatibility assessment is applied to the pre-compile persisted snapshot (`client_result_shape_v1`), but `clinician_report_v1` (and `balanced_systems_v1`) are intentionally derived only in `build_analysis_result_dto` at GET time.** Every new live analysis that follows the current persist path will get `render_blockers: ["clinician_report_v1"]` and `compatible: false` even when the compiler succeeds and the page renders correctly.

**Classification:** Backend — **DTO assembly vs versioning policy mismatch** (not generation failure, not persistence loss, not frontend checker bug).

---

## Proposed smallest safe fix (not implemented)

**Option A (recommended, minimal):** In `get_analysis_result`, assess compatibility on the **assembled DTO**:

```python
dto = build_analysis_result_dto(raw)
dto["result_versioning"] = build_result_versioning_metadata(dto, raw_biomarkers=...)
```

Stale heuristics (`detect_launch_core_stale_reasons`) should still run on fields that **are** persisted (`consumer_domain_scores`, `meta`, etc.) — those exist on both `raw` and `dto`.

**Option B (contract alignment):** Split `PERSISTED_RENDER_REQUIRED_KEYS` into:

- `PERSISTED_STORED_REQUIRED_KEYS` — orchestrator fields actually written at save time (exclude derived-at-read keys)
- Keep full set for post-`build_analysis_result_dto` assessment only

Option A is one-line behavioural fix; Option B is cleaner long-term documentation of two shapes.

**Explicitly not recommended per investigation constraints:** dummy `clinician_report_v1`, frontend ignore, hiding banner.

**Separate follow-up (out of scope for incompatible banner):** `ResultsBodyOverview` fallback text when `showPatternGroupBuckets=false` but `clusters.length > 0` — copy says “not available” when data exists but is gated.

---

## Files likely to change

| File | Change |
|------|--------|
| `backend/app/routes/analysis.py` | Pass `dto` (not `raw`) to `build_result_versioning_metadata` in `get_analysis_result` |
| `backend/core/dto/persisted_replay_contract_v1.py` | Optionally split stored vs API required keys |
| `backend/tests/unit/test_launch_core3_result_versioning.py` | Add test: stored shape without `clinician_report_v1` + DTO build → compatible |
| `backend/tests/integration/test_analysis_api.py` or new regression | POST `/start` → GET `/result` → `result_versioning.compatible is True` for fresh run |
| `backend/tests/regression/test_lc_s20_22_persisted_replay_sentinel_phase2.py` | Align fixtures/expectations if stored vs API contract split |

---

## Tests needed

1. **Regression:** Simulate `start_analysis` stored dict (no `clinician_report_v1`) → `build_analysis_result_dto` → `build_result_versioning_metadata` → assert `compatible=True`, `render_blockers=[]`, `result_status != "incompatible"`.
2. **Integration:** Full `POST /api/analysis/start` + `GET /api/analysis/result` → no incompatible banner metadata on fresh analysis.
3. **Regression:** Regenerate path → new `analysis_id` → same compatibility assertion.
4. **Negative (keep):** Truly missing `report_v1` in meta → `compile_clinician_report_v1` returns `None` → should remain incompatible (real failure case).
5. **Optional UX test:** `clusters.length > 0` + `showPatternGroupBuckets=false` → don’t assert “not available” (separate work package).

---

## Summary table

| Question | Answer |
|----------|--------|
| Analysis created | `POST /api/analysis/start` → `start_analysis` |
| `clinician_report_v1` generated | `compile_clinician_report_v1` in `build_analysis_result_dto` |
| Persisted | **No** — `processing_metadata["client_result_shape_v1"]` |
| Dropped in DTO | **No** — added at read time |
| Checker wrong location | **Yes** — checks `raw` not `dto` |
| Old engine/path | **No** — current pipeline; policy/implementation drift |
| Empty pattern groups | **Frontend gating** (`showPatternGroupBuckets=showDetails`); 3 clusters exist |
| `compatible: false` correct? | **No** — false positive |
| Regenerate fixes? | **No** — repeats same persist + assess bug |

---

## API snapshot (key fields)

```json
{
  "status": "completed",
  "biomarker_count": 79,
  "result_versioning": {
    "compatible": false,
    "result_status": "incompatible",
    "launch_user_behaviour": "display_stale_warning",
    "user_message": "This saved result cannot be displayed with the current results page contract.",
    "render_blockers": ["clinician_report_v1"],
    "regeneration_available": true,
    "stale_reasons": []
  },
  "idl_strong_signal": "Vascular Inflammation Risk",
  "primary_concern": "Homocysteine Elevation Context: warrants attention on this panel",
  "hypothesis_title": "B12-associated pattern",
  "clusters_count": 3
}
```

---

**Status:** Investigation complete. Awaiting approval before implementation.
