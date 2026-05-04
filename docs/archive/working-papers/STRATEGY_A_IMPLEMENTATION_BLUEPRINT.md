# Strategy A — Customer-Facing Health Score Implementation Blueprint

**Document type:** Repo-grounded implementation research
**Date:** 2026-04-26
**Author:** Claude Code (research only — no implementation authority)
**Status:** Draft for GPT architectural review and sprint planning

---

## Purpose

This document is the output of a repo-grounded implementation research task.

It assesses how the agreed Strategy A customer-facing health score model can be implemented against the current HealthIQ codebase. It is not a sprint prompt. It is not a UX specification. It is not an authorisation to implement.

Its purpose is to provide the evidence base needed to:
- confirm which of the six launch domains are genuinely supported by the current repo
- identify where gaps exist and what kind of work they require
- define a realistic sprint sequence for GPT to author into work packages

---

## Background

HealthIQ has agreed **Strategy A**: launch exactly six customer-facing health score domains first.

1. Cardiovascular health
2. Blood sugar control
3. Liver health
4. Blood, iron & oxygen
5. Thyroid & energy regulation
6. Kidney function

Second-wave only (not assessed here): Silent inflammation, Hormone balance.

These scores are a translation layer **above** the deterministic engine. They must not replace the clinical handout labels or the internal phenotype/system logic.

The full strategic context is in `User Health to Systems Map_v4.md` (stored externally).

---

## Pre-assessment: What the engine actually outputs today

Before domain-by-domain assessment, three architectural facts shape every recommendation.

### Scoring track 1 — `scoring_policy.yaml` system scores

Range-position scoring, clinical band calibration. Systems with active weights:

| System | Weight | Biomarkers scored |
|---|---|---|
| metabolic | 0.25 | glucose, hba1c, insulin |
| cardiovascular | 0.25 | total_cholesterol, ldl_cholesterol, hdl_cholesterol, triglycerides, tc_hdl_ratio |
| inflammatory | 0.15 | crp |
| kidney | 0.15 | creatinine, urea |
| liver | 0.10 | alt, ast |
| cbc | 0.10 | hemoglobin, hematocrit, wbc, platelets |
| hormonal | 0.0 | (none — placeholder only) |
| nutritional | 0.0 | (none — placeholder only) |

### Scoring track 2 — `system_capacity_scores` (burden-derived)

Computed as `100 - (burden × 12.5)`. Already emitted in `AnalysisDTO.system_capacity_scores`. Covers a broader set of systems:

`metabolic`, `cardiovascular`, `thyroid`, `renal`, `hepatic`, `hematological`, `immune`, `hormonal`, `nutritional`, `musculoskeletal`, `autonomic`

### Critical architectural note

These two tracks have **different calibrations, different system names, and different scopes**. The domain score assembler must navigate this deliberately — not collapse them naively.

Neither track currently exposes a consumer-facing domain score. The field `consumer_domain_scores` does not exist anywhere in the DTO or frontend. **All six domains require a new translation layer.**

---

## Domain 1: Cardiovascular Health

**Consumer label:** Cardiovascular health
**Clinical label:** Cardiometabolic / Vascular Risk Status

### Internal engine mapping

| Layer | Current assets |
|---|---|
| Scoring system | `cardiovascular` in scoring_policy.yaml — tc, ldl, hdl, triglycerides, tc_hdl_ratio. Weight 0.25. Produces `HealthSystemScore`. |
| Burden system | `cardiovascular` in burden_registry — extends to apob, apoa1, ldl_hdl_ratio, tg_hdl_ratio, non_hdl_cholesterol, apob_apoa1_ratio, lipoprotein_a, homocysteine |
| Derived ratios | tc_hdl_ratio, tg_hdl_ratio, ldl_hdl_ratio, non_hdl_cholesterol, apob_apoa1_ratio — all governed in scoring_policy derived_ratio_policy_bounds |
| Signals | signal_ldl_cholesterol_high, signal_hdl_cholesterol_low, signal_triglycerides_high, signal_total_cholesterol_high, signal_lipid_transport_dysfunction, signal_homocysteine_elevation_context |
| KB packages | pkg_lipid_transport, pkg_homocysteine_elevation_context, pkg_kb52c_apob_high_*, pkg_kb52c_apoa1_low_*, pkg_kb52c_apob_apoa1_ratio_*, pkg_kb45_apob_high_atherogenic, pkg_kb45_apoa1_low_cardio_risk |
| WHY generators | load_ldl_cholesterol_high_hypotheses_v1, load_hdl_cholesterol_low_hypotheses_v1, load_triglycerides_high_hypotheses_v1, load_total_cholesterol_high_hypotheses_v1 (R-8 Wave 1), load_lipid_transport_dysfunction_hypotheses_v1, load_hcy_hypotheses_v1 |
| Sub-system contributors | Lipid transport (ldl/hdl/ratios), atherogenic particle burden (apob/apoa1 when present), homocysteine / endothelial strain (when tested) |

### Current codebase support

**Full.** Both scoring tracks active. Derived ratios computed. Six WHY generators registered. Multiple KB packages across particle imbalance, ApoB excess, ApoA1 deficiency, and homocysteine patterns. The strongest single domain in the repo.

### Missing pieces

Lipoprotein(a) is tracked in burden_registry (weight 0.7, HIGH_IS_RISK) and KB packages exist, but no dedicated `signal_lipoprotein_a_high` is in `_ROOT_CAUSE_TARGETS` in root_cause_compiler_v1.py — minor gap, does not block launch.

### Launch readiness

**LAUNCH-READY NOW**

### Confidence inputs already in system

scoring_policy cardiovascular system confidence (HIGH/MEDIUM/LOW based on marker count vs min_biomarkers_required: 3). ApoB/ApoA1 presence escalates interpretive depth. Derived ratio availability further extends pattern strength.

### Score band derivation

The scoring_policy `cardiovascular` system score (0–100, range-position calibration) maps directly to the proposed consumer score bands. No new calibration needed for Wave 1.

### What the expanded card can truthfully say today

Lipid panel status, atherogenic ratio direction, HDL protective capacity, LDL absolute risk direction, triglyceride-HDL metabolic coupling, homocysteine endothelial strain if tested, WHY hypotheses for each active signal.

### Codebase paths requiring change

- `backend/core/analytics/domain_score_assembler.py` — **NEW**: translation layer aggregating scoring_policy `cardiovascular` system score + active cardiovascular signals → `DomainScore` object
- `backend/core/models/results.py` — add `consumer_domain_scores: Optional[Dict[str, DomainScore]]` to AnalysisDTO
- `backend/core/pipeline/orchestrator.py` — call domain score assembler post-arbitration
- `frontend/app/components/results/HealthDomainScoreCards.tsx` — **NEW** frontend component
- `frontend/app/types/analysis.ts` — add DomainScore type

---

## Domain 2: Blood Sugar Control

**Consumer label:** Blood sugar control
**Clinical label:** Glycaemic Regulation / Insulin Resistance Status

### Internal engine mapping

| Layer | Current assets |
|---|---|
| Scoring system | `metabolic` in scoring_policy.yaml — glucose (weight 0.4), hba1c (weight 0.4), insulin (weight 0.2). Weight 0.25 overall. min_biomarkers_required: 2. |
| Burden system | `metabolic` in burden_registry — glucose, hba1c, insulin (core) plus calcium, chloride, magnesium, potassium, sodium, creatine_kinase (these are not blood sugar markers — dilutants in burden scoring) |
| Derived markers | tyg_index (glucose + triglycerides composite), tg_hdl_ratio (insulin resistance proxy), homa_ir (when insulin present) |
| Signals | signal_insulin_resistance (TyG primary, evidence-anchored thresholds, prediabetes override), signal_hba1c_high |
| KB packages | pkg_insulin_resistance, pkg_glucose_dysregulation_hba1c_context, pkg_s24_hba1c_high_glycaemia |
| WHY generators | load_hba1c_hypotheses_v1, load_insulin_resistance_hypotheses_v1 |

### Current codebase support

**Strong.** The scoring_policy `metabolic` system score is a clean blood sugar proxy — it uses only glucose, hba1c, and insulin. No electrolyte dilutants contaminate the score (those appear only in burden capacity). The insulin resistance signal is the repo's most evidence-complete signal, with TyG thresholds from Navarro-González 2016 and Irace 2022, prediabetes override, and HOMA-IR multi-metric architecture.

### Important note on metabolic burden capacity

The metabolic burden capacity score pulls in calcium, magnesium, potassium, sodium, chloride, creatine_kinase. **Do not use metabolic burden capacity as the blood sugar domain score.** Use the scoring_policy `metabolic` system score instead.

### Missing pieces

No signal for isolated hyperglycaemia without HbA1c (glucose-only panel). No fasting insulin signal independent of TyG. Both are edge cases for routine panels and do not block launch.

### Launch readiness

**LAUNCH-READY NOW**

### Confidence inputs already in system

Glucose + HbA1c are minimum (min_biomarkers_required: 2). Insulin presence escalates confidence. When triglycerides are also present, TyG index is computable — extends pattern depth significantly.

### Score band derivation

The scoring_policy metabolic score maps directly to proposed bands. The prediabetes override in signal_insulin_resistance means the score will correctly flag borderline glycaemia even when numeric scores look acceptable.

### What the expanded card can truthfully say today

Glucose stability status, HbA1c trend proxy, insulin resistance phenotype if triglycerides present, prediabetes range detection, WHY depth on metabolic root causes.

### Codebase paths requiring change

- `domain_score_assembler.py` — map scoring_policy `metabolic` system score → blood_sugar_control domain score. Straightforward. Do NOT use metabolic burden capacity.
- Same AnalysisDTO / frontend changes as Domain 1.

---

## Domain 3: Liver Health

**Consumer label:** Liver health
**Clinical label:** Hepatic-Metabolic Strain Status

### Internal engine mapping

| Layer | Current assets |
|---|---|
| Scoring system | `liver` in scoring_policy.yaml — alt (weight 0.5, sex-adjusted), ast (weight 0.5). Weight 0.10 overall. min_biomarkers_required: 1. |
| Burden system | `hepatic` in burden_registry — alt, ggt, alp, bilirubin, albumin, total_protein, globulin. Substantially richer than scoring system. |
| Signals | signal_hepatic_alt_context, signal_ggt_high, signal_hepatic_metabolic_stress, signal_alp_high, signal_alp_low, signal_bilirubin_high, signal_hyperbilirubinemia |
| KB packages | pkg_hepatic_alt_context, pkg_hepatic_metabolic_stress, pkg_kb52c_alt_high_hepatocellular_injury_pattern, pkg_kb52c_alt_high_metabolic_steatotic_liver_pattern, pkg_kb52c_alt_high_muscle_source_or_exertional_pattern, pkg_kb52c_albumin_low_*, pkg_kb52c_alp_high_cholestatic_pattern |
| WHY generators | load_alt_hypotheses_v1, load_ggt_high_hypotheses_v1, load_hepatic_metabolic_stress_hypotheses_v1, load_alp_high_hypotheses_v1, load_alp_low_hypotheses_v1, load_bilirubin_high_hypotheses_v1, load_hyperbilirubinemia_hypotheses_v1 |

### Current codebase support

**Moderate-to-strong.** The WHY layer is the richest of any non-cardiovascular domain — seven hypothesis generators, steatotic/cholestatic/muscle-source ALT pattern differentiation, albumin and bilirubin context. The scoring system is the weak point: `liver` system in scoring_policy uses only alt + ast with weight 0.10 — the lowest of any active system.

### Scoring mismatch

The `liver` system score is narrow. The `hepatic` burden capacity is richer but uses a different calibration formula. For the consumer domain, the correct approach is to use the scoring_policy liver score as the floor, and blend with the hepatic burden capacity when additional markers (GGT, ALP, albumin, bilirubin) are present. The assembler must weight by marker availability.

### Missing pieces

GGT, ALP, bilirubin, albumin are tracked in burden and have WHY generators but are not in scoring_policy.yaml. This is an acceptable gap for Wave 1 if most routine panels include only ALT/AST. The domain score will be honest about its narrow basis when only ALT/AST are available.

### Launch readiness

**LAUNCHABLE WITH LIGHT ASSEMBLY**

Light assembly: domain score aggregator blends scoring_policy liver score with hepatic burden capacity, weighted by which markers are actually present. When only ALT/AST available: use scoring_policy score. When GGT/ALP/albumin also present: blend with hepatic burden capacity.

### Confidence inputs already in system

ALT required (min_biomarkers_required: 1). AST extends confidence. GGT + ALP together escalate pattern strength significantly. Albumin adds synthetic function context. Multi-signal co-activation (e.g., both signal_hepatic_alt_context and signal_ggt_high) raises confidence materially.

### What the expanded card can truthfully say today

Liver enzyme pattern status, hepatocellular vs cholestatic pattern differentiation when multi-enzyme present, metabolic-fatty-liver pattern context, steatotic ALT context when metabolic syndrome co-present, WHY depth across seven root cause generators.

### Codebase paths requiring change

- `domain_score_assembler.py` — hepatic domain: blend scoring_policy `liver` + hepatic capacity, conditional on marker availability
- No SSOT changes required for Wave 1

---

## Domain 4: Blood, Iron & Oxygen

**Consumer label:** Blood, iron & oxygen
**Clinical label:** Iron-Erythropoietic / Oxygen-Carrying Status

### Internal engine mapping

| Layer | Current assets |
|---|---|
| Scoring system | `cbc` in scoring_policy.yaml — hemoglobin (weight 0.4, sex-adjusted), hematocrit (weight 0.3, sex-adjusted), wbc (weight 0.2), platelets (weight 0.1). min_biomarkers_required: 2. |
| Burden system — red cell | `hematological` in burden_registry — hemoglobin, hematocrit, ferritin, rbc, mcv, mch, mchc, rdw_cv, rdw_sd, mpv, pdw, wbc, platelets |
| Burden system — iron stores | `nutritional` in burden_registry — iron (BOTH_SIDES_RISK, weight 0.5), transferrin (BOTH_SIDES_RISK, weight 0.5) |
| Signals | signal_iron_deficiency_context (ferritin primary + hematological cascade), signal_iron_overload_context, signal_oxygen_transport_capacity, signal_ferritin_low, signal_ferritin_high, signal_hemoglobin_low, signal_transferrin_high, signal_transferrin_low |
| KB packages | pkg_iron_deficiency_context, pkg_iron_overload_context, pkg_s24_ferritin_low_iron_deficiency, pkg_s24_ferritin_high_overload, pkg_s24_hgb_low_anemia, pkg_s24_mcv_high_macrocytosis |
| WHY generators | load_iron_deficiency_context_hypotheses_v1, load_iron_overload_context_hypotheses_v1, load_hemoglobin_low_hypotheses_v1, load_ferritin_low_hypotheses_v1, load_ferritin_high_hypotheses_v1, load_oxygen_transport_capacity_hypotheses_v1, load_transferrin_high_hypotheses_v1, load_transferrin_low_hypotheses_v1 |

### Critical architectural observation

Iron markers are **split across two internal burden systems** — iron stores/transport in `nutritional`, red cell indices in `hematological`. The scoring_policy `cbc` system captures only the red cell output (hemoglobin, hematocrit, wbc, platelets) and does not include ferritin or serum iron.

However, the signal layer correctly bridges both. `signal_iron_deficiency_context` activates on low ferritin and escalates on anaemia-compatible red cell changes (low hemoglobin, low MCV, elevated RDW). The WHY layer is the most complete cross-system iron pathway in the repo.

### Missing pieces

No single system score represents the full iron-to-oxygen pathway. The domain score must aggregate the `cbc` system score + `hematological` burden capacity + active iron signals (which live under the `nutritional` burden system). This is the one domain that genuinely requires intentional cross-system aggregation in the assembler.

### Launch readiness

**LAUNCHABLE WITH LIGHT ASSEMBLY**

Light assembly: domain score assembler pulls from `cbc` system score + `hematological` burden capacity + nutritional iron signal activations. No new SSOT or KB work needed — the signals and WHY are already built.

### Confidence inputs already in system

Hemoglobin + hematocrit are minimum (cbc min_biomarkers_required: 2). Ferritin is the critical additional marker — its presence doubles interpretive depth. MCV + MCH extend pattern differentiation. Iron + transferrin complete the full pathway picture.

### Score band derivation

The `cbc` system score provides the red cell floor. When ferritin is present and iron signals are active (iron_deficiency_context at_risk state), the domain score is pulled toward a fuller iron-pathway assessment. Signal activation state must be a domain score modifier in the assembler.

### What the expanded card can truthfully say today

Red cell health status, iron store status if ferritin present, microcytic/normocytic/macrocytic pattern differentiation if MCV present, iron transport pattern if transferrin present, oxygen carrying capacity assessment, WHY depth across eight registered hypothesis generators.

### Codebase paths requiring change

- `domain_score_assembler.py` — blood_iron_oxygen domain: aggregate cbc system score + hematological capacity + iron signal states. Most complex single assembly rule of the six.
- No SSOT or KB changes needed.

---

## Domain 5: Thyroid & Energy Regulation

**Consumer label:** Thyroid & energy regulation
**Clinical label:** Thyroid Axis Status

### Internal engine mapping

| Layer | Current assets |
|---|---|
| Scoring system | **None.** Thyroid is absent from scoring_policy.yaml. The `hormonal` system in scoring_policy has weight 0 and no biomarkers. |
| Burden system | `thyroid` in burden_registry — tsh (weight 0.8, BOTH_SIDES_RISK), free_t3 (0.5), free_t4 (0.5), tpo_ab (0.6, HIGH_IS_RISK), tgab (0.4, HIGH_IS_RISK). Full panel covered. |
| Capacity score | `system_capacity_scores["thyroid"]` computed by burden engine. Already emitted in AnalysisDTO. |
| Signals | signal_thyroid_tsh_context (lab_range_exceeded, escalates on fT3/fT4 pattern), signal_tsh_high, signal_tsh_low, signal_free_t3_high, signal_free_t3_low, signal_free_t4_high, signal_free_t4_low, signal_tpo_ab_high, signal_tgab_high |
| KB packages | pkg_thyroid_tsh_context, pkg_s24_tsh_high_hypothyroidism, pkg_s24_tsh_low_hyperthyroidism, pkg_kb47_free_t3_high_t3_predominant_thyrotoxicosis, pkg_kb47_free_t3_low_low_t3_syndrome, pkg_kb47_free_t4_high_thyrotoxicosis_context, pkg_kb47_free_t4_low_thyroid_hormone_deficiency |
| WHY generators | load_tsh_hypotheses_v1, load_tsh_high_hypotheses_v1, load_tsh_low_hypotheses_v1, load_free_t3_high_hypotheses_v1, load_free_t3_low_hypotheses_v1, load_free_t4_high_hypotheses_v1, load_free_t4_low_hypotheses_v1, load_tpo_ab_high_hypotheses_v1, load_tgab_high_hypotheses_v1 |

### Critical gap

There is **no scoring_policy system for thyroid**. The only numeric score that can represent thyroid today is `system_capacity_scores["thyroid"]` from the burden engine. This is computed as `100 - (thyroid_burden × 12.5)` — a valid direction signal but using a different calibration than the range-position scores used by all other active systems.

Consuming this directly as a consumer domain score without acknowledging the calibration difference is an architectural risk.

### Two resolution paths

**Path A (recommended — medium work, architecturally clean):**
Add thyroid as a scored system in scoring_policy.yaml with TSH, free_t4, free_t3 as biomarkers with scoring bands. TSH bands exist in ranges.yaml. This makes thyroid consistent with all other domain scores and is the correct long-term approach. This is a HIGH-risk governed SSOT change.

**Path B (faster — interim only):**
Use `system_capacity_scores["thyroid"]` directly in the domain score assembler with a documented calibration caveat. Ship sooner but with an acknowledged calibration inconsistency. Only appropriate as a time-bounded interim while Path A is being governed.

### Missing pieces

No scoring_policy system entry for thyroid. No TSH/FT4/FT3 scoring bands in scoring_policy.yaml (though bands exist in ranges.yaml). Calibration question between burden and range-position scoring.

### Launch readiness

**LAUNCHABLE WITH MEDIUM BACKEND WORK**

The WHY layer is strong. The analytical signals are comprehensive. The only gap is infrastructure: no scoring_policy system for thyroid. Resolved by a single governed SSOT sprint.

### Confidence inputs already in system

TSH is the gate — if absent, domain cannot score. Free T4 and T3 escalate confidence. TPO/TgAb add autoimmune axis context. Routine thyroid panel (TSH only): moderate confidence. Extended panel (TSH + FT4 + FT3): high confidence.

### What the expanded card can truthfully say today (using burden capacity as interim)

TSH axis status, direction of deviation (high = possible hypothyroid context, low = possible hyperthyroid context), antibody-driven autoimmune pattern when TPO/TgAb present, WHY depth across seven registered generators.

### Codebase paths requiring change

- `backend/ssot/scoring_policy.yaml` — add `thyroid` system with tsh, free_t4, free_t3 biomarkers and scoring bands. **Path A — recommended. HIGH risk governed SSOT change.**
- `backend/ssot/clusters.yaml` — add thyroid cluster if using cluster-based aggregation
- `domain_score_assembler.py` — thyroid domain assembly (straightforward once scoring_policy entry exists)
- If using Path B interim: read from `system_capacity_scores["thyroid"]` with explicit confidence downgrade

---

## Domain 6: Kidney Function

**Consumer label:** Kidney function
**Clinical label:** Renal Filtration / Renal Strain Status

### Internal engine mapping

| Layer | Current assets |
|---|---|
| Scoring system | `kidney` in scoring_policy.yaml — creatinine (weight 0.6, age+sex adjusted), urea (weight 0.4). Weight 0.15 overall. min_biomarkers_required: 1. |
| Burden system | `renal` in burden_registry — creatinine (0.8), urea (0.5), egfr (0.7, LOW_IS_RISK), urate (0.5, HIGH_IS_RISK), urea_creatinine_ratio (0.5) |
| Derived ratios | urea_creatinine_ratio in scoring_policy derived_ratio_policy_bounds |
| Signals | signal_creatinine_high, signal_urea_high, signal_urate_high |
| KB packages | pkg_s24_creatinine_high_renal, pkg_s24_urea_high_renal, pkg_kb47_egfr_low_chronic_kidney_function_reduction, pkg_kb47_egfr_low_hemodynamic_filtration_drop, pkg_kb52c_creatinine_high_reduced_glomerular_filtration, pkg_kb52c_creatinine_low_low_muscle_mass_or_low_generation |
| WHY generators | load_creatinine_high_hypotheses_v1, load_urea_high_hypotheses_v1, load_urate_high_hypotheses_v1 |

### Current codebase support

**Moderate.** The scoring_policy kidney system (creatinine + urea) gives a functional starting point for most routine biochemistry panels. The burden registry adds eGFR and urate. The WHY layer covers creatinine, urea, and urate with reasonable depth. The two eGFR KB packages (chronic reduction vs hemodynamic drop) show architectural sophistication.

### Missing pieces

eGFR is not in scoring_policy.yaml — it is only in burden_registry (weight 0.7, LOW_IS_RISK). eGFR is clinically the most important renal filtration marker and is often computed automatically by labs. Not scoring eGFR directly means the domain score is built primarily from creatinine, which is an indirect proxy.

This is a meaningful but not blocking gap — creatinine and urea scores will still correctly identify significant renal strain in most panels. eGFR addition is the medium-term priority for this domain.

Note: adding eGFR to scoring_policy also requires a new scoring type for inverse-direction biomarkers (LOW_IS_RISK), since the current score_curve model assumes high values are bad. This is a small but real scoring engine change.

### Launch readiness

**LAUNCHABLE WITH LIGHT ASSEMBLY**

Light assembly: blend scoring_policy `kidney` system score with `renal` burden capacity (which includes eGFR direction). When urate is also present and elevated, surface the gout/renal context from signal_urate_high.

### Confidence inputs already in system

Creatinine alone meets min_biomarkers_required of 1. Urea adds confidence. eGFR (if lab-reported) significantly extends interpretive quality. Urate adds metabolic-renal context.

### Score band derivation

scoring_policy `kidney` score maps directly to proposed bands. The score correctly penalises elevated creatinine via range-position bands.

### What the expanded card can truthfully say today

Kidney filtration marker status, creatinine/urea pattern, low-creatinine/low-muscle-mass differentiation (pkg_kb52c_creatinine_low), eGFR directional context from renal burden capacity, urate/gout axis if urate present.

### Codebase paths requiring change

- `domain_score_assembler.py` — kidney domain: blend scoring_policy `kidney` + `renal` burden capacity
- Medium-term: add `egfr` to scoring_policy.yaml as a direct biomarker. Requires new scoring engine support for LOW_IS_RISK band direction (eGFR low = bad, not high = bad).

---

## Final Summary

### A. Strongest 2–3 domains for earliest implementation (least risk)

**1. Blood sugar control** — cleanest internal mapping of all six. scoring_policy `metabolic` system score is a direct blood sugar proxy using only glucose + hba1c + insulin. The insulin resistance signal is the repo's most evidence-complete signal. No assembly complexity. One-to-one system score mapping.

**2. Cardiovascular health** — most analytically mature domain in the entire repo. Six WHY generators registered, lipid transport signals comprehensive, derived ratios complete, homocysteine pathway present, ApoB/ApoA1 depth when available. scoring_policy cardiovascular score maps directly. Can show meaningful sub-system contributing factors without new backend work.

**3. Liver health** — scoring_policy liver system is thin (alt/ast only, weight 0.10) but has min_biomarkers_required of 1 and is reliable for most routine panels. WHY layer is rich enough (seven generators, steatotic/cholestatic/muscle-source differentiation) to make the expanded card genuinely informative. Light assembly to blend burden capacity for extended panels.

### B. Domains most likely to need new governed work

**Thyroid & energy regulation** is the only domain with no scoring_policy system entry at all. The analytical depth is strong — signals, WHY generators, and KB packages are all present — but the scoring infrastructure gap is real. Adding thyroid to scoring_policy.yaml is a HIGH-risk governed SSOT change requiring full governance. Without it, only burden capacity is available, with calibration inconsistency vs other domains.

**Blood, iron & oxygen** is analytically complete but requires the most complex assembly logic. Iron stores (nutritional burden system) and red cell indices (hematological + cbc scoring system) are split across three internal systems that must be unified for a single consumer score. The domain is launchable, but the assembler logic is the most non-trivial of the six.

**Kidney function** is technically launchable from creatinine + urea, but clinically incomplete without eGFR scoring. Adding eGFR to scoring_policy also requires a new inverse-direction scoring type in the scoring engine. This is the most architecturally novel of the required changes.

### C. Launch sequence recommendation: Phased 3-then-6

Flat 6-score launch is **not recommended**. Three domains are ready or near-ready with minimal assembly; three have real infrastructure gaps (thyroid: no scoring system; iron/blood: cross-system assembly; kidney: eGFR gap and inverse scoring type).

**Recommended sequence:**

**Wave 1 (Blood sugar control, Cardiovascular health, Liver health)**
- All three map from existing scored systems in scoring_policy.yaml
- All three have mature WHY depth for expanded card content
- No SSOT changes required
- Light assembly only for liver (blend with hepatic burden capacity when extended markers present)

**Wave 2 (Blood, iron & oxygen; Kidney function; Thyroid & energy regulation)**
- Blood/iron/oxygen: cross-system assembler logic across cbc + hematological + nutritional
- Kidney: blend with renal burden capacity; eGFR addition for full coverage
- Thyroid: requires scoring_policy system entry (Path A) or interim burden capacity derivation (Path B)

### D. Most realistic sprint sequence from current repo state

| Sprint | change_type | Risk | Description |
|---|---|---|---|
| **D-1** | BEHAVIOUR | HIGH | Implement `domain_score_assembler.py`. New analytics component in `backend/core/analytics/`. Aggregates system scores + capacity scores + active signals → 6 `DomainScore` objects. Add `consumer_domain_scores` field to AnalysisDTO. Wire into orchestrator post-arbitration. Wave 1 logic only (cardiovascular, metabolic/blood_sugar, liver). |
| **D-2** | CONTENT | HIGH | Add `thyroid` scoring system to scoring_policy.yaml with tsh, free_t4, free_t3 scoring bands + weights. Add eGFR support to scoring_policy (new LOW_IS_RISK scoring type or derived ratio policy). Governed SSOT sprint. Add thyroid to clusters.yaml. |
| **D-3** | BEHAVIOUR | HIGH | Extend domain_score_assembler.py for Wave 2 domains: blood_iron_oxygen (cross-system cbc + hematological + iron signals), kidney (kidney score + renal capacity + egfr), thyroid (now using scoring_policy thyroid system from D-2). |
| **D-4** | BEHAVIOUR | STANDARD | Implement domain confidence logic per domain. Count present markers vs expected full panel. Assess signal coherence (concordant vs contradictory signals). Output HIGH/MEDIUM/LIMITED confidence per domain. Extend DomainScore model with confidence field and "what would improve confidence" list. |
| **D-5** | BEHAVIOUR | STANDARD | Frontend: new `HealthDomainScoreCards` component. Score display (0–100 + band label). Confidence badge. Expandable panel showing contributing signals, WHY hypotheses, "what would improve confidence" items. Wire from AnalysisDTO consumer_domain_scores. |
| **D-6** | CONTENT | LOW | Governed expanded card copy assets. Truthful "what this score means", "what contributed most", "what this may mean over time" content per domain. Static governed copy — no LLM. |

---

## Cross-cutting implementation notes

### The domain_score_assembler.py is the key new component

It sits in `backend/core/analytics/` and consumes `AnalysisResult` outputs (scoring system results + capacity scores + active signals). It produces `consumer_domain_scores`. It must not touch the scoring engine, burden engine, or signal evaluator — it is a read-and-aggregate layer above them.

### The AnalysisDTO extension is the new contract surface

`consumer_domain_scores: Optional[Dict[str, DomainScore]]` must be added with `Optional` default (backward compatible). Existing results page rendering continues to work off existing fields. Domain score cards are an additive layer — they do not replace existing ResultsHeroBlocks, SystemUnderstandingSection, or narrative surfaces.

### Calibration consistency principle

All six consumer domain scores should use the same 0–100 calibration basis wherever possible. Domains 1–3 and 6 can use scoring_policy range-position scores directly. Domains 4 and 5 require either Path A (add to scoring_policy) for calibration consistency, or an explicit calibration note when using burden capacity as an interim source.

### Three-layer naming discipline must be preserved throughout

- Dashboard / patient UI → consumer label only
- Clinician handout / PDF → clinical label (unchanged by this work)
- Engine / mapping docs → internal phenotype/system logic (unchanged by this work)

Consumer labels must never appear in the clinician report. Clinical labels must never be used as consumer-facing card titles.

---

*End of blueprint. This document is research-only. All implementation requires GPT-authored work packages, Claude hardening, and kernel execution per Automation Bus SOP v1.3.1.*
