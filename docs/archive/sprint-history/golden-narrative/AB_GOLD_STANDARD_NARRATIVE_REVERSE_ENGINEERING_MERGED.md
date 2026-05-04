# HealthIQ AI — AB Gold Standard Narrative Reverse Engineering (Merged)

## 1. Executive summary
- The benchmark is **partly supportable today** from existing deterministic backend assets. The repo is already strong at canonical biomarker governance, rich AB fixtures, signal evaluation, ranked findings, root-cause hypotheses, confirmatory tests, and structured clinician-report assembly.
- The master gap is still the same across both source reports: **HealthIQ does not yet have the deterministic narrative asset and compiler stack** needed to turn those structured signals into pathway-led, body-wide, benchmark-grade narrative output.
- The most important confirmed gaps are:
  - no deterministic narrative compiler layer
  - no body-overview / panel-posture compiler
  - no lifestyle-to-pathway interpretation joins for key benchmark moves
  - no longitudinal raw-value and numeric-delta support for benchmark-style prose
  - no pathway-grade explainer assets
  - no functional-interpretation / confidence-narrative compiler
  - no governed methylation-first, protective-lipid, or cross-system vascular interpretation entities
  - no retail patient summary compiler

## 2. Source authorities used
- Benchmark narrative:
  - `docs/golden-narrative/AB_GOLD_STANDARD_NARRATIVE_REPORT_CHAT_2_FINAL.md`
- Reverse-engineering reports:
  - `docs/golden-narrative/AB_GOLD_STANDARD_NARRATIVE_REVERSE_ENGINEERING_CURSOR.md`
  - `docs/golden-narrative/AB_GOLD_STANDARD_NARRATIVE_REVERSE_ENGINEERING_CLAUDE.md`
- Final strategy:
  - `docs/golden-narrative/HealthIQ_Deterministic_Narrative_Sprint_Strategy_FINAL.md`

## 3. Merged reverse-engineering matrix
| Section / narrative move | Benchmark text summary | Required support type | Existing repo asset(s) | Exact file path(s) | Support status | Gap explanation | Required deterministic build implication | Likely owning sprint |
|---|---|---|---|---|---|---|---|---|
| Patient context as authoritative interpretation input | Age/sex, alcohol, fasting, weight loss, work pattern, sleep/stress, prior panel | Questionnaire SSOT; lifestyle registry; prior-panel support | Questionnaire and lifestyle capture exist; AB current/prior fixtures exist | `backend/ssot/questionnaire.json`; `backend/ssot/lifestyle_registry.yaml`; `backend/core/pipeline/questionnaire_mapper.py`; `backend/tests/fixtures/panels/ab_full_panel_with_ranges.json`; `backend/tests/fixtures/panels/ab_full_panel_with_ranges_test0.json` | FULL | The governed input fields needed for this case are present. The remaining gap is use in narrative compilation, not capture. | Reuse current input layer as authority for later narrative compilers. | `N-1`, then `N-4` |
| Retail patient summary block | Short lay summary of reassuring background, lead issue, secondary issue, next step | Retail summary compiler | No cross-system retail summary compiler exists; only biomarker-level explainer support | `backend/ssot/retail_explainer_v1/registry.yaml` | NONE | The repo does not have a retail-facing summary assembly layer. Biomarker educational explainer content is too narrow. | New retail patient summary compiler. | `N-6`, `N-8` |
| Body overview / overall panel posture | "Background physiology is calm"; not broad metabolic pressure | Cross-system narrative compiler; reassurance synthesis | Cluster/system/grouping and bounded reassurance infrastructure exist | `backend/ssot/clusters.yaml`; `backend/ssot/system_burden_registry.yaml`; `backend/core/analytics/balanced_systems_presentation_v1.py`; `backend/core/analytics/calibration_engine.py` | PARTIAL | The inputs exist, but no compiler assembles them into benchmark-grade body-overview or exclusionary posture prose. | New body-overview / panel-posture compiler. | `N-2`, `N-6`, `N-8` |
| Hierarchy of concern | One lead issue, one secondary issue, with explicit ordering logic | Deterministic ranking and arbitration | Ranking logic and clinician page-1 lead handling already exist | `backend/ssot/arbitration_registry.yaml`; `backend/core/analytics/report_compiler_v1.py`; `backend/core/contracts/report_v1.py`; `backend/core/contracts/clinician_report_v1.py` | FULL | The repo can deterministically rank and headline lead concerns. | Existing ranked outputs can be reused; later compiler only needs to narrate them better. | `N-2`, `N-8` |
| Why the lead leads / why the secondary does not | Explicit comparison across competing systems and signals | Comparative ranking explanation compiler | Deterministic ranking exists, but explanation prose does not | `backend/core/analytics/report_compiler_v1.py`; `backend/ssot/arbitration_registry.yaml`; `backend/ssot/clusters.yaml` | PARTIAL | Ranking exists, but there is no governed compiler for "why this leads over that" and "why this did not lead." | Add hierarchy-explanation narrative logic on top of ranked outputs. | `N-2`, `N-8` |
| Lead pattern identification | Homocysteine/red-cell size/methylation efficiency is the lead issue | Signal, root-cause, and interpretation entity alignment | Strong homocysteine signal and root-cause stack exists | `knowledge_bus/packages/pkg_homocysteine_elevation_context/signal_library.yaml`; `knowledge_bus/root_cause/hypotheses/hcy_hypotheses_v1.yaml`; `backend/tests/fixtures/reports/clinician_report_v1_ab.json` | PARTIAL | The signal stack is strong, but the governed interpretation entity is still not methylation-first. Current phenotype/IDL framing is more vascular/inflammation-led. | New methylation-first governed interpretation entity. | `N-5`, `N-7` |
| Lead pathway system biology | One-carbon metabolism, remethylation, transsulfuration, red-cell maturation | Pathway-grade explainer asset | Some pathway text exists in KB packages and investigation specs | `knowledge_bus/packages/pkg_homocysteine_elevation_context/signal_library.yaml`; `knowledge_bus/research/investigation_specs/inv_homocysteine_high_metabolic.yaml`; `knowledge_bus/interpretation_display_layer_v1/idl_records_v1.yaml` | PARTIAL | Mechanism text exists, but not as a governed narrative-grade prose asset for deterministic output. | New methylation / one-carbon pathway explainer asset. | `N-5` |
| Lead pathway marker evidence block | Markers carrying the pattern vs markers making it more reassuring | Root-cause evidence block compiler | Evidence-for / evidence-against structure already exists and is deterministic | `knowledge_bus/root_cause/hypotheses/hcy_hypotheses_v1.yaml`; `backend/core/analytics/root_cause_compiler_v1.py`; `backend/core/contracts/root_cause_v1.py` | FULL | Existing hypothesis evidence structures map directly to this narrative move. | Reuse current evidence block in later narrative output. | `N-8` |
| Functional reading label | "Not simple deficiency; incomplete pathway efficiency" | Functional-label compiler | Root-cause evidence supports this distinction, but not the benchmark phrasing | `knowledge_bus/root_cause/hypotheses/hcy_hypotheses_v1.yaml`; `backend/core/contracts/root_cause_v1.py` | PARTIAL | There is no governed functional interpretation label layer that converts evidence/ranking into "this is X, not Y" prose. | Add functional interpretation assets/compiler. | `N-6` |
| Confidence, limits, and clarifying tests | Moderate confidence; MMA/B6/repeat homocysteine would clarify | Confidence-narrative compiler; confirmatory test support | Evidence strength, missing data, and confirmatory tests already exist | `knowledge_bus/root_cause/hypotheses/hcy_hypotheses_v1.yaml`; `knowledge_bus/registries/confirmatory_tests_v1.yaml`; `backend/core/contracts/root_cause_v1.py` | PARTIAL | The structured ingredients exist, but the benchmark-style confidence prose layer does not. B6/P5P support is also incomplete in governed assets. | New confidence / uncertainty compiler and expanded clarifying-test coverage. | `N-6` |
| Monitoring relevance / what improvement would look like | Improvement and persistence criteria for the lead pathway | Monitoring criteria asset; resolution compiler | Transition codes exist per biomarker | `backend/core/analytics/state_transition_engine.py`; `backend/core/contracts/state_transition_v1.py`; `knowledge_bus/interventions/intervention_library_v1.yaml` | PARTIAL | The repo can track status changes, but not compile pathway-level "improvement would mean X / persistence would mean Y" criteria. | Add monitoring criteria schema and compiler. | `N-6`, `N-8` |
| Alcohol-to-pathway interpretation | Alcohol contributes to macrocytosis and one-carbon drag | Lifestyle-to-pathway deterministic join | Lifestyle data and some macrocytosis/alcohol context exist | `backend/ssot/lifestyle_registry.yaml`; `backend/core/analytics/lifestyle_modifier_engine.py`; `knowledge_bus/packages/pkg_kb52c_mcv_high_nonmegaloblastic_macrocytosis/signal_library.yaml` | PARTIAL | Alcohol currently joins mainly into hepatic burden, not the homocysteine / methylation interpretation pathway the benchmark needs. | New alcohol-to-methylation deterministic bridge. | `N-4` |
| Lipid system biology | LDL/HDL/ApoB/TG transport architecture explanation | Pathway-grade lipid explainer asset | Marker coverage and lipid hypotheses exist | `backend/ssot/biomarkers.yaml`; `knowledge_bus/root_cause/hypotheses/lipid_transport_dysfunction_hypotheses_v1.yaml`; `backend/ssot/retail_explainer_v1/registry.yaml` | PARTIAL | The repo has marker-level coverage, but not a governed system-biology narrative for lipid transport architecture. | New lipid transport pathway explainer asset. | `N-5` |
| Protective lipid context | Mild residual LDL exposure within a mostly protective transport profile | Multi-marker protective-context compiler; governed interpretation asset | All required lipid markers and ratios exist in SSOT/fixtures | `backend/ssot/biomarkers.yaml`; `backend/tests/fixtures/panels/ab_full_panel_with_ranges.json`; `knowledge_bus/packages/pkg_lipid_transport/signal_library.yaml` | PARTIAL | The marker set exists, but the protective-context framing is not encoded as a governed interpretation entity or compiler. | New protective lipid transport interpretation asset and compiler logic. | `N-5`, `N-7`, `N-8` |
| Cross-system vascular synthesis | Lipid context plus homocysteine context jointly shape vascular interpretation | Cross-system phenotype / chain asset | Separate homocysteine and lipid assets exist | `knowledge_bus/packages/pkg_homocysteine_elevation_context/signal_library.yaml`; `knowledge_bus/packages/pkg_lipid_transport/signal_library.yaml`; `knowledge_bus/phenotypes/phenotype_map_v1.yaml` | NONE | No governed phenotype or chain currently combines these two mechanisms into one vascular synthesis entity. | New cross-system vascular synthesis interpretation entity. | `N-7` |
| Longitudinal broad direction of travel | Overall trajectory is favourable and physiologically meaningful | Longitudinal narrative compiler | Prior-snapshot linking and transition codes exist | `backend/core/analytics/snapshot_linker.py`; `backend/core/analytics/state_transition_engine.py`; `backend/core/contracts/state_transition_v1.py` | PARTIAL | The repo can say whether markers improved/worsened, but not compile a benchmark-grade direction-of-travel narrative with physiological framing. | New longitudinal narrative compiler. | `N-3`, `N-8` |
| Longitudinal numeric deltas | "110 -> 87", "32 -> 26", etc. | Raw-value persistence and numeric-delta compiler | Current snapshots preserve status/score, not raw prior values | `backend/core/analytics/snapshot_linker.py`; `backend/core/contracts/insight_graph_v1.py` | NONE | This is a confirmed contract gap: benchmark-style numeric delta prose is impossible without raw prior-value preservation. | Explicit architectural decision plus contract upgrade for raw values and delta compilation. | `N-3` |
| Secondary systems worth noting | Iron, renal context, androgen context are relevant but not lead issues | Secondary-systems narrative compiler | Underlying signal/hypothesis support exists for these systems | `backend/ssot/clusters.yaml`; `backend/core/pipeline/questionnaire_mapper.py`; `knowledge_bus/interventions/intervention_library_v1.yaml`; `backend/ssot/biomarkers.yaml` | PARTIAL | Signals and groupings exist, but there is no "worth noting, not lead" narrative output layer. | Add secondary-systems narrative section compiler. | `N-8` |
| Practical next steps | Repeat HCY/CBC, clarify B-vitamin status, review alcohol, continue lipid monitoring, preserve glycaemic gains | Prioritised action compiler | Confirmatory-test and action scaffolding already exist | `knowledge_bus/registries/confirmatory_tests_v1.yaml`; `knowledge_bus/interventions/intervention_library_v1.yaml`; `backend/core/contracts/report_v1.py`; `backend/core/analytics/intervention_selector_v1.py` | PARTIAL | The structured actions exist, but not the benchmark's prioritised, cross-system, context-aware next-step narrative. | Extend action assembly into a prioritised next-steps compiler. | `N-6`, `N-8` |
| Clinician-style integrated summary | Concise final synthesis covering reassurance, lead pattern, secondary pattern, trend, and next step | Clinician synthesis compiler | Structured clinician-report contracts already exist | `backend/core/contracts/clinician_report_v1.py`; `backend/core/analytics/report_compiler_v1.py`; `backend/artifacts/golden_runs/20260405T085509Z/narrative.txt` | PARTIAL | The contract exists, but current compiled narrative quality is placeholder-level rather than benchmark-grade synthesis. | New richer clinician synthesis compiler. | `N-8` |

## 4. Approved deterministic gap categories
The merged/adjudicated gap categories for this workstream are:

1. **Data and contract gaps**
   - longitudinal raw prior/current value preservation
   - numeric delta support
   - safe contract decisions for trend narration

2. **Governed interpretation entity gaps**
   - methylation-first / homocysteine-macrocytosis interpretation entity
   - protective lipid transport context entity
   - cross-system vascular synthesis entity

3. **Governed narrative asset gaps**
   - pathway-grade explainers
   - functional interpretation labels
   - confidence / uncertainty phrasing
   - monitoring / resolution criteria
   - retail patient summary assets

4. **Compiler and assembly gaps**
   - body overview / panel-posture compiler
   - hierarchy explanation compiler
   - longitudinal narrative compiler
   - next-steps compiler
   - clinician synthesis compiler
   - retail summary compiler

5. **Lifestyle-to-interpretation bridge gaps**
   - alcohol -> methylation / macrocytosis
   - hydration -> renal context
   - weight loss / fasting -> glycaemic improvement context

6. **Display/output surfacing gaps**
   - surfacing already-strong structured evidence blocks
   - surfacing ranked findings, confirmatory tests, and reassurance outputs without overclaiming

## 5. Sprint linkage map
| Gap category | Intended sprint(s) |
|---|---|
| Benchmark lock / adjudicated authority | `N-1` |
| Narrative compiler architecture | `N-2` |
| Longitudinal raw-value and numeric-delta contract gap | `N-3` |
| Lifestyle-to-interpretation joins | `N-4` |
| Pathway-grade explainers and governed narrative assets | `N-5` |
| Functional labels, confidence phrasing, monitoring criteria, richer action framing | `N-6` |
| New governed interpretation entities (methylation-first, protective lipid, cross-system vascular) | `N-7` |
| Deterministic narrative compiler implementation and section outputs | `N-8` |
| Runtime benchmark validation against AB case | `N-9` |
| Serious frontend re-entry around stronger deterministic outputs | `N-10` |

## 6. Authority notes / ambiguities
- `backend/tests/fixtures/panels/ab_full_panel_with_ranges_test0.json` is clearly useful and benchmark-aligned, but it remains closer to a prior-panel fixture than to the formally named AB acceptance anchor in `backend/tests/fixtures/panels/panel_acceptance_profiles_v1.yaml`.
- The branch point between `N-5` and `N-7` matters: explanation assets should not get too far ahead of the governed interpretation entities they are meant to explain.
- `N-3` requires an explicit decision, not just implementation work: either preserve raw prior values in a safe contract or accept that benchmark-style numeric delta narration remains out of scope.
- The merged conclusion intentionally prefers the more precise Claude diagnosis on the confirmed longitudinal raw-value gap, while preserving Cursor’s stronger emphasis on methylation-first and protective-context interpretation-entity gaps.
