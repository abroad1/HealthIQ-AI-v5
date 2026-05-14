# LC-S8 — Biomarker unit / reference-range normalisation preflight audit

**Mode:** Read-only investigation (no implementation).  
**Work ID:** `LC-S8-BIOMARKER-UNIT-RANGE-NORMALISATION-QA` (preflight only).  
**Evidence:** Current merged codebase; LC-S7 docs cited below.  
**Not used:** `healthiq-analysis-2026-05-12.json` — file not present in workspace (glob search 2026-05-12); no byte-level claims from that artefact.

---

## 1. Executive summary

The biomarker pipeline applies **canonical alias mapping** and **unit normalisation** at the HTTP analysis route, then runs the orchestrator with **lab-sovereign** reference ranges copied from the post-normalised payload. **Scoring compares numeric values to numeric lab bounds without a general unit-coherence guard** (except **HbA1c**, which has explicit harmonisation). **Non-strict** biomarkers in `UnitRegistry` can **passthrough** values and reference bounds in the **input unit** while the output dict’s top-level `unit` may still reflect the **registry “base” unit** from the value leg of conversion, producing **value unit vs reference unit** splits (e.g. g/dL vs g/L, % vs L/L). **One-sided** reference ranges are copied through without numeric conversion (`elif ref_range: ref_converted = dict(ref_range)`), which can preserve **original lab units** beside a converted value. The orchestrator’s DTO builder reads **reference range units from `input_reference_ranges`** (preserved from the panel dict) while status uses **`frontend_status_from_lab_reference`**, which is **unit-agnostic** — so **status and score can reflect numerically wrong comparisons** when units disagree. LC-S7 added **frontend-only** suppression of clearly incompatible range rows (`BiomarkerDials.tsx`); sprint docs state **backend normalisation remains future work**. **Risk for LC-S8 is HIGH** because fixes touch `backend/core/units/`, `backend/core/pipeline/orchestrator.py`, `backend/core/scoring/`, and `backend/ssot/` surfaces.

---

## 2. Launch-readiness verdict

**Not launch-ready** for analytical trust on biomarker cards where lab payloads mix units or use one-sided ranges, until backend unit/range coherence is proven. LC-S7 mitigated **display** of some bad pairs only; it did not certify scoring or status correctness under unit mismatch.

---

## 3. End-to-end biomarker pipeline map

| Stage | File path | Function / class | Primary inputs | Primary outputs | Where value, unit, ref min/max/unit, score, status, interpretation are set |
|-------|-----------|-------------------|----------------|-----------------|-------------------------------------------------------------------------------|
| 1. Upload / parsed API body | `backend/app/routes/analysis.py` | Route handler (analysis start) | `request.biomarkers`, `request.user`, questionnaire | Normalised biomarkers + DTO for storage | Incoming dict per marker: `value`, `unit`, `reference_range` (lines 131–178 area). |
| 2. Canonical ID mapping | `backend/core/canonical/normalize.py` | `normalize_biomarkers_with_metadata` → `BiomarkerNormalizer.normalize_biomarkers` | Raw keys / dicts | Canonical keys, `BiomarkerValue` with `value`, `unit`, `reference_range` | Alias resolution lines 56–70; dict branch lines 87–126; output dict lines 244–249. |
| 2b (same module, orchestrator re-entry) | `backend/core/canonical/normalize.py` | `BiomarkerNormalizer.normalize_biomarkers` | Post–unit-normalisation dicts | `BiomarkerPanel` | Reads `value["unit"]` if present (lines 88–91); copies `reference_range` including `unit` (lines 93–106). |
| 3. Unit normalisation | `backend/core/units/registry.py` | `apply_unit_normalisation` | Dict of marker → `{value, unit, reference_range?}` | Same keys with converted `value`, `unit`, `reference_range`, audit keys | Value conversion lines 355–359; reference handling lines 363–399; passthrough when no factor lines 241–245; one-sided passthrough lines 398–399; output assembly lines 401–420. |
| 3b HbA1c id arbitration (pre-normalisation) | `backend/core/canonical/hba1c_layer_b_arbitration.py` (imported from route) | `arbitrate_hba1c_layer_b_input` | Normalised biomarkers dict | Same dict with single HbA1c id | Docstring states ordering vs normalisation (`hba1c_layer_b_arbitration.py` lines 4–6 in prior read; route call `analysis.py` line 146). |
| 4. Route → orchestrator handoff | `backend/app/routes/analysis.py` | After `apply_unit_normalisation` | `normalized` dict | `orchestrator.run(...)` | Injects `__unit_normalisation_meta__` (key `UNIT_NORMALISATION_META_KEY`) lines 160–164; `run` pops it `orchestrator.py` lines 1017–1023. |
| 5. Reference range capture for engine | `backend/core/pipeline/orchestrator.py` | `run` Step 1 | `filtered_biomarkers` | `simple_biomarkers`, `input_reference_ranges` | Extracts numeric value + ref dict from each marker dict lines 1068–1090. |
| 5b Derived ratios | `backend/core/analytics/ratio_registry.py` | `compute` | Panel dict (post-normalisation) | `derived` entries, version metadata | States “Runs after unit normalisation; uses base-unit values only” lines 6–8; `_derived_unit` lines 75–77; `DERIVED_IDS` lines 28–32. |
| 6. Context | `backend/core/pipeline/orchestrator.py` | `create_analysis_context` | `raw_biomarkers=filtered_biomarkers` | `AnalysisContext` | Called at lines 1296–1305 with `assume_canonical=True`. |
| 7. Scoring | `backend/core/scoring/engine.py` | `_score_health_system` → `ScoringRules.calculate_biomarker_score` | `BiomarkerValue` + `input_reference_ranges` | `score`, `score_range`, `unscored_reason` | `value_unit` from `val.unit` lines 198–212; rules entry `rules.py` lines 256–310. |
| 8. API result assembly (biomarker rows) | `backend/core/pipeline/orchestrator.py` | Step 6 DTO build | `biomarker_score`, `context.biomarker_panel`, `input_reference_ranges` | `BiomarkerScoreDTO` | Unit from panel dict / resolver lines 1836–1848; ref from `input_reference_ranges` lines 1850–1872; status `frontend_status_from_lab_reference` lines 1884–1890; interpretation lines 1900–1917. |
| 9. Frontend result type / mapping | `frontend/app/(app)/results/page.tsx` | `biomarkerDialData` construction | API `biomarkers[]` | `BiomarkerDialEntry` | Maps `value`, `unit`, `reference_range` fields lines 498–511. |
| 10. Biomarker card display | `frontend/app/components/biomarkers/BiomarkerDials.tsx` | `BiomarkerDials` | `biomarkerDialData` | Rendered cards | `shouldSuppressReferenceRange` lines 92–105; value line + conditional range lines 343–377; dial `calculateDialValue` lines 167–183, usage line 339. |

---

## 4. Known defect tracing

### 4.1 Haemoglobin (value `144`, display `g/dL`, reference `130–175 g/L`)

**Likely root-cause category:** **Backend unit normalisation + lab-range preservation** (not frontend parsing).

**Evidence:**

- `apply_unit_normalisation` does **not** treat haemoglobin as a **strict-conversion** biomarker (`_STRICT_CONVERSION_BIOMARKERS` omits haemoglobin) — see `registry.py` lines 60–78 and passthrough branch lines 241–245.
- When `ref_unit != base_unit` from the **value** conversion, reference min/max are passed through `_convert_with_explicit_unit`; if **no factor** exists, **numeric bounds are unchanged** but `ref_converted["unit"]` is set to the **value leg’s `base_unit`** (`registry.py` lines 378–395). That can yield **g/L magnitudes** with a **g/dL label** (or the inverse pattern depending on input order), i.e. **incoherent pairs**.
- **One-sided** ranges skip the two-sided conversion block: `has_ref_bounds` requires **both** min and max numeric (`registry.py` line 327); otherwise `ref_converted = dict(ref_range)` preserves the **original** range dict (`registry.py` lines 398–399), while the value may still be normalised — explicit split risk.
- SSOT declares haemoglobin `unit: g/dL` (`backend/ssot/biomarkers.yaml` lines 644–648).
- Frontend **passes through** API fields (`results/page.tsx` lines 498–511); LC-S7 only hides some incompatible pairs in display (`BiomarkerDials.tsx` lines 92–105).

**Was the upload `144 g/L` or `144 g/dL`?** **Cannot be determined** from repo alone without the stored request JSON.

**Is scoring using the value “correctly”?** **Unknown without the payload**; if bounds and value are in **different mass/volume scales** but compared as floats, **scoring and status are not trustworthy** (`rules.py` uses raw numeric min/max in `_calculate_score_from_range`, lines 312–328).

---

### 4.2 Haematocrit (value `0.4`, display `%`, reference `0.35–0.48 L/L`)

**Likely root-cause category:** **Same class as haemoglobin** — fraction vs percent vs L/L families without a governed conversion path in `UnitRegistry` for this marker; SSOT unit is `%` (`biomarkers.yaml` lines 659–664).

**Evidence:** Passthrough and reference-conversion structure identical to §4.1 (`registry.py` lines 216–252, 363–399). **Display unit** on the card comes from API `biomarker.unit` (`results/page.tsx` line 500). **Range unit** comes from API `reference_range.unit` (lines 504–508).

**Should display be `0.438 L/L` or `43.8%`?** **Product/clinical policy not encoded** in repo beyond SSOT `unit: '%'` for `hematocrit` (`biomarkers.yaml` line 663).

---

### 4.3 HbA1c (`%` vs mmol/mol)

**Likely root-cause category:** **Partially governed** — scoring has explicit harmonisation; display may still be inconsistent if API emits mismatched artefacts before harmonisation or for unscored paths.

**Evidence:**

- `ScoringRules._harmonise_hba1c_reference_range` converts bounds between `%` and `mmol/mol` when families differ (`rules.py` lines 203–254).
- Mismatch that cannot be harmonised yields `UNSCORED_REASON_HBA1C_UNIT_MISMATCH` (`rules.py` lines 47–48, 279–282).
- DTO interpretation maps that reason to explicit copy (`orchestrator.py` lines 1907–1911).
- LC-S7 sprint: backend unit/range normalisation still **future work** (`docs/sprints/LC-S7_consumer_boundary_and_biomarker_display_qa_completion_2026-05.md` lines 11, 36–38).

**Dual-unit support:** **Scoring path yes** (harmonise); **general display policy** beyond FE suppression list **not documented** as a single authority.

---

### 4.4 Testosterone — “Not scored - no reference range available”

**Likely root-cause category:** **Reference-range lookup / payload completeness / lab-range validity**, not frontend mapping.

**Evidence:**

- Non-derived biomarkers **must** use lab `input_reference_range`; else `calculate_biomarker_score` returns `(0.0, CRITICAL, UNSCORED_REASON)` (`rules.py` lines 297–299). `UNSCORED_REASON` is policy-driven default `missing_lab_reference_range` (`rules.py` lines 40–44).
- Orchestrator builds `input_reference_ranges` only when ref dict has **at least one** numeric min or max and min \< max when both present (`orchestrator.py` lines 1073–1089).
- DTO interpretation `"Not scored - no reference range available"` when `ur` empty, status `unknown`, and no numeric bounds (`orchestrator.py` lines 1900–1917).
- SSOT canonical unit for total testosterone is `nmol/L` (`biomarkers.yaml` lines 1102–1103); if upload used **unsupported unit** without conversion, ingestion may **400** at `apply_unit_normalisation` (`analysis.py` lines 149–158) — if request succeeded, **missing or invalid ref** is the plausible branch for the quoted string.

**Total vs free vs ratio:** `testosterone_free_testosterone_ratio` is in `DERIVED_IDS` (`ratio_registry.py` lines 28–31, 51); policy bounds exist (`scoring_policy.yaml` lines 322–327). Confusion between **total** and **free** keys would surface as **missing rule biomarker** in scoring (`engine.py` lines 193–196) or wrong ratio inputs — distinct from the **exact** “no reference range” string unless ref truly absent on the scored id.

---

### 4.5 Ratios (`tc_hdl_ratio`, `tg_hdl_ratio`, `ldl_hdl_ratio`, `apob_apoa1_ratio`, `urea_creatinine_ratio`, `testosterone_free_testosterone_ratio`)

**Unitless?** **Intended yes** for ratio markers: SSOT `unit: ratio` for `tc_hdl_ratio` (`biomarkers.yaml` lines 66–68); `_derived_unit` returns `"ratio"` except `non_hdl_cholesterol` (`ratio_registry.py` lines 75–77). Policy table stores `unit: "ratio"` for listed ratios (`scoring_policy.yaml` lines 285–327). **`non_hdl_cholesterol` is explicitly `mmol/L`** in policy (lines 304–309) — not unitless.

**mmol/L on ratio bounds?** **Not for named ratios** in current `derived_ratio_policy_bounds`; **yes for `non_hdl_cholesterol`** (concentration surrogate).

**Computed vs lab-supplied:** `ratio_registry.py` documents lab-supplied wins (`ratio_registry.py` lines 70–72, `compute` not fully quoted here); orchestrator merges policy ref for ratios when lab ref invalid (`orchestrator.py` grep hits 1232–1272 region — logic for ratio id injection).

---

## 5. Whole-codebase unit/range scan

**Method:** Static architecture review (no automated multi-artifact diff of all SSOT markers vs policy). **Confirmed high-risk patterns:**

| Pattern | Mechanism | Likely affected markers (non-exhaustive) |
|--------|-----------|-------------------------------------------|
| Passthrough conversion | Biomarker **not** in `_STRICT_CONVERSION_BIOMARKERS` (`registry.py` lines 70–78, 241–245) | Any marker lacking a YAML factor to SSOT base unit — **includes CBC-style markers** (haemoglobin, haematocrit) and many others not in the strict set. |
| Ref unit stamped from value `base_unit` while bounds passthrough | `ref_converted` uses `min_conv`/`max_conv` but `unit: base_unit` from value path (`registry.py` lines 386–395) | Markers where value and reference start in **different compatible families** without conversion factors. |
| One-sided ref preserves raw dict | `has_ref_bounds` false → `dict(ref_range)` (`registry.py` lines 327, 398–399) | Any marker with only min **or** max in lab data. |
| Scoring ignores unit beyond HbA1c | Numeric compare only (`rules.py` lines 285–287, 312–328) | All non-HbA1c markers when ref/value units drift. |
| Status unit-agnostic | `frontend_status_from_lab_reference` (`primitives.py` lines 96–108) | Same set — **status can look “normal”** on incoherent numerics. |
| Derived ratio policy unit mismatch test | Golden runner documents behaviour (`test_golden_panel_runner.py` around `test_derived_policy_unit_mismatch_is_unscored_with_deterministic_reason` per grep) | Derived markers when policy `unit` does not match computed dimension — **class exists in tests**, not in Sentinel pack list. |

---

## 6. Unit normalisation architecture

| Question | Answer (from code) |
|----------|---------------------|
| Unit registry? | Yes — `backend/core/units/registry.py`, loads `backend/ssot/units.yaml` (`registry.py` lines 102–109). |
| Conversion utilities? | `UnitRegistry._get_conversion_factor`, `_convert_with_explicit_unit`, `apply_unit_normalisation` (`registry.py` lines 216–252, 280+). |
| Canonical unit policy? | `UnitRegistry.get_base_unit` reads `backend/ssot/biomarkers.yaml` (`registry.py` lines 112–119). |
| Lab reference policy? | Docstring: “Lab-provided reference ranges remain sovereign” (`registry.py` lines 6–7); orchestrator: “Lab-Range Sovereignty” comment (`orchestrator.py` lines 1850–1851). |
| Ratio registry? | `backend/core/analytics/ratio_registry.py` (`DERIVED_IDS`, `compute`). |
| Derived marker registry? | Same file; orchestrator Step 1.5 (`orchestrator.py` line 1097). |
| Parser-level unit mapping? | **Out of scope of this audit file depth**; HTTP route assumes structured JSON already (`analysis.py`). |
| Display-unit mapping? | **Frontend:** LC-S7 suppression only (`BiomarkerDials.tsx` lines 92–105). |

**Authoritative sources:**

- **Canonical / base unit (SSOT):** `backend/ssot/biomarkers.yaml` via `UnitRegistry._load_biomarker_base_units` (`registry.py` lines 112–119).
- **Conversions:** `backend/ssot/units.yaml` (`registry.py` lines 102–109).
- **Reference range numeric bounds for scoring:** Lab dict on payload, carried into `input_reference_ranges` (`orchestrator.py` lines 1066–1090); **not** SSOT fallback for non-derived markers (`rules.py` lines 297–299).
- **Derived ratio fallback bounds:** `backend/ssot/scoring_policy.yaml` `derived_ratio_policy_bounds` (`rules.py` lines 22–31).

**Governed rule convert vs raw:** **Strict biomarkers** must convert or error (`registry.py` lines 246–251). **Non-strict** may **passthrough** numeric with input unit (`registry.py` lines 241–245). **One-sided** refs copy raw (`registry.py` lines 398–399).

---

## 7. Scoring safety assessment

| Marker / issue | Display-only? | Scoring-impacting? | Ref-lookup? | Status / interpretation? | Evidence |
|----------------|---------------|--------------------|-------------|---------------------------|----------|
| Haemoglobin unit split | FE can hide range text (LC-S7) | **Yes, plausible** — same floats used in `calculate_biomarker_score` | If ref omitted → unscored | Misleading if `position_in_range` uses wrong scale | `rules.py` 285–287; `BiomarkerDials.tsx` 92–105 |
| Haematocrit | Same | **Yes, plausible** | Same | Same | Same |
| HbA1c | Partially masked by harmonisation / FE | **Reduced** when harmonisation succeeds; **unscored** on hard mismatch | Harmonise path | Explicit mismatch copy | `rules.py` 203–254, 279–282; `orchestrator.py` 1907–1911 |
| Testosterone “no reference range” | N/A | **Unscored** when lab range missing/invalid | **Yes** | String from DTO branch | `rules.py` 297–299; `orchestrator.py` 1912–1917 |
| Ratios | Label/unit mostly policy-driven | Policy bounds used when lab missing (`rules.py` 301–307) | Orchestrator ratio merge | — | `scoring_policy.yaml` 285–327 |

---

## 8. Frontend LC-S7 defensive display assessment

**Where:** `frontend/app/components/biomarkers/BiomarkerDials.tsx` — `shouldSuppressReferenceRange` (lines 92–105); used when rendering range (lines 343–371) and amber note (lines 372–376).

**What it suppresses:** Numeric min/max line when known-bad **pairs** (g/dL vs g/L; % vs L/L; % vs mmol/mol) match.

**Safety:** Avoids showing an **obviously** incoherent band; shows neutral guidance (lines 372–376).

**Masking scoring defects?** **Yes.** Backend may still score using incoherent numerics; UI may show **no range** while a **non-zero score** exists — user cannot see the band that justified the score. Sprint explicitly scoped FE as non-clinical (`docs/sprints/LC-S7_consumer_boundary_and_biomarker_display_qa_completion_2026-05.md` lines 36–38).

**Dial caveat:** `calculateDialValue` uses `referenceRange` when `score` is absent (`BiomarkerDials.tsx` lines 167–183) but **does not** receive `hideRange`; if a future payload had `score` undefined with numeric range, dial could still use mismatched bounds. Current path often has `score` as number (including `0`).

---

## 9. Existing test / Sentinel coverage

**Unit normalisation:** `backend/tests/unit/test_unit_registry.py` (e.g. ref mismatch rejection cases per grep hit at line 210+). **Strict vs non-strict** behaviour is defined in production code (`registry.py` lines 70–78, 241–251) but **haemoglobin g/L vs g/dL end-to-end** is not highlighted in grep hits as a dedicated case.

**Scoring rules:** `backend/tests/unit/test_scoring_rules.py` includes haemoglobin with lab refs in **consistent** units (grep lines 202–205).

**Orchestrator integration:** Fixtures often use **aligned** `g/L` across value and ref (`ab_full_panel_with_ranges.json` per grep).

**Sentinel:** `sentinel/packs/escaped_defects_v1.json` lists classes such as `ggt_alias_miss`, `slug_leakage`, `wave1_contradiction` (lines 5–37) — **no** `biomarker_unit_range` defect class.

**Why UAT issues escaped:** Tests and fixtures **over-represent coherent units**; Sentinel **does not** encode unit-range incoherence; **non-strict passthrough** is a deliberate code path (`registry.py` lines 241–245); LC-S7 **explicitly** deferred backend normalisation (`docs/sprints/LC-S7_consumer_boundary_and_biomarker_display_qa_completion_2026-05.md` lines 11, 36–38).

---

## 10. Similar undetected issue risk

**High** for any biomarker where:

- Lab sends **alternate unit** not in conversion matrix.
- **One-sided** reference ranges are common.
- **Sex/age-specific** ranges are flattened to numbers without unit harmonisation (not audited deeply here).

---

## 11. Recommended LC-S8 implementation scope

**Recommended:** **Option E — mixed backend + frontend package**, sequenced **backend first** (normalisation, ref coherence, scoring guards), then **frontend** (display policy, optional warnings, dial coherence).

- **Do not** rely on **Option A alone** — sprint already states limits (`docs/sprints/LC-S7_consumer_boundary_and_biomarker_display_qa_completion_2026-05.md` lines 36–38).

---

## 12. Expected files to touch (implementation phase — not done here)

- `backend/core/units/registry.py`, `backend/ssot/units.yaml`, `backend/ssot/biomarkers.yaml`
- `backend/core/pipeline/orchestrator.py` (DTO ref sourcing vs panel)
- `backend/core/scoring/rules.py`, `backend/core/scoring/engine.py`, possibly `backend/core/analytics/primitives.py`
- `backend/core/analytics/ratio_registry.py` (only if ratio unit policy changes)
- `frontend/app/components/biomarkers/BiomarkerDials.tsx`, `frontend/app/(app)/results/page.tsx`
- Tests under `backend/tests/unit/`, integration tests, optional **new** Sentinel pack JSON + regression test

---

## 13. Risk classification

**HIGH** for LC-S8 as scoped: touches **`backend/core/units/`**, **`backend/core/pipeline/orchestrator.py`**, **`backend/core/scoring/`**, **`backend/ssot/`**, canonicalisation-adjacent behaviour, scoring, and reference-range logic — matches the user’s HIGH definition.

---

## 14. Stop conditions for implementation

- Any change that **scores differently** on historical fixtures without explicit **migration / replay** policy.
- Introducing **silent** unit coercion without audit fields on DTO.
- Frontend-only “fix” that **invents** clinical conversion (violates frontend shell rules per `AGENTS.md` and LC-S7 notes).

---

## 15. Recommended tests and Sentinel candidates

1. **Matrix tests** for `apply_unit_normalisation`: value + ref in **g/L**, **g/dL**, one-sided, missing ref unit with explicit value unit — assert **coherent** `(value, unit, ref.min, ref.max, ref.unit)` or deterministic **400**.
2. **Orchestrator DTO tests:** `input_reference_ranges` unit matches panel unit after normalisation.
3. **Scoring tests:** mismatched mass/volume → **unscored** or **converted**, never silent wrong score (policy decision).
4. **HbA1c:** already partially covered — extend edge cases.
5. **Ratios:** lab-supplied vs computed; policy `unit: ratio` vs displayed `reference_range.unit`.
6. **New Sentinel defect class** (proposal): `biomarker_value_reference_unit_incoherence` with deterministic payload fingerprint — **backend pytest** primary; optional FE snapshot for suppressed range.

---

## 16. Open questions / blockers

1. **Authoritative replay JSON** for the reported analysis (`healthiq-analysis-2026-05-12.json`) — **not in repo**; needed to confirm exact payload units.
2. **Clinical policy** for haematocrit display (% vs L/L) vs SSOT `%`.
3. Whether **old stored analyses** must replay through a **versioned normaliser** (migration scope).

---

## 17. Files inspected

- `backend/app/routes/analysis.py`
- `backend/core/units/registry.py`
- `backend/core/canonical/normalize.py`
- `backend/core/canonical/hba1c_layer_b_arbitration.py` (import / ordering reference via route)
- `backend/core/pipeline/orchestrator.py`
- `backend/core/scoring/rules.py`
- `backend/core/scoring/engine.py`
- `backend/core/analytics/primitives.py`
- `backend/core/analytics/ratio_registry.py`
- `backend/ssot/biomarkers.yaml`
- `backend/ssot/units.yaml` (partial via registry)
- `backend/ssot/scoring_policy.yaml`
- `frontend/app/(app)/results/page.tsx`
- `frontend/app/components/biomarkers/BiomarkerDials.tsx`
- `backend/tests/unit/test_unit_registry.py` (grep-led)
- `backend/tests/unit/test_scoring_rules.py` (grep-led)
- `sentinel/packs/escaped_defects_v1.json`
- `docs/testing/LC-S7_preflight_triage_post_LC-S6_UAT.md`
- `docs/sprints/LC-S7_consumer_boundary_and_biomarker_display_qa_completion_2026-05.md`
- `AGENTS.md` (governance scope)

---

## Appendix — User-requested closing summary

| Item | Result |
|------|--------|
| **Files inspected** | See §17. |
| **File created** | `docs/audit-papers/LC-S8_biomarker_unit_range_normalisation_preflight.md` |
| **Non-audit files modified?** | **No** |
| **Root-cause category (known issues)** | Haemoglobin / haematocrit: **backend unit normalisation + lab ref handling**; HbA1c: **governed in scoring**, gaps possible at API edges; Testosterone message: **missing/invalid lab ref or lookup**; Ratios: mostly **policy/registry**, `non_hdl_cholesterol` is **concentration**. |
| **Scoring may be affected?** | **Yes** for unit mismatches (non-HbA1c); not display-only. |
| **Similar issues elsewhere?** | **Yes** — all **non-strict** markers and **one-sided** refs. |
| **Recommended strategy** | **Option E** (backend-first, then FE). |
| **Recommended risk level** | **HIGH** |
