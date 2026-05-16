---
work_id: LC-S8C-PREFLIGHT
branch: launch-core/lc-s8c-ssot-wide-unit-governance-preflight
risk_level: STANDARD
change_type: CONTENT
date: 2026-05-16
---

# LC-S8C-PREFLIGHT — SSOT-Wide UK/SI Unit Governance Validation

**Classification:** STANDARD-risk CONTENT (evidence-gathering and policy authoring only).  
**Authority:** Extends [LC-S8B](LC-S8B_uk_canonical_unit_policy_validation.md) (31 UK-policy rows) to the **full** SSOT inventory (**103 biomarkers**).  
**No runtime, SSOT, registry, Sentinel, frontend, or test files were modified.**

**Human review status (2026-05-16):** **APPROVED WITH CONDITIONS — WORKING ARCHITECTURAL BASIS ONLY** — evidence-quality addendum (§19) accepted. **Not final clinical evidence authority.** Branch provenance corrected in §3. **No implementation sprint** may start until a separate HIGH-risk remediation prompt is authored and hardened.

---

## 1. Executive summary

HealthIQ AI v5 has a **complete SSOT biomarker inventory (103 IDs)** in [`backend/ssot/biomarkers.yaml`](../../backend/ssot/biomarkers.yaml), but **UK/SI Layer B analytical unit policy is not enforced consistently** across SSOT labels, [`units.yaml`](../../backend/ssot/units.yaml), [`registry.py`](../../backend/core/units/registry.py), [`scoring_policy.yaml`](../../backend/ssot/scoring_policy.yaml), Layer C display, and Sentinel.

**Key findings:**

| Finding | Count / status |
|---------|----------------|
| Biomarkers inventoried | **103** |
| Already UK/SI compliant at SSOT (`COMPLIANT_NO_CHANGE`) | **77** |
| Label equivalence only (Phase A) | **5** (`platelets`, `white_blood_cells`, `sodium`, `potassium`, `chloride`) |
| True conversion blocked pending primary evidence (Phase B) | **4** (`calcium`, `corrected_calcium`, `magnesium`, `free_t4`) + **2** with factors pending sign-off (`hemoglobin`, `urate`) |
| Layer B scoring-policy unit migration (Phase C) | **8** scored markers + **hba1c_pct** merge |
| Layer C display policy (Phase D) | **urea/BUN**, **vitamin_d**, secondary display for HbA1c/HCT/US lipids |
| Dual authority: SSOT UK units vs `scoring_policy.yaml` US bands | **glucose**, **lipids**, **creatinine** |
| Duplicate HbA1c analytical identity | `hba1c` + `hba1c_pct` (arbitration mitigates API path; SSOT/KB remain) |

This document is a **working governance table** for the later HIGH-risk remediation sprint. §4 alone is **not** final clinical authority (see §19). Implementation must follow **phased STOP gates** (§20; LC-S8C pre-sprint note §5.2). **Do not begin implementation** until this addendum is reviewed on the correct work-package branch.

---

## 2. Direct answers to the three governance questions

### Q1 — Does every biomarker in `biomarkers.yaml` have a validated UK/SI canonical analytical unit for Layer B?

**Answer: Yes for policy assignment; partial for SSOT alignment.**

| Status | Count | Meaning |
|--------|-------|---------|
| Layer B unit declared in §4 table | **103 / 103** | Every row has a proposed UK/SI (or internationally standard) Layer B analytical unit |
| SSOT `unit:` already matches Layer B | **77** | `COMPLIANT_NO_CHANGE` |
| SSOT label drift (US customary canonical) | **16** | Requires equivalence, conversion, or scoring migration |
| `BLOCKED_PENDING_EVIDENCE` | **4** | Ca, corrected Ca, Mg, fT4 — no primary-source factor in repo |

No launch-critical biomarker is left without a defensible Layer B unit. Phase B rows are **blocked for implementation** until conversion factors are cited to NHS/lab primary sources.

### Q2 — What is the primary Layer B calculation unit for every biomarker?

**Answer:** See **§4 Whole-SSOT unit governance table** column **UK/SI primary analytical unit for Layer B**.  

Representative launch-critical mappings:

| Domain | Layer B unit (UK-first) | Current SSOT drift |
|--------|-------------------------|-------------------|
| Lipids, glucose | `mmol/L` | SSOT OK; **scoring_policy** uses `mg/dL` |
| Creatinine | `µmol/L` | SSOT OK; **scoring_policy** uses `mg/dL` |
| Urea (incl. BUN alias) | `mmol/L` | Aligned |
| HbA1c | `mmol/mol` (IFCC) | SSOT `%`; norm → `%` |
| Haematocrit | `L/L` | SSOT `%`; norm → `%` |
| FBC counts | `10^9/L` / `10^12/L` | `K/μL` for PLT/WBC |
| Electrolytes | `mmol/L` | `mEq/L` label |
| Haemoglobin | `g/L` | `g/dL` |
| Minerals / thyroid | `mmol/L` / `pmol/L` | `mg/dL` / `ng/dL` |

### Q3 — What is the governed Layer C / frontend display-unit policy?

**Answer: Not yet implemented.** Layer C must remain **renderer-only** for unit conversion; governed display rules are **backend-authored**. Layer C operates in **two presentation modes** (§10.1) — uploaded-panel fidelity vs analytical-report collapse. Locale-specific secondary display units (UK vs US) remain in [`display_unit_policy.yaml`](../../backend/ssot/display_unit_policy.yaml) (proposed).

| User cohort | Policy |
|-------------|--------|
| **UK users** | Analytical-report mode: display unit = Layer B analytical unit unless a governed row allows **coherent** secondary form (e.g. HCT `%` when value and reference range are both transformed) |
| **US / non-UK users** | Same Layer B canonical internally; optional **display-only** familiar units via `display_unit` / `display_value` on analysis DTO — **not** client-side conversion |
| **Ownership (proposed)** | [`backend/ssot/display_unit_policy.yaml`](../../backend/ssot/display_unit_policy.yaml) keyed by `biomarker_id`, `locale`, `presentation_mode`, `display_unit` |

Frontend today passes through `biomarker.unit` from API ([`results/page.tsx`](../../frontend/app/(app)/results/page.tsx)); LC-S7 in [`BiomarkerDials.tsx`](../../frontend/app/components/biomarkers/BiomarkerDials.tsx) only **suppresses** incoherent reference bands — it does not convert.

---

## 3. Current SSOT biomarker inventory

### Preflight commands (recorded at closure on work-package branch)

```text
Branch: launch-core/lc-s8c-ssot-wide-unit-governance-preflight
Status:
?? docs/audit-papers/LC-S8C_pre_sprint_unit_policy_validation_note.md

git log --oneline -n 5  (recorded at closure; branch tip = commit containing this file):
docs(LC-S8C): SSOT-wide unit governance preflight audit (closure)
4828d5d docs(LC-S8B): architectural review remediation — evidence and counts
0982034 chore(bus): LC-S8B kernel COMPLETE status
da64898 chore(bus): LC-S8B kernel IN_PROGRESS status
2f83b2d docs(LC-S8B): UK canonical unit policy validation table
```

### Branch provenance — resolved

| Item | Value |
|------|--------|
| Work-package branch (YAML front matter) | `launch-core/lc-s8c-ssot-wide-unit-governance-preflight` |
| Branch at closure (`git branch --show-current`) | `launch-core/lc-s8c-ssot-wide-unit-governance-preflight` (matches YAML front matter) |
| Initial authoring | Occurred on `main` before WP branch existed; audit squashed to single commit on WP branch at closure |
| Status | **Resolved** — verify tip with `git log -1` on this branch; §3 block recorded at closure |

### File scope — confirmation (Condition 2)

| Path | Role in LC-S8C-PREFLIGHT | Created/modified by preflight agent? |
|------|--------------------------|--------------------------------------|
| `docs/audit-papers/LC-S8C_ssot_wide_unit_governance_preflight.md` | **Deliverable** | **Yes — created** (this file) |
| `docs/audit-papers/LC-S8C_pre_sprint_unit_policy_validation_note.md` | Prior input (read-only) | **No** — already present as untracked before this sprint; not authored as part of LC-S8C-PREFLIGHT deliverable |
| `backend/ssot/*`, `backend/core/*`, `frontend/*`, `sentinel/*`, tests, fixtures, KB | Forbidden | **No changes** |
| Ephemeral generator scripts under `scripts/` | Internal tooling | **Removed** after assembly; not part of deliverable |

**Confirmation:** For the LC-S8C-PREFLIGHT sprint scope, **only** `docs/audit-papers/LC-S8C_ssot_wide_unit_governance_preflight.md` was intentionally created. No other tracked files were modified. (The pre-sprint note may appear in `git status` from an earlier session.)

**Inventory script:** `COUNT=103` biomarkers under `biomarkers:` dict in `backend/ssot/biomarkers.yaml`.

**Select-String sample** (unit-related hits in SSOT/core/tests): confirms `hba1c` `%`, `urea`/`BUN` aliases, `mEq/L` electrolytes, `K/μL` counts, `µmol/L` creatinine, mmol/L lipids — see repository grep output in sprint working notes.

### Authority files reviewed

| File | Path | Role |
|------|------|------|
| ADR-001 | `architecture/ADR-001-platform-non-negotiables.md` | SSOT invariants |
| ADR-002 | `architecture/ADR-002-deterministic-analysis-engine.md` | Layer A/B/C separation |
| Master PRD v5.2 | `architecture/Master_PRD_v5.2.md` | Product architecture |
| Biomarkers | `backend/ssot/biomarkers.yaml` | 103 canonical IDs |
| Units | `backend/ssot/units.yaml` | Conversions + definitions |
| Registry | `backend/core/units/registry.py` | Layer A normalisation |
| Aliases | `backend/ssot/biomarker_alias_registry.yaml` | BUN, uric acid, HbA1c |
| Scoring | `backend/ssot/scoring_policy.yaml` | Layer B bands (US mg/dL for several) |
| System burden | `backend/ssot/system_burden_registry.yaml` | `hba1c` + `hba1c_pct` |
| LC-S8B | `docs/audit-papers/LC-S8B_uk_canonical_unit_policy_validation.md` | 31-row policy seed |
| LC-S8C note | `docs/audit-papers/LC-S8C_pre_sprint_unit_policy_validation_note.md` | Phased STOP gates |

---

## 4. Whole-SSOT unit governance table

**103 rows — one per biomarker ID in SSOT.**

**Evidence authority warning:** The **Evidence source** column in §4 uses mixed quality. Rows with vague wording (e.g. “UK SI concentration”, “SSOT unit accepted UK/SI or international”, “audit”, “TBD”, “US alt if applicable”) are **not final clinical authority**. Per-row classification and implementation permission are in **§19**.

| Biomarker ID | Display name | Current SSOT unit | Current aliases | UK/SI primary analytical unit for Layer B | Accepted UK input units | Accepted US/non-UK input units | UK display unit | US/non-UK display unit | Conversion/equivalence required | Current registry support | Current scoring-policy unit | Layer B migration needed? | Layer C display policy needed? | Evidence source | Decision | Implementation phase |
| ------------ | ------------ | ----------------- | --------------- | ----------------------------------------- | ----------------------- | ------------------------------ | --------------- | ---------------------- | ------------------------------- | ------------------------ | --------------------------- | ------------------------- | ------------------------------ | --------------- | -------- | -------------------- |
| `acth` | acth | pmol/L | adrenocorticotropic_hormone | pmol/L | pmol/L | US alt if applicable | pmol/L | pmol/L | no | no | — | no | no | UK SI concentration | COMPLIANT_NO_CHANGE | DEFER |
| `active_b12` | active_b12 | pmol/L |  | pmol/L | pmol/L | US alt if applicable | pmol/L | pmol/L | no | no | — | no | no | UK SI concentration | COMPLIANT_NO_CHANGE | DEFER |
| `albumin` | albumin | g/L |  | g/L | g/L | g/L | g/L | g/L | no | no | — | no | no | ADR-002 proteins g/L | COMPLIANT_NO_CHANGE | DEFER |
| `aldolase` | aldolase | U/L | serum_aldolase | U/L | U/L | U/L | U/L | U/L | no | no | — | no | no | UK reports U/L (RCPath) | COMPLIANT_NO_CHANGE | DEFER |
| `alp` | alp | U/L |  | U/L | U/L | U/L | U/L | U/L | no | no | — | no | no | UK reports U/L (RCPath) | COMPLIANT_NO_CHANGE | DEFER |
| `alt` | alt | U/L | alt, alanine_aminotransferase, sgpt | U/L | U/L | U/L | U/L | U/L | no | no | U/L | no | no | UK reports U/L (RCPath) | COMPLIANT_NO_CHANGE | DEFER |
| `apoa1` | apoa1 | g/L | apo_a1, apolipoprotein_a1 | g/L | g/L | g/L | g/L | g/L | no | no | — | no | no | ADR-002 proteins g/L | COMPLIANT_NO_CHANGE | DEFER |
| `apob` | apob | g/L | apo_b, apolipoprotein_b | g/L | g/L | g/L | g/L | g/L | no | no | — | no | no | ADR-002 proteins g/L | COMPLIANT_NO_CHANGE | DEFER |
| `apob_apoa1_ratio` | apob_apoa1_ratio | ratio |  | ratio | ratio | ratio | ratio | ratio | no | n/a | — | no | no | Dimensionless derived | COMPLIANT_NO_CHANGE | DEFER |
| `ast` | ast | U/L | aspartate_aminotransferase, sgot | U/L | U/L | U/L | U/L | U/L | no | no | U/L | no | no | UK reports U/L (RCPath) | COMPLIANT_NO_CHANGE | DEFER |
| `ast_alt_ratio` | ast_alt_ratio | ratio |  | ratio | ratio | ratio | ratio | ratio | no | n/a | — | no | no | Dimensionless derived | COMPLIANT_NO_CHANGE | DEFER |
| `basophil_pct` | basophil_pct | % |  | % | % | % | % | % | no | n/a | — | no | optional | Differential % | REMOVE_OR_DEFER_NOT_LAUNCH_CRITICAL | DEFER |
| `basophils_abs` | basophils_abs | 10^9/L | basophils_(bas_#), basophils_abs_count | 10^9/L | 10^9/L | K/μL | 10^9/L | K/μL | no | no | — | no | no | UK FBC absolute | COMPLIANT_NO_CHANGE | DEFER |
| `bilirubin` | bilirubin | umol/L |  | µmol/L | µmol/L, umol/L | mg/dL where applicable | µmol/L | mg/dL | partial | spelling only | — | no | no | UK µmol/L | COMPLIANT_NO_CHANGE | DEFER |
| `calcium` | calcium | mg/dL | calcium_(venous) | mmol/L | mmol/L | mg/dL | mmol/L | mg/dL (US display optional) | yes — mg/dL↔mmol/L | no | — | no | yes | NICE CKD mmol/L; factor not in units.yaml | BLOCKED_PENDING_EVIDENCE | PHASE_B_TRUE_CONVERSION |
| `chloride` | chloride | mEq/L | chloride_(venous) | mmol/L | mmol/L | mEq/L | mmol/L | mmol/L | yes — 1:1 equivalence | no | — | yes | optional | UK NHS mmol/L; LC-S8B | ADD_EQUIVALENCE_ONLY | PHASE_A_SAFE_EQUIVALENCE |
| `corrected_calcium` | corrected_calcium | mg/dL | corrected_calcium_(venous) | mmol/L | mmol/L | mg/dL | mmol/L | mg/dL | yes | no | — | no | optional | Same as calcium | BLOCKED_PENDING_EVIDENCE | PHASE_B_TRUE_CONVERSION |
| `cortisol` | cortisol | nmol/L |  | nmol/L | nmol/L | US alt if applicable | nmol/L | nmol/L | no | no | — | no | no | UK SI concentration | COMPLIANT_NO_CHANGE | DEFER |
| `creatine_kinase` | creatine_kinase | U/L | total_creatine_kinase, total_ck, ck_total, creatine_kinase_(total), total_creatine_kinese_ck_(venous) | U/L | U/L | U/L | U/L | U/L | no | no | — | no | no | UK reports U/L (RCPath) | COMPLIANT_NO_CHANGE | DEFER |
| `creatinine` | creatinine | µmol/L | creat, serum_creatinine | µmol/L | µmol/L, umol/L | mg/dL | µmol/L | mg/dL | yes | yes | mg/dL | yes | yes | UK µmol/L; scoring_policy mg/dL | MIGRATE_LAYER_B_SCORING_UNIT | PHASE_C_LAYER_B_SCORING_MIGRATION |
| `crp` | crp | mg/L | c_reactive_protein, hs_crp, high_sensitivity_crp, c-reactive_protein_crp_(venous) | mg/L | mg/L | TBD | mg/L | mg/L | audit | no | mg/L | no | no | SSOT unit accepted UK/SI or international | COMPLIANT_NO_CHANGE | DEFER |
| `cystatin_c` | cystatin_c | mg/L | cystatin_c_serum | mg/L | mg/L | TBD | mg/L | mg/L | audit | no | — | no | no | SSOT unit accepted UK/SI or international | COMPLIANT_NO_CHANGE | DEFER |
| `dhea` | dhea | umol/L |  | µmol/L | µmol/L, umol/L | mg/dL where applicable | µmol/L | mg/dL | partial | spelling only | — | no | no | UK µmol/L | COMPLIANT_NO_CHANGE | DEFER |
| `dhea_s` | dhea_s | umol/L | dheas, dhea_sulfate, dehydroepiandrosterone_sulfate | µmol/L | µmol/L, umol/L | mg/dL where applicable | µmol/L | mg/dL | partial | spelling only | — | no | no | UK µmol/L | COMPLIANT_NO_CHANGE | DEFER |
| `egfr` | egfr | mL/min/1.73m2 |  | mL/min/1.73m2 | mL/min/1.73m2 | mL/min/1.73m2 | mL/min/1.73m2 | mL/min/1.73m2 | no | no | — | no | no | eGFR UK reporting | COMPLIANT_NO_CHANGE | DEFER |
| `eosinophil_pct` | eosinophil_pct | % |  | % | % | % | % | % | no | n/a | — | no | optional | Differential % | REMOVE_OR_DEFER_NOT_LAUNCH_CRITICAL | DEFER |
| `eosinophils_abs` | eosinophils_abs | 10^9/L | eosinophils_(eos_#), eosinophils_abs_count | 10^9/L | 10^9/L | K/μL | 10^9/L | K/μL | no | no | — | no | no | UK FBC absolute | COMPLIANT_NO_CHANGE | DEFER |
| `fai` | fai | % |  | % | % | % | % | % | no | no | — | no | no | Dimensionless % | COMPLIANT_NO_CHANGE | DEFER |
| `ferritin` | ferritin | ng/mL | ferritin_(venous) | ng/mL | ng/mL | TBD | ng/mL | ng/mL | audit | no | — | no | no | SSOT unit accepted UK/SI or international | COMPLIANT_NO_CHANGE | DEFER |
| `fib_4` | fib_4 | ratio |  | ratio | ratio | ratio | ratio | ratio | no | n/a | — | no | no | Dimensionless derived | COMPLIANT_NO_CHANGE | DEFER |
| `folate` | folate | ug/L |  | µg/L | µg/L | ng/mL | µg/L | ng/mL | possible | no | — | no | no | Folate UK µg/L | COMPLIANT_NO_CHANGE | DEFER |
| `free_t3` | free_t3 | pmol/L |  | pmol/L | pmol/L | US alt if applicable | pmol/L | pmol/L | no | no | — | no | no | UK SI concentration | COMPLIANT_NO_CHANGE | DEFER |
| `free_t4` | free_t4 | ng/dL | free_thyroxine, freet4 | pmol/L | pmol/L | ng/dL | pmol/L | ng/dL | yes | no | — | no | yes | NICE thyroid pmol/L | BLOCKED_PENDING_EVIDENCE | PHASE_B_TRUE_CONVERSION |
| `free_testosterone` | free_testosterone | pmol/L |  | pmol/L | pmol/L | US alt if applicable | pmol/L | pmol/L | no | no | — | no | no | UK SI concentration | COMPLIANT_NO_CHANGE | DEFER |
| `free_testosterone_pct` | free_testosterone_pct | % |  | % | % | % | % | % | no | n/a | — | no | optional | Free androgen index %; dimensionless | COMPLIANT_NO_CHANGE | DEFER |
| `fsh` | fsh | mIU/mL |  | mIU/mL | mIU/mL | TBD | mIU/mL | mIU/mL | audit | no | — | no | no | SSOT unit accepted UK/SI or international | COMPLIANT_NO_CHANGE | DEFER |
| `ggt` | ggt | U/L |  | U/L | U/L | U/L | U/L | U/L | no | no | — | no | no | UK reports U/L (RCPath) | COMPLIANT_NO_CHANGE | DEFER |
| `globulin` | globulin | g/L |  | g/L | g/L | g/L | g/L | g/L | no | no | — | no | no | ADR-002 proteins g/L | COMPLIANT_NO_CHANGE | DEFER |
| `glucose` | glucose | mmol/L | blood_sugar, blood_glucose, sugar | mmol/L | mmol/L | mg/dL | mmol/L | mg/dL | yes | yes | mg/dL | yes | yes | UK SI mmol/L; scoring_policy mg/dL mismatch | MIGRATE_LAYER_B_SCORING_UNIT | PHASE_C_LAYER_B_SCORING_MIGRATION |
| `hba1c` | hba1c | % | hemoglobin_a1c, a1c, glycated_hemoglobin | mmol/mol | mmol/mol, % | % | mmol/mol | % (secondary display only) | yes — IFCC↔% | yes | % | yes | yes | NICE NG28 IFCC; DH 2009 switch | MIGRATE_LAYER_B_SCORING_UNIT | PHASE_C_LAYER_B_SCORING_MIGRATION |
| `hba1c_pct` | hba1c_pct | % |  | mmol/mol (via hba1c) | %, mmol/mol | % | as hba1c | % secondary | merge to hba1c | arbitration only | — | yes | optional | Deprecate independent SSOT row; alias-only | MERGE_OR_DEPRECATE_DUPLICATE_BIOMARKER | PHASE_C_LAYER_B_SCORING_MIGRATION |
| `hdl_cholesterol` | hdl_cholesterol | mmol/L | hdl, hdl_chol, good_cholesterol | mmol/L | mmol/L | mg/dL | mmol/L | mg/dL | yes | yes | mg/dL | yes | yes | UK lipids | MIGRATE_LAYER_B_SCORING_UNIT | PHASE_C_LAYER_B_SCORING_MIGRATION |
| `hematocrit` | hematocrit | % | hct, pcv | L/L | L/L, % (coherent pair) | % | L/L or % (coherent) | % (coherent only) | yes — L/L↔% | yes | % | yes | yes | Gloucestershire/NBT NHS L/L; LC-S8C pre-sprint | MIGRATE_LAYER_B_SCORING_UNIT | PHASE_C_LAYER_B_SCORING_MIGRATION |
| `hemoglobin` | hemoglobin | g/dL | hgb, hb, haemoglobin | g/L | g/L | g/dL | g/L | g/dL (US display optional) | yes — ×10 scale | yes | g/dL | no | yes | ADR-002 g/L proteins; NHS g/L; BLOCKED_PENDING_EVIDENCE until handbook sign-off | ADD_TRUE_CONVERSION | PHASE_B_TRUE_CONVERSION |
| `homa_ir` | homa_ir | ratio |  | ratio | ratio | ratio | ratio | ratio | no | n/a | — | no | no | Dimensionless derived | COMPLIANT_NO_CHANGE | DEFER |
| `homocysteine` | homocysteine | umol/L |  | µmol/L | µmol/L, umol/L | mg/dL where applicable | µmol/L | mg/dL | partial | spelling only | — | no | no | UK µmol/L | COMPLIANT_NO_CHANGE | DEFER |
| `insulin` | insulin | μU/mL | insulin_level, serum_insulin | μU/mL | μU/mL | TBD | μU/mL | μU/mL | audit | no | μU/mL | no | no | SSOT unit accepted UK/SI or international | COMPLIANT_NO_CHANGE | DEFER |
| `iron` | iron | umol/L |  | µmol/L | µmol/L, umol/L | mg/dL where applicable | µmol/L | mg/dL | partial | spelling only | — | no | no | UK µmol/L | COMPLIANT_NO_CHANGE | DEFER |
| `ldl_cholesterol` | ldl_cholesterol | mmol/L | ldl, ldl_chol, bad_cholesterol | mmol/L | mmol/L | mg/dL | mmol/L | mg/dL | yes | yes | mg/dL | yes | yes | UK lipids | MIGRATE_LAYER_B_SCORING_UNIT | PHASE_C_LAYER_B_SCORING_MIGRATION |
| `ldl_hdl_ratio` | ldl_hdl_ratio | ratio |  | ratio | ratio | ratio | ratio | ratio | no | n/a | — | no | no | Dimensionless derived | COMPLIANT_NO_CHANGE | DEFER |
| `lh` | lh | mIU/mL |  | mIU/mL | mIU/mL | TBD | mIU/mL | mIU/mL | audit | no | — | no | no | SSOT unit accepted UK/SI or international | COMPLIANT_NO_CHANGE | DEFER |
| `lipoprotein_a` | lipoprotein_a | g/L |  | g/L | g/L | g/L | g/L | g/L | no | no | — | no | no | ADR-002 proteins g/L | COMPLIANT_NO_CHANGE | DEFER |
| `lymphocyte_pct` | lymphocyte_pct | % |  | % | % | % | % | % | no | n/a | — | no | optional | LC-S8B defer | REMOVE_OR_DEFER_NOT_LAUNCH_CRITICAL | DEFER |
| `lymphocytes` | lymphocytes | 10^9/L | lymphocyte_count, lymphocytes_(venous) | 10^9/L | 10^9/L | K/μL | 10^9/L | K/μL | no | no | — | no | no | UK FBC absolute | COMPLIANT_NO_CHANGE | DEFER |
| `lymphocytes_abs` | lymphocytes_abs | 10^9/L | lymphocyte_(lym_#), lymphocytes_abs_count | 10^9/L | 10^9/L | K/μL | 10^9/L | K/μL | no | no | — | no | no | UK FBC absolute | COMPLIANT_NO_CHANGE | DEFER |
| `magnesium` | magnesium | mg/dL | magnesium_(venous) | mmol/L | mmol/L | mg/dL | mmol/L | mg/dL | yes | no | — | no | optional | UK panels mmol/L | BLOCKED_PENDING_EVIDENCE | PHASE_B_TRUE_CONVERSION |
| `mch` | mch | pg |  | pg | pg | pg | pg | pg | no | no | — | no | no | MCH pg | COMPLIANT_NO_CHANGE | DEFER |
| `mchc` | mchc | g/L |  | g/L | g/L | g/L | g/L | g/L | no | no | — | no | no | ADR-002 proteins g/L | COMPLIANT_NO_CHANGE | DEFER |
| `mcv` | mcv | fL |  | fL | fL | fL | fL | fL | no | no | — | no | no | UK FBC indices | COMPLIANT_NO_CHANGE | DEFER |
| `monocyte_pct` | monocyte_pct | % |  | % | % | % | % | % | no | n/a | — | no | optional | Differential % | REMOVE_OR_DEFER_NOT_LAUNCH_CRITICAL | DEFER |
| `monocytes_abs` | monocytes_abs | 10^9/L | monocyte_(mon_#), monocytes_abs_count | 10^9/L | 10^9/L | K/μL | 10^9/L | K/μL | no | no | — | no | no | UK FBC absolute | COMPLIANT_NO_CHANGE | DEFER |
| `mpv` | mpv | fL |  | fL | fL | fL | fL | fL | no | no | — | no | no | UK FBC indices | COMPLIANT_NO_CHANGE | DEFER |
| `neutrophil_pct` | neutrophil_pct | % |  | % | % | % | % | % | no | n/a | — | no | optional | Differential % dimensionless; LC-S8B defer | REMOVE_OR_DEFER_NOT_LAUNCH_CRITICAL | DEFER |
| `neutrophils` | neutrophils | 10^9/L | neutrophil_count, neutrophils_(venous) | 10^9/L | 10^9/L | K/μL | 10^9/L | K/μL | no | no | — | no | no | UK FBC absolute | COMPLIANT_NO_CHANGE | DEFER |
| `neutrophils_abs` | neutrophils_abs | 10^9/L | neutrophil_(neu_#), neutrophils_abs_count | 10^9/L | 10^9/L | K/μL | 10^9/L | K/μL | no | no | — | no | no | UK FBC absolute | COMPLIANT_NO_CHANGE | DEFER |
| `nlr` | nlr | ratio |  | ratio | ratio | ratio | ratio | ratio | no | n/a | — | no | no | Dimensionless derived | COMPLIANT_NO_CHANGE | DEFER |
| `non_hdl_cholesterol` | non_hdl_cholesterol | mmol/L |  | mmol/L | mmol/L | US alt if applicable | mmol/L | mmol/L | no | no | — | no | no | UK SI concentration | COMPLIANT_NO_CHANGE | DEFER |
| `oestradiol` | oestradiol | pmol/L |  | pmol/L | pmol/L | US alt if applicable | pmol/L | pmol/L | no | no | — | no | no | UK SI concentration | COMPLIANT_NO_CHANGE | DEFER |
| `pdw` | pdw | fL |  | fL | fL | fL | fL | fL | no | no | — | no | no | UK FBC indices | COMPLIANT_NO_CHANGE | DEFER |
| `platelets` | platelets | K/μL | plt, platelet_count | 10^9/L | 10^9/L, x10^9/L | K/μL, K/uL | 10^9/L | 10^9/L or K/μL (US display policy) | yes — 1:1 equivalence | no | K/μL | yes | optional | UK NEQAS FBC; BCSH — ×10⁹/L; LC-S8B | ADD_EQUIVALENCE_ONLY | PHASE_A_SAFE_EQUIVALENCE |
| `potassium` | potassium | mEq/L | potassium_(venous) | mmol/L | mmol/L | mEq/L | mmol/L | mmol/L | yes — 1:1 equivalence | no | — | yes | optional | UK NHS mmol/L; LC-S8B | ADD_EQUIVALENCE_ONLY | PHASE_A_SAFE_EQUIVALENCE |
| `prolactin` | prolactin | mIU/L |  | mIU/L | mIU/L | US alt if applicable | mIU/L | mIU/L | no | no | — | no | no | UK SI concentration | COMPLIANT_NO_CHANGE | DEFER |
| `rbc` | rbc | 10^12/L |  | 10^12/L | 10^12/L | M/μL | 10^12/L | 10^12/L | no | no | — | no | no | UK RBC count | COMPLIANT_NO_CHANGE | DEFER |
| `rdw_cv` | rdw_cv | % |  | % | % | % | % | % | no | no | — | no | no | Dimensionless % | COMPLIANT_NO_CHANGE | DEFER |
| `rdw_sd` | rdw_sd | fL |  | fL | fL | fL | fL | fL | no | no | — | no | no | UK FBC indices | COMPLIANT_NO_CHANGE | DEFER |
| `remnant_cholesterol` | remnant_cholesterol | mmol/L |  | mmol/L | mmol/L | US alt if applicable | mmol/L | mmol/L | no | no | — | no | no | UK SI concentration | COMPLIANT_NO_CHANGE | DEFER |
| `shbg` | shbg | nmol/L |  | nmol/L | nmol/L | US alt if applicable | nmol/L | nmol/L | no | no | — | no | no | UK SI concentration | COMPLIANT_NO_CHANGE | DEFER |
| `sodium` | sodium | mEq/L | sodium_(venous) | mmol/L | mmol/L | mEq/L | mmol/L | mmol/L | yes — 1:1 equivalence | no | — | yes | optional | NICE electrolytes; 1 mEq/L = 1 mmol/L monovalent; LC-S8B | ADD_EQUIVALENCE_ONLY | PHASE_A_SAFE_EQUIVALENCE |
| `tc_hdl_ratio` | tc_hdl_ratio | ratio |  | ratio | ratio | ratio | ratio | ratio | no | n/a | ratio | no | no | Dimensionless derived | COMPLIANT_NO_CHANGE | DEFER |
| `testosterone` | testosterone | nmol/L |  | nmol/L | nmol/L | US alt if applicable | nmol/L | nmol/L | no | no | — | no | no | UK SI concentration | COMPLIANT_NO_CHANGE | DEFER |
| `testosterone_free_testosterone_ratio` | testosterone_free_testosterone_ratio | ratio |  | ratio | ratio | ratio | ratio | ratio | no | n/a | — | no | no | Dimensionless derived | COMPLIANT_NO_CHANGE | DEFER |
| `tg_hdl_ratio` | tg_hdl_ratio | ratio |  | ratio | ratio | ratio | ratio | ratio | no | n/a | — | no | no | Dimensionless derived | COMPLIANT_NO_CHANGE | DEFER |
| `tgab` | tgab | IU/mL | thyroglobulin_antibodies_-_tgab, thyroglobulin_antibodies | IU/mL | IU/mL | TBD | IU/mL | IU/mL | audit | no | — | no | no | SSOT unit accepted UK/SI or international | COMPLIANT_NO_CHANGE | DEFER |
| `total_cholesterol` | total_cholesterol | mmol/L | cholesterol, total_chol, chol_total | mmol/L | mmol/L | mg/dL | mmol/L | mg/dL | yes | yes | mg/dL | yes | yes | UK lipids mmol/L; scoring_policy mg/dL | MIGRATE_LAYER_B_SCORING_UNIT | PHASE_C_LAYER_B_SCORING_MIGRATION |
| `total_ige` | total_ige | kU/L | total_immunoglobulin_e, ige_total | kU/L | kU/L | TBD | kU/L | kU/L | audit | no | — | no | no | SSOT unit accepted UK/SI or international | COMPLIANT_NO_CHANGE | DEFER |
| `total_protein` | total_protein | g/L |  | g/L | g/L | g/L | g/L | g/L | no | no | — | no | no | ADR-002 proteins g/L | COMPLIANT_NO_CHANGE | DEFER |
| `tpo_ab` | tpo_ab | kU/L |  | kU/L | kU/L | TBD | kU/L | kU/L | audit | no | — | no | no | SSOT unit accepted UK/SI or international | COMPLIANT_NO_CHANGE | DEFER |
| `transferrin` | transferrin | g/L |  | g/L | g/L | g/L | g/L | g/L | no | no | — | no | no | ADR-002 proteins g/L | COMPLIANT_NO_CHANGE | DEFER |
| `transferrin_saturation` | transferrin_saturation | % |  | % | % | % | % | % | no | no | — | no | no | Dimensionless % | COMPLIANT_NO_CHANGE | DEFER |
| `triglycerides` | triglycerides | mmol/L | trig, triglyceride, triglycerides_(venous) | mmol/L | mmol/L | mg/dL | mmol/L | mg/dL | yes | yes | mg/dL | yes | yes | UK lipids | MIGRATE_LAYER_B_SCORING_UNIT | PHASE_C_LAYER_B_SCORING_MIGRATION |
| `troponin` | troponin | ng/L | troponin_i, troponin_t, hs_troponin | ng/L | ng/L | TBD | ng/L | ng/L | audit | no | — | no | no | SSOT unit accepted UK/SI or international | COMPLIANT_NO_CHANGE | DEFER |
| `tryptase` | tryptase | ng/mL | serum_tryptase | ng/mL | ng/mL | TBD | ng/mL | ng/mL | audit | no | — | no | no | SSOT unit accepted UK/SI or international | COMPLIANT_NO_CHANGE | DEFER |
| `tsh` | tsh | mIU/L | thyroid_stimulating_hormone, thyrotropin | mIU/L | mIU/L | US alt if applicable | mIU/L | mIU/L | no | no | — | no | no | UK SI concentration | COMPLIANT_NO_CHANGE | DEFER |
| `tyg_index` | tyg_index | ratio |  | ratio | ratio | ratio | ratio | ratio | no | n/a | — | no | no | Dimensionless derived | COMPLIANT_NO_CHANGE | DEFER |
| `uacr` | uacr | mg/mmol | urine_albumin_creatinine_ratio, acr | mg/mmol | mg/mmol | TBD | mg/mmol | mg/mmol | audit | no | — | no | no | SSOT unit accepted UK/SI or international | COMPLIANT_NO_CHANGE | DEFER |
| `urate` | urate | umol/L |  | µmol/L | µmol/L, umol/L | mg/dL | µmol/L | mg/dL | yes — mg/dL↔µmol/L needed | partial | — | no | yes | Lab Tests Online UK urate µmol/L | ADD_TRUE_CONVERSION | PHASE_B_TRUE_CONVERSION |
| `urea` | urea | mmol/L | Urea, BUN, Blood urea nitrogen | mmol/L | mmol/L | mg/dL (BUN) | mmol/L | mg/dL BUN (US display optional) | yes — BUN mg/dL→mmol/L | yes | mmol/L | no | yes | UK urea mmol/L; BUN alias not uric acid | COMPLIANT_NO_CHANGE | PHASE_D_DISPLAY_POLICY |
| `urea_creatinine_ratio` | urea_creatinine_ratio | ratio |  | ratio | ratio | ratio | ratio | ratio | no | n/a | — | no | no | Dimensionless derived | COMPLIANT_NO_CHANGE | DEFER |
| `urine_protein_creatinine_ratio` | urine_protein_creatinine_ratio | mg/mmol |  | mg/mmol | mg/mmol | TBD | mg/mmol | mg/mmol | audit | no | — | no | no | SSOT unit accepted UK/SI or international | COMPLIANT_NO_CHANGE | DEFER |
| `vitamin_b12` | vitamin_b12 | pg/mL |  | pg/mL | pg/mL | TBD | pg/mL | pg/mL | audit | no | — | no | no | SSOT unit accepted UK/SI or international | COMPLIANT_NO_CHANGE | DEFER |
| `vitamin_d` | vitamin_d | nmol/L | Vitamin D, 25(OH) Vitamin D, 25-Hydroxy Vitamin D | nmol/L | nmol/L | ng/mL | nmol/L | ng/mL | yes | yes | — | no | no | UK nmol/L standard | COMPLIANT_NO_CHANGE | PHASE_D_DISPLAY_POLICY |
| `white_blood_cells` | white_blood_cells | K/μL | wbc, leukocytes | 10^9/L | 10^9/L | K/μL | 10^9/L | 10^9/L or K/μL | yes — 1:1 equivalence | no | K/μL | yes | optional | UK NEQAS FBC; LC-S8B | ADD_EQUIVALENCE_ONLY | PHASE_A_SAFE_EQUIVALENCE |
| `zinc` | zinc | umol/L |  | µmol/L | µmol/L, umol/L | mg/dL where applicable | µmol/L | mg/dL | partial | spelling only | — | no | no | UK µmol/L | COMPLIANT_NO_CHANGE | DEFER |


---

## 5. Biomarkers already UK/SI compliant

**77 biomarkers** with `Decision = COMPLIANT_NO_CHANGE` — SSOT unit matches UK/SI or international standard (U/L enzymes, g/L proteins, mmol/L lipids where SSOT already correct, 10^9/L absolutes, ratios, etc.).

No SSOT label change required for launch unit governance; some still need **scoring_policy** alignment only when scored (see §8).

---

## 6. Biomarkers requiring SSOT canonical unit change

**Label relabel only (Phase A — equivalence before relabel):**

| ID | Current SSOT | Target Layer B / SSOT |
|----|--------------|------------------------|
| `platelets` | `K/μL` | `10^9/L` |
| `white_blood_cells` | `K/μL` | `10^9/L` |
| `sodium` | `mEq/L` | `mmol/L` |
| `potassium` | `mEq/L` | `mmol/L` |
| `chloride` | `mEq/L` | `mmol/L` |

**True canonical flip (Phase B/C — after conversion evidence or policy):**

| ID | Current SSOT | Target Layer B |
|----|--------------|----------------|
| `hemoglobin` | `g/dL` | `g/L` |
| `calcium`, `corrected_calcium` | `mg/dL` | `mmol/L` |
| `magnesium` | `mg/dL` | `mmol/L` |
| `free_t4` | `ng/dL` | `pmol/L` |
| `hematocrit` | `%` | `L/L` |
| `hba1c` | `%` | `mmol/mol` |

---

## 7. Biomarkers requiring unit-registry conversion/equivalence support

| Gap | Biomarkers | Registry / units.yaml today |
|-----|------------|------------------------------|
| 1:1 equivalence missing | PLT, WBC, Na, K, Cl | No `K/μL`↔`10^9/L`; no `mEq/L`↔`mmol/L` in `_units_equivalent` |
| True conversion present | glucose, lipids, TG, creatinine, urea, vit D, Hb, HCT, hba1c | `_STRICT_CONVERSION_BIOMARKERS` |
| True conversion missing | Ca, Mg, fT4, urate | Not in strict set; factors absent (Ca/Mg/fT4) |
| µmol spelling only | `urate`, `bilirubin`, etc. | `_UMOL_EQUIVALENTS` only |

---

## 8. Biomarkers requiring Layer B scoring-policy unit migration

**Critical dual-authority defect:** Layer A normalises to SSOT UK units; `scoring_policy.yaml` bands remain US customary for:

| Biomarker | SSOT / post–Layer A | `scoring_policy.yaml` | Action |
|-----------|---------------------|----------------------|--------|
| `glucose` | mmol/L | mg/dL | Reband or harmonise to mmol/L |
| `total_cholesterol`, `ldl_cholesterol`, `hdl_cholesterol`, `triglycerides` | mmol/L | mg/dL | Same |
| `creatinine` | µmol/L | mg/dL | Same |
| `hba1c` | policy → mmol/mol | % | Reband to IFCC mmol/mol |
| `hematocrit` | policy → L/L | % | Reband to L/L or convert bands |
| `platelets`, `white_blood_cells` | policy → 10^9/L | K/μL | Align policy unit label |
| `hemoglobin` | policy → g/L | g/dL | Align after Phase B |

Also scored with aligned units today: `urea` (mmol/L), `hba1c`/`hematocrit` bands match **current** SSOT `%` but not **target** UK policy.

---

## 9. Biomarkers requiring Layer C display-unit policy

| Biomarker | UK display | US/non-UK display (governed secondary) |
|-----------|------------|--------------------------------------|
| `urea` | mmol/L | mg/dL as **BUN** label (Layer B stays mmol/L) |
| `vitamin_d` | nmol/L | ng/mL |
| Lipids, glucose, creatinine | mmol/L / µmol/L | mg/dL optional |
| `hba1c` | mmol/mol | % secondary only |
| `hematocrit` | L/L | % only if value + ref transformed together |
| `hemoglobin` | g/L | g/dL optional |

---

## 10. Layer C display policy

### 10.1 Two presentation modes (general rule)

Layer C must support **two governed presentation modes**. The same analysis run may use both: fidelity where the user verifies their upload, collapse where the product interprets results.

#### Mode A — Uploaded-panel fidelity

**Use for:** biomarker dials, raw uploaded-results review, upload/edit flows.

| Rule | Requirement |
|------|-------------|
| Preserve rows | Keep **every uploaded biomarker row** where safe (no silent drop). |
| Duplicate-equivalent units | If the **same canonical biomarker** appears in current/canonical and legacy/equivalent units (e.g. `mmol/mol` and `%` for one HbA1c identity, or `10^9/L` and `K/μL` for platelets), **show both uploaded representations** back to the user. |
| Visual linkage | **Link or annotate** equivalent rows as one biomarker (shared identity label, “equivalent representation” badge, or grouped UI) so the user sees they were not ignored or lost. |
| No false omission | Do **not** imply the duplicate-equivalent row was discarded after Layer A normalisation. |
| No client conversion | Display values/units from governed API fields only; frontend does not apply conversion factors. |

#### Mode B — Analytical-report

**Use for:** personalised observational reports, narrative interpretation, burden/signal summaries that refer to biomarkers in prose.

| Rule | Requirement |
|------|-------------|
| Single identity | Refer to each biomarker **once** by canonical biomarker identity. |
| Canonical unit | Use the **Layer B analytical unit** unless `display_unit_policy.yaml` authorises a governed secondary display for locale or UX. |
| No duplicate equivalents | Do **not** list both `%` and `mmol/mol` (or `K/μL` and `10^9/L`) as separate analytical results in narrative or summary tables. |
| Layer B authority | Narrative and scored interpretation consume **collapsed** Layer B input (after arbitration and unit normalisation), not raw duplicate upload rows. |

#### General rule (cross-mode)

```text
Preserve duplicate-equivalent source observations for uploaded-results fidelity.
Collapse duplicate-equivalent observations for Layer B analysis and report interpretation.
```

| Layer | Duplicate-equivalent behaviour |
|-------|--------------------------------|
| **Layer A** | Normalise to one canonical value per biomarker ID for scoring; retain upload provenance in metadata where required for Mode A. |
| **Layer B** | Single analytical value per canonical ID (e.g. HbA1c arbitration before scoring). |
| **Layer C Mode A** | Surface all safe uploaded representations with equivalence linkage. |
| **Layer C Mode B** | One reference per canonical ID in canonical Layer B unit (optional governed secondary display). |

**Ownership (proposed):** `display_unit_policy.yaml` includes `presentation_mode: upload_fidelity | analytical_report` per surface or API contract.

### 10.2 Non-UK / US input and display handling

1. **Layer A** accepts US customary **input** units only when registered in `units.yaml` + `registry.py` (strict set or new equivalence).
2. **Layer B** always calculates on UK/SI canonical analytical unit (§4 column).
3. **Layer C** may emit a **display_unit** ≠ analytical `unit` only when `display_unit_policy.yaml` authorises it for the user locale and presentation mode.
4. **Forbidden:** Frontend mmol/mg/dL math, silent unit repair, or inferring BUN as uric acid.
5. **US panels** commonly use mg/dL (glucose, lipids, creatinine, BUN), ng/dL (fT4), K/μL (CBC) — all must enter via Layer A conversion, not Layer C.

### 10.3 Frontend today (read-only baseline)

| Surface | Likely mode | Current gap |
|---------|-------------|-------------|
| Upload review / dials | Mode A | No equivalence linkage for duplicate unit families; LC-S7 suppresses incoherent refs only |
| Results / trends / narrative | Mode B | Pass-through `unit` from API; no governed collapse contract |
| `trendComparison.ts` | Mode B | No unit guard on cross-run deltas |

---

## 11. BUN / urea / uric acid clarification

| Question | Resolution |
|----------|------------|
| Is BUN uric acid? | **No.** BUN is blood urea nitrogen — **urea/nitrogen domain**. |
| SSOT IDs | **`urea`** canonical only; aliases `BUN`, `Blood Urea Nitrogen` (`biomarkers.yaml` ~311–316; `biomarker_alias_registry.yaml` ~732–743). **No `bun` ID.** |
| Uric acid | Canonical **`urate`**; alias `uric_acid` → `urate` (not `urea`). |
| Layer B unit | **`mmol/L` urea** (UK NHS) |
| US BUN input | **`mg/dL`** with factor 0.357 in `units.yaml` `mg_dL_to_mmol_L_urea` |
| Layer C US display | Optional **`mg/dL` BUN** label via display policy; Layer B remains mmol/L |
| `urea_creatinine_ratio` | Aliases include `BUN/Creatinine Ratio` — still urea domain, not urate |

**Sentinel rule:** `bun_not_uric_acid` — fail if alias registry maps BUN to `urate`.

---

## 12. HbA1c policy

| Policy element | Encoding |
|----------------|----------|
| UK Layer B primary | **`mmol/mol`** (IFCC) |
| `%` input | Accepted legacy; convert via `units.yaml` |
| `%` display | **Secondary only** for familiar US/legacy panels |
| Dual panel | Collapse to one result: `arbitrate_hba1c_layer_b_input` ([`hba1c_layer_b_arbitration.py`](../../backend/core/canonical/hba1c_layer_b_arbitration.py)); API route calls arbitration |
| `hba1c_pct` | **Deprecate as independent SSOT row** → alias-only under `hba1c`; remap `system_burden_registry.yaml` and `knowledge_bus/packages/pkg_kb52d_hba1c_pct_*` |
| `hba1c_pct` scoring | Not in `scoring_policy.yaml` metabolic list; must not be independently scored |
| Current gap | Layer A normalises to SSOT **`%`**; harmonisation in `rules.py` targets `%` families |

**Evidence:** [NICE NG28 — Blood glucose management](https://www.nice.org.uk/guidance/ng28/chapter/blood-glucose-management) (IFCC-standardised measurement); UK switch to mmol/mol reporting (DH, June 2009).

---

## 13. Haematocrit policy

| Policy element | Encoding |
|----------------|----------|
| UK Layer B primary | **`L/L`** volume fraction |
| `%` input | Legacy; convert with ×0.01 / ×100 when coherent |
| `%` display | Allowed only when **value and reference range** use same transform |
| Forbidden | **`0.438 %`** (fraction labelled as percent); mixed L/L value with `%` ref without conversion |
| Current Layer A | Converts L/L → SSOT **`%`** base ([`registry.py`](../../backend/core/units/registry.py) `_HEMATOCRIT_BIOMARKERS`) |
| Scoring migration | `scoring_policy.yaml` bands 36–46 in `%` must move to L/L or governed conversion |

**Evidence:** [Gloucestershire Hospitals — Haematology reference ranges](https://www.gloshospitals.nhs.uk/our-services/services-we-offer/pathology/haematology/haematology-reference-ranges/) (male 0.40–0.54 L/L); [North Bristol — Haematocrit](https://www.nbt.nhs.uk/severn-pathology/requesting/test-information/haematocrit) (0.40–0.52 fraction).

---

## 14. Required implementation phases for the later HIGH-risk sprint

| Phase | Scope | STOP gate |
|-------|--------|-----------|
| **PHASE_A_SAFE_EQUIVALENCE** | PLT, WBC, Na, K, Cl | Equivalence in `units.yaml` + registry **before** SSOT relabel |
| **PHASE_B_TRUE_CONVERSION** | Hb, Ca, Mg, fT4, urate | Primary-source factor per row |
| **PHASE_C_LAYER_B_SCORING_MIGRATION** | Lipids, glucose, creatinine, HbA1c, HCT, scored PLT/WBC/Hb | Golden fixtures + `scoring_policy.yaml` |
| **PHASE_D_DISPLAY_POLICY** | `display_unit_policy.yaml` + DTO fields | No frontend conversion |
| **PHASE_E_SENTINEL_LOCKDOWN** | §16 rules | After A–D green |

**Do not** run Phases B–E in one undifferentiated pass (LC-S8C pre-sprint note §5.1).

---

## 15. Required tests

| Test area | File / action |
|-----------|----------------|
| Registry conversions | Extend `backend/tests/unit/test_unit_registry.py` |
| HbA1c arbitration | `backend/tests/unit/test_hba1c_governance.py` |
| Value/ref coherence | `backend/tests/regression/test_lc_s8_biomarker_unit_reference_incoherence_regression.py` |
| SSOT-wide conformance | **New:** load §4 governance table (golden) — assert SSOT `unit` matches approved post-remediation |
| Scoring bands | `backend/tests/unit/test_scoring_rules.py` — mmol/L bands after Phase C |
| Sentinel pack | **New:** one test per §16 rule |
| Frontend | Assert no conversion constants in `frontend/app/**/*.ts(x)` |
| Layer C contract | API test: `display_unit` only when policy row exists; `unit` = Layer B |

---

## 16. Required Sentinel guardrail design

| Rule name | Scan target | Fail example | Pass example | CI mode |
|-----------|-------------|--------------|--------------|---------|
| `uk_layer_b_canonical_unit_drift` | `biomarkers.yaml` vs governance table | `platelets: K/μL` after remediation | `10^9/L` | **block** |
| `layer_b_unit_declared` | SSOT + governance metadata | new ID without Layer B unit | all 103 declared | **block** |
| `input_unit_has_authority` | `units.yaml`, `registry.py` | score `K/μL` without equivalence | equivalence registered | **block** |
| `unknown_unit_not_scored` | strict conversion paths | unmapped unit reaches scoring | reject or convert | **block** |
| `biomarker_value_reference_unit_incoherence` | existing LC-S8 class | g/dL value, g/L ref | coherent pair | **block** (exists) |
| `hba1c_single_analytical_identity` | SSOT, burden registry, KB | `hba1c` + `hba1c_pct` both scored | one canonical | **block** |
| `hematocrit_fraction_percent_display` | normalised payloads | `0.438 %` | `0.438` L/L or `43.8 %` coherent | **block** |
| `bun_not_uric_acid` | `biomarker_alias_registry.yaml` | BUN → urate | BUN → urea | **block** |
| `frontend_no_unit_repair` | `frontend/app/**` | `* 0.055` mmol conversion | pass-through only | **warn** → block |
| `new_biomarker_unit_metadata` | SSOT PR diff | new biomarker without input/display/evidence | full §4 row | **block** |

Pack location (proposed): `sentinel/packs/uk_unit_governance_v1.json` + runner registration in `sentinel/sentinel_runner.py`.

---

## 17. Remaining blockers

| ID | Blocker | Phase |
|----|---------|-------|
| B1 | Ca, corrected Ca, Mg, fT4 — no primary-source factors in repo | B |
| B2 | Hb g/L↔g/dL — factor in `units.yaml` but LC-S8B held validation | B |
| B3 | HbA1c mmol/mol canonical inverts normalise-to-% pipeline | C |
| B4 | `hba1c_pct` in SSOT + burden + KB | C |
| B5 | HCT L/L canonical inverts convert-to-% base | C |
| B6 | Sentinel last | E |
| B7 | `scoring_policy.yaml` US bands vs UK SSOT for glucose/lipids/creatinine | C |
| B8 | No `display_unit_policy.yaml` | D |

**Not a preflight STOP:** dual authority is **documented** and remediated in Phase C.

---

## 18. Recommendation (closure)

```text
APPROVED_WITH_CONDITIONS — WORKING_ARCHITECTURAL_BASIS_ONLY
```

**LC-S8C-PREFLIGHT is accepted** as a working architectural basis for planning the HIGH-risk remediation sprint. It is **not** final clinical evidence authority (§19).

**Closure conditions met:**

1. Evidence-quality addendum (§19) accepted.
2. Audit committed on `launch-core/lc-s8c-ssot-wide-unit-governance-preflight` with §3 branch record matching the work-package branch.
3. Layer C two-mode display policy recorded (§10.1).

**Hard stop — no implementation yet:**

- **No implementation sprint** may start until a **separate** HIGH-risk remediation work package is **authored and hardened** (Automation Bus / kernel as applicable).
- Phase gates remain as §20 (Phase A after WP commit only; Phase B blocked; Phase C row-by-row; Sentinel last).

Prior lines retained for traceability:

```text
READY_FOR_REMEDIATION_SPRINT  (superseded)
APPROVED_WITH_CONDITIONS (interim)  (superseded by closure status above)
```

---

## 19. Evidence-quality addendum (Condition 3–4)

### 19.1 Purpose

Classify **every** §4 biomarker row by evidence quality. Rows marked **REPO_POLICY_ONLY** or vague §4 wording must **not** be treated as final clinical authority. Only **PRIMARY_EVIDENCE_CITED** rows support clinical unit policy without further citation (and Phase B/C may still require engineering STOP gates).

### 19.2 Classification definitions

| Class | Meaning | Final clinical authority? |
|-------|---------|---------------------------|
| **PRIMARY_EVIDENCE_CITED** | At least one **named** UK-primary source (NICE, NHS trust handbook URL, UK NEQAS, RCPath/BCSH with specific unit statement) cited for this row or an approved policy subsection (§11–§13). | **Partial** — policy direction only; conversion factors may still be blocked. |
| **CATEGORY_EVIDENCE_CITED** | Unit inferred from **family template** (e.g. all enzymes `U/L`, all FBC absolutes `10^9/L`) or LC-S8B equivalence class — not a dedicated handbook line for this analyte. | **No** — architectural default only. |
| **REPO_POLICY_ONLY** | SSOT label, registry behaviour, scoring_policy mismatch, arbitration, or vague §4 phrases (“SSOT unit accepted…”, “audit”, “TBD”, “US alt if applicable”). | **No** |
| **BLOCKED_PENDING_EVIDENCE** | Layer B direction stated but **primary conversion factor** or per-marker primary source missing; Phase B must not implement. | **No** — blocked |

### 19.3 Summary counts (103 rows)

| Evidence quality class | Count | May drive implementation? |
|------------------------|------:|----------------------------|
| CATEGORY_EVIDENCE_CITED | 60 | Phase A equivalence only (5 rows with `phase_a_only`); others deferred |
| REPO_POLICY_ONLY | 35 | No |
| BLOCKED_PENDING_EVIDENCE | 6 | No — Phase B STOP |
| PRIMARY_EVIDENCE_CITED | 2 | Phase C policy (`hba1c`, `hematocrit`) with engineering STOP |

**Not final clinical authority:** **101 of 103** rows are not `PRIMARY_EVIDENCE_CITED` (35 `REPO_POLICY_ONLY` with vague §4 wording; 60 `CATEGORY_EVIDENCE_CITED`; 6 `BLOCKED_PENDING_EVIDENCE`). Only **`hba1c`** and **`hematocrit`** have per-marker primary UK sources cited in §19.5.

### 19.4 Per-row evidence classification table

| Biomarker ID | Evidence quality class | Implementation authority | Notes |
| ------------ | ---------------------- | ------------------------ | ----- |
| `acth` | REPO_POLICY_ONLY | no | Vague §4 evidence — not final authority |
| `active_b12` | REPO_POLICY_ONLY | no | Vague §4 evidence — not final authority |
| `albumin` | CATEGORY_EVIDENCE_CITED | no | Category template; not per-marker primary source |
| `aldolase` | CATEGORY_EVIDENCE_CITED | no | Category template; not per-marker primary source |
| `alp` | CATEGORY_EVIDENCE_CITED | no | Category template; not per-marker primary source |
| `alt` | CATEGORY_EVIDENCE_CITED | no | Category template; not per-marker primary source |
| `apoa1` | CATEGORY_EVIDENCE_CITED | no | Category template; not per-marker primary source |
| `apob` | CATEGORY_EVIDENCE_CITED | no | Category template; not per-marker primary source |
| `apob_apoa1_ratio` | CATEGORY_EVIDENCE_CITED | no | Category template; not per-marker primary source |
| `ast` | CATEGORY_EVIDENCE_CITED | no | Category template; not per-marker primary source |
| `ast_alt_ratio` | CATEGORY_EVIDENCE_CITED | no | Category template; not per-marker primary source |
| `basophil_pct` | REPO_POLICY_ONLY | no | Treat as non-authoritative until cited |
| `basophils_abs` | CATEGORY_EVIDENCE_CITED | no | Category template; not per-marker primary source |
| `bilirubin` | CATEGORY_EVIDENCE_CITED | no | Category template; not per-marker primary source |
| `calcium` | BLOCKED_PENDING_EVIDENCE | no | Phase B blocked until primary conversion factor cited |
| `chloride` | CATEGORY_EVIDENCE_CITED | phase_a_only | LC-S8B equivalence class; not per-marker primary handbook |
| `corrected_calcium` | BLOCKED_PENDING_EVIDENCE | no | Phase B blocked until primary conversion factor cited |
| `cortisol` | REPO_POLICY_ONLY | no | Vague §4 evidence — not final authority |
| `creatine_kinase` | CATEGORY_EVIDENCE_CITED | no | Category template; not per-marker primary source |
| `creatinine` | CATEGORY_EVIDENCE_CITED | phase_c_only | SSOT UK + registry; scoring reband needs primary bands |
| `crp` | REPO_POLICY_ONLY | no | Vague §4 evidence — not final authority |
| `cystatin_c` | REPO_POLICY_ONLY | no | Vague §4 evidence — not final authority |
| `dhea` | CATEGORY_EVIDENCE_CITED | no | Category template; not per-marker primary source |
| `dhea_s` | CATEGORY_EVIDENCE_CITED | no | Category template; not per-marker primary source |
| `egfr` | REPO_POLICY_ONLY | no | Treat as non-authoritative until cited |
| `eosinophil_pct` | REPO_POLICY_ONLY | no | Treat as non-authoritative until cited |
| `eosinophils_abs` | CATEGORY_EVIDENCE_CITED | no | Category template; not per-marker primary source |
| `fai` | CATEGORY_EVIDENCE_CITED | no | Category template; not per-marker primary source |
| `ferritin` | REPO_POLICY_ONLY | no | Vague §4 evidence — not final authority |
| `fib_4` | CATEGORY_EVIDENCE_CITED | no | Category template; not per-marker primary source |
| `folate` | REPO_POLICY_ONLY | no | Treat as non-authoritative until cited |
| `free_t3` | REPO_POLICY_ONLY | no | Vague §4 evidence — not final authority |
| `free_t4` | BLOCKED_PENDING_EVIDENCE | no | Phase B blocked until primary conversion factor cited |
| `free_testosterone` | REPO_POLICY_ONLY | no | Vague §4 evidence — not final authority |
| `free_testosterone_pct` | CATEGORY_EVIDENCE_CITED | no | Category template; not per-marker primary source |
| `fsh` | REPO_POLICY_ONLY | no | Vague §4 evidence — not final authority |
| `ggt` | CATEGORY_EVIDENCE_CITED | no | Category template; not per-marker primary source |
| `globulin` | CATEGORY_EVIDENCE_CITED | no | Category template; not per-marker primary source |
| `glucose` | CATEGORY_EVIDENCE_CITED | phase_c_only | SSOT UK + registry; scoring reband needs primary bands |
| `hba1c` | PRIMARY_EVIDENCE_CITED | phase_c_with_policy_stop | IFCC policy cited; registry/scoring inversion STOP |
| `hba1c_pct` | REPO_POLICY_ONLY | no | Deprecate/merge — repo §12 only |
| `hdl_cholesterol` | CATEGORY_EVIDENCE_CITED | phase_c_only | SSOT UK + registry; scoring reband needs primary bands |
| `hematocrit` | PRIMARY_EVIDENCE_CITED | phase_c_with_policy_stop | UK NHS L/L ranges cited; canonical direction STOP |
| `hemoglobin` | BLOCKED_PENDING_EVIDENCE | no | Phase B blocked until primary conversion factor cited |
| `homa_ir` | CATEGORY_EVIDENCE_CITED | no | Category template; not per-marker primary source |
| `homocysteine` | CATEGORY_EVIDENCE_CITED | no | Category template; not per-marker primary source |
| `insulin` | REPO_POLICY_ONLY | no | Vague §4 evidence — not final authority |
| `iron` | CATEGORY_EVIDENCE_CITED | no | Category template; not per-marker primary source |
| `ldl_cholesterol` | CATEGORY_EVIDENCE_CITED | phase_c_only | SSOT UK + registry; scoring reband needs primary bands |
| `ldl_hdl_ratio` | CATEGORY_EVIDENCE_CITED | no | Category template; not per-marker primary source |
| `lh` | REPO_POLICY_ONLY | no | Vague §4 evidence — not final authority |
| `lipoprotein_a` | CATEGORY_EVIDENCE_CITED | no | Category template; not per-marker primary source |
| `lymphocyte_pct` | REPO_POLICY_ONLY | no | LC-S8B cross-ref without per-marker primary |
| `lymphocytes` | CATEGORY_EVIDENCE_CITED | no | Category template; not per-marker primary source |
| `lymphocytes_abs` | CATEGORY_EVIDENCE_CITED | no | Category template; not per-marker primary source |
| `magnesium` | BLOCKED_PENDING_EVIDENCE | no | Phase B blocked until primary conversion factor cited |
| `mch` | REPO_POLICY_ONLY | no | Treat as non-authoritative until cited |
| `mchc` | CATEGORY_EVIDENCE_CITED | no | Category template; not per-marker primary source |
| `mcv` | CATEGORY_EVIDENCE_CITED | no | Category template; not per-marker primary source |
| `monocyte_pct` | REPO_POLICY_ONLY | no | Treat as non-authoritative until cited |
| `monocytes_abs` | CATEGORY_EVIDENCE_CITED | no | Category template; not per-marker primary source |
| `mpv` | CATEGORY_EVIDENCE_CITED | no | Category template; not per-marker primary source |
| `neutrophil_pct` | CATEGORY_EVIDENCE_CITED | no | Category template; not per-marker primary source |
| `neutrophils` | CATEGORY_EVIDENCE_CITED | no | Category template; not per-marker primary source |
| `neutrophils_abs` | CATEGORY_EVIDENCE_CITED | no | Category template; not per-marker primary source |
| `nlr` | CATEGORY_EVIDENCE_CITED | no | Category template; not per-marker primary source |
| `non_hdl_cholesterol` | REPO_POLICY_ONLY | no | Vague §4 evidence — not final authority |
| `oestradiol` | REPO_POLICY_ONLY | no | Vague §4 evidence — not final authority |
| `pdw` | CATEGORY_EVIDENCE_CITED | no | Category template; not per-marker primary source |
| `platelets` | CATEGORY_EVIDENCE_CITED | phase_a_only | LC-S8B equivalence class; not per-marker primary handbook |
| `potassium` | CATEGORY_EVIDENCE_CITED | phase_a_only | LC-S8B equivalence class; not per-marker primary handbook |
| `prolactin` | REPO_POLICY_ONLY | no | Vague §4 evidence — not final authority |
| `rbc` | REPO_POLICY_ONLY | no | Treat as non-authoritative until cited |
| `rdw_cv` | CATEGORY_EVIDENCE_CITED | no | Category template; not per-marker primary source |
| `rdw_sd` | CATEGORY_EVIDENCE_CITED | no | Category template; not per-marker primary source |
| `remnant_cholesterol` | REPO_POLICY_ONLY | no | Vague §4 evidence — not final authority |
| `shbg` | REPO_POLICY_ONLY | no | Vague §4 evidence — not final authority |
| `sodium` | CATEGORY_EVIDENCE_CITED | phase_a_only | LC-S8B equivalence class; not per-marker primary handbook |
| `tc_hdl_ratio` | CATEGORY_EVIDENCE_CITED | no | Category template; not per-marker primary source |
| `testosterone` | REPO_POLICY_ONLY | no | Vague §4 evidence — not final authority |
| `testosterone_free_testosterone_ratio` | CATEGORY_EVIDENCE_CITED | no | Category template; not per-marker primary source |
| `tg_hdl_ratio` | CATEGORY_EVIDENCE_CITED | no | Category template; not per-marker primary source |
| `tgab` | REPO_POLICY_ONLY | no | Vague §4 evidence — not final authority |
| `total_cholesterol` | CATEGORY_EVIDENCE_CITED | phase_c_only | SSOT UK + registry; scoring reband needs primary bands |
| `total_ige` | REPO_POLICY_ONLY | no | Vague §4 evidence — not final authority |
| `total_protein` | CATEGORY_EVIDENCE_CITED | no | Category template; not per-marker primary source |
| `tpo_ab` | REPO_POLICY_ONLY | no | Vague §4 evidence — not final authority |
| `transferrin` | CATEGORY_EVIDENCE_CITED | no | Category template; not per-marker primary source |
| `transferrin_saturation` | CATEGORY_EVIDENCE_CITED | no | Category template; not per-marker primary source |
| `triglycerides` | CATEGORY_EVIDENCE_CITED | phase_c_only | SSOT UK + registry; scoring reband needs primary bands |
| `troponin` | REPO_POLICY_ONLY | no | Vague §4 evidence — not final authority |
| `tryptase` | REPO_POLICY_ONLY | no | Vague §4 evidence — not final authority |
| `tsh` | REPO_POLICY_ONLY | no | Vague §4 evidence — not final authority |
| `tyg_index` | CATEGORY_EVIDENCE_CITED | no | Category template; not per-marker primary source |
| `uacr` | REPO_POLICY_ONLY | no | Vague §4 evidence — not final authority |
| `urate` | BLOCKED_PENDING_EVIDENCE | no | Phase B blocked until primary conversion factor cited |
| `urea` | CATEGORY_EVIDENCE_CITED | phase_d_display | Urea mmol/L + BUN alias map §11 |
| `urea_creatinine_ratio` | CATEGORY_EVIDENCE_CITED | no | Category template; not per-marker primary source |
| `urine_protein_creatinine_ratio` | REPO_POLICY_ONLY | no | Vague §4 evidence — not final authority |
| `vitamin_b12` | REPO_POLICY_ONLY | no | Vague §4 evidence — not final authority |
| `vitamin_d` | CATEGORY_EVIDENCE_CITED | phase_d_only | UK nmol/L category; registry conversion present |
| `white_blood_cells` | CATEGORY_EVIDENCE_CITED | phase_a_only | LC-S8B equivalence class; not per-marker primary handbook |
| `zinc` | CATEGORY_EVIDENCE_CITED | no | Category template; not per-marker primary source |

### 19.5 Rows with PRIMARY_EVIDENCE_CITED (full list)

| Biomarker ID | Primary source (as cited in §4 / §11–§13) | Implementation authority |
|--------------|-------------------------------------------|-------------------------|
| `hba1c` | [NICE NG28](https://www.nice.org.uk/guidance/ng28/chapter/blood-glucose-management); DH 2009 IFCC switch | `phase_c_with_policy_stop` only |
| `hematocrit` | [Gloucestershire Hospitals haematology ranges](https://www.gloshospitals.nhs.uk/our-services/services-we-offer/pathology/haematology/haematology-reference-ranges/); [NBT haematocrit](https://www.nbt.nhs.uk/severn-pathology/requesting/test-information/haematocrit) | `phase_c_with_policy_stop` only |

All other rows: see §19.4 table — predominantly **CATEGORY_EVIDENCE_CITED** or **REPO_POLICY_ONLY**.

### 19.6 BLOCKED_PENDING_EVIDENCE rows (Phase B hard STOP)

| Biomarker ID | Reason |
|--------------|--------|
| `calcium` | NICE CKD mmol/L policy cited; **mg/dL↔mmol/L factor** not in `units.yaml` |
| `corrected_calcium` | Same as calcium |
| `magnesium` | UK mmol/L category only; **no primary factor** |
| `free_t4` | NICE pmol/L policy cited; **ng/dL↔pmol/L factor** not validated |
| `hemoglobin` | g/L↔g/dL in `units.yaml` but **no UK handbook sign-off** per LC-S8B |
| `urate` | µmol/L direction; **mg/dL↔µmol/L** not in registry |

---

## 20. Conditional remediation approval gates (Conditions 5–8)

| Phase | May proceed from this audit? | Conditions |
|-------|------------------------------|------------|
| **A — Safe equivalence** (`platelets`, `white_blood_cells`, `sodium`, `potassium`, `chloride`) | **Yes, after branch/file-scope correction** | §19: `phase_a_only` — **CATEGORY_EVIDENCE_CITED** via LC-S8B; register equivalence before SSOT relabel. Not final clinical authority. |
| **B — True conversion** | **No — remain blocked** | All §19.6 rows; no implementation until **PRIMARY_EVIDENCE_CITED** conversion factor per biomarker. |
| **C — Layer B scoring migration** | **Partial — row-by-row** | **Allowed only** where §19 grants `phase_c_only` or `phase_c_with_policy_stop`: `glucose`, `total_cholesterol`, `ldl_cholesterol`, `hdl_cholesterol`, `triglycerides`, `creatinine` (SSOT + registry + category evidence; reband needs NICE/lipid primary bands); `hba1c`, `hematocrit` (primary policy cited + engineering STOP). **Not allowed** on category-only lipids evidence alone for regulated thresholds — attach primary band source before merge. `hba1c_pct`: repo merge only. PLT/WBC scoring unit alignment: **after Phase A**. |
| **D — Display policy** | **After A; parallel planning OK** | `urea` (BUN display), `vitamin_d` — category/repo; governed `display_unit_policy.yaml` still required. |
| **E — Sentinel lockdown** | **Last — unchanged** | Only after A–D stable and green regression (LC-S8C pre-sprint B6). |

**Explicit prohibition:** Do **not** begin SSOT, registry, scoring, frontend, or Sentinel **implementation** until the **next HIGH-risk remediation prompt** is separately authored, hardened, and opened; §19 must be reviewed for the phase being opened.

---

*End of LC-S8C-PREFLIGHT audit (rev. conditional approval addendum).*
