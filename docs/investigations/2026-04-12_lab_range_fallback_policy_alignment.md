# Lab-range-first vs governed-fallback scoring — policy / runtime alignment

**Date:** 2026-04-12  
**Scope:** Repo-and-runtime investigation only (no code changes).  
**Product expectation (stated):** Prefer lab-specific ranges; when missing, use governed fallback for eligible biomarkers so supported markers are not hard-stopped or zero-scored solely due to missing lab ranges.

---

## 1. Executive summary

| Question | Repo truth |
|----------|------------|
| Does the scoring engine use SSOT `biomarkers.*.bands` as a fallback when the lab sends no reference range? | **No** for ordinary (non–derived-ratio) biomarkers. `ScoringRules.calculate_biomarker_score` returns unscored (`missing_lab_reference_range`) unless a valid **input** min/max exists, or the marker is a **derived ratio** listed under `derived_ratios` with an entry in `derived_ratio_policy_bounds`. |
| Where do governed fallbacks live? | **`backend/ssot/scoring_policy.yaml`** → `derived_ratio_policy_bounds` (and the `derived_ratios` allow-list). Loaded in `core/scoring/rules.py` as `DERIVED_RATIO_POLICY_BOUNDS` / `DERIVED_RATIOS`. |
| Does orchestrator “policy injection” change that for lipid panels? | The orchestrator **injects policy bounds into `input_reference_ranges`** for **derived ratios** when lab range is missing (subject to unit compatibility). That feeds the **same** scoring path (lab-range-first, then derived-table for derived IDs only). It does **not** inject SSOT bands for `hba1c`, `ldl_cholesterol`, etc. |
| Alignment with stated product policy | **Misaligned / partial:** Runtime is intentionally **lab-range sovereign** for standard scored biomarkers (documented in code and tests). Governed numeric fallback exists for a **narrow** set: **derived ratios** in `derived_ratios`, not for general “supported” analytes. |

**Root-cause classification:** **Intended policy (product) and implemented runtime are misaligned** if product assumes SSOT bands in `scoring_policy.yaml` act as fallback for ordinary biomarkers. The implementation is **consistent with an alternate policy**: “lab ranges for measured analytes; policy bounds only for allow-listed derived ratios.” Evidence: `backend/core/scoring/rules.py` (lines 182–222), `backend/tests/test_scoring_lab_range_only.py`, and orchestrator comments at `backend/core/pipeline/orchestrator.py` (~1792–1795, ~1914–1916).

---

## 2. Files inspected (authoritative)

| Path | Role |
|------|------|
| `backend/core/scoring/rules.py` | **`calculate_biomarker_score`:** lab min/max first; non-derived → unscored without lab; derived allow-list → `derived_ratio_policy_bounds`. |
| `backend/core/scoring/engine.py` | Passes `input_reference_range` per biomarker into `calculate_biomarker_score`. |
| `backend/ssot/scoring_policy.yaml` | System biomarker lists, `biomarkers.*.bands` (loaded into `BiomarkerRule` but **not** used as fallback in `calculate_biomarker_score` for non-derived markers), `derived_ratios`, `derived_ratio_policy_bounds`, `scoring_runtime.unscored_reason_missing_lab_reference_range`. |
| `backend/core/analytics/scoring_policy_registry.py` | Loads/validates `scoring_policy.yaml`; stamps version/hash for replay. |
| `backend/core/pipeline/orchestrator.py` | Preserves lab ref ranges; injects **ratio** policy bounds via `_policy_bounds_for_ratio` + `DERIVED_RATIO_POLICY_BOUNDS`; DTO builder: **“Lab-Range Sovereignty: no SSOT fallback for scoring/display status paths”** for reference ranges; interpretation strings for unscored vs policy/lab. |
| `backend/core/analytics/ratio_registry.py` | Computes `apob_apoa1_ratio` etc.; units for ratios are **`ratio`** (or `mmol/L` for `non_hdl_cholesterol`). |
| `backend/ssot/biomarker_alias_registry.yaml` | Canonical `apob_apoa1_ratio` aliases include `apolipoprotein_ratio` and text like `Apolipoprotein ratio (Venous)` — **not** a slug with underscores/parentheses. |
| `backend/tests/test_scoring_lab_range_only.py` | Contract tests: HDL/LDL **without** lab range → unscored; `tc_hdl_ratio` **without** lab → uses derived table; SSOT ref lookup must not run. |
| `frontend/app/services/analysis.ts` | `validateBiomarkerData`: unit must be a **non-empty string** (not an allow-list per biomarker). |
| `frontend/app/state/analysisStore.ts` | Calls `AnalysisService.validateBiomarkerData` before POST. |
| `frontend/app/(app)/upload/page.tsx` | Biomarker object keys: `name.toLowerCase().replace(/\s+/g, '_')` → can produce `apolipoprotein_ratio_(venous)` etc. |
| `frontend/app/components/preview/EditDialog.tsx` | `COMMON_UNITS` list has no **`ratio`**; free-text unit field still allows typing `ratio`. |

---

## 3. Authoritative current runtime policy

### 3.1 Scoring engine (`ScoringRules.calculate_biomarker_score`)

1. If `input_reference_range` has numeric **min** and **max** with **min < max** → score using **position-in-range** curve (`_calculate_score_from_range`).  
2. Else if biomarker **not** in `DERIVED_RATIOS` → **`(0.0, CRITICAL, missing_lab_reference_range)`** (see `backend/core/scoring/rules.py` lines 208–211).  
3. Else (derived ratio) → use **`DERIVED_RATIO_POLICY_BOUNDS[biomarker_name]`** if valid min/max/unit; else unscored.

**Important nuance:** `BiomarkerRule` / SSOT **bands** under `biomarkers:` are used to **construct** rule objects (`_load_biomarker_rules`) but **`calculate_biomarker_score` does not consult those bands** for non-derived markers. So **`hba1c` bands in YAML do not substitute for a missing lab range** in the current scoring path.

### 3.2 Orchestrator: injection + DTO narrative

- For each **derived** ratio from `ratio_registry.compute`, if there is no valid **lab**-sourced range (`source == "lab"` with valid bounds), the orchestrator may inject **`ratio_registry`** policy bounds into `input_reference_ranges` when `_policy_bounds_for_ratio` accepts the derived marker’s unit vs policy (`backend/core/pipeline/orchestrator.py` ~1160–1228, ~1194–1227).  
- DTO copy explicitly states **no SSOT fallback for reference ranges** on scoring/display paths (~1792–1795, ~1914–1916). Unscored rows get **“Not scored - no reference range available”** when there is no usable range and no unscored_reason branch sets a different string (~1837–1846, ~1981–1994).

### 3.3 Enforcement / tests

- `backend/tests/test_scoring_lab_range_only.py` encodes **lab-only** for HDL/LDL and **derived-table** for `tc_hdl_ratio`.  
- `backend/tests/enforcement/test_scoring_policy_not_hardcoded.py` requires policy data to live in YAML, not inline literals in `rules.py` — it does **not** assert product “fallback for all supported analytes.”

---

## 4. Governed fallback sources

| Source | What it is | Used as scoring fallback? |
|--------|------------|---------------------------|
| `scoring_policy.yaml` → `biomarkers.*.bands` | Global/policy band **definitions** for many analytes | **No** — not applied when lab range missing in `calculate_biomarker_score` (non-derived). |
| `scoring_policy.yaml` → `derived_ratio_policy_bounds` | Min/max/unit/source for **allow-listed** derived ratios | **Yes** — only for IDs in `derived_ratios` and only after lab-range check fails (or for computed ratios merged by orchestrator). |
| Orchestrator injection | Copies policy bounds into `input_reference_ranges` for derived ratios | **Yes** — enables the same scoring path as an explicit range **for those IDs only**. |

**Conclusion:** “Governed fallback” in the **runtime scoring sense** means **`derived_ratio_policy_bounds` + `derived_ratios`**, not the main `biomarkers` band tables.

---

## 5. Per-example marker matrix

Assumptions: “lab range missing” means no valid min/max in `input_reference_ranges` for that canonical biomarker after normalization. “Governed fallback exists” means an entry in **`derived_ratio_policy_bounds`** *and* biomarker ID ∈ **`derived_ratios`** (for scoring), or orchestrator can inject bounds for that derived ID.

| Marker | In `scoring_policy` systems / biomarkers? | In `derived_ratios`? | Lab range required for engine score? | Governed fallback in scoring policy? | If lab range missing: current runtime scores? | Matches stated product policy? |
|--------|-------------------------------------------|----------------------|--------------------------------------|----------------------------------------|-----------------------------------------------|--------------------------------|
| **Folate** (`folate`) | **No** — not listed under `systems.*.biomarkers` | No | N/A (not in scoring engine’s weighted systems) | No | **No** engine score; DTO “unscored” path only if present in panel | **No** — no SSOT scoring fallback defined |
| **Free testosterone %** (`free_testosterone_pct`) | **No** | No | N/A | No | **No** engine score | **No** |
| **HbA1c** (`hba1c`) | Yes (metabolic) | No | **Yes** | Bands exist under `biomarkers.hba1c` but **not used** as fallback in `calculate_biomarker_score` | **No** — `missing_lab_reference_range` | **No** — contradicts “use governed fallback when lab missing” if product meant SSOT bands |
| **LDL cholesterol** (`ldl_cholesterol`) | Yes | No | **Yes** | Same: bands in YAML, **no** fallback path | **No** | **No** |
| **HDL cholesterol** (`hdl_cholesterol`) | Yes | No | **Yes** | Same | **No** | **No** |
| **Triglycerides** (`triglycerides`) | Yes | No | **Yes** | Same | **No** | **No** |
| **Apolipoprotein ratio** (canonical **`apob_apoa1_ratio`**) | Not under systems list as a separate row; treated as **derived** | **Yes** | Lab range preferred; if missing, **policy bounds** apply if unit matches | **Yes** (`apob_apoa1_ratio` in `derived_ratio_policy_bounds`, unit `ratio`) | **Yes** (policy band) **if** the value is keyed canonically and ratio pipeline runs | **Partial** — works for canonical ID; see §6 |

---

## 6. Apolipoprotein ratio — validation and contract notes

### 6.1 Intended unit (runtime)

- `ratio_registry.compute` sets lab and computed `apob_apoa1_ratio` with **`"unit": "ratio"`** (`backend/core/analytics/ratio_registry.py` ~159–171, `_derived_unit`).  
- `derived_ratio_policy_bounds.apob_apoa1_ratio.unit` is **`"ratio"`** in `scoring_policy.yaml` (~310–315).  
- So the **intended** dimensionless representation is **unit `ratio`**, not mg/dL.

### 6.2 Frontend validation path

1. **`AnalysisService.validateBiomarkerData`** (`frontend/app/services/analysis.ts` ~224–256): each biomarker must have `unit` as a **string** (any non-empty string passes). Message: **`Biomarker ${key} must have a valid unit`**.  
2. **`useAnalysisStore.startAnalysis`** (`frontend/app/state/analysisStore.ts` ~181–200): runs the above before API call.  
3. **Upload slug:** `frontend/app/(app)/upload/page.tsx` ~84–87 builds keys from display name → e.g. `Apolipoprotein ratio (Venous)` → **`apolipoprotein_ratio_(venous)`** (parentheses preserved).  
4. **Alias registry:** `apob_apoa1_ratio` lists aliases like `apolipoprotein_ratio` and human-readable **“Apolipoprotein ratio (Venous)”**, but **not** the underscore slug `apolipoprotein_ratio_(venous)` (`backend/ssot/biomarker_alias_registry.yaml` ~37–47).

### 6.3 Contract-alignment assessment

- **Empty/missing unit** → frontend validation fails (`valid unit` message) — **before** backend.  
- **Slug mismatch** (`apolipoprotein_ratio_(venous)` vs canonical `apob_apoa1_ratio`) → risk of **unmapped** or non-canonical key behaviour vs acceptance docs that assume mapping from plain text “Apolipoprotein ratio (Venous)” (`backend/tests/fixtures/panels/ab_full_panel_parsing_notes.md`).  
- **Edit UI:** `EditDialog` `COMMON_UNITS` does not include **`ratio`**; users can still type it in the free-text unit field.

**Verdict:** The “valid unit” blocker is **primarily frontend client-side validation** (non-empty string). It is **related** to broader contract alignment when parsers omit units for dimensionless ratios. Separately, **canonical ID alignment** (slug vs alias) affects whether **derived ratio** scoring and policy injection apply.

---

## 7. Overall root-cause classification

**Primary:** **Intended product policy (graceful governed fallback for “supported” biomarkers when lab ranges are missing) and implemented runtime are misaligned.** The codebase implements **lab-range sovereignty** for standard scored analytes and **policy bounds only** for **derived ratios** in an explicit allow-list.

**Secondary:** **Fallback exists for a narrower subset than the product paragraph implies** — derived ratios only, not the SSOT `biomarkers.*.bands` tables.

**Tertiary (UAT-specific):** **Validator / slug / alias mismatch can block or divert flows before normalization** (empty unit; non-matching biomarker key for apo ratio).

---

## 8. Does current runtime match intended product policy?

**Answer: Partial / No.**

- **Partial:** Derived ratios (e.g. **`apob_apoa1_ratio`** when canonical and unit-compatible) match “lab first, then governed fallback.”  
- **No:** Ordinary analytes (**HbA1c, LDL, HDL, triglycerides**) and non-scoring-policy markers (**folate, free_testosterone_pct**) do **not** receive SSOT band fallback in `calculate_biomarker_score` when the lab omits ranges.

---

## 9. Smallest safe next fix scope (for a future implementation sprint — not executed here)

1. **Clarify authority:** Decide whether SSOT `biomarkers.*.bands` should ever be used as scoring fallback (behaviour change + tests + governance).  
2. **If yes:** Single scoring-path change in `calculate_biomarker_score` (or explicit orchestrator injection mirroring derived-ratio pattern) with strict allow-list and versioning — **HIGH risk** (Intelligence Core).  
3. **If no:** Product/docs alignment only — **CONTENT**-class updates describing lab-range sovereignty.  
4. **Frontend/DX (narrow):** Add `ratio` to optional quick-pick units; ensure upload slug resolves to **`apob_apoa1_ratio`** (alias or normalizer) consistently with `biomarker_alias_registry.yaml`.

---

## 10. Recommended sprint grouping

| Sprint theme | Contents |
|--------------|----------|
| **A — Policy & contract** | Decide authoritative policy: lab-only vs SSOT fallback for which IDs; update governance artefacts accordingly. |
| **B — Scoring behaviour (if policy changes)** | Implement gated fallback from `scoring_policy.yaml` bands for chosen biomarkers; regression tests mirroring `test_scoring_lab_range_only.py`. |
| **C — Ingestion / FE contract** | Alias for `apolipoprotein_ratio_(venous)` → `apob_apoa1_ratio`; optional `ratio` in unit presets; parser unit defaults for dimensionless markers. |

---

## 11. References (code citations for navigation)

- Lab-only vs derived fallback: `backend/core/scoring/rules.py` (`calculate_biomarker_score`, `DERIVED_RATIOS`, `DERIVED_RATIO_POLICY_BOUNDS`).  
- Lab-range sovereignty comments: `backend/core/pipeline/orchestrator.py` (DTO builder sections ~1792–1795, ~1914–1916).  
- Tests: `backend/tests/test_scoring_lab_range_only.py`.  
- Policy lists: `backend/ssot/scoring_policy.yaml` (`systems`, `biomarkers`, `derived_ratios`, `derived_ratio_policy_bounds`).  

---

*End of report.*
