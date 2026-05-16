# LC-S8D — UK/SI Unit Governance Remediation Notes

**work_id:** LC-S8D  
**branch:** `launch-core/lc-s8d-uk-si-unit-governance-remediation`  
**date:** 2026-05-16

---

## Phase A — Safe equivalence remediation

**Status:** COMPLETE

**Files changed:**
- `backend/ssot/units.yaml` — named `mmol/L`, `mEq/L`, `10^9/L`; 1:1 equivalence conversions
- `backend/core/units/registry.py` — equivalence groups and conversion dispatch
- `backend/ssot/biomarkers.yaml` — canonical units for platelets, WBC, Na/K/Cl
- `backend/ssot/scoring_policy.yaml` — PLT/WBC scoring units → `10^9/L` (numeric bands unchanged)

**Tests run:**
- `backend/tests/unit/test_unit_registry.py` (Phase A vectors)
- Phase A equivalence assertions in `test_lc_s8d_unit_governance_sentinel.py`

**Decisions:** K/μL, K/uL, and 10^9/L are 1:1; mEq/L and mmol/L are 1:1 for monovalent electrolytes only.

**Next phase safe:** YES

---

## Phase B — True conversion evidence gate

**Status:** `PHASE_B_BLOCKED_PENDING_EVIDENCE`

**Blocked rows (unchanged):** calcium, corrected_calcium, magnesium, free_t4, hemoglobin

**Reason:** No primary UK lab source citations attached in-repo per LC-S8C §2.4 and §4 B1–B2.

**Next phase safe:** YES for Phase C rows not dependent on Phase B

---

## Phase C — Layer B scoring migration

**Status:** COMPLETE (authorised rows)

**Migrations:**
| Biomarker | Layer B unit (was → now) |
|-----------|--------------------------|
| glucose | mg/dL → mmol/L |
| total_cholesterol, ldl, hdl, triglycerides | mg/dL → mmol/L |
| creatinine | mg/dL → µmol/L |
| hba1c | % → mmol/mol |
| hematocrit | % → L/L |
| platelets, white_blood_cells | K/μL → 10^9/L (after Phase A) |

**HbA1c:** Arbitration unchanged; `%` legacy input converts to mmol/mol base; `hba1c_pct` dropped on Layer B path only.

**Haematocrit:** L/L canonical; `%` input converts via ×0.01; prevents `0.438 %` storage when normalisation runs.

**Tests run:**
- `test_scoring_rules.py`, `test_hba1c_governance.py`, `test_lc_s8_biomarker_unit_reference_incoherence_regression.py`

**Deferred:** `hba1c_pct` KB signal remap (out of allowed files).

**Next phase safe:** YES

---

## Phase D — Layer C display policy

**Status:** COMPLETE (backend contract)

**Files:**
- `backend/ssot/display_unit_policy.yaml` (new)
- `backend/core/units/display_policy.py` (loader)
- `backend/app/routes/analysis.py` — `display_unit_policy` + `upload_panel_observations` meta

**Mode A:** `upload_panel_observations` preserves pre-arbitration rows (e.g. dual HbA1c lines).

**Mode B:** Policy declares analytical-report collapse per biomarker; narrative path consumes collapsed Layer B input.

**Frontend:** Renderer-only; no conversion constants added.

**Next phase safe:** YES

---

## Phase E — Sentinel lockdown

**Status:** COMPLETE (warn for Phase B deferred rows)

**Files:**
- `sentinel/packs/lc_s8d_unit_governance_v1.json`
- `backend/tests/regression/test_lc_s8d_unit_governance_sentinel.py`

---

## Files changed (summary)

SSOT: `biomarkers.yaml`, `units.yaml`, `scoring_policy.yaml`, `display_unit_policy.yaml`  
Core: `registry.py`, `display_policy.py`, `hba1c_layer_b_arbitration.py`, `scoring/rules.py`  
App: `analysis.py`  
Tests: unit + regression updates; new `test_lc_s8d_unit_governance_sentinel.py`  
Sentinel: `lc_s8d_unit_governance_v1.json`

---

## Deferred items

- Phase B true conversions (Ca, corrected Ca, Mg, fT4, Hb) pending primary evidence
- `hba1c_pct` knowledge_bus package remap
- Full frontend Mode A/B UI wiring (types/contracts only in this sprint via API meta)

---

## Known residual risk

- Panels that skip `apply_unit_normalisation` may still pass incoherent raw units
- Hemoglobin scoring remains g/dL (US) until Phase B evidence passes

---

## Cursor completion recommendation

Implementation complete for Phases A, C, D, E and documented Phase B block. Recommend Claude audit + GPT architectural review (HIGH risk) before merge. Kernel `finish` pending closure audit.
