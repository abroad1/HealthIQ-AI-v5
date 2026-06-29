---
work_id: P3-PROSE-DEPTH-1
branch: feature/p3-prose-depth-1-prose-library-depth-modifier-schema
risk_level: STANDARD
execution_model: SINGLE_PHASE
change_type: CONTENT
---

# P3-PROSE-DEPTH-1 — Prose Library Depth and Modifier Schema Sprint

You are Cursor, acting as implementation agent for HealthIQ AI under the standard Automation Bus and Knowledge Bus governance rules.

This is a STANDARD / CONTENT sprint.

This sprint must create the governed foundations for scalable prose-library population.

It must not activate Gemini, modify runtime behaviour, bind modifiers at runtime, change Intelligence Core logic, or promote candidate prose into production assets.

## Sprint purpose

HealthIQ AI needs a scalable, governed prose library that supports personalised marker-level and system-level explanation without creating an unmaintainable bespoke-paragraph monster.

The architecture review `DYNAMIC-PROSE-ARCH-1` concluded:

* HealthIQ should use **hybrid minimum viable composition**;
* do not build a new composition engine;
* do not build thousands of bespoke prose paragraphs;
* use the existing `NarrativePayloadV1` / `NarrativeReportV1` path;
* extend the existing governed asset model with content depth, modifier fragments, MR candidate asset schema, review status, destination mapping and compile/promotion discipline;
* MR LLM assets must remain candidate assets until reviewed and promoted.

This sprint creates the content-factory foundations.

It does not populate production runtime prose directly.

## Product output

At completion, the repo should contain:

1. a governed MR candidate prose asset schema;
2. an illustrative MR candidate asset template;
3. a prose asset coverage matrix for beta/launch-core coverage;
4. a first MR work-batch brief for candidate prose generation;
5. modifier prose fragment authoring templates for high-value lifestyle/medication/supplement modifier classes;
6. sprint artefacts documenting what exists, what is missing, what is candidate-only, and what requires medical review;
7. no runtime activation of new prose, modifiers, Gemini, or frontend behaviour.

## Controlling authority and source reads

This sprint must not re-run the architecture review.

Use `DYNAMIC-PROSE-ARCH-1` as the primary architecture authority. It already concluded that HealthIQ should use hybrid minimum viable composition and extend the existing governed prose path rather than build a new composition engine.

### Mandatory authority reads

1. `docs/planning-papers/DYNAMIC-PROSE-ARCH-1_dynamic_personalised_prose_architecture_review.md`
2. `docs/planning-papers/PROSE-INVENTORY-1_prose_library_prose_to_ux_architecture_inventory_review.md`, if present
3. `docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md`
4. `docs/sprints/beta_readiness/P2-2_P2-3_retail_pathway_explainer_completion.md`
5. `docs/sprints/beta_readiness/P2-4_narrativepayload_brief_hardening_completion.md`

### Mandatory asset/source reads for the coverage matrix

6. `backend/ssot/retail_explainer_v1/registry.yaml`
7. `knowledge_bus/pathway_explainers_v1/pathway_explainers_v1.yaml`
8. `knowledge_bus/missing_marker_explainers_v1/missing_marker_explainers_v1.yaml`
9. `knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml`, if present
10. `knowledge_bus/interventions/intervention_effects_registry_v1.yaml`, if present

### Optional reference only if needed for boundary clarification

* `docs/architecture/ADR_WP2_layer_b_layer_c_contract_path_b.md`
* `docs/architecture/ADR-LAYER-BOUNDARY-RECONCILIATION-1.md`
* `docs/sprints/beta_readiness/P2-1_prose_substrate_wave1_wired_completion.md`
* `docs/architecture/RETAIL_EXPLAINER_CONTENT_BOUNDARIES_v1.md`
* `docs/intelligence/DOMAIN_NARRATIVE_CONTRACT_WAVE1.md`

Do not expand this into another architecture review.

## Core principle

The prose model is hybrid minimum viable composition:

`base explainer + signal/frame explainer + pathway explainer + additive modifier fragment + missing-marker caveat + resilience/caution qualifier`

Do not create bespoke paragraphs for every age/sex/result/lifestyle/medication/supplement combination.

Do not create sex-specific or age-specific assets unless `DYNAMIC-PROSE-ARCH-1`, existing medical governance, or later medical review justifies that the axis materially changes interpretation, not merely the reference range.

## Scope

This sprint is allowed to create or update documentation, schema, candidate templates, coverage matrices and sprint artefacts only.

Expected new files:

1. `docs/sprints/beta_readiness/P3-PROSE-DEPTH-1_prose_library_depth_modifier_schema_completion.md`
2. `docs/sprints/beta_readiness/P3-PROSE-DEPTH-1_manifest.yaml`
3. `docs/sprints/beta_readiness/P3-PROSE-DEPTH-1_carry_forward.yaml`
4. `docs/sprints/beta_readiness/P3-PROSE-DEPTH-1_prose_coverage_matrix.yaml`
5. `docs/sprints/beta_readiness/P3-PROSE-DEPTH-1_mr_candidate_asset_schema.yaml`
6. `docs/sprints/beta_readiness/P3-PROSE-DEPTH-1_mr_candidate_asset_template.yaml`
7. `docs/sprints/beta_readiness/P3-PROSE-DEPTH-1_mr_batch_001_brief.md`
8. `docs/sprints/beta_readiness/P3-PROSE-DEPTH-1_modifier_fragment_templates.yaml`
9. update `docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md`

If the repo already has a better canonical location for candidate prose schemas or planning artefacts, use that location instead, but record the decision in the manifest.

## Out of scope

Do not modify:

* runtime loaders;
* signal evaluators;
* scoring policy;
* domain assembler;
* root-cause compiler;
* `narrative_payload_builder_v1.py`;
* `narrative_report_compiler_v1.py`;
* `narrative_compiler_lc_s3_assembly_v1.py`;
* `NarrativePayloadV1`;
* `NarrativeReportV1`;
* frontend files;
* Gemini files;
* prompt templates;
* production PSI packages;
* compiled health-system cards;
* production signal libraries;
* production retail explainer registry;
* production pathway explainers;
* production missing-marker explainers;
* production context modifier catalogue;
* production intervention effects registry;
* parser files;
* questionnaire files;
* `.codex/`;
* `.cursor/`;
* `.vscode/`;
* `AGENTS.md`.

No runtime behaviour change is authorised.

No production asset promotion is authorised.

No Gemini activation is authorised.

No context modifier runtime binding is authorised.

No medical claim should be promoted as approved content in this sprint.

## Phase 0 — Automation Bus preflight

Before modifying files:

1. Confirm current branch is:

`feature/p3-prose-depth-1-prose-library-depth-modifier-schema`

2. Confirm `automation_bus/state/work_package_active.json` exists.
3. Confirm active token has `work_id: P3-PROSE-DEPTH-1`.
4. Confirm active token branch matches current branch.
5. Confirm repo/stash/parked-file state is governed.
6. Confirm P2-4 is merged.
7. Confirm no P4-1 implementation is running in parallel.
8. Confirm this sprint is CONTENT-only.

STOP if preflight fails.

## Phase 1 — Inventory existing prose assets

Create a coverage matrix that identifies existing, partial, missing and deferred prose asset coverage.

Do not rewrite existing assets.

Do not duplicate existing assets.

For each relevant asset row, classify:

* `existing_asset_found: true | false`
* `current_location`
* `asset_quality: reusable | reusable_with_edit | supersede | unsafe_or_obsolete | missing | unknown`
* `normalisation_required: true | false`
* `mr_action: none | evidence_check | normalise_existing | draft_new_candidate | defer_medical_review | defer_architecture`
* `runtime_ready: true | false`
* `candidate_only: true | false`
* `requires_medical_review: true | false`

Coverage matrix must include at least:

1. all existing retail explainer entries already present;
2. all known missing retail biomarker explainers from the launch/beta panel, if discoverable from existing registry scope;
3. pathway explainers currently present;
4. pathway explainers missing for launch-core domains, especially hepatic and metabolic;
5. missing-marker caveats currently present;
6. missing-marker caveat gaps for Wave 1 / launch-core panel where discoverable;
7. known lifestyle modifier classes from the context modifier catalogue;
8. known medication modifier classes from the intervention effects registry or governance docs;
9. known supplement modifier classes, especially creatine, iron, B12, vitamin D, folate, protein, testosterone/hormone supplementation if documented;
10. positive/resilience qualifier status;
11. frame-level prose status, noting that frame routing remains deferred.

The matrix is an inventory and planning artefact. It must not be consumed by runtime.

## Phase 2 — MR candidate prose asset schema

Create a schema file:

`docs/sprints/beta_readiness/P3-PROSE-DEPTH-1_mr_candidate_asset_schema.yaml`

It must define required fields for MR-authored candidate prose assets.

At minimum include:

* `asset_id`
* `asset_type`
* `audience`
* `scope`
* `personalisation_axes`
* `trigger_conditions`
* `evidence_refs`
* `evidence_strength`
* `safety_boundaries`
* `review_status`
* `destination_mapping`
* `prose_content`
* `max_word_count`
* `authored_by`
* `authored_utc`
* `source_asset_ids`, where normalising existing prose
* `supersedes_asset_ids`, where replacing weak/unsafe prose
* `notes_for_medical_reviewer`

Allowed `asset_type` values must include:

* `base_biomarker_explainer`
* `result_direction_explainer`
* `system_explainer`
* `subsystem_explainer`
* `pathway_explainer`
* `signal_frame_explainer`
* `lifestyle_modifier_fragment`
* `medication_modifier_fragment`
* `supplement_modifier_fragment`
* `missing_marker_caveat`
* `weak_evidence_fallback`
* `positive_resilience_qualifier`
* `clinician_detail`
* `retail_user_summary`

Allowed `review_status` values must include:

* `CANDIDATE`
* `NEEDS_MEDICAL_REVIEW`
* `APPROVED`
* `REJECTED`
* `DEPRECATED`

The schema must make clear:

* MR LLM output starts as `CANDIDATE`;
* candidate assets are not runtime assets;
* candidate assets must not be consumed directly in production;
* approved assets require later promotion/compile work;
* no treatment recommendations are allowed;
* no diagnostic wording is allowed;
* lab-derived reference ranges remain the only interpretation authority where ranges are used.

## Phase 3 — Candidate asset template

Create:

`docs/sprints/beta_readiness/P3-PROSE-DEPTH-1_mr_candidate_asset_template.yaml`

This should be a reusable template MR can fill.

It must show:

* one generic base biomarker explainer template;
* one signal/frame explainer template;
* one pathway explainer template;
* one lifestyle modifier fragment template;
* one medication modifier fragment template;
* one supplement modifier fragment template;
* one missing-marker caveat template;
* one positive/resilience qualifier template.

These can be skeletal examples. Do not author clinically definitive prose unless the source wording already exists in governed documents.

All examples must have:

`review_status: CANDIDATE`

## Phase 4 — MR Batch 001 brief

Create:

`docs/sprints/beta_readiness/P3-PROSE-DEPTH-1_mr_batch_001_brief.md`

This is the instruction pack for the Medical Research LLM.

It must request candidate prose assets only.

Batch 001 should focus on beta-critical depth, not the whole universe.

Include at least:

1. hepatic pathway explainer candidate;
2. metabolic/glycaemic pathway explainer candidate;
3. top 10 missing retail biomarker explainers by launch/beta relevance, using the coverage matrix;
4. missing-marker caveat candidates for hepatic/metabolic/lipid/kidney contexts where gaps are identified;
5. lifestyle modifier fragment candidates for:

   * alcohol/hepatic markers;
   * smoking/inflammation context, if supported by existing catalogue;
   * exercise/creatinine or muscle enzyme context, if supported by existing catalogue;
   * hydration/creatinine or renal concentration context, if supported by existing catalogue;
6. medication modifier fragment candidates for:

   * statins/lipid interpretation;
   * metformin/glucose or B12 context, if supported by existing registry;
   * NSAID/renal context, if supported by existing registry;
7. supplement modifier fragment candidates for:

   * creatine/creatinine;
   * iron supplements/ferritin/iron interpretation;
   * B12/folate supplementation context.

The brief must instruct MR:

* do not write directly to runtime files;
* do not claim diagnosis;
* do not recommend treatment, dose changes, supplements or medication actions;
* cite evidence for each non-educational claim;
* state uncertainty;
* use cautious UK consumer-facing language;
* separate retail and clinician variants only where required;
* only create sex/age-specific wording where medically justified;
* mark all assets `CANDIDATE`;
* identify any asset requiring medical review before activation.

## Phase 5 — Modifier fragment templates

Create:

`docs/sprints/beta_readiness/P3-PROSE-DEPTH-1_modifier_fragment_templates.yaml`

This should define template structures for additive modifier fragments.

Include:

* lifestyle modifier fragment;
* medication modifier fragment;
* supplement modifier fragment;
* conflict-resolution fragment;
* suppression rule note;
* maximum fragment length;
* required evidence;
* prohibited claims;
* target destination mapping placeholder.

Emphasise:

* modifiers are additive caveats, not paragraph replacements;
* modifiers must not imply causation unless evidence supports it;
* modifiers must not provide advice;
* Gemini must never infer modifier relationships.

## Phase 6 — Completion report

Create:

`docs/sprints/beta_readiness/P3-PROSE-DEPTH-1_prose_library_depth_modifier_schema_completion.md`

Use this structure:

1. start state;
2. architecture authority reviewed;
3. existing assets found;
4. coverage gaps identified;
5. schema created;
6. MR Batch 001 scope;
7. modifier template scope;
8. what remains candidate-only;
9. what requires medical review;
10. what requires future runtime/promotion work;
11. recommended next sprint.

## Phase 7 — Manifest and carry-forward

Create:

`docs/sprints/beta_readiness/P3-PROSE-DEPTH-1_manifest.yaml`

Include:

* files created/updated;
* no runtime files changed;
* no production assets changed;
* no Gemini activation;
* no modifier runtime binding;
* no medical content promoted to approved runtime status;
* candidate-only status.

Create:

`docs/sprints/beta_readiness/P3-PROSE-DEPTH-1_carry_forward.yaml`

Include at least:

* MR Batch 001 needs medical research completion;
* MR candidate assets need medical review before promotion;
* runtime promotion/import route remains future work;
* modifier binding remains future work;
* frame routing remains deferred;
* P4-1 Gemini activation design remains CEO-gated;
* product-quality frontend UAT remains blocked by content depth, frame routing, modifier activation, Gemini pilot and Journey v6 IA work;
* decision needed on whether full 79/79 retail coverage is beta-blocking or whether prioritised subset is acceptable.

Update:

`docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md`

Keep the entry concise.

## Validation

Run available documentation/schema validation relevant to the repo.

At minimum:

* YAML parse validation for all new `.yaml` files;
* existing repository doc lint/validation if available;
* grep or equivalent check confirming no runtime/production asset files were modified;
* Automation Bus finish command:

`python backend/scripts/run_work_package.py finish`

Do not modify validators to force a pass.

## Acceptance criteria

This sprint passes only if:

1. Automation Bus preflight passes.
2. Risk remains STANDARD.
3. Change type remains CONTENT.
4. No runtime behaviour files are modified.
5. No Intelligence Core files are modified.
6. No frontend files are modified.
7. No Gemini files or prompt templates are modified.
8. No production prose registry/YAML assets are modified.
9. No production PSI or compiled card files are modified.
10. No context modifier is activated.
11. No medical content is promoted to `APPROVED` runtime status.
12. Coverage matrix exists and identifies existing/partial/missing/deferred asset status.
13. Existing assets are mapped before new candidate work is requested.
14. MR candidate asset schema exists.
15. MR candidate asset template exists.
16. MR Batch 001 brief exists and is usable by Medical Research LLM.
17. Modifier fragment templates exist.
18. All MR-generated or MR-targeted content is explicitly candidate-only.
19. Medical review requirements are recorded.
20. Carry-forward records runtime promotion, modifier activation, frame routing, P4-1 CEO gate and frontend UAT blockers.
21. Build register is updated.
22. Final audit includes `pipeline_advisory_trigger: true` and explains whether next work should be MR Batch 001, prose promotion/import, frame routing, P4-1, or another content-depth tranche.

## Closure requirements

Before finish, perform the mandatory Post-Implementation Closure Protocol.

Run and report:

* `git branch --show-current`
* `git status --short`
* `git log --oneline -n 5`
* `git diff --name-only`
* `git diff --cached --name-only`
* `git stash list`

Confirm:

* branch matches this sprint branch;
* no unrelated tracked/untracked files;
* no tooling leakage;
* no stash ambiguity;
* no parked files outside the repository;
* latest commit contains only in-scope work.

Then run:

`python backend/scripts/run_work_package.py finish`

After successful finish, handle `automation_bus/latest_cursor_status.json` under Automation Bus SOP v1.3.1.

Do not merge. Human merge authority is required.
