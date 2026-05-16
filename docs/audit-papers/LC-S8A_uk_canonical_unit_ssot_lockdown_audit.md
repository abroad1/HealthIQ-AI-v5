# LC-S8A — UK Canonical Unit SSOT Lockdown Audit

**Mode:** Read-only investigation (no implementation).  
**Work ID:** `LC-S8A-UK-CANONICAL-UNIT-SSOT-LOCKDOWN` (preflight only).  
**Date:** 2026-05-14  
**Auditor:** Claude Code (investigation role)  
**Trigger:** Platelet count displayed as `225 K/μL`; UK lab source was `225 10^9/L, reference 150–450 10^9/L`.

---

## 1. Executive Summary

The LC-S8 scoring guard is working as designed: it correctly blocks mixed-unit numeric scoring. However, the LC-S8A trigger reveals a deeper problem — the canonical unit SSOT (`backend/ssot/biomarkers.yaml`) still contains **US-style, non-SI, or ambiguous canonical units** for a UK-first analytical engine. These units affect **what the engine treats as canonical**, **what gets displayed**, and **what conversions the registry expects to encounter from UK labs**.

The primary issues confirmed:

1. **`platelets` and `white_blood_cells` use `K/μL`** (US-style) — UK labs report `10^9/L`. No conversion registered. Numerically equivalent but SSOT should reflect UK canonical.
2. **`hemoglobin` SSOT canonical unit is `g/dL`** — UK labs report `g/L` (10× different). Conversion exists in registry (added LC-S8) but the SSOT canonical itself remains US-style.
3. **`calcium` and `corrected_calcium` use `mg/dL`** — UK labs report `mmol/L`. No conversion registered. Numeric mismatch factor ≈0.25. UNSAFE for UK labs.
4. **`magnesium` uses `mg/dL`** — UK labs report `mmol/L`. No conversion registered. UNSAFE.
5. **`free_t4` uses `ng/dL`** — UK labs report `pmol/L`. No conversion registered. UNSAFE (factor ≈12.87).
6. **`sodium`, `potassium`, `chloride` use `mEq/L`** — UK standard is `mmol/L`. Numerically equivalent for monovalent ions but US-style label with no registered equivalence.
7. **`hba1c` and `hba1c_pct` use `%`** — UK standard since 2009 is `mmol/mol` (IFCC). Deferred in LC-S8. Policy decision required.

The `10^9/L`-format absolute count markers (`neutrophils`, `lymphocytes`, etc.) are correctly set and do NOT require correction. The electrolyte mEq/L issue is low-risk (numerically equivalent) but must be labelled correctly for UK launch.

**Launch-critical blockers before UK launch:** Calcium/magnesium/free_t4 conversions are missing and numeric scale mismatches are unsafe.

---

## 2. Launch-Readiness Verdict

**NOT launch-ready** for UK clinical accuracy without corrections to:

- `calcium` / `corrected_calcium` SSOT unit and conversion (UNSAFE — no conversion, wrong scale)
- `magnesium` SSOT unit and conversion (UNSAFE — no conversion, wrong scale)
- `free_t4` SSOT unit and conversion (UNSAFE — no conversion, wrong scale)
- `K/μL` → `10^9/L` for `platelets` and `white_blood_cells` (SAFE numerically, but wrong canonical; causes incorrect display labels)
- `mEq/L` → `mmol/L` for electrolytes (safe numerically, but US-style label causing display issues and scoring guard ambiguity)

Deferred for policy confirmation before correcting:
- `hemoglobin` `g/dL` → `g/L` (explicitly deferred in LC-S8; requires fixture migration plan)
- `hematocrit` `%` → `L/L` (explicit LC-S8 deferral; UK labs report both)
- `hba1c` `%` → `mmol/mol` (explicit LC-S8 deferral; dual reporting exists in UK)

---

## 3. Authority Chain and Governing Rule

### 3.1 File authority chain

| Function | Authority File | Evidence |
|----------|---------------|---------|
| Canonical biomarker IDs and aliases | `backend/ssot/biomarkers.yaml` | ADR-001 §SSOT Invariants line 71; ADR-002 Layer A section |
| Canonical per-marker units | `backend/ssot/biomarkers.yaml` each marker's `unit:` field | `biomarkers.yaml` line 1 → every marker entry |
| Unit conversion factors | `backend/ssot/units.yaml` | `registry.py` lines 108–115 load `ssot/units.yaml` |
| Runtime loader | `backend/core/units/registry.py` (`UnitRegistry._load_units`, `_load_biomarker_base_units`) | `registry.py` lines 108–136 |
| Unit conversion layer | Layer A — `apply_unit_normalisation` in `registry.py` | ADR-002 Invariant 5: "Unit normalisation happens once, in Layer A" |
| Scoring layer | Layer B — `backend/core/scoring/rules.py` `calculate_biomarker_score` | `rules.py` lines 260–320 |
| Value/reference unit coherence (post LC-S8) | `value_and_reference_units_coherent_for_numeric_compare()` in `registry.py` lines 476–502; called from `rules.py` lines 289–292 | `sentinel/packs/escaped_defects_v1.json` lines 83–90 |

### 3.2 Governing architectural rule (ADR-002)

ADR-002 Invariant 5 (line 126): "Unit normalisation happens once, in Layer A. Layer B operates exclusively on canonical base units. No unit conversion logic appears in Layer B or C."

ADR-002 Layer A (line 52–55): "Converts units to canonical base units (mmol/L for lipids and glucose; IU/L for enzymes; g/L for proteins)"

**Critical finding:** ADR-002 explicitly states `g/L` for proteins — this is the UK/SI standard. The SSOT `hemoglobin` entry (`g/dL`) is in direct conflict with this stated policy.

### 3.3 Working governing rule for this audit

Per the investigation brief: *Layer A canonical units are UK/SI-first analytical units. US/customary units may exist only as accepted input aliases or future governed display outputs. Mixed-unit scoring is not allowed. Equivalent units must be explicitly registered before scoring.*

This rule is **consistent** with ADR-002 Layer A specification. It is **not** fully implemented in the current SSOT.

---

## 4. Full SSOT Canonical Unit Audit

Full audit of all biomarkers in `backend/ssot/biomarkers.yaml`. Evidence: exact file paths and line numbers cited for each entry.

| Biomarker ID | Line | Aliases | Current SSOT unit | UK/SI canonical | Acceptable? | Reason | Action |
|---|---|---|---|---|---|---|---|
| `total_cholesterol` | 2 | cholesterol, total_chol, chol_total | `mmol/L` | `mmol/L` | ✓ ACCEPT | UK/SI standard | None |
| `ldl_cholesterol` | 18 | ldl, ldl_chol, bad_cholesterol | `mmol/L` | `mmol/L` | ✓ ACCEPT | UK/SI standard | None |
| `hdl_cholesterol` | 34 | hdl, hdl_chol, good_cholesterol | `mmol/L` | `mmol/L` | ✓ ACCEPT | UK/SI standard | None |
| `triglycerides` | 50 | trig, triglyceride, triglycerides_(venous) | `mmol/L` | `mmol/L` | ✓ ACCEPT | UK/SI standard | None |
| `tc_hdl_ratio` | 66 | — | `ratio` | `ratio` (dimensionless) | ✓ ACCEPT | Unitless computed ratio | None |
| `tg_hdl_ratio` | 79 | — | `ratio` | `ratio` | ✓ ACCEPT | Unitless | None |
| `tyg_index` | 92 | — | `ratio` | `ratio` (index) | ✓ ACCEPT | Dimensionless index | None |
| `ldl_hdl_ratio` | 105 | — | `ratio` | `ratio` | ✓ ACCEPT | Unitless | None |
| `non_hdl_cholesterol` | 118 | — | `mmol/L` | `mmol/L` | ✓ ACCEPT | Concentration surrogate | None |
| `apob_apoa1_ratio` | 131 | — | `ratio` | `ratio` | ✓ ACCEPT | Dimensionless | None |
| `apob` | 144 | apo_b, apolipoprotein_b | `g/L` | `g/L` | ✓ ACCEPT | UK/SI standard | None |
| `apoa1` | 159 | apo_a1, apolipoprotein_a1 | `g/L` | `g/L` | ✓ ACCEPT | UK/SI standard | None |
| `glucose` | 174 | blood_sugar, blood_glucose, sugar | `mmol/L` | `mmol/L` | ✓ ACCEPT | UK/SI standard | None |
| `hba1c` | 191 | hemoglobin_a1c, a1c, glycated_hemoglobin | `%` | `mmol/mol` preferred (IFCC; UK since 2009) | ⚠️ NEEDS_POLICY_DECISION | UK dual-reports %. Conversion exists. LC-S8 explicitly deferred. | Policy decision; tests before change |
| `insulin` | 207 | insulin_level, serum_insulin | `μU/mL` | `pmol/L` (some UK labs) or `mIU/L` | ⚠️ NEEDS_POLICY_DECISION | No conversion registered; UK labs vary | Register conversion or confirm policy |
| `creatine_kinase` | 224 | total_ck, ck_total, creatine_kinase_(total), total_creatine_kinese_ck_(venous) | `U/L` | `U/L` | ✓ ACCEPT | Universal enzyme unit | None |
| `aldolase` | 243 | serum_aldolase | `U/L` | `U/L` | ✓ ACCEPT | Universal enzyme unit | None |
| `troponin` | 260 | troponin_i, troponin_t, hs_troponin | `ng/L` | `ng/L` (hs-troponin UK) | ✓ ACCEPT | ng/L is used by UK hs-troponin assays | None |
| `creatinine` | 279 | creat, serum_creatinine | `µmol/L` | `µmol/L` | ✓ ACCEPT | UK/SI standard | None |
| `cystatin_c` | 294 | cystatin_c_serum | `mg/L` | `mg/L` | ✓ ACCEPT | UK standard | None |
| `urea` | 311 | Urea, BUN, Blood urea nitrogen | `mmol/L` | `mmol/L` | ✓ ACCEPT | UK/SI standard | None |
| `uacr` | 327 | urine_albumin_creatinine_ratio, acr | `mg/mmol` | `mg/mmol` | ✓ ACCEPT | UK standard | None |
| `urine_protein_creatinine_ratio` | 347 | — | `mg/mmol` | `mg/mmol` | ✓ ACCEPT | UK standard | None |
| `vitamin_d` | 364 | Vitamin D, 25(OH) Vitamin D, 25-Hydroxy Vitamin D | `nmol/L` | `nmol/L` | ✓ ACCEPT | UK/SI standard | None |
| `alt` | 380 | alanine_aminotransferase, sgpt | `U/L` | `U/L` | ✓ ACCEPT | Universal enzyme unit | None |
| `ast` | 397 | aspartate_aminotransferase, sgot | `U/L` | `U/L` | ✓ ACCEPT | Universal enzyme unit | None |
| `neutrophils` | 413 | neutrophil_count, neutrophils_(venous) | `10^9/L` | `10^9/L` | ✓ ACCEPT | UK/SI standard | None |
| `lymphocytes` | 428 | lymphocyte_count, lymphocytes_(venous) | `10^9/L` | `10^9/L` | ✓ ACCEPT | UK/SI standard | None |
| `basophils_abs` | 443 | basophils_(bas_#), basophils_abs_count | `10^9/L` | `10^9/L` | ✓ ACCEPT | UK/SI standard | None |
| `eosinophils_abs` | 458 | eosinophils_(eos_#), eosinophils_abs_count | `10^9/L` | `10^9/L` | ✓ ACCEPT | UK/SI standard | None |
| `lymphocytes_abs` | 473 | lymphocyte_(lym_#), lymphocytes_abs_count | `10^9/L` | `10^9/L` | ✓ ACCEPT | UK/SI standard | None |
| `monocytes_abs` | 488 | monocyte_(mon_#), monocytes_abs_count | `10^9/L` | `10^9/L` | ✓ ACCEPT | UK/SI standard | None |
| `neutrophils_abs` | 503 | neutrophil_(neu_#), neutrophils_abs_count | `10^9/L` | `10^9/L` | ✓ ACCEPT | UK/SI standard | None |
| `ferritin` | 518 | ferritin_(venous) | `ng/mL` | `µg/L` (numerically equal) | ⚠️ DISPLAY_ONLY_ALIAS_REQUIRED | `ng/mL` = `µg/L` (1:1). UK label is `µg/L`. No numeric risk. | Register `ng/mL` ≡ `µg/L` alias or relabel |
| `fib_4` | 532 | — | `ratio` | `ratio` (dimensionless score) | ✓ ACCEPT | Dimensionless index | None |
| `crp` | 545 | c_reactive_protein, hs_crp, high_sensitivity_crp, c-reactive_protein_crp_(venous) | `mg/L` | `mg/L` | ✓ ACCEPT | UK/SI standard | None |
| `total_ige` | 563 | total_immunoglobulin_e, ige_total | `kU/L` | `kU/L` | ✓ ACCEPT | UK standard | None |
| `tryptase` | 582 | serum_tryptase | `ng/mL` | `µg/L` (numerically equal) | ⚠️ DISPLAY_ONLY_ALIAS_REQUIRED | Same as ferritin — numeric equivalence. | Register equivalence or relabel |
| `free_t4` | 599 | free_thyroxine, freet4 | `ng/dL` | `pmol/L` | ✗ CORRECT_TO_UK_SI | `ng/dL` is US. UK labs report `pmol/L`. Scale difference: ×12.87. No conversion registered. UK lab panels will silently use wrong scale if passed through. | CORRECT_TO_UK_SI + add conversion |
| `tgab` | 614 | thyroglobulin_antibodies_-_tgab, thyroglobulin_antibodies | `IU/mL` | `IU/mL` ≡ `kU/L` | ✓ ACCEPT | IU/mL = kU/L numerically. UK labs use both. | None |
| `tsh` | 629 | thyroid_stimulating_hormone, thyrotropin | `mIU/L` | `mIU/L` or `µIU/mL` (equivalent) | ✓ ACCEPT | mIU/L is UK standard | None |
| `hemoglobin` | 644 | hgb, hb, haemoglobin | `g/dL` | `g/L` | ✗ CORRECT_TO_UK_SI | UK labs report `g/L`. Scale difference ×10. Conversion exists (LC-S8). SSOT itself remains US-style, causing display of `g/dL` even for UK-sourced data. | POLICY DECISION (was LC-S8 explicit deferral) |
| `hematocrit` | 660 | hct, pcv | `%` | `L/L` preferred (UK); `%` also used | ⚠️ NEEDS_POLICY_DECISION | UK labs report as ratio (0.45) or %. Both are used. LC-S8 explicitly deferred. | Policy decision required |
| `white_blood_cells` | 675 | wbc, leukocytes | `K/μL` | `10^9/L` | ✗ CORRECT_TO_UK_SI | US-style unit. Numerically = `10^9/L` but no conversion registered. UK lab data in `10^9/L` passes through with wrong SSOT label causing `K/μL` display. | CORRECT_TO_UK_SI (label only; no numeric change) |
| `platelets` | 690 | plt, platelet_count | `K/μL` | `10^9/L` | ✗ CORRECT_TO_UK_SI | Same as WBC. Confirmed trigger for this audit (`225 K/μL` display). | CORRECT_TO_UK_SI (label only; no numeric change) |
| `nlr` | 705 | — | `ratio` | `ratio` | ✓ ACCEPT | Computed ratio | None |
| `urea_creatinine_ratio` | 718 | — | `ratio` | `ratio` (dimensionless convention) | ✓ ACCEPT | Treated as dimensionless per policy | None |
| `ast_alt_ratio` | 731 | — | `ratio` | `ratio` | ✓ ACCEPT | Dimensionless | None |
| `calcium` | 744 | calcium_(venous) | `mg/dL` | `mmol/L` | ✗ UNSAFE_OR_AMBIGUOUS | US unit. UK labs report `mmol/L`. Factor ≈0.2495. No conversion registered. UK lab data would be used as `mg/dL` magnitudes in scoring — severe numeric error (e.g. 2.4 mmol/L treated as 2.4 mg/dL). | CORRECT_TO_UK_SI + add conversion URGENTLY |
| `corrected_calcium` | 758 | corrected_calcium_(venous) | `mg/dL` | `mmol/L` | ✗ UNSAFE_OR_AMBIGUOUS | Same as calcium. No conversion. | CORRECT_TO_UK_SI + add conversion URGENTLY |
| `sodium` | 772 | sodium_(venous) | `mEq/L` | `mmol/L` | ✗ CORRECT_TO_UK_SI | `mEq/L` = `mmol/L` for Na⁺ (monovalent). US label. No equivalence registered. Numeric risk is low but label is incorrect for UK. | CORRECT_TO_UK_SI (label relabel; register equivalence) |
| `potassium` | 783 | potassium_(venous) | `mEq/L` | `mmol/L` | ✗ CORRECT_TO_UK_SI | Same as sodium. | CORRECT_TO_UK_SI (label) |
| `chloride` | 800 | chloride_(venous) | `mEq/L` | `mmol/L` | ✗ CORRECT_TO_UK_SI | Same as sodium. | CORRECT_TO_UK_SI (label) |
| `magnesium` | 814 | magnesium_(venous) | `mg/dL` | `mmol/L` | ✗ UNSAFE_OR_AMBIGUOUS | US unit. Factor ≈0.4113. No conversion. UK lab data would be scored at wrong numeric scale. | CORRECT_TO_UK_SI + add conversion URGENTLY |
| `rbc` | 828 | — | `10^12/L` | `10^12/L` | ✓ ACCEPT | UK/SI standard | None |
| `mcv` | 847 | — | `fL` | `fL` | ✓ ACCEPT | Universal | None |
| `mch` | 869 | — | `pg` | `pg` | ✓ ACCEPT | Universal | None |
| `mchc` | 886 | — | `g/L` | `g/L` | ✓ ACCEPT | UK/SI standard | None |
| `rdw_cv` | 903 | — | `%` | `%` | ✓ ACCEPT | Percentage is correct for RDW-CV | None |
| `rdw_sd` | 923 | — | `fL` | `fL` | ✓ ACCEPT | Absolute size unit | None |
| `remnant_cholesterol` | 939 | — | `mmol/L` | `mmol/L` | ✓ ACCEPT | UK/SI | None |
| `mpv` | 952 | — | `fL` | `fL` | ✓ ACCEPT | Universal | None |
| `pdw` | 967 | — | `fL` | `fL` | ✓ ACCEPT | Universal | None |
| `neutrophil_pct` | 981 | — | `%` | `%` | ✓ ACCEPT | Differential percentage | None |
| `lymphocyte_pct` | 1001 | — | `%` | `%` | ✓ ACCEPT | Differential percentage | None |
| `monocyte_pct` | 1020 | — | `%` | `%` | ✓ ACCEPT | Differential percentage | None |
| `eosinophil_pct` | 1037 | — | `%` | `%` | ✓ ACCEPT | Differential percentage | None |
| `basophil_pct` | 1055 | — | `%` | `%` | ✓ ACCEPT | Differential percentage | None |
| `free_t3` | 1069 | — | `pmol/L` | `pmol/L` | ✓ ACCEPT | UK/SI standard | None |
| `tpo_ab` | 1088 | — | `kU/L` | `kU/L` | ✓ ACCEPT | UK standard | None |
| `testosterone` | 1103 | — | `nmol/L` | `nmol/L` | ✓ ACCEPT | UK/SI standard | None |
| `free_testosterone` | 1126 | — | `pmol/L` | `pmol/L` | ✓ ACCEPT | UK/SI standard | None |
| `free_testosterone_pct` | 1144 | — | `%` | `%` | ✓ ACCEPT | Percentage ratio | None |
| `shbg` | 1158 | — | `nmol/L` | `nmol/L` | ✓ ACCEPT | UK/SI standard | None |
| `oestradiol` | 1182 | — | `pmol/L` | `pmol/L` | ✓ ACCEPT | UK/SI standard | None |
| `lh` | 1204 | — | `mIU/mL` | `IU/L` (= `mIU/mL` numerically) | ⚠️ DISPLAY_ONLY_ALIAS_REQUIRED | 1 mIU/mL = 1 IU/L numerically. UK label preference is `IU/L`. No numeric risk. | Relabel to `IU/L` or register equivalence |
| `fsh` | 1226 | — | `mIU/mL` | `IU/L` | ⚠️ DISPLAY_ONLY_ALIAS_REQUIRED | Same as LH | Relabel or register |
| `prolactin` | 1246 | — | `mIU/L` | `mIU/L` (UK standard) | ✓ ACCEPT | UK labs use mIU/L for prolactin | None |
| `cortisol` | 1266 | — | `nmol/L` | `nmol/L` | ✓ ACCEPT | UK/SI standard | None |
| `acth` | 1289 | adrenocorticotropic_hormone | `pmol/L` | `pmol/L` (SI) | ✓ ACCEPT | SI unit; UK labs vary (pg/mL also used) | None |
| `dhea` | 1308 | — | `umol/L` | `µmol/L` | ✓ ACCEPT | UK/SI (ASCII vs Unicode equivalent) | None |
| `dhea_s` | 1328 | dheas, dhea_sulfate, dehydroepiandrosterone_sulfate | `umol/L` | `µmol/L` | ✓ ACCEPT | UK/SI | None |
| `fai` | 1349 | — | `%` | `%` (FAI is dimensionless × 100) | ✓ ACCEPT | Correct for FAI index | None |
| `testosterone_free_testosterone_ratio` | 1367 | — | `ratio` | `ratio` | ✓ ACCEPT | Dimensionless | None |
| `egfr` | 1380 | — | `mL/min/1.73m2` | `mL/min/1.73m²` | ✓ ACCEPT | Universal CKD-EPI unit | None |
| `urate` | 1400 | — | `umol/L` | `µmol/L` | ✓ ACCEPT | UK/SI | None |
| `ggt` | 1423 | — | `U/L` | `U/L` | ✓ ACCEPT | Universal enzyme unit | None |
| `alp` | 1443 | — | `U/L` | `U/L` | ✓ ACCEPT | Universal enzyme unit | None |
| `bilirubin` | 1466 | — | `umol/L` | `µmol/L` | ✓ ACCEPT | UK/SI standard | None |
| `albumin` | 1485 | — | `g/L` | `g/L` | ✓ ACCEPT | UK/SI standard | None |
| `total_protein` | 1507 | — | `g/L` | `g/L` | ✓ ACCEPT | UK/SI standard | None |
| `globulin` | 1528 | — | `g/L` | `g/L` | ✓ ACCEPT | UK/SI standard | None |
| `lipoprotein_a` | 1549 | — | `g/L` | `g/L` or `nmol/L` (both UK) | ✓ ACCEPT | g/L acceptable; nmol/L increasingly preferred | Potentially add nmol/L as alias |
| `homocysteine` | 1567 | — | `umol/L` | `µmol/L` | ✓ ACCEPT | UK/SI standard | None |
| `homa_ir` | 1590 | — | `ratio` | `ratio` | ✓ ACCEPT | Dimensionless index | None |
| `hba1c_pct` | 1603 | — | `%` | `mmol/mol` preferred | ⚠️ NEEDS_POLICY_DECISION | Second HbA1c entry using `%`. See §6. | Policy decision |
| `vitamin_b12` | 1623 | — | `pg/mL` | `ng/L` (= `pg/mL`) or `pmol/L` | ⚠️ DISPLAY_ONLY_ALIAS_REQUIRED | `pg/mL` = `ng/L` numerically. UK labs commonly use `ng/L`. No numeric risk. | Relabel to `ng/L` or register equivalence |
| `active_b12` | 1644 | — | `pmol/L` | `pmol/L` | ✓ ACCEPT | UK standard for holotranscobalamin | None |
| `folate` | 1663 | — | `ug/L` | `µg/L` (= `ug/L`) | ✓ ACCEPT | ASCII/Unicode variant; same unit | None |
| `zinc` | 1683 | — | `umol/L` | `µmol/L` | ✓ ACCEPT | UK/SI | None |
| `iron` | 1704 | — | `umol/L` | `µmol/L` | ✓ ACCEPT | UK/SI standard | None |
| `transferrin` | 1724 | — | `g/L` | `g/L` | ✓ ACCEPT | UK/SI standard | None |
| `transferrin_saturation` | 1745 | — | `%` | `%` | ✓ ACCEPT | TSAT as % is UK standard | None |

---

## 5. CBC / Cell-Count Unit Audit

Evidence: `backend/ssot/biomarkers.yaml` lines cited throughout.

| Marker | Line | SSOT Unit | UK Lab Unit | Classification | Risk | Required action |
|---|---|---|---|---|---|---|
| `platelets` | 690 | `K/μL` | `10^9/L` | ✗ WRONG LABEL | Display error, no scoring numeric risk (values identical) | Change SSOT to `10^9/L`; register K/μL as alias |
| `white_blood_cells` | 675 | `K/μL` | `10^9/L` | ✗ WRONG LABEL | Display error, no scoring numeric risk | Change SSOT to `10^9/L`; register K/μL as alias |
| `neutrophils` | 413 | `10^9/L` | `10^9/L` | ✓ CORRECT | None | None |
| `neutrophils_abs` | 503 | `10^9/L` | `10^9/L` | ✓ CORRECT | None | None |
| `lymphocytes` | 428 | `10^9/L` | `10^9/L` | ✓ CORRECT | None | None |
| `lymphocytes_abs` | 473 | `10^9/L` | `10^9/L` | ✓ CORRECT | None | None |
| `monocytes_abs` | 488 | `10^9/L` | `10^9/L` | ✓ CORRECT | None | None |
| `eosinophils_abs` | 458 | `10^9/L` | `10^9/L` | ✓ CORRECT | None | None |
| `basophils_abs` | 443 | `10^9/L` | `10^9/L` | ✓ CORRECT | None | None |
| `rbc` | 828 | `10^12/L` | `10^12/L` | ✓ CORRECT | None | None |
| `hemoglobin` | 644 | `g/dL` | `g/L` | ✗ WRONG SCALE | ×10 numeric risk if lab sends g/L; conversion exists (LC-S8) but SSOT still US-style | Policy decision required (LC-S8 deferral) |
| `hematocrit` | 660 | `%` | `L/L` or `%` | ⚠️ POLICY | UK labs report as 0.45 (L/L) or 45%; conversion exists (LC-S8) | Policy decision required |
| `mcv` | 847 | `fL` | `fL` | ✓ CORRECT | None | None |
| `mch` | 869 | `pg` | `pg` | ✓ CORRECT | None | None |
| `mchc` | 886 | `g/L` | `g/L` | ✓ CORRECT | None | None |
| `rdw_cv` | 903 | `%` | `%` | ✓ CORRECT | None | None |
| `rdw_sd` | 923 | `fL` | `fL` | ✓ CORRECT | None | None |

**Conclusion on CBC:** Most absolute count markers (neutrophils, lymphocytes, etc.) correctly use `10^9/L`. The two SSOT violations are `platelets` and `white_blood_cells` still using `K/μL`. Both are numerically equivalent to `10^9/L` but display incorrectly. No conversion factor is needed — only a label correction and alias registration.

**Why `K/μL` is still appearing in display:** `K/μL` is the SSOT canonical unit (`biomarkers.yaml` line 694/679). The DTO assembly in the orchestrator uses the SSOT unit for the display label. When a UK lab sends `10^9/L`, `apply_unit_normalisation` passthrough returns the input unit (`10^9/L`), but some display path must be falling back to the SSOT unit. Regardless of display mechanism, the correct fix is to change the SSOT canonical unit to `10^9/L` and register `K/μL` as an input alias.

---

## 6. HbA1c Unit Policy Assessment

Evidence: `backend/ssot/biomarkers.yaml` lines 191–206 (`hba1c`), lines 1603–1622 (`hba1c_pct`); `backend/ssot/units.yaml` lines 121–134; `backend/core/units/registry.py` lines 68–84 and 219–236; `backend/core/scoring/rules.py` lines 197–258.

### 6.1 Does the SSOT currently use `%` or `mmol/mol`?

Both `hba1c` and `hba1c_pct` use `%`:
- `hba1c` (line 196): `unit: '%'`
- `hba1c_pct` (line 1603 via implied structure): `unit: '%'`

### 6.2 Dual representation

Yes. Both exist in code:
- Conversion `%` → `mmol/mol`: `units.yaml` lines 121–125, factor `10.929`
- Conversion `mmol/mol` → `%`: `units.yaml` lines 127–134, slope `0.09148`, intercept `2.152` (IFCC→NGSP linear)
- Registry handles both: `_HBA1C_BIOMARKERS = frozenset({"hba1c"})` at `registry.py` line 68
- Scoring `_harmonise_hba1c_reference_range` converts between families before scoring (`rules.py` lines 207–258)
- `hba1c_pct` mapped to `hba1c` for registry lookups (`rules.py` line 494)

### 6.3 Is HbA1c scoring coherent?

Yes, within the `%` canonical domain. The harmonisation function ensures mmol/mol lab refs are converted to `%` before numeric comparison. The `biomarker_value_reference_unit_incoherence` Sentinel class was extended to allow the `%`/`mmol/mol` pair for HbA1c.

### 6.4 Is changing canonical to `mmol/mol` safe now?

**No — not without a dedicated work package.** LC-S8 QA completion doc (line 38–39) explicitly states: "Canonical SSOT unit for HbA1c was not flipped to mmol/mol globally (would be broad behavioural change; deferred / STOP per Task 5)." This must remain a separate policy decision involving:
- Fixture migration (all test fixtures use `%` thresholds)
- New scoring baseline establishment
- Harmonisation direction reversal (convert incoming `%` to `mmol/mol` for scoring)
- Frontend display implications

### 6.5 Required tests before changing

1. Full HbA1c-specific regression suite covering both unit families
2. Scoring baseline replay with mmol/mol as canonical
3. All `test_unit_registry.py` HbA1c path tests
4. `test_hba1c_governance.py::TestHbA1cLayerBBoundPath`
5. New Sentinel fingerprint for mmol/mol canonical

**Recommendation:** Keep HbA1c as `%` canonical for now. Register as `NEEDS_POLICY_DECISION`. Track as LC-S8B or separate policy sprint.

---

## 7. Ratio and Derived-Marker Unit Assessment

Evidence: `backend/ssot/biomarkers.yaml` cited line numbers throughout; `docs/audit-papers/LC-S8_biomarker_unit_range_normalisation_preflight.md` §4.5.

### 7.1 True unitless ratios

All the following are correctly declared `unit: ratio`:
- `tc_hdl_ratio` (line 68) — TC÷HDL, both mmol/L → dimensionless
- `tg_hdl_ratio` (line 80) — TG÷HDL, both mmol/L → dimensionless
- `ldl_hdl_ratio` (line 111) — LDL÷HDL → dimensionless
- `apob_apoa1_ratio` (line 136) — g/L ÷ g/L → dimensionless
- `testosterone_free_testosterone_ratio` (line 1369) — nmol/L ÷ pmol/L → ratio with unit (policy declared as dimensionless)
- `fib_4` (line 533) — calculated index, declared as `ratio`
- `homa_ir` (line 1592) — dimensionless index
- `tyg_index` (line 95) — dimensionless index
- `nlr` (line 708) — dimensionless
- `ast_alt_ratio` (line 735) — dimensionless

### 7.2 Concentration-derived markers (not ratios)

- `non_hdl_cholesterol` (line 120): `mmol/L` ✓ correct — derived concentration, not a ratio
- `remnant_cholesterol` (line 941): `mmol/L` ✓ correct — derived concentration

### 7.3 Urea:creatinine ratio unit policy

`urea_creatinine_ratio` (line 719): `unit: ratio`. Technically this has units (mmol/L ÷ µmol/L = 1000/L), but the clinical convention treats it as dimensionless. The policy declaration as `ratio` is acceptable as a clinical convention, not a physics unit.

### 7.4 Lab-supplied vs computed ratios

No inconsistency detected. Derived ratios computed by `ratio_registry.py` emit `unit: "ratio"` (`LC-S8_preflight.md` §4.5, line 104). Lab-supplied ratios (if any) would use the same canonical ID and be evaluated against the same policy bounds.

### 7.5 ApoB:ApoA1 ratio

`apob_apoa1_ratio` (line 136): `unit: ratio` — dimensionless (g/L ÷ g/L). Correct.

### 7.6 Findings

No ratio markers are incorrectly using concentration units. No concentration markers are incorrectly using `ratio`. The urea:creatinine ratio unit policy is a clinical convention; no action required.

---

## 8. Conversion Matrix Audit

Evidence: `backend/ssot/units.yaml` lines 83–194; `backend/core/units/registry.py` lines 62–84 and 152–216.

| Unit pair | Direction | Conversion in units.yaml | Registered in registry.py | Notes |
|---|---|---|---|---|
| `K/μL` ↔ `10^9/L` | both | ✗ MISSING | ✗ MISSING | Numerically equal (factor=1). Not registered as equivalent. Must add. |
| `K/uL` ↔ `10^9/L` | both | ✗ MISSING | ✗ MISSING | ASCII variant of above. |
| `10^3/μL` ↔ `10^9/L` | both | ✗ MISSING | ✗ MISSING | Mathematically identical. |
| `g/dL` ↔ `g/L` (hemoglobin) | both | ✓ PRESENT (lines 154–164) | ✓ PRESENT (lines 201–208) | Factor 0.1 / 10.0. Added in LC-S8. |
| `%` ↔ `L/L` (hematocrit) | both | ✓ PRESENT (lines 166–176) | ✓ PRESENT (lines 209–216) | Factor 0.01 / 100.0. Added in LC-S8. |
| `%` ↔ `mmol/mol` (HbA1c) | `%`→mmol/mol | ✓ PRESENT (lines 121–125) | ✓ PRESENT (lines 185–188) | Factor 10.929 |
| `mmol/mol` ↔ `%` (HbA1c) | mmol/mol→`%` | ✓ PRESENT (lines 127–134) | ✓ PRESENT (lines 219–236) | Linear: slope 0.09148, intercept 2.152 |
| `mg/dL` ↔ `mmol/L` (cholesterol) | both | ✓ PRESENT (lines 85–96) | ✓ PRESENT (lines 169–176) | Factors 0.02586 / 38.67 |
| `mg/dL` ↔ `mmol/L` (triglycerides) | both | ✓ PRESENT (lines 97–107) | ✓ PRESENT (lines 177–184) | Factors 0.01129 / 88.57 |
| `mg/dL` ↔ `mmol/L` (glucose) | both | ✓ PRESENT (lines 109–119) | ✓ PRESENT (lines 161–168) | Factors 0.0556 / 18.0 |
| `mg/dL` ↔ `mmol/L` (urea) | `mg/dL`→`mmol/L` | ✓ PRESENT (lines 136–140) | ✓ PRESENT (lines 189–192) | Factor 0.357 |
| `mg/dL` ↔ `µmol/L` (creatinine) | `mg/dL`→`µmol/L` | ✓ PRESENT (lines 142–146) | ✓ PRESENT (lines 193–196) | Factor 88.4 |
| `ng/mL` ↔ `nmol/L` (vitamin D) | `ng/mL`→`nmol/L` | ✓ PRESENT (lines 148–152) | ✓ PRESENT (lines 197–200) | Factor 2.5 |
| `mg/dL` ↔ `mmol/L` (calcium) | both | ✗ MISSING | ✗ MISSING | Factor would be 0.2495 / 4.008. UNSAFE. |
| `mg/dL` ↔ `mmol/L` (magnesium) | both | ✗ MISSING | ✗ MISSING | Factor would be 0.4113 / 2.431. UNSAFE. |
| `ng/dL` ↔ `pmol/L` (free_t4) | both | ✗ MISSING | ✗ MISSING | Factor would be 12.87 / 0.0777. UNSAFE. |
| `mEq/L` ↔ `mmol/L` (Na, K, Cl) | both | ✗ MISSING | ✗ MISSING | Factor = 1.0 for monovalent ions. Low numeric risk but missing as registered equivalence. |
| `µU/mL` ↔ `pmol/L` (insulin) | both | ✗ MISSING | ✗ MISSING | Factor ≈ 6.0 (but varies by assay). Policy decision needed. |
| `U/L` ↔ `IU/L` (enzymes) | equivalence | Not explicit | Not registered | 1 U/L = 1 IU/L by definition. No conversion needed; register as string equivalence. |

**Missing conversion summary:**
- `K/μL` / `K/uL` / `10^3/μL` ↔ `10^9/L` — factor 1.0 (register as equivalence)
- `mg/dL` ↔ `mmol/L` for calcium — factor 0.2495 / 4.008
- `mg/dL` ↔ `mmol/L` for magnesium — factor 0.4113 / 2.431
- `ng/dL` ↔ `pmol/L` for free_t4 — factor 12.87 / 0.0777
- `mEq/L` ↔ `mmol/L` for monovalent electrolytes — factor 1.0

---

## 9. Strict Conversion Policy Audit

Evidence: `backend/core/units/registry.py` lines 62–84.

### 9.1 Current strict biomarkers

`_STRICT_CONVERSION_BIOMARKERS` (lines 74–84) contains the union of:
- `_CHOLESTEROL_BIOMARKERS`: `{total_cholesterol, ldl_cholesterol, hdl_cholesterol}`
- `_TRIGLYCERIDE_BIOMARKERS`: `{triglycerides}`
- `_GLUCOSE_BIOMARKERS`: `{glucose}`
- `_HBA1C_BIOMARKERS`: `{hba1c}`
- `_UREA_BIOMARKERS`: `{urea}`
- `_CREATININE_BIOMARKERS`: `{creatinine}`
- `_VITAMIN_D_BIOMARKERS`: `{vitamin_d}`
- `_HEMOGLOBIN_BIOMARKERS`: `{hemoglobin}` (added LC-S8)
- `_HEMATOCRIT_BIOMARKERS`: `{hematocrit}` (added LC-S8)

### 9.2 Biomarkers that should be strict but are not

| Biomarker | Why strict is needed | Risk of not being strict |
|---|---|---|
| `platelets` | SSOT canonical `K/μL`; UK labs send `10^9/L`; no conversion registered | Passthrough preserves input unit; display uses SSOT label → display mismatch |
| `white_blood_cells` | Same as platelets | Same |
| `calcium` | SSOT canonical `mg/dL`; UK labs send `mmol/L`; no conversion → factor 0.2495 mismatch | Lab value in mmol/L scored as mg/dL magnitudes → catastrophic scoring error |
| `corrected_calcium` | Same | Same |
| `magnesium` | SSOT canonical `mg/dL`; no conversion to mmol/L | Same as calcium |
| `free_t4` | SSOT canonical `ng/dL`; UK labs send `pmol/L`; factor 12.87 mismatch | Lab values at pmol/L magnitude scored as ng/dL → wrong status |
| `sodium` | `mEq/L` vs `mmol/L` — numerically equivalent for Na⁺ | Low numeric risk; but unregistered equivalence is architecturally incorrect |
| `potassium` | Same | Same |
| `chloride` | Same | Same |

### 9.3 Should CBC/cell-count markers become strict?

**Yes, for `platelets` and `white_blood_cells`**, but only AFTER registering the `K/μL` ↔ `10^9/L` equivalence (otherwise all labs currently sending `K/μL` would hard-fail). The correct sequence:
1. Register equivalence in `units.yaml` and `_units_equivalent()`
2. Change SSOT canonical to `10^9/L`
3. Mark as strict

For the absolute count markers already using `10^9/L` (neutrophils, lymphocytes, etc.) — they are already correct and strictness is lower priority since no conversion is needed.

### 9.4 Risk of broad strictness

Adding strict for calcium/magnesium/free_t4 WITHOUT first registering conversions would block all UK lab submissions for those markers. The correct sequence is always: **add conversion → then add strictness**. Strictness without conversion = hard breakage.

---

## 10. Scoring and Sentinel Coverage Assessment

Evidence: `backend/core/scoring/rules.py` lines 289–292; `sentinel/packs/escaped_defects_v1.json` lines 83–90; `sentinel/sentinel_runner.py` lines 47–68.

### 10.1 Does current Sentinel catch `K/μL` vs `10^9/L`?

**Partially.** The `biomarker_value_reference_unit_incoherence` defect class (Sentinel pack line 83, test file `test_lc_s8_biomarker_unit_reference_incoherence_regression.py`) catches the case where **value unit and reference unit are incoherent after LC-S8 normalisation**.

However, for `K/μL` vs `10^9/L` specifically:
- If a UK lab submits `platelets: {value: 225, unit: "10^9/L", reference_range: {min: 150, max: 450, unit: "10^9/L"}}`
- Registry passthrough returns `(225, "10^9/L")` — value and ref are the SAME unit
- `value_and_reference_units_coherent_for_numeric_compare("platelets", "10^9/L", "10^9/L")` → True
- Scoring proceeds correctly numerically
- **The Sentinel coherence check does NOT fire because value and ref units match**
- But the **display unit** shows `K/μL` from SSOT — the Sentinel does not check this

Therefore the LC-S8 Sentinel class **cannot detect the `K/μL` SSOT label problem**. It only detects value-vs-reference unit incoherence at scoring time.

### 10.2 Does it catch US-style canonical SSOT drift?

**No.** No existing Sentinel class checks that the SSOT canonical unit field is UK/SI appropriate.

### 10.3 Recommendation for new Sentinel class

**Proposed class: `uk_canonical_unit_ssot_drift`**

This class would:
- Load `backend/ssot/biomarkers.yaml`
- Assert that no launch-critical biomarker uses a known US-only canonical unit string
- Fail conditions (UK-inappropriate canonical units):
  - `K/μL` or `K/uL` for any cell-count marker
  - `g/dL` for hemoglobin (policy-conditional)
  - `mg/dL` for calcium, corrected_calcium, or magnesium
  - `ng/dL` for free_t4
  - `mEq/L` for sodium, potassium, or chloride

This would act as a regression guard: if any future sprint accidentally re-introduces a US-style canonical unit, the Sentinel would catch it immediately.

The existing `biomarker_value_reference_unit_incoherence` class should be **extended** (not replaced) to also cover the case where the SSOT canonical unit differs from the unit in the reference range, even when value and ref are coherent.

---

## 11. Similar Undetected Issue Risk

The following categories carry HIGH risk for similar undetected UK vs US unit conflicts:

1. **Lab panels with calcium** — Any UK lab reporting calcium in `mmol/L` against an SSOT canonical of `mg/dL` with no conversion path means the value is scored against UK reference ranges at the wrong numeric scale. This is the **highest-risk undetected issue** in the SSOT.

2. **Magnesium** — Same as calcium but less commonly reported in UK panels.

3. **Free T4 (ng/dL vs pmol/L)** — Factor 12.87 mismatch. Any thyroid panel from a UK lab would have a severely wrong T4 score if the lab sends pmol/L and the SSOT is ng/dL.

4. **Electrolytes (mEq/L)** — Numerically safe for monovalent ions but labelling is incorrect. No risk of scoring error.

5. **Display-only unit label drift** — The `K/μL` display issue on platelets is symptomatic of a broader pattern: the orchestrator DTO uses the SSOT canonical unit for display, so any non-UK SSOT unit will display in a UK-inappropriate label even when the underlying value is correct.

---

## 12. Recommended LC-S8A Implementation Scope

**Recommended: Option E — combined SSOT + conversion + strictness + Sentinel package, delivered in two sequenced sub-sprints.**

### Sub-sprint A: SSOT labelling corrections (LOW risk)

Corrections that are numerically safe (no scale change):

| File | Change | Numeric risk |
|---|---|---|
| `backend/ssot/biomarkers.yaml` | `platelets`: `K/μL` → `10^9/L` | NONE (1:1 equiv) |
| `backend/ssot/biomarkers.yaml` | `white_blood_cells`: `K/μL` → `10^9/L` | NONE (1:1 equiv) |
| `backend/ssot/biomarkers.yaml` | `sodium`: `mEq/L` → `mmol/L` | NONE (1:1 equiv for Na⁺) |
| `backend/ssot/biomarkers.yaml` | `potassium`: `mEq/L` → `mmol/L` | NONE (1:1 equiv for K⁺) |
| `backend/ssot/biomarkers.yaml` | `chloride`: `mEq/L` → `mmol/L` | NONE (1:1 equiv for Cl⁻) |
| `backend/ssot/biomarkers.yaml` | `lh`: `mIU/mL` → `IU/L` | NONE (1:1 equiv) |
| `backend/ssot/biomarkers.yaml` | `fsh`: `mIU/mL` → `IU/L` | NONE (1:1 equiv) |
| `backend/ssot/biomarkers.yaml` | `vitamin_b12`: `pg/mL` → `ng/L` | NONE (1:1 equiv) |
| `backend/ssot/biomarkers.yaml` | `ferritin`: `ng/mL` → `µg/L` | NONE (1:1 equiv) |
| `backend/ssot/biomarkers.yaml` | `tryptase`: `ng/mL` → `µg/L` | NONE (1:1 equiv) |
| `backend/ssot/units.yaml` | Add `10^9/L` as unit entry; add `K/μL` / `K/uL` as aliases; register equivalence | Low |
| `backend/ssot/units.yaml` | Add `IU/L` entry; register `mIU/mL` equivalence | Low |
| `backend/core/units/registry.py` | Add `K/μL` / `10^9/L` to `_units_equivalent` equivalence set | Low |
| `sentinel/packs/escaped_defects_v1.json` | Add `uk_canonical_unit_ssot_drift` class | None |
| new test file | Sentinel regression test for SSOT unit label validation | None |

### Sub-sprint B: Conversion additions and unsafe unit corrections (STANDARD–HIGH risk)

Corrections requiring new conversion factors:

| File | Change | Numeric risk |
|---|---|---|
| `backend/ssot/biomarkers.yaml` | `calcium`: `mg/dL` → `mmol/L` | HIGH (requires all test fixtures using calcium to be on mmol/L) |
| `backend/ssot/biomarkers.yaml` | `corrected_calcium`: `mg/dL` → `mmol/L` | HIGH |
| `backend/ssot/biomarkers.yaml` | `magnesium`: `mg/dL` → `mmol/L` | HIGH |
| `backend/ssot/biomarkers.yaml` | `free_t4`: `ng/dL` → `pmol/L` | HIGH |
| `backend/ssot/units.yaml` | Add calcium conversion: `mg/dL` ↔ `mmol/L` (factor 0.2495 / 4.008) | — |
| `backend/ssot/units.yaml` | Add magnesium conversion: `mg/dL` ↔ `mmol/L` (factor 0.4113 / 2.431) | — |
| `backend/ssot/units.yaml` | Add free_t4 conversion: `ng/dL` ↔ `pmol/L` (factor 12.87 / 0.0777) | — |
| `backend/core/units/registry.py` | Add `_CALCIUM_BIOMARKERS`, `_MAGNESIUM_BIOMARKERS`, `_FREE_T4_BIOMARKERS` sets and conversion dispatch | STANDARD |
| `backend/core/units/registry.py` | Add calcium, magnesium, free_t4 to `_STRICT_CONVERSION_BIOMARKERS` | STANDARD |
| `backend/tests/regression/` | New regression tests for calcium/magnesium/free_t4 unit normalisation | None |

Sub-sprint B requires an ADR or policy statement confirming calcium, magnesium, and free_t4 UK canonical units before implementation.

---

## 13. Expected Files to Touch

### Sub-sprint A (LOW risk)

- `backend/ssot/biomarkers.yaml`
- `backend/ssot/units.yaml`
- `backend/core/units/registry.py` (`_units_equivalent` function and equivalence sets)
- `sentinel/packs/escaped_defects_v1.json`
- `backend/tests/regression/test_lc_s8a_uk_canonical_unit_ssot_drift_regression.py` (new)

### Sub-sprint B (HIGH risk)

All Sub-sprint A files plus:
- `backend/core/units/registry.py` (new biomarker groups, conversion dispatch, strict set expansion)
- `backend/tests/regression/test_lc_s8b_calcium_magnesium_free_t4_unit_normalisation.py` (new)
- Possibly `backend/tests/unit/test_unit_registry.py` (extend existing)
- Possibly `backend/tests/unit/test_scoring_rules.py` (extend for new conversions)

**Must NOT be touched in LC-S8A:**

- `backend/core/pipeline/orchestrator.py` (no scope)
- `backend/core/scoring/rules.py` (no scope unless Sub-sprint B)
- `backend/core/analytics/` (no scope)
- Knowledge Bus packages
- Frontend

---

## 14. Risk Classification

| Sub-sprint | Risk level | Justification |
|---|---|---|
| A (label corrections) | **STANDARD** | All corrections are numerically equivalent (factor=1). No scoring behaviour changes. SSOT is touched (HIGH trigger) but changes are label-only with no numeric consequence. Requires Claude audit + GPT review per SOP. |
| B (conversion + SSOT corrections) | **HIGH** | Touches `backend/ssot/`, `backend/core/units/registry.py` conversion matrix, and strict set. Behavioural change: calcium/magnesium/free_t4 from UK labs will now normalise correctly instead of passing through. Requires Claude audit + GPT architectural review + dual approval. |

---

## 15. Stop Conditions

### Sub-sprint A

- Any test fixture breakage caused by label change (unit string comparison changes)
- Any scoring difference on existing fixtures from label-only SSOT changes
- Unexpected test failures in `test_unit_registry.py`, `test_scoring_rules.py`, or Sentinel pack

### Sub-sprint B

- **Clinical policy not confirmed** for calcium (`mg/dL` → `mmol/L`), magnesium, or free_t4 before implementation
- Any scoring regression on historical test fixtures that is not explicitly acknowledged as a deliberate normalisation correction
- Introducing silent coercion without `unit_normalised` flag on DTO
- Any change that breaks the `hemoglobin` or `hematocrit` paths established in LC-S8

---

## 16. Recommended Tests and Sentinel Candidates

### Tests — Sub-sprint A

1. **`test_lc_s8a_uk_canonical_unit_ssot_drift_regression.py`**: Assert that `platelets`, `white_blood_cells`, and electrolytes SSOT units are UK-canonical; assert `K/μL` is not the canonical for any cell-count marker; assert `mEq/L` is not canonical for any electrolyte.
2. **`test_unit_registry.py` extension**: Assert `_units_equivalent("K/μL", "10^9/L")` returns True; assert `_units_equivalent("10^9/L", "K/uL")` returns True; assert passthrough for a `10^9/L` input on `platelets` produces `unit: "10^9/L"` with no conversion.
3. **Scoring regression**: Pass `platelets: {value: 225, unit: "10^9/L", reference_range: {min: 150, max: 450, unit: "10^9/L"}}` — assert coherence check passes, score is non-zero.

### Tests — Sub-sprint B

4. **Calcium normalisation**: `calcium: {value: 2.4, unit: "mmol/L", reference_range: {min: 2.1, max: 2.6, unit: "mmol/L"}}` → normalises to canonical mmol/L, scores correctly. Also: `value: 9.6, unit: "mg/dL"` → converts to `2.395 mmol/L`.
5. **Magnesium normalisation**: `magnesium: {value: 0.85, unit: "mmol/L"}` → scores correctly. `value: 2.06, unit: "mg/dL"` → converts to `0.848 mmol/L`.
6. **Free T4**: `free_t4: {value: 15, unit: "pmol/L"}` → scores correctly. `value: 1.17, unit: "ng/dL"` → converts to `15.06 pmol/L`.

### Sentinel candidates

7. **`uk_canonical_unit_ssot_drift`**: New Sentinel class. Loads `biomarkers.yaml`, asserts no launch-critical biomarker has a US-only canonical unit. Fail conditions: `K/μL`, `g/dL` (hemoglobin), `mg/dL` for electrolytes/calcium/magnesium, `ng/dL` for thyroid markers. Guard type: `active_deterministic`. This runs statically — no lab data needed.

---

## 17. Open Questions / Blockers

1. **Hemoglobin `g/dL` vs `g/L`**: LC-S8 explicitly deferred this (completion doc line 10). Is this re-authorised in LC-S8A scope? Clinical policy for UK-first engine says `g/L`. ADR-002 Layer A explicitly says `g/L` for proteins. If the answer is yes, this should be in Sub-sprint B with explicit fixture migration plan.

2. **Hematocrit `%` vs `L/L`**: LC-S8 deferred (completion doc line 39). Conversion exists. UK labs report both. Policy decision: keep `%` as canonical (display-native) or change to `L/L` (SI-native)?

3. **HbA1c `%` vs `mmol/mol`**: LC-S8 deferred explicitly. UK standard since 2009 is IFCC mmol/mol. This requires a dedicated policy decision + full migration plan.

4. **Insulin `μU/mL` vs `pmol/L`**: No conversion factor registered. UK labs vary. Which canonical unit should be adopted? Is this in scope for LC-S8A?

5. **Calcium conversion factor confirmation**: The standard factor is 0.2495 (mmol/L = mg/dL × 0.2495). This should be confirmed against a governed clinical reference before registering in units.yaml.

6. **Magnesium conversion factor confirmation**: Standard factor is 0.4113 (mmol/L = mg/dL × 0.4113). Confirm before registering.

7. **Free T4 conversion factor confirmation**: Standard conversion is `pmol/L = ng/dL × 12.87`. Confirm against a governed reference.

8. **`10^9/L` string vs `10^9/L` unicode/caret**: Lab systems may send this as `10^9/L`, `10⁹/L`, or other encodings. The alias registration must cover all common forms.

9. **`ferritin` / `vitamin_b12` label change impact**: If any existing analysis stored in the database uses `ng/mL` as the unit string for ferritin, changing the canonical to `µg/L` would affect replay. Confirm scope of impact before changing.

---

## 18. Files Inspected

All evidence in this audit is derived exclusively from direct file reads. No chat history or prior session memory was used.

| File | Evidence used |
|---|---|
| `backend/ssot/biomarkers.yaml` | Full read, lines 1–1763 — all biomarker unit fields |
| `backend/ssot/units.yaml` | Full read, lines 1–195 — unit definitions, categories, conversion factors |
| `backend/core/units/registry.py` | Full read, lines 1–503 — UnitRegistry, conversion dispatch, strict set, coherence guard |
| `backend/core/scoring/rules.py` | Full read, lines 1–483 — scoring logic, HbA1c harmonisation, coherence gate |
| `sentinel/sentinel_runner.py` | Full read, lines 1–381 — defect class registry, test mapping |
| `sentinel/packs/escaped_defects_v1.json` | Full read, lines 1–92 — current guarded defect classes |
| `docs/audit-papers/LC-S8_biomarker_unit_range_normalisation_preflight.md` | Full read, lines 1–290 — LC-S8 preflight audit findings |
| `docs/sprints/LC-S8_biomarker_unit_range_normalisation_qa_completion_2026-05.md` | Full read, lines 1–95 — LC-S8 completion record, explicit deferrals |
| `architecture/ADR-001-platform-non-negotiables.md` | Full read, lines 1–104 — SSOT invariants |
| `architecture/ADR-002-deterministic-analysis-engine.md` | Full read, lines 1–150 — Layer A unit policy, `g/L` for proteins |

**Files NOT found / not read:**

- `architecture/Master_PRD_v5.2.md` — not checked in this audit (ADR-002 cites it; ADRs are sufficient for governing rule purposes)
- `backend/core/pipeline/orchestrator.py` — not read in this audit; LC-S8 preflight covered the relevant DTO assembly pattern

---

## Closing Summary

| Item | Result |
|------|--------|
| Files inspected | 10 (see §18) |
| File created | `docs/audit-papers/LC-S8A_uk_canonical_unit_ssot_lockdown_audit.md` |
| Non-audit files modified? | **No** |
| US-style canonical units remaining in SSOT? | **Yes — 5 categories confirmed** |
| `K/μL` still canonical anywhere? | **Yes — `platelets` (line 694), `white_blood_cells` (line 679)** |
| `g/dL` still canonical? | **Yes — `hemoglobin` (line 649)** (explicitly deferred in LC-S8) |
| `%` used where UK lab canonical should differ? | **Yes — `hematocrit` (policy: L/L vs %); `hba1c`/`hba1c_pct` (policy: mmol/mol)** |
| `mg/dL` used where UK standard is `mmol/L`? | **Yes — `calcium` (line 747), `corrected_calcium` (line 762), `magnesium` (line 819)** |
| `ng/dL` used where UK standard is `pmol/L`? | **Yes — `free_t4` (line 602)** |
| `mEq/L` used where UK standard is `mmol/L`? | **Yes — `sodium` (line 777), `potassium` (line 789), `chloride` (line 805)** |
| Launch-critical unit corrections (unsafe, no conversion) | calcium, corrected_calcium, magnesium, free_t4 |
| Launch-critical label corrections (safe, 1:1 equivalent) | platelets, white_blood_cells, sodium, potassium, chloride |
| Recommended LC-S8A risk level | **STANDARD for Sub-sprint A; HIGH for Sub-sprint B** |
| Should implementation proceed immediately? | **Sub-sprint A (label corrections): yes, proceed. Sub-sprint B (conversions): requires clinical unit policy confirmation first.** |
