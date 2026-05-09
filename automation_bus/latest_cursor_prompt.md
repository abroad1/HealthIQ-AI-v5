---
work_id: LC-S2-CONTEXT-INTEGRATION
branch: feature/lc-s2-context-integration
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
agent_owner: healthiq-core-engine
primary_cursor_agent: healthiq-core-engine
requires_claude_audit: true
requires_gpt_architecture_review: true
---

# Sprint 2 — Launch-core context integration

## SOP status

This work package is governed under the active Automation Bus / Knowledge Bus SOPs.

Before any file changes:
- verify the authoritative prompt path being used by the runtime/process
- verify the active work package state file exists and matches this `work_id` and `branch`
- verify work is not being performed on `main`
- verify the working tree is clean or intentionally governed
- follow the required two-phase start/finish lifecycle for HIGH-risk work

This is HIGH risk because it changes live analytical-context wiring, report carriage, and governed interpretation flow.

## Assigned execution agent

Use Cursor agent:

**`healthiq-core-engine`**

This is analytical/context pipeline work with DTO/report-surface implications, not a frontend-shell-only task.

## Objective

Implement the real, production-grade statin context path for the launch-core slice.

Sprint 2 must wire the already-existing governed statin assets and annotation compiler through the live pipeline so that statin-on vs statin-off produces deterministic, user-visible context changes without mutating analytical truth.

This sprint is not about inventing statin science.
The governed statin truth already exists.
This sprint is about making the real path work end to end.

## Gate authority

This sprint may proceed because the Pre-Sprint 2 statin gate is closed.

Use the closed statin gate pack as binding authority.

## Fixed inputs from the closed statin gate

These are not open questions.

### 1. Statin questionnaire capture
Approved:
- add **“Statins (cholesterol medication)”** to the existing `long_term_medications` checkbox
- do not create a standalone statin question

### 2. Governed statin truth location
Approved:
- use existing governed asset(s)
- do not author new statin-effect science unless an unexpected hard blocker forces a separately governed follow-up

### 3. Modifier engine approach
Approved:
- wire the existing architecture
- do not build a separate ad hoc statin engine
- do not use sprint-only shortcuts

### 4. Minimum affected outputs
Approved:
- clinician surface
- plus as many consumer-visible fields as are naturally relevant to the medication prose
- do not artificially constrain the statin path to only one consumer field if multiple launch-core fields should properly change

### 5. Allowed effect type
Approved:
- statin context may change interpretation framing, confidence/context explanation, and follow-up wording where governed
- statin context must not mutate signal firing, domain bands, rankings, or analytical truth

### 6. Layer B / Layer C rule
Approved:
- Layer B decides
- Layer C synthesises

Statin context is a Layer B deterministic annotation.
Layer C may narrate it, not invent it.

### 7. Proving checks
Approved:
- S-1 through S-6 as written in the closed statin gate pack

## Verified current-state starting point

Use the closed statin gate pack as source of truth, including these starting facts:

- statin governed truth already exists in the intervention effects registry
- statin alias map already exists
- intervention annotation compiler already exists and is tested
- current production gap is missing pipeline wiring:
  - no statin questionnaire capture
  - no mapper path to `user_intervention_document`
  - no orchestrator pass-through
  - no `AnalysisDTO` carriage for the annotation
  - no live clinician / consumer surface reading the annotation

## Scope

### In scope

1. Add statin capture to the existing questionnaire path.
2. Extend the questionnaire mapper to build a valid `user_intervention_document` for statin-on responses.
3. Pass that document through the live orchestrator path.
4. Ensure the existing intervention annotation compiler is invoked in the live production path.
5. Expose the resulting statin annotation through the production DTO / output path.
6. Make clinician-facing output reflect statin context where appropriate.
7. Make all relevant consumer-visible launch-core fields reflect statin context where appropriate.
8. Add bounded proving/regression coverage for the statin-on vs statin-off path.
9. Produce a concise completion note and explicit proof against checks S-1 through S-6.

### Explicitly out of scope

- broad medication ontology expansion
- free-text medication entry
- named-drug alias resolution at intake
- additional drug categories beyond statins
- signal-threshold mutation
- band/ranking mutation
- broad questionnaire redesign beyond the approved statin checkbox addition
- non-statin intervention content authoring
- speculative frontend redesign outside launch-core surfaces

## Required implementation tasks

### A. Questionnaire capture
Implement the approved questionnaire change:
- add **“Statins (cholesterol medication)”** to the existing `long_term_medications` checkbox

Do not introduce a new standalone question.

### B. Mapper output
Extend the questionnaire mapper so a statin-on response produces a valid `user_intervention_document` with the correct governed class mapping:

- `intervention_class_id: lipid_lowering_statin`
- `link_status: mapped`

This must use the real production document shape.

### C. Orchestrator wiring
Wire the live orchestrator path so the `user_intervention_document` reaches the existing intervention annotation compiler.

Do not create a side-path or debug-only path.

### D. DTO / contract propagation
Expose the statin annotation through the live production output path.

If `AnalysisDTO` needs to carry `intervention_annotations_v1`, do it cleanly and explicitly using the real contract shape.

Do not invent a temporary parallel field.

### E. Clinician surface
Ensure clinician-facing structured output reflects statin context where relevant.

This should be a real clinician-grade context statement, not vague prose.

### F. Consumer-visible surfaces
Ensure all launch-core consumer-visible fields that are naturally affected by statin context are updated accordingly.

Do not artificially constrain this to a single field if multiple consumer-facing fields should legitimately reflect the annotation.

But also do not spray statin prose everywhere unnecessarily.

### G. Boundary discipline
Preserve the approved statin boundary:
- annotation/context only
- no mutation of signal firing
- no mutation of ranking
- no mutation of domain score banding
- no Layer C invention

### H. Regression / proving protection
Add bounded tests for:
- S-1 questionnaire capture
- S-2 mapper output
- S-3 annotation compiler resolution
- S-4 pipeline carriage
- S-5 visible difference between statin-on and statin-off
- S-6 no analytical truth mutation from statin annotation alone

Keep this bounded.
Do not redesign Sentinel broadly.

## Acceptance criteria

Sprint 2 is complete only if all of the following are true:

1. The questionnaire includes **“Statins (cholesterol medication)”** in the approved place.
2. A statin-on questionnaire response produces a valid `user_intervention_document` with `lipid_lowering_statin`.
3. The live pipeline invokes the existing intervention annotation compiler and carries the resulting annotation forward.
4. The production DTO/output path exposes the statin annotation cleanly.
5. Clinician-facing output changes appropriately when statin context is present.
6. All relevant consumer-visible launch-core fields change appropriately when statin context is present.
7. A statin-on vs statin-off comparison produces at least one user-visible difference.
8. Rankings, signal states, and domain bands remain unchanged by statin annotation alone.
9. No sprint-only stub, hardcoded shortcut, or fake statin logic is introduced.
10. A concise Sprint 2 completion note is produced.

## Required outputs

1. Questionnaire update for statin capture
2. Mapper update producing valid `user_intervention_document`
3. Orchestrator wiring for intervention annotation path
4. DTO / contract propagation update if required
5. Clinician + consumer surface updates
6. Bounded tests for S-1 through S-6
7. Sprint 2 completion note

## Guardrails

- Do not build a new statin science layer.
- Do not change the locked governed statin registry unless a genuine hard blocker forces separately governed follow-up.
- Do not mutate analytical truth.
- Do not fake visible payoff.
- Do not constrain consumer carriage to one field if more are naturally affected.
- Do not widen into multi-medication support.
- Do not turn this into a general questionnaire redesign.
- Do not weaken the Layer B / Layer C boundary.

## If blocked

If a required Sprint 2 completion item cannot be achieved without violating scope:
- complete everything else that remains valid
- document the blocker precisely
- identify whether it needs:
  - a small Sprint 2 addendum
  - a new governed follow-up
  - or a later sprint

Do not improvise a broad workaround.

## Deliverable format back to leadership

When complete, report in this structure:

### 1. Summary
- what was implemented
- whether Sprint 2 acceptance criteria were met

### 2. Questionnaire capture
- exact change made

### 3. Mapper / document path
- how statin-on responses now map to `user_intervention_document`

### 4. Pipeline wiring
- how the annotation now travels through the live path

### 5. Surface changes
- clinician-facing changes
- consumer-facing changes

### 6. Tests added or updated
- exact tests for S-1 through S-6

### 7. Remaining intentional gaps
- only those outside Sprint 2 scope

### 8. Risks / follow-ons
- especially anything that affects later medication-category expansion

### 9. Branch / working tree / SOP status
- confirm governed execution under the correct branch and active work package state