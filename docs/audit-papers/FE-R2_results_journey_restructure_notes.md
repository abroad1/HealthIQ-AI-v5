# FE-R2 — Results Journey Restructure Notes

**work_id:** FE-R2  
**branch:** `frontend/fe-r2-results-journey-restructure`  
**SOP:** AUTOMATION_BUS v1.3.1

## 1. Preflight results

| Check | Result |
|-------|--------|
| Branch | `frontend/fe-r2-results-journey-restructure` |
| Stash | empty |
| Kernel | `FE-R2` STARTED / IN_PROGRESS |
| Working tree at start | clean after `chore(bus): FE-R2 work package prompt and hardening` |

## 2. FE-R1 merge confirmation

| Evidence | Result |
|----------|--------|
| `dcd6ff7` on `main` ancestry | FE-R1 merged |
| `test_fe_r1_consumer_prose_cleanup.py` | present, passes |
| FE-R1 notes + Sentinel classes | present |

## 3. Page structure before change

Top-to-bottom (retail flow):

1. Hero + retail summary card  
2. What's driving this  
3. Wave1 domain cards  
4. Balanced systems  
5. Pipeline status  
6. Open **What this means** accordion (body overview, patterns, uncertainty, narratives, primary finding buried inside)  
7. Collapsed Actions accordion  
8. Collapsed Advanced accordion (biomarker dials, clinician report)

## 4. Implemented FE-R2 section order

1. **Your body overview** — framing, hero, body overview, retail summary  
2. **What's working well** — `balanced_systems_v1`  
3. **Primary finding and why** — `PrimaryFindingAndWhy`  
4. **Why this lead won / uncertainty** — `WhyThisLeadWonSection` + `PipelineStatus`  
5. **Marker-level evidence** — driving signals + `BiomarkerDials` + upload fidelity  
6. **What to do next** — longitudinal/next steps + action cards  
7. **Clinician summary** — collapsed disclosure with `ClinicianReportRenderer`

Secondary (collapsed): pattern cards + domains; additional interpretation context; advanced analysis.

## 5. Frontend files changed

- `frontend/app/(app)/results/page.tsx` — journey restructure  
- `frontend/app/lib/feR2ResultsJourneyOrder.ts` — canonical test-id order  
- `frontend/app/components/results/ResultsBodyOverview.tsx` — default heading “Your body overview”

## 6. DTO fields per section

| Section | Primary DTO / API fields |
|---------|---------------------------|
| Body overview | `narrative_report_v1.body_overview`, `clinician_report_v1.sections.page1`, `interpretation_display_layer_v1`, hero from IDL + report |
| Working well | `balanced_systems_v1` |
| Primary finding | `clinician_report_v1.sections.page1`, `root_cause` |
| Uncertainty | `runner_up_*`, `confidence_and_missing_data`, `data_quality` |
| Marker evidence | `biomarkers[]` display fields, upload fidelity meta |
| Next steps | `narrative_report_v1.next_steps_narrative`, actions |
| Clinician summary | `clinician_report_v1`, `narrative_report_v1.clinician_synthesis` |

## 7. Sections moved / demoted

| Section | Disposition |
|---------|-------------|
| Wave1DomainCards | Demoted → “Pattern cards and health domains” (collapsed) |
| ResultsInvestigationSpine | Demoted → additional context |
| SystemUnderstandingSection | Demoted → additional context |
| InterpretationPatternsSection | Demoted → pattern cards disclosure |
| NarrativeLeadAndSupportingSections | Demoted → additional context |
| BiomarkerDials | **Moved** to main journey §5 |
| Actions | **Moved** into §6 (not separate hidden accordion) |
| ClinicianReportRenderer | **Moved** to §7 clinician disclosure |
| Open “What this means” accordion | **Removed** from main flow |

## 8. Not changed

- Backend narrative compilers / scoring / units / pipeline  
- Knowledge Bus packages  
- Clinical interpretation logic in frontend  
- Phase 2 full patterns layer  
- Broad visual redesign  

## 9. Tests added/updated

- `backend/tests/regression/test_fe_r2_results_journey_restructure.py` (new)  
- FE-R1 and scaffold guards re-run (pass)

## 10. Sentinel updates

Added to `escaped_defects_v1.json`: `retail_results_journey_wrong_order`, `body_overview_not_first`, `working_well_section_missing_or_late`, `biomarker_evidence_hidden_in_advanced_only`, `clinician_language_in_retail_flow`, `results_page_accordion_dominated`, `duplicate_what_this_means_heading`.

## 11. Browser / UAT

Not performed in this session (no authenticated local browser session verified). Residual: manual UAT on `results?analysis_id=…` recommended before merge.

## 12. Residual risks

- Long narrative blocks remain in collapsed “Additional interpretation context”  
- Hero + retail summary + body overview may still feel dense (FE-R3 polish)  
- Domain cards demoted but not removed  

## 13. Recommendation for FE-R3

Focus on marker education expansions, contribution context, and progressive disclosure within §5 without re-opening backend compilers or journey order.
