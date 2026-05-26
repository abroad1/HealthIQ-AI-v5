# DOMAIN-R1 — Launch-Core Health Domain Readiness Audit

**Date:** 2026-05-25
**Authority source:** `docs/architecture/User Health to Systems Map_FINAL.md` (v0.4)
**Audit type:** Read-only investigation — no code changes

---

## 1. Executive Verdict

| Domain | Verdict |
|---|---|
| Cardiovascular health | **Launchable with light assembly** |
| Blood sugar control | **Launchable with light assembly** |
| Liver health | **Launchable with light assembly** |
| Blood, iron & oxygen | **Not ready — medium backend/governed work required** |
| Thyroid & energy regulation | **Not ready — medium backend/governed work required** |
| Kidney function | **Not ready — medium backend/governed work required** |

**Recommended implementation strategy: phased three-score then six-score.**

Wave 1 (cardiovascular, blood sugar, liver) already has end-to-end deterministic infrastructure: scoring rails, domain score assembler, DTO fields, TypeScript types, and a rendered frontend component. The output exists in the live DTO. The gap is that Wave 1 domain cards are hidden behind a `ResultsDisclosureSection` with `defaultOpen={false}` — they are not in the main journey. Light assembly means surfacing what already exists and polishing the copy already generated.

Wave 2 (blood iron & oxygen, thyroid & energy regulation, kidney function) requires new domain score assembler blocks analogous to `cv_block()`, `met_block()`, and `liv_block()` in `backend/core/analytics/domain_score_assembler.py`. Scoring rails exist (`kidney`, `cbc`/`hematological`, `thyroid`) but confidence logic must be designed, IDL records must exist or be authored, and narrative sentences must be governed. This is non-trivial and must not be compressed into Wave 1.

---

## 2. Source Authority Summary

Source: `docs/architecture/User Health to Systems Map_FINAL.md` (v0.4)

**Three naming layers (non-negotiable):**
1. **Consumer label** — calm, simple, emotionally legible dashboard language
2. **Clinical handout label** — medically grounded language for clinician-facing output
3. **Internal engine mapping** — phenotypes, systems, signal groups, clusters, governed assets

**Non-negotiable rule:** Consumer labels must never replace clinical labels in the clinician PDF/handout. Dashboard/patient UI uses consumer labels; clinician handout/PDF uses clinical labels; engine/mapping docs use internal phenotype/system logic. These three layers must not be conflated in any implementation.

**Six launch-core domains (Strategy A, Wave 1):**
1. Cardiovascular health → Cardiometabolic / Vascular Risk Status → lipid transport, vascular inflammation, homocysteine/endothelial strain
2. Blood sugar control → Glycaemic Regulation / Insulin Resistance Status → insulin resistance phenotype, glycaemic dysregulation, TG/HDL coupling
3. Liver health → Hepatic-Metabolic Strain Status → hepatic stress, fatty-liver-adjacent, metabolic overload
4. Blood, iron & oxygen → Iron-Erythropoietic / Oxygen-Carrying Status → iron deficiency/inflammation, anaemia-adjacent, one-carbon/macrocytosis
5. Thyroid & energy regulation → Thyroid Axis Status → thyroid-axis disturbance, thyroid-linked lipid disturbance
6. Kidney function → Renal Filtration / Renal Strain Status → renal strain, eGFR/creatinine/urea patterns

**Second-wave only (do not promote without evidence):**
7. Silent inflammation → Systemic Inflammatory Activity
8. Hormone balance → Gonadal / Sex-Hormone Balance

---

## 3. Current Repo Outputs Relevant to Domain Scoring

All citations verified from file reads.

**`consumer_domain_scores` — EXISTS and is live.**
- File: `backend/core/analytics/domain_score_assembler.py` (entire file)
- Function: `assemble_consumer_domain_scores_v1()` — builds three Wave 1 rows: `wave1_cardiovascular`, `wave1_blood_sugar`, `wave1_liver`
- Confirmed in the live DTO from UAT audit (`docs/audit-papers/POST_MAP_R1A_world_class_results_experience_audit_3c4d2b1c.md`, section 9, row: "consumer_domain_scores | Yes — cardiovascular card with good headline_sentence")
- Root key present in `frontend_contract_v1.py` line 36: `"consumer_domain_scores"`

**`system_capacity_scores` — EXISTS and is live.**
- Computed by `scale_capacity_scores_v1` (imported in `orchestrator.py` line 76)
- In DTO (confirmed in UAT audit, section 9: "system_capacity_scores | Yes (11 systems, most at 100) | Not directly surfaced")
- Root key: `backend/core/dto/frontend_contract_v1.py` line 32: `"system_capacity_scores"`
- Systems confirmed in SSOT: `cardiovascular`, `metabolic`, `hepatic`, `hematological`, `immune`, `thyroid`, `renal`, `hormonal`, `nutritional`

**`interpretation_display_layer_v1` — EXISTS and is live.**
- Computed by `publish_interpretation_display_layer_v1` (orchestrator line 53)
- Records confirmed: `ph_vascular_hcy_inflammation_v1`, `ph_lipid_residual_ldl_favourable_transport_v1`, `ph_hba1c_metabolic_stress_v1`, `ph_metabolic_early_ir_v1`, `ph_hepatic_alt_inflammatory_v1`
- Selected by domain_score_assembler via `_IDL_ORDER_CV`, `_IDL_ORDER_MET`, `_IDL_ORDER_LIV`

**`root_cause_v1` — EXISTS**, surfaced in `clinician_report_v1.sections.root_cause` (UAT confirmed, section 9)

**`narrative_report_v1` — EXISTS.** Fields: `retail_summary`, `body_overview`, `lead_narrative`, `secondary_narratives`, `longitudinal_narrative`, `next_steps_narrative`, `clinician_synthesis`. Live truncation bug confirmed in `lead_narrative` (UAT section 5, "route homocysteine toward..." cut off mid-sentence).

**`clinician_report_v1` — EXISTS and is live.** Appropriately behind a disclosure toggle. `frontend_contract_v1.py` confirms it as a root key. Consumer label / clinical label separation is correctly enforced at this layer.

**`balanced_systems_v1` — EXISTS and is live.** Surfaced in "What's working well" section.

**Clusters — EXISTS.** `cluster_engine_v2.py` (ClusterEngineV2) produces cluster objects with `cluster_id`, `name`, `biomarkers`, `severity`, `confidence`. Current clusters confirmed from UAT: `cardiovascular_4_biomarkers` as `primary_driver_system_id`.

**Biomarker scores/statuses — EXISTS** for all 79 markers in UAT panel. Per-biomarker: `value`, `score` (0–100), `status` (optimal/normal/elevated/critical), `educational_explainer` (partial), `contribution_context` (partial).

**Signal IDs (`signal_results`) — EXISTS.** `signal_evaluator.py` runs during pipeline, results serialized into InsightGraph and emitted. Active signals in UAT: `signal_homocysteine_elevation`, `signal_lipid_transport_dysfunction`, cardiovascular signals, etc.

**Knowledge Bus / package estate — EXISTS with material coverage.** Confirmed packages with `signal_library.yaml`:
- `pkg_lipid_transport` — lipid signals, cardiovascular domain
- `pkg_insulin_resistance` — metabolic/blood sugar domain
- `pkg_hepatic_metabolic_stress` — liver domain
- `pkg_homocysteine_elevation_context` — cardiovascular subdomain
- `pkg_b12_deficiency_context`, `pkg_iron_deficiency_context`, `pkg_iron_overload_context` — blood/iron domain
- `pkg_thyroid_tsh_context` — thyroid domain
- `pkg_s24_*` series — broad signal library coverage including `pkg_s24_creatinine_high_renal`, `pkg_s24_tsh_high/low_hypothyroidism/hyperthyroidism`, `pkg_s24_hba1c_high_glycaemia`, `pkg_s24_alt_high_hepatocellular_injury`, `pkg_s24_ggt_high_hepatic`, `pkg_s24_ferritin_*`, `pkg_s24_hgb_low_anemia`, `pkg_s24_ldl_high_dyslipidaemia`, etc.
- `pkg_chronic_inflammation` — second-wave domain
- No comprehensive renal filtration domain package found

---

## 4. Domain-by-Domain Readiness Matrix

| Domain | Current supporting outputs | Biomarkers/signals/patterns available | Score source candidate | Confidence source candidate | Explainer source candidate | Current readiness | Main gaps | Recommended implementation route |
|---|---|---|---|---|---|---|---|---|
| Cardiovascular health | `wave1_cardiovascular` in consumer_domain_scores; scoring rail `cardiovascular`; IDL records `ph_vascular_hcy_inflammation_v1`, `ph_lipid_residual_ldl_favourable_transport_v1`; signal evaluator CV signals | `total_cholesterol`, `ldl_cholesterol`, `hdl_cholesterol`, `triglycerides`, `tc_hdl_ratio`, `apob`, `apoa1`, `lipoprotein_a`, `homocysteine`, derived ratios | `health_system_scores.cardiovascular.overall_score` | `_cardiovascular_confidence_tier()` in domain_score_assembler.py (panel coverage × derived ratios) | `headline_sentence`, `contributor_sentence`, `consequence_sentence`, `confidence_sentence`, `next_step_sentence` — all deterministically assembled | **Launchable with light assembly** | Cards hidden behind disclosure toggle; some template copy; `evidence_anchor_sentence` partially implemented; ApoA1 scoring inconsistency noted | Surface existing Wave1DomainCards in main journey; fix reveal position |
| Blood sugar control | `wave1_blood_sugar` in consumer_domain_scores; scoring rail `metabolic`; IDL records `ph_hba1c_metabolic_stress_v1`, `ph_metabolic_early_ir_v1` | `glucose`, `hba1c`, `insulin`, `triglycerides`, derived `tyg_index`, `homa_ir` | `health_system_scores.metabolic.overall_score` | `_metabolic_blood_sugar_confidence_tier()` (glucose + HbA1c core; insulin/TG enhance) | Same assembled narrative fields as CV | **Launchable with light assembly** | `_MET_NO_ACTIVE_SIGNAL_CONTRIBUTOR` fallback fires when only HbA1c present (common panel) — copy is honest but constrained; insulin rarely uploaded | Surface in main journey; no structural changes needed |
| Liver health | `wave1_liver` in consumer_domain_scores; scoring rail `liver` + `hepatic` burden/capacity; IDL record `ph_hepatic_alt_inflammatory_v1` | `alt`, `ast`, `ggt`, `alp`, `albumin`, `bilirubin`, `total_protein`, `fib_4` | min(`health_system_scores.liver.overall_score`, `system_capacity_scores.hepatic`) | `_liver_confidence_tier_domain()` (requires alt; high if alt+ast+ggt or fuller panel) | Assembled narrative; D-7 neutral consequence gate when surface reads stable | **Launchable with light assembly** | Confidence often "low" on minimal liver panels (alt-only); caveat copy verbose; missing_marker_ids list can be long | Surface in main journey; caveat copy polish before wide release |
| Blood, iron & oxygen | No domain assembler block; no `wave1_blood_iron_oxygen` in consumer_domain_scores; `hematological` system_capacity_score exists; iron studies split to `nutritional` system | `hemoglobin`, `hematocrit`, `rbc`, `mcv`, `mch`, `mchc`, `rdw_cv`, `iron`, `transferrin`, `transferrin_saturation`, `ferritin`, `folate`, `vitamin_b12`, `active_b12` | None. `cbc` rail exists but covers CBC only; iron studies are in `nutritional` — not blended into any current domain score | None. No `_blood_iron_confidence_tier()` function exists | KB packages exist (`pkg_iron_deficiency_context`, `pkg_s24_hgb_low_anemia`, etc.) but no IDL order arrays for this domain | **Not ready — medium backend/governed work required** | No domain assembler block; no IDL records ordered for this domain; scoring rail does not cover iron/B12/folate; system key split (`hematological` vs `nutritional`) creates assembly challenge | DOMAIN-R2C sprint: new assembler block; define scoring rail; author IDL records for iron-erythropoietic phenotypes |
| Thyroid & energy regulation | No domain assembler block; no `wave1_thyroid` in consumer_domain_scores; scoring_policy `hormonal` system has `system_weight: 0.0` and empty biomarker list; `thyroid` system_capacity_score likely exists; KB packages exist | `tsh`, `free_t4`, `free_t3`, `tpo_ab`, `tgab` | None. scoring_policy.yaml `hormonal` system is zeroed out. A thyroid scoring rail would need to be added or `hormonal` system repurposed | None. No `_thyroid_confidence_tier()` function exists | KB packages: `pkg_thyroid_tsh_context`, `pkg_s24_tsh_high_hypothyroidism`, `pkg_s24_tsh_low_hyperthyroidism`; no IDL records for thyroid in `_IDL_ORDER_*` arrays | **Not ready — medium backend/governed work required** | No scoring rail; no assembler block; no IDL phenotype integration; scoring_policy.yaml `hormonal` weight is 0.0 and biomarker list is empty | DOMAIN-R2C sprint: add thyroid scoring rail to scoring_policy.yaml (HIGH risk); build assembler block; author IDL records |
| Kidney function | No domain assembler block; no `wave1_kidney` in consumer_domain_scores; scoring rail `kidney` exists with `creatinine` and `urea` only; `renal` system_capacity_score exists | `creatinine`, `urea`, `egfr`, `uacr`, `urine_protein_creatinine_ratio`, `cystatin_c`, `urate`, `urea_creatinine_ratio` (derived) | `health_system_scores.kidney.overall_score` exists but `egfr` not in scoring_policy.yaml `kidney` rail; score is incomplete without it | None. No `_kidney_confidence_tier()` function | KB package: `pkg_s24_creatinine_high_renal`; investigation specs for creatinine and urea; no renal IDL records in domain assembler order arrays | **Not ready — medium backend/governed work required** | No assembler block; scoring rail incomplete (no eGFR); no IDL records ordered for renal; confidence logic undefined; mild-abnormality handling needs care | DOMAIN-R2C sprint: extend kidney rail with eGFR; build assembler block; design confidence logic |

---

## 5. Domain Detail Sections

### Domain: Cardiovascular Health

**Consumer label:** Cardiovascular health
**Clinical handout label:** Cardiometabolic / Vascular Risk Status
**Internal mapping:** `wave1_cardiovascular`; scoring rail `cardiovascular` (scoring_policy.yaml); burden/capacity key `cardiovascular`; IDL `ph_vascular_hcy_inflammation_v1` and `ph_lipid_residual_ldl_favourable_transport_v1`

**Relevant current systems/clusters/signals:** `lipid_transport` system in signal evaluator; `cardiovascular` cluster; signals: `signal_lipid_transport_dysfunction`, `signal_ldl_cholesterol_high`, `signal_hdl_cholesterol_low`, `signal_triglycerides_high`, `signal_homocysteine_elevation`, `signal_total_cholesterol_high` (all coded in `domain_score_assembler.py` lines 139–153)

**Relevant biomarkers (SSOT):** `total_cholesterol`, `ldl_cholesterol`, `hdl_cholesterol`, `triglycerides`, `tc_hdl_ratio`, `tg_hdl_ratio`, `ldl_hdl_ratio`, `non_hdl_cholesterol`, `apob`, `apoa1`, `apob_apoa1_ratio`, `homocysteine`, `lipoprotein_a`, `remnant_cholesterol`

**Existing governed assets:** `pkg_lipid_transport` (signal_library.yaml present); `pkg_homocysteine_elevation_context` (signal_library.yaml, clinical_signoff.md); IDL records `ph_vascular_hcy_inflammation_v1`, `ph_lipid_residual_ldl_favourable_transport_v1`; `pkg_s24_ldl_high_dyslipidaemia`, `pkg_s24_hdl_low_cardiovascular`, `pkg_s24_hdl_high_cardiovascular`, `pkg_s24_triglycerides_high_metabolic`

**Existing frontend-visible content:** Score, band, confidence tier, headline_sentence, contributor_sentence, confidence_sentence, consequence_sentence, next_step_sentence, evidence_anchor_sentence, missing_marker_ids — all fully rendered in `Wave1DomainCards.tsx`. Currently hidden behind `ResultsDisclosureSection` with `defaultOpen={false}` (`results/page.tsx` line 808–813).

**Potential score logic:** Already implemented. `health_system_scores.cardiovascular.overall_score` → `_as_float_0_100()` → `_band_label_from_0_100()`. Score is 0–100, band is strong/stable/watch/review.

**Potential confidence logic:** Already implemented. `_cardiovascular_confidence_tier()` — high if full lipid panel including derived ratios; medium if core lipid markers; low if only TC/LDL. Blended with cluster confidence rail.

**Potential expanded-card content:** Already implemented in `Wave1DomainCards.tsx`. Why this score, confidence, what this may mean, what to do next, what would improve confidence (missing markers), caveats. Cards also surface `evidence_anchor_sentence`.

**Risks:** ApoA1 scoring inconsistency noted in UAT (value 1.73 above range 0.79–1.69 but scored optimal — should be investigated separately). "On this panel" template language leaks into consumer copy. Homocysteine-led cardiovascular story can conflict with strong lipid numbers — D-4 coherence gate in `headline_cv_coherent()` handles this case.

**Implementation difficulty:** Low. Infrastructure complete. Main work: change `defaultOpen={false}` to `defaultOpen={true}` or move `Wave1DomainCards` above the disclosure section into the main journey.

**Verdict:** Launchable with light assembly — specifically, repositioning from hidden to visible in the main journey.

---

### Domain: Blood Sugar Control

**Consumer label:** Blood sugar control
**Clinical handout label:** Glycaemic Regulation / Insulin Resistance Status
**Internal mapping:** `wave1_blood_sugar`; scoring rail `metabolic`; IDL `ph_hba1c_metabolic_stress_v1`, `ph_metabolic_early_ir_v1`

**Relevant current systems/clusters/signals:** `metabolic` cluster; signals: `signal_hba1c_*`, `signal_insulin_resistance`, `signal_glucose_*`

**Relevant biomarkers (SSOT):** `glucose`, `hba1c`, `hba1c_pct`, `insulin`, `homa_ir`, `tyg_index` (derived), `triglycerides` (enhancer)

**Existing governed assets:** `pkg_insulin_resistance` (signal_library + research_brief); `pkg_glucose_dysregulation_hba1c_context`; `pkg_s24_hba1c_high_glycaemia`; `pkg_s24_triglycerides_high_metabolic`; IDL records `ph_hba1c_metabolic_stress_v1`, `ph_metabolic_early_ir_v1`

**Existing frontend-visible content:** Same as cardiovascular — fully assembled and rendered, currently hidden inside `ResultsDisclosureSection`.

**Potential score logic:** Already implemented. `health_system_scores.metabolic.overall_score`. Metabolic system includes glucose, HbA1c, insulin with weights in scoring_policy.yaml (weight 0.4 each).

**Potential confidence logic:** Already implemented. `_metabolic_blood_sugar_confidence_tier()` — high if glucose + HbA1c + insulin + (TG or TYG); high if glucose + HbA1c + (TG or insulin); medium if glucose + HbA1c; low if only one marker.

**Potential expanded-card content:** Full narrative already assembled. Note: `_MET_NO_ACTIVE_SIGNAL_CONTRIBUTOR` honest fallback fires when only HbA1c is present without glucose or insulin — "HbA1c is within range on this panel. Glucose and insulin were not included, so a fuller glycaemic read would require those markers." This is appropriate honest copy.

**Risks:** Common consumer panels often include only HbA1c without fasting glucose or insulin. The "limited confidence" / honest fallback path is the most common real-world scenario. This is handled correctly but should be verified in UAT against a minimal-panel result.

**Implementation difficulty:** Low. Same as cardiovascular — reveal existing card.

**Verdict:** Launchable with light assembly.

---

### Domain: Liver Health

**Consumer label:** Liver health
**Clinical handout label:** Hepatic-Metabolic Strain Status
**Internal mapping:** `wave1_liver`; scoring rail `liver` (alt, ast only in scoring_policy.yaml); burden/capacity key `hepatic`; IDL `ph_hepatic_alt_inflammatory_v1`

**Relevant current systems/clusters/signals:** `hepatic` system in burden/capacity; `liver` scoring rail; signals from `signal_alt_*`, `signal_ast_*`, `signal_ggt_*`, `signal_hepatic_*`, `signal_bilirubin_*`

**Relevant biomarkers (SSOT):** `alt`, `ast`, `ggt`, `alp`, `albumin`, `bilirubin`, `total_protein`, `globulin`, `fib_4`, `ast_alt_ratio` (derived)

**Existing governed assets:** `pkg_hepatic_metabolic_stress` (signal_library, research_brief, clinical_signoff); `pkg_hepatic_alt_context`; `pkg_s24_alt_high_hepatocellular_injury`; `pkg_s24_ggt_high_hepatic`; IDL record `ph_hepatic_alt_inflammatory_v1`

**Existing frontend-visible content:** Fully assembled and rendered, currently hidden. Note the explicit liver key split: scoring rail uses `liver`, burden/capacity uses `hepatic` — `domain_score_assembler.py` lines 8–9 document this governance rule explicitly.

**Potential score logic:** Already implemented. Blended score = min(liver_rail_score, hepatic_capacity_score). Documented in `domain_score_assembler.py` lines 508–511.

**Potential confidence logic:** Already implemented. `_liver_confidence_tier_domain()` — requires alt present; high if alt+ast+ggt+alp+albumin or alt+ast+ggt (n≥4 with ast); medium if alt+ast; low otherwise. Appropriately cautious.

**Potential expanded-card content:** Full narrative assembled. D-7 coherence gate prevents strain consequence copy when surface reads stable and no active hepatic signals — prevents false alarm copy when liver markers are normal.

**Risks:** Liver confidence is frequently "low" on consumer panels that only include alt without ast/ggt/alp. The caveat lines are verbose — `_LIVER_CAVEAT_USER_LINES` generates two sentences. Missing marker list can include 4–5 markers even for a reasonable panel. This could make the liver card feel like a "we can't really say" message rather than a useful score.

**Implementation difficulty:** Low for surfacing. Medium for caveat polish.

**Verdict:** Launchable with light assembly. Caveat copy should be reviewed before wide release.

---

### Domain: Blood, Iron & Oxygen

**Consumer label:** Blood, iron & oxygen
**Clinical handout label:** Iron-Erythropoietic / Oxygen-Carrying Status
**Internal mapping:** None currently. Engine fragments exist across `hematological` (CBC markers in scoring_policy.yaml) and `nutritional` (iron studies, B12, folate in SSOT).

**Relevant current systems/clusters/signals:** `hematological` system capacity scores; `immune` system (ferritin, CRP — iron-inflammation coupling); signals for `signal_mcv_*`, `signal_hemoglobin_*`, `signal_ferritin_*`, `signal_transferrin_*`, `signal_b12_*`; IDL record `ph_one_carbon_homocysteine_macrocytosis_v1` (confirmed in UAT as "Methylation pathway pattern" card — strongest content on the page)

**Relevant biomarkers (SSOT):** `hemoglobin`, `hematocrit`, `rbc`, `mcv`, `mch`, `mchc`, `rdw_cv`, `rdw_sd`, `iron`, `transferrin`, `transferrin_saturation`, `ferritin`, `folate`, `vitamin_b12`, `active_b12`, `crp` (inflammation-iron coupling)

**Existing governed assets:** `pkg_iron_deficiency_context` (signal_library); `pkg_iron_overload_context` (signal_library); `pkg_b12_deficiency_context` (signal_library); `pkg_s24_hgb_low_anemia`; `pkg_s24_ferritin_high_overload`; `pkg_s24_ferritin_low_iron_deficiency`; `pkg_s24_folate_low_deficiency`; investigation specs: `inv_hgb_low_anemia.yaml`, `inv_mcv_high_macrocytosis.yaml`, `inv_ferritin_spec_v1.yaml`, `inv_vitamin_b12_spec_v1.yaml`, `inv_folate_low_deficiency.yaml`

**Existing frontend-visible content:** Zero domain card. Transferrin (critical, score 5/100 in UAT) is narratively silent. MCV (score 19/100 in UAT) has no explainer. Homocysteine is the primary driver but its card has no educational content. The IDL pattern `ph_one_carbon_homocysteine_macrocytosis_v1` is the best content on the page per UAT but is not connected to any domain score.

**Potential score logic:** Not yet designed. Candidate approach: blend `system_capacity_scores.hematological` (covers CBC) with a new iron-studies scoring rail tracking `hemoglobin`, `ferritin`, `transferrin_saturation`, `iron`. The SSOT categorises iron studies under `nutritional`, which would need either reclassification or a domain-specific scoring aggregate.

**Potential confidence logic:** Must be designed. High confidence if hemoglobin + ferritin + iron + transferrin_saturation; medium if hemoglobin + ferritin; low if only hemoglobin or CBC without iron studies.

**Potential expanded-card content:** KB packages exist but need to be wired into IDL records and governed narrative. `ph_one_carbon_homocysteine_macrocytosis_v1` IDL record already provides excellent `why_it_matters` copy (confirmed UAT) — this content needs to be connected to the domain score output path.

**Risks:** The iron/CBC/nutritional system split in SSOT (`hematological` for CBC, `nutritional` for iron/B12/folate) means there is no single scoring rail that covers the full domain. A new composite rail or scoring aggregate must be designed. Cross-system blending must be deterministic and documented — cannot be improvised in a single sprint. The domain must remain anchored to the iron availability → erythropoiesis → oxygen transport pathway and must not absorb the one-carbon/methylation phenotype wholesale — that belongs partly in cardiovascular (homocysteine) and partly in haematological context.

**Implementation difficulty:** Medium. Requires: (1) design decision on scoring rail architecture, (2) new `_is_wave1_blood_iron()` signal filter, (3) new `_blood_iron_confidence_tier()` function, (4) new IDL records or wiring of existing `ph_one_carbon_homocysteine_macrocytosis_v1` into domain ordering, (5) governed narrative sentences.

**Verdict:** Not ready — medium backend/governed work required.

---

### Domain: Thyroid & Energy Regulation

**Consumer label:** Thyroid & energy regulation
**Clinical handout label:** Thyroid Axis Status
**Internal mapping:** None currently in domain_score_assembler. SSOT system key `thyroid` exists for TSH, free_t4, free_t3, tpo_ab, tgab. Scoring_policy.yaml `hormonal` system has `system_weight: 0.0` and empty biomarker list — the scoring engine does not currently produce a usable `hormonal` system score. The `thyroid` system runs in `system_capacity_scores` but `health_system_scores.hormonal` does not include thyroid biomarkers.

**Relevant current systems/clusters/signals:** `thyroid` system capacity score (exists); signals for `signal_tsh_*` from `pkg_thyroid_tsh_context`, `pkg_s24_tsh_high_hypothyroidism`, `pkg_s24_tsh_low_hyperthyroidism`; investigation specs: `inv_tsh_high_hypothyroidism_v1.yaml`, `inv_tsh_low_hyperthyroidism_v1.yaml`

**Relevant biomarkers (SSOT):** `tsh` (system: thyroid, clinical_weight: 0.8), `free_t4` (system: thyroid, clinical_weight: 0.5), `free_t3` (system: thyroid, clinical_weight: 0.6), `tpo_ab` (system: thyroid, clinical_weight: 0.5), `tgab` (system: thyroid, clinical_weight: 0.4)

**Existing governed assets:** `pkg_thyroid_tsh_context` (signal_library); `pkg_s24_tsh_high_hypothyroidism`; `pkg_s24_tsh_low_hyperthyroidism`; no IDL records for thyroid found in `_IDL_ORDER_*` arrays in domain_score_assembler.py

**Existing frontend-visible content:** TSH appears in the biomarker grid with an `educational_explainer` (confirmed in UAT section 8: "TSH | educational_explainer present"). No domain card. No system-level thyroid narrative surfaces to the consumer.

**Potential score logic:** Must be designed. Requires adding a `thyroid` system entry to `scoring_policy.yaml` with TSH, free_t4 biomarkers and appropriate scoring weights/bands, or reading directly from `system_capacity_scores.thyroid`. The current scoring_policy `hormonal` system is explicitly zeroed out and empty — this is not suitable for thyroid scoring without modification.

**Potential confidence logic:** Must be designed. TSH alone = medium (widely available); TSH + free_t4 = high (standard thyroid assessment); TSH + free_t4 + free_t3 = high; adding tpo_ab = high with autoimmune context.

**Potential expanded-card content:** KB packages provide signal-level content. IDL records need to be authored for `ph_thyroid_axis_tsh_*` phenotype constructs.

**Risks:** Scoring_policy.yaml modification is a HIGH risk change (touches SSOT-adjacent files). The thyroid scoring approach (whether to repurpose `hormonal` system, add a `thyroid` system, or derive from `system_capacity_scores.thyroid` directly) requires architectural design before implementation. TSH direction is bidirectional (high = hypothyroid, low = hyperthyroid) — confidence and score direction handling must be deterministically governed.

**Implementation difficulty:** Medium to high. Requires scoring_policy change (HIGH risk by SOP), IDL phenotype authoring, new assembler block with dual-direction handling.

**Verdict:** Not ready — medium backend/governed work required.

---

### Domain: Kidney Function

**Consumer label:** Kidney function
**Clinical handout label:** Renal Filtration / Renal Strain Status
**Internal mapping:** None in domain_score_assembler. Scoring rail `kidney` exists in scoring_policy.yaml with `creatinine` and `urea` (system_weight: 0.15, min_biomarkers_required: 1). `system_capacity_scores.renal` exists. `egfr` is in SSOT under system `renal` but not in scoring_policy.yaml `kidney` biomarkers.

**Relevant current systems/clusters/signals:** `renal` system capacity score; signals from `pkg_s24_creatinine_high_renal`; investigation specs: `inv_creatinine_high_renal_v1.yaml`, `inv_urea_high_renal.yaml`, `inv_uric_acid_high_metabolic.yaml`

**Relevant biomarkers (SSOT):** `creatinine` (system: renal, clinical_weight: 0.8), `urea` (system: renal, clinical_weight: 0.6), `egfr` (system: renal, clinical_weight: 0.7), `uacr` (system: renal, clinical_weight: 0.75), `urine_protein_creatinine_ratio` (system: renal, 0.75), `cystatin_c` (system: renal, 0.65), `urate` (system: renal, 0.5), `urea_creatinine_ratio` (derived, system: renal)

**Existing governed assets:** `pkg_s24_creatinine_high_renal` (signal_library); investigation specs for creatinine and urea; no comprehensive renal IDL phenotype record confirmed in domain_score_assembler `_IDL_ORDER_*` arrays

**Existing frontend-visible content:** Creatinine card in UAT has `contribution_context` present (cluster membership). No domain card. Renal system appears in `balanced_systems_v1.items` as "Renal — broadly within expected ranges" in "What's working well."

**Potential score logic:** Candidate: use `health_system_scores.kidney.overall_score` augmented by `system_capacity_scores.renal`. However scoring_policy.yaml `kidney` system only covers creatinine and urea — eGFR is the more clinically meaningful marker and must be added to the scoring policy for a trustworthy kidney score.

**Potential confidence logic:** Must be designed. Creatinine + eGFR = medium (standard); + urea = medium-high; + uacr = high (complete renal assessment); creatinine alone = low.

**Potential expanded-card content:** KB signal packages exist but IDL phenotype records need authoring for renal filtration constructs. Mild abnormality handling is critical — a slightly elevated creatinine or mildly reduced eGFR needs carefully worded copy that avoids alarming users unnecessarily.

**Risks:** Mild abnormality handling for kidney is the highest clinical risk in the six domains. A score below 80 for a CKD stage 1–2 pattern could trigger user anxiety without proportionate clinical context. eGFR-based scoring requires age and sex inputs (available from questionnaire). Confidence explanation must reference the absence of albuminuria assessment when UACR is not present.

**Implementation difficulty:** Medium. Requires scoring_policy.yaml extension for eGFR (HIGH risk change), new assembler block, IDL phenotype authoring with careful mild-abnormality language.

**Verdict:** Not ready — medium backend/governed work required.

---

## 6. Second-Wave Domain Assessment

### Silent Inflammation

Repo evidence: `pkg_chronic_inflammation` package (package_manifest.yaml, research_brief.yaml — no signal_library.yaml confirmed in glob results); `pkg_s24_crp_high_inflammation` (signal_library present); `pkg_inflammation_crp_context` (signal_library present); `crp` is in SSOT under system `immune`, scoring_policy `inflammatory` system (weight 0.15, CRP only). IDL records for a systemic inflammation phenotype are not confirmed in the IDL order arrays. The `balanced_systems_v1` surface correctly identifies stable/unstable inflammatory markers but there is no consumer domain card.

**Assessment:** Correctly positioned as second-wave. CRP alone is a weak anchor for a "silent inflammation" domain score — CRP can be elevated transiently and is not specific. Without IL-6, ESR, fibrinogen, or a governed multi-marker inflammatory composite, a "Silent inflammation" score risks either (a) false reassurance when CRP is normal but subclinical inflammation exists, or (b) unnecessary alarm on a transient CRP spike. The repo does not have sufficient governed multi-marker inflammation phenotypes to support a trustworthy consumer score. **Keep second-wave.**

### Hormone Balance

Repo evidence: SSOT has comprehensive hormonal biomarkers: `testosterone`, `free_testosterone`, `shbg`, `oestradiol`, `lh`, `fsh`, `prolactin`, `cortisol`, `acth`, `dhea`, `dhea_s`, `fai` — all under system `hormonal`. Scoring_policy.yaml `hormonal` system has `system_weight: 0.0` and **empty biomarker list**. This is not an accident — it is a deliberate zeroing of the hormonal scoring rail. No governed IDL phenotype records for hormone balance have been confirmed in the domain_score_assembler.

**Assessment:** Correctly positioned as second-wave. The zero-weight scoring policy reflects the architectural reality: hormone interpretation is heavily sex-specific, age-specific, and phase-of-cycle-specific (for females). A single domain score for "Hormone balance" covering male hypogonadism, female PCOS, menopause, adrenal status, and cortisol patterns simultaneously would require multiple distinct governed sub-phenotypes and robust sex/age stratification logic. None of this exists in the current codebase. Premature promotion would produce either dangerously misleading scores or trivially low confidence that renders the card useless. **Keep second-wave.**

---

## 7. Proposed DTO / Contract Shape

The existing `ConsumerDomainScoreV1` TypeScript interface (`frontend/app/types/analysis.ts` lines 328–351) is already well-designed and should be extended to six domains without restructuring. The current shape covers most required fields.

**Recommended `domain_scores_v1[]` contract (annotated against current DTO):**

```typescript
interface DomainScoreV1 {
  // Identity
  domain_id: string;                      // EXISTING: e.g. "wave1_cardiovascular"
  card_schema_version?: string;           // EXISTING: "1.1"
  consumer_label: string;                 // EXISTING: "Cardiovascular health"
  clinical_label: string;                 // EXISTING: "Cardiometabolic / Vascular Risk Status"

  // Score
  score: number;                          // EXISTING: 0–1 (multiply × 100 for display)
  band_label: string;                     // EXISTING: "strong" | "stable" | "watch" | "review"

  // Confidence
  confidence_tier: 'high' | 'medium' | 'low'; // EXISTING
  confidence_sentence: string;            // EXISTING

  // Short explainer (collapsed card)
  headline_sentence: string;              // EXISTING
  contributor_sentence: string;           // EXISTING — "why this score" short form
  evidence_anchor_sentence?: string;      // EXISTING — "Based on: [IDL label]"

  // Expanded card content
  consequence_sentence: string;           // EXISTING — maps to "what this may mean over time"
  next_step_sentence: string;             // EXISTING — maps to "next-step framing"

  // Contributors / evidence
  active_signal_ids: string[];            // EXISTING — which signals fired
  contributing_system_keys: string[];     // EXISTING — e.g. ["cardiovascular"]
  primary_idl_record_id: string | null;   // EXISTING — IDL phenotype driving the narrative
  missing_marker_ids: string[];           // EXISTING — what would improve confidence
  caveat_flags: string[];                 // EXISTING — domain-specific caveats

  // Traceability
  source_track: string;                   // EXISTING — assembly provenance string
  raw_evidence_refs: Record<string, unknown>; // EXISTING — scored/capacity values

  // GAPS — fields with no current source (Wave 2 concerns, not Wave 1 blockers):
  // short_explainer — currently split across headline + contributor; could consolidate to one sentence
  // what_this_score_means — no single field; candidate: new "meaning" sentence per band
  // top_contributors[] — partially available via wave1_aligned_drivers_meta.by_domain[] in meta
  //   but not part of the domain card DTO itself; authoring needed for Wave 2 domains
}
```

**Fields sourced from existing DTO:** All fields marked EXISTING above. No structural DTO changes required for Wave 1 launch.

**Fields with no current source (Wave 2 gaps):**
- `top_contributors[]` as a named biomarker list with direction (high/low) — partially available via `wave1_aligned_drivers_meta.by_domain[]` in `meta` but not part of the domain card DTO itself
- `what_this_score_means` — currently implied by the band label but not an explicit sentence per band in the DTO

These gaps are Wave 2 assembly concerns. No structural changes needed for Wave 1 launch.

---

## 8. Frontend Surfacing Recommendation

**Current position:** `Wave1DomainCards` is rendered inside a `ResultsDisclosureSection` (a collapsible toggle, `defaultOpen={false}`) titled "Health domains", after "What to do next" and before "Clinician summary." It is the last substantive section in the consumer journey before the clinician-facing content. As confirmed by both the UAT audit and the results page code (`results/page.tsx` lines 807–813), the best consumer-facing sentence in the DTO is invisible by default.

**Recommended option: immediately after the primary finding card and before the body overview.**

Place three domain cards as the second section visible to the user after the primary finding hero. The domain score grid answers "where do I look strong, where am I under strain, how confident is the platform in that judgement?" This is a first-screen need, not a supplementary need. The UAT audit explicitly identifies surfacing the cardiovascular headline sentence as the single highest commercial "wow" change. Placing three domain cards early gives the user an immediate map of their health before the detailed journey begins. The detailed journey then functions as supporting evidence for what the domain cards already stated.

**Alternative acceptable option:** As a first-screen dashboard section before the detailed journey ("Your health at a glance"), replacing or merging with the current "What's working well" section. This would require frontend restructuring but produces a stronger first impression.

**Do not:** Place domain scores only in the supplementary/collapsible section. Do not render them after the detailed biomarker evidence — users will not reach them. Do not implement placement here; this section is recommendation only.

---

## 9. Implementation Sequence

### DOMAIN-R2A — Domain Score DTO / Contract Hardening
**Scope:** Confirm the Wave 1 DTO contract is clean for production. Review and fix: ApoA1 scoring inconsistency (UAT finding — value above range but scored optimal); verify `evidence_anchor_sentence` is populated correctly for all three Wave 1 cards; confirm `wave1_aligned_drivers_meta` is correctly assembled and passed through `meta`; add integration test coverage for all three domain card fields.
**Risk:** STANDARD (DTO validation, no engine logic change)
**Files:** `backend/core/analytics/domain_score_assembler.py`, `backend/core/analytics/domain_narrative_wave1.py`, test suite

### DOMAIN-R2B — Wave 1 Frontend Surface (Cardiovascular, Blood Sugar, Liver)
**Scope:** Move `Wave1DomainCards` from hidden `ResultsDisclosureSection` into the main results journey, positioned immediately after the primary finding card. Update `defaultOpen` state. Ensure the three-card grid renders at appropriate breakpoints. Update section labels and descriptions. No backend changes — pure frontend layout/positioning.
**Risk:** LOW (frontend layout only, no analytical changes)
**Files:** `frontend/app/(app)/results/page.tsx`, `frontend/app/components/results/Wave1DomainCards.tsx`

### DOMAIN-R2C — Wave 2 Domain Backend Assembly (Blood Iron & Oxygen, Thyroid & Energy, Kidney Function)
**Scope:** Build three new assembler blocks in `domain_score_assembler.py`. Each requires: (a) scoring rail identification or scoring_policy.yaml extension, (b) signal filter predicate (`_is_wave1_*` pattern), (c) confidence tier function, (d) IDL record selection order, (e) governed narrative sentence assembly (headline/contributor/consequence/confidence/next_step). For thyroid and kidney this requires scoring_policy.yaml changes — HIGH risk, must go through full Automation Bus governance with GPT architectural review.
**Risk:** HIGH (touches scoring_policy.yaml, IDL records, analytical assembler logic)
**Files:** `backend/ssot/scoring_policy.yaml`, `backend/core/analytics/domain_score_assembler.py`, `backend/core/analytics/domain_narrative_wave1.py`, IDL registry, knowledge_bus packages

### DOMAIN-R3 — Frontend Six-Domain Surface
**Scope:** Extend `Wave1DomainCards` to render six domain cards. Update `WAVE1_ORDER` array (`Wave1DomainCards.tsx` line 10–14) to add the three new `domain_id` values. Confirm TypeScript types are unchanged (they are — `ConsumerDomainScoreV1` is already generic). Add responsive grid handling for six cards. Update section heading.
**Risk:** LOW (frontend layout extension)
**Files:** `frontend/app/components/results/Wave1DomainCards.tsx`, `frontend/app/(app)/results/page.tsx`

### DOMAIN-R4 — Human UAT and Narrative Polish
**Scope:** End-to-end UAT across all six domains using real panel data with varied marker coverage (minimal panels, full panels, panels with abnormals). Verify confidence tiers fire correctly. Verify score bands are proportionate. Verify "on this panel" template language has been eliminated from domain card copy. Verify clinical label / consumer label separation is clean (no clinical label in consumer cards). Verify no domain score appears without deterministic support. Review narrative sentences for polish.
**Risk:** LOW (no code changes unless defects found)

---

## 10. Risks and STOP Conditions

**Fake scoring.** A domain score must not appear unless a real deterministic score exists. For Wave 2 domains, the STOP condition is: do not emit a domain card if the scoring rail has no relevant biomarkers on the panel. The existing `_liver_confidence_tier_domain()` returns `"low"` and requires alt to be present — this pattern must be replicated exactly for all three Wave 2 domains. If no relevant biomarkers exist, the card must either not be emitted or must show "Insufficient data" as a distinct non-score state. Do not show `score: 0.0` as if it is a scored result.

**Unsupported domain labels.** Consumer labels are not permitted to appear in the clinician report. The architecture document is explicit: the three-layer separation is non-negotiable. Implementation must verify that the `consumer_label` field in the DTO never surfaces inside `clinician_report_v1`. Current implementation correctly separates these (verified in `Wave1DomainCards.tsx` — it only renders consumer_label and clinical_label in their correct positions).

**Consumer labels leaking into clinician outputs.** The `clinical_label` field exists in `ConsumerDomainScoreV1` precisely so the clinician-facing surface can use it. Current `ClinicianReportRenderer` does not render domain cards — this is the correct separation. If clinician report PDF generation is extended in future, this boundary must be enforced in code, not just convention.

**Duplicated scoring logic.** The `_cardiovascular_confidence_tier()` logic in `domain_score_assembler.py` independently recomputes panel coverage. This must not diverge from the scoring_policy.yaml system definition. Any change to which biomarkers belong to a system in scoring_policy.yaml must propagate to the domain score assembler. A mechanical coupling or cross-check should be implemented in DOMAIN-R2C.

**Over-broad domains.** "Blood, iron & oxygen" risks becoming a kitchen sink for CBC + iron studies + B12/folate + homocysteine. The domain must remain anchored to the iron availability → erythropoiesis → oxygen transport pathway and must not absorb the one-carbon/methylation phenotype wholesale — that belongs partly in cardiovascular (homocysteine) and partly in haematological context.

**Confidence not grounded.** Confidence tiers must be driven by biomarker panel coverage, not inferred from score band. A score of 70/100 on a two-biomarker panel is not the same clinical statement as a score of 70/100 on an eight-biomarker panel. The existing `_cardiovascular_confidence_tier()` function correctly models this. Wave 2 tiers must be held to the same standard.

**Frontend inventing interpretation.** The `Wave1DomainCards.tsx` component renders only what the DTO provides — it does not generate any text. This is correct and must be maintained. Any narrative sentence that reaches the frontend must have been deterministically assembled in the backend. No `if (score < 50) { return "This area needs attention" }` logic in frontend components.

**Lead narrative truncation bug.** Confirmed in UAT: `narrative_report_v1.lead_narrative` is truncated mid-sentence. If the truncation affects domain card `consequence_sentence` assembly (unlikely — domain sentences are assembled independently in `domain_score_assembler.py` not via `narrative_report_compiler`) the risk is low. But the truncation bug should be investigated and resolved before any content sprint.

**Kidney mild-abnormality handling.** A score below 80 for a CKD stage 1–2 pattern could trigger user anxiety without proportionate clinical context. eGFR-based scoring requires age and sex inputs (available from questionnaire). STOP condition: kidney card must not be emitted with score < 70 without a governed consequence sentence that has been clinically reviewed. Alarm-free framing is mandatory for this domain.

---

## 11. Final Recommendation

**The next implementation sprint should be DOMAIN-R2B.**

The Wave 1 infrastructure is complete. Three domain cards (Cardiovascular health, Blood sugar control, Liver health) are already assembled, typed, and rendered in the frontend component `Wave1DomainCards.tsx`. The only thing standing between these cards and user value is a `defaultOpen={false}` and their position at the bottom of the results journey inside a `ResultsDisclosureSection`.

The sprint is LOW risk (frontend layout only, no analytical changes), can be executed by Cursor without GPT architectural review, and will immediately surface the highest-value consumer content in the DTO. The UAT audit confirmed the cardiovascular card's `headline_sentence` is the best consumer-facing sentence in the entire DTO — it is currently invisible to 100% of users.

**Specific implementation target for DOMAIN-R2B:**
- `frontend/app/(app)/results/page.tsx` — extract `<Wave1DomainCards>` from its `ResultsDisclosureSection` wrapper and place it in the main journey, after the primary finding card section and before the body overview
- `frontend/app/components/results/Wave1DomainCards.tsx` — confirm section heading reads naturally in its new position; no functional changes needed
- No backend changes; no DTO changes; no analytical changes
- Acceptance criteria: three domain cards visible without any user interaction on page load; cards render correctly on mobile and desktop; `confidence_sentence`, `consequence_sentence`, `next_step_sentence`, `missing_marker_ids` all display correctly in expanded state; no `clinical_label` visible in consumer view

**After DOMAIN-R2B:** Run DOMAIN-R2A (DTO contract verification + ApoA1 scoring fix) either concurrently or immediately after, before beginning DOMAIN-R2C which requires HIGH-risk scoring_policy changes and full Automation Bus governance.
