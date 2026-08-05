# CLIN-PRIORITY-CORE-1 — Implementation and Verification Report

**work_id:** `CLIN-PRIORITY-CORE-1`  
**branch:** `feature/clin-priority-core-1`  
**Date:** 2026-08-05  

## 1. Final architecture

```text
SignalEvaluator / SignalRegistry (unchanged activation)
        ↓
concern_constructor (+ longitudinal_rules annotations)
        ↓
ConsolidatedConcernSet → InsightGraphV1.clinical_concern_set
        ↓
AnalysisResult.meta.insight_graph.clinical_concern_set
        ↓
Frontend ClinicalConcernPrioritySection (sole clinical-priority UI authority)
Legacy clinician_report technical_tiebreak_lead → demoted / non-clinical when concern set present
```

## 2. Longitudinal implementation

| Rule | Authority | Behaviour |
|---|---|---|
| RE-T1 | Renal NICE NG148 | AKI finding when ≥50%/7d or ≥26 µmol/L/48h |
| RE-S-2 | Renal chronicity | Stable G3a only with ≥3 month comparable prior |
| HEP-T1 | Hepatic statin monitoring | Doubling within 3 months annotated; never advises cessation; not assessable without baseline |
| HAEM-T5 | Haematology `[J]` windows | 12m chronicity / 3m rate windows; absent ≠ stable |
| THY-T1 | NICE NG145 | Two occasions ≥3 months; no treatment claim from single result |
| CN-T2/T3 | Cardiometabolic | HbA1c spacing; no diabetes diagnosis assertion |

Fixtures: `backend/tests/fixtures/clinical_priority_longitudinal_v1.json`  
Coverage metric separate from 109-scenario estate.

## 3. Frontend integration and single-authority proof

When `meta.insight_graph.clinical_concern_set` is present:

1. Results journey renders `ClinicalConcernPrioritySection`.
2. `isCloseCallMode(..., { clinicalConcernAuthority: true })` returns false for `technical_tiebreak_lead`.
3. Competing ranked finding / close-call clinical framing is suppressed.
4. Constituent activation keys remain accessible under each finding (not deleted).

Proof tests: `frontend/tests/lib/clinicalConcernAuthority.test.ts`, `frontend/tests/components/ClinicalConcernPriority.test.tsx`.

## 4. Signal preservation

- Baseline 183 / preserved 183 / retired 0
- Supporting signal baseline/preserved 0 (schema has no supporting-signal dependency shape)

## 5. Scenario totals

- 110 rows / 109 unique / 0 skips / 0 failures
- No unauthorised fixture expectation changes in FINISH

## 6. FIB-4 / quarantines

- `ratio_registry.fib_4` untouched
- Concern set never uses FIB-4 for classification
- CV-risk % not computed

## 7. Deviations / STOP conditions

- None requiring invention of clinical thresholds.
- Backend unit estate contains pre-existing failures outside FINISH scope (classified in FINISH evidence).

## 8. File inventory (FINISH)

**Backend:** `longitudinal_rules.py`, `concern_constructor.py`, longitudinal fixture + tests  
**Frontend:** concern set types/helpers/section; demotion in WhyThisLeadWon, ClinicianReportRenderer, InsightPanel, body overview, results page; FE tests  
**Docs:** FINISH evidence, this report, START evidence update, BDR entry
