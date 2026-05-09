---
work_id: LC-PROVING-HARNESS-AUTOMATION
branch: feature/lc-proving-harness-automation
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
agent_owner: healthiq-qa-uat
primary_cursor_agent: healthiq-qa-uat
requires_claude_audit: true
requires_gpt_architecture_review: true
---

# Launch-core proving harness automation

## SOP status

This work package is governed under the active Automation Bus / Knowledge Bus SOPs.

Before any file changes:
- verify the authoritative prompt path being used by the runtime/process
- verify the active work package state file exists and matches this `work_id` and `branch`
- verify work is not being performed on `main`
- verify the working tree is clean or intentionally governed
- follow the required two-phase start/finish lifecycle for HIGH-risk work

This is HIGH risk because it affects how the product is validated going forward and may touch protected verification, fixture, and reporting paths.

## Assigned execution agent

Use Cursor agent:

**`healthiq-qa-uat`**

This is proving/verification automation work, not intelligence expansion and not a frontend-only task.

## Objective

Build a repeatable, fixture-driven proving harness for the launch-core slice so Anthony does not need to manually upload panels and fill in questionnaires to validate end-to-end behaviour.

The harness must run a bounded matrix of fixed scenarios and produce a compact, human-readable comparison output showing:

- what changed
- what stayed stable
- whether expected context effects appeared
- whether analytical truth stayed intact where required

This is not a demo script.
It is a production-grade proving tool for the current launch-core pathway.

## Why this exists

The programme has now completed:
- Sprint 1 launch-core analytical hardening
- Sprint 2 statin context integration

The next need is not more manual clicking.  
It is a governed way to repeatedly prove the slice using fixed fixtures and scenario payloads.

Human review should become:
- review the proving output
- decide whether it is correct

not:
- repeatedly key in panels and questionnaires by hand

## Fixed programme assumptions

These are binding inputs, not open questions:

### 1. The launch-core slice already exists
The proving harness is validating the current launch-core slice, not inventing a new one.

### 2. Statin context is now on the mainline
The harness must include statin-on / statin-off proving scenarios.

### 3. Questionnaire proving must stay minimal
The harness should use a very small number of fixed questionnaire payloads, not a giant scenario library.

### 4. Layer B / Layer C boundary remains binding
The harness must be able to show that context changes produce appropriate wording differences without mutating analytical truth where they should not.

### 5. Human proving remains necessary
The harness does not replace judgement.
It replaces repetitive manual setup.

## Scope

### In scope

1. Define a bounded launch-core proving scenario matrix.
2. Encode the matrix as fixed fixtures / payloads.
3. Run those scenarios automatically through the real pipeline.
4. Produce a compact comparison output suitable for human review.
5. Show both:
   - expected differences
   - expected invariants
6. Reuse existing verification tooling where sensible.
7. Keep the harness narrow, deterministic, and easy to rerun.

### Explicitly out of scope

- full UAT framework redesign
- broad Sentinel redesign
- broad fixture explosion across many panels and personas
- new analytical logic
- new questionnaire strategy
- new medication categories beyond the already approved launch-core context path
- frontend redesign
- ad hoc one-off notebooks/scripts that are not fit to live in the repo

## Required proving matrix

At minimum, support a bounded matrix around the current launch-core panels:

### Panels
- AB
- VR

### Scenario types
At minimum:
1. baseline
2. lifestyle/context variant
3. statin-off
4. statin-on

Use the smallest scenario matrix that still proves:
- questionnaire/lifestyle payoff
- statin payoff
- analytical invariants

Do not create a huge matrix unless a very small matrix is clearly insufficient.

## Required outputs of the harness

For each scenario run, capture and compare at least:

- top findings
- consumer domain scores
- lead / retail narrative summary fields
- clinician summary surface
- IDL / interpretation pattern surface where relevant
- intervention/statin-related wording where present

The comparison output must make it easy to see:

### Expected changes
Examples:
- statin context wording appears
- lifestyle/alcohol context wording appears
- relevant clinician summary wording changes

### Expected invariants
Examples:
- top-finding order unchanged where required
- signal states unchanged where required
- domain band labels unchanged where required

## Implementation requirements

### A. Reuse before rebuilding
Inspect the current verification tooling and reuse existing pieces where sensible, especially:
- recovered verification scripts
- any golden-panel or ledger tooling already on `main`
- existing fixture assets

Do not rebuild equivalent plumbing unnecessarily.

### B. Real pipeline only
The harness must run the real current launch-core pipeline, not a mocked shadow path.

### C. Deterministic scenario payloads
Scenario definitions must be fixed, reviewable, and easy to rerun.
No manual UI entry required.

### D. Human-readable output
The final output should be understandable by Anthony without deep technical digging.
A compact markdown or similarly readable comparison summary is preferred.

### E. Bounded but extensible
The harness should be built in a shape that can later expand to more panels/scenarios, but do not overbuild that future now.

## Acceptance criteria

This work package is complete only if all of the following are true:

1. A bounded proving matrix exists for the current launch-core slice.
2. AB and VR can be run through the harness without manual UI data entry.
3. Lifestyle/context and statin scenarios are included.
4. The output clearly distinguishes:
   - expected changes
   - expected invariants
5. The output is human-reviewable, not raw debug noise.
6. The harness uses the real pipeline.
7. The harness is committed as a maintainable repo asset, not an ad hoc local script.
8. A concise completion note explains:
   - scenario matrix
   - tooling used
   - output format
   - how to rerun it

## Required outputs

1. Bounded proving harness implementation
2. Fixed scenario definitions / payloads
3. Human-readable comparison output format
4. Any required bounded tests for the harness itself
5. Completion note with rerun instructions

## Guardrails

- Do not turn this into a broad testing platform project.
- Do not use stashes as a convenience mechanism during start.
- Do not widen scope into general product analytics.
- Do not create a harness that only works for one run and is then forgotten.
- Do not introduce fake test-only product behaviour.
- Do not require Anthony to manually drive the scenarios through the UI.

## If blocked

If the harness cannot be built cleanly without a wider architectural change:
- complete the bounded parts that are still valid
- document the blocker precisely
- identify whether it should be:
  - a small addendum
  - a follow-on proving sprint
  - or a later infrastructure task

Do not improvise a large hidden redesign.

## Deliverable format back to leadership

When complete, report in this structure:

### 1. Summary
- what proving harness was built
- whether acceptance criteria were met

### 2. Scenario matrix
- exact panels and scenarios included

### 3. Tooling / assets used
- what existing verification tooling was reused
- what new assets were added

### 4. Output format
- what the human reviewer sees
- how expected changes/invariants are shown

### 5. Rerun method
- exact command or procedure to run the harness again

### 6. Remaining gaps
- only those outside this bounded proving-harness scope

### 7. Branch / working tree / SOP status
- confirm governed execution under the correct branch and active work package state