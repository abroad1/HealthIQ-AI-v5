---
work_id: LC-S1-ANALYTICAL-HARDENING
branch: feature/lc-s1-analytical-hardening
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
agent_owner: healthiq-core-engine
primary_cursor_agent: healthiq-core-engine
requires_claude_audit: true
requires_gpt_architecture_review: true
---

# Sprint 1 — Launch-core analytical hardening

## SOP status

This work package is governed under the active Automation Bus / Knowledge Bus SOPs.

Before any file changes:
- verify the authoritative prompt path being used by the runtime/process
- verify the active work package state file exists and matches this `work_id` and `branch`
- verify work is not being performed on `main`
- verify the working tree is clean or intentionally governed
- follow the required two-phase start/finish lifecycle for HIGH-risk work

This is HIGH risk because it touches the analytical core and governed interpretation behaviour.

## Assigned execution agent

Use Cursor agent:

**`healthiq-core-engine`**

This is core analytical estate work, not frontend-shell work.

## Operational precondition

Do not begin Stage 3 execution until the currently active Q-2 token has been formally cleared via the required finish flow.

If Q-2 remains active, stop and report that the operational precondition is not yet satisfied.

## Objective

Harden the launch-core analytical slice so that the bounded proving use case has the governed WHY assets and analytical behaviour needed for end-to-end proving.

This sprint is:
- not broad WHY expansion
- not medication modifier implementation
- not frontend redesign
- not Layer C payload authoring

This sprint is targeted analytical completion for the approved proving slice.

## Approved decisions from the closed Pre-Sprint 1 gate

These are fixed inputs, not questions to reopen.

### 1. Launch-core biology slice
Approved bounded slice:
- homocysteine / methylation / cardiometabolic / lipid cluster
- based on the active signal set already proven on AB and VR

Use the approved launch-core signal set already recorded in the closed gate pack.

### 2. Frontend/report proving surface
All working parts needed to prove the pipeline are in scope for proving.
Do not artificially narrow the proving surface.

### 3. Medication category
- statins

### 4. Medication path sequencing
- statin prerequisites are **not Sprint 1 scope**
- they are deferred to a separate **pre-Sprint 2 gate**

Do not start building the statin modifier path in this sprint.

### 5. Silent-WHY policy
Sprint 1 must build the governed WHY assets needed to support:
- the chosen test panel
- the minimal proving questionnaire
- the drug-usage pathway

This is targeted WHY completion for the proving slice only.

### 6. `insights[]`
`insights[]` is being retired as an intelligence layer.
Do not build new logic around it.
Do not use it as a source of truth.

### 7. Layer B → Layer C rule
**Layer B decides. Layer C synthesises.**

Sprint 1 must not weaken this boundary.

## Scope

### In scope

1. Confirm the exact launch-core signal list from the closed gate pack and bind Sprint 1 work to it.
2. Identify which signals in that approved slice still lack governed WHY support.
3. Author the missing governed WHY assets required for the proving slice.
4. Ensure the analytical outputs required for AB/VR proving are complete and coherent for the approved slice.
5. Remove silent-WHY gaps within the approved slice.
6. Preserve deterministic analytical truth and existing governed outputs.
7. Add or update regression protection for the newly hardened launch-core analytical slice where appropriate.
8. Produce a concise audit trail of:
   - which signals were hardened
   - which WHY assets were added
   - which gaps remain intentionally deferred

### Explicitly out of scope

- full WHY Wave 2
- statin/drug modifier engine
- questionnaire schema expansion beyond what is strictly needed for Sprint 1 analytical compatibility review
- frontend carriage redesign
- Layer C payload redesign
- speculative expansion outside the approved slice
- reintroducing `insights[]` as a reasoning layer

## Required repo-grounded tasks

### A. Lock the approved signal set
Use the closed Pre-Sprint 1 pack as authority.

Translate the approved biology slice into the exact named signal list Sprint 1 will harden.

This list must be explicit in the implementation notes / completion report.

**Mandatory warning resolution:**
- explicitly verify the canonical LDL signal ID used by the runtime/compiler
- the gate pack references `signal_ldl_high`
- hardening must confirm whether the canonical ID is actually `signal_ldl_cholesterol_high` or another registered form
- do not proceed on naming assumption

### B. Identify remaining silent-WHY gaps inside the approved slice
Repo-ground and runtime-ground this.
Do not assume.

State clearly for each signal:
- signal ID
- current status
- whether WHY exists
- whether fallback is currently used
- whether the signal is visible on proving surfaces

### C. Build missing WHY assets only for the approved slice
Create the minimum governed assets needed so the approved slice is analytically complete for proving.

These assets must be medically disciplined and deterministic.
Do not write shallow filler WHYs just to tick the box.

**Mandatory warning resolution:**
- verify whether `signal_apoa1_cardio_risk` is truly registered and supportable for Sprint 1 WHY authoring
- confirm whether it has:
  - KB package support
  - SSOT presence
  - WHY loader path
- if not, document precisely and treat it as a scoped blocker or intentional deferral rather than improvising unsupported WHY authoring

### D. Preserve analytical coherence
Ensure the new WHY assets do not create:
- contradiction with existing top-finding ranking
- contradiction with domain scores
- contradiction with existing clinician-facing structured outputs
- contradiction with IDL / pattern outputs where already active

### E. Regression protection
Add or strengthen regression checks for the approved slice so the newly hardened WHY behaviour is protected.

This should be bounded and directly related to Sprint 1 work.
Do not turn this into a testing-estate redesign.

## Acceptance criteria

Sprint 1 is complete only if all of the following are true:

1. The approved launch-core signal list is explicitly documented.
2. Every signal in the approved Sprint 1 slice that needs governed WHY for proving now has governed WHY support, or is explicitly documented as intentionally deferred with justification.
3. No user-visible signal inside the approved proving slice is relying on the generic fallback because Sprint 1 failed to supply the necessary WHY asset.
4. AB and VR proving runs show the approved slice behaving coherently after the Sprint 1 changes.
5. No broad WHY expansion has occurred outside the approved slice.
6. No statin modifier implementation has been started in Sprint 1.
7. Regression checks protecting the newly hardened slice are added or updated.
8. A concise Sprint 1 completion note is produced.

## Required outputs

1. Updated governed WHY assets for the approved slice
2. Any necessary bounded analytical-core code changes required to support those assets
3. Regression tests/checks for the approved slice
4. A concise completion note covering:
   - exact signals hardened
   - exact WHY assets added/updated
   - proof that work remained inside approved scope
   - remaining intentional gaps
   - anything that should feed the pre-Sprint 2 statin gate

## Guardrails

- Do not expand scope because adjacent signals look interesting.
- Do not silently author WHY outside the approved slice.
- Do not solve Sprint 2 problems inside Sprint 1.
- Do not introduce demo-only logic.
- Do not alter ranking/interpretation rules casually while adding WHY assets.
- Do not use `insights[]` as an active design dependency.
- Do not weaken the Layer B / Layer C boundary.

## If blocked

If you discover that a required Sprint 1 completion item cannot be finished without violating scope, do not improvise a broad solution.

Instead:
- complete everything that remains valid within scope
- document the blocker precisely
- identify whether it should be handled by:
  - a small Sprint 1 addendum
  - the pre-Sprint 2 statin gate
  - or a later sprint

## Deliverable format back to leadership

When complete, report back in this structure:

### 1. Summary
- what was hardened
- whether Sprint 1 acceptance criteria were met

### 2. Exact signal list in scope
- approved named signals actually worked on
- include canonical ID confirmation where naming differed from the gate pack wording

### 3. WHY assets added or updated
- signal by signal

### 4. Regression protection added
- exact tests/checks

### 5. Remaining intentional gaps
- only those outside Sprint 1 scope

### 6. Risks / follow-ons
- especially anything relevant to the pre-Sprint 2 statin gate
- include any registration/SSOT/KB-path issue affecting ApoA1-related work

### 7. Branch / working tree / SOP status
- confirm governed execution under the correct branch and active work package state