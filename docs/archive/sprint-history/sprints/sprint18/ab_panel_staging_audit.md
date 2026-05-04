# AB Panel Staging Audit Report

**Branch:** sprint18/biomarker-expansion  
**Baseline tag:** v0.17-freeze  
**Report date:** 2026-02-27  
**Scope:** Investigation + reporting only (no migration performed)

> **Post-migration (2026-02-25):** Staging folder `backend/ssot/_ab_panel_staging/` has been removed. This document is retained for historical reference.

---

## Task 0 — File Mapping (Staging ↔ Runtime)

### 1) Staging files (exact names)

| # | Staging file |
|---|--------------|
| 1 | `backend/ssot/_ab_panel_staging/ab_panel_biomarkers.yaml` |
| 2 | `backend/ssot/_ab_panel_staging/ab_panel_alias_registry.yaml` |
| 3 | `backend/ssot/_ab_panel_staging/ab_panel_system_burden_registry.yaml` |

**Evidence:** `Glob` search for `**/_ab_panel_staging/*` returns exactly these 3 files.

### 2) Runtime counterparts

| Staging file | Runtime counterpart | Mapping justification |
|--------------|---------------------|------------------------|
| `ab_panel_biomarkers.yaml` | `backend/ssot/biomarkers.yaml` | Same schema (`biomarkers:` top-level key); staging is expansion of production biomarkers |
| `ab_panel_alias_registry.yaml` | `backend/ssot/biomarker_alias_registry.yaml` | Staging uses `ab_full_panel` list; runtime uses flat canonical_id/aliases structure; migration merges |
| `ab_panel_system_burden_registry.yaml` | `backend/ssot/system_burden_registry.yaml` | Same schema; staging expands burden entries |

**Evidence:** `backend/scripts/validate_ab_panel_ssot.py` lines 139–146 define `required_files` mapping:
- `ab_biomarkers` → `staging_dir / "ab_panel_biomarkers.yaml"`
- `ab_alias` → `staging_dir / "ab_panel_alias_registry.yaml"`
- `ab_burden` → `staging_dir / "ab_panel_system_burden_registry.yaml"`

And compares against `prod_biomarkers`, `prod_alias`, `prod_burden` from `ssot_dir`.

### 3) Indirectly impacted SSOT files

| File | Impact |
|------|--------|
| `backend/ssot/clusters.yaml` | References `white_blood_cells`; staging now uses `white_blood_cells` — **aligned** |
| `backend/ssot/scoring_policy.yaml` | References `white_blood_cells`; staging aligned — **aligned** |
| `backend/ssot/criticality.yaml` | References `white_blood_cells` — **aligned** |
| `backend/ssot/ranges.yaml` | References `white_blood_cells` — **aligned** |
| `backend/ssot/relationships.yaml` | Uses derived markers (`tg_hdl_ratio`, `ast_alt_ratio`, `urea_creatinine_ratio`, `nlr`); staging has `tc_hdl_ratio`, `apoB_apoA1_ratio`; production has `ast`, `nlr` inputs — **partial overlap** |
| `backend/ssot/scoring_policy.yaml` `derived_ratios` | Lists derived markers; staging adds `apoB_apoA1_ratio`, `tc_hdl_ratio`, `non_hdl_cholesterol`, `testosterone_free_testosterone_ratio` — **additive** |
| `backend/core/analytics/ratio_registry.py` | Hardcoded `DERIVED_IDS`; not in SSOT but must align with biomarkers — **code dependency** |
| `backend/core/llm/prompts/parsing_prompt_*.txt` | May list canonical IDs; need sync if migration changes canonicals |

---

## Task 1 — AB Full Panel Coverage Audit

### Authoritative AB biomarker list

**Source:** Extracted from `AB_full panel_generated.pdf` (Sussex Pathology / OneDayTests Ultimate Longevity Blood Test). PDF path used in prior session: `c:\Users\abroa\Downloads\AB_full panel_generated.pdf`. PDF is **not in repo**; list produced from prior Read-tool extraction.

**Total unique biomarkers:** 79

### Extracted list (deterministic, as-labelled)

```
Leukocytes (WBC), Erythrocytes (RBC), Haemoglobin (HGB), Haematocrit (HCT),
Mean Corpuscular Volume (MCV), Mean Corpuscular Haemoglobin (MCH), Mean Corpuscular Haemoglobin Concentration (MCHC),
Red Cell Distribution Width (RDW-CV), Red Cell Distribution Width SD (RDW-SD),
Platelets (PLT), Mean Platelet Volume (MPV), Platelet Distribution Width (PDW),
Neutrophil (NEU %), Neutrophil (NEU #), Lymphocyte (LYM %), Lymphocyte (LYM #),
Monocyte (MON %), Monocyte (MON #), Eosinophils (EOS %), Eosinophils (EOS #),
Basophils (BAS %), Basophils (BAS #),
Thyroglobulin Antibodies (TgAb), Thyroid Peroxidase Antibodies (TPO Ab),
Free T4, Free T3, TSH,
Zinc, Vitamin D, Active Vitamin B12, Vitamin B12, Folic Acid,
Oestradiol, Free Testosterone Calculation, Free Testosterone % Calculation,
Testosterone : Free Testosterone Ratio,
Luteinizing Hormone (LH), FSH, Sex Hormone Binding Globulin (SHBG), Testosterone,
Prolactin, Cortisol, Free Androgen Index (FAI), DHEA,
eGFR, Creatinine, Urea, Uric Acid,
Apolipoprotein B, Apolipoprotein A1, Apolipoprotein ratio,
LDL, HDL, Total Cholesterol, Triglycerides, Non HDL Cholesterol, Total Cholesterol/HDL Ratio,
Lipoprotein (A), Homocysteine, CRP,
HbA1c %, HbA1c (mmol/mol),
Transferrin, Serum Iron, Ferritin,
ALT, GGT, ALP, Bilirubin, Albumin, Total Protein, Globulin,
Creatine Kinase,
Sodium, Potassium, Calcium, Chloride, Magnesium, Corrected Calcium
```

### A) Mapping table: AB biomarker name → staging canonical_id

| AB biomarker (lab label) | Staging canonical_id | Status |
|--------------------------|----------------------|--------|
| Leukocytes (WBC) | white_blood_cells | PRESENT_AS_ALIAS |
| Erythrocytes (RBC) | rbc | PRESENT_AS_ALIAS |
| Haemoglobin (HGB) | hemoglobin | PRESENT_AS_ALIAS |
| Haematocrit (HCT) | hematocrit | PRESENT_AS_ALIAS |
| Mean Corpuscular Volume (MCV) | mcv | PRESENT_AS_ALIAS |
| Mean Corpuscular Haemoglobin (MCH) | mch | PRESENT_AS_ALIAS |
| Mean Corpuscular Haemoglobin Concentration (MCHC) | mchc | PRESENT_AS_ALIAS |
| Red Cell Distribution Width (RDW-CV) | rdw_cv | PRESENT_AS_ALIAS |
| Red Cell Distribution Width SD (RDW-SD) | rdw_sd | PRESENT_AS_ALIAS |
| Platelets (PLT) | platelets | PRESENT_AS_ALIAS |
| Mean Platelet Volume (MPV) | mpv | PRESENT_AS_ALIAS |
| Platelet Distribution Width (PDW) | pdw | PRESENT_AS_ALIAS |
| Neutrophil (NEU %) | neutrophil_pct | PRESENT_AS_ALIAS |
| Neutrophil (NEU #) | neutrophils_abs | PRESENT_AS_ALIAS |
| Lymphocyte (LYM %) | lymphocyte_pct | PRESENT_AS_ALIAS |
| Lymphocyte (LYM #) | lymphocytes_abs | PRESENT_AS_ALIAS |
| Monocyte (MON %) | monocyte_pct | PRESENT_AS_ALIAS |
| Monocyte (MON #) | monocytes_abs | PRESENT_AS_ALIAS |
| Eosinophils (EOS %) | eosinophil_pct | PRESENT_AS_ALIAS |
| Eosinophils (EOS #) | eosinophils_abs | PRESENT_AS_ALIAS |
| Basophils (BAS %) | basophil_pct | PRESENT_AS_ALIAS |
| Basophils (BAS #) | basophils_abs | PRESENT_AS_ALIAS |
| Thyroglobulin Antibodies (TgAb) | tgab | PRESENT_AS_ALIAS |
| Thyroid Peroxidase Antibodies (TPO Ab) | tpo_ab | PRESENT_AS_ALIAS |
| Free T4 | free_t4 | PRESENT_AS_ALIAS |
| Free T3 | free_t3 | PRESENT_AS_ALIAS |
| TSH | tsh | PRESENT_AS_ALIAS |
| Zinc | zinc | PRESENT_AS_ALIAS |
| Vitamin D | vitamin_d | PRESENT_AS_ALIAS |
| Active Vitamin B12 | active_b12 | PRESENT_AS_ALIAS |
| Vitamin B12 | vitamin_b12 | PRESENT_AS_ALIAS |
| Folic Acid | folate | PRESENT_AS_ALIAS |
| Oestradiol | oestradiol | PRESENT_AS_ALIAS |
| Free Testosterone Calculation | free_testosterone | PRESENT_AS_ALIAS |
| Free Testosterone % Calculation | free_testosterone_pct | PRESENT_AS_ALIAS |
| Testosterone : Free Testosterone Ratio | testosterone_free_testosterone_ratio | PRESENT_AS_ALIAS |
| Luteinizing Hormone (LH) | lh | PRESENT_AS_ALIAS |
| FSH | fsh | PRESENT_AS_ALIAS |
| Sex Hormone Binding Globulin (SHBG) | shbg | PRESENT_AS_ALIAS |
| Testosterone | testosterone | PRESENT_AS_ALIAS |
| Prolactin | prolactin | PRESENT_AS_ALIAS |
| Cortisol | cortisol | PRESENT_AS_ALIAS |
| Free Androgen Index (FAI) | fai | PRESENT_AS_ALIAS |
| DHEA | dhea | PRESENT_AS_ALIAS |
| eGFR | egfr | PRESENT_AS_ALIAS |
| Creatinine | creatinine | PRESENT_AS_ALIAS |
| Urea | urea | PRESENT_AS_ALIAS |
| Uric Acid | urate | PRESENT_AS_ALIAS |
| Apolipoprotein B | apob | PRESENT_AS_ALIAS |
| Apolipoprotein A1 | apoa1 | PRESENT_AS_ALIAS |
| Apolipoprotein ratio | apoB_apoA1_ratio | PRESENT_AS_ALIAS |
| Low Density Lipoproteins | ldl_cholesterol | PRESENT_AS_ALIAS |
| HDL | hdl_cholesterol | PRESENT_AS_ALIAS |
| Cholesterol (Total) | total_cholesterol | PRESENT_AS_ALIAS |
| Triglycerides | triglycerides | PRESENT_AS_ALIAS |
| Non HDL Cholesterol | non_hdl_cholesterol | PRESENT_AS_ALIAS |
| Total Cholesterol/HDL Ratio | tc_hdl_ratio | PRESENT_AS_ALIAS |
| Lipoprotein (A) | lipoprotein_a | PRESENT_AS_ALIAS |
| Homocysteine | homocysteine | PRESENT_AS_ALIAS |
| C-Reactive Protein CRP | crp | PRESENT_AS_ALIAS |
| HbA1c % | hba1c_pct | PRESENT_AS_ALIAS |
| HbA1c (mmol/mol) | hba1c | PRESENT_AS_ALIAS |
| Transferrin | transferrin | PRESENT_AS_ALIAS |
| Serum Iron | iron | PRESENT_AS_ALIAS |
| Ferritin | ferritin | PRESENT_AS_ALIAS |
| Alanine AminoTransferase ALT | alt | PRESENT_AS_ALIAS |
| Gamma-GlutamylTransferase GGT | ggt | PRESENT_AS_ALIAS |
| Alkaline Phosphatase ALP | alp | PRESENT_AS_ALIAS |
| Bilirubin Total | bilirubin | PRESENT_AS_ALIAS |
| Albumin | albumin | PRESENT_AS_ALIAS |
| Total Protein | total_protein | PRESENT_AS_ALIAS |
| Globulin Calculation | globulin | PRESENT_AS_ALIAS |
| Total Creatine Kinase CK | creatine_kinase | PRESENT_AS_ALIAS |
| Sodium | sodium | PRESENT_AS_ALIAS |
| Potassium | potassium | PRESENT_AS_ALIAS |
| Calcium | calcium | PRESENT_AS_ALIAS |
| Chloride | chloride | PRESENT_AS_ALIAS |
| Magnesium | magnesium | PRESENT_AS_ALIAS |
| Corrected Calcium | corrected_calcium | PRESENT_AS_ALIAS |

### B) Coverage counts

| Status | Count |
|--------|------:|
| PRESENT_AS_CANONICAL | 0 |
| PRESENT_AS_ALIAS | 79 |
| MISSING | 0 |
| AMBIGUOUS | 0 |

### C) Known risk area: wbc vs white_blood_cells — RESOLVED

**Evidence (post-fix):**

- **Staging** (`backend/ssot/_ab_panel_staging/ab_panel_biomarkers.yaml` lines 10–22):
  ```yaml
  white_blood_cells:
    aliases: ["wbc", "leukocytes"]
    unit: "K/μL"
    description: "White blood cell count"
    category: "cbc"
    system: "hematological"
    ...
  ```
  Canonical = `white_blood_cells`; `wbc` is alias. Definition matches production.

- **Staging alias** (`ab_panel_alias_registry.yaml`): `canonical_id: white_blood_cells` with AB raw labels.

- **Runtime references** (`clusters.yaml`, `scoring_policy.yaml`, `criticality.yaml`, `ranges.yaml`, `system_burden_registry.yaml`) all use `white_blood_cells` — no conflict.

**rbc, hgb, hct:** No duplicate canonicals. Staging uses `rbc`, `hemoglobin`, `hematocrit`; production has `hemoglobin`, `hematocrit`; `rbc` is NEW_IN_AB. No conflict.

---

## Task 2 — Collision and Invariants Audit

### Validator run (staging-only)

**Command:** `python backend/scripts/validate_ab_panel_ssot.py`

**Result:** OVERALL: PASS

| Check | Status |
|-------|--------|
| CHECK 0 — AB Full Panel Completeness | PASS |
| CHECK 1 — System Allowlist Enforcement | PASS |
| CHECK 2 — Canonical Naming Standards | PASS |
| CHECK 3 — Duplicate Canonical ID Drift | PASS |
| CHECK 4 — Burden Registry Coverage | PASS |
| CHECK 5 — Risk Direction Validity | PASS |
| CHECK 6 — Alias Collision Detection | PASS |
| CHECK 7 — Derived Marker Separation | PASS |

**Counts:** n_ab_biomarkers=78, n_ab_burden_entries=78, n_ab_aliases=78, n_raw_labels_resolvable=385

### Collision / invariant summary

| Check | Result |
|-------|--------|
| Alias collision status | No collisions (CHECK 6 PASS) |
| Canonical ID uniqueness | All unique (CHECK 2, 3 PASS) |
| Alias → missing canonical | None (validator enforces canonical_id ∈ ab_biomarkers) |
| Derived marker separation | PASS (CHECK 7) — no derived markers incorrectly in primary list |

### Staging vs runtime diff summary

**Source:** `backend/scripts/report_ab_panel_delta.py` output + manual comparison.

#### File 1: biomarkers

| Delta type | Details |
|------------|---------|
| **Added canonical IDs** | 44: active_b12, albumin, alp, basophil_pct, bilirubin, cortisol, dhea, egfr, eosinophil_pct, fai, folate, free_t3, free_testosterone, free_testosterone_pct, fsh, ggt, globulin, hba1c_pct, homocysteine, iron, lh, lipoprotein_a, lymphocyte_pct, mch, mchc, mcv, monocyte_pct, mpv, neutrophil_pct, oestradiol, pdw, prolactin, rbc, rdw_cv, rdw_sd, shbg, testosterone, total_protein, tpo_ab, transferrin, urate, vitamin_b12, wbc, zinc |
| **Removed canonical IDs** | 11 (informational, staging is superset): ast, ast_alt_ratio, glucose, insulin, ldl_hdl_ratio, lymphocytes, neutrophils, nlr, tg_hdl_ratio, urea_creatinine_ratio, white_blood_cells |
| **Changed fields** | 33 production canonicals have matching staging definitions (CHECK 3 notes); unit/system/description aligned for overlap |
| **Scoring/clustering impact** | `white_blood_cells` → `wbc` canonical swap breaks clusters, scoring_policy, burden, ranges, criticality |

#### File 2: alias registry

| Delta type | Details |
|------------|---------|
| **Added aliases** | 344 AB-only raw labels (see `backend/reports/ab_panel_delta_report.md` §4) |
| **Removed aliases** | None (staging is additive) |
| **Structure** | Staging uses `ab_full_panel` list; runtime uses flat `canonical_id`/`aliases`; migration must merge |

#### File 3: system burden

| Delta type | Details |
|------------|---------|
| **Added burden entries** | 44 (one per NEW_IN_AB canonical) |
| **Removed burden entries** | 11 (for MISSING_FROM_AB) |
| **Changed fields** | Production overlap entries match (CHECK 3) |
| **Scoring impact** | Staging uses `white_blood_cells`; aligned with production |

---

## Task 3 — Migration Readiness Recommendation

### Final status: **READY_TO_MIGRATE**

**Verification (2026-02-27):**
- `validate_ab_panel_ssot.py`: OVERALL PASS
- No canonical fracture (wbc eliminated; white_blood_cells canonical in staging)
- No new alias collisions
- testosterone_free_testosterone_ratio added with lab-supplied + computed fallback

### Resolved (previously blockers)

1. ~~wbc vs white_blood_cells~~ — **RESOLVED**: Staging uses `white_blood_cells`; definition matches production.
2. ~~Testosterone : Free Testosterone Ratio missing~~ — **RESOLVED**: Added canonical, alias, burden, and RatioRegistry compute fallback.

### Remaining considerations (non-blocking)

- **MISSING_FROM_AB production canonicals**: Migration must merge (not replace) so production-only canonicals (ast, glucose, insulin, nlr, etc.) remain.
- **Alias registry merge strategy**: Staging `ab_full_panel` list must be merged into runtime flat structure.

### Migration plan (when executing)

1. Merge staging into runtime:
   - `biomarkers.yaml`: Merge `ab_panel_biomarkers.yaml` into production (add new, preserve production-only).
   - `biomarker_alias_registry.yaml`: Convert `ab_full_panel` list to flat entries; merge with production.
   - `system_burden_registry.yaml`: Merge burden entries (add new, preserve production-only).
2. Run `validate_ab_panel_ssot.py` and enforcement tests post-migration.

---

## Appendix: Evidence file paths

| Evidence | Path |
|----------|------|
| Validator | `backend/scripts/validate_ab_panel_ssot.py` |
| Delta report | `backend/reports/ab_panel_delta_report.md` |
| Staging biomarkers | `backend/ssot/_ab_panel_staging/ab_panel_biomarkers.yaml` |
| Staging alias | `backend/ssot/_ab_panel_staging/ab_panel_alias_registry.yaml` |
| Staging burden | `backend/ssot/_ab_panel_staging/ab_panel_system_burden_registry.yaml` |
| Production biomarkers | `backend/ssot/biomarkers.yaml` |
| Production white_blood_cells | `backend/ssot/biomarkers.yaml` lines 482–483 |
| Clusters | `backend/ssot/clusters.yaml` |
| Scoring policy | `backend/ssot/scoring_policy.yaml` |
| Ratio registry (code) | `backend/core/analytics/ratio_registry.py` |
