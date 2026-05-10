---
work_id: LC-OBS2-QUESTIONNAIRE-SEMANTICS-INVESTIGATION
branch: feature/lc-obs2-questionnaire-semantics-investigation
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
agent_owner: healthiq-qa-uat
primary_cursor_agent: healthiq-qa-uat
requires_claude_audit: true
requires_gpt_architecture_review: true
---

# LC-OBS2 — Questionnaire semantics investigation

## SOP status

This work package is governed under the active Automation Bus / Knowledge Bus SOPs.

Before any file changes:
- verify the authoritative prompt path being used by the runtime/process
- verify the active work package state file exists and matches this `work_id` and `branch`
- verify work is not being performed on `main`
- verify the working tree is clean or intentionally governed
- follow the required two-phase start/finish lifecycle for HIGH-risk work

This is HIGH risk because it may touch live questionnaire semantics and context interpretation behaviour.

## Assigned execution agent

Use Cursor agent:

**`healthiq-qa-uat`**

This is a bounded behavioural investigation of launch-core pipeline semantics, not a new feature sprint.

## Objective

Investigate OBS-2 surfaced by the launch-core proving harness:

- AB band label diverges between:
  - baseline = no questionnaire data
  - statin_off = explicit `"None"` style questionnaire response

Determine whether this divergence is:

1. expected product semantics
2. an unintended behavioural inconsistency
3. a fixture/harness artefact
4. a mapper/orchestrator/questionnaire-normalisation issue

This package is primarily an **investigation and clarification** package.  
Do not assume the outcome is “fix it.”  
First establish whether the behaviour is correct.

## Background

The proving harness surfaced OBS-2 and preserved it in:
- `docs/sprints/LC-PROVING-HARNESS-AUTOMATION_completion_2026-05.md`
- `docs/audit-papers/launch-core-proving/PROVING_REPORT.md`

The key question is:

**Should “no questionnaire provided” and “explicitly answered none” be treated as equivalent by the live pipeline, or not?**

The harness has done its job by exposing the difference.
This package determines whether the difference is correct.

## Scope

### In scope

1. Reproduce OBS-2 cleanly.
2. Trace the behavioural difference through the real pipeline.
3. Identify the first point at which:
   - no-questionnaire state
   - explicit-none state
   diverge.
4. Determine whether that divergence is intentional, documented, and product-correct.
5. Recommend one of:
   - retain behaviour and document it
   - normalise the two states to equivalence
   - narrow fix in mapper/orchestrator/questionnaire semantics
6. Add or update a bounded test that locks the intended behaviour once decided.
7. Produce a concise investigation note.

### Explicitly out of scope

- broad questionnaire redesign
- multi-medication expansion
- statin-path redesign
- new proving harness work
- broad analytics refactor
- opportunistic fixing of unrelated questionnaire behaviours

## Required method

### A. Reproduce the issue
Use the proving harness or the smallest equivalent real-pipeline run to reproduce:
- AB baseline with no questionnaire payload
- AB explicit-none equivalent payload

Make the comparison explicit.

### B. Trace the divergence
Inspect and trace the semantics through the relevant live path, including as needed:
- questionnaire intake shape
- questionnaire mapper
- orchestrator
- any lifestyle / context defaulting logic
- any domain-score assembly inputs
- DTO/report assembly

The goal is to identify the exact reason the band label diverges.

### C. Establish intended semantics
Use the current product/gate docs and repo logic to answer:

- is absence of questionnaire data supposed to mean “unknown / no evidence”
- is explicit-none supposed to mean “known negative / user denied factor”
- should those differ in scoring/context
- if so, where is that rule actually expressed
- if not, where is the accidental divergence being introduced

### D. Decide whether code change is needed
If the behaviour is correct:
- do not “fix” it
- instead document it and add a test that locks it

If the behaviour is incorrect:
- implement the smallest clean correction at the right layer
- then add a test that locks the corrected semantics

### E. Keep this bounded
This is an OBS-2 investigation package, not a new feature sprint.

## Acceptance criteria

This package is complete only if all of the following are true:

1. OBS-2 is reproducibly explained.
2. The first semantic divergence point is identified.
3. A clear conclusion is reached:
   - expected behaviour
   - or real inconsistency
4. If no code change is required, the intended behaviour is documented and test-protected.
5. If a code change is required, the narrowest correct fix is implemented and test-protected.
6. No unrelated questionnaire or analytics behaviour is changed.
7. A concise investigation/completion note is produced.

## Required outputs

1. Reproduction evidence for OBS-2
2. Root-cause explanation
3. Decision on intended semantics
4. Narrow fix or documentation update, as appropriate
5. Bounded regression test locking the intended behaviour
6. Completion note

## Guardrails

- Do not assume “difference = bug.”
- Do not assume “same label = correct.”
- Do not widen into general questionnaire semantics.
- Do not alter statin-path behaviour unless the OBS-2 root cause truly requires it.
- Do not redesign the proving harness.

## Deliverable format back to leadership

When complete, report in this structure:

### 1. Summary
- what OBS-2 turned out to be
- whether code change was required

### 2. Reproduction
- exact scenarios used
- what differed

### 3. Root cause
- first point of semantic divergence
- why it happens

### 4. Decision
- expected behaviour or inconsistency
- rationale

### 5. Action taken
- code change / test / docs update
- exact files

### 6. Protection added
- exact test(s) added or updated

### 7. Remaining implications
- only if this affects later questionnaire or proving work

### 8. Branch / working tree / SOP status
- confirm governed execution under the correct branch and active work package state