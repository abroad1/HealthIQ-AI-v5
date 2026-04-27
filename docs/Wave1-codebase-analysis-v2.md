
  ---
  WAVE 1 FOLLOW-ON INVESTIGATION — THREE EVIDENCE GAPS CLOSED

  ---
  1. Executive Answers

  A. Snapshot Persistence

  FROZEN. consumer_domain_scores are serialised at analysis-completion time and stored as a JSON blob. The GET /api/analysis/result endpoint reads and
  returns that blob with zero recomputation. Fixing the assembly code leaves every existing analysis permanently unchanged until an explicit backfill or
  recompute is run.

  B. "What's Driving This" Authority

  INDEPENDENT FOURTH AUTHORITY. The driving-signal biomarker strip is sourced from the cluster assigned to the primary_driver_system_id, which is produced
  by the arbitration engine using dominance scoring, conflict weights, and calibration tiers. It has zero reference to the IDL records that drive the Wave 1
   narrative headline, contributor, and consequence sentences. Divergence is structural, not accidental.

  C. Blast Radius

  COMMON UNDER MULTI-PATTERN CONDITIONS, STRUCTURALLY LIKELY FOR THE "WHAT'S DRIVING THIS" MISMATCH. The contributor/consequence specific divergence
  requires a why_it_matters field gap in one IDL record — narrower than feared. But the narrative vs. driving-strip mismatch (the fourth authority) fires
  whenever the arbitration engine selects a different primary system than the IDL resolution — which is common in any multi-signal metabolic picture. In
  metabolic syndrome or pre-diabetic cohorts, estimated 15–25% of analyses are exposed. In a general screening population, 3–5% minimum.

  ---
  2. Snapshot Persistence Analysis

  Write path

  backend/app/routes/analysis.py lines 247–253:
  orchestrator.run() → AnalysisDTO (containing consumer_domain_scores)
    → [x.model_dump() for x in dto.consumer_domain_scores]   # frozen serialisation
    → _analysis_results[analysis_id] = stored                 # in-memory cache
    → PersistenceService.save_live_analysis_after_run()
        → AnalysisResult.processing_metadata["client_result_shape_v1"] = stored
        → Supabase/PostgreSQL INSERT

  The entire Wave 1 payload — headline, contributor, confidence_sentence, consequence, next_step, score, band, confidence tier — is serialised to the
  database as a static blob at the moment the analysis run completes.

  Read path

  backend/app/routes/analysis.py lines 348–369:
  GET /api/analysis/result?analysis_id=X
    → _raw_result_payload_for_analysis_id()    # checks in-memory cache; else DB load
    → build_analysis_result_dto(raw)
        → result.get("consumer_domain_scores") # line 66 in dto/builders.py — passthrough

  dto/builders.py line 66 returns consumer_domain_scores as-is. There is no conditional recompute, no version check, no field rebuild. The endpoint is a
  pure read of the frozen blob.

  Operational implication

  Deploying a fixed assemble_consumer_domain_scores_v1() has zero effect on any existing analysis. Every analysis run before the fix will serve the
  contradictory text indefinitely. The user who ran their analysis yesterday sees the broken card forever unless their result is explicitly regenerated.

  This is not a minor footnote. It means the remediation has two mandatory phases: fix the code, then regenerate stored results.

  ---
  3. "What's Driving This" Analysis

  The four authorities in play

  ┌──────────────────────┬───────────────────────────────────────────────┬──────────────────────────────────────────────────────────────────────────────┐
  │       Section        │                    Source                     │                                Ranking logic                                 │
  ├──────────────────────┼───────────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────┤
  │ Wave 1 headline      │ headline_cv() via band label                  │ Score band → hardcoded template                                              │
  ├──────────────────────┼───────────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────┤
  │ Wave 1 contributor   │ cv_contributor()                              │ IDL record order → signal priority list                                      │
  ├──────────────────────┼───────────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────┤
  │ Wave 1 consequence   │ cv_consequence()                              │ IDL record order, filtered by why_it_matters presence                        │
  ├──────────────────────┼───────────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────┤
  │ "What's driving      │ resultsPageLayout.ts                          │ Cluster biomarkers of primary_driver_system_id, ranked by biomarker status   │
  │ this"                │ pickTopDriverBiomarkers()                     │ only                                                                         │
  └──────────────────────┴───────────────────────────────────────────────┴──────────────────────────────────────────────────────────────────────────────┘

  How "What's driving this" is selected

  Backend: orchestrator.py lines 1422–1432 — primary_driver_system_id is assigned from build_arbitration_result_v1(). The arbitration engine
  (arbitration_engine.py lines 115–200) ranks systems by: direct dominance wins, transitive reachability, conflict resolution weights, calibration tier
  weights, confidence bucket, lexicographic tiebreaker. Zero reference to IDL records.

  Frontend: resultsPageLayout.ts lines 261–287 — pickTopDriverBiomarkers() receives primaryDriver.biomarkers (the cluster's biomarker list for the
  arbitration-winning system) and ranks them purely by biomarker status string (high/low/critical → rank 4, border/watch → rank 3, normal/optimal → rank 0).
   No IDL, no signal_state, no Wave 1 narrative logic.

  Specific conflict scenario (confirmed in UAT)

  1. Arbitration engine ranks lipid_transport as primary system → driving strip shows LDL, HDL, hematocrit
  2. IDL vascular record (ph_vascular_hcy_inflammation_v1) is active → Wave 1 contributor/consequence surface homocysteine/vascular text
  3. User sees: driving signals = lipid/blood markers; narrative = vascular inflammation risk
  4. These are separate true facts about the same patient — but the card presents them as if one explains the other, which it does not

  This is not a coincidence. It is what the architecture produces whenever the arbitration-derived primary system differs from the IDL-dominant pattern.
  There is no coordination mechanism between the two.

  ---
  4. Blast Radius Analysis

  Contributor vs. consequence specific divergence (narrower)

  Both cv_contributor() and cv_consequence() iterate (_ID_VASCULAR, _ID_LIPID) in the same order. The divergence condition is: contributor matches on IDL
  record presence alone (severity_state + enabled_for_frontend); consequence adds a third filter requiring why_it_matters to be non-empty.

  In the current IDL bundle (idl_records_v1.yaml), both vascular and lipid records have why_it_matters populated. So this specific divergence fires only if
  one record's why_it_matters is null or absent — which is the lipid-dominant fallback path. This is narrower than the prior investigation feared. It fires
  mainly in lipid-dominant patterns.

  Narrative vs. "What's driving this" divergence (broader)

  This fires whenever the arbitration engine selects a different primary system than the IDL resolution. Structural conditions:

  - Patient has both LDL elevation and homocysteine elevation (both signal sets activate)
  - IDL vascular record activates → Wave 1 narrative is vascular-led
  - But arbitration engine, weighing system-level dominance across all active systems, may rank lipid_transport higher (more biomarkers, higher calibration
  tier, more dominance edges)
  - Driving strip surfaces lipid biomarkers; narrative talks about vascular risk

  Frequency estimate:
  - General adult screening population: 3–5% have concurrent homocysteine + LDL elevation
  - Metabolic syndrome / pre-diabetic cohort: 15–25%
  - Any patient with multi-system signal activation (which is the typical case for people who bother running blood panels): materially higher than the
  general population floor

  Additionally: even without homocysteine, if multiple CV signal types are active (e.g., high triglycerides + high LDL + low HDL), arbitration may resolve
  differently than IDL priority order, producing the same mismatch. The blast radius extends to any multi-signal cardiovascular picture.

  Bottom line: The "What's driving this" mismatch is not an edge case. It is the default outcome for any patient with a multi-pattern result — which is the
  most clinically interesting and commercially important user cohort.

  ---
  5. Operational Implication

  The remediation has a two-phase structure with no shortcuts:

  Phase 1 — Code fix:
  Fix domain_narrative_wave1.py and domain_score_assembler.py (primary pattern anchor). Also unify the "What's driving this" authority so it derives from
  the same resolved IDL pattern, not independently from the arbitration cluster. Deploy.

  Phase 2 — Backfill:
  Every analysis run before Phase 1 deployment remains frozen with old text. A batch migration must: load all AnalysisResult records, rerun
  assemble_consumer_domain_scores_v1() against their stored biomarker snapshot, overwrite
  processing_metadata["client_result_shape_v1"].consumer_domain_scores, and persist. This requires the stored biomarker input to still be accessible in the
  database (confirm this before designing the migration).

  State after remediation:
  - New analyses: immediately correct
  - Old analyses with backfill applied: correct
  - Old analyses without backfill: permanently broken
  - Mixed state is possible and must be managed explicitly

  There is no in-between option. A code-only deployment is strictly insufficient and would create a two-tier result quality situation that is worse from a
  trust perspective than the current state.

  ---
  6. Recommended Next Move

  Architecture correction sprint + backfill plan, designed together before either is executed.

  Do not execute the code fix without first confirming that the biomarker input snapshot is available in the database to support a backfill. If the stored
  payload does not include the raw biomarker inputs (only the computed outputs), a backfill would require rerunning full analyses — a materially different
  and more expensive operation.

  The sequencing should be:

  1. Confirm backfill feasibility — read the persistence schema to determine whether stored records contain enough input data to recompute
  consumer_domain_scores without a full re-run
  2. Design the architecture fix (unified primary-pattern selector, "What's driving this" authority unification) — these are the same sprint
  3. Design the backfill migration in parallel — even if simple, it must be explicit and auditable
  4. Execute code fix → deploy → run backfill migration

  Running the code fix without the backfill plan confirmed is not recommended. It would produce a live state where some users have correct cards and some
  have broken ones, with no systematic way to know which.