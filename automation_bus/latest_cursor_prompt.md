---
work_id: P1-22
branch: sprint/P1-22-thyroid-activation-pack
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: BEHAVIOUR
---

# P1-22 — Thyroid Activation Pack

You are Cursor, acting as the Core Engine implementation agent with Knowledge Bus / governance read-only support.

Implement this work package under Automation Bus SOP v1.3.1.

This is an outcome-based runtime activation sprint.

It is not a Knowledge Bus package-promotion sprint.
It is not a frontend sprint.
It is not a Gemini/report-prose sprint.
It is not a Medical Review sprint.

## Purpose

Deliver `wave1_thyroid` as an active launch-core runtime domain by bundling the necessary preconditions and implementation into one governed package:

1. populate the hormonal `lab_range_only` scoring rail for the thyroid-axis marker set;
2. record a bounded TSH authority decision;
3. implement the `wave1_thyroid` domain assembler/card/subsystem routing;
4. enable TSH, FT4 and FT3-high-safe thyroid scoring/firing where authorised;
5. keep TSH signal intelligence and FT3 low runtime activation explicitly deferred.

This sprint must not split hormonal scoring, TSH authority, and thyroid domain activation into separate micro-sprints. They are internal phases of one outcome-based package.

## Stage 0 / Stage B baseline

The v0.5 Stage 0 pipeline advisory reduced the previous thyroid sequence into one outcome-based P1-22 package by absorbing:

* hormonal scoring policy;
* TSH launch-authority decision;
* thyroid domain card retry.

Stage B Mode 1 confirmed this shape with amendments:

1. TSH scoring and TSH signal intelligence must be distinguished.
2. FT3 high is already cleared by ADR, with mandatory TSH-suppressed companion gate.
3. FT3 low remains deferred and excluded.
4. `lab_range_only` is first production use, so schema must be verified before scoring-policy writes.

## Mandatory read list

Read before editing:

* `automation_bus/latest_pipeline_advisory.md`
* `automation_bus/latest_scope_advisory.md`
* `docs/discussion documents/healthiq_pre_sop_prompt_scoping_workflow_v0_5.md` if present, otherwise v0.4 plus amended §6 notes
* `docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md`
* P1-8 scoring ADR / scoring sprint report / scoring implementation notes
* `docs/architecture/ADR-THYROID-FT3-AUTHORITY-RECONCILIATION-1.md`
* any existing thyroid ADRs, thyroid sprint reports or P1-4 blocker reports
* `backend/ssot/scoring_policy.yaml`
* scoring policy validator and schema code used for `scoring_type: lab_range_only`
* current scoring tests
* current domain score assembler / domain card / subsystem routing code
* existing launch-core domain examples to mirror implementation pattern
* current thyroid-related Knowledge Bus package manifests / signal libraries as read-only evidence only
* current thyroid-related tests

Use targeted search:

* `rg "lab_range_only|hormonal|scoring_type|scoring_policy" backend docs`
* `rg "wave1_thyroid|thyroid|TSH|FT4|FT3|free_t3|free_t4|thyroid_stimulating" backend docs knowledge_bus`
* `rg "FT3 low|FT3 high|TSH suppressed|TSH-suppressed|companion gate" docs backend knowledge_bus`
* `rg "wave1_.*domain|domain card|domain_score_assembler|subsystem routing" backend`
* `rg "pkg_kb52c.*tsh|signal_tsh|signal_ft4|signal_ft3" knowledge_bus docs backend`

Inspect relevant hits before editing.

## Files in scope

Allowed if justified:

* `backend/ssot/scoring_policy.yaml`
* scoring policy schema/validator files only if required to support existing P1-8 `lab_range_only` contract without weakening validation
* backend domain assembler / domain card / subsystem routing files required to implement `wave1_thyroid`
* backend tests for scoring policy, thyroid domain routing, signal gating and regression coverage
* concise ADR / decision note for bounded TSH launch treatment:

  * use existing ADR location if present;
  * otherwise create under `docs/architecture/`
* `docs/sprints/beta_readiness/P1-22_thyroid_activation_pack.md`
* `docs/sprints/beta_readiness/P1-22_thyroid_activation_manifest.yaml`
* `docs/sprints/beta_readiness/P1-22_pass3_carry_forward.yaml`
* `docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md`

## Files out of scope

Do not modify:

* frontend/
* Gemini files
* report prose / DTO presentation files unless hardening proves they are part of backend card DTO contract and unavoidable
* raw Pass 3 research
* Knowledge Bus package medical content
* Knowledge Bus `signal_library.yaml`
* Knowledge Bus `research_brief.yaml`
* Knowledge Bus `promoted_signal_intelligence.yaml`
* Knowledge Bus package manifests except read-only inspection
* generated-pilot files
* parser files
* TSAT / transferrin saturation policy
* iron/ferritin/CBC packages
* ferritin-low packages
* `.codex/`
* `.cursor/`
* `.vscode/`
* `AGENTS.md`

## Critical clinical / architectural boundaries

### TSH boundary

TSH participates in hormonal `lab_range_only` scoring at launch.

TSH signal intelligence is not promoted in this sprint.

The bounded TSH decision must state:

* TSH enters the `lab_range_only` scoring policy;
* TSH signal intelligence from kb52c packages remains deferred;
* the thyroid domain card must not imply that TSH clinical-context intelligence is active at launch;
* TSH can contribute lab-range scoring/status only.

STOP if domain card wording, DTO fields, assembler wiring or tests imply that TSH signal intelligence / kb52c clinical context is active at launch.

### FT4 boundary

FT4 may enter the hormonal `lab_range_only` scoring rail and `wave1_thyroid` domain routing where existing authority supports launch use.

Do not alter FT4 Knowledge Bus medical content.

### FT3 boundary

FT3 high is already cleared by ADR with a mandatory TSH-suppressed companion gate.

P1-22 must treat FT3 high as eligible for:

* hormonal `lab_range_only` scoring;
* `wave1_thyroid` domain allowlist;
* only with the mandatory TSH-suppressed companion gate required by ADR.

FT3 low remains excluded from all domain allowlists.

No FT3 low runtime activation path may be introduced in P1-22.

STOP if implementation would activate FT3 low, imply FT3 low launch visibility, or remove/loosen the mandatory TSH-suppressed companion gate for FT3 high.

### Lab-range authority

Lab-provided reference ranges remain authoritative.

Do not introduce global/default thyroid reference ranges.

Do not calculate clinical normality from non-lab reference bands.

Do not add hardcoded thyroid ranges unless they are test fixtures clearly isolated from production scoring.

## Phase 0 — Automation Bus preflight

Before implementation:

1. Confirm current branch is:

`sprint/P1-22-thyroid-activation-pack`

2. Confirm `automation_bus/state/work_package_active.json` exists.
3. Confirm active token has `work_id: P1-22`.
4. Confirm token branch matches current branch.
5. Confirm repo/stash/parked-file state is governed under the standard start prompt.

If any condition fails, STOP.

## Phase 1 — Scoring policy schema and authority gate

Phase 1 must complete and validate before Phase 2 begins.

### 1A — Confirm `lab_range_only` schema before writing

Before editing `backend/ssot/scoring_policy.yaml`, inspect the P1-8 scoring policy validator/schema and confirm the required YAML shape for `scoring_type: lab_range_only`.

Record in:

`docs/sprints/beta_readiness/P1-22_thyroid_activation_manifest.yaml`

For the schema record:

* required fields;
* forbidden fields;
* whether hardcoded `bands` are omitted;
* how lab-provided ranges are consumed;
* validation command to prove correctness.

STOP if the schema is ambiguous, unsupported or would require inventing hardcoded ranges.

### 1B — Confirm marker set

Confirm the Phase 1 scoring-policy marker set:

* TSH — scoring only; no signal intelligence;
* FT4 — scoring and domain use where authorised;
* FT3 high — scoring and domain use with mandatory TSH-suppressed companion gate;
* FT3 low — excluded/deferred.

Record the marker decision in the activation manifest.

STOP if repo evidence contradicts this boundary.

### 1C — Populate hormonal scoring rail

Populate `backend/ssot/scoring_policy.yaml` for the confirmed thyroid-axis marker set using `scoring_type: lab_range_only`.

Do not add hardcoded production bands.

Do not change unrelated scoring rails or unrelated biomarker scoring policy.

If a marker cannot be represented cleanly under `lab_range_only`, STOP for that marker and carry it forward.

### 1D — Bounded TSH authority decision

Create a concise ADR / decision note for TSH launch treatment.

The ADR must state:

* TSH enters lab-range-only scoring at launch;
* TSH signal intelligence is not promoted in P1-22;
* TSH kb52c clinical context remains deferred;
* thyroid domain output must not imply TSH signal intelligence is present;
* P1-22 may use TSH as scoring/status context only.

Keep this ADR concise.

Do not create a broad thyroid medical authority paper.

### 1E — Phase 1 validation gate

Run scoring-policy validation and relevant scoring tests.

Required proof:

* `lab_range_only` entries validate;
* lab-provided ranges remain authoritative;
* no global/default ranges added;
* no unrelated scoring behaviour changed unexpectedly;
* FT3 low remains excluded;
* FT3 high retains mandatory TSH-suppressed companion gate;
* TSH signal intelligence remains deferred.

If Phase 1 validation fails, STOP. Do not proceed to Phase 2.

## Phase 2 — Thyroid runtime domain activation

Proceed to Phase 2 only after Phase 1 passes.

### 2A — Implement `wave1_thyroid`

Implement the thyroid launch-core domain following established launch-core domain patterns.

Expected runtime/product output:

* `wave1_thyroid` domain active;
* thyroid domain assembler/card/subsystem routing implemented;
* TSH scoring/status visible only as lab-range-only scoring, not signal intelligence;
* FT4 scoring/firing visible where authorised;
* FT3 high scoring/firing visible only with mandatory TSH-suppressed companion gate;
* FT3 low absent from allowlists and not launch-visible.

### 2B — Tests

Add/update tests proving:

* thyroid domain appears as active launch-core domain;
* TSH lab-range-only scoring works without implying TSH signal intelligence;
* FT4 thyroid scoring/routing works;
* FT3 high requires mandatory TSH-suppressed companion gate;
* FT3 low does not activate and is not in thyroid domain allowlists;
* lab-provided ranges remain authoritative;
* no global/default ranges introduced;
* existing launch-core domains are not regressed;
* scoring policy validation passes;
* snapshot/replay or domain assembler tests are updated only where expected.

### 2C — No frontend/report prose work

Do not implement frontend display changes, Gemini wording, report prose or marketing copy.

If backend DTO/card contract must expose thyroid domain data for existing render-only frontend to consume, keep it minimal and backend-contract focused.

## Phase 3 — Carry-forward manifest

Create:

`docs/sprints/beta_readiness/P1-22_pass3_carry_forward.yaml`

Include only material unresolved items.

Expected carry-forwards may include:

* TSH signal intelligence / kb52c promotion deferred;
* FT3 low runtime activation deferred;
* any thyroid marker unable to enter `lab_range_only` scoring safely;
* any domain routing issue blocked by external authority.

For each item record:

* item ID;
* marker/package reference;
* reason not implemented;
* blocker class;
* owner agent:

  * Core Engine
  * Knowledge Bus
  * Medical Review
  * Frontend/Presentation
* launch/beta relevance;
* recommended future package.

Do not re-document unrelated iron/ferritin/CBC carry-forwards.

## Phase 4 — Sprint report and build register

Create:

`docs/sprints/beta_readiness/P1-22_thyroid_activation_pack.md`

Keep it concise.

Maximum structure:

1. start state;
2. Phase 1 scoring/authority outcome;
3. Phase 2 runtime activation outcome;
4. marker boundary decisions;
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

P1-22 passes only if:

1. `lab_range_only` schema is verified before scoring-policy edits.
2. Hormonal scoring rail is populated only for authorised thyroid-axis marker scope.
3. TSH enters scoring only, not signal intelligence.
4. TSH authority decision note records signal intelligence deferral.
5. Domain output does not imply TSH kb52c clinical context is active.
6. FT4 is included only where launch authority supports it.
7. FT3 high is included with mandatory TSH-suppressed companion gate.
8. FT3 low remains excluded from all allowlists and activation paths.
9. No global/default thyroid reference ranges are introduced.
10. Lab-provided ranges remain authoritative.
11. Phase 1 validation passes before Phase 2 begins.
12. `wave1_thyroid` domain is active at runtime after Phase 2.
13. Thyroid domain assembler/card/subsystem routing is implemented.
14. Tests prove thyroid domain activation.
15. Tests prove TSH scoring without TSH signal intelligence.
16. Tests prove FT3 high companion-gate behaviour.
17. Tests prove FT3 low remains inactive/deferred.
18. Existing launch-core domains do not regress.
19. No Knowledge Bus medical content is edited.
20. No raw Pass 3 research is edited.
21. No frontend/Gemini/report prose work is introduced.
22. Carry-forward manifest captures deferred thyroid items with owner and blocker class.
23. Build register is updated concisely.
24. Sprint report is concise.
25. Final audit includes `pipeline_advisory_trigger` and `pipeline_advisory_reason`.

## Validation commands

Run all relevant existing validation commands.

At minimum:

* scoring policy validator / schema validation command identified in Phase 1A;
* relevant scoring policy tests;
* thyroid domain/domain assembler tests;
* regression tests for launch-core domain routing;
* architecture/governance tests required by Automation Bus finish;
* `python backend/scripts/run_work_package.py finish`.

Do not invent new validation tooling unless existing test patterns require a new test file.

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
