# HealthIQ AI — Reverse Engineering of AB Gold Standard Narrative

**Produced by:** Claude Code (claude-sonnet-4-6)  
**Date:** 2026-04-19  
**Task:** Reverse-engineer `AB_GOLD_STANDARD_NARRATIVE_REPORT_CHAT_2_FINAL.md` back to backend/governed assets and produce a deterministic support map.

---

## 1. Executive Summary

### How much of the benchmark is supportable today

Of the ~22 distinct narrative moves identified in the benchmark, approximately **7 are fully supportable** from existing deterministic assets, **11 are partially supportable** (the underlying data exists but the compiled narrative layer does not), and **4 are not currently supportable** at all.

The backend is strong at the data-layer and signal-evaluation level. The critical gap is not data — it is the absence of a **narrative compilation layer** that translates signals, hypotheses, lifestyle context, and longitudinal deltas into the kind of pathway-led prose the benchmark demonstrates.

### Biggest backend strengths

1. **Signal and hypothesis coverage for the lead pathway is excellent.** The homocysteine/methylation domain is one of the best-covered areas in the knowledge bus. Root cause hypotheses (`hcy_hypotheses_v1.yaml`), multiple KB packages, MCV macrocytosis signal packages, and confirmatory test references (MMA, active B12, repeat homocysteine) are all in place.
2. **Lipid transport coverage is solid.** ApoB, ApoA1, lipoprotein(a), TC:HDL, non-HDL, triglycerides are all registered in SSOT and supported by root cause hypotheses and multiple KB packages through KB-S45 and KB-S60.
3. **Longitudinal infrastructure exists.** `snapshot_linker.py`, `state_transition_engine.py`, and `state_transition_v1.py` provide biomarker-level improving/worsening transition codes and prior snapshot linking. The foundation is present.
4. **Lifestyle data is captured.** `lifestyle_registry.yaml` and `questionnaire.json` include `alcohol_units_per_week`, `fasting` pattern indicators, and other inputs from the benchmark context. The `lifestyle_modifier_engine.py` applies modifiers to burden scores.
5. **Cluster/system grouping covers all benchmark systems.** `clusters.yaml` defines metabolic, cardiovascular, hepatic, renal, inflammatory, hematological, hormonal, and nutritional clusters — matching the benchmark's multi-system "background is calm" structure.

### Most important deterministic gaps

1. **No narrative assembly compiler.** The current `report_compiler_v1.py` assembles structured JSON outputs (ranked top findings, hypotheses, evidence items, confirmatory tests). It does not produce the pathway-led, system-biology prose the benchmark demonstrates. The actual golden narrative output (`backend/artifacts/golden_runs/20260405T085509Z/narrative.txt`) confirms this: it is a single-sentence repetition, not a clinical narrative.
2. **No body-overview / systemic reassurance compiler.** The benchmark's multi-system "this is not broad metabolic deterioration" framing requires a cross-cluster, exclusionary narrative layer that does not exist. Cluster statuses exist; compiled explanatory prose does not.
3. **No lifestyle-to-pathway interpretation join for the alcohol → one-carbon chemistry link.** The lifestyle engine modifies hepatic burden scores, but there is no deterministic asset connecting `alcohol_units_per_week` to the homocysteine/methylation pathway, MCV, or one-carbon metabolism drag.
4. **No longitudinal numeric-delta compiler.** The state_transition engine produces `improving`/`worsening` codes but does not emit the specific numeric values (creatinine 110→87, HbA1c 32→26, B12 236→336) or the physiological interpretation of those changes. The benchmark's entire Section 5 depends on this.
5. **No functional reading / confidence-grade / uncertainty compiler.** The benchmark's "what limits certainty" prose, the nuanced confidence grade (moderate vs moderately high), and the "this is not X, it is Y" functional interpretation labels are not governed assets anywhere in the repo.

---

## 2. Source Benchmark

`docs/golden-narrative/AB_GOLD_STANDARD_NARRATIVE_REPORT_CHAT_2_FINAL.md`

---

## 3. Reverse-Engineering Matrix

> **Legend:** FULL = deterministically supportable from existing assets | PARTIAL = underlying data/signals exist, compiled narrative layer missing | NONE = no relevant backend asset exists

| # | Section / Narrative Move | Benchmark Text Summary | Required Support Type | Existing Repo Asset(s) | Exact File Path(s) | Support Status | Gap Explanation | Required Deterministic Build Implication |
|---|---|---|---|---|---|---|---|---|
| 1 | **Patient context block** — demographics and lifestyle as authoritative interpretation inputs | 59M, 25u/wk alcohol, 13–14h fasting, 4–7 kg weight loss, manual work, good sleep, low stress | Questionnaire + lifestyle SSOT; runtime context injection | `questionnaire.json` (DOB → age, biological_sex, chronic_conditions, medications), `lifestyle_registry.yaml` (alcohol_units_per_week, sleep_hours, waist_circumference_cm etc.) | `backend/ssot/questionnaire.json`, `backend/ssot/lifestyle_registry.yaml` | **FULL** | All required fields exist in governed registries. Age is derivable from DOB at runtime. | None — data capture is complete. Surface existing fields as authoritative interpretation context block. |
| 2 | **Placeholder patient summary** — retail-grade 4-sentence overview for lay audience | "Overall this panel is reassuring… main issue is homocysteine/red-cell pathway… second theme is cholesterol handling… most useful next step is targeted follow-up" | Retail narrative compiler; cross-system priority synthesis asset | None. `retail_explainer_v1/registry.yaml` has per-biomarker education text only (not a cross-system summary layer) | `backend/ssot/retail_explainer_v1/registry.yaml` | **NONE** | No retail summary narrative compiler exists. The benchmark itself labels this "Placeholder patient summary — to be refined into final retail summary layer." The retail explainer registry contains biomarker-level education prose only, not a cross-system priority synthesis output. | New compiler needed: retail summary compiler. Inputs: ranked top findings + cluster statuses + longitudinal direction. Output: 3–4 sentence lay-readable panel summary. |
| 3 | **Body overview** — multi-system "background is calm" framing | "Background physiology is relatively calm. Glycaemic control is strong. Inflammatory tone is low. Liver markers are quiet. Renal markers materially more reassuring. That matters because the panel does not read as a body under broad metabolic pressure." | Cross-cluster narrative assembler; exclusionary/confirmatory framing layer | Cluster definitions (`clusters.yaml`), system burden registry (`system_burden_registry.yaml`), calibration engine (`calibration_engine.py`), signal evaluator outputs — provide the *data* for each system. | `backend/ssot/clusters.yaml`, `backend/ssot/system_burden_registry.yaml`, `backend/core/analytics/calibration_engine.py` | **PARTIAL** | System-level burden/status data exists deterministically. There is no governed asset or compiler that assembles this into "background is calm" prose with the correct exclusionary logic ("The panel does not read as a body under broad metabolic pressure"). Current report_compiler_v1.py produces ranked top_findings, not a multi-system reassurance narrative. | New compiler asset needed: body-overview narrative compiler. Must consume cluster/system burdens, identify quiet vs active systems, and compile exclusionary framing ("not broad deterioration because X, Y, Z are quiet"). |
| 4 | **Hierarchy of concern** — lead vs secondary pattern with explicit ranking rationale | "The main interpretive weight sits in homocysteine/MCV/methylation… The second theme is lipid transport… overall picture is one clearer functional inefficiency and one secondary long-term vascular monitoring issue." | Lead-phenotype determination logic + narrative hierarchy compiler | Arbitration engine (`arbitration_registry.yaml`, `scoring_policy.yaml`), `report_compiler_v1.py` `_top_finding_sort_tuple` and `PrimaryConcernMode` logic | `backend/ssot/arbitration_registry.yaml`, `backend/ssot/scoring_policy.yaml`, `backend/core/analytics/report_compiler_v1.py` | **PARTIAL** | The arbitration engine deterministically ranks lead vs secondary findings. `PrimaryConcernMode` classifies `distinct_lead`, `near_tie_ambiguity`, and `technical_tiebreak_lead`. However, the *prose explanation* of why the lead leads and why the secondary is secondary is not a governed asset. The compiler emits ranked JSON, not the "why this leads over that" narrative. | New narrative asset needed: hierarchy-explanation compiler. Must consume lead/secondary ranked outputs and emit a governed prose rationale for the ordering. |
| 5 | **"This is not broad metabolic deterioration"** — explicit exclusionary framing | "The more precise reading is that the clearest residual inefficiency is not general metabolic deterioration, but incomplete handling of one-carbon chemistry." | Negative-space / exclusionary narrative compiler; quiet-system catalogue | Same cluster/system burden infrastructure as #3 | `backend/ssot/clusters.yaml`, `backend/ssot/system_burden_registry.yaml` | **PARTIAL** | Data to support the negative framing exists (glycaemia, inflammation, liver, renal, thyroid cluster burdens are all computable). No compiler translates "these clusters are quiet" into the exclusionary "not broad metabolic deterioration" prose the benchmark uses. | Same compiler as #3 — extend to emit exclusionary sentences when ≥3 clusters are quiet and a single lead pathway is active. |
| 6 | **Lead pathway: system biology explanation** — one-carbon metabolism explained at pathway level | "How efficiently it transfers methyl groups… how it recycles homocysteine… supports vascular maintenance, nucleotide synthesis, neurological signalling, red-cell maturation… Homocysteine sits at a metabolic junction… transsulfuration pathway… B6 dependent" | Governed pathway prose asset; system-level educational explainer (not just biomarker-level) | IDL record `ph_vascular_hcy_inflammation_v1` (why_it_matters: "Accumulating vascular-risk signals warrant cardiometabolic review and lifestyle action" — one sentence only). `retail_explainer_v1/registry.yaml` has no homocysteine entry for pathway-level prose. Signal libraries have `description` fields but these are condition labels, not narrative pathway explanations. | `knowledge_bus/interpretation_display_layer_v1/idl_records_v1.yaml` (line ~33), `backend/ssot/retail_explainer_v1/registry.yaml` | **PARTIAL** | The IDL record exists for the vascular-homocysteine construct but its `why_it_matters` field is a single brief sentence. No governed pathway prose asset exists that explains one-carbon metabolism at the level the benchmark demonstrates. The KB signal descriptions are evaluation metadata, not user-facing pathway narratives. | New governed asset needed: pathway-grade prose explainer for methylation/one-carbon system. Could live in IDL v1 `system_biology_prose` field or a dedicated pathway_explainer registry. Must cover: methionine cycle, remethylation routes, transsulfuration, red-cell maturation link. |
| 7 | **Lead pathway: marker evidence block** — which markers carry the pattern and which are reassuring | "Markers carrying this pattern: elevated homocysteine, raised MCV, upper-range MCH, prior below-range B12, low CRP. Markers making picture reassuring: CRP low, haemoglobin normal, folate not frankly deficient, active B12 adequate." | Root cause hypothesis compiler; evidence_for / evidence_against structured output | `hcy_hypotheses_v1.yaml` has `evidence_for_rules` (B12 low/borderline, macrocytosis support, folate low/borderline) and `evidence_against_rules` (B12 clearly normal, folate clearly normal). Root cause compiler (`root_cause_compiler_v1.py`) and contract (`root_cause_v1.py`) emit `evidence_for` and `evidence_against` lists with marker_refs. | `knowledge_bus/root_cause/hypotheses/hcy_hypotheses_v1.yaml`, `backend/core/analytics/root_cause_compiler_v1.py`, `backend/core/contracts/root_cause_v1.py` | **FULL** | Root cause compiler deterministically assembles evidence_for and evidence_against with marker references. The schema (`RootCauseEvidenceItemV1`) supports `item` and `marker_refs`. This directly maps to the benchmark's "markers carrying this pattern / markers making picture reassuring" structure. | None — asset exists. Surfacing gap: the compiled evidence block needs to be included in the display output with appropriate framing (two-column evidence layout). |
| 8 | **Lead pathway: functional reading label** — "incomplete homocysteine clearance / methylation efficiency, not simple persistent serum B12 deficiency" | "The more precise interpretation is incomplete homocysteine clearance / methylation efficiency, rather than a simple persistent serum B12 deficiency." | Governed functional-label compiler; hypothesis title + interpretation disambiguation | `hcy_hypotheses_v1.yaml` hypotheses include `hcy_b12_pattern_v1` (title: "B12-associated pattern") and evidence_against rule for "B12 clearly normal" — these support ranking hypotheses by fit. However, no governed "functional reading label" or "this is X not Y" disambiguation asset exists. The `summary_template` fields are brief. | `knowledge_bus/root_cause/hypotheses/hcy_hypotheses_v1.yaml` | **PARTIAL** | The hypothesis ranking mechanism exists, and the B12-normal evidence_against rule fires when serum B12 is within range — which would surface the correct hypothesis ranking. However, the functional reading prose ("incomplete clearance / methylation efficiency, not simple deficiency") is not a governed narrative asset. No compiler translates hypothesis ranking output into the benchmark's disambiguation prose. | New asset needed: functional-label compiler or governed functional_reading_prose field in root cause hypotheses. When `hcy_b12_pattern_v1` has evidence_against rule fired but signal is still at_risk, emit the "pathway running with friction, not simple deficiency" prose label. |
| 9 | **Lead pathway: why this matters beyond itself** — upstream vascular context | "Matters for vascular biology because homocysteine is not simply a passive by-product… persistently inefficient clearance keeps a less favourable vascular maintenance environment in view even when CRP is low and lipid transport profile is partly protective." | Governed cross-pathway impact narrative; upstream link to vascular biology | IDL record `ph_vascular_hcy_inflammation_v1` has `why_it_matters` = one sentence. Signal library condition descriptions cover elevation context. Phenotype map has vascular homocysteine inflammation pattern with evidence notes. Interaction map has relevant chain edges. | `knowledge_bus/interpretation_display_layer_v1/idl_records_v1.yaml`, `knowledge_bus/phenotypes/phenotype_map_v1.yaml`, `knowledge_bus/interaction_maps/interaction_map_v1.yaml` | **PARTIAL** | The phenotype map and IDL record acknowledge the vascular relevance, but the depth of the "why this matters beyond itself" prose — specifically the cross-pathway interaction ("even when CRP is low and lipid transport is protective, homocysteine still matters because…") — is not governed. No compiler produces this cross-pathway contextualisation. | Extend IDL v1 `why_it_matters` field with a governed `beyond_itself_prose` subfield, or add a cross-system contextualisation block to the phenotype narrative compiler. |
| 10 | **Lead pathway: why this leads** — competitive comparison across all systems | "This pattern leads because it is coherent across multiple connected markers and because the competing systems are either quieter or more buffered. There is no equally strong glycaemic, hepatic, inflammatory, thyroid, or renal signal competing." | Lead-determination compiler + competitive exclusion narrative | Arbitration engine + `PrimaryConcernMode` logic (as in #4) | `backend/core/analytics/report_compiler_v1.py`, `backend/ssot/arbitration_registry.yaml` | **PARTIAL** | Arbitration engine can determine that homocysteine-pattern leads by score. `PrimaryConcernMode = distinct_lead` would fire. No compiler translates that determination into the "there is no equally strong glycaemic / hepatic / inflammatory signal competing" narrative prose. | Same compiler as #4 — include a "why leads" prose block that lists quiet competing systems by name. Requires cluster-status output to be fed into the lead-explanation compiler. |
| 11 | **Lead pathway: confidence and limits** — nuanced confidence grade with named clarifying tests | "Confidence is moderate. What limits certainty: absence of methylmalonic acid, pyridoxal-5-phosphate, repeat homocysteine after alcohol-reduction period." | Confidence grading compiler; uncertainty prose asset; confirmatory test narrative | `hcy_hypotheses_v1.yaml` has `evidence_strength: "moderate"` and `missing_data_markers` with `methylmalonic_acid` (marker_id, reason). Confirmatory tests registry has `test_methylmalonic_acid_v1`. Root cause contract has `missing_data` and `confirmatory_tests` fields. | `knowledge_bus/root_cause/hypotheses/hcy_hypotheses_v1.yaml`, `knowledge_bus/registries/confirmatory_tests_v1.yaml`, `backend/core/contracts/root_cause_v1.py` | **PARTIAL** | The structured data for confidence grade and missing tests exists. `evidence_strength` = "moderate" is a governed field. `missing_data_markers` and `confirmatory_tests` are compiled deterministically by `root_cause_compiler_v1.py`. However, no compiler translates this into the narrative "confidence is moderate because X and Y are absent; this would be clarified by Z" prose. Pyridoxal-5-phosphate (B6) is not currently in `hcy_hypotheses_v1.yaml` missing_data — gap in hypothesis coverage. | New compiler asset needed: confidence-narrative compiler. Must consume `evidence_strength`, `missing_data`, and `confirmatory_tests` and emit the benchmark-style "confidence is X, limited by Y, would improve if Z" prose block. |
| 12 | **Lead pathway: monitoring relevance** — improvement criteria and persistence meaning | "Improvement would mean: homocysteine falling back into range, MCV moving closer to range, maintenance of normal haemoglobin. Persistence would suggest pathway efficiency remains incomplete even if serum B12 acceptable." | Governed monitoring criteria compiler; improvement/persistence narrative | No explicit `monitoring_criteria` field in `hcy_hypotheses_v1.yaml` or root_cause_v1.py contract. `state_transition_v1.py` transitions (improving/worsening) exist but apply to individual biomarker statuses, not to pathway-level resolution criteria. | `backend/core/contracts/state_transition_v1.py`, `backend/core/analytics/state_transition_engine.py` | **PARTIAL** | Longitudinal transition codes exist per biomarker. No governed "pathway resolution criteria" asset exists that names which markers define improvement vs persistence for a given pattern. The benchmark's monitoring framing ("what improvement looks like for this pathway") requires a compiler that translates hypothesis-level targets into a monitoring narrative. | New asset needed: pathway monitoring criteria compiler. Add `resolution_markers` and `persistence_indicators` fields to root cause hypothesis schema; compile into monitoring narrative. |
| 13 | **Lead pathway: alcohol-lifestyle link to macrocytosis/one-carbon metabolism** | "Daily alcohol intake is relevant here. Alcohol can contribute to macrocytosis and can impair one-carbon metabolism even without producing abnormal liver enzymes. It can alter folate handling, interfere with efficient B-vitamin use." | Lifestyle-to-pathway interpretation join; alcohol-specific mechanism narrative | `lifestyle_modifier_engine.py` maps `alcohol_units_per_week` to hepatic burden modifier. `clusters.yaml` hepatic cluster includes alcohol. `pkg_kb52c_mcv_high_nonmegaloblastic_macrocytosis/signal_library.yaml` has evidence_against rule for alcohol-related macrocytosis when GGT is high. `lifestyle_registry.yaml` line 219: `hepatic: [alcohol_units_per_week]`. | `backend/core/analytics/lifestyle_modifier_engine.py`, `backend/ssot/lifestyle_registry.yaml`, `knowledge_bus/packages/pkg_kb52c_mcv_high_nonmegaloblastic_macrocytosis/signal_library.yaml` | **PARTIAL** | Alcohol is captured as a lifestyle input and applied as a hepatic burden modifier. The MCV non-megaloblastic package mentions alcohol-related macrocytosis. However, there is **no deterministic join** between `alcohol_units_per_week` and the homocysteine pathway / one-carbon metabolism signal. The benchmark's alcohol → methylation → macrocytosis interpretation chain is not governed. The lifestyle engine modifies hepatic scores only; it does not feed into the methylation/homocysteine signal evaluation or root cause compiler. | New deterministic asset needed: alcohol-to-methylation pathway modifier. Add `alcohol_context_modifier` to hcy_hypotheses or a lifestyle-signal bridge in `lifestyle_registry.yaml` for the nutritional/methylation system. Deterministic rule: if `alcohol_units_per_week > threshold`, add alcohol context to MCV and homocysteine root cause evidence blocks. |
| 14 | **Secondary phenotype: lipid system biology** — transport architecture explanation | "LDL particles deliver cholesterol into tissues. HDL participates in reverse transport. ApoB gives a better sense of atherogenic particles. Triglycerides often reflect insulin resistance distorting lipid flow." | Governed lipid system pathway prose asset | `retail_explainer_v1/registry.yaml` has per-biomarker education prose for total_cholesterol, ldl_cholesterol, hdl_cholesterol, triglycerides, non_hdl_cholesterol — but these are single-marker education texts, not system-level transport architecture explanations. `lipid_transport_dysfunction_hypotheses_v1.yaml` provides root cause structure but not pathway prose. | `backend/ssot/retail_explainer_v1/registry.yaml`, `knowledge_bus/root_cause/hypotheses/lipid_transport_dysfunction_hypotheses_v1.yaml` | **PARTIAL** | Individual biomarker education prose exists. No governed "lipid transport architecture" system-level pathway explainer exists. The benchmark's lipid biology section explains how the whole system works (LDL + HDL + ApoB + TG as a unified transport architecture), which is a system-biology prose asset distinct from individual marker explanations. | New governed asset needed: lipid transport system pathway explainer. Add `system_biology_prose` to IDL record for lipid cluster or create a dedicated `pathway_explainer_v1` registry entry for the cardiovascular/lipid system. |
| 15 | **Secondary phenotype: protective architecture framing** — "not uniformly adverse, here is why" | "HDL strong, TG low, ApoB controlled, ApoB:ApoA1 favourable, TC:HDL low, non-HDL in range, lipoprotein(a) low — this changes the vascular reading." | Multi-marker protective-feature compiler; ApoB/ApoA1/Lp(a) compound framing | All relevant biomarkers registered: `apob`, `apob_apoa1_ratio`, `lipoprotein_a`, `tc_hdl_ratio`, `non_hdl_cholesterol`, `hdl_cholesterol`, `triglycerides` in `biomarkers.yaml`. KB packages exist: `pkg_kb45_apob_high_atherogenic`, `pkg_kb45_apob_apoa1_ratio_high_imbalance`, `pkg_kb60_tc_hdl_ratio_high_atherogenic_discordance_pattern`, `pkg_kb52d_non_hdl_cholesterol_*`, `pkg_kb52c_lipoprotein_a_*`. Root cause hypotheses in `lipid_transport_dysfunction_hypotheses_v1.yaml`. | `backend/ssot/biomarkers.yaml`, `knowledge_bus/packages/pkg_kb45_apob_apoa1_ratio_high_imbalance/`, `knowledge_bus/packages/pkg_kb60_total_cholesterol_*/`, `knowledge_bus/root_cause/hypotheses/lipid_transport_dysfunction_hypotheses_v1.yaml` | **PARTIAL** | All marker data and signal evaluation packages exist. No compiler assembles the "protective architecture" narrative — the logic of "LDL is mildly elevated BUT the protective side is strong, therefore interpret as residual exposure not dangerous dyslipidaemia." The root cause compiler emits hypotheses for each signal; it does not emit a cross-marker compound protective framing. | New compiler asset needed: compound lipid transport narrative compiler. Must consume the full lipid marker set (LDL, HDL, TG, ApoB, ApoB:ApoA1, TC:HDL, Lp(a)) and emit a protective-architecture framing when the majority of transport markers are favourable despite LDL being mildly elevated. |
| 16 | **Secondary phenotype: why this did not lead** — explicit secondary-to-lead comparative rationale | "This did not lead because the system is only mildly adverse on the LDL side and materially more reassuring elsewhere. The homocysteine/macrocytosis pattern is less compensated and more clearly unresolved." | Comparative ranking explanation compiler | Arbitration engine produces ranking; `PrimaryConcernMode` and `_near_tie_cluster_in_top3()` logic classify the relationship. No compiler translates that classification into "why the secondary did not lead" prose. | `backend/core/analytics/report_compiler_v1.py` | **PARTIAL** | The arbitration ranking is deterministic. The "why secondary" prose is not a governed output. | Same as #4 — hierarchy explanation compiler should cover both "why lead leads" and "why secondary did not lead." |
| 17 | **Longitudinal section: direction of travel** — broad trajectory framing with physiological interpretation | "The broad trajectory over four months is favourable. The panel does not suggest deteriorating metabolic health. Weight loss and longer fasting have plausibly improved glycaemic efficiency." | Longitudinal narrative compiler; physiological interpretation of state transitions | `snapshot_linker.py` builds prior InsightGraph snapshots. `state_transition_engine.py` produces `improving`/`worsening` codes per biomarker. `state_transition_v1.py` defines `BiomarkerTransitionNode` with `from_status`, `to_status`, `transition`. Calibration and precedence registries include `system_trending_improving`/`system_trending_worse` codes. | `backend/core/analytics/snapshot_linker.py`, `backend/core/analytics/state_transition_engine.py`, `backend/core/contracts/state_transition_v1.py`, `backend/ssot/calibration_registry.yaml` | **PARTIAL** | The infrastructure to detect that systems are improving exists at the biomarker-transition level. No compiler translates biomarker-level transition codes into a "broad trajectory is favourable / background system is now cleaner" prose narrative. The physiological interpretation of the aggregate trajectory ("weight loss and fasting have plausibly improved glycaemic efficiency") requires a governed lifestyle-context join with the transition output — which also doesn't exist. | New compiler needed: longitudinal narrative compiler. Inputs: aggregated transition codes (improving/worsening per system), lifestyle change deltas (weight loss, fasting change). Output: direction-of-travel prose paragraph with physiological framing. |
| 18 | **Longitudinal section: specific marker deltas** — named prior values vs current values | "Creatinine improved from 110 to 87. eGFR improved from 67 to 84. HbA1c improved from 32 to 26. B12 from 236 to 336. Folate: modest improvement. Triglyceride-related transport improved." | Numeric delta compiler; prior panel value access | `snapshot_linker.py` builds `LinkedSnapshots` from persisted `AnalysisResult` rows. However, `_nodes_from_biomarkers_payload()` reconstructs `BiomarkerNode` objects containing only `biomarker_id`, `status` (normalised low/normal/high), and `score` (0–100 band). **Raw measurement values are not preserved in the snapshot.** | `backend/core/analytics/snapshot_linker.py` (lines ~62–78) | **NONE** | The snapshot linker intentionally reconstructs only normalised status codes and band scores from persisted payloads — not raw numeric values. The benchmark's specific delta values (110→87, 32→26, 236→336) require prior raw measurements to be persisted and accessible. The current contract has no `raw_value` field in `BiomarkerNode`. | New contract field needed: add `raw_value: Optional[float]` to `BiomarkerNode` in `insight_graph_v1.py` and persist it in the analysis result payload. Requires a numeric-delta compiler that outputs "marker X improved from Y to Z" with units. |
| 19 | **Longitudinal section: what has not resolved** — identifying persistent patterns | "Homocysteine/macrocytosis pattern: now more visible because the larger panel measured homocysteine directly. LDL-related exposure: still mildly present. Alcohol-related context: still physiologically relevant." | Persistent pattern identifier; cross-panel pattern stability compiler | `state_transition_engine.py` stable_abnormal transition code covers this structurally for individual biomarkers. No compiler assembles a "what has not resolved" narrative block. | `backend/core/contracts/state_transition_v1.py` (`stable_abnormal` TransitionCode), `backend/core/analytics/state_transition_engine.py` | **PARTIAL** | `stable_abnormal` transition code exists — this is the correct signal for "persistent pattern." No compiler translates `stable_abnormal` outputs into "what has not resolved" narrative prose with physiological context. | Extend longitudinal narrative compiler (#17) with a persistence block: when transition = `stable_abnormal` for lead-system markers, emit a governed "what has not resolved and why it matters" prose block. |
| 20 | **Secondary systems section** — iron, renal context, androgen context as non-lead systems worth noting | "Iron: high-normal, ferritin comfortably replete, transferrin slightly low — not iron deficiency. Renal: reassuring but hydration still relevant. Androgen: within range, not a lead lane." | Secondary-system narrative compiler; multi-cluster ranked output with "worth noting" framing | `clusters.yaml` defines hematological, renal, hormonal clusters. Root cause hypotheses exist for iron (ferritin_high, ferritin_low, iron_deficiency_context, iron_overload_context, creatinine_high), transferrin (transferrin_high, transferrin_low), testosterone (pkg_kb47_free_testosterone_* packages). Cluster burdens are computable. | `backend/ssot/clusters.yaml`, `knowledge_bus/root_cause/hypotheses/ferritin_*`, `knowledge_bus/root_cause/hypotheses/transferrin_*`, `knowledge_bus/packages/pkg_kb47_free_testosterone_*/` | **PARTIAL** | All underlying signal/hypothesis data exists for iron transport, renal, and androgen systems. No compiler produces a "secondary systems worth noting" narrative block for systems that are not lead but have non-trivial findings. The report_compiler_v1 currently emits a ranked top_findings list — it would include these in order but without the "not a lead lane" contextualisation. | Extend report compiler to produce a `secondary_systems_narrative` block: systems ranked below threshold but not fully quiet, emitting a one-paragraph "worth noting" entry with a governed framing for "not a lead abnormality." |
| 21 | **Practical next steps** — prioritised follow-up action list | "1. Repeat HCY + CBC. 2. Clarify functional B-vitamin status (MMA, B6). 3. Review alcohol intake in relation to macrocytosis/homocysteine. 4. Continue longitudinal lipid monitoring. 5. Preserve favourable glycaemic background." | Prioritised action/next-steps compiler; lifestyle-linked recommendation; monitoring continuation rule | `confirmatory_tests_v1.yaml` has `test_methylmalonic_acid_v1`, `test_holotranscobalamin_active_b12_v1`, `test_homocysteine_repeat_v1`. Root cause compiler emits `confirmatory_tests` per hypothesis. `intervention_selector_v1.py` and `intervention_annotation_compiler_v1.py` exist. Report contract has `ReportActionsV1`. | `knowledge_bus/registries/confirmatory_tests_v1.yaml`, `backend/core/analytics/root_cause_compiler_v1.py`, `backend/core/analytics/intervention_selector_v1.py`, `backend/core/contracts/report_v1.py` (`ReportActionsV1`) | **PARTIAL** | Confirmatory tests and interventions are compiled deterministically. No compiler currently: (a) ranks next steps by clinical priority across multiple systems, (b) includes the alcohol-intake review as an actionable step (because the alcohol→methylation join is missing, see #13), or (c) emits the "what improvement would look like" monitoring criteria as part of the next-steps output. | Extend intervention compiler to produce a prioritised `next_steps_narrative` block. Must include cross-signal priority ordering, lifestyle-linked actions, and monitoring continuation rules derived from resolution criteria (#12). |
| 22 | **Clinician-style summary** — dense single-paragraph synthesis for clinical audience | "Relatively favourable panel overall, with reassuring glycaemic, inflammatory, hepatic, thyroid, endocrine, and renal background signals. Leading residual abnormality is coherent homocysteine-macrocytosis/methylation-efficiency pattern…" | Clinician summary compiler; cross-system synthesis block | `report_compiler_v1.py` produces `ClinicianReportV1` with `ClinicianHeaderV1`, `ClinicianSectionsV1`, `Page1SummaryBlockV1`. The contract exists. Current golden narrative output (`narrative.txt` in golden_runs) shows a placeholder single-sentence repetition, not a synthesised clinical paragraph. | `backend/core/analytics/report_compiler_v1.py`, `backend/core/contracts/clinician_report_v1.py`, `backend/artifacts/golden_runs/20260405T085509Z/narrative.txt` | **PARTIAL** | The `ClinicianReportV1` contract and `Page1SummaryBlockV1` structure exist. The compiler that populates these fields with the benchmark-quality synthesis prose does not yet exist. The golden run output confirms this: the narrative.txt is a placeholder sentence repeated. | Populate the `Page1SummaryBlockV1` via a governed clinician summary compiler. Inputs: ranked top findings, cluster statuses, longitudinal direction, confidence grades. Output: dense 3–5 sentence synthesis with lead abnormality, reassuring background, direction of travel, and highest-value next step. |

---

## 4. Existing Backend Strengths

### 4.1 Signal and hypothesis depth for lead pathway

The homocysteine/methylation pathway is among the best-covered areas in the repo. The evidence is:
- `knowledge_bus/root_cause/hypotheses/hcy_hypotheses_v1.yaml` — four hypotheses (B12-associated, folate-associated, inflammatory context, renal clearance), each with `evidence_for_rules`, `evidence_against_rules`, `missing_data_markers`, and `confirmatory_tests`
- `knowledge_bus/packages/pkg_kb52c_homocysteine_high_b_vitamin_related_methylation_impairment/signal_library.yaml` and `pkg_homocysteine_elevation_context/` — dedicated signal packages
- `knowledge_bus/packages/pkg_kb52c_mcv_high_megaloblastic_macrocytosis/` and `pkg_kb52c_mcv_high_nonmegaloblastic_macrocytosis/` — MCV macrocytosis packages including alcohol-related context
- `knowledge_bus/registries/confirmatory_tests_v1.yaml` — MMA, active B12, repeat homocysteine, full blood count all referenced

### 4.2 Comprehensive lipid transport coverage

Every lipid marker in the benchmark (LDL, HDL, ApoB, ApoA1, ApoB:ApoA1, TC:HDL, TG, Lp(a), non-HDL) is registered in `backend/ssot/biomarkers.yaml` with canonical IDs. The knowledge bus has dedicated packages for each:
- `pkg_kb45_apob_high_atherogenic`, `pkg_kb45_apob_apoa1_ratio_high_imbalance`
- `pkg_kb52c_ldl_high_atherogenic_ldl_burden`, `pkg_kb52c_lipoprotein_a_high_*`
- `pkg_kb60_total_cholesterol_*`, `pkg_kb60_tc_hdl_ratio_*`
- `knowledge_bus/root_cause/hypotheses/lipid_transport_dysfunction_hypotheses_v1.yaml` and `ldl_cholesterol_high_hypotheses_v1.yaml`

### 4.3 Lifestyle data capture is complete for this case

The AB case's lifestyle context (alcohol, fasting, weight, activity) maps cleanly to governed fields:
- `backend/ssot/questionnaire.json`: `date_of_birth`, `biological_sex`, `chronic_conditions`, `long_term_medications`
- `backend/ssot/lifestyle_registry.yaml`: `alcohol_units_per_week`, `sleep_hours`, `weight_kg`, `height_cm`, `waist_circumference_cm`, `resting_heart_rate`
- `backend/core/analytics/lifestyle_modifier_engine.py`: applies modifiers deterministically

### 4.4 Longitudinal infrastructure is in place at the transition-code level

- `backend/core/analytics/snapshot_linker.py` — links up to 3 prior InsightGraph snapshots from persisted analysis rows
- `backend/core/analytics/state_transition_engine.py` — produces `improving`, `worsening`, `stable_normal`, `stable_abnormal`, `volatile` codes per biomarker
- `backend/ssot/calibration_registry.yaml` — `system_trending_improving` / `system_trending_worse` transition requirement rules
- `backend/ssot/precedence_registry.yaml` and `conflict_registry.yaml` — trend-opposition conflict logic

### 4.5 Cluster / system groupings cover all benchmark systems

`backend/ssot/clusters.yaml` defines eight clusters: metabolic, cardiovascular, hepatic, renal, inflammatory, hematological, hormonal, nutritional. These directly map to every system the benchmark mentions in its "body overview" and "secondary systems" sections.

### 4.6 Root cause compiler architecture is production-grade

`backend/core/analytics/root_cause_compiler_v1.py`, `backend/core/contracts/root_cause_v1.py`, and the `RootCauseV1` / `RootCauseFindingV1` / `RootCauseHypothesisV1` models provide a deterministic, schema-governed pipeline for hypothesis ranking and evidence assembly. The confirmation test registry integration is complete.

### 4.7 Arbitration and lead-finding ranking is deterministic

`report_compiler_v1.py` implements `PrimaryConcernMode` classification (`distinct_lead`, `near_tie_ambiguity`, `technical_tiebreak_lead`), confidence-weighted ranking via `_top_finding_sort_tuple`, and near-tie cluster detection via `_near_tie_cluster_in_top3`. The ranking logic for lead vs secondary is deterministic.

---

## 5. Deterministic Asset Gaps

### Gap 1 — No narrative compiler (critical)

The current `report_compiler_v1.py` emits structured JSON (ranked top_findings, clinician_report with hypothesis lists, evidence arrays, confirmatory tests). The actual `narrative.txt` golden output confirms the current system does not produce prose. Every narrative section of the benchmark — body overview, pathway explanation, why-this-leads, confidence prose, longitudinal narrative, next steps — requires a narrative compilation layer that does not exist.

**Affected benchmark sections:** All of them, to varying degrees.

### Gap 2 — No body-overview / cross-cluster exclusionary compiler

There is no governed asset or compiler that takes cluster-level statuses (metabolic, hepatic, inflammatory, renal, hormonal) and emits a "background is calm / not broad metabolic deterioration" framing. The data exists; the compilation logic does not.

**Affected benchmark sections:** Body Overview (§1), Hierarchy of Concern (§1 body), Why This Leads (§3 lead phenotype).

### Gap 3 — No alcohol → one-carbon chemistry interpretation join

`lifestyle_modifier_engine.py` maps `alcohol_units_per_week` → hepatic burden modifier only. No deterministic asset connects alcohol intake to the homocysteine pathway, folate handling, or macrocytosis interpretation. The benchmark's alcohol context is one of its most clinically important narrative moves.

**Affected benchmark sections:** Lead pathway §3 (alcohol context), Longitudinal §5 (what has not resolved), Next steps §7.

### Gap 4 — No longitudinal numeric-delta compiler

`snapshot_linker.py` preserves normalised status codes and band scores but **not raw measurement values** (`BiomarkerNode` has no `raw_value` field). The benchmark's specific value deltas (creatinine 110→87, HbA1c 32→26, B12 236→336) are unproducible deterministically without raw value persistence.

**Affected benchmark sections:** Longitudinal change §5 (entire section for specific values).

### Gap 5 — No functional-label / confidence-narrative compiler

The root cause hypotheses have `evidence_strength` fields and `missing_data_markers` lists, but no compiler translates these into the benchmark's "confidence is moderate, limited by absence of MMA and B6, would improve if…" narrative prose. The nuanced "not simple deficiency but incomplete clearance / methylation efficiency" functional label is also not a governed output.

**Affected benchmark sections:** Lead pathway confidence block (§3), Secondary phenotype confidence block (§4).

### Gap 6 — No pathway-grade system biology prose assets

Individual biomarker education text exists in `retail_explainer_v1/registry.yaml`. The IDL records have one-sentence `why_it_matters` fields. Neither constitutes the pathway-level biology explanations the benchmark uses — the methionine cycle / transsulfuration explanation, the lipid transport architecture explanation. These would need to be new governed prose assets (pathway_explainer registry or extended IDL fields).

**Affected benchmark sections:** Lead pathway system biology (§3), Secondary phenotype system biology (§4).

### Gap 7 — No retail patient summary compiler

The benchmark opens with a "Placeholder patient summary" block explicitly marking that this layer is not yet built. No retail summary narrative compiler exists. `retail_explainer_v1/registry.yaml` contains biomarker education text, not a cross-system priority synthesis.

**Affected benchmark sections:** Patient summary (top of document).

---

## 6. Recommended Next Build Implications

Listed in rough priority order by their impact on producing the benchmark narrative:

### B1 — Narrative prose compiler (highest priority)
**Type:** New compiler asset  
**What:** A deterministic prose-assembly compiler that takes the structured outputs of the existing pipeline (ranked top_findings, cluster statuses, root cause hypotheses, transition codes, confirmatory tests) and assembles them into the narrative structure the benchmark demonstrates.  
**Note:** This is the master gap. Without it, all other improvements remain in structured JSON and do not produce the benchmark-style narrative.

### B2 — Raw biomarker value persistence and delta compiler
**Type:** New contract field + compiler  
**What:** Add `raw_value: Optional[float]` to `BiomarkerNode` in `backend/core/contracts/insight_graph_v1.py`. Persist raw measurement values in the analysis result payload. Build a numeric-delta compiler that emits "marker X changed from Y to Z (units)" for the longitudinal section.  
**Specific file:** `backend/core/analytics/snapshot_linker.py` (update `_nodes_from_biomarkers_payload`), `backend/core/contracts/insight_graph_v1.py`.

### B3 — Alcohol → methylation pathway interpretation join
**Type:** New deterministic lifestyle-signal bridge asset  
**What:** Add an `alcohol_context_modifier` rule to `lifestyle_registry.yaml` for the nutritional/methylation system. Create a governed rule: when `alcohol_units_per_week > X`, add alcohol context tag to homocysteine and MCV root cause evidence blocks. Update `hcy_hypotheses_v1.yaml` to include an alcohol-context `evidence_for_rule`.

### B4 — Pathway-grade system biology prose assets
**Type:** New governed content assets  
**What:** Extend the IDL record schema to include a `system_biology_prose` field (multi-sentence pathway explanation). Author governed prose for: (a) methylation / one-carbon chemistry system, (b) lipid transport architecture. These would be loaded by the narrative compiler (#B1).  
**Specific files:** `knowledge_bus/interpretation_display_layer_v1/idl_records_v1.yaml` (schema extension), new prose content entries.

### B5 — Confidence-narrative and functional-label compiler
**Type:** New compiler asset  
**What:** A compiler that consumes `evidence_strength`, `evidence_for`, `evidence_against`, `missing_data_markers`, and `confirmatory_tests` from the root cause output and emits: (a) a confidence grade sentence, (b) a "what limits certainty" list, (c) a "what would improve this" sentence, (d) a functional reading label. Add `functional_label_template` to root cause hypothesis schema.

### B6 — Body-overview / exclusionary framing compiler
**Type:** New compiler asset  
**What:** A compiler that takes all cluster statuses and emits: (a) a list of quiet systems ("glycaemic control is strong, inflammatory tone is low, liver markers are quiet"), (b) an exclusionary sentence ("the panel does not read as a body under broad metabolic pressure"), and (c) a narrow-lead framing ("the main interpretive weight sits in X"). Input: cluster burden outputs. Output: governed body-overview prose block.

### B7 — Monitoring criteria and resolution targets compiler
**Type:** New governed schema field + compiler  
**What:** Add `resolution_markers` and `persistence_indicators` fields to root cause hypothesis schema. Populate for hcy_hypotheses and lipid_transport_dysfunction. Compiler emits the "improvement would mean X, persistence would suggest Y" monitoring paragraph.

### B8 — Retail patient summary compiler
**Type:** New compiler asset  
**What:** A retail-facing 3–4 sentence compiler that takes: ranked lead finding label, secondary finding label, direction of travel, and highest-priority next step, and emits a lay-readable summary paragraph. This is the last touchpoint before user display.

---

## 7. Authority and Evidence Notes

### SSOT registries (authoritative sources)

| Asset | Path | Role |
|---|---|---|
| Biomarker registry | `backend/ssot/biomarkers.yaml` | Canonical marker IDs, aliases, context_tags (alcohol, fasting etc.) |
| Reference ranges | `backend/ssot/ranges.yaml` | Threshold values for status classification |
| Questionnaire schema | `backend/ssot/questionnaire.json` | Age (DOB), sex, conditions, medications |
| Lifestyle registry | `backend/ssot/lifestyle_registry.yaml` | alcohol_units_per_week, sleep, weight, activity modifiers |
| Clusters | `backend/ssot/clusters.yaml` | 8 body systems: metabolic, cardiovascular, hepatic, renal, inflammatory, hematological, hormonal, nutritional |
| System burden registry | `backend/ssot/system_burden_registry.yaml` | System-level burden scoring |
| Scoring policy | `backend/ssot/scoring_policy.yaml` | Confidence and severity scoring rules |
| Arbitration registry | `backend/ssot/arbitration_registry.yaml` | Lead vs secondary ranking rules |
| Retail explainer v1 | `backend/ssot/retail_explainer_v1/registry.yaml` | Per-biomarker education prose (individual markers only) |
| Calibration registry | `backend/ssot/calibration_registry.yaml` | Transition requirement rules (system_trending_improving/worse) |

### Knowledge Bus — signal and hypothesis assets

| Asset | Path | Role |
|---|---|---|
| Homocysteine root cause hypotheses | `knowledge_bus/root_cause/hypotheses/hcy_hypotheses_v1.yaml` | B12, folate, inflammatory, renal hypotheses with evidence rules |
| Lipid transport dysfunction hypotheses | `knowledge_bus/root_cause/hypotheses/lipid_transport_dysfunction_hypotheses_v1.yaml` | Non-HDL atherogenic burden hypothesis |
| LDL high hypotheses | `knowledge_bus/root_cause/hypotheses/ldl_cholesterol_high_hypotheses_v1.yaml` | LDL-specific root cause |
| Methylation impairment signal | `knowledge_bus/packages/pkg_kb52c_homocysteine_high_b_vitamin_related_methylation_impairment/signal_library.yaml` | B12/folate-related methylation signal |
| MCV megaloblastic package | `knowledge_bus/packages/pkg_kb52c_mcv_high_megaloblastic_macrocytosis/signal_library.yaml` | B12/folate macrocytosis signal |
| MCV non-megaloblastic package | `knowledge_bus/packages/pkg_kb52c_mcv_high_nonmegaloblastic_macrocytosis/signal_library.yaml` | Alcohol/hepatic macrocytosis signal |
| Phenotype map | `knowledge_bus/phenotypes/phenotype_map_v1.yaml` | Vascular HCY-inflammation phenotype, insulin resistance dyslipidaemia phenotype |
| IDL records | `knowledge_bus/interpretation_display_layer_v1/idl_records_v1.yaml` | Display labels, why_it_matters (brief), retail labels |
| Confirmatory tests registry | `knowledge_bus/registries/confirmatory_tests_v1.yaml` | MMA, active B12, repeat homocysteine, FBC, serum B12 test records |
| Interaction map | `knowledge_bus/interaction_maps/interaction_map_v1.yaml` | Signal interaction chains (homocysteine, inflammation, lipid) |

### Backend pipeline (analytical layer)

| Asset | Path | Role |
|---|---|---|
| Root cause compiler | `backend/core/analytics/root_cause_compiler_v1.py` | Assembles hypothesis evidence blocks from YAML rules |
| Report compiler | `backend/core/analytics/report_compiler_v1.py` | Assembles ranked top_findings + clinician report JSON |
| Snapshot linker | `backend/core/analytics/snapshot_linker.py` | Links up to 3 prior InsightGraph snapshots |
| State transition engine | `backend/core/analytics/state_transition_engine.py` | Produces improving/worsening/stable transition codes per biomarker |
| Lifestyle modifier engine | `backend/core/analytics/lifestyle_modifier_engine.py` | Applies alcohol, BMI, sleep modifiers to burden scores |
| Root cause contract | `backend/core/contracts/root_cause_v1.py` | `RootCauseV1`, `RootCauseFindingV1`, `RootCauseHypothesisV1` schema |
| State transition contract | `backend/core/contracts/state_transition_v1.py` | `BiomarkerTransitionNode`, `TransitionCode` literals |
| Clinician report contract | `backend/core/contracts/clinician_report_v1.py` | `ClinicianReportV1`, `Page1SummaryBlockV1`, `RootCauseFindingV1` |
| Report contract | `backend/core/contracts/report_v1.py` | `ReportV1`, `ReportActionsV1`, `ReportTopFindingV1` |

### Fixtures and golden outputs (not authoritative — for comparison only)

| Asset | Path | Note |
|---|---|---|
| Latest golden narrative | `backend/artifacts/golden_runs/20260405T085509Z/narrative.txt` | Current actual output — single placeholder sentence repeated, confirming narrative compiler gap |
| VR clinician report | `_vr_manual_review/clinician_report_v1_vr.generated.json` | Verification run output — structured JSON, not prose narrative |

---

*End of reverse-engineering report.*
