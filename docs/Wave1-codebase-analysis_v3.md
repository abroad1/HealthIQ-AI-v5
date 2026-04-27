 Here is the pre-remediation feasibility decision document:

  ---
  PRE-REMEDIATION FEASIBILITY INVESTIGATION — CLOSED

  ---
  1. Executive Answer

  A. Pipeline rerun feasibility

  Feasible with a small adapter/shim. The orchestrator does not require auth context, request models, DB sessions, or live upload objects. Two gaps exist —
  both are bridgeable without refactoring the pipeline.

  B. Snapshot versioning recommendation

  Option C — explicit schema version state, with Option B's audit safety built in. Add card_schema_version to ConsumerDomainScoreV1 (default "1.0");
  backfill writes "1.1". Old records are implicitly legacy; new records are unambiguous.

  C. Main blocker

  The orchestrator generates a new analysis_id internally at runtime (orchestrator.py:1006) — it must be made to accept the pre-existing stored ID,
  otherwise a rerun creates a new analysis record instead of correcting the existing one.

  ---
  2. Pipeline Entry-Point Analysis

  The entry path

  POST /start → backend/app/routes/analysis.py:173 → AnalysisOrchestrator().run() → backend/core/pipeline/orchestrator.py:966

  Orchestrator.run() signature

  run(
      biomarkers: Mapping[str, Any],
      user: Mapping[str, Any],
      *,
      assume_canonical: bool = False,
      lifestyle_inputs: Optional[Dict[str, Any]] = None,
      questionnaire_data: Optional[Dict[str, Any]] = None,
  )

  No auth token. No request context. No DB session. No upload object. The orchestrator is stateless with respect to request-time infrastructure.

  What is stored vs what is missing

  ┌─────────────────────────────────┬─────────┬─────────────────────────────┬────────────────────────────────────────────────────────────────┐
  │         Required input          │ Stored? │          Location           │                             Notes                              │
  ├─────────────────────────────────┼─────────┼─────────────────────────────┼────────────────────────────────────────────────────────────────┤
  │ biomarkers dict (lab values)    │ YES     │ Analysis.raw_biomarkers     │                                                                │
  ├─────────────────────────────────┼─────────┼─────────────────────────────┼────────────────────────────────────────────────────────────────┤
  │ questionnaire_data              │ YES     │ Analysis.questionnaire_data │                                                                │
  ├─────────────────────────────────┼─────────┼─────────────────────────────┼────────────────────────────────────────────────────────────────┤
  │ analysis_id                     │ YES     │ Analysis.analysis_id        │ But orchestrator generates its own — see blocker               │
  ├─────────────────────────────────┼─────────┼─────────────────────────────┼────────────────────────────────────────────────────────────────┤
  │ user_id                         │ YES     │ Analysis.user_id            │ Can reconstruct minimal user dict                              │
  ├─────────────────────────────────┼─────────┼─────────────────────────────┼────────────────────────────────────────────────────────────────┤
  │ __unit_normalisation_meta__ key │ NO      │ Not persisted               │ Must be re-applied via current apply_unit_normalisation()      │
  ├─────────────────────────────────┼─────────┼─────────────────────────────┼────────────────────────────────────────────────────────────────┤
  │ Normalised user dict            │ NO      │ Not persisted               │ Must be reconstructed from stored user_id + questionnaire_data │
  └─────────────────────────────────┴─────────┴─────────────────────────────┴────────────────────────────────────────────────────────────────┘

  The two gaps in detail

  Gap 1 — __unit_normalisation_meta__:
  The orchestrator validates at line 1002–1004 that this metadata key is embedded in the biomarkers dict. It is not persisted separately. However, it is not
   a data gap — it is a processing-step marker. The backfill adapter re-applies apply_unit_normalisation() to the stored raw_biomarkers using the current
  unit registry, which recreates it deterministically. If the unit registry version has changed since the original run, scores may differ slightly. The
  replay_manifest stored in each analysis records the original registry version hash, so version-drift can be detected and flagged.

  Gap 2 — analysis_id generation:
  Orchestrator line 1006 generates a fresh UUID. A backfill runner must pass the stored analysis_id as an override parameter — either via a constructor
  argument or a thin wrapper that patches the generated ID before the pipeline writes its output. This requires a 1-line change to the orchestrator, or a
  post-run ID substitution before the persistence call, but it does not require pipeline refactoring.

  Backfill rerun determinism

  Yes, with a caveat. The pipeline is deterministic: no LLM in the analytical core, no randomness, no external API calls in the scoring path. Given
  identical inputs and identical registry versions, it produces identical output. If registry versions have drifted since the original run, output will
  differ — but this is the correct behaviour (the backfill would produce the corrected narrative using current registry assets, which is the intent). The
  replay_manifest field in each stored result contains version hashes and can be used to flag any analyses where version drift is material.

  ---
  3. Minimum Backfill Execution Shape

  A thin dedicated backfill runner script — not a pipeline refactor.

  The runner would:

  1. Query all Analysis + AnalysisResult rows where consumer_domain_scores is present in the stored blob
  2. For each record: load raw_biomarkers, questionnaire_data, user_id, analysis_id from Analysis
  3. Re-apply unit normalisation to embed the required metadata key
  4. Reconstruct a minimal user dict from stored user_id and questionnaire_data
  5. Instantiate AnalysisOrchestrator and call run() with the stored inputs
  6. Intercept the returned DTO; extract only consumer_domain_scores (do not overwrite the rest of the stored blob)
  7. Set card_schema_version: "1.1" on each score object
  8. Write corrected consumer_domain_scores back into AnalysisResult.processing_metadata["client_result_shape_v1"]
  9. Log: analysis_id, old score hash, new score hash, registry versions used

  This runner does not touch the pipeline itself. It calls the pipeline as a black box and applies the corrected output surgically to the stored blob. The
  rest of the frozen snapshot (biomarkers, insights, narrative report, IDL bundle, etc.) is left untouched.

  ---
  4. Snapshot Versioning Policy Analysis

  Current blob structure (relevant to the decision)

  The stored client_result_shape_v1 blob already contains result_version: "1.0.0" — a top-level version field for the overall result shape. However it is
  not granular per feature, not queryable at the domain-score level, and not currently used by any conditional read-path logic. ConsumerDomainScoreV1 itself
   (results.py:166–238) has no version field; it is frozen=True, extra="forbid".

  Option A — Overwrite in place

  Strengths: Zero schema change. Simplest write. Single source of truth.

  Weaknesses: Destructive and unrecoverable. No audit trail of what was corrected. If the fix introduces a new bug, the original output is gone. Cannot
  validate corrected vs original on the same record. Violates the governance principle that analysis artefacts should be immutable once produced.

  Medical-grade risk: HIGH. For a product making health inferences, "we overwrote the original without record" is an untenable audit position.

  Verdict: Not appropriate for this product.

  ---
  Option B — Write corrected output to a new key

  Strengths: Non-destructive. Original preserved. Side-by-side comparison possible during validation. Read-path fallback is trivial (check new key, fall
  back to old).

  Weaknesses: Schema ambiguity — two keys with no semantic label saying which is authoritative. Storage bloat (every record carries both). Eventual cleanup
  requires a second migration. Clients must be updated to use the new key.

  Medical-grade risk: MEDIUM. Preserved audit trail is correct. But the dual-key ambiguity creates confusion in future debugging and governance reviews.

  Verdict: Safe but leaves schema debt.

  ---
  Option C — Explicit schema version state

  Strengths: Semantically unambiguous — the version field is the authoritative statement of which generation produced the data. Fully queryable: SELECT ...
  WHERE consumer_domain_scores @> '[{"card_schema_version": "1.1"}]' identifies all backfilled records. Non-destructive (old records implicitly carry "1.0"
  default). Scalable — future fixes increment the version without new keys. Governance-friendly — auditors can trace exactly which logic version produced
  each result.

  Weaknesses: Requires a model update to ConsumerDomainScoreV1 (add field with default). Because the model is frozen=True, extra="forbid", deserialization
  of old stored records will fail if the field is absent — requires a default value strategy (Field(default="1.0")). Read path requires no logic change
  initially (just serves what is stored), but must handle missing field on old records gracefully during transition.

  Medical-grade risk: LOW. This is the pattern used in the existing replay_manifest, cluster schema files, and calibration registries in this codebase. It
  is already the established governance idiom.

  Verdict: Correct for a deterministic governance product.

  ---
  Hybrid (recommended): Option C as primary, Option B's audit safety retained

  During the backfill window: preserve the original consumer_domain_scores as consumer_domain_scores_legacy (one additional key, temporarily). Once the
  backfill is validated and signed off, the legacy key can be dropped in a subsequent cleanup migration. This gives Option C's semantic clarity plus Option
  B's rollback safety during the correction window, without making the dual-key state permanent.

  ---
  5. Recommended Policy

  Option C with a temporary legacy key during the backfill validation window.

  - Add card_schema_version: str = Field(default="1.0") to ConsumerDomainScoreV1
  - Old stored records deserialise cleanly (default fills the missing field)
  - Backfill runner writes corrected scores with card_schema_version: "1.1"
  - During backfill window: old scores preserved as consumer_domain_scores_legacy key
  - Read path serves consumer_domain_scores as before — no change needed at launch
  - After backfill is validated: drop consumer_domain_scores_legacy in a cleanup pass
  - Governance query: any record with card_schema_version != "1.1" has not yet been backfilled

  Why not Option A: Destructive, no audit trail, wrong governance posture for a medical product.
  Why not pure Option B: Schema ambiguity, dual-key maintenance burden, no semantic version label.
  Why Option C wins: It is already the governance idiom in this codebase. It makes version state explicit, queryable, and immutable. It costs one model
  field and one default value.

  ---
  6. Operational Rollout Implication

  The remediation package must include all four of the following — they are not separable:

  1. Model update (ConsumerDomainScoreV1): add card_schema_version field with default "1.0". Deploy first, ahead of the fix, to ensure old records
  deserialise safely.

  2. Architecture correction (domain_narrative_wave1.py, domain_score_assembler.py): the primary pattern anchor fix and any "What's driving this" authority
  alignment. All new analyses post-deployment automatically receive corrected output tagged "1.1".

  3. Backfill runner: a standalone script that reruns the corrected pipeline against stored raw_biomarkers + questionnaire_data for each existing
  AnalysisResult, writes corrected consumer_domain_scores tagged "1.1", and preserves originals as consumer_domain_scores_legacy during the validation
  window.

  4. Backfill validation gate: before dropping legacy data, confirm that a representative sample of backfilled records produce coherent narratives (headline
   and consequence tell the same story), and that no score regressions are introduced for analyses where the underlying signals have not changed.

  A code-fix-only deployment is insufficient and produces a permanent two-tier result quality state. All four components must ship together as one governed
  package.

  ---
  7. Recommended Next Move

  All prerequisite questions are now closed. The remediation sprint can be written.

  The sprint should be scoped as a single MIXED work package (per SOP change_type: MIXED) covering:

  - Behavioural change: architecture correction to domain_narrative_wave1.py and domain_score_assembler.py
  - Content change: ConsumerDomainScoreV1 model update (new field)
  - Infrastructure: backfill runner script
  - Read-path: optional version-aware handling if needed

  Before the prompt is authored, GPT should confirm: does the "What's driving this" authority unification belong in this same sprint, or is it scoped
  separately? That decision determines whether this is one sprint or two. The narrative assembly fix and the backfill are inseparable. The driving-signal
  authority fix may or may not be.

  That scoping decision is the next governance action.
