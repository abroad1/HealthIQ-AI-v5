# ARCH-CONV-PKG2 — Launch-Critical Provenance Decision Inventory

**Work ID:** `ARCH-CONV-PKG2`  
**Branch:** `feature/arch-conv-pkg2-provenance-reachability`  
**Baseline HEAD:** `d696fca3ba5483ae59d547a55a817c9284b2e981`  
**STOP Gate 1:** **PASS**

---

## 1. Framing correction (hardening observation)

Before Package 2 there was **zero runtime enforcement** of provenance status. `classify_package_provenance_status` / `is_beta_eligible_explicit_lineage` were reporting-only (offline gate). Package 2 adds the **first** production choke point at `SignalRegistry._load`, scoped to the Gate 0 launch-critical cohort (`pkg_kb47_*`).

---

## 2. STOP Gate 1

| Trigger | Result |
|---|---|
| Wave 1 relied-upon package suppressed without approval | **Not proposed** — Wave 1 INCLUDE (6) receive lineage and stay reachable |
| Invented `source_spec_id` | **No** — all ids copied from `Batch_2_Pass_3.json` |
| Unmappable batch research | **No** — 20/20 recoverable |
| Multi-frame ambiguity without selection | **No** — one package per Pass 3 `spec_id` |
| Estate-wide regeneration | **No** — bounded to kb47 |
| Package 3 WHY prerequisite | **No** |
| Cohort must materially change | **No** |

**PASS — proceed.**

---

## 3. Decision table (all 20 `pkg_kb47_*`)

Shared baseline before Package 2: loadable=yes, fire-capable if biomarkers/gates pass, ranking-capable if fired, provenance=BLOCKED (batch JSON), beta_eligible=false, standalone inv YAML=no, Pass 3 lineage=yes.

### Wave 1 INCLUDE — ATTACH + KEEP_REACHABLE

| package_id | signal_id | activation_key | disposition | human approval |
|---|---|---|---|---|
| pkg_kb47_free_t3_low_low_t3_syndrome | signal_free_t3_low | signal_free_t3_low::inv_free_t3_low_low_t3_syndrome | ATTACH_EXPLICIT_LINEAGE + KEEP_REACHABLE_AFTER_LINEAGE | Gate 0 INCLUDE (merged) |
| pkg_kb47_free_t3_high_t3_predominant_thyrotoxicosis | signal_free_t3_high | …::inv_free_t3_high_t3_predominant_thyrotoxicosis | ATTACH + KEEP_REACHABLE | Gate 0 INCLUDE |
| pkg_kb47_free_t4_low_thyroid_hormone_deficiency | signal_free_t4_low | …::inv_free_t4_low_thyroid_hormone_deficiency | ATTACH + KEEP_REACHABLE | Gate 0 INCLUDE |
| pkg_kb47_free_t4_high_thyrotoxicosis_context | signal_free_t4_high | …::inv_free_t4_high_thyrotoxicosis_context | ATTACH + KEEP_REACHABLE | Gate 0 INCLUDE |
| pkg_kb47_egfr_low_chronic_kidney_function_reduction | signal_egfr_low | …::inv_egfr_low_chronic_kidney_function_reduction | ATTACH + KEEP_REACHABLE | Gate 0 INCLUDE |
| pkg_kb47_egfr_low_hemodynamic_filtration_drop | signal_egfr_low | …::inv_egfr_low_hemodynamic_filtration_drop | ATTACH + KEEP_REACHABLE | Gate 0 INCLUDE |

**Lineage source:** exact Pass 3 frame dump → `knowledge_bus/research/investigation_specs/{spec_id}.yaml` + manifest `source_spec_id`. No medical reinterpretation.

**After attach:** provenance=`EXPLICIT_SPEC`, beta_eligible_explicit=`true`, production reachable=`yes`.

### Androgen — MAKE_NON_REACHABLE (exclude from controlled-beta production load)

| package_id | signal_id | disposition | product impact if non-reachable | medical impact | human approval |
|---|---|---|---|---|---|
| pkg_kb47_dhea_high_androgen_excess_context | signal_dhea_high | MAKE_NON_REACHABLE | Low for Wave 1 cards (not Wave 1 domain) | Context/MR still open (BATCH2-MEDREVIEW-1) | Gate 0 REQUIRES_MEDICAL_REVIEW + EXCLUDE_FROM_BETA |
| pkg_kb47_dhea_low_adrenal_androgen_reduction | signal_dhea_low | MAKE_NON_REACHABLE | Low | Same | Gate 0 |
| pkg_kb47_fai_high_biochemical_hyperandrogenism | signal_fai_high | MAKE_NON_REACHABLE | Low | Same | Gate 0 |
| pkg_kb47_fai_low_reduced_free_androgen_availability | signal_fai_low | MAKE_NON_REACHABLE | Low | Same | Gate 0 |
| pkg_kb47_free_testosterone_high_androgen_excess_context | signal_free_testosterone_high | MAKE_NON_REACHABLE | Low | Same | Gate 0 |
| pkg_kb47_free_testosterone_low_androgen_deficiency_context | signal_free_testosterone_low | MAKE_NON_REACHABLE | Low | Same | Gate 0 |
| pkg_kb47_free_testosterone_pct_high_elevated_free_androgen_fraction | signal_free_testosterone_pct_high | MAKE_NON_REACHABLE | Low | Same | Gate 0 |
| pkg_kb47_free_testosterone_pct_low_reduced_free_androgen_fraction | signal_free_testosterone_pct_low | MAKE_NON_REACHABLE | Low | Same | Gate 0 |

Assets retained on disk. Test opt-in: `SignalRegistry(allow_launch_critical_blocked=True)` or `HEALTHIQ_ALLOW_LAUNCH_CRITICAL_BLOCKED=1`.

### CK / eosinophils — MAKE_NON_REACHABLE (DEFER from Wave 1 beta surface)

| package_id | signal_id | disposition | product impact | human approval |
|---|---|---|---|---|
| pkg_kb47_creatine_kinase_high_exertional_muscle_injury | signal_creatine_kinase_high | MAKE_NON_REACHABLE | Low — not Wave 1 domain | Gate 0 DEFER |
| pkg_kb47_creatine_kinase_high_persistent_nonexertional_muscle_injury | signal_creatine_kinase_high | MAKE_NON_REACHABLE | Low | Gate 0 DEFER |
| pkg_kb47_eosinophil_pct_high_reactive_atopic_eosinophilia | signal_eosinophil_pct_high | MAKE_NON_REACHABLE | Low | Gate 0 DEFER |
| pkg_kb47_eosinophil_pct_high_secondary_or_systemic_eosinophilia | signal_eosinophil_pct_high | MAKE_NON_REACHABLE | Low | Gate 0 DEFER |
| pkg_kb47_eosinophils_abs_high_reactive_eosinophilic_inflammation | signal_eosinophils_abs_high | MAKE_NON_REACHABLE | Low | Gate 0 DEFER |
| pkg_kb47_eosinophils_abs_high_hypereosinophilic_or_secondary_eosinophilia | signal_eosinophils_abs_high | MAKE_NON_REACHABLE | Low | Gate 0 DEFER |

---

## 4. Golden / representative appearance (pre-implementation)

| Check | Finding |
|---|---|
| Fixtures name `pkg_kb47` | No |
| `golden_panel_160.json` biomarkers | Has free_t3/free_t4/CK/dhea/fai; **no egfr**, **no eosinophil** |
| Expected fire of Wave 1 kb47 on golden | Likely suppressed by context/TSH gates (UNVERIFIABLE without full panel re-run before change; see impact report) |
| Expected fire of androgen/CK/eos after exclusion | N/A — removed from production registry |

---

## 5. Canonical policy

| Eligibility | Meaning |
|---|---|
| `production_reachable` | Launch-critical with EXPLICIT_SPEC/COMPILED_MANIFEST |
| `non_reachable` | Launch-critical without acceptable explicit lineage |
| `test_only_opt_in` | Explicit harness/env override |
| `out_of_launch_critical_cohort` | Non-kb47 — unchanged load behaviour |
| `unknown_fail_closed` | Empty package_id |

Call site: `SignalRegistry._load` before activation-key insertion.

---

## 6. Totals

| Slice | Count |
|---|---:|
| ATTACH + KEEP_REACHABLE | 6 |
| MAKE_NON_REACHABLE | 14 |
| Package directories deleted | 0 |
| Estate packages outside kb47 touched | 0 |
