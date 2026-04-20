---
work_id: N-2
branch: feature/n-2-narrative-compiler-architecture-design
risk_level: STANDARD
execution_model: TWO_PHASE_START_FINISH
change_type: CONTENT
---

# N-2 — Narrative compiler architecture design

## Objective

Design the deterministic narrative compiler architecture for HealthIQ AI before any implementation sprint begins.

This is an architecture-design sprint.
It is not a coding sprint.
Do not modify backend or frontend application code.
Do not write implementation patches.
Do not create provisional runtime logic.

This sprint exists to answer the key architectural questions that must be settled before new deterministic narrative assets and compiler work can be implemented safely.

---

## Strategic context already settled

The following are already decided and are not open for reinterpretation in this sprint:

- The benchmark narrative is locked as the target-state narrative reference.
- The merged reverse-engineering matrix is now the planning authority for supportability and gap analysis.
- The main problem is not raw data alone and not frontend polish alone.
- The main missing layer is the deterministic narrative support stack:
  - data/contract layer
  - governed narrative asset layer
  - compiler/assembly layer
  - output/display layer
- The final sprint strategy is the approved roadmap for this workstream.
- N-2 is the architecture sprint that must define the compiler model before N-3 and later implementation sprints proceed.

Your job is to produce the architectural design authority for the deterministic narrative compiler stack.

---

## Required inputs

Treat the following as required inputs:

1. Benchmark narrative target lock
`docs/golden-narrative/AB_GOLD_STANDARD_NARRATIVE_TARGET_LOCK.md`

2. Merged reverse-engineering matrix
`docs/golden-narrative/AB_GOLD_STANDARD_NARRATIVE_REVERSE_ENGINEERING_MERGED.md`

3. Final sprint strategy
`docs/golden-narrative/HealthIQ_Deterministic_Narrative_Sprint_Strategy_FINAL.md`

4. Current relevant runtime authorities in the repo, including at minimum:
- `backend/core/analytics/report_compiler_v1.py`
- `backend/core/contracts/report_v1.py`
- `backend/core/contracts/clinician_report_v1.py`
- `backend/core/contracts/insight_graph_v1.py`
- `backend/core/analytics/root_cause_compiler_v1.py`
- `backend/core/analytics/interpretation_display_layer_publish_v1.py`
- `backend/core/analytics/balanced_systems_presentation_v1.py`
- `backend/core/analytics/snapshot_linker.py`
- `backend/core/analytics/state_transition_engine.py`
- any other files you determine are architecturally relevant

---

## Core architectural questions this sprint must answer

This sprint must answer, explicitly and in writing:

1. Should the deterministic narrative compiler extend `report_compiler_v1.py`, or should it be a separate module/layer?

2. What is the output contract called?
For example:
- new `NarrativeReportV1`
- extension of `ReportV1`
- extension of `ClinicianReportV1`
- another governed contract shape

3. What is the relationship between the new narrative compiler output and existing contracts:
- `ReportV1`
- `ClinicianReportV1`
- IDL bundle
- Layer C features
- any future retail summary layer

4. What are the compiler stages?
For example:
- source data / contract inputs
- governed narrative assets
- interpretation joins
- narrative assembly
- output contracts

5. Which narrative sections should be emitted as separate compiled assets versus assembled at display time?

6. Which future sprint owns each layer of this architecture?

---

## Required outcome

Deliver a formal architecture design package that:

1. defines the deterministic narrative compiler stack clearly
2. defines the compiler boundary and module placement
3. defines the output contract strategy
4. defines the input asset classes the compiler will consume
5. defines the relationship to current report/compiler/runtime artifacts
6. identifies any architectural prerequisite decisions for N-3 and later sprints
7. leaves behind an implementation-ready design authority for later HIGH-risk build sprints

---

## In scope

### 1. Compiler boundary decision
Determine whether the deterministic narrative compiler should:
- extend `report_compiler_v1.py`
- sit alongside it as a separate compiler
- or introduce another layered architecture

You must justify the decision with repo-grounded reasoning.

### 2. Output contract design
Define the recommended output contract strategy.

At minimum, answer:
- what new contract(s), if any, should exist
- what each contract is for
- which contract is authoritative for:
  - retail patient summary
  - body overview
  - pathway-level narrative blocks
  - longitudinal section
  - next-steps narrative
  - clinician synthesis

### 3. Compiler stage model
Define the stages of the deterministic narrative support stack.

At minimum, describe:
- data / contract layer
- governed narrative asset layer
- compiler / assembly layer
- output / display layer

Make the dependency order explicit.

### 4. Asset-consumption model
For each major narrative section type, state what kinds of inputs the compiler should consume.

Examples:
- biomarker and reference-range data
- cluster/system burden outputs
- root-cause hypotheses
- confirmatory tests
- questionnaire/lifestyle context
- longitudinal transition outputs
- pathway explainer assets
- functional-reading assets
- monitoring-criteria assets
- IDL records

### 5. Architectural constraints and prerequisites
Identify any hard prerequisites for later sprints.

Examples:
- raw-value persistence needed before longitudinal narrative build
- governed interpretation entities needed before certain compiler sections
- lifestyle-to-pathway joins needed before contextual narrative can be emitted

### 6. Sprint dependency mapping
Map the architecture to the sprint strategy so later work packages are sequenced correctly.

---

## Out of scope

The following are explicitly out of scope:

- implementation changes to runtime code
- changing backend contracts in code
- adding new narrative assets in code or YAML
- frontend redesign
- Gemini / LLM work
- rewriting the benchmark narrative
- redoing the merged matrix
- broad strategic debate already settled in prior documents

---

## Required output files

Create the following files in:
`docs/golden-narrative/`

### 1. Narrative compiler architecture design
Suggested filename:
`HealthIQ_Deterministic_Narrative_Compiler_Architecture_v1.md`

### 2. Optional companion decision log
If helpful, create:
`HealthIQ_Deterministic_Narrative_Compiler_Architecture_DECISIONS.md`

Only create the second file if it adds real value and does not duplicate the first.

---

## Output structure requirements

### File 1 — Narrative compiler architecture design
Must include, at minimum:

#### 1. Purpose
What this architecture is for and why it is needed.

#### 2. Source authorities used
List the target lock, merged matrix, final strategy, and runtime files inspected.

#### 3. Deterministic narrative support stack
Define the stack layers explicitly.

#### 4. Compiler boundary decision
State whether the compiler extends existing architecture or becomes a new module, and why.

#### 5. Output contract strategy
Name the recommended output contract(s), their roles, and relationship to existing contracts.

#### 6. Section-to-compiler model
For each major narrative section type, state:
- intended compiled output type
- likely inputs
- likely owning asset classes

#### 7. Architectural prerequisites
List the hard prerequisites that later sprints must satisfy.

#### 8. Sprint dependency implications
Map architecture decisions to the sprint sequence.

#### 9. Risks and failure modes
State the main architectural risks if the wrong design is chosen.

#### 10. Recommended next implementation sprint
State what N-3 must do in light of this architecture.

### Optional File 2 — Decision log
If created, it should contain:
- major decisions
- alternatives considered
- reasons rejected
- open questions requiring future adjudication

---

## Design rules

### Rule 1 — architecture before convenience
Do not choose an architecture merely because it is easiest to patch into current code.

### Rule 2 — preserve authority separation
Do not collapse:
- source data
- governed narrative assets
- compiler logic
- output contracts
into one muddy layer.

### Rule 3 — avoid brittle coupling
If extending an existing compiler would make the narrative layer brittle or overloaded, say so clearly.

### Rule 4 — repo-grounded design
Use actual current runtime structures, not hypothetical generic architecture.

### Rule 5 — design for deterministic scale
The architecture must support future narrative assets beyond the AB benchmark case.

### Rule 6 — respect SOP implications
Call out where future implementation work will become HIGH-risk under the SOP due to touched paths such as:
- `backend/core/contracts/`
- `backend/core/analytics/`
- pipeline/control-plane areas

---

## Expected implementation shape

This sprint should amount to:

1. inspect current runtime compiler and contract architecture
2. inspect the planning authority documents
3. answer the architecture questions explicitly
4. write the architecture design document
5. save it in `docs/golden-narrative/`

No code changes should result.

---

## STOP conditions

STOP immediately and report if any of the following are true:

1. the current runtime architecture is too ambiguous to determine compiler boundaries without new code investigation
2. the merged matrix and final strategy materially conflict on what the compiler must produce
3. no clean output-contract strategy can be recommended without first resolving another upstream design issue
4. repo reality shows the current report/compiler contracts are materially different from what the planning docs assume

If blocked, report the exact blocker and the smallest safe remediation path.

---

## Success criteria

This sprint is successful only if:

1. the deterministic narrative support stack is explicitly defined
2. the compiler boundary decision is made and justified
3. the output contract strategy is clear
4. later sprint authors can see what assets and contracts the compiler will depend on
5. N-3 and later sprints have a clean architectural starting point
6. no implementation code was changed

---

## Deliverables

At finish, the sprint should leave behind:

- `docs/golden-narrative/HealthIQ_Deterministic_Narrative_Compiler_Architecture_v1.md`
- optionally, `docs/golden-narrative/HealthIQ_Deterministic_Narrative_Compiler_Architecture_DECISIONS.md`

plus a short completion note stating:
- output filename(s)
- the compiler boundary decision
- the recommended output contract strategy
- the top 3 architectural risks

---

## Evidence requirements

You must show, with exact file paths and grounded references:

- the current compiler/runtime files inspected
- the contract files inspected
- the reasons for the chosen compiler boundary
- the reasons for the chosen output contract strategy
- the architectural prerequisites for later sprints

Do not produce a generic architecture memo.
Produce implementation-ready design authority.