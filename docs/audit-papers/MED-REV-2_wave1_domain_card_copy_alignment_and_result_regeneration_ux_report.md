# MED-REV-2 — Wave 1 Domain Card Copy Alignment and Result Regeneration UX Report

**Work ID:** `MED-REV-2_wave1_domain_card_copy_alignment_and_result_regeneration_ux`  
**Branch:** `work/MED-REV-2-wave1-domain-card-copy-alignment-and-result-regeneration-ux`  
**Change type:** MIXED (Layer B narrative/DTO + Layer C regeneration UX)

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

Not executed in this session (requires local stack + login for `746f2b0a-b470-4d87-8ed8-e2c3d1e68c02`).

## Remaining risks / carry-forwards

- Full DB lineage table (`parent_analysis_id` column) deferred per LAUNCH-CORE-3 policy; meta field only for v1
- Regeneration uses current auth user demographics when original `user` payload was not stored on analysis row
- Homocysteine/CRP IDL records remain enabled for non-card surfaces (patterns/hero) — out of Track A card scope
