# LC-S16 — Knowledge Asset Frontend-Surface Audit

**Work package:** LC-S16-17-19  
**Branch:** `scaffold/lc-s16-17-19-kb-surface-payload-contract`  
**Date:** 2026-05-23

## 1. Executive verdict

**PASS WITH GAPS**

Visible consumer results are predominantly traceable to governed DTO fields (clinician report, narrative report, IDL bundle, domain scores, biomarker rows). Gaps: full `meta.insight_graph` exposure, hero/body frontend derivation chains, and KB-S52+ packages not reflected in governance inventory (runtime-loaded but estate inventory stale).

**STOP / rescope:** Not triggered. Majority of content is not generic-only fallback; contract hardening does not require breaking DTO renames in this sprint.

## 2. Sources inspected

| Source | Path |
|--------|------|
| Results page | `frontend/app/(app)/results/page.tsx` |
| Results components | `frontend/app/components/results/**` |
| Layout / shaping | `frontend/app/lib/resultsPageLayout.ts`, `bodyOverviewPrimarySentence.ts`, `primaryFindingShaping.ts`, `retailNarrativeSanitize.ts` |
| Types | `frontend/app/types/analysis.ts` |
| Fetch | `frontend/app/queries/analysisResult.ts`, `frontend/app/services/analysis.ts` |
| DTO builder | `backend/core/dto/builders.py` |
| API route | `backend/app/routes/analysis.py` |
| Compilers | `report_compiler_v1.py`, `root_cause_compiler_v1.py`, `narrative_report_compiler_v1.py`, `interpretation_display_layer_publish_v1.py` |
| KB runtime | `backend/core/analytics/signal_evaluator.py` (`SignalRegistry`) |

## 3. Representative outputs reviewed

- AB full panel with ranges (`backend/tests/fixtures/panels/ab_full_panel_with_ranges.json`) via `AnalysisOrchestrator` (homocysteine lead family preserved).
- Static inspection of results page render tree and DTO field references.

## 4. Frontend section map

| Frontend section | Visible content summary | DTO/API field | Runtime source | Classification | Evidence | Notes |
|---|---|---|---|---|---|---|
| Hero / primary finding | Lead concern headline + summary | `clinician_report_v1.sections.page1.primary_concern`, `interpretation_display_layer_v1.records[]`, `narrative_report_v1` (IDL wins in `buildPrimaryHeroSummary`) | `compile_clinician_report_v1` ← `meta.insight_graph.report_v1`; IDL publish; narrative compiler | Governed DTO + governed IDL; hero assembly **frontend-derived** | `resultsPageLayout.ts`, `builders.py` L49–54 | Fallback title `'Your analysis summary'` when all sources empty |
| What's driving this | Up to 3 marker rows | `biomarkers[]`, `meta.wave1_aligned_drivers.biomarker_keys` | Orchestrator biomarker rows; meta wave1 alignment | DTO-backed; interpretation lines may be boilerplate | `page.tsx` L203–204, `ResultsDrivingSignals` | Status-based one-liner fallback |
| Body overview | Primary paragraph | `narrative_report_v1.body_overview`, `clinician_report_v1.sections.page1` | Narrative compiler + clinician compile | Governed DTO; frontend primary sentence merge | `ResultsBodyOverview.tsx` | `BODY_OVERVIEW_FALLBACK_PRIMARY` constant |
| Domain cards (Wave 1) | Three domain score cards | `consumer_domain_scores[]` | `assemble_consumer_domain_scores_v1` + domain narrative | Governed DTO (sentences from backend) | `Wave1DomainCards.tsx` | Hidden if empty |
| Interpretation / pattern cards | Pattern cards Section 5 | `interpretation_display_layer_v1.records[]` | `publish_interpretation_display_layer_v1` ← KB IDL YAML | **Governed Knowledge Bus asset** (IDL) | `InterpretationPatternsSection.tsx` | Filtered by `enabled_for_frontend` |
| Long-form WHY | Lead + secondary narratives | `narrative_report_v1.lead_narrative`, `secondary_narratives` | Layer C compilers + LC-S3 assembly | Governed DTO (deterministic narrative) | `NarrativeLeadAndSupportingSections` | Homocysteine path guarded by `test_narrative_compiler_why_surface_regression` |
| Why this lead won | Runner-up / co-primary lines | `clinician_report_v1.sections.page1` | Clinician report compile | Governed DTO | `WhyThisLeadWonSection.tsx` | |
| Clinician / advanced | Full report, dials, insights | `clinician_report_v1`, `biomarkers[]`, `insights[]`, `meta.insight_graph` | Compile-on-read + orchestrator | DTO-backed; **meta.insight_graph** is internal-heavy | `ClinicianReportRenderer`, Advanced disclosure | Technical detail gated by `showDetails` |
| Biomarker dials | Numeric dials + explainers | `biomarkers[]` | Scoring + display enrichment (LC-S8G) | DTO-backed | `BiomarkerDials` | `patternRelevanceLine` is frontend-derived |
| Uploaded-panel fidelity | Upload unit rows | `meta.upload_panel_observations`, `meta.display_unit_policy` | Orchestrator meta (LC-S8G) | Governed DTO metadata | `UploadedPanelFidelity` | |
| Next steps | Narrative + action cards | `narrative_report_v1.next_steps_narrative`, `recommendations[]`, cluster recommendations | Narrative compiler + orchestrator | Governed DTO + DTO list | `ResultsActionCardsBlock` | Deduped in frontend |
| Trust / data-quality strip | Panel completeness caveats | `clinician_report_v1.data_quality`, `sections.confirmatory_tests` | Clinician report compile | Governed DTO | `PipelineStatus` | Empty-state copy if missing |
| Balanced systems | System health summary | `balanced_systems_v1` | `compile_balanced_systems_v1` | Governed DTO (compile-on-read) | `BalancedSystemsSummary` | |
| Mock / LLM disclosure | Honesty banner | `meta.narrative_runtime` | Orchestrator meta | Display metadata | `narrativeRuntimePresentation.ts` | Not clinical claim |

## 5. Governed asset-backed sections

- `interpretation_display_layer_v1` (IDL records from `knowledge_bus/interpretation_display_layer_v1/`).
- Narrative sections backed by KB pathway/functional assets via `narrative_report_compiler_v1`.
- Signal-driven copy in domain cards (`why_it_matters` resolution in `domain_narrative_wave1.py`).
- Root-cause hypotheses in clinician report (`knowledge_bus/root_cause/hypotheses/`).

## 6. DTO-backed but generic/boilerplate sections

- Hero severity label defaults (`'Review in context'`, `'moderate'`).
- Driving-marker interpretation when `interpretation` and explainer body absent (status boilerplate).
- Empty trust strip: fixed “No data-quality summary…” string.

## 7. Fallback-backed sections

- Hero title `'Your analysis summary'` and generic hero body when IDL + clinician + narrative exhausted.
- Body overview `BODY_OVERVIEW_FALLBACK_PRIMARY` when no compiled/page1 text.

## 8. Frontend-derived sections

- `resultsPageLayout.ts`: hero title/body precedence, primary driver pick, action card dedupe.
- `SystemUnderstandingSection`: prose from clusters + balanced systems (no new API fields).
- `biomarkerPatternRelevance.ts`: dial relevance lines.

## 9. Unsupported / contradictory / internal-leak sections

- **Risk:** `meta.insight_graph` exposed on consumer payload (advanced section / debugging). Classified internal-only for retail; not stripped in this sprint.
- **Mitigated:** `slug_leakage` and LC-S11A guards for `signal_*` in domain sentences and sprint strings.
- No evidence of unsupported clinical claims beyond governed compilers on AB baseline.

## 10. Knowledge Bus assets not surfaced despite being available

- Many `pkg_kb52c_*` / `pkg_kb58_*` packages on disk are runtime-loaded via `SignalRegistry` but absent from `package_estate_KB-S49_v1.yaml` inventory (estate drift — see LC-S17 §13).
- PSI-rich packages without matching IDL records do not appear as pattern cards until IDL publish maps them.

## 11. DTO fields consumed by frontend

`analysis_id`, `biomarkers`, `clusters`, `insights`, `status`, `created_at`, `overall_score`, `meta` (partial), `clinician_report_v1`, `balanced_systems_v1`, `interpretation_display_layer_v1`, `narrative_report_v1`, `consumer_domain_scores`, `recommendations`, `risk_assessment`, `replay_manifest`, `primary_driver_system_id`, `derived_markers`.

## 12. DTO fields present but not surfaced

- `intervention_annotations_v1` (passthrough; limited retail surfacing).
- `system_capacity_scores`, `burden_hash` (engine context; advanced/debug).
- Full `meta.insight_graph.report_v1` (internal analytical truth; partial indirect surfacing via compile-on-read).

## 13. Implications for LC-S17

- Need lifecycle state `runtime-loaded` vs inventory `validated` separation.
- Orphan reporting required when disk packages exceed governance inventory (machine reporter added).

## 14. Implications for LC-S19

- Protect root keys via `frontend_contract_v1.FRONTEND_CONSUMED_ROOT_KEYS`.
- Classify `meta.insight_graph` as internal-only for consumer-safe subset (future Gemini-safe payload).

## 15. STOP / rescope recommendation

**Do not STOP.** Proceed to LC-S17 framework and LC-S19 contract classification. Defer inventory refresh and meta graph trimming to LC-S18.
