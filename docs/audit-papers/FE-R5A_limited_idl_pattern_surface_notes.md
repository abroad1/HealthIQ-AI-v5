# FE-R5A — Limited IDL Pattern Surface

**work_id:** FE-R5A  
**branch:** `frontend/fe-r5a-limited-idl-pattern-surface`  
**change_type:** MIXED (frontend surfacing only; no backend runtime changes)

---

## 1. Preflight results

| Check | Result |
|-------|--------|
| Stash | Empty |
| Pre-start dirty | Bus prompt/hardening — committed before kernel start |
| Kernel | `start` → implementation → `finish` |
| Cross-sprint guards (pre) | FE-R1/R2/R3 + LC-S16/17/19 + LC-S20/22 — **pass** |

---

## 2. FE-R4 merge confirmation

`docs/audit-papers/FE-R4_patterns_layer_gate_and_implementation_decision.md` on `main` at `fc999e2`. GO WITH CONDITIONS verdict implemented here.

---

## 3. IDL fields used

From `interpretation_display_layer_v1.records[]` (via `selectSafeIdlPatternRecords`):

- `retail_display_label`
- `subtitle`
- `why_it_matters`
- `supporting_biomarkers_summary` (omitted when generic publish fallback only)
- `severity_state` (chip)
- `scientific_class` (consumer chip via `formatScientificClassChipLabel`)
- Optional: `supporting_systems_summary`, `user_safe_description`, `display_caveat`

Gate: `enabled_for_frontend === true`, `frontend_allowed_term !== 'clinical_only'`, label passes `isUnsafePatternRetailLabel`.

---

## 4. IDL fields deliberately not used

- `internal_id` (React key only — not displayed)
- `clinical_display_label` (not shown separately — retail label is consumer surface)
- `frontend_allowed_term` (filter only)
- `clusters[]` / `cluster.name` / `cluster_id`
- `consumer_domain_scores` (remain in supplementary “Health domains” disclosure)
- `root_cause_v1` hypothesis titles

---

## 5. Sections/components changed

| File | Change |
|------|--------|
| `frontend/app/(app)/results/page.tsx` | Retail journey slot for patterns; conditional section; indices shifted |
| `frontend/app/components/results/InterpretationPatternsSection.tsx` | FE-R5A guards, scientific-class chip, embed mode, supporting-marker gate |
| `frontend/app/lib/feR2ResultsJourneyOrder.ts` | Added `fe-r5a-journey-patterns-across-body` |
| `frontend/app/lib/feR5aIdlPatternGuards.ts` | **New** — safe record selection + label guards |
| `backend/tests/regression/test_fe_r2_results_journey_restructure.py` | Journey length/index updates |
| `backend/tests/regression/test_fe_r3_evidence_depth_ux_quality.py` | Journey index updates |
| `backend/tests/regression/test_fe_r5a_limited_idl_pattern_surface.py` | **New** |
| `sentinel/packs/escaped_defects_v1.json` | Six FE-R5A defect classes |

---

## 6. Current retail journey position

```
body overview → working well → primary finding → uncertainty → patterns across your body* → marker evidence → next steps → clinician summary
```

\*Section omitted entirely when `selectSafeIdlPatternRecords` returns zero rows (no placeholder).

Journey test id: `fe-r5a-journey-patterns-across-body` (`FE_R2_RESULTS_JOURNEY_SECTION_TEST_IDS[4]`).

---

## 7. Safeguards against raw cluster/internal labels

- Pattern cards render only from IDL records passing `selectSafeIdlPatternRecords`.
- `isUnsafePatternRetailLabel` blocks labels matching FE-R0 failure modes (e.g. `Functional read —`, `Cardiovascular 4 Biomarkers`, `ph_*`, `signal_*`).
- No `clusters[]` references in `InterpretationPatternsSection`.
- Duplicate IDL block removed from secondary disclosure (Wave-1 domain cards only there).

---

## 8. Classification/taxonomy display decision

`scientific_class` shown as restrained consumer chips: **Phenotype**, **Risk pattern**, **Organ pattern**, **Health pattern**. Raw enum tokens are not shown.

---

## 9. Fallback behaviour

- `showRetailIdlPatterns === false` → journey section not rendered (no heading-only shell).
- Component returns `null` when no safe rows.
- No fallback to `clusters[]`.
- Generic supporting summary `"Key pattern signals for this interpretation."` hidden on cards.

---

## 10. Tests added/updated

- `test_fe_r5a_limited_idl_pattern_surface.py` (9 cases)
- Updated `test_fe_r2_results_journey_restructure.py`, `test_fe_r3_evidence_depth_ux_quality.py`

Validation (post-implementation):

```text
pytest backend/tests/regression/test_fe_r1_consumer_prose_cleanup.py -q
pytest backend/tests/regression/test_fe_r2_results_journey_restructure.py -q
pytest backend/tests/regression/test_fe_r3_evidence_depth_ux_quality.py -q
pytest backend/tests/regression/test_fe_r5a_limited_idl_pattern_surface.py -q
pytest backend/tests/regression/test_lc_s16_17_19_kb_surface_payload_contract.py -q
pytest backend/tests/regression/test_lc_s20_22_persisted_replay_sentinel_phase2.py -q
npm run type-check
```

---

## 11. Sentinel updates

Added: `patterns_section_missing_when_idl_safe`, `patterns_section_wrong_journey_position`, `raw_cluster_name_used_as_pattern_label`, `unsafe_pattern_taxonomy_visible`, `patterns_section_placeholder_visible`, `fe_r3_marker_evidence_regressed` → `test_fe_r5a_limited_idl_pattern_surface.py`.

---

## 12. Residual risks

- Panels with only `clinical_only` IDL rows may show **no** patterns section (by design).
- Hero/domain copy may still reference internal names outside this section (PATTERN-C1).
- Browser UAT not run in this session.
- Multiple enabled IDL rows on large panels not manually verified.

---

## 13. Recommendation for PATTERN-C1

- Expand signal→IDL enablement across panel fixtures.
- Fix `evidence_anchor_sentence` / hero internal name leaks.
- Review `frontend_allowed_term` policy for additional retail-safe rows.
- Add Sentinel for generic supporting-summary at publish time.

---

*Cursor implements limited IDL surfacing only — not self-certified for merge or PATTERN-C1 authorisation.*
