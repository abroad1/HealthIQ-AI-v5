---
work_id: D-2
branch: feature/domain-narrative-wave1
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# D-2 — Wave 1 domain narrative contract implementation

## Cursor agent

Use `healthiq-core-engine`.

This is mandatory.
Do not use `healthiq-frontend-shell`, `healthiq-qa-uat`, or `healthiq-docs-hygiene` for this sprint.

---

## Objective

Implement the deterministic narrative assembly layer for the three Wave 1 customer domains:

1. Cardiovascular health
2. Blood sugar control
3. Liver health

This sprint must populate the backend/domain contract with the narrative fields required for the new UX, using only existing governed engine outputs and approved content sources.

This sprint must also close the known Wave 1 cardiovascular content gap for the lipid-dominant consequence line.

Do not expose anything to the frontend yet.

---

## Branch requirement

Before doing anything else:

1. create and switch to this branch:
   `feature/domain-narrative-wave1`
2. confirm the branch name before implementation begins

If the branch already exists locally, check it out and confirm.

---

## Required background inputs

Read these before implementation:

1. `docs/HealthIQ_phased_customer_domain_score_sprint_plan_FINAL.md`
2. `docs/Strategy_A_Domain_Narrative_Contract_v1.md`
3. `docs/DOMAIN_NARRATIVE_CONTRACT_WAVE1.md`
4. `docs/Strategy_A_Launch_Domains_Implementation_Blueprint.md`
5. `docs/STRATEGY_A_IMPLEMENTATION_BLUEPRINT.md`
6. `AGENTS.md`
7. `.cursor/rules/healthiq-core-engine.mdc`
8. `docs/AUTOMATION_BUS_SOP_v1.3.1.md`  
   If v1.3.2 has been adopted in-repo before execution, use that instead.

Treat those as the governing context for this sprint.

---

## Precondition

D-1 must already exist on the current branch history or be cleanly available for this branch to build on.

Before implementation, restate:

- where D-1 output is being read from
- which existing domain contract fields were added in D-1
- which narrative fields remain unpopulated and are being populated now

If D-1 output is missing or inconsistent, STOP and report.

---

## In scope

### Domains
Wave 1 only:

- Cardiovascular health
- Blood sugar control
- Liver health

### Backend work
1. Populate deterministic narrative fields for the three Wave 1 domains.
2. Implement assembly rules for:
   - headline / score-band statement
   - contributor sentence
   - confidence sentence
   - consequence sentence
   - next-step sentence
3. Surface “what would improve confidence” inputs from existing deterministic evidence where required.
4. Close the known cardiovascular lipid-dominant consequence gap via governed content/source update and deterministic routing.
5. Keep all narrative backend-only in this sprint.

---

## Out of scope

- frontend rendering
- clinician PDF changes
- score recalibration
- thyroid scoring
- kidney expansion
- blood/iron/oxygen implementation
- second-wave domains
- LLM-generated prose
- broad SSOT redesign

Do not widen scope.

---

## Architectural constraints

### 1. Narrative is a translation layer
This sprint must assemble narrative from deterministic sources already in the repo.
Do not invent a new storytelling layer.

### 2. Consumer/clinical separation
Consumer-facing narrative fields must not leak into clinician-facing outputs.
Do not replace or alter clinical labels for clinician surfaces.

### 3. Deterministic sources only
Use only approved sources such as:
- D-1 domain score fields
- active signal ids
- IDL subtitle
- IDL `why_it_matters`
- `insights`
- `narrative_report_v1` only where domain use is explicitly justified
- root-cause missing-data structures
- governed next-step sources

### 4. No free-text invention
Do not write new medical interpretation prose unless it is the explicitly scoped governed content fix for the known cardiovascular gap.

### 5. Keep scoring and narrative separate
Do not re-open score logic except where absolutely necessary to connect existing D-1 evidence fields to narrative assembly.

---

## Required narrative outputs

For each of the three domains, populate deterministic fields for:

- `headline_sentence`
- `contributor_sentence`
- `confidence_sentence`
- `consequence_sentence`
- `next_step_sentence`

Also support:
- `missing_marker_ids` / equivalent existing D-1 evidence fields for “what would improve confidence”

If field names differ, keep naming clean and internally consistent, but do not bloat the contract.

---

## Domain rules

## Domain 1 — Cardiovascular health

### Headline
Use D-1 score/band output only.

### Contributor sentence
Assemble deterministically from the approved source hierarchy in the narrative contract research.
Do not silently mix separate systems into one sentence without explicit wording.

### Confidence sentence
Use the D-1 confidence tier and deterministic coverage logic.
Do not invent a second independent confidence model.

### Consequence sentence
This sprint explicitly owns the known lipid-dominant cardiovascular content gap.

You must implement a governed and deterministic consequence path for lipid-dominant cardiovascular cases.
Preferred route:
- approved governed content/source update in the most appropriate existing source
- deterministic selection logic from that source

Do not leave this gap unresolved.

### Next-step sentence
Use existing deterministic governed sources only.

---

## Domain 2 — Blood sugar control

### Headline
Use D-1 score/band output only.

### Contributor sentence
Follow the approved signal/IDL selection logic from the narrative contract research.

### Confidence sentence
Use D-1 confidence tier and evidence coverage.
If insulin/triglyceride-related completeness matters, reflect that through deterministic existing evidence only.

### Consequence sentence
Use existing governed consequence sources already available in the repo where identified by the research.

### Next-step sentence
Use deterministic governed next-step sources only.

---

## Domain 3 — Liver health

### Headline
Use D-1 score/band output only.
Keep wording honest about enzyme-led assessment where required.

### Contributor sentence
Use approved deterministic hepatic pattern-selection logic only.

### Confidence sentence
Use the D-1 domain-level liver confidence logic.
Do not fall back to the inadequate narrow cluster-only confidence logic if D-1 introduced a better domain confidence basis.

### Consequence sentence
Use existing governed source where already available.

### Next-step sentence
Use deterministic governed next-step sources only.

---

## Known Wave 1 content gap to resolve in this sprint

There is a known cardiovascular gap for the lipid-dominant consequence path.

This sprint must assign and implement that fix explicitly.

Requirements:
- governed source only
- smallest safe content change
- deterministic routing
- no broad KB rewrite
- report exactly where the new source text now lives

This is the only intentional content-scope element in the sprint.

---

## Files likely in scope

These are likely, not mandatory:

- `backend/core/analytics/domain_score_assembler.py`
- `backend/core/models/results.py`
- `backend/core/dto/builders.py`
- `backend/core/pipeline/orchestrator.py`
- relevant IDL or governed content source file(s) for the cardiovascular consequence gap
- targeted tests

Potentially:
- `knowledge_bus/interpretation_display_layer_v1/idl_records_v1.yaml`
or another clearly justified governed source, if that is the approved minimal fix path

---

## Files likely out of scope

Do not touch unless absolutely required and justified in your report:

- `frontend/**`
- clinician PDF/export surfaces
- broad scoring policy files
- unrelated analytics modules
- thyroid/kidney/blood-iron domain logic
- second-wave domain assets

---

## Testing discipline

Do not run the full repository test suite.

Run only:

1. new or updated targeted backend/content tests for Wave 1 narrative assembly
2. directly relevant existing tests for touched contract/orchestrator/domain assembler paths
3. minimal validation needed to prove:
   - all 3 Wave 1 domains emit the narrative fields
   - the cardiovascular lipid-dominant consequence path is now filled
   - no frontend dependency was introduced
   - no clinician-layer outputs were unintentionally altered

Before running tests, state:
- what you will run
- why it is relevant
- what you are deliberately not running

---

## Acceptance criteria

This sprint is successful only if:

1. Wave 1 domain objects now emit:
   - headline sentence
   - contributor sentence
   - confidence sentence
   - consequence sentence
   - next-step sentence

2. All narrative is assembled from deterministic approved sources.

3. The cardiovascular lipid-dominant consequence gap is closed and clearly reported.

4. Blood sugar and liver domain narrative follow the repo-grounded contract work and do not introduce unsupported claims.

5. No frontend exposure is introduced.

6. No clinician-facing language is replaced by consumer-layer language.

7. Targeted tests pass.

---

## Reporting requirements

When finished, report back in these sections:

### 1. Branch
- confirm branch name

### 2. Preflight restatement
- objective
- files touched
- files not touched
- where D-1 fields were read from
- what new narrative fields were populated

### 3. Requested changes made
- exact files changed
- where sentence assembly lives
- how each of the three domains now sources:
  - headline
  - contributor
  - confidence
  - consequence
  - next step

### 4. Cardiovascular gap closure
- exact file/source changed
- exact path now used
- why this was the minimal safe governed fix

### 5. Tests run
- exact tests
- results

### 6. Known limits intentionally deferred
- anything left for later phases
- any domain-level caveats not solved here

### 7. Uncommitted / not merged
- confirm work is not merged to `main`

---

## STOP conditions

STOP and report instead of widening scope if any of the following occurs:

1. D-1 output is missing or inconsistent.
2. A domain narrative field cannot be assembled without inventing unsupported prose.
3. The cardiovascular consequence gap cannot be fixed without a broad KB/content redesign.
4. Frontend changes become necessary to validate the backend work.
5. Clinician-layer outputs would need modification to complete this sprint.
6. Any second-wave domain starts to creep into implementation.

If blocked, report:
- exact blocker
- affected files
- smallest safe remediation path