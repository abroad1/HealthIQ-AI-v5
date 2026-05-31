# MED-REV-2 — Wave 1 Domain Card Copy Alignment and Result Regeneration UX Report

**Work ID:** `MED-REV-2_wave1_domain_card_copy_alignment_and_result_regeneration_ux`  
**Branch:** `work/MED-REV-2-wave1-domain-card-copy-alignment-and-result-regeneration-ux`  
**Change type:** MIXED (Layer B narrative/DTO + Layer C regeneration UX)  
**Audit status:** Manual UAT and endpoint verification complete — **ready for Claude re-audit** (2026-05-31)

## Track A — root cause and fix path

**Root cause:** MED-REV-1 hid thin subsystems at the card-evidence layer, but domain-card prose still resolved from IDL ordering and legacy narrative fallbacks:

- `_IDL_ORDER_CV` preferred `ph_vascular_hcy_inflammation_v1` → “Vascular Inflammation Risk” anchor
- `_IDL_ORDER_MET` could select `ph_metabolic_early_ir_v1` → insulin-resistance contributor copy
- `_WAVE1_PLAIN_DESCRIPTOR` still said “Sugar and insulin balance”
- Liver low-confidence copy hardcoded GGT/ALP/albumin as missing regardless of panel

**Fix path (Layer B — Path B per hardening):** Reordered Wave 1 primary IDL selection to lipid-first / HbA1c-only; removed homocysteine and insulin-resistance IDL fallbacks from primary contributor paths; added `_evidence_anchor_from_visible_subsystems` so anchors use visible scored subsystem labels (“Atherogenic lipid pattern”, “Long-term blood sugar”); made liver confidence copy panel-aware.

IDL registry `enabled_for_frontend` flags were **not** changed (avoid global IDL consumer side effects).

## Track A — before/after examples

| Domain | Before (typical) | After |
|---|---|---|
| Cardiovascular anchor | Based mainly on: Vascular Inflammation Risk | Based mainly on: Atherogenic lipid pattern |
| Blood sugar descriptor | Sugar and insulin balance | Long-term blood sugar pattern |
| Blood sugar anchor | IDL / IR-framed | Based mainly on: Long-term blood sugar |
| Liver low confidence | …including GGT, ALP, albumin… (even when present) | Names only markers actually absent from panel |

## Track B — preflight findings

| Question | Finding |
|---|---|
| Raw upload stored? | Yes — `analyses.raw_biomarkers` (JSON) |
| Questionnaire stored? | Yes — `analyses.questionnaire_data` |
| Parsed payload stored? | Yes — `analysis_results.processing_metadata[client_result_shape_v1]` (immutable snapshot) |
| Orchestrator re-runnable? | Yes — same normalisation path as `POST /start` |
| Overwrites old result? | **No** — regeneration creates new `analysis_id` |
| DB lineage columns? | Not required for v1 — `meta.regenerated_from_analysis_id` on new snapshot |
| Stale/incompatible detection? | Yes — LAUNCH-CORE-3 `build_result_versioning_metadata` |
| UAT IDs regeneratable? | When `raw_biomarkers` preserved on analysis row (typical for DB-persisted live runs) |

## Track B — implementation

- `POST /api/analysis/{analysis_id}/regenerate` — reads preserved input, runs current engine, persists **new** analysis/result, stamps lineage in meta
- `regeneration_available` derived from stored `raw_biomarkers` sufficiency (not hardcoded false)
- `StaleResultBanner` shows **Regenerate with latest engine** button only when backend sets `regeneration_available: true`
- Unavailable path shows `regeneration_unavailable_reason` or upload-again guidance

**Immutability:** Source analysis row and snapshot are never mutated.

## Layer responsibility split

| Layer | Changes |
|---|---|
| A | Unchanged (stored inputs already preserved) |
| B | `domain_score_assembler.py`, `domain_narrative_wave1.py`, `result_versioning_policy_v1.py`, `analysis_regeneration_v1.py`, `analysis_regeneration.py`, `analysis.py` regenerate route |
| C | `StaleResultBanner.tsx`, `results/page.tsx`, `analysis.ts` types |

## Files changed

- `backend/core/analytics/domain_score_assembler.py`
- `backend/core/analytics/domain_narrative_wave1.py`
- `backend/core/dto/analysis_regeneration_v1.py` (new)
- `backend/core/dto/result_versioning_policy_v1.py`
- `backend/app/analysis_regeneration.py` (new)
- `backend/app/routes/analysis.py`
- `frontend/app/components/results/StaleResultBanner.tsx`
- `frontend/app/(app)/results/page.tsx`
- `frontend/app/types/analysis.ts`
- `backend/tests/regression/test_med_rev2_domain_card_copy_and_regeneration.py` (new)
- `backend/tests/regression/test_domain_ux1a_wave1_health_systems_card_scaffold.py`
- `frontend/tests/components/StaleResultBanner.test.tsx`

## Evidence preservation

- No marker evidence removed; no scoring rails/thresholds changed
- MED-REV-1 hidden subsystems remain hidden
- `total_bilirubin` protection unchanged

## Tests run

```powershell
python backend/scripts/validate_day_one_architecture.py
python -m pytest backend/tests/architecture/test_day_one_architecture_guardrails.py -q
python -m pytest backend/tests/regression/test_med_rev2_domain_card_copy_and_regeneration.py -q
python -m pytest backend/tests/regression/test_med_rev1_wave1_subsystem_visibility.py -q
python -m pytest backend/tests/unit/test_launch_core3_result_versioning.py -q
```

All PASS.

## Manual validation

**Executed:** 2026-05-31  
**Operator:** Cursor agent (browser + authenticated API)  
**Login:** `test-user3@example.com`  
**Stack:** `frontend` @ `http://localhost:3000`, `backend` @ `http://127.0.0.1:8000` (MED-REV-2 branch `bf7fc3d`; backend restarted so `POST …/regenerate` is live — prior process on :8000 was pre-route and returned 404)

**Primary URL:** `http://localhost:3000/results?analysis_id=746f2b0a-b470-4d87-8ed8-e2c3d1e68c02`  
**Regenerated sibling (same preserved upload):** `f0e5e6ff-4952-44a2-b144-1cc35344c2d2` (`meta.regenerated_from_analysis_id = 746f2b0a…`)

### Immutable-snapshot note (expected)

`746f2b0a…` is a **persisted immutable snapshot** (LAUNCH-CORE-3). Domain-card copy and subsystem rows are served from stored `consumer_domain_scores`; they are **not** retrofitted on read. Pre-MED-REV-2 copy therefore remains on the source record until regeneration. MED-REV-2 Track A criteria are verified on the **regenerated** result produced by `POST /api/analysis/746f2b0a…/regenerate`.

### Browser UAT checklist

| # | Criterion | Result | Evidence |
|---|---|---|---|
| 1 | CV card does not anchor on “Vascular Inflammation Risk” | **PASS (post-regen)** / **N/A on source snapshot** | Source `746f2b0a`: card header “Based mainly on: Vascular Inflammation Risk” (immutable pre-fix snapshot). Regenerated `f0e5e6ff`: “Based mainly on: **Atherogenic lipid pattern**”. |
| 2 | CV prose aligns with “Atherogenic lipid pattern” | **PASS (post-regen)** | Regenerated card expanded subsystem: single row **Atherogenic lipid pattern**; mechanism line uses atherogenic lipoprotein framing. |
| 3 | Blood sugar card does not imply insulin context when hidden | **PASS (post-regen)** | Regenerated descriptor **Long-term blood sugar pattern**; anchor **Long-term blood sugar**; expanded evidence shows only **Long-term blood sugar** subsystem (HbA1c included, glucose missing — no insulin-resistance row). Source snapshot still shows legacy “Sugar and insulin balance” + insulin subsystem rows. |
| 4 | Liver prose aligns with flattened model and available markers | **PASS (post-regen)** | Regenerated descriptor **Liver health from your blood markers**; expanded card has **no “Evidence by subsystem” rows**; confidence **“additional liver markers would strengthen this read”** (not hardcoded GGT/ALP/albumin list). Source snapshot still lists two liver subsystem rows and legacy GGT/ALP/albumin confidence line. |
| 5 | Hidden subsystems not shown as scored subsystem rows | **PASS (post-regen)** | Regenerated CV: one subsystem (lipid only). Regenerated MET: one subsystem. Regenerated LIV: none. Source snapshot: homocysteine, vascular strain, insulin/metabolic, and both liver subsystems still visible (pre-MED-REV-1/MED-REV-2 snapshot). |
| 6 | Regenerate button only when `regeneration_available: true` | **PASS** | On `746f2b0a`: stale/incompatible banner + **Regenerate with latest engine** button. API: `regeneration_available: true`, `regeneration_policy: med_rev2_versioned_regeneration_v1`. |
| 7 | Unavailable reason visible when `regeneration_available: false` | **PASS (policy + UI contract)** / **not live-fixture exercised** | All DB-persisted UAT analyses for this user retain `raw_biomarkers`, so live banner shows the button (not the unavailable copy). Verified unavailable path: `build_result_versioning_metadata(..., raw_biomarkers=None)` → `regeneration_available: false`, `regeneration_unavailable_reason: "Original upload biomarkers were not preserved…"`. `StaleResultBanner` renders that string (or upload-again fallback) when `regeneration_available` is false; unit test asserts no regenerate button in that path. |
| 8 | Regeneration: old result accessible, new result loads | **PASS** | `POST /api/analysis/746f2b0a…/regenerate` → `f0e5e6ff…` (3.3 s). Browser loaded new URL with MED-REV-2 cards. Re-fetch of `746f2b0a` unchanged (anchor still “Vascular Inflammation Risk”; snapshot immutable). |
| 9 | No internal IDs/traces visible | **PASS** | DOM text search on both pages: no `signal_*`, `wave1_cv_*`, `ph_vascular`, or `health_system_card_evidence` strings. Consumer labels only. |

### Stale / versioning banner (source analysis)

On `746f2b0a`:

- Banner title: **This saved result uses an older format**
- Body: **This saved result cannot be displayed with the current results page contract.**
- `result_versioning.result_status`: `incompatible`
- `stale_reasons`: `completeness_policy_missing`
- Regenerate CTA visible (item 6)

### Endpoint verification — `POST /api/analysis/{analysis_id}/regenerate`

**Request**

```http
POST /api/analysis/746f2b0a-b470-4d87-8ed8-e2c3d1e68c02/regenerate
Authorization: Bearer <test-user3 session>
```

**Response (200, ~3336 ms)**

```json
{
  "analysis_id": "f0e5e6ff-4952-44a2-b144-1cc35344c2d2",
  "source_analysis_id": "746f2b0a-b470-4d87-8ed8-e2c3d1e68c02",
  "status": "completed",
  "message": "Analysis regenerated successfully as a new result"
}
```

**Post-conditions verified**

| Check | Outcome |
|---|---|
| New analysis/result ID created | `f0e5e6ff-4952-44a2-b144-1cc35344c2d2` |
| Old result not overwritten | `GET …/result?analysis_id=746f2b0a…` — CV anchor unchanged |
| Lineage stamped on new snapshot | `meta.regenerated_from_analysis_id = 746f2b0a-b470-4d87-8ed8-e2c3d1e68c02` |
| New result loads with current engine copy | Browser + API confirm MED-REV-2 anchors/subsystems on `f0e5e6ff` |
| Old result remains accessible | `GET …/result?analysis_id=746f2b0a…` → 200 |

**Supporting GET (versioning on source)**

```json
{
  "regeneration_available": true,
  "regeneration_unavailable_reason": null,
  "regeneration_policy": "med_rev2_versioned_regeneration_v1",
  "result_status": "incompatible",
  "stale_reasons": ["completeness_policy_missing"]
}
```

### Defects found

None requiring implementation changes. Persisted pre-regeneration copy on `746f2b0a` is **by design** (immutable snapshot policy); regeneration is the supported remediation path.

## Remaining risks / carry-forwards

- Full DB lineage table (`parent_analysis_id` column) deferred per LAUNCH-CORE-3 policy; meta field only for v1
- Regeneration uses current auth user demographics when original `user` payload was not stored on analysis row
- Homocysteine/CRP IDL records remain enabled for non-card surfaces (patterns/hero) — out of Track A card scope
