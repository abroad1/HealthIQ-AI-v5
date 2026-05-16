# LC-S8B — UK Canonical Unit Policy Validation

**Work ID:** `LC-S8B`  
**Branch:** `launch-core/lc-s8b-uk-canonical-unit-policy-validation`  
**Date:** 2026-05-16  
**Change type:** CONTENT (policy validation only — no runtime changes)  
**Risk:** HIGH (governs downstream SSOT implementation; this sprint does not modify runtime)

---

## 1. Executive summary

HealthIQ AI does not yet have a locked, evidence-backed UK-first canonical biomarker unit policy enforced consistently across SSOT, the unit registry, Layer A normalisation, Layer B scoring, Layer C display, tests, and Sentinel. LC-S8A documented the defect inventory; **this document is the decision table that authorises later implementation sprints (LC-S8C–LC-S8F)**.

**Baseline confirmed:** Unresolved UK/SI canonical-unit policy issues remain in `backend/ssot/biomarkers.yaml` (US-style or ambiguous canonical units for cell counts, haemoglobin, haematocrit, electrolytes, minerals, thyroid, and HbA1c).

**Policy outcomes at a glance:**

| Category | Count (this table) | Primary follow-on |
|----------|-------------------|-------------------|
| `APPROVED_LABEL_EQUIVALENCE_ONLY` | 5 rows | LC-S8C |
| `NEEDS_CONVERSION_FACTOR_VALIDATION` | 5 rows | LC-S8D |
| `NEEDS_POLICY_DECISION` | 3 rows | LC-S8E / LC-S8F |
| `NO_CHANGE_REQUIRED` | 16 rows | — |
| `DEFER_NOT_LAUNCH_CRITICAL` | 2 rows | Post-launch |
| **Total (§6 table)** | **31 rows** | — |

**Launch-critical blockers for UK analytical accuracy:** calcium, corrected calcium, magnesium, and free T4 must not be implemented until conversion factors are validated from primary clinical/laboratory sources (LC-S8D).

---

## 2. Current defect statement

The immediate user-visible trigger (platelets displayed as `225 K/μL` when the UK lab reported `225 10^9/L`) is a **symptom** of SSOT canonical units that are not UK-first. The LC-S8 scoring guard correctly blocks **mixed value/reference units** at scoring time but does **not** detect SSOT canonical label drift or missing true-scale conversions.

**Confirmed unresolved issues (SSOT canonical units, 2026-05-16):**

| Defect class | Biomarkers | SSOT evidence |
|--------------|------------|---------------|
| US cell-count label | `platelets`, `white_blood_cells` | `K/μL` at `biomarkers.yaml` lines 679, 694 |
| US mass concentration | `hemoglobin` | `g/dL` line 649 |
| Fraction vs percent ambiguity | `hematocrit` | `%` line 664 |
| US mineral concentration | `calcium`, `corrected_calcium`, `magnesium` | `mg/dL` lines 747, 761, 817 |
| US thyroid concentration | `free_t4` | `ng/dL` line 603 |
| US electrolyte label | `sodium`, `potassium`, `chloride` | `mEq/L` lines 775, 789, 803 |
| Dual HbA1c representation | `hba1c`, `hba1c_pct` | `%` lines 196, 1604 |

**Missing registry conversions (not invented here):** `units.yaml` has no calcium/magnesium/free T4 `mg/dL`↔`mmol/L` or `ng/dL`↔`pmol/L` blocks; no `K/μL`↔`10^9/L` equivalence; no `mEq/L`↔`mmol/L` registration (`units.yaml` lines 44–49, 83–177).

---

## 3. Authority files reviewed

| File | Resolved path | Role |
|------|---------------|------|
| ADR-001 Platform non-negotiables | `architecture/ADR-001-platform-non-negotiables.md` | SSOT invariants |
| ADR-002 Deterministic engine | `architecture/ADR-002-deterministic-analysis-engine.md` | Layer A/B/C; g/L for proteins (line 51–52) |
| Master PRD v5.2 | `architecture/Master_PRD_v5.2.md` | Product architecture (relocated from repo root per CLAUDE.md) |
| Biomarker SSOT | `backend/ssot/biomarkers.yaml` | Canonical IDs, aliases, per-marker `unit:` |
| Unit SSOT | `backend/ssot/units.yaml` | Unit definitions and conversion factors |
| Unit registry | `backend/core/units/registry.py` | Runtime loader, equivalence, strict sets |
| LC-S8 preflight | `docs/audit-papers/LC-S8_biomarker_unit_range_normalisation_preflight.md` | Pipeline defect map |
| LC-S8A audit | `docs/audit-papers/LC-S8A_uk_canonical_unit_ssot_lockdown_audit.md` | Defect enumeration (input only, not implementation authority) |

**Preflight commands (recorded):**

```text
Branch: launch-core/lc-s8b-uk-canonical-unit-policy-validation
HEAD:   (post kernel start on sprint branch)
Porcelain: clean at kernel start
Stash:   stash@{0} retained — unrelated LC-S1 on feature/questionnaire-visual-redesign (not triaged into this sprint)
```

---

## 4. Baseline SSOT unit inventory (UK-policy-relevant subset)

| Biomarker ID | SSOT `unit:` | Line | UK/SI expectation |
|--------------|-------------|------|-------------------|
| `hemoglobin` | `g/dL` | 649 | `g/L` |
| `hematocrit` | `%` | 664 | `L/L` analytical; `%` display common |
| `white_blood_cells` | `K/μL` | 679 | `10^9/L` |
| `platelets` | `K/μL` | 694 | `10^9/L` |
| `rbc` | `10^12/L` | 829 | `10^12/L` ✓ |
| `neutrophils` | `10^9/L` | 417 | ✓ |
| `lymphocytes` | `10^9/L` | 432 | ✓ |
| `neutrophils_abs` | `10^9/L` | 507 | ✓ |
| `lymphocytes_abs` | `10^9/L` | 477 | ✓ |
| `monocytes_abs` | `10^9/L` | 492 | ✓ |
| `eosinophils_abs` | `10^9/L` | 462 | ✓ |
| `basophils_abs` | `10^9/L` | 447 | ✓ |
| `calcium` | `mg/dL` | 747 | `mmol/L` |
| `corrected_calcium` | `mg/dL` | 761 | `mmol/L` |
| `magnesium` | `mg/dL` | 817 | `mmol/L` |
| `sodium` | `mEq/L` | 775 | `mmol/L` (label) |
| `potassium` | `mEq/L` | 789 | `mmol/L` (label) |
| `chloride` | `mEq/L` | 803 | `mmol/L` (label) |
| `free_t4` | `ng/dL` | 603 | `pmol/L` |
| `tsh` | `mIU/L` | 633 | ✓ |
| `hba1c` | `%` | 196 | `mmol/mol` (IFCC UK standard) |
| `hba1c_pct` | `%` | 1604 | dual entry — policy required |
| `glucose` | `mmol/L` | 179 | ✓ |
| `total_cholesterol` | `mmol/L` | 7 | ✓ |
| `ldl_cholesterol` | `mmol/L` | 23 | ✓ |
| `hdl_cholesterol` | `mmol/L` | 39 | ✓ |
| `triglycerides` | `mmol/L` | 55 | ✓ |
| `creatinine` | `µmol/L` | 283 | ✓ |
| `urea` | `mmol/L` | 316 | ✓ |

**Not present in SSOT:** `red_blood_cells` (canonical ID is `rbc`); `haematocrit` (canonical ID is `hematocrit`); `bicarbonate` / `phosphate` as standalone markers.

---

## 5. Evidence methodology

1. **Primary preference:** UK NHS laboratory reporting conventions, NHS Trust pathology handbooks, NICE guidance, UK NEQAS / professional haematology or clinical chemistry standards, and SI/BIPM unit definitions.
2. **Project inputs:** Current `biomarkers.yaml`, `units.yaml`, `registry.py` — read for baseline only.
3. **LC-S8A:** Used to identify which rows to evaluate; **not** cited as sole evidence for any approval.
4. **Conversion factors:** No factor is invented in this document. Illustrative factors from LC-S8A are noted only as *candidates* pending primary-source validation.
5. **Row status:** Every row has an explicit `Decision`. Rows without primary-source conversion validation use `NEEDS_CONVERSION_FACTOR_VALIDATION` or `NEEDS_POLICY_DECISION`.

---

## 6. Full policy-validation table

| Biomarker ID | Display name | Current SSOT unit | Current accepted input units / aliases | Proposed UK canonical analytical unit | Proposed UK launch display unit | Evidence source(s) | Conversion type | Risk | Decision | Rationale | Follow-on sprint |
| ------------ | ------------ | ----------------- | -------------------------------------- | ------------------------------------- | ------------------------------- | ------------------ | --------------- | ---- | -------- | --------- | ---------------- |
| `platelets` | Platelet count | `K/μL` | `plt`, `platelet_count`; UK labs commonly `10^9/L`, `x10^9/L` | `10^9/L` | `10^9/L` | **UK display:** UK NEQAS Haematology EQA and NHS pathology data definitions report platelet count as ×10⁹/L (not K/μL). **Equivalence proof:** SI/BIPM volume: 1 L = 10⁶ μL; “K/μL” = 10³ cells·μL⁻¹ → 10³ × 10⁶ cells·L⁻¹ = 10⁹ cells·L⁻¹; numeric factor 1.0. **Professional:** BCSH/RCPath UK FBC reporting aligns with SI multiples (10⁹/L). | `LABEL_EQUIVALENCE_1_TO_1` | LOW | `APPROVED_LABEL_EQUIVALENCE_ONLY` | UK launch display must be 10⁹/L; K/μL is a US customary label for the same magnitude. No scale conversion—register equivalence before SSOT relabel. | LC-S8C |
| `white_blood_cells` | White blood cell count | `K/μL` | `wbc`, `leukocytes`; UK `10^9/L` | `10^9/L` | `10^9/L` | **UK display:** NHS/UK NEQAS FBC programmes report total WBC as ×10⁹/L (leucocyte count). **Equivalence proof:** Identical dimensional reduction to platelets: 1 K/μL = 1×10⁹/L (10³/μL × 10⁶ μL/L). **Professional:** BCSH standard UK full blood count reporting uses 10⁹/L for total white cell count. | `LABEL_EQUIVALENCE_1_TO_1` | LOW | `APPROVED_LABEL_EQUIVALENCE_ONLY` | Same 1:1 label equivalence class as platelets; not a separate conversion policy. | LC-S8C |
| `neutrophils` | Neutrophils (absolute) | `10^9/L` | `neutrophil_count`, `neutrophils_(venous)` | `10^9/L` | `10^9/L` | UK FBC standard unit for absolute differential | `NO_CHANGE_REQUIRED` | LOW | `NO_CHANGE_REQUIRED` | Already UK/SI canonical. | — |
| `lymphocytes` | Lymphocytes (absolute) | `10^9/L` | `lymphocyte_count`, `lymphocytes_(venous)` | `10^9/L` | `10^9/L` | UK FBC standard | `NO_CHANGE_REQUIRED` | LOW | `NO_CHANGE_REQUIRED` | Already correct. | — |
| `neutrophils_abs` | Neutrophils absolute | `10^9/L` | `neutrophil_(neu_#)`, etc. | `10^9/L` | `10^9/L` | UK FBC | `NO_CHANGE_REQUIRED` | LOW | `NO_CHANGE_REQUIRED` | Already correct. | — |
| `lymphocytes_abs` | Lymphocytes absolute | `10^9/L` | `lymphocyte_(lym_#)`, etc. | `10^9/L` | `10^9/L` | UK FBC | `NO_CHANGE_REQUIRED` | LOW | `NO_CHANGE_REQUIRED` | Already correct. | — |
| `monocytes_abs` | Monocytes absolute | `10^9/L` | `monocyte_(mon_#)`, etc. | `10^9/L` | `10^9/L` | UK FBC | `NO_CHANGE_REQUIRED` | LOW | `NO_CHANGE_REQUIRED` | Already correct. | — |
| `eosinophils_abs` | Eosinophils absolute | `10^9/L` | `eosinophils_(eos_#)`, etc. | `10^9/L` | `10^9/L` | UK FBC | `NO_CHANGE_REQUIRED` | LOW | `NO_CHANGE_REQUIRED` | Already correct. | — |
| `basophils_abs` | Basophils absolute | `10^9/L` | `basophils_(bas_#)`, etc. | `10^9/L` | `10^9/L` | UK FBC | `NO_CHANGE_REQUIRED` | LOW | `NO_CHANGE_REQUIRED` | Already correct. | — |
| `rbc` | Red blood cell count | `10^12/L` | (none listed) | `10^12/L` | `10^12/L` | UK reports RBC as ×10¹²/L | `NO_CHANGE_REQUIRED` | LOW | `NO_CHANGE_REQUIRED` | Canonical ID `rbc` (not `red_blood_cells`). Already UK/SI. | — |
| `hemoglobin` | Haemoglobin | `g/dL` | `hgb`, `hb`, `haemoglobin`; UK labs `g/L` | `g/L` | `g/L` (pending LC-S8D validation) | ADR-002 Layer A: g/L for proteins; NHS/UK labs report haemoglobin in g/L; conversion exists in `units.yaml` lines 154–164 (factor 10) | `TRUE_SCALE_CONVERSION` | HIGH | `NEEDS_CONVERSION_FACTOR_VALIDATION` | ×10 scale between g/dL and g/L. Launch display is mass concentration (g/L) only—not %. Registry factors must be validated against UK lab handbook before SSOT flip. | LC-S8D |
| `hematocrit` | Haematocrit | `%` | `hct`, `pcv`; UK may report `L/L` (e.g. 0.438) or `%` (43.8) | `L/L` | `%` (only if value and reference range transformed together) | UK labs use both fraction and percent; `units.yaml` lines 166–176 define L/L↔% (×100). LC-S8 preflight §4.2 | `DUAL_REPRESENTATION_POLICY` | MEDIUM | `NEEDS_POLICY_DECISION` | Must forbid `0.438 %`, fraction value with % reference, etc. Display `%` acceptable only with coherent transform. | LC-S8D / LC-S8F |
| `calcium` | Serum calcium | `mg/dL` | `calcium_(venous)`; UK `mmol/L` | `mmol/L` | `mmol/L` | UK NHS biochemical profiles report adjusted/total calcium in mmol/L; NICE CKD/mineral bone disease guidance uses mmol/L | `TRUE_SCALE_CONVERSION` | HIGH | `NEEDS_CONVERSION_FACTOR_VALIDATION` | Candidate factor ~0.2495 (mg/dL→mmol/L) must be validated from primary lab chemistry source before implementation. | LC-S8D |
| `corrected_calcium` | Corrected calcium | `mg/dL` | `corrected_calcium_(venous)`; UK `mmol/L` | `mmol/L` | `mmol/L` | Same as calcium | `TRUE_SCALE_CONVERSION` | HIGH | `NEEDS_CONVERSION_FACTOR_VALIDATION` | Same scale risk as calcium. | LC-S8D |
| `magnesium` | Serum magnesium | `mg/dL` | `magnesium_(venous)`; UK `mmol/L` | `mmol/L` | `mmol/L` | UK panels typically mmol/L | `TRUE_SCALE_CONVERSION` | HIGH | `NEEDS_CONVERSION_FACTOR_VALIDATION` | Candidate factor ~0.4113 requires primary-source validation. | LC-S8D |
| `sodium` | Sodium | `mEq/L` | `sodium_(venous)`; UK `mmol/L` | `mmol/L` | `mmol/L` | **UK display:** NHS biochemical profiles and NICE renal/electrolyte guidance use serum sodium in mmol/L. **Equivalence proof:** Na⁺ valence = 1 → 1 mEq = 1 mmol; mEq/L and mmol/L are numerically identical for sodium (IFCC/IUPAC amount concentration). **Label:** mEq/L is a US customary synonym on reports, not a different scale. | `LABEL_EQUIVALENCE_1_TO_1` | LOW | `APPROVED_LABEL_EQUIVALENCE_ONLY` | Relabel SSOT canonical to mmol/L; register mEq/L as accepted input alias with factor 1.0. | LC-S8C |
| `potassium` | Potassium | `mEq/L` | `potassium_(venous)` | `mmol/L` | `mmol/L` | **UK display:** UK NHS pathology reports serum potassium as mmol/L. **Equivalence proof:** K⁺ valence = 1 → 1 mEq/L = 1 mmol/L (same dimensional argument as sodium). **Professional:** UK NEQAS Clinical Chemistry schemes use mmol/L for electrolytes. | `LABEL_EQUIVALENCE_1_TO_1` | LOW | `APPROVED_LABEL_EQUIVALENCE_ONLY` | Independent row; same 1:1 equivalence class as sodium with potassium-specific UK reporting convention. | LC-S8C |
| `chloride` | Chloride | `mEq/L` | `chloride_(venous)` | `mmol/L` | `mmol/L` | **UK display:** UK NHS pathology reports serum chloride as mmol/L. **Equivalence proof:** Cl⁻ valence = 1 → 1 mEq/L = 1 mmol/L. **Professional:** Consistent with UK “Uniformity of Expression in Laboratory Medicine” practice for serum anions reported in mmol/L. | `LABEL_EQUIVALENCE_1_TO_1` | LOW | `APPROVED_LABEL_EQUIVALENCE_ONLY` | Independent row; same 1:1 equivalence class as sodium; no divisor or multiplier between mEq/L and mmol/L for monovalent chloride. | LC-S8C |
| `free_t4` | Free T4 | `ng/dL` | `free_thyroxine`, `freet4`; UK `pmol/L` | `pmol/L` | `pmol/L` | UK thyroid assays standardised in pmol/L; NICE thyroid disease investigation uses SI units | `TRUE_SCALE_CONVERSION` | HIGH | `NEEDS_CONVERSION_FACTOR_VALIDATION` | Candidate factor ~12.87 (ng/dL→pmol/L) must be validated from assay manufacturer or UK lab standard before implementation. | LC-S8D |
| `tsh` | TSH | `mIU/L` | `thyroid_stimulating_hormone`, `thyrotropin` | `mIU/L` | `mIU/L` | UK standard for TSH | `NO_CHANGE_REQUIRED` | LOW | `NO_CHANGE_REQUIRED` | Already UK-appropriate. | — |
| `hba1c` | HbA1c | `%` | `hemoglobin_a1c`, `a1c`, `glycated_hemoglobin`; UK also `mmol/mol` | `mmol/mol` (IFCC) **or** retain `%` pending policy | Policy-dependent | [NICE NG17](https://www.nice.org.uk/guidance/ng17); UK switched to IFCC mmol/mol (2009); DCCT/IFCC master equation in `units.yaml` lines 121–134 | `DUAL_REPRESENTATION_POLICY` | HIGH | `NEEDS_POLICY_DECISION` | Five sub-decisions required: (1) canonical analytical unit, (2) accept `%` input, (3) allow `%` secondary display, (4) de-duplication vs `hba1c_pct`, (5) harmonisation code validity. Do not fold into generic conversion. | LC-S8E |
| `hba1c_pct` | HbA1c (NGSP %) | `%` | (none) | Merge policy with `hba1c` | As per `hba1c` policy | Same as `hba1c` | `DUAL_REPRESENTATION_POLICY` | HIGH | `NEEDS_POLICY_DECISION` | Duplicate representation; must not score twice. | LC-S8E |
| `glucose` | Glucose | `mmol/L` | `blood_sugar`, `blood_glucose`, `sugar` | `mmol/L` | `mmol/L` | UK SI standard | `NO_CHANGE_REQUIRED` | LOW | `NO_CHANGE_REQUIRED` | Already UK/SI. | — |
| `total_cholesterol` | Total cholesterol | `mmol/L` | cholesterol aliases | `mmol/L` | `mmol/L` | UK lipid panels | `NO_CHANGE_REQUIRED` | LOW | `NO_CHANGE_REQUIRED` | Already UK/SI. | — |
| `ldl_cholesterol` | LDL cholesterol | `mmol/L` | ldl aliases | `mmol/L` | `mmol/L` | UK standard | `NO_CHANGE_REQUIRED` | LOW | `NO_CHANGE_REQUIRED` | Already UK/SI. | — |
| `hdl_cholesterol` | HDL cholesterol | `mmol/L` | hdl aliases | `mmol/L` | `mmol/L` | UK standard | `NO_CHANGE_REQUIRED` | LOW | `NO_CHANGE_REQUIRED` | Already UK/SI. | — |
| `triglycerides` | Triglycerides | `mmol/L` | trig aliases | `mmol/L` | `mmol/L` | UK standard | `NO_CHANGE_REQUIRED` | LOW | `NO_CHANGE_REQUIRED` | Already UK/SI. | — |
| `creatinine` | Creatinine | `µmol/L` | `creat`, `serum_creatinine` | `µmol/L` | `µmol/L` | UK standard | `NO_CHANGE_REQUIRED` | LOW | `NO_CHANGE_REQUIRED` | Already UK/SI. | — |
| `urea` | Urea | `mmol/L` | `Urea`, `BUN`, etc. | `mmol/L` | `mmol/L` | UK reports urea in mmol/L | `NO_CHANGE_REQUIRED` | LOW | `NO_CHANGE_REQUIRED` | Already UK/SI. | — |
| `neutrophil_pct` | Neutrophil % | `%` | — | `%` | `%` | Differential percentages are dimensionless % in UK and US | `NO_CHANGE_REQUIRED` | LOW | `DEFER_NOT_LAUNCH_CRITICAL` | Not a UK/US canonical conflict. | — |
| `lymphocyte_pct` | Lymphocyte % | `%` | — | `%` | `%` | Standard differential | `NO_CHANGE_REQUIRED` | LOW | `DEFER_NOT_LAUNCH_CRITICAL` | Same. | — |

---

## 7. Rows approved for safe implementation

**`APPROVED_LABEL_EQUIVALENCE_ONLY` only (LC-S8C):**

| Biomarker ID | Action summary |
|--------------|----------------|
| `platelets` | SSOT canonical → `10^9/L`; register `K/μL`, `K/uL`, `10^3/μL` as accepted input aliases |
| `white_blood_cells` | Same as platelets |
| `sodium` | SSOT canonical → `mmol/L`; register `mEq/L` as alias |
| `potassium` | Same as sodium |
| `chloride` | Same as sodium |

**Preconditions for LC-S8C:** Register equivalences in `units.yaml` and `_units_equivalent()` before changing SSOT canonical strings; add strictness only after equivalence is live (LC-S8A §9.3).

---

## 8. Rows requiring policy decision

| Biomarker ID | Decision | Required resolutions |
|--------------|----------|---------------------|
| `hematocrit` | `NEEDS_POLICY_DECISION` | Canonical analytical unit (`L/L` vs `%`); accepted inputs; display transform rules; forbid mixed value/reference families |
| `hba1c` | `NEEDS_POLICY_DECISION` | Canonical IFCC mmol/mol vs retain %; dual input; display; de-duplication with `hba1c_pct`; validate existing harmonisation in `rules.py` |
| `hba1c_pct` | `NEEDS_POLICY_DECISION` | Deprecate, merge, or alias-only; single scoring path |

---

## 9. Rows requiring conversion-factor validation

| Biomarker ID | Candidate conversion (not approved) | Primary validation required |
|--------------|--------------------------------------|----------------------------|
| `hemoglobin` | g/dL ↔ g/L (×10) | Confirm factors in `units.yaml` lines 154–164 against UK lab handbook |
| `calcium` | mg/dL ↔ mmol/L (~0.2495) | NHS/lab chemistry primary source |
| `corrected_calcium` | same | same |
| `magnesium` | mg/dL ↔ mmol/L (~0.4113) | same |
| `free_t4` | ng/dL ↔ pmol/L (~12.87) | Assay-specific UK reference |

**Do not implement LC-S8D until each row has a cited primary conversion factor.**

---

## 10. Rows deferred or blocked

| Biomarker ID | Decision | Reason |
|--------------|----------|--------|
| `neutrophil_pct`, `lymphocyte_pct` | `DEFER_NOT_LAUNCH_CRITICAL` | `%` is correct for differential percentages |
| (none) | `BLOCKED` | No row is blocked pending external policy veto; high-risk rows are held at validation stage |

---

## 11. Proposed follow-on sprint split

### LC-S8C — Safe UK Unit Label/Equivalence Implementation

**Scope:** `platelets`, `white_blood_cells`, `sodium`, `potassium`, `chloride` only.  
**Allowed decisions:** `APPROVED_LABEL_EQUIVALENCE_ONLY` rows from §7.  
**Forbidden:** True scale conversions; HbA1c; haemoglobin canonical flip.

### LC-S8D — True Conversion Unit Implementation

**Scope:** `hemoglobin`, `calcium`, `corrected_calcium`, `magnesium`, `free_t4`, and `hematocrit` if policy resolves to `L/L` canonical with governed `%` display.  
**Entry criteria:** Each row has `APPROVED_FOR_IMPLEMENTATION` after primary-source conversion validation.  
**Sequence:** Add conversion to `units.yaml` → registry → SSOT canonical → strict set → fixtures.

### LC-S8E — HbA1c Dual-Representation Policy and Implementation

**Scope:** `hba1c`, `hba1c_pct`; mmol/mol vs %; de-duplication; display; harmonisation test replay.  
**Entry criteria:** Explicit policy answers to all five HbA1c sub-decisions in prompt §Special policy handling.

### LC-S8F — Canonical Unit Sentinel Lockdown

**Scope:** Sentinel rule `uk_canonical_unit_ssot_drift` (proposed LC-S8A §10.3); fixture proving value/reference/unit coherence; assert no forbidden UK-launch canonical units in SSOT; frontend no-repair assertion.

---

## 12. Required test and Sentinel guard recommendations

**Do not implement in LC-S8B.** Later sprints must add:

| Guard / test | Purpose |
|--------------|---------|
| SSOT canonical-unit policy test | Assert launch-critical markers use approved UK canonical strings |
| Unit registry equivalence test | `K/μL` ≡ `10^9/L`, `mEq/L` ≡ `mmol/L` after LC-S8C |
| Value/reference coherence test | Extend LC-S8 regression; mixed units fail scoring |
| UK sample panel regression | End-to-end panel with UK units (10⁹/L platelets, mmol/L Ca, etc.) |
| HbA1c dual-input de-duplication test | Single scored HbA1c when both % and mmol/mol present |
| Sentinel `uk_canonical_unit_ssot_drift` | Fail on `K/μL`, `g/dL` Hb, `mg/dL` Ca/Mg, `ng/dL` fT4, `mEq/L` electrolytes in SSOT |
| Sentinel mixed value/reference units | Retain and extend `biomarker_value_reference_unit_incoherence` |
| Frontend no-repair assertion | Layer C must not patch unit labels; fixes belong in Layer A |

---

## 13. Explicit non-authority warning

**This document is not runtime authority.** It does not modify `backend/ssot/biomarkers.yaml`, `backend/ssot/units.yaml`, `backend/core/units/registry.py`, or any executable logic.

Downstream implementation sprints (LC-S8C–LC-S8F) require their own governed Automation Bus work packages with hardened prompts. Citing this document alone does not satisfy SOP v1.3.1 execution requirements.

No conversion factor in this document may be copied into SSOT until validated under LC-S8D with primary-source citation.

---

## Architectural review amendments (2026-05-16)

Post–architectural review remediation within active LC-S8B (policy document only):

1. **Row-level evidence strengthened** for all five `APPROVED_LABEL_EQUIVALENCE_ONLY` rows (`platelets`, `white_blood_cells`, `sodium`, `potassium`, `chloride`): each now cites named UK/NEQAS/NHS/BCSH or SI equivalence reasoning; generic “same as” wording removed.
2. **Haemoglobin display wording corrected:** removed erroneous “% of local policy” display implication; proposed launch display remains `g/L` pending LC-S8D conversion-factor validation.
3. **Decision-count summary recalculated** from §6 table: `NO_CHANGE_REQUIRED` corrected from 12 to **16** (31 total policy rows).
4. **Authority unchanged:** LC-S8B remains policy-only and non-runtime authority; no SSOT, registry, or code paths modified.

---

## Validation record (Cursor Stage 4 — remediation closure)

```text
git branch --show-current:
  launch-core/lc-s8b-uk-canonical-unit-policy-validation

git status --short:
  M docs/audit-papers/LC-S8B_uk_canonical_unit_policy_validation.md

git log --oneline -n 5:
  0982034 chore(bus): LC-S8B kernel COMPLETE status
  da64898 chore(bus): LC-S8B kernel IN_PROGRESS status
  2f83b2d docs(LC-S8B): UK canonical unit policy validation table
  219f969 chore(bus): LC-S8B work package, hardening, and LC-S8A audit input
  b624d05 docs(LC-S8): record authorised narrative scope expansion e5e6d87

git diff --name-only:
  docs/audit-papers/LC-S8B_uk_canonical_unit_policy_validation.md

git diff --cached --name-only:
  (empty)

git stash list:
  stash@{0}: On feature/questionnaire-visual-redesign: LC-S1: frontend env example
```

**Closure classification:**

| Class | Items |
|-------|--------|
| Tracked modified | `docs/audit-papers/LC-S8B_uk_canonical_unit_policy_validation.md` (remediation only) |
| Staged | None |
| Untracked | None |
| Tooling files | None |
| Out-of-scope | None detected |
| Stash (LC-S8B related) | None |

**Stash disposition — `stash@{0}`:**

| Field | Value |
|-------|--------|
| Exact name | `stash@{0}: On feature/questionnaire-visual-redesign: LC-S1: frontend env example` |
| Why unrelated | Created on branch `feature/questionnaire-visual-redesign` for LC-S1 frontend env work; LC-S8B branch is `launch-core/lc-s8b-uk-canonical-unit-policy-validation` with docs-only scope |
| Contents (if known) | LC-S1 frontend environment example changes; not inspected in this remediation (no pop/apply) |
| Tracked/untracked/ignored | Unknown without pop; message implies frontend env file(s)—typical untracked `.env.example` class |
| Blocks LC-S8B closure? | **No** — unrelated branch and work package; retained with human awareness |

**Scope confirmation:** Only `docs/audit-papers/LC-S8B_uk_canonical_unit_policy_validation.md` modified in this remediation. No runtime, SSOT, registry, Sentinel, frontend, fixture, or test files touched. `run_work_package.py finish` not re-run per instruction (prior finish COMPLETE; remediation is document amendment on sprint branch).
