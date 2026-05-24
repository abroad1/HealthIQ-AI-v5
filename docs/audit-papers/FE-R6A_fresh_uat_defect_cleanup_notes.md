# FE-R6A — Fresh UAT Defect Cleanup Notes

## 1. Preflight

| Check | Result |
|---|---|
| Branch | `frontend/fe-r6a-fresh-uat-defect-cleanup` |
| Stash | Empty |
| Work package token | `FE-R6A` (kernel started) |
| Controlling UAT | `FRESH_UAT_results_journey_quality_audit_f2dcb58f.md`, `FRESH_UAT_cursor_crosscheck_f2dcb58f.md` |

## 2. FE-R1 through FE-R5A merge confirmation

Evidence on `main` before FE-R6A branch: `test_fe_r1_consumer_prose_cleanup.py`, `test_fe_r2_results_journey_restructure.py`, `test_fe_r3_evidence_depth_ux_quality.py`, `test_fe_r4` gate doc, `test_fe_r5a_limited_idl_pattern_surface.py` — all present; FE-R6A regression suite re-run in validation below.

## 3. Fresh UAT defects addressed

| Defect | Fix layer |
|---|---|
| Hero buried under “How to read this page” | Frontend — removed instruction h2 wrapper; hero first; demoted framing note |
| Duplicate Summary card | Frontend — removed `NarrativeRetailSummaryCard` from retail journey |
| Pattern counter “Needs attention: 0” vs lead signal | Frontend — `showPatternGroupBuckets={showDetails}` on body overview |
| “interpretation confidence for this read” leak | Frontend — `feR6aRetailCopy` + `BalancedSystemsSummary` scrub + `retailNarrativeSanitize` |
| “Linked to …” internal labels | Frontend — removed from `UploadedPanelFidelity` |
| Next steps blob / packaged fallback | Frontend — `<ul><li>` in `DeterministicNarrativeSurface`; dedup vs confirmatory; removed hero fallback |
| Raw `Not scored - result unit…` on cards | Frontend — `sanitizeBiomarkerInterpretationForRetail` on card face and expansion |
| Hero vs section finding label mismatch | Frontend — `leadPatternLabel` bridge in `PrimaryFindingAndWhy` |
| Thin biomarker expansion (scoring-only) | Frontend — limited-state message; retail-safe interpretation zones; expandable when only scoring text |

## 4. Fresh UAT defects deferred

| Item | Reason |
|---|---|
| Homocysteine / Transferrin rich educational depth | DTO lacks `biomarker_educational_explainer` / contribution for this panel — KB-WAVE/content, not FE-R6A fabrication |
| Model-explainer sentence in body overview source | Scrubbed at retail boundary via `scrubFeR6aRetailSurfacePhrases`; compiler-side cleanup optional later |
| Full visual redesign | Out of scope |

## 5. Files changed

- `frontend/app/(app)/results/page.tsx`
- `frontend/app/lib/feR6aRetailCopy.ts` (prior commit)
- `frontend/app/lib/retailNarrativeSanitize.ts`
- `frontend/app/lib/resultsPageLayout.ts`
- `frontend/app/components/biomarkers/BiomarkerDials.tsx`
- `frontend/app/components/biomarkers/UploadedPanelFidelity.tsx`
- `frontend/app/components/results/*.tsx` (body overview, balanced systems, narrative surface, primary finding, hero blocks)
- `backend/tests/regression/test_fe_r6a_fresh_uat_defect_cleanup.py`
- `sentinel/packs/escaped_defects_v1.json`

## 6. Before / after (visible text)

| Before | After |
|---|---|
| H2: “How to read this page” wrapping hero + overview | Hero visible first; body overview under “Your body overview” |
| Standalone “Summary” card | Removed from main journey |
| “Needs attention: 0” pattern buckets in retail | Hidden unless advanced/details |
| “interpretation confidence for this read: insufficient” | Scrubbed from balanced-systems evidence lines |
| “Linked to hba1c” | Label removed; value-only display |
| “No separate checklist of follow-up lines was packaged” | `null` when no actions |
| Raw unit-alignment Not scored string on Homocysteine card | Consumer message or limited-state copy |
| Hero “Homocysteine Elevation Context” vs section “B12-associated pattern” | Bridge line when labels differ |

## 7. Biomarker expansion diagnosis

Expansion zones (interpretation / contribution / education) render when DTO fields exist. For `f2dcb58f` panel, Homocysteine often has only lab-range scoring text in `interpretation`; FE-R6A shows `BIOMARKER_LIMITED_STATE_MESSAGE` instead of sole “Scored using lab reference range” and keeps expand affordance for unscored-safe copy.

## 8. Homocysteine / Transferrin DTO diagnosis

Persisted biomarker records for this analysis lack governed educational explainer bodies in API payload inspected during UAT. Fixes are presentation-safe only; depth requires backend/KB content (KB-WAVE-1), not frontend inference.

## 9. Fix classification

| Area | Classification |
|---|---|
| Journey structure, copy scrub, list markup | Frontend presentation |
| Educational depth | Deferred content/DTO |
| Compiler | Not changed in FE-R6A |

## 10. Tests

- Added `test_fe_r6a_fresh_uat_defect_cleanup.py` (11 regression tests)
- Re-ran FE-R1, FE-R2, FE-R3, FE-R5A, LC-S8G, LC-S20-22, scoring rules (see validation log in commit message / CI)

## 11. Sentinel

Nine `fresh_uat_*` defect classes added to `escaped_defects_v1.json`, each mapped to `test_fe_r6a_fresh_uat_defect_cleanup.py`.

## 12. Browser UAT

Target URL: `http://localhost:3000/results?analysis_id=f2dcb58f-e816-4ff6-9011-e93c5d48b82c`  
**Not re-run in this session** — validation relied on deterministic regression + type-check. Recommend human spot-check before merge.

## 13. Residual risks

- Scrub-at-boundary may miss new internal phrases until Sentinel catches them
- Panels with partial DTO may still feel thin until KB-WAVE-1
- Confirmatory dedup depends on display_name matching narrative lines

## 14. KB-WAVE-1 recommendation

**Proceed only after** human spot-check on `f2dcb58f` and merge of FE-R6A. Evidence surface is **readier** (structure + safety); **not** fully differentiated until content/DTO depth lands in KB-WAVE-1.
