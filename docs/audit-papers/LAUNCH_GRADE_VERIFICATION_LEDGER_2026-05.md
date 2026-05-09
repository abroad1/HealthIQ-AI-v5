# Launch-Grade Verification Ledger — HealthIQ AI

**Date:** 2026-05-04
**Purpose:** Verify, with real runtime evidence, what the current analysis engine actually delivers on representative panels — and whether questionnaire responses meaningfully influence the result.
**Mode of evidence:** Live orchestrator runs (`AnalysisOrchestrator.run`), DTO compilation via `build_analysis_result_dto`, both in `deterministic_mock` runtime (no LLM). 12 panel × profile combinations. All artifacts retained under `docs/audit-papers/verification-2026-05-04/artifacts/`.
**Scope sources:**
- `LAUNCH_GRADE_ANALYTICAL_TARGET_STATE_2026-05.md`
- `LAUNCH_GRADE_ANALYTICAL_GAP_MAP_2026-05.md`
- Repository code at HEAD, AGENTS.md governance.
**Runtime artifacts:**
- `docs/audit-papers/verification-2026-05-04/ledger_runs.json` (raw per-run summary)
- `docs/audit-papers/verification-2026-05-04/ledger_extract.json` (structured deep extract)
- `docs/audit-papers/verification-2026-05-04/ledger_diff.json` (per-panel cross-profile diff)
- `docs/audit-papers/verification-2026-05-04/clinician_report_summary.json` (clinician-report-V1 deep extract per run)
- `docs/audit-papers/verification-2026-05-04/artifacts/<panel>__<profile>/` (full DTO, narrative, insight graph, replay manifest, arbitration report per run)
- `docs/audit-papers/verification-2026-05-04/profile_*.json` (lifestyle profiles used)

---

## 1. Executive summary

The engine is **noticeably stronger** than the static gap map credited it for in three areas:

1. **Governed WHY for the lead finding is real and structurally rich** on both AB and VR. The lead signal (`signal_homocysteine_elevation_context` in both panels) carries 4 governed hypotheses with `evidence_for`, `evidence_against`, `missing_data`, `confirmatory_tests`, and `hypothesis_confidence` per hypothesis. No fallback string ("No hypothesis set available …") was emitted in any of the 12 runs.
2. **Runner-up surfacing works correctly when ambiguity is present.** AB has a clearly distinct lead → `primary_concern_mode = "distinct_lead"`, `runner_up_*` fields empty (correct). VR has a near-tie → `primary_concern_mode = "near_tie_ambiguity"`, `runner_up_signal_id = "signal_homocysteine_high"`, with a transparent `runner_up_why_not_lead_line` explaining the tie ("similarly strong on this panel (0.90 vs 0.90); the headline shows one pattern first…"). This is high-quality behaviour.
3. **The Interpretation Display Layer (IDL) bundle is live and populated.** AB returns 11 records with 4 enabled for frontend (e.g. "Vascular Inflammation Risk", "Methylation pathway pattern", "LDL in context"); VR returns enabled records too. Each record has `severity_state`, `frontend_allowed_term`, `supporting_biomarkers_summary`, `display_order_priority`, and a real `why_it_matters`.

The engine is **substantially weaker** than the strategic papers and gap map imply in two areas, both of which the user actually sees:

1. **The questionnaire is, in user-visible terms, effectively ignored.** The lifestyle modifier engine computes the right modifiers (BMI, BP, smoking, waist-to-height, alcohol all fire correctly), and the lifestyle interpretation bridge for alcohol/methylation does activate when relevant. But the user-visible output — `consumer_domain_scores.score`, `consumer_domain_scores.band_label`, `consumer_domain_scores.headline_sentence`, `consumer_domain_scores.consequence_sentence`, `consumer_domain_scores.next_step_sentence`, `narrative_report_v1.retail_summary`, `narrative_report_v1.next_steps_narrative`, and the `clinician_report_v1.sections.page1` — is **identical across all four profiles** for the same panel (P0 no_lifestyle, P1 healthy, P2 minimal, P3 stressed with BMI 32, BP 158/96, smoker, 35 alcohol units/wk, 5h sleep). The ranked top findings list is identical. The intervention list is identical. Overall score is identical to seven decimal places. The only places lifestyle changes anything visible are: a 1-line technical bridge sentence inserted into `lead_narrative` when the alcohol bridge fires (`+124 chars`, raw rationale code language), and 1–2 point shifts in capacity numbers buried inside `body_overview` and `clinician_synthesis` ("hepatic (99) … metabolic (98)" vs all-100s baseline). That is the entire payoff.
2. **The legacy `insights[]` array on the AnalysisDTO is generic placeholder content.** All 12 runs emitted the same 6 entries — "Metabolic focus: summarise structured signals; review with your clinician", "Cardiovascular focus: …", etc. — each with `confidence: 0.72`, `manifest_id: legacy_v1`, empty `biomarkers`, empty `drivers`, empty `evidence`, identical recommendation string. If the frontend ever surfaces `analysis_result.insights`, the user is shown empty per-domain placeholders that look like an output but contain nothing.

The runtime is honest about being deterministic_mock (`narrative_runtime.runtime_mode = "deterministic_mock"`, `policy_reason = "orchestrator_explicit_false"`) — but that flag is buried inside `meta` and the surface narrative still uses possessive language ("your measured homocysteine", "your cardiovascular read on this panel") that a user could reasonably read as personalised AI output.

**Bottom line for leadership:**
The analytical engine is meaningfully more capable than the gap map credited it for. The launch problem is not engine depth on the lead finding, and not runner-up handling. The launch problem is that the questionnaire produces almost no user-visible payoff, and that an alternative legacy "insights" surface still emits empty-shell placeholders. Neither is acceptable in a paid launch product.

---

## 2. Panels and profiles tested

### Panels
| Key | Source path | Notes |
|---|---|---|
| `AB_full_panel_with_ranges` | `backend/tests/fixtures/panels/ab_full_panel_with_ranges.json` | UK-style commercial panel; 82 normalised biomarkers; user: male, age 58. Multi-system pattern: high homocysteine, elevated LDL/total cholesterol, MCV high, low transferrin. |
| `VR_full_panel_with_ranges` | `backend/tests/fixtures/panels/vr_full_panel_with_ranges.json` | UK-style commercial panel; 82 normalised biomarkers; user: female, age 58. Different signal mix: HCY elevation, vitamin D low, ALP low, hypercortisolism, no LDL elevation. |
| `AB_full_panel_with_profiles` | `backend/tests/fixtures/panels/ab_full_panel_with_profiles.json` | Sister-fixture with biomarker reference profile metadata. Used as a sanity contrast against `_with_ranges`. |

No additional clearly distinct UK commercial panels with the required ranged-biomarker schema exist in the repo at this time. `green_metabolic.json`, `amber_hepatic.json`, `red_metabolic.json`, `canonical_small.json` are smaller list-shaped fixtures that don't match the orchestrator's panel schema and were not used.

### Lifestyle / questionnaire profiles
All four profiles were applied to each panel (12 runs total). The profiles are real lifestyle inputs at the schema understood by `LifestyleModifierEngine` and `lifestyle_interpretation_bridges_v1`. The repo's questionnaire submission contract was not exercised through the full `QuestionnaireMapper.map_submission` path because `run_golden_panel` calls `orchestrator.run` with `questionnaire_data=payload.get("questionnaire_data")` (none of the panels carry that key) and `lifestyle_inputs=lifestyle_payload`. The lifestyle path is the same path that questionnaire submissions ultimately drive (the questionnaire is mapped into the lifestyle inputs vector before the lifestyle engine runs), so this is a faithful test of the questionnaire payoff downstream of the QuestionnaireMapper.

| Key | Source | Description | Realised modifier set on run |
|---|---|---|---|
| `P0_no_lifestyle` | n/a | No lifestyle inputs at all. | `lifestyle` key absent on DTO; `lifestyle_interpretation_bridges_v1` present but inactive. |
| `P1_healthy` | `docs/audit-papers/verification-2026-05-04/profile_healthy.json` | BMI 22.2; BP 112/70; HR 58; never smoker; 0 alcohol units/wk; 8h sleep; sit-stand 22 reps. | `lifestyle.system_modifiers` all fire **zero** capped modifiers. No bridges active. |
| `P2_minimal_existing_fixture` | `backend/tests/fixtures/lifestyle_minimal.json` | BMI ~27.8; BP 145/88; HR 72; never smoker; 7 alcohol units/wk; 6.5h sleep; no sit-stand. | `cardiovascular = +0.13`, `metabolic = +0.08` capped modifiers. No bridges active. |
| `P3_stressed` | `docs/audit-papers/verification-2026-05-04/profile_stressed.json` | BMI 32.4; waist-to-height 0.61; BP 158/96; HR 88; **current smoker**; **35 alcohol units/wk**; 5h sleep; sit-stand 7 reps. | `cardiovascular = +0.20` (cap), `metabolic = +0.20` (cap), `hepatic = +0.10` (cap), `immune = +0.06`, `musculoskeletal = +0.05`. **`alcohol_methylation_macrocytosis` bridge active** with `coherence: {homocysteine_band: high, mcv_band: high}`. |

**Caveat:** the runs are in `deterministic_mock` mode (no LLM), which is consistent with the documented production runtime posture (Layer C narrative defaults to mock unless `HEALTHIQ_NARRATIVE_LLM=1` and `HEALTHIQ_ENABLE_LLM=1` are both set). Findings about questionnaire influence on *engine reasoning* (signals, ranking, scores, top_findings, root_cause hypotheses) are therefore conclusive, because none of those paths are LLM-gated. Findings about questionnaire influence on *narrative wording* are conclusive within the mock runtime; they show what a user actually sees today on the production-default runtime.

---

## 3. Verification ledger

### 3.1 Lead finding, runner-up, WHY depth (per panel — questionnaire-invariant)

These rows are identical across all four profiles for a given panel — see §4 for why.

| Field | AB panel | VR panel |
|---|---|---|
| Primary concern (clinician_report.page1) | "Homocysteine Elevation Context: warrants attention on this panel" | "Homocysteine Elevation Context: is outside the optimal range on this panel" |
| `primary_concern_mode` | **`distinct_lead`** | **`near_tie_ambiguity`** |
| Lead signal id | `signal_homocysteine_elevation_context` | `signal_homocysteine_elevation_context` |
| Lead signal state | `at_risk` (escalation) | `suboptimal` |
| Lead signal confidence | 0.95 | 0.90 |
| `confidence_reasons` | `ALL_SUPPORTING_MARKERS_PRESENT, ESCALATION_SINGLE_CONDITION, REFERENCE_RANGE_COMPLETE, PRIMARY_METRIC_PRESENT` | `ALL_SUPPORTING_MARKERS_PRESENT, REFERENCE_RANGE_COMPLETE, PRIMARY_METRIC_PRESENT` |
| Supporting markers (ranking layer) | `vitamin_b12, folate, transferrin, mcv, crp` | `vitamin_b12, folate, transferrin, mcv, crp` |
| Primary metric | `homocysteine` | `homocysteine` |
| Plausibility verdict | Plausible — marker pattern is consistent with lead. | Plausible — same pattern, milder. |
| **Governed WHY for lead** | **YES** — 4 hypotheses (B12-associated, Folate-associated, Inflammatory context, Renal clearance context). 3 evidence_for items, 2 evidence_against items, 1 missing_data item, 4 confirmatory_tests across hypotheses. | **YES** — 4 hypotheses (same set). 1 evidence_for, 2 evidence_against, 1 missing_data. Slightly thinner because supporting biomarkers are nearer normal. |
| Fallback string ("No hypothesis set available …") | None | None |
| Runner-up surfaced | **No** (correctly empty: `runner_up_signal_id=""`) | **Yes** — `signal_homocysteine_high`. `runner_up_why_not_lead_line` = "Homocysteine Elevation Context and Homocysteine High are similarly strong on this panel (0.90 vs 0.90); the headline shows one pattern first so the discussion has a single starting point." |
| `co_primary_signal_ids` | `[]` | `["signal_alp_low", "signal_homocysteine_elevation_context", "signal_homocysteine_high"]` |
| `top_hypothesis_line` (page1) | "Top hypothesis: B12-associated pattern (confidence 0.60)." | "Top hypothesis: B12-associated pattern (confidence 0.60)." |
| `confidence_and_missing_data` (page1) | "Overall confidence for this lead pattern: 0.95. Some expected confirmatory markers are not on this panel, which limits how specific the story can be." | "Overall confidence for this lead pattern: 0.90. Some expected confirmatory markers are not on this panel, which limits how specific the story can be." |
| Chain narrative (page1) | "Linked pattern (chain_001): Homocysteine High → Homocysteine Elevation Context."; "Linked pattern (chain_002): Systemic Inflammation → Homocysteine Elevation Context." | Same chains. |
| Top findings count | 13 | 12 |
| Findings with governed root_cause_v1 entries | 7 of 13 | 6 of 12 |
| Top findings WITHOUT governed WHY (silent omission) | rank 2 `signal_homocysteine_high`, rank 3 `signal_mcv_high`, rank 5 `signal_apoa1_cardio_risk`, rank 7 `signal_ldl_high`, rank 13 `signal_renal_metabolic_stress` (optimal so OK) | rank 4 `signal_hypercortisolism`, rank 6 `signal_cortisol_high`, rank 7 `signal_creatine_kinase_high`, rank 12 `signal_renal_metabolic_stress` (optimal so OK) |
| `interpretation_display_layer_v1` records / enabled | 11 / 4 enabled for frontend | enabled count: 2 |
| Lead-corresponding IDL record | `ph_vascular_hcy_inflammation_v1` (severity `strong_signal`, frontend term `clinical_only`) and `ph_one_carbon_homocysteine_macrocytosis_v1` (`strong_signal`, `phenotype_allowed`) | Smaller IDL set; lead pattern covered by methylation phenotype record. |
| `actions.interventions` count | **5** (`intv_vascular_clinician_referral_v1`, `intv_hepatic_clinician_referral_v1`, `intv_vascular_pattern_lifestyle_v1`, `intv_lipid_transport_lifestyle_v1`, `intv_hepatic_burden_lifestyle_v1`) | non-zero, panel-appropriate set |
| `actions.clinician_referrals` count | 2 | non-zero |
| `narrative_runtime.runtime_mode` | `deterministic_mock` | `deterministic_mock` |
| `meta.system_confidence` (sample) | `liver: 75, metabolic: 72` (because `ast`, `glucose`, `insulin` missing) | `liver: 75, metabolic: 72` (same missing markers) |
| `meta.missing_markers` | `liver: [ast]; metabolic: [glucose, insulin]` — surfaced in DTO | same |
| `meta.confidence_downgrades` | populated | populated |

### 3.2 Runtime cross-section coherence (per panel — questionnaire-invariant)

| Surface | AB | VR |
|---|---|---|
| Top finding rank 1 (`top_findings[0]`) | `signal_homocysteine_elevation_context` (vascular, at_risk, conf 0.95) | `signal_homocysteine_elevation_context` (vascular, suboptimal, conf 0.90) |
| `clinician_report_v1.sections.page1.primary_concern` | "Homocysteine Elevation Context: warrants attention on this panel" | "Homocysteine Elevation Context: is outside the optimal range on this panel" |
| `narrative_report_v1.retail_summary` | Headlines "Methylation pathway pattern (strong signal): Homocysteine elevation with larger red-cell index suggesting one-carbon / marrow context" + "LDL in context (protective transport features)" | (different content — methylation-led, no LDL line for VR) |
| `interpretation_display_layer_v1` — first enabled record | `ph_vascular_hcy_inflammation_v1` ("Vascular Inflammation Risk", `strong_signal`) | (analogous methylation record) |
| `consumer_domain_scores` cardiovascular `headline_sentence` | "Your cardiovascular read on this panel is not a simple all-clear: the leading pattern here still deserves clinical context alongside your numbers." (band `stable`, score 0.68, `confidence_tier: high`) | (analogous) |
| `clinician_report_v1.sections.page1.key_findings[0]` | "Homocysteine Elevation Context warrants attention on this panel. …" | "Homocysteine Elevation Context is outside the optimal range on this panel. …" |
| Coherence verdict | **Mostly coherent**. Lead, retail summary, primary IDL record, and clinician page1 all agree on "homocysteine / methylation / vascular". One internal tension: cardiovascular consumer card `band_label = "stable"` and `confidence_tier = "high"`, while its `headline_sentence` says "not a simple all-clear" — these can read as competing signals to a user. | **Mostly coherent** under near-tie disclosure: the page1 explicitly tells the user "Several findings have similar strength on this panel; the headline highlights one first…". Same band/headline tension exists for the cardiovascular card. |

### 3.3 Questionnaire effect — what changed when going from P0 → P3 stressed for the same panel

This is the heart of the verification. Captured by direct file diff between paired runs.

| Surface | AB: P0 vs P3 | VR: P0 vs P3 |
|---|---|---|
| `overall_score` | identical (0.81207558…) | identical (0.94013232…) |
| `primary_driver_system_id` | identical (`cardiovascular_4_biomarkers`) | identical |
| `top_findings` ordering & ids | **identical rank-by-rank** (verified for all 13 ranks) | identical rank-by-rank (12 ranks) |
| `top_findings[*].confidence` & `confidence_reasons` | identical | identical |
| `meta.insight_graph.report_v1.root_cause_v1.findings` | identical | identical |
| `clinician_report_v1.sections.page1.primary_concern` | identical | identical |
| `clinician_report_v1.sections.page1.primary_concern_mode` | identical (`distinct_lead`) | identical (`near_tie_ambiguity`) |
| `clinician_report_v1.sections.page1.runner_up_*` | identical (empty) | identical (`signal_homocysteine_high` + same why-not-lead text) |
| `clinician_report_v1.sections.page1.confidence_and_missing_data` | identical | identical |
| `interpretation_display_layer_v1.records` enabled count and ids | identical | identical |
| `consumer_domain_scores[*].score` | identical | identical |
| `consumer_domain_scores[*].band_label` | identical | identical |
| `consumer_domain_scores[*].headline_sentence` | identical | identical |
| `consumer_domain_scores[*].consequence_sentence` | identical | identical |
| `consumer_domain_scores[*].next_step_sentence` | identical | identical |
| `consumer_domain_scores[*].confidence_sentence` & `confidence_tier` | identical | identical |
| `consumer_domain_scores[*].raw_evidence_refs.burden_capacity_*` | **changes** (e.g. cardiovascular 73 → 88, metabolic 100 → 98, hepatic 100 → 99). Internal numbers only; not user-visible. | analogous internal-only changes |
| `actions.interventions` & `actions.clinician_referrals` | identical (5 + 2 ids, identical bodies) | identical |
| `narrative_report_v1.retail_summary` | **identical** | identical |
| `narrative_report_v1.next_steps_narrative` | identical | identical |
| `narrative_report_v1.lead_narrative` | **+124 chars only** when the alcohol bridge fires (P3 only). Inserted line: "Lifestyle bridge - one-carbon / alcohol context: active (alcohol_intake_moderate_or_higher_with_one_carbon_lab_coherence)." Raw rationale-code language, not user-friendly. | same +124 chars |
| `narrative_report_v1.body_overview` | small numeric drift inside the "high-capacity systems" sentence (e.g. `hepatic (100)` → `hepatic (99)`) | same kind of small drift |
| `narrative_report_v1.clinician_synthesis` | small analogous numeric drift | same |
| `meta.system_confidence` | identical | identical |
| `meta.confidence_downgrades` | identical | identical |
| `meta.lifestyle_interpretation_bridges_v1.alcohol_methylation_macrocytosis.active` | **changes** — `false` (P0) → `true` with rationale code (P3, 35 units/wk). Visible inside meta but only the one technical bridge sentence reaches `lead_narrative`. | same change |
| `lifestyle.system_modifiers` (when profile present) | populated, correct (cap-respecting) | populated, correct |
| `lifestyle.derived_inputs.bmi`, `waist_to_height_ratio` | computed correctly (P3: BMI 32.4, WHR 0.61) | same |
| `lifestyle.confidence_adjustments` (per system) | **all 0.0** in every profile | all 0.0 |

### 3.4 Healthy vs no-lifestyle (P0 vs P1) — same panel

The "did the lifestyle layer kick in at all" sanity check.

| Surface | AB / VR P0 vs P1_healthy |
|---|---|
| Differences in user-visible scores, bands, headlines, retail summary, next steps, runner-up | None |
| Differences in clinician_synthesis / body_overview | Minor — additional sentence listing systems with capacity ≥90 (otherwise identical) |
| `lifestyle.system_modifiers.*.capped_total_modifier` | All zero — healthy profile correctly produces no modifiers |
| Net effect of "having answered the questionnaire honestly with healthy values" vs "not answering at all" | **None visible to the user** |

### 3.5 Mock-mode honesty

| Probe | Verdict |
|---|---|
| `meta.narrative_runtime.runtime_mode` set to `deterministic_mock` | YES, on every run. |
| `policy_reason` field set | YES — `orchestrator_explicit_false` (matches double-opt-in posture). |
| `client_kind: mock` | YES. |
| Master switch flag exposed (`master_switch_HEALTHIQ_NARRATIVE_LLM`) | YES, and it is `false`. |
| Is the flag visible to a user reading the surface narrative? | **No** — it's nested inside `meta.narrative_runtime`. The retail summary, page1 headlines, and `narrative_report_v1.lead_narrative` use phrases such as "your measured homocysteine is the main lab anchor", "your cardiovascular read on this panel", and "Functional read — one-carbon pathway and homocysteine patterning" without any visible "deterministic / template-generated" framing. |
| Is the output content actually template-generated? | YES. Wording is deterministic, panel-bound, and not LLM-personalised. |
| Could a paying user reasonably believe AI personalisation was happening? | YES. The wording invites that read; the fact that the questionnaire visibly does almost nothing makes the impression worse on second look. |

---

## 4. Questionnaire influence analysis

This section answers the central question explicitly.

### 4.1 What the engine *does* with questionnaire / lifestyle inputs (verified)

The lifestyle path is wired and behaves as the registry says it should:

- `LifestyleModifierEngine.apply` runs and produces:
  - `lifestyle.derived_inputs` — BMI, waist-to-height computed correctly.
  - `lifestyle.system_modifiers.*.contributions` — per-input modifiers (smoking_status, systolic_bp, diastolic_bp, resting_heart_rate, waist_to_height_ratio etc.) with `capped_modifier` per cap rule and `total_modifier` capped to system cap. For the stressed profile this returns +0.20 (cap) on cardiovascular and metabolic, +0.10 (cap) on hepatic, +0.06 immune, +0.05 musculoskeletal — clinically appropriate magnitudes.
  - `lifestyle.confidence_adjustments` is populated but is **0.0 for every system in every profile** in our runs (confidence-rule path appears either gated, dormant, or only triggered by missing core inputs that the profiles supplied).
  - `lifestyle.adjusted_system_burdens` numerical vector is computed.
- `meta.lifestyle_interpretation_bridges_v1` (`bridge_asset_version: 1.0.0`) runs three bridge probes (alcohol↔one-carbon/macrocytosis; fasting↔glycaemic; hydration/activity↔renal) and **correctly activates** `alcohol_methylation_macrocytosis` only when alcohol_units_per_week is elevated *and* homocysteine + MCV bands are coherent. P0/P1/P2 do not activate it; P3 does.
- The lifestyle layer changes internal `burden_capacity_*` numbers shown in `consumer_domain_scores[*].raw_evidence_refs.burden_capacity_*` (cardiovascular 73 → 88, metabolic 100 → 98, hepatic 100 → 99 between P0 and P3 on AB). These numbers **are not surfaced** in the user-facing fields of the same card.

### 4.2 What the questionnaire *does not* affect (verified)

For the same panel, varying the lifestyle profile from healthy → mid-range → severely unhealthy with active alcohol bridge **does not change**:

- Active signals or signal activation states (signals are deterministic from biomarker values; this is by design and is correct).
- Top findings ordering or any `top_findings[*]` field.
- `overall_score` (identical to seven decimal places).
- `primary_driver_system_id`.
- The clinician report page1: `primary_concern`, `primary_concern_mode`, `co_primary_signal_ids`, `key_findings`, `chains`, `top_hypothesis_line`, `confidence_and_missing_data`, `runner_up_signal_id`, `runner_up_topic_line`, `runner_up_why_not_lead_line`.
- The `interpretation_display_layer_v1` record set or enabled count.
- Every retail-facing line of `consumer_domain_scores[*]` — `band_label`, `score`, `headline_sentence`, `consequence_sentence`, `next_step_sentence`, `confidence_sentence`, `confidence_tier`, `consumer_label`, `clinical_label`.
- `narrative_report_v1.retail_summary`.
- `narrative_report_v1.next_steps_narrative`.
- `actions.interventions` (5 ids on AB are identical in body and ordering across profiles).
- `actions.clinician_referrals`.
- `meta.system_confidence` (the per-system 0–100 confidence vector that drives missing-data framing).

### 4.3 Where the questionnaire *does* show through (verified)

- `narrative_report_v1.lead_narrative` gains exactly **one technical sentence** when the alcohol bridge activates: "Lifestyle bridge - one-carbon / alcohol context: active (alcohol_intake_moderate_or_higher_with_one_carbon_lab_coherence)." This sentence uses the internal rationale code verbatim and is not user-friendly.
- `narrative_report_v1.body_overview` and `clinician_synthesis` show small numeric drift in the "high-capacity / comparatively calmer systems in this snapshot (governed capacity score ≥ 90): autonomic (100), hematological (100), hepatic (99), …" sentence (1–2 point drops for stressed). A non-clinical user is unlikely to register this as personalisation.
- The `meta.lifestyle_interpretation_bridges_v1` block contains the active bridges and rationale codes, but `meta` is not user-facing in the current contract.
- Internal `burden_capacity_*` numbers in `raw_evidence_refs` change. These are explicitly internal references, not part of the displayed sentence.

### 4.4 Verdict

The questionnaire is **wired into the engine but effectively absent from the user-facing output**. It does not affect reasoning at the signal level, it does not reorder findings, it does not change the lead, it does not change the runner-up disclosure, it does not change the recommendations, it does not change the band on any consumer card, and it does not change any of the core narrative surfaces a user reads (retail summary, next steps, page1, IDL records). The most generous reading is "presentation-level, technical and partial". An honest reading is "the user would not detect any payoff from filling in the questionnaire". For a paid product that asks users for blood pressure, BMI, smoking status, alcohol units, and sleep hours, this is a serious gap between promise and delivery.

---

## 5. Launch-grade standard assessment (runtime-verified)

Mapped to `LAUNCH_GRADE_ANALYTICAL_TARGET_STATE_2026-05.md`.

| Target standard | Status (runtime-verified) | Evidence |
|---|---|---|
| **Lead finding plausible, anchored, with primary metric and supporting markers** | **MET** | AB: HCY-elevation context, anchored to homocysteine, 5 supporting markers, all_supporting_markers_present + reference_range_complete + escalation flag. VR: same signal, milder state. |
| **Lead finding has governed WHY with structured evidence_for / evidence_against / missing_data / confirmatory_tests** | **MET** | Both panels: 4 governed hypotheses; structured evidence; no fallback string. |
| **No silent fallback ("No hypothesis set available …") on the lead** | **MET** | Zero fallback strings emitted across 12 runs. |
| **Runner-up surfaced when ranking is ambiguous, with `why_not_lead` rationale** | **MET (clinician_report_v1)** | VR: `near_tie_ambiguity` mode populates `runner_up_signal_id`, `runner_up_topic_line`, `runner_up_why_not_lead_line` with a transparent rationale. AB: `distinct_lead` mode correctly leaves them empty. |
| **WHY coverage across major active findings beyond the lead** | **PARTIALLY MET** | AB: 7 of 13 top findings get governed root_cause; 4 active suboptimal findings get **none** (silent omission: `signal_homocysteine_high`, `signal_mcv_high`, `signal_apoa1_cardio_risk`, `signal_ldl_high`). VR: 6 of 12 with several active findings (`signal_hypercortisolism`, `signal_cortisol_high`, `signal_creatine_kinase_high`) silently omitted. |
| **Cross-section coherence: hero / retail / clinician tell the same core story** | **PARTIALLY MET** | Lead, retail summary, IDL primary record, and clinician page1 align. Internal tension: cardiovascular consumer card simultaneously says band `stable` + confidence `high` + headline "not a simple all-clear" — readable as a contradiction. Worth a coherence guard. |
| **Missing-data and confidence visibly framed at the user-facing surface** | **MET** | `consumer_domain_scores[*].confidence_sentence` + `confidence_tier`, `system_confidence` in meta, missing_markers in meta, page1 `confidence_and_missing_data` line, hypothesis-level `missing_data` arrays — all populated. |
| **One-sided lab range scoring works** | **MET (verified at lab-range level)** | AB and VR fixtures contain one-sided ranges (e.g. `apob_apoa1_ratio` max only, `triglycerides` max only, `vitamin_b12` min only); none triggered "insufficient numeric bounds"; the orchestrator's `_has_valid_numeric_bounds` accepts them via `has_valid_numeric_lab_range`. The clinician-report fixture confirms `lab_range_quality_by_primary_metric: "ldl_cholesterol: one-sided"` is rendered. |
| **No contradictory dual-state signal activation on healthy ranges** | **MET (no contradictory firings observed)** | Across 12 runs and ~13 active signals per panel, no signal-id appeared with conflicting "high" + "low" simultaneously; activation_state honors `enable_upper_bound`/`enable_lower_bound`. |
| **Recommendations / interventions / referrals are emitted** | **MET-but-questionnaire-invariant** | AB: 5 interventions + 2 referrals. VR: panel-appropriate set. **Identical regardless of lifestyle profile** — no lifestyle-aware action set. |
| **Questionnaire / lifestyle materially used in user-visible output** | **NOT MET** | See §4. Lead, retail, page1, IDL, scores, bands, headlines, consequences, next-steps, recommendations all identical across radically different profiles. |
| **Mock-mode honesty surfaced to the user** | **PARTIALLY MET** | `runtime_mode = "deterministic_mock"` on the DTO meta block. Not surfaced in user-visible narrative. Wording invites a personalised-AI read. |
| **Legacy `insights[]` array is either non-empty/meaningful or absent** | **NOT MET** | Always emits 6 generic placeholder entries (`legacy_v1` manifest, empty biomarkers/drivers/evidence) regardless of panel content. If the frontend renders `analysis_result.insights`, those entries become user-visible empty placeholders. Either remove the array or replace it with real per-domain content. |
| **Replay manifest stamped per run** | **MET** | `replay_manifest.json` written per run with engine versions, registry hashes, signal_registry_version, arbitration_version. |
| **Persistence guard / replay regression tests in Sentinel** | **UNCLEAR (not exercised in this verification)** | Out of scope — `test_persisted_result_replay_status.py` is a status-reporting placeholder per Sentinel Phase 1 report; not verified at runtime here. |
| **Coherence guards (e.g. mismatched band ↔ headline) in Sentinel** | **NOT MET (verified absent at runtime)** | The cardiovascular `stable / high / "not a simple all-clear"` pattern reaches DTO without triggering any guard. No coherence assertion is exercised on the live output. |

---

## 6. Most important verified launch blockers

These are the only items the runtime evidence actually justifies treating as launch blockers.

1. **The questionnaire produces no user-visible payoff.** Verified across 12 runs: identical lead, identical scores, identical bands, identical headlines, identical retail summary, identical next steps, identical recommendations, identical IDL, even with extreme lifestyle contrast. This is the single biggest credibility risk for paid launch — the product asks for lifestyle data and visibly does nothing with it.
2. **The legacy `insights[]` array on the AnalysisDTO emits 6 generic empty-shell placeholders on every run.** If the frontend ever renders `analysis_result.insights[*]`, the user sees boilerplate dressed as personalised insight. Either remove this surface, gate it, or rebuild it from the now-rich `top_findings` + `interpretation_display_layer_v1` + `root_cause_v1` data.
3. **Several active suboptimal findings carry no governed WHY (silent omission).** AB: `signal_homocysteine_high` (rank 2), `signal_mcv_high` (rank 3), `signal_apoa1_cardio_risk` (rank 5), `signal_ldl_high` (rank 7). VR: `signal_hypercortisolism` (rank 4), `signal_cortisol_high` (rank 6), `signal_creatine_kinase_high` (rank 7). On the runtime surface these become entries in `top_findings` and `consumer_domain_scores[*].active_signal_ids` without any structured WHY behind them. Either add to `_ROOT_CAUSE_TARGETS`, or deduplicate against the canonical signal that already has a hypothesis set, or suppress from user-visible top-finding rendering.
4. **Mock-mode honesty is implicit, not explicit.** Wording such as "your measured homocysteine is the main lab anchor for this thread" invites a personalised-AI read. The `runtime_mode` flag is in the meta block but not surfaced to the user. The product should be honest about template generation in deterministic_mock.
5. **One coherence-guard gap is reproducible.** Cardiovascular consumer card with `band_label: stable`, `confidence_tier: high`, and `headline_sentence: "not a simple all-clear"` is internally inconsistent and reaches the DTO unchallenged. A regression guard for "band ↔ headline polarity coherence" would catch this.

Items the gap map flagged as launch-blockers but **runtime evidence does not support**:
- "Runner-up surfacing exists in contract but is unverified in runtime." → **Verified working** in `clinician_report_v1.sections.page1` for VR.
- "WHY coverage may be shallow / many fallback strings on the lead." → **Verified rich and governed** for the lead on both panels; zero fallback strings in 12 runs.
- "IDL bundle may be wired in code but not present at runtime." → **Verified present** with multiple enabled records.
- "One-sided ranges may break scoring." → **Verified working** on AB/VR.
- "Contradictory signal activation may still occur." → **None observed** on AB/VR with the four contrasting profiles.

---

## 7. Most important surprises

### Better than expected
- **Governed WHY for the lead is a genuine, structurally well-formed product.** Evidence_for, evidence_against, missing_data, confirmatory_tests, hypothesis_confidence, multiple competing hypotheses — this is a real differentiator and it works without LLM augmentation.
- **Runner-up disclosure language is unusually honest** when it fires. "…similarly strong on this panel (0.90 vs 0.90); the headline shows one pattern first so the discussion has a single starting point." This is the kind of honesty most consumer health products avoid.
- **The IDL bundle is actually populated** with rich `why_it_matters`, `severity_state`, `frontend_allowed_term`, and `supporting_biomarkers_summary`. Frontend has live material to render today.
- **Replay manifest, arbitration report, explainability report are all stamped per run.** Auditability infrastructure is real.
- **Missing-data framing is consistent** across `meta.missing_markers`, `meta.system_confidence`, `consumer_domain_scores[*].confidence_sentence`, and per-hypothesis `missing_data` arrays.

### Worse than expected
- **The questionnaire is functionally invisible to users.** This is the single most damaging gap between strategic narrative and runtime reality. The lifestyle modifier engine is correct; the bridge is correct; the path that joins them to user-visible surfaces is the gap.
- **The legacy `insights[]` array is dead weight.** Every run produces six boilerplate placeholders that look like content and contain none.
- **Active findings without WHY are still common.** Even though `_ROOT_CAUSE_TARGETS` was expanded to 37 entries, the runtime shows 4–5 active suboptimal findings per panel falling outside that list. The fix is partly definitional (some entries are duplicates of canonical signals that already have hypotheses), partly substantive.
- **`lifestyle.confidence_adjustments` is uniformly 0.0** in all four profiles. The path exists but isn't producing values in our runs — either gated or not exercised by any of the profile shapes we used. Worth a quiet investigation.
- **Cardiovascular `band_label: stable` + `headline_sentence: "not a simple all-clear"` coherence bug is reproducible and unguarded.**

---

## 8. Recommended next move

Not a sprint plan; a single workstream that the runtime evidence now ranks above all others.

**Make the questionnaire produce a visible, defensible payoff on the user-facing surface — and clean up the empty `insights[]` array along the way.**

Concretely, before any further analytical depth expansion, the next workstream that genuinely matters is:

> Connect the lifestyle modifier engine and `lifestyle_interpretation_bridges_v1` to the user-facing surfaces that already exist (`consumer_domain_scores`, `clinician_report_v1.sections.page1`, `narrative_report_v1.retail_summary`, `actions.interventions`), and decide what to do with the legacy `insights[]` array.

A minimum acceptance bar for that workstream, derived from the runtime gaps verified here:

- Two contrasting lifestyle profiles on the same AB panel produce **at least one different user-visible field** in `consumer_domain_scores`, `clinician_report_v1.sections.page1`, or `narrative_report_v1.retail_summary` — and the difference is explained in language a paying user can read.
- The alcohol-methylation bridge surfaces in user-readable language (not raw rationale codes) when it activates, and is suppressed cleanly when it does not.
- `actions.interventions` differs by lifestyle profile in at least one panel — for example, an alcohol-aware lifestyle intervention surfaces only when the alcohol bridge is active.
- `analysis_result.insights[]` is either removed from the public DTO, gated behind a feature flag, or rebuilt from the data already present in `top_findings` + `interpretation_display_layer_v1` + `root_cause_v1` so that it carries real per-domain content.
- A regression guard exists at Sentinel level proving that swapping a healthy lifestyle profile for a stressed one on the same panel changes at least one user-visible field, and that the alcohol bridge text reaches the user when active.

Without that workstream, the product can claim launch-grade analytical depth on the lead finding (fairly), but cannot honestly claim that it uses the questionnaire — which is a more dangerous claim to break than to defer.
