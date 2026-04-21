---
work_id: N-3
branch: feature/n-3-longitudinal-contract-upgrade
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# N-3 — Longitudinal contract upgrade

## Objective

Upgrade the deterministic longitudinal contract layer so HealthIQ can support benchmark-grade prior/current comparison, including raw numeric deltas, pathway-level persistence/improvement logic, and future narrative compilation.

This is the first implementation sprint in the deterministic narrative workstream.

It is a HIGH-risk sprint because it is expected to touch backend contracts and analytical infrastructure.

This sprint is not a frontend sprint.
Do not redesign the results page.
Do not introduce Gemini or any other LLM dependency.
Do not widen into full narrative compilation.

The purpose of N-3 is to solve the contract and data-shape gap that currently prevents deterministic benchmark-style longitudinal narration such as:
- “creatinine improved from 110 to 87”
- “HbA1c improved from 32 to 26”
- “this pathway remains unresolved despite broader systemic improvement”

---

## Strategic context already settled

The following are already decided and are not open for reinterpretation in this sprint:

- The benchmark narrative is locked.
- The merged reverse-engineering matrix is locked.
- The narrative compiler architecture is now defined in:
  - `docs/golden-narrative/HealthIQ_Deterministic_Narrative_Compiler_Architecture_v1.md`
- The architecture decision is to introduce a separate narrative compiler module rather than overload `report_compiler_v1.py`.
- The merged planning authority identified a specific longitudinal gap:
  - current prior snapshot support preserves status/score metadata
  - but does not preserve raw prior numeric values sufficiently for benchmark-style delta narration
- N-3 exists to close that gap at the contract/data layer before later compiler sprints.

Your job is to implement the minimum clean contract/data upgrade that makes deterministic longitudinal narrative support possible.

---

## Required inputs

Treat the following as required inputs:

1. Benchmark target lock
`docs/golden-narrative/AB_GOLD_STANDARD_NARRATIVE_TARGET_LOCK.md`

2. Merged reverse-engineering matrix
`docs/golden-narrative/AB_GOLD_STANDARD_NARRATIVE_REVERSE_ENGINEERING_MERGED.md`

3. Final sprint strategy
`docs/golden-narrative/HealthIQ_Deterministic_Narrative_Sprint_Strategy_FINAL.md`

4. Narrative compiler architecture
`docs/golden-narrative/HealthIQ_Deterministic_Narrative_Compiler_Architecture_v1.md`

5. Current runtime files expected to be relevant
At minimum inspect and use:
- `backend/core/contracts/insight_graph_v1.py`
- `backend/core/analytics/snapshot_linker.py`
- `backend/core/analytics/state_transition_engine.py`
- `backend/core/contracts/state_transition_v1.py`
- `backend/core/dto/builders.py`
- any analysis-result persistence or prior-snapshot loading path you determine is authoritative
- any tests already covering snapshot linking / state transitions / longitudinal behaviour

---

## Core problem this sprint must solve

Current longitudinal support is not enough for benchmark-grade narrative because prior/current snapshot handling preserves normalized status/score-style metadata but not a clean raw-value layer suitable for deterministic numeric delta narration.

This sprint must determine and implement the correct safe shape for preserving and exposing the longitudinal numeric facts needed for later narrative compilation.

It must also avoid corrupting existing longitudinal logic or overloading current contracts carelessly.

---

## Required outcome

Deliver a bounded HIGH-risk upgrade that:

1. defines and implements the correct contract support for longitudinal raw numeric comparison
2. preserves backward-safe longitudinal behaviour where possible
3. allows prior/current biomarker value comparisons to be accessed deterministically
4. leaves state-transition logic intact or safely adapted
5. provides a clean substrate for later narrative compilation
6. adds or updates tests proving the new longitudinal contract behaviour

---

## In scope

### 1. Preflight architectural verification
Before changing code, verify and cite:

- the exact current structure of `BiomarkerNode` or equivalent prior-snapshot biomarker representation
- whether raw numeric values are currently preserved, discarded, or inaccessible in the prior snapshot path
- the exact current role of `snapshot_linker.py`
- the exact current role of `state_transition_engine.py`
- how prior analysis results are currently loaded and normalized
- whether downstream consumers assume the existing snapshot node shape

You must confirm the real contract gap before patching it.

### 2. Contract upgrade
Implement the minimum clean contract change needed to support deterministic prior/current numeric comparison.

This may include, if repo reality confirms it is the correct design:
- adding raw numeric value support to the relevant biomarker snapshot contract
- preserving units where required
- preserving enough context to safely compare prior/current values

Do not widen the contract casually.
Add only what is needed for safe deterministic longitudinal comparison.

### 3. Snapshot-linking upgrade
Update the prior snapshot reconstruction/loading path so the new contract fields are actually populated from persisted analysis data where available.

### 4. Longitudinal comparison readiness
Ensure the upgraded longitudinal layer can support later narrative moves such as:
- improved from X to Y
- worsened from X to Y
- stable abnormal
- stable normal
- unresolved pathway despite other improvements

This sprint does not have to build the narrative prose compiler, but it must make those later moves possible.

### 5. State-transition compatibility
Verify that the state-transition engine and existing transition contracts remain correct under the upgraded data shape.

If minor adaptation is required, keep it bounded and explain it clearly.

### 6. Tests and regression coverage
Add or update tests covering at minimum:
- raw prior/current numeric preservation
- safe snapshot reconstruction
- compatibility with transition evaluation
- no breakage of existing longitudinal logic where prior behaviour should remain intact

### 7. Documentation note
Add a concise implementation note in the audit/summary or nearby sprint output describing:
- what contract changed
- why it changed
- what later sprint this unblocks

---

## Out of scope

The following are explicitly out of scope:

- narrative prose compilation
- patient summary generation
- body-overview compiler logic
- frontend changes
- lifestyle-to-interpretation joins
- new phenotype / IDL entities
- broad report compiler redesign
- any unrelated refactor of snapshot/persistence infrastructure

---

## Design rules

### Rule 1 — minimum viable contract change
Do not redesign half the pipeline.
Make the smallest clean change that unlocks numeric longitudinal comparison.

### Rule 2 — preserve existing deterministic behaviour
Do not break current transition/status logic to gain narrative convenience.

### Rule 3 — contracts before prose
This sprint is about enabling later narrative compilation, not starting it prematurely.

### Rule 4 — explicit units and comparison safety
If raw values are preserved, ensure comparison remains safe and interpretable.
Do not create ambiguous numeric comparisons.

### Rule 5 — no speculative widening
Do not add broad future-proofing fields unless there is a clear grounded need.

### Rule 6 — HIGH-risk discipline
Because this sprint is expected to touch:
- `backend/core/contracts/`
- `backend/core/analytics/`
it must be treated as HIGH-risk under the SOP.
Keep the touched-file scope tight and justified.

---

## Expected implementation shape

The expected shape is:

1. inspect current longitudinal contract and runtime flow
2. verify the exact raw-value gap
3. implement bounded contract upgrade
4. implement bounded snapshot-linker/runtime support
5. validate state-transition compatibility
6. add regression tests
7. document the contract change clearly

This must remain a precise enabling sprint, not a generalized refactor.

---

## STOP conditions

STOP immediately and report if any of the following are true:

1. raw prior values are not actually available in persisted analysis outputs and cannot be recovered from the current storage path
2. supporting numeric deltas would require a much wider persistence redesign than assumed
3. downstream consumers are too tightly coupled to the old contract shape for a safe bounded change
4. the correct solution appears to require introducing a separate longitudinal contract object rather than extending the current node shape, and that needs architectural adjudication first
5. the touched-file scope expands materially beyond the expected contract/snapshot/transition layer
6. repo reality contradicts the N-2 architecture assumptions

If blocked, report:
- the exact blocker
- the affected files
- the smallest safe remediation path
- whether N-3 should be split before implementation continues

---

## Required output files and code expectations

This is an implementation sprint.

Expected outputs may include changes to:
- contract files
- analytics/snapshot files
- transition files
- tests

You do not need to create a new strategy document unless a very short implementation note is necessary.

---

## Success criteria

This sprint is successful only if:

1. the longitudinal contract now supports deterministic raw prior/current numeric comparison
2. the snapshot-linking path populates the required fields where data exists
3. existing transition logic still works correctly or is safely adapted
4. tests prove the new behaviour
5. later narrative compiler work is materially unblocked
6. the sprint remains bounded and does not become a broad pipeline rewrite

---

## Deliverables

At finish, the sprint should leave behind:

- bounded code changes implementing the longitudinal contract upgrade
- regression tests
- audit-ready explanation of:
  - what changed
  - why it changed
  - what future sprint it unblocks

Report back with:
- files touched
- contract decision taken
- whether raw numeric deltas are now deterministically supportable
- any remaining limitation that later sprints must respect

---

## Evidence requirements

You must show, with exact file paths and grounded repo evidence:

- where the old contract shape was insufficient
- what new contract/data fields were introduced
- where snapshot reconstruction now populates them
- how tests prove the change
- how this specifically unblocks later narrative compilation

Do not claim success merely because tests pass.
Show that benchmark-style numeric longitudinal support is now actually enabled.