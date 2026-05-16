# LC-S8C Pre-Sprint Unit Policy Validation Note

**Mode:** Evidence-gathering only (no implementation).  
**Date:** 2026-05-16  
**Purpose:** Validate remaining unit-policy decisions before authoring a combined HIGH-risk governed sprint.  
**Authority inputs:** LC-S8B policy table; current `main` codebase (read-only inspection).

**Non-authority:** This note does not modify runtime, SSOT, registry, tests, or Sentinel.

---

## 1. Executive recommendation

**Recommendation:** `READY_FOR_COMBINED_HIGH_RISK_SPRINT` **only if** the sprint is structured with **mandatory internal STOP gates** (phased delivery). A single undifferentiated “implement everything” pass is **`BLOCKED_WITH_REASONS`** (see §5).

| Phase | Scope | Gate to proceed |
|-------|--------|-----------------|
| A | Label equivalence (5 rows) | LC-S8B `APPROVED_LABEL_EQUIVALENCE_ONLY` — **clear** |
| B | True conversions (Hb, Ca, corrected Ca, Mg, fT4) | Primary conversion-factor evidence per biomarker — **not present in LC-S8B** |
| C | HbA1c dual representation | Arbitration path clear; canonical flip to mmol/mol **conflicts with current Layer A/B** — policy evidenced, implementation path needs design STOP |
| D | Haematocrit L/L canonical | UK evidence clear; current Layer A normalises **to** SSOT `%` — policy evidenced, canonical-direction STOP |
| E | Sentinel lockdown | Only after A–D stable |

---

## 2. Evidence table

### 2.1 HbA1c — provisional policy validation

| Question | Finding | Evidence |
|----------|---------|----------|
| UK primary reporting unit | **IFCC mmol/mol** is the UK NHS standard since June 2009 | UK Department of Health press release (1 June 2009): HbA1c reporting changed to IFCC mmol/mol; dual % + mmol/mol reporting until 31 May 2011, then mmol/mol primary ([DHSC / WiredGov summary](https://www.wired-gov.net/wg/wg-news-1.nsf/0/699D6E15B35BD9B7802575C5004B821F?OpenDocument=)); Lab Tests Online UK “Diabetic's lab reports to have 'make over'” (April 2009) documents impending switch |
| NICE alignment | NICE recommends IFCC-standardised measurement | [NICE NG28 — Blood glucose management](https://www.nice.org.uk/guidance/ng28/chapter/blood-glucose-management): measure HbA1c using methods calibrated to IFCC standardisation |
| Legacy `%` still valid input? | **Yes historically and in some panels** — dual reporting period 2009–2011; some UK labs/patient materials still show % alongside mmol/mol; DCCT/NGSP % remains clinically familiar | DiabetesontheNet / IFCC standardisation articles; repo already holds `%` ↔ `mmol/mol` conversions in `units.yaml` lines 121–134 |
| Provisional policy support | **Supported** for mmol/mol as UK canonical analytical unit; `%` as accepted legacy input; dual input must not double-score | — |

**Provisional policy verdict:** **Evidence supports the policy direction.** Implementation is **not** a label-equivalence change — it inverts current engine behaviour (see §3).

### 2.2 Haematocrit — provisional policy validation

| Source | Haematocrit unit / range | Citation |
|--------|-------------------------|----------|
| Gloucestershire Hospitals NHS — Haematology reference ranges | Adult male **0.40–0.54 L/L**; adult female **0.37–0.47 L/L** | [Haematology reference ranges](https://www.gloshospitals.nhs.uk/our-services/services-we-offer/pathology/haematology/haematology-reference-ranges/) |
| Gloucestershire Hospitals NHS — FBC test page | HCT part of standard FBC | [Full Blood Count (FBC)](https://gloshospitals.nhs.uk/our-services/services-we-offer/pathology/tests-and-investigations/full-blood-count-fbc) |
| North Bristol NHS Trust — Severn Pathology | Adult male **0.40–0.52**; adult female **0.37–0.45** (volume fraction, L/L convention); aliases HCT, PCV | [Haematocrit test information](https://www.nbt.nhs.uk/severn-pathology/requesting/test-information/haematocrit) |

**Provisional policy verdict:** **UK NHS trusts report haematocrit as a volume fraction (L/L or decimal 0.40–0.52), not as a bare “0.438 %” on primary analytical reports.** Display as `%` is acceptable only with coherent ×100 transform of **both** value and reference range.

### 2.3 Label-equivalence rows (LC-S8B approved — unchanged)

Per LC-S8B §7: platelets, WBC, sodium, potassium, chloride — evidence already strengthened in LC-S8B. No additional validation required for this note beyond confirming **ready for Phase A**.

### 2.4 True-conversion rows — evidence status

| Biomarker | LC-S8B decision | Primary factor evidence in repo? |
|-----------|-----------------|----------------------------------|
| `hemoglobin` | `NEEDS_CONVERSION_FACTOR_VALIDATION` | Factors exist in `units.yaml` 154–164 but **not cited to UK lab primary source** in LC-S8B |
| `calcium`, `corrected_calcium` | `NEEDS_CONVERSION_FACTOR_VALIDATION` | **Missing** in `units.yaml`; candidate ~0.2495 not validated |
| `magnesium` | `NEEDS_CONVERSION_FACTOR_VALIDATION` | **Missing**; candidate ~0.4113 not validated |
| `free_t4` | `NEEDS_CONVERSION_FACTOR_VALIDATION` | **Missing**; candidate ~12.87 not validated |

**Phase B verdict:** **STOP** until primary-source conversion factors are attached to the sprint prompt.

---

## 3. Repo impact map (read-only)

### 3.1 HbA1c — current handling and duplicate-scoring risk

| Layer | File / symbol | Current behaviour | Duplicate-scoring risk |
|-------|---------------|-------------------|------------------------|
| SSOT | `backend/ssot/biomarkers.yaml` | `hba1c` unit `%` (line 196); separate `hba1c_pct` entry `%` (line 1604) | Two SSOT IDs exist |
| Aliases | `backend/ssot/biomarker_alias_registry.yaml` | `hba1c` and `hba1c_pct` are **distinct** canonical IDs | Parser can emit either key |
| Layer B arbitration | `backend/core/canonical/hba1c_layer_b_arbitration.py` | If both present: keep `hba1c`, **delete** `hba1c_pct` before unit norm (lines 39–42). If only `hba1c_pct`: promote to `hba1c` | **Mitigates duplicate** on paths that call arbitration |
| HTTP entry | `backend/app/routes/analysis.py` line 146 | Calls `arbitrate_hba1c_layer_b_input` after normalise | Protected on main API path |
| Golden / scripts | `backend/tools/run_golden_panel.py` line 337 | Calls arbitration | Protected |
| Unit norm | `backend/core/units/registry.py` | `_HBA1C_BIOMARKERS = {hba1c}`; SSOT base `%`; `mmol/mol` input **converts to %** (strict); linear IFCC→NGSP in scoring harmonisation | **Conflicts** with provisional mmol/mol canonical |
| Scoring | `backend/core/scoring/rules.py` | `_harmonise_hba1c_reference_range` converts ref to **value family**; policy bands in `scoring_policy.yaml` use `%` (lines 66–78); `hba1c_pct` in `_HBA1C_IDS` for harmonisation only | **Single score** for `hba1c` on orchestrator path; `hba1c_pct` **not** in metabolic `scoring_policy.yaml` system list (line 22) |
| Coherence guard | `registry.py` `value_and_reference_units_coherent_for_numeric_compare` | Allows `%` / `mmol/mol` pair for hba1c (lines 494–496) | OK for dual-unit refs |
| System burden | `backend/ssot/system_burden_registry.yaml` | **Both** `hba1c` (line 74) and `hba1c_pct` (line 314) registered | Secondary path if `hba1c_pct` reaches burden engine **without** arbitration |
| Knowledge Bus | `knowledge_bus/packages/pkg_kb52d_hba1c_pct_*` | Signals use `primary_metric: hba1c_pct` | **Signal evaluation risk** if panel still contains `hba1c_pct` after arbitration drops it — signals may not fire or may reference missing metric; **not** duplicate numeric scoring via `ScoringRules` |

**Duplicate scoring conclusion:**

- **Orchestrator / ScoringRules path:** Duplicate HbA1c **numeric score is already prevented** when `arbitrate_hba1c_layer_b_input` runs (tested in `backend/tests/unit/test_hba1c_governance.py`).
- **Residual risks if provisional policy adopted without follow-on:**
  1. `hba1c_pct` remains in SSOT and KB packages — not independently scored in `scoring_policy.yaml`, but still a **second analytical identity** in burden/signal graphs.
  2. Any code path that **skips** arbitration could pass both IDs to unit norm (orchestrator tests generally include arbitration).
  3. Flipping canonical to mmol/mol requires **reversing** normalisation target (currently → `%`), harmonisation defaults, scoring policy bands, and broad fixture set (`test_hba1c_governance.py`, `test_unit_registry.py::test_get_base_unit_hba1c` expects `%`).

**Provisional policy alignment gap:** Policy says mmol/mol primary for scoring/display; repo primary is **`%` after normalisation**. Resolution belongs in combined sprint Phase C with explicit STOP.

### 3.2 Haematocrit — current handling

| Layer | File / symbol | Current behaviour | Coherence / “0.438 %” risk |
|-------|---------------|-------------------|----------------------------|
| SSOT | `biomarkers.yaml` `hematocrit` | Canonical unit `%`; aliases `hct`, `pcv` (lines 660–664) | Display label from SSOT is `%` |
| Aliases | `alias_registry.py` / `biomarker_alias_registry.yaml` | `hct`, `pcv` → `hematocrit` | — |
| Unit SSOT | `units.yaml` | `L/L` defined; conversions `l_L_to_percent_hematocrit` (×100), `percent_to_l_L_hematocrit` (×0.01) lines 166–176 | Factors present |
| Layer A | `registry.py` lines 209–216, `_HEMATOCRIT_BIOMARKERS` strict | Input `L/L` → converts to SSOT base **`%`** (value 0.438 → 43.8) | **Prevents** literal `0.438 %` **if** normalisation runs |
| Layer A mixed ref | `test_lc_s8_biomarker_unit_reference_incoherence_regression.py` | L/L value + `%` ref → both converted to `%` coherently (lines 57–79) | Supports “transform together” rule |
| Layer A homogeneous L/L | Same test file lines 146–167 | L/L value + L/L ref → both → `%` | UK lab L/L panel **works** but canonical storage is still `%` |
| Scoring | `scoring_policy.yaml` `hematocrit` | Bands in `%` (36–46 etc.) lines 235–247 | Compares after Layer A |
| Frontend | LC-S8 preflight | Some display suppression only; **not** unit repair authority | Policy requires Layer A ownership |

**Provisional policy alignment gap:** Policy says UK canonical analytical unit **`L/L`**; repo SSOT and post-norm storage remain **`%`**. Accepting `%` as legacy input is compatible **only if** conversion direction is redefined when SSOT flips to L/L (invert current LC-S8 “always normalise to %” behaviour).

**“Never allow 0.438 %”:** Currently **avoided** when `apply_unit_normalisation` runs on L/L fractional input; **would recur** if raw `0.438` were labelled `%` without conversion, or if display used SSOT `%` against unconverted fractional value — Sentinel does not currently assert SSOT canonical unit UK drift (LC-S8B §12).

### 3.3 Combined sprint — file touch map (forecast)

| Area | Files likely touched (implementation sprint — not this note) |
|------|---------------------------------------------------------------|
| SSOT | `backend/ssot/biomarkers.yaml`, `units.yaml` |
| Layer A | `backend/core/units/registry.py` |
| Layer B | `backend/core/scoring/rules.py`, `hba1c_layer_b_arbitration.py` |
| Policy | `backend/ssot/scoring_policy.yaml`, `system_burden_registry.yaml`, possibly `biomarker_alias_registry.yaml` |
| KB / signals | `knowledge_bus/packages/*hba1c_pct*` (remap or deprecate) |
| Tests | `backend/tests/unit/test_hba1c_governance.py`, `test_unit_registry.py`, `test_lc_s8_biomarker_unit_reference_incoherence_regression.py`, new SSOT/Sentinel tests |
| Sentinel | `sentinel/packs/*`, new `uk_canonical_unit_ssot_drift` class |

---

## 4. Remaining blockers

| ID | Blocker | Affects phase | Resolution required |
|----|---------|---------------|---------------------|
| B1 | No primary-source validated conversion factors for Ca, corrected Ca, Mg, fT4 in LC-S8B | B | Attach NHS/lab chemistry citations per factor before implementation |
| B2 | Hb factor exists but LC-S8B held `NEEDS_CONVERSION_FACTOR_VALIDATION` | B | UK lab handbook sign-off on g/L ↔ g/dL (10×) |
| B3 | HbA1c canonical flip mmol/mol conflicts with current normalise-to-`%` and `%` scoring bands | C | Sprint sub-design: harmonisation direction, fixture replay, KB `hba1c_pct` deprecation/remap |
| B4 | `hba1c_pct` remains in SSOT + system_burden + KB packages | C | Policy: deprecate SSOT row or alias-only; remap signals to `hba1c` |
| B5 | Haematocrit L/L canonical conflicts with LC-S8 convert-to-`%` base | D | Sprint sub-design: invert canonical direction; scoring bands in L/L or governed display transform |
| B6 | Sentinel must be last | E | Gate after regression suite green for all prior phases |

---

## 5. Combined sprint feasibility

### 5.1 If sprint = single phase, all rows at once

**Verdict:** `BLOCKED_WITH_REASONS`

- True-conversion rows lack LC-S8B-mandated primary evidence (B1, B2).
- HbA1c and haematocrit policy changes are **architectural inversions**, not label equivalence (B3–B5).
- Test + Sentinel scope is large enough to fail stop conditions without phased gates.

### 5.2 If sprint = one HIGH-risk package with internal STOP gates

**Verdict:** `READY_FOR_COMBINED_HIGH_RISK_SPRINT`

**Conditions:**

1. **STOP gate 1 (mandatory):** Phase A only — five label-equivalence biomarkers; no SSOT change to HbA1c/haematocrit/true conversions until gate evidence recorded.
2. **STOP gate 2:** Phase B does not start without cited primary conversion factors per row (documented in sprint prompt, not invented).
3. **STOP gate 3:** Phase C requires written decision on: (a) mmol/mol canonical, (b) `%` input + optional display, (c) `hba1c_pct` deprecation/remap, (d) harmonisation rewrite — before any SSOT flip.
4. **STOP gate 4:** Phase D requires written decision on L/L canonical vs `%` display transform — before SSOT flip.
5. **STOP gate 5:** Sentinel `uk_canonical_unit_ssot_drift` only after full regression suite passes for implemented phases.

**Phase A alone** could ship as LOW-risk subset; bundling as HIGH-risk is appropriate because SSOT/registry/scoring/Sentinel are collectively touched.

---

## 6. Validation record

| Check | Result |
|-------|--------|
| Runtime files modified | **No** |
| Only deliverable | `docs/audit-papers/LC-S8C_pre_sprint_unit_policy_validation_note.md` |
| Implementation performed | **No** |

---

**End of note.** Author combined HIGH-risk sprint prompt only after human/GPT acceptance of STOP-gate structure and resolution of blockers B1–B5 for phases B–D.
