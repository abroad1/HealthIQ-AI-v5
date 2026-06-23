---
work_id: P1-25
branch: feature/p1-25-thyroid-mr-v2-activation-completion
risk_level: HIGH
execution_model: SINGLE_PHASE
change_type: MIXED
---

# P1-25 — Thyroid MR-v2 Activation Completion

You are Cursor, acting as a combined Knowledge Bus + Core Engine implementation agent under Automation Bus SOP v1.3.1.

This is a HIGH-risk MIXED sprint.

This sprint implements the MR-v2-cleared thyroid activation package as one outcome-based sprint:

1. FT3-low / reduced peripheral T3 availability context.
2. TPOAb-high / autoimmune thyroid context supporting hypothyroid biochemistry.

Do not split this into separate FT3-only, TPOAb-only, ADR-only, allowlist-only, or card-only sprints unless a hard STOP gate fires.

## Authority inputs

Read before editing:

* `automation_bus/latest_pipeline_advisory.md`
* `automation_bus/latest_pipeline_advisory_throughput_challenge.md`
* `automation_bus/latest_scope_advisory.md`
* latest `automation_bus/latest_audit_summary.md`
* `docs/Medical Research Documents/Medical_Research_Activation_Review_Deferred_Wave_1_Items_v2.md`
* `docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md`
* latest P1-22, P1-23 and P1-24 sprint artefacts
* `docs/architecture/ADR-THYROID-FT3-AUTHORITY-RECONCILIATION-1.md`
* `docs/architecture/ADR-THYROID-TSH-LAUNCH-SCORING-ONLY-1.md`
* `docs/architecture/ADR-THYROID-TSH-SIGNAL-INTELLIGENCE-ACTIVATION-1.md`
* `docs/architecture/ADR-THYROID-SCORING-LAB-RANGE-ARCHITECTURE-1.md`

Treat MR-v2 as the medical activation authority.

Treat `latest_pipeline_advisory_throughput_challenge.md` and `latest_scope_advisory.md` as the current scoping authority.

Do not make new medical judgements.

## Sprint purpose

Deliver one governed thyroid activation package that:

* activates `signal_free_t3_low` only under strict MR-v2 gates;
* activates `signal_tpo_ab_high` only under strict MR-v2 gates;
* updates the thyroid domain allowlist once;
* creates the required ADR authority document;
* hardens the relevant Knowledge Bus signal libraries;
* authors the missing TPOAb PSI;
* updates medical frame governance;
* enriches the compiled thyroid subsystem card;
* updates regression and activation tests;
* records carry-forwards clearly.

## Expected product output

After successful P1-25:

* FT3-low is no longer categorically deferred.
* FT3-low can fire only when all deterministic safety gates are satisfied.
* FT3-low must not fire when required context is absent.
* FT3-low must not fire when TSH is suppressed below the lab-provided range.
* TPOAb-high can fire only when TPOAb is above the lab-provided range, TSH is above the lab-provided range, and FT4 is present.
* TPOAb-high must not fire in euthyroid biochemistry.
* TPOAb-high must not diagnose Hashimoto’s disease or autoimmune thyroid disease.
* The thyroid launch allowlist includes both `signal_free_t3_low` and `signal_tpo_ab_high`.
* `wave1_thy_hormonal_axis` includes FT3-low and TPOAb source-spec depth.
* Prior FT3-low deferral is closed.
* kb59 thyroid antibody deferral is partially closed: TPOAb hypothyroid frame only.

## Files in scope

### HIGH-risk behaviour / Intelligence Core

* `backend/core/analytics/domain_score_assembler.py`

Expected allowlist changes:

* remove `signal_free_t3_low` from `_THYROID_EXCLUDED_SIGNAL_IDS`;
* add `signal_free_t3_low` to `_THYROID_LAUNCH_SIGNAL_IDS`;
* add `signal_tpo_ab_high` to `_THYROID_LAUNCH_SIGNAL_IDS`;
* keep `signal_thyroid_tsh_context` excluded;
* update the thyroid comment to reference P1-25 and `ADR-THYROID-MR-V2-ACTIVATION-1`.

### Knowledge Bus package files

* `knowledge_bus/packages/pkg_kb47_free_t3_low_low_t3_syndrome/signal_library.yaml`
* `knowledge_bus/packages/pkg_kb47_free_t3_low_low_t3_syndrome/promoted_signal_intelligence.yaml`
* `knowledge_bus/packages/pkg_kb59_tpo_ab_high_autoimmune_hypothyroid_pattern/signal_library.yaml`
* `knowledge_bus/packages/pkg_kb59_tpo_ab_high_autoimmune_hypothyroid_pattern/promoted_signal_intelligence.yaml`
* `knowledge_bus/packages/pkg_kb59_tpo_ab_high_autoimmune_hypothyroid_pattern/package_manifest.yaml`

### Governance / authority

* `knowledge_bus/governance/medical_frame_identity_index_v1.yaml`
* `docs/architecture/ADR-THYROID-MR-V2-ACTIVATION-1.md`

### Compiled card estate

* `knowledge_bus/compiled/health_system_cards/wave1_thy_hormonal_axis.yaml`
* `knowledge_bus/compiled/manifests/p1_25_thyroid_completion_card_evidence.yaml`
* `knowledge_bus/compiled/estate_index_v1.yaml`

### Tests

* `backend/tests/unit/test_p1_22_thyroid_activation_pack.py`
* `backend/tests/regression/test_batch2_thyroid_tsh_gating.py`
* `backend/tests/unit/test_p1_25_thyroid_completion.py`

### Sprint artefacts

* `docs/sprints/beta_readiness/P1-25_thyroid_completion_manifest.yaml`
* `docs/sprints/beta_readiness/P1-25_pass3_carry_forward.yaml`
* `docs/sprints/beta_readiness/P1-25_thyroid_mr_v2_activation_completion.md`
* `docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md`

## Files out of scope

Do not modify:

* `backend/core/analytics/signal_evaluator.py` unless a hard STOP gate proves deterministic FT3-low safety cannot otherwise be achieved and human approval is obtained before broadening scope.
* `backend/ssot/scoring_policy.yaml`
* `backend/ssot/biomarkers.yaml`
* `backend/ssot/questionnaire.json`
* TgAb packages
* TPOAb euthyroid packages or context
* `signal_thyroid_tsh_context`
* frontend files
* Gemini files
* report prose / Layer C prose substrate
* parser files
* unrelated thyroid packages
* unrelated Knowledge Bus packages
* `.codex/`
* `.cursor/`
* `.vscode/`
* `AGENTS.md`

## Phase 0 — Automation Bus preflight

Before implementation:

1. Confirm current branch is:

`feature/p1-25-thyroid-mr-v2-activation-completion`

2. Confirm `automation_bus/state/work_package_active.json` exists.
3. Confirm active token has `work_id: P1-25`.
4. Confirm token branch matches current branch.
5. Confirm repo/stash/parked-file state is governed under the standard start prompt.
6. Re-verify that the files named in the Stage B advisory have not changed since the advisory date.
7. If any named file has changed, re-read and re-validate affected assumptions before editing.

STOP if preflight fails.

## Phase 1 — Authority and current-state verification

### 1A — MR-v2 authority verification

Read MR-v2 and extract the thyroid decisions for:

* FT3 low / reduced peripheral T3 availability context;
* TPOAb high / autoimmune thyroid context supporting hypothyroid biochemistry;
* TPOAb euthyroid context;
* TgAb packages.

Confirm:

* FT3-low is cleared with strict gates.
* TPOAb hypothyroid context is cleared with strict gates.
* TPOAb euthyroid context remains deferred post-launch.
* TgAb remains deferred / corroborator-only.
* No Hashimoto’s diagnosis wording is allowed.
* No hypothyroidism diagnosis may be made from FT3-low.

STOP if MR-v2 is missing or contradicts these decisions.

### 1B — Existing thyroid ADR verification

Read the existing thyroid ADRs.

Create a new ADR:

`docs/architecture/ADR-THYROID-MR-V2-ACTIVATION-1.md`

Do not amend existing ADRs.

The new ADR must:

* cite MR-v2 dated 2026-06-23 as the current medical authority;
* supersede Decision 3 from `ADR-THYROID-TSH-SIGNAL-INTELLIGENCE-ACTIVATION-1.md` where FT3-low was kept excluded;
* partially supersede the thyroid antibody deferral in `ADR-THYROID-FT3-AUTHORITY-RECONCILIATION-1.md` for TPOAb hypothyroid frame only;
* leave TPOAb euthyroid and TgAb deferred;
* record required gates for FT3-low and TPOAb;
* prohibit diagnostic wording.

ADR creation is required in this sprint.

STOP if an ADR cannot be created safely.

### 1C — Package state verification

Verify:

FT3-low package:

* `pkg_kb47_free_t3_low_low_t3_syndrome`
* `signal_id: signal_free_t3_low`
* `promoted_signal_intelligence.yaml` exists
* `signal_library.yaml` exists
* package status supports activation after MR-v2 clearance

TPOAb package:

* `pkg_kb59_tpo_ab_high_autoimmune_hypothyroid_pattern`
* `signal_id: signal_tpo_ab_high`
* `signal_library.yaml` exists
* `promoted_signal_intelligence.yaml` does not currently exist and must be created
* `package_manifest.yaml` exists and currently needs behavioural-impact update after activation

STOP affected candidate if package identity is unclear.

## Phase 2 — FT3-low implementation

### 2A — Required FT3-low gates

FT3-low must not be allowlisted unless deterministic gating can enforce:

* FT3 below lab-provided range;
* TSH present;
* FT4 present;
* thyroid medication context requirement;
* illness/recovery context requirement;
* calorie restriction context requirement;
* fasting / low-energy availability context requirement;
* pregnancy/postpartum safety handling;
* biotin / assay-interference disclosure handling;
* no emission when TSH is below the lab-provided range;
* no diagnostic hypothyroidism framing;
* no diagnostic “low T3 syndrome” framing.

### 2B — Existing context-gate behaviour

The Stage B advisory found that several questionnaire fields are absent and that FT3-low will fail closed in production until questionnaire alignment exists.

Preserve this fail-closed behaviour.

Do not modify `backend/ssot/questionnaire.json` in this sprint.

Create a carry-forward item for questionnaire context alignment.

### 2C — Biotin / assay-interference gate

Add `biotin_or_assay_interference_disclosure` as an eighth runtime context requirement if supported by schema v2.0.0.

Design it so that `not_answered` and `not_applicable` do not further suppress the signal.

Candidate STOP:

* If this cannot be added within schema constraints, document it as a signal-library schema follow-on.
* Do not block FT3-low solely for this if all other safety gates are preserved.

### 2D — TSH-suppressed suppression gate

This is a GPT safety amendment to the Stage B advisory.

FT3-low must not be added to `_THYROID_LAUNCH_SIGNAL_IDS` unless the sprint can deterministically prevent FT3-low emission when TSH is below the lab-provided range.

Cursor must verify whether existing signal-library / evaluator semantics support one of the following:

* a negative / suppression-on-condition gate;
* a “require TSH not below minimum” gate;
* an equivalent deterministic gate that prevents emission when TSH is suppressed.

Candidate STOP:

* If deterministic TSH-suppressed suppression cannot be implemented without editing `backend/core/analytics/signal_evaluator.py`, do not add `signal_free_t3_low` to the thyroid launch allowlist in this sprint.
* Record FT3-low as still blocked by evaluator gate semantics.
* Proceed with TPOAb if its gates are valid.
* Do not silently activate FT3-low without this suppression.

Do not broaden into `signal_evaluator.py` without explicit human approval.

### 2E — FT3-low PSI wording review

Review `promoted_signal_intelligence.yaml`.

If any consumer-facing field uses unsafe wording such as:

* “low T3 syndrome” as a diagnosis;
* hypothyroidism wording;
* thyroid failure wording;

then reframe to MR-v2-safe language such as:

* “reduced peripheral T3 availability pattern”
* “contextual low FT3 pattern”
* “non-diagnostic low FT3 context”

If the field is internal-only and not user-visible, document this.

Candidate STOP:

* If unsafe consumer-facing wording cannot be corrected, do not activate FT3-low.

## Phase 3 — TPOAb implementation

### 3A — Required TPOAb gates

TPOAb must not be allowlisted unless deterministic gating can enforce:

* TPOAb above lab-provided range;
* TSH present and above lab-provided range;
* FT4 present;
* no emission when TSH is within range;
* no emission when TSH is suppressed;
* no emission when FT4 is absent;
* thyroid medication context represented safely;
* pregnancy/postpartum context represented safely;
* no Hashimoto’s diagnosis wording;
* no autoimmune thyroid disease diagnosis wording;
* no “immune system attacking thyroid” wording;
* no “thyroid will fail” wording.

### 3B — TPOAb signal library hardening

Update:

`knowledge_bus/packages/pkg_kb59_tpo_ab_high_autoimmune_hypothyroid_pattern/signal_library.yaml`

Required changes:

* add `runtime_context_requirements`;
* require `tsh` present;
* require `free_t4` present;
* add thyroid medication context with `not_answered` allowed if appropriate;
* add pregnancy/postpartum context with `not_answered` allowed if appropriate;
* add `mandatory_pre_emission_gate` requiring `tsh` `above_max`.

Candidate STOP:

* If `boundary: above_max` is not supported by the signal evaluator, do not add `signal_tpo_ab_high` to the launch allowlist.
* Record carry-forward for evaluator support.
* Continue FT3-low if valid.

### 3C — TPOAb PSI authoring

Create:

`knowledge_bus/packages/pkg_kb59_tpo_ab_high_autoimmune_hypothyroid_pattern/promoted_signal_intelligence.yaml`

Use `pkg_kb47` PSI as the structural template.

Derive content from:

* `pkg_kb59` signal library;
* MR-v2 Section F;
* existing package manifest / research brief if present.

Required wording constraints:

* no “Hashimoto’s disease” diagnosis;
* no “autoimmune thyroid disease” diagnosis;
* no “your immune system is attacking your thyroid”;
* no “your thyroid will fail”;
* no “you have hypothyroidism”.

Use neutral framing such as:

* “thyroid peroxidase antibody elevation pattern”
* “autoimmune thyroid context supporting hypothyroid biochemistry”
* “not diagnostic on its own”

Candidate STOP:

* If PSI authoring requires new medical interpretation not covered by MR-v2 or package source, stop TPOAb and record carry-forward.
* Do not invent medical content.

### 3D — TPOAb package manifest

Update:

`package_manifest.yaml`

`behavioural_impact` must no longer remain `NONE` if allowlist activation makes the signal contribute to thyroid domain scoring.

Match the declaration pattern used by other active-signal packages.

## Phase 4 — Thyroid allowlist update

Update:

`backend/core/analytics/domain_score_assembler.py`

Required post-sprint target if both candidates pass:

* `_THYROID_LAUNCH_SIGNAL_IDS` contains:

  * `signal_free_t3_high`
  * `signal_free_t4_high`
  * `signal_free_t4_low`
  * `signal_tsh_high`
  * `signal_tsh_low`
  * `signal_free_t3_low`
  * `signal_tpo_ab_high`

* `_THYROID_EXCLUDED_SIGNAL_IDS` contains:

  * `signal_thyroid_tsh_context`

If FT3-low candidate STOP fires:

* do not add `signal_free_t3_low`;
* keep it excluded;
* document carry-forward.

If TPOAb candidate STOP fires:

* do not add `signal_tpo_ab_high`;
* document carry-forward.

Do not activate any other thyroid signals.

## Phase 5 — Medical frame governance update

Update:

`knowledge_bus/governance/medical_frame_identity_index_v1.yaml`

Required changes:

* update FT3-low frame from inactive/deferred to active / cleared by MR-v2, if FT3-low candidate passes;
* add TPOAb hypothyroid frame entry, if TPOAb candidate passes;
* keep TPOAb euthyroid context deferred;
* keep TgAb deferred;
* preserve `signal_thyroid_tsh_context` exclusion.

Do not overstate authority.

## Phase 6 — Compiled thyroid card enrichment

Update:

`knowledge_bus/compiled/health_system_cards/wave1_thy_hormonal_axis.yaml`

If both candidates pass:

* add `inv_free_t3_low_low_t3_syndrome` to `source_spec_ids`;
* add `inv_tpo_ab_high_autoimmune_hypothyroid_pattern` to `source_spec_ids`;
* add TPOAb as a marker entry:

  * `marker_role: contextual_marker`
  * `relationship_kind: contextual_support`
  * `presence_policy: optional_on_panel`
* update FT3 marker rationale to reflect both high and low FT3 contexts;
* update mechanism line and subsystem summary;
* update `compile_manifest_ref`.

Create:

`knowledge_bus/compiled/manifests/p1_25_thyroid_completion_card_evidence.yaml`

Update:

`knowledge_bus/compiled/estate_index_v1.yaml`

If only one candidate passes, enrich the card only for the passing candidate.

Do not add unactivated source specs to the compiled card as active depth.

## Phase 7 — Tests

Update existing tests that are expected to change:

* `backend/tests/unit/test_p1_22_thyroid_activation_pack.py`

  * update `test_ft3_low_not_in_thyroid_domain_allowlist`
  * retain TSH high/low tests
  * retain `signal_thyroid_tsh_context` exclusion test
  * retain FT3-high companion-gate test

* `backend/tests/regression/test_batch2_thyroid_tsh_gating.py`

  * update `test_ft3_low_frame_deferred_after_p1_5_reconciliation` only if FT3-low candidate passes;
  * retain FT3-high / FT4 / TSH regression tests.

Create:

`backend/tests/unit/test_p1_25_thyroid_completion.py`

Required test coverage:

FT3-low:

* `signal_free_t3_low` is in thyroid launch allowlist if candidate passes;
* FT3-low suppresses when context fields are missing;
* FT3-low fires when all gates are mocked as satisfied;
* FT3-low suppresses when TSH is absent;
* FT3-low suppresses when FT4 is absent;
* FT3-low suppresses when TSH is below lab-provided range;
* FT3-low does not emit unsafe diagnostic wording.

TPOAb:

* `signal_tpo_ab_high` is in thyroid launch allowlist if candidate passes;
* TPOAb fires when TPOAb is above range, TSH is above range and FT4 is present;
* TPOAb suppresses when TSH is within range;
* TPOAb suppresses when TSH is absent;
* TPOAb suppresses when TSH is below range;
* TPOAb suppresses when FT4 is absent;
* TPOAb override / escalation behaviour is covered if existing signal library includes it;
* TPOAb PSI contains no prohibited wording.

Compiled card:

* thyroid card includes only passing candidate source specs;
* TPOAb marker entry exists only if TPOAb passes;
* estate index points to the P1-25 manifest if card enrichment occurs.

## Phase 8 — Carry-forward management

Create:

`docs/sprints/beta_readiness/P1-25_pass3_carry_forward.yaml`

Must record:

* cf_A / FT3-low:

  * `closed` if FT3-low candidate passes;
  * otherwise carry forward with exact blocker.

* cf_B / kb59 thyroid antibodies:

  * `partially_closed` if TPOAb hypothyroid passes;
  * remaining deferred:

    * TPOAb euthyroid context;
    * TgAb packages.

* questionnaire context alignment:

  * FT3-low context fields absent from questionnaire;
  * FT3-low fail-closed in production until questionnaire alignment;
  * owner: Product / questionnaire / frontend-input workflow;
  * not a blocker to safe activation if fail-closed behaviour is proven.

* conditional evaluator gate carry-forward:

  * only if deterministic TSH-suppressed suppression cannot be implemented;
  * if this fires, FT3-low must not be allowlisted.

Do not re-document unrelated carry-forwards.

## Phase 9 — Sprint report and build register

Create:

`docs/sprints/beta_readiness/P1-25_thyroid_mr_v2_activation_completion.md`

Keep concise.

Maximum structure:

1. start state;
2. MR-v2 authority used;
3. FT3-low implementation result;
4. TPOAb implementation result;
5. ADR / governance updates;
6. compiled card updates;
7. validation results;
8. carry-forwards;
9. recommended next sprint.

Create:

`docs/sprints/beta_readiness/P1-25_thyroid_completion_manifest.yaml`

Update:

`docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md`

Keep the register entry lightweight.

## Validation

Run all relevant existing validation.

At minimum:

* package validation for modified Knowledge Bus packages;
* PSI validation for new / modified PSI;
* signal library validation;
* compiled card validation;
* estate index validation;
* medical frame identity index validation if available;
* thyroid activation unit tests;
* thyroid gating regression tests;
* new P1-25 test file;
* architecture / governance tests required by Automation Bus finish;
* `python backend/scripts/run_work_package.py finish`.

Do not edit validators to force a pass.

## Acceptance criteria

P1-25 passes only if:

1. Front matter remains `risk_level: HIGH`, `change_type: MIXED`.
2. Automation Bus preflight passes.
3. MR-v2 authority is cited and used.
4. `ADR-THYROID-MR-V2-ACTIVATION-1.md` is created.
5. Existing ADRs are not destructively amended.
6. `signal_thyroid_tsh_context` remains excluded.
7. No TgAb or TPOAb euthyroid context is activated.
8. No frontend, Gemini, report prose or questionnaire files are modified.
9. FT3-low is only allowlisted if deterministic TSH-suppressed suppression is enforceable.
10. FT3-low suppresses when required context fields are absent.
11. FT3-low suppresses when TSH is absent.
12. FT3-low suppresses when FT4 is absent.
13. FT3-low suppresses when TSH is below lab-provided range.
14. FT3-low fires when all gates are satisfied.
15. FT3-low PSI wording is MR-v2 safe.
16. TPOAb is only allowlisted if TSH `above_max` mandatory gate is supported.
17. TPOAb suppresses when TSH is within range.
18. TPOAb suppresses when TSH is below range.
19. TPOAb suppresses when TSH is absent.
20. TPOAb suppresses when FT4 is absent.
21. TPOAb fires when TPOAb high + TSH high + FT4 present.
22. TPOAb PSI is created if TPOAb passes.
23. TPOAb PSI contains no prohibited diagnostic wording.
24. `pkg_kb59` behavioural impact is updated if activated.
25. Medical frame identity index is updated to match actual activation outcome.
26. Thyroid compiled card is enriched only for passing candidates.
27. P1-25 compile manifest is created if card enrichment occurs.
28. Estate index points to P1-25 manifest if card enrichment occurs.
29. Existing thyroid activation tests are updated correctly.
30. New P1-25 tests pass.
31. P1-25 carry-forward file records questionnaire alignment and any candidate stops.
32. Build register is updated concisely.
33. Final audit includes `pipeline_advisory_trigger` and `pipeline_advisory_reason`.

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
