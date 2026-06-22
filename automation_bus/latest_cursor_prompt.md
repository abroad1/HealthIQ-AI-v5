---
work_id: P1-23
branch: sprint/P1-23-thyroid-intelligence-surface
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# P1-23 — Thyroid Intelligence Surface Completion

You are Cursor, acting as the Knowledge Bus + Core Engine implementation agent.

Implement this work package under Automation Bus SOP v1.3.1.

This is a HIGH-risk mixed CONTENT + BEHAVIOUR sprint.

It is not a frontend sprint.
It is not a Gemini sprint.
It is not a report-prose sprint.
It is not a broad thyroid redesign sprint.
It is not a Medical Review sprint.

## Purpose

Complete the `wave1_thyroid` intelligence surface after P1-22 activated thyroid as the sixth launch-core domain.

P1-22 made thyroid live but shallow:

* TSH participates in lab-range-only scoring only;
* TSH signal intelligence remains deferred;
* `wave1_thyroid` routes with an empty subsystem tuple;
* no compiled thyroid subsystem card exists.

P1-23 must close the beta-critical thyroid intelligence gaps by:

1. authoring and opting in modern kb52c TSH packages from governed Pass 3 investigation specs;
2. deprecating the legacy s24 TSH packages in-place;
3. moving only authorised TSH directional signals into the thyroid launch allowlist;
4. authoring and registering the compiled thyroid subsystem card;
5. ensuring thyroid subsystem evidence is emitted at runtime;
6. preserving all P1-22 boundaries for FT3-low, `signal_thyroid_tsh_context`, FT3-high companion gating and TSH clinical authority.

## Stage 0 / Stage B baseline

Stage 0 v0.5 advisory identified P1-23 as the highest-value next package.

Stage B Mode 2 amended the scope:

1. Do not attempt s24 revalidation as the launch path.
2. Author two new kb52c TSH packages from `Batch_4_Pass_3.json`.
3. Deprecate the legacy s24 TSH packages before kb52c opt-in.
4. Add an explicit Medical Review authority gate before any TSH allowlist update.
5. Move exactly two TSH signal IDs into launch if gates pass:

   * `signal_tsh_high`
   * `signal_tsh_low`
6. Keep excluded:

   * `signal_free_t3_low`
   * `signal_thyroid_tsh_context`
7. Author and register:

   * `knowledge_bus/compiled/health_system_cards/wave1_thy_hormonal_axis.yaml`
8. Do not modify:

   * `backend/core/analytics/domain_narrative_wave1.py`
   * `backend/core/analytics/signal_evaluator.py`
   * `backend/ssot/scoring_policy.yaml`

## Mandatory read list

Read before editing:

* `automation_bus/latest_pipeline_advisory.md`
* `automation_bus/latest_scope_advisory.md`
* `docs/discussion documents/healthiq_pre_sop_prompt_scoping_workflow_v0_5.md`
* `docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md`
* `docs/sprints/beta_readiness/P1-22_pass3_carry_forward.yaml`
* `docs/sprints/beta_readiness/P1-22_thyroid_activation_pack.md`
* `docs/sprints/beta_readiness/P1-22_thyroid_activation_manifest.yaml`
* `docs/architecture/ADR-THYROID-TSH-LAUNCH-SCORING-ONLY-1.md`
* `docs/architecture/ADR-THYROID-FT3-AUTHORITY-RECONCILIATION-1.md`
* `docs/Medical Research Documents/thyroid_blood_marker_interpretation_clinical_signoff.md`
* `knowledge_bus/research/investigation_specs/multi_llm_research/Batch_4_Pass_3.json`
* `knowledge_bus/governance/batch2_thyroid_gate_execution_register_v1.yaml`
* `backend/ssot/biomarkers.yaml`
* `backend/core/analytics/domain_score_assembler.py`
* `backend/core/analytics/wave1_subsystem_evidence.py`
* `backend/core/knowledge/health_system_card_evidence.py`
* existing compiled health-system card examples under:

  * `knowledge_bus/compiled/health_system_cards/`
* existing thyroid Knowledge Bus packages:

  * `knowledge_bus/packages/pkg_s24_tsh_high_hypothyroidism/`
  * `knowledge_bus/packages/pkg_s24_tsh_low_hyperthyroidism/`
  * `knowledge_bus/packages/pkg_thyroid_tsh_context/`
* kb47 FT3/FT4 package manifests needed to trace thyroid compiled card source spec IDs
* existing tests covering:

  * thyroid activation;
  * domain assembler;
  * domain allowlists;
  * compiled health-system card evidence;
  * signal authority / package validation;
  * FT3-low exclusion;
  * FT3-high companion gate behaviour.

Use targeted search:

* `rg "signal_tsh_high|signal_tsh_low|signal_thyroid_tsh_context|signal_free_t3_low" backend knowledge_bus docs`
* `rg "pkg_s24_tsh_high_hypothyroidism|pkg_s24_tsh_low_hyperthyroidism|pkg_thyroid_tsh_context" knowledge_bus docs backend`
* `rg "inv_tsh_high_primary_hypothyroid_pattern|inv_tsh_low_thyrotoxic_pattern" knowledge_bus`
* `rg "wave1_thyroid|wave1_thy_hormonal_axis|WAVE1_COMPILED_SUBSYSTEM_IDS" backend knowledge_bus docs`
* `rg "health_system_card_evidence_schema|assemble_subsystem_from_compiled_card_evidence|compiled_subsystem" backend knowledge_bus`
* `rg "ft3_low|signal_free_t3_low|companion gate|TSH-suppressed" backend docs knowledge_bus`
* `rg "ldl|crp|supporting_metrics|dependencies" knowledge_bus/research/investigation_specs/multi_llm_research/Batch_4_Pass_3.json backend/ssot/biomarkers.yaml`

Inspect relevant hits before editing.

## Files in scope

Allowed if justified:

### Knowledge Bus package creation / deprecation

* New package directory:

  * `knowledge_bus/packages/pkg_kb52c_tsh_high_primary_hypothyroid_pattern/`
* New package directory:

  * `knowledge_bus/packages/pkg_kb52c_tsh_low_thyrotoxic_pattern/`
* Within each new kb52c package:

  * `package_manifest.yaml`
  * `research_brief.yaml`
  * `signal_library.yaml`
  * `promoted_signal_intelligence.yaml`
* Legacy package manifests only:

  * `knowledge_bus/packages/pkg_s24_tsh_high_hypothyroidism/package_manifest.yaml`
  * `knowledge_bus/packages/pkg_s24_tsh_low_hyperthyroidism/package_manifest.yaml`

### Compiled thyroid card

* `knowledge_bus/compiled/health_system_cards/wave1_thy_hormonal_axis.yaml`
* `backend/core/knowledge/health_system_card_evidence.py`
* `backend/core/analytics/wave1_subsystem_evidence.py`

### Core Engine allowlist

* `backend/core/analytics/domain_score_assembler.py`

### Tests

Allowed test updates/additions for P1-23 scope only, including but not limited to:

* `backend/tests/unit/test_p1_22_thyroid_activation_pack.py`
* domain assembler tests
* compiled card evidence tests
* package/PSI validation tests if existing patterns require them
* regression tests required to preserve FT3-low exclusion and TSH/context boundaries

### Sprint artefacts

* `docs/architecture/ADR-THYROID-TSH-SIGNAL-INTELLIGENCE-ACTIVATION-1.md`
* `docs/sprints/beta_readiness/P1-23_thyroid_intelligence_surface_completion.md`
* `docs/sprints/beta_readiness/P1-23_thyroid_intelligence_manifest.yaml`
* `docs/sprints/beta_readiness/P1-23_pass3_carry_forward.yaml`
* `docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md`

## Files out of scope

Do not modify:

* `backend/core/analytics/domain_narrative_wave1.py`
* `backend/core/analytics/signal_evaluator.py`
* `backend/ssot/scoring_policy.yaml`
* frontend files
* Gemini files
* report prose / Layer C presentation files
* raw Pass 3 research
* generated-pilot files
* non-TSH Knowledge Bus package medical content
* `knowledge_bus/packages/pkg_thyroid_tsh_context/`
* FT3-low packages or activation-control files
* FT3-high companion-gate logic
* iron/ferritin/CBC packages
* TSAT / transferrin saturation policy
* parser files
* `.codex/`
* `.cursor/`
* `.vscode/`
* `AGENTS.md`

## Critical boundaries

### TSH package path

Do not attempt to revalidate s24 packages as the launch path.

P1-23 must close cf_005 by replacing the legacy s24 path with modern kb52c authority:

* author `pkg_kb52c_tsh_high_primary_hypothyroid_pattern`;
* author `pkg_kb52c_tsh_low_thyrotoxic_pattern`;
* deprecate the s24 TSH packages in-place;
* document that cf_005 is closed by kb52c replacement, not s24 revalidation.

The phrase “s24 revalidation path” must not appear as a live option in sprint artefacts.

### Medical Review gate

Before proceeding to domain allowlist update, confirm whether:

`docs/Medical Research Documents/thyroid_blood_marker_interpretation_clinical_signoff.md`

constitutes sufficient Medical Review authority for TSH directional signal activation, or whether a new Medical Review intake is required.

STOP and escalate to GPT if Medical Review is required and not satisfied.

Do not move TSH signals into the launch allowlist unless this gate is resolved.

### TSH allowlist boundary

If all Phase 1 gates pass, move exactly these signal IDs into `_THYROID_LAUNCH_SIGNAL_IDS`:

* `signal_tsh_high`
* `signal_tsh_low`

Keep these excluded:

* `signal_free_t3_low`
* `signal_thyroid_tsh_context`

Do not move `signal_thyroid_tsh_context` into launch.

Do not add a broad context signal for TSH.

Do not add any additional TSH signal IDs unless hardening identifies a canonical naming issue and GPT approves before implementation.

### FT3-low boundary

`signal_free_t3_low` must remain excluded.

No FT3-low activation path may be introduced.

Tests must preserve `signal_free_t3_low` exclusion as a named independent assertion after any refactor.

### FT3-high boundary

Preserve existing FT3-high companion-gate behaviour.

Do not modify `signal_evaluator.py`.

Do not loosen or bypass the mandatory pre-emission gate for FT3-high.

### Scoring boundary

Do not modify `backend/ssot/scoring_policy.yaml`.

P1-22 already implemented thyroid lab-range-only scoring.

P1-23 is signal intelligence + compiled subsystem evidence, not scoring-policy work.

### Narrative boundary

Do not modify `domain_narrative_wave1.py`.

The existing thyroid narrative fallback is acceptable for TSH signal IDs in this sprint.

TSH-specific narrative enrichment is deferred to a future governed narrative sprint.

## Phase 0 — Automation Bus preflight

Before implementation:

1. Confirm current branch is:

`sprint/P1-23-thyroid-intelligence-surface`

2. Confirm `automation_bus/state/work_package_active.json` exists.
3. Confirm active token has `work_id: P1-23`.
4. Confirm token branch matches current branch.
5. Confirm repo/stash/parked-file state is governed under the standard start prompt.

If any condition fails, STOP.

## Phase 1 — Knowledge Bus authority and PSI opt-in gate

Phase 1 must complete before any Core Engine allowlist or compiled-card runtime registration.

### 1A — Medical Review authority check

Before package authoring or allowlist planning, inspect:

`docs/Medical Research Documents/thyroid_blood_marker_interpretation_clinical_signoff.md`

and relevant thyroid ADRs.

Determine whether existing clinical signoff is sufficient for TSH directional signal activation.

Record the decision in:

`docs/sprints/beta_readiness/P1-23_thyroid_intelligence_manifest.yaml`

If existing signoff is not sufficient, STOP and classify:

`BLOCKED_MEDICAL_REVIEW_REQUIRED`

Do not proceed to TSH package opt-in or Core Engine allowlist changes.

### 1B — Source specification verification

Verify in `Batch_4_Pass_3.json`:

* `inv_tsh_high_primary_hypothyroid_pattern`
* `inv_tsh_low_thyrotoxic_pattern`

Confirm each has:

* `investigation_spec_contract_version: 3.0.0`
* correct intended signal ID:

  * `signal_tsh_high`
  * `signal_tsh_low`
* sufficient source fields for package authoring;
* source traceability suitable for package manifests and PSI.

STOP if either source spec is absent, not v3.0.0, malformed, or insufficient.

### 1C — SSOT canonical biomarker ID verification

Before authoring `signal_library.yaml` for kb52c TSH packages, verify all `supporting_metrics` and `dependencies.biomarkers` fields against:

`backend/ssot/biomarkers.yaml`

Specifically verify / normalise any source references such as:

* `ldl`
* `crp`

Use canonical IDs required by the SSOT and validator.

STOP if any field fails canonical validation or cannot be mapped without medical interpretation.

Do not invent canonical mappings.

Record canonical ID decisions in the P1-23 manifest.

### 1D — Legacy s24 deprecation before kb52c opt-in

Before kb52c production opt-in:

* add deprecation metadata to:

  * `pkg_s24_tsh_high_hypothyroidism/package_manifest.yaml`
  * `pkg_s24_tsh_low_hyperthyroidism/package_manifest.yaml`

Use the P1-21 ferritin-high in-place deprecation pattern.

Deprecation metadata must state:

* deprecated: true
* deprecated_by:

  * relevant kb52c replacement package
* deprecated_reason:

  * replacement by governed Pass 3 kb52c package per P1-23

Do not modify s24 `signal_library.yaml` or `research_brief.yaml`.

STOP if the signal authority collision cannot be resolved cleanly.

### 1E — Author kb52c TSH packages

Author exactly two new production packages:

1. `knowledge_bus/packages/pkg_kb52c_tsh_high_primary_hypothyroid_pattern/`

   * from `inv_tsh_high_primary_hypothyroid_pattern`
   * signal ID: `signal_tsh_high`

2. `knowledge_bus/packages/pkg_kb52c_tsh_low_thyrotoxic_pattern/`

   * from `inv_tsh_low_thyrotoxic_pattern`
   * signal ID: `signal_tsh_low`

For each package create:

* `package_manifest.yaml`
* `research_brief.yaml`
* `signal_library.yaml`
* `promoted_signal_intelligence.yaml`

All content must be derived from governed Pass 3 source artefacts.

Do not invent medical content.

Do not edit raw research.

Do not edit generated-pilot files.

Do not use global/default reference ranges.

### 1F — PSI opt-in validation

Validate both packages and both PSI files using the repository’s established validators.

Required outcome:

* package validation passes;
* PSI validation passes;
* no signal ID collision remains;
* activation readiness / production opt-in scanner detects the new TSH PSI opt-ins;
* production opt-in count increases by the expected amount, unless a STOP gate prevents one candidate.

If either package fails validation, STOP for that candidate and carry forward with blocker class.

### 1G — Phase 1 decision record

Create a concise ADR:

`docs/architecture/ADR-THYROID-TSH-SIGNAL-INTELLIGENCE-ACTIVATION-1.md`

It must record:

* existing TSH scoring-only boundary from P1-22;
* Medical Review authority decision;
* kb52c replacement path;
* s24 packages deprecated, not revalidated;
* exact TSH signal IDs authorised for launch:

  * `signal_tsh_high`
  * `signal_tsh_low`
* excluded TSH context signal:

  * `signal_thyroid_tsh_context`
* FT3-low remains excluded;
* Phase 2 allowlist/card work may proceed only because Phase 1 gates passed.

Keep it concise.

Do not write a long narrative architecture paper.

## Phase 2 — Core Engine thyroid intelligence surface

Proceed to Phase 2 only if Phase 1 gates pass.

### 2A — Domain allowlist update

Update `backend/core/analytics/domain_score_assembler.py`.

Move exactly:

* `signal_tsh_high`
* `signal_tsh_low`

from `_THYROID_EXCLUDED_SIGNAL_IDS` to `_THYROID_LAUNCH_SIGNAL_IDS`.

Keep excluded:

* `signal_free_t3_low`
* `signal_thyroid_tsh_context`

Update the comment around the thyroid launch allowlist to reflect P1-23 authority extension.

Do not modify FT3-high companion-gate logic.

Do not modify `signal_evaluator.py`.

### 2B — Compiled thyroid subsystem card

Create:

`knowledge_bus/compiled/health_system_cards/wave1_thy_hormonal_axis.yaml`

Required fields:

* `subsystem_id: wave1_thy_hormonal_axis`
* `domain_id: wave1_thyroid`
* `visibility_tier: scored_subsystem`
* source spec IDs must be traceable and not invented.

Source spec IDs must be read from:

* `Batch_4_Pass_3.json` for the two TSH source specs;
* kb47 package manifests for FT3 / FT4 source spec IDs.

STOP if any source spec ID cannot be traced to an existing file.

Do not invent marker roles, relationship kinds or presence policies.

Use existing compiled health-system card examples and schema as authority.

### 2C — Register compiled thyroid subsystem card

Update:

* `backend/core/knowledge/health_system_card_evidence.py`
* `backend/core/analytics/wave1_subsystem_evidence.py`

Register:

* `wave1_thy_hormonal_axis`

Update `wave1_thyroid` subsystem order from empty tuple to:

`("wave1_thy_hormonal_axis",)`

Do not modify unrelated domain subsystem orders.

### 2D — Tests

Update or add tests exactly protecting the P1-23 boundaries.

Required test changes:

1. Update `test_ft3_low_not_in_thyroid_domain_allowlist` by splitting it into two tests:

   * `signal_free_t3_low` remains excluded;
   * `signal_tsh_high` now fires in the thyroid domain when active.

2. Update `test_thyroid_domain_includes_ft4_high_when_active` so:

   * `signal_tsh_low` appears in `active_signal_ids` when active;
   * it is no longer incorrectly filtered out.

3. Add:

   * `test_tsh_high_fires_in_thyroid_domain_after_p1_23`
   * `test_tsh_low_fires_in_thyroid_domain_after_p1_23`
   * `test_signal_thyroid_tsh_context_remains_excluded`
   * `test_thyroid_subsystem_evidence_row_emitted`

Also ensure tests continue to prove:

* FT3-low remains excluded;
* `signal_thyroid_tsh_context` remains excluded;
* FT3-high companion gate remains preserved;
* existing six launch-core domain ordering remains stable;
* compiled thyroid subsystem evidence is emitted at runtime;
* no scoring policy change occurred in P1-23.

## Phase 3 — Carry-forward manifest

Create:

`docs/sprints/beta_readiness/P1-23_pass3_carry_forward.yaml`

Include only unresolved items.

Expected resolved if sprint succeeds:

* cf_001: TSH signal intelligence deferred;
* cf_004: wave1_thyroid compiled subsystem card evidence missing;
* cf_005: legacy s24 TSH revalidation.

If any are unresolved, record:

* item ID;
* marker/package reference;
* reason not implemented;
* blocker class;
* owner agent:

  * Knowledge Bus
  * Core Engine
  * Medical Review
  * Frontend/Presentation
* launch/beta relevance;
* recommended future package.

Do not re-document unrelated iron/ferritin/CBC items unless newly affected.

Do not include P1-24 bio-oxygen card depth unless P1-23 touches it, which it should not.

## Phase 4 — Sprint report and build register

Create:

`docs/sprints/beta_readiness/P1-23_thyroid_intelligence_surface_completion.md`

Keep it concise.

Maximum structure:

1. start state;
2. Phase 1 Knowledge Bus outcome;
3. Phase 2 Core Engine outcome;
4. authority decisions;
5. validation results;
6. carry-forwards;
7. recommended next sprint.

Update:

`docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md`

Keep the register entry lightweight:

* delivered;
* blocked/carry-forward;
* recommended next sprint.

Do not write long narrative documentation.
Do not duplicate audit content.
Do not list every untouched file.

## Acceptance criteria

P1-23 passes only if:

1. Existing Medical Review authority for TSH directional activation is explicitly assessed before package opt-in or allowlist change.
2. Sprint stops if Medical Review is required and not satisfied.
3. `pkg_kb52c_tsh_high_primary_hypothyroid_pattern` is authored from `inv_tsh_high_primary_hypothyroid_pattern`.
4. `pkg_kb52c_tsh_low_thyrotoxic_pattern` is authored from `inv_tsh_low_thyrotoxic_pattern`.
5. Both source specs are confirmed v3.0.0.
6. SSOT canonical biomarker IDs are verified before `signal_library.yaml` authoring.
7. s24 TSH packages are deprecated in-place before kb52c opt-in.
8. s24 `signal_library.yaml` and `research_brief.yaml` are not modified.
9. No raw Pass 3 research is edited.
10. No generated-pilot files are edited.
11. No medical content is invented.
12. Both kb52c TSH packages validate.
13. Both PSI files validate.
14. Production opt-in scanner detects the new TSH PSI opt-ins if gates pass.
15. No unresolved signal ID collision remains.
16. Phase 1 ADR records kb52c replacement and s24 deprecation.
17. Phase 2 does not begin unless Phase 1 gates pass.
18. Exactly `signal_tsh_high` and `signal_tsh_low` are added to `_THYROID_LAUNCH_SIGNAL_IDS`.
19. `signal_free_t3_low` remains excluded.
20. `signal_thyroid_tsh_context` remains excluded.
21. `signal_evaluator.py` is not modified.
22. `domain_narrative_wave1.py` is not modified.
23. `backend/ssot/scoring_policy.yaml` is not modified.
24. `wave1_thy_hormonal_axis.yaml` is created with traceable source spec IDs.
25. `wave1_thy_hormonal_axis` is registered in compiled card evidence registry.
26. `wave1_thyroid` subsystem order is updated from empty tuple to `("wave1_thy_hormonal_axis",)`.
27. Tests prove TSH high fires in thyroid domain.
28. Tests prove TSH low fires in thyroid domain.
29. Tests prove `signal_thyroid_tsh_context` remains excluded.
30. Tests prove FT3-low remains excluded.
31. Tests prove thyroid subsystem evidence row is emitted.
32. Existing launch-core domain order remains stable.
33. Carry-forward manifest captures unresolved items only.
34. Build register is updated concisely.
35. Sprint report is concise.
36. Final audit includes `pipeline_advisory_trigger` and `pipeline_advisory_reason`.

## Validation commands

Run all relevant existing validation commands.

At minimum:

* validators for each new Knowledge Bus package;
* validators for each new `promoted_signal_intelligence.yaml`;
* activation readiness / production opt-in scanner;
* compiled health-system card schema validation for `wave1_thy_hormonal_axis.yaml`;
* unit tests covering thyroid domain allowlist and subsystem evidence;
* regression tests for compiled card evidence and domain assembly;
* architecture/governance tests required by Automation Bus finish;
* `python backend/scripts/run_work_package.py finish`.

Do not edit validators to make validation pass.

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
