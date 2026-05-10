---
work_id: WP2-LAYER-B-LAYER-C-TECHNICAL-CLOSURE
branch: wp2/layer-b-layer-c-technical-closure
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# WP2 — Pre-Sprint 3 Technical Closure: Layer B → Layer C Contract Readiness

## Objective

Close the remaining Pre-Sprint 3 technical blockers so Sprint 3 can be safely authored.

This work package must formalise the Layer B → Layer C handoff using the existing typed `ReportV1` contract as the short-term authoritative source, introduce a minimal governed narrative payload contract, harden the LLM validator boundary, correct the proving harness clinician surface extraction, and fix the IDL `clinical_only` consumer gate.

This is not Sprint 3.

Do not build final user prose.  
Do not redesign the frontend.  
Do not broaden the questionnaire.  
Do not retire `insights[]`.  
Do not implement mock-mode honesty wording.

## Authority documents

Read before implementation:

- `docs/planning-papers/healthiq_pre_sprint1_decision_pack_FINAL.md`
  - especially §3.9 Layer B → Layer C boundary
- `docs/planning-papers/healthiq_pre_sprint2_statin_gate_pack_FINAL.md`
- `docs/planning-papers/healthiq_pre_sprint3_closure_pack_FINAL.md`
- `docs/audit-papers/gate_compliance_audit_sprint3_readiness.md`
- `docs/audit-papers/wp2_layer_b_layer_c_implementation_readiness_audit.md`
- `docs/planning-papers/healthiq_launch_core_transformation_plan_FINAL.md`
- `docs/AUTOMATION_BUS_SOP_v1.3.1.md`

Pre-Sprint 1 §3.9 is the governing authority:

> Layer B decides. Layer C synthesises.

Layer C must not invent, alter, reorder, reinterpret, or strengthen analytical truth.

## Architecture decision for this work package

Use Path B now.

`ReportV1` is the approved typed Layer B source for:

- `top_findings`
- `root_cause_v1`
- clinician-report source material
- ranked finding / hypothesis source material required for narrative payload construction

Do not promote `top_findings` or `root_cause_v1` directly onto `AnalysisDTO` in this work package.

Path A — first-class `AnalysisDTO.top_findings` and `AnalysisDTO.root_cause_v1` — is deferred as later structural cleanup unless implementation evidence proves Path B cannot safely satisfy this work package.

## Required architecture output

Create an ADR recording this decision:

`docs/architecture/ADR_WP2_layer_b_layer_c_contract_path_b.md`

The ADR must state:

- `ReportV1` is the short-term typed Layer B source
- `NarrativePayloadV1` is the formal Layer B → Layer C handoff object for Sprint 3 readiness
- `NarrativeReportV1` remains the Layer C prose output
- `AnalysisDTO` restructuring is deferred
- Layer C must not access arbitrary `meta` fields for medical meaning
- Path A remains a later architectural cleanup option, not a prerequisite for Sprint 3

## Scope

Implement the following bounded tasks only.

---

# Task 1 — Add `NarrativePayloadV1`

Create a new contract:

`backend/core/contracts/narrative_payload_v1.py`

This must be a typed Pydantic contract representing the governed Layer B → Layer C input payload.

It should use existing typed contracts wherever possible.

Minimum required structure:

- `analysis_id`
- `report_v1`
- `top_findings`
- `root_cause_v1`
- `intervention_annotations_v1`
- `section_intents`
- `claim_boundaries`

Use the existing types:

- `ReportV1`
- `ReportTopFindingV1`
- `RootCauseV1`
- `InterventionAnnotationsV1`

Do not duplicate those model definitions.

## Required section intent scaffold

The payload must include a typed section-intent structure for the five existing narrative sections:

- `retail_summary`
- `lead_narrative`
- `body_overview`
- `next_steps_narrative`
- `clinician_synthesis`

Each section intent should minimally express:

- section id
- intent code
- permitted source fields
- fallback rule

Allowed intent codes should cover:

- `reassure`
- `prioritise`
- `explain_mechanism`
- `express_uncertainty`
- `frame_next_steps`
- `support_clinician_fast_read`

## Required claim-boundary scaffold

The payload must include a typed claim-boundary structure that minimally expresses:

- allowed claim strength
- allowed consumer wording
- prohibited claims
- clinician-only boundary flag or equivalent

The prohibited claims must include at least wording patterns equivalent to:

- diagnosis / diagnoses / diagnostic
- confirms / confirmed
- rules out
- guarantees
- treatment recommendation
- medication recommendation
- supplement recommendation

Use sensible typed enums or constrained literals where appropriate.

Do not over-engineer.

---

# Task 2 — Build payload from existing `ReportV1`

Add a small, deterministic builder/helper that constructs `NarrativePayloadV1` from existing pipeline state.

Preferred location:

`backend/core/analytics/narrative_report_compiler_v1.py`

or a new narrowly scoped helper module if cleaner, for example:

`backend/core/analytics/narrative_payload_builder_v1.py`

The builder must:

- accept `analysis_id`
- accept the existing `ReportV1`
- accept `intervention_annotations_v1` where available
- derive `top_findings` from `report_v1.top_findings`
- derive `root_cause_v1` from `report_v1.root_cause_v1`
- populate the five required section intents
- populate the default claim boundaries

Do not derive new medical reasoning.

Do not change ranking.

Do not change confidence.

Do not change signal state.

Do not modify `ReportV1`.

---

# Task 3 — Update narrative compiler input path

Update `compile_narrative_report_v1()` so the governed typed narrative payload is available to the compiler.

Preferred approach:

- add an optional `narrative_payload_v1: Optional[NarrativePayloadV1] = None` parameter
- preserve backwards compatibility for current deterministic paths
- avoid breaking existing call sites unnecessarily
- where both payload and raw `insight_graph` are available, prefer the typed payload for Layer B truth

Do not remove deterministic mock output.

Do not activate Gemini.

Do not rewrite the narrative report prose.

The change is to formalise the input contract, not to make the report more polished.

---

# Task 4 — Wire `NarrativePayloadV1` in orchestrator path

In the production analysis path, construct the `NarrativePayloadV1` from the existing `ReportV1` before calling `compile_narrative_report_v1()`.

Likely files:

- `backend/core/pipeline/orchestrator.py`
- `backend/core/analytics/narrative_report_compiler_v1.py`
- possible helper module from Task 2

Use the existing `InsightGraphV1.report_v1` / `ReportV1` source.

Do not add `top_findings` or `root_cause_v1` to `AnalysisDTO`.

Do not change frontend response shape unless unavoidable.

---

# Task 5 — Harden `validate_llm_output_v2`

Update:

`backend/core/llm/validator_v2.py`

The validator must be reviewed and hardened against the §3.9 boundary.

Add or confirm tests for:

1. numeric invention guard — existing protection must remain
2. lead finding preservation
3. invented hypothesis rejection
4. prohibited claim language rejection

The implementation should use the prompt / payload fields available to the validator.

Minimum required behaviour:

- reject LLM output that centres a different lead finding than the provided Layer B lead finding
- reject output that references a hypothesis ID not present in `root_cause_v1`
- reject output containing prohibited claim-strength terms such as “diagnoses”, “confirms”, “rules out”, “guarantees”, “treatment recommendation”, “medication recommendation”, or equivalent unsafe phrasing
- preserve existing numeric invention checks

If any check cannot be implemented because the validator input lacks the necessary source fields, STOP and report the exact missing field and required upstream payload change.

---

# Task 6 — Fix proving harness clinician extraction

Fix the proving harness so it correctly captures clinician report heads.

Current issue:

The proving harness reads `clinician_report_v1` from `AnalysisDTO.model_dump()`, but `clinician_report_v1` is added later by `build_analysis_result_dto()` and is not present directly on `AnalysisDTO`.

Update:

`backend/tools/launch_core_proving_harness.py`

Required outcome:

- `primary_concern_head` is extracted from the correctly compiled clinician report
- `key_findings_head` is extracted correctly
- `top_hypothesis_line_head` is extracted correctly where available

Use the same safe pattern demonstrated in:

`backend/tests/unit/test_clinician_report_runtime_alignment.py`

Do not change the clinician report compiler unless investigation proves the compiler itself is broken.

After the fix, re-run the proving harness and update the proving output artefacts if this is the established project pattern.

Expected artefacts may include:

- `docs/audit-papers/launch-core-proving/latest_fingerprints.json`
- `docs/audit-papers/launch-core-proving/PROVING_REPORT.md`

Only update these if produced by the harness as normal output.

---

# Task 7 — Fix IDL `clinical_only` consumer gate

Update:

`frontend/app/components/results/InterpretationPatternsSection.tsx`

Current selector filters only:

```ts
r.enabled_for_frontend === true
````

Required selector logic:

```ts
r.enabled_for_frontend === true &&
r.frontend_allowed_term !== "clinical_only"
```

Do not change backend IDL publication logic.

Do not change IDL YAML.

Do not rename terms.

Do not change ordering.

Add/update frontend tests proving:

* `phenotype_allowed` records with `enabled_for_frontend: true` render
* `clinical_only` records with `enabled_for_frontend: true` do not render
* `enabled_for_frontend: false` records do not render
* display ordering remains preserved for visible records

Likely test file:

`frontend/tests/components/InterpretationPatternsSection.test.tsx`

---

# Task 8 — Tests

Add/update focused tests only.

Backend tests should cover:

* `NarrativePayloadV1` schema construction
* payload builder produces section intents for all five narrative sections
* payload builder carries `top_findings` from `ReportV1`
* payload builder carries `root_cause_v1` from `ReportV1`
* validator rejects invented lead finding
* validator rejects invented hypothesis
* validator rejects prohibited claim language
* proving harness produces non-empty `primary_concern_head`

Frontend tests should cover:

* IDL `clinical_only` exclusion
* preserved rendering of allowed IDL records
* preserved display ordering

Run the narrowest relevant tests first, then the project’s broader available backend/frontend test commands.

---

# Required validation commands

Inspect project scripts and run the appropriate existing commands.

At minimum, attempt targeted tests for:

Backend:

* narrative payload contract/builder tests
* validator v2 tests
* proving harness tests
* clinician report runtime alignment tests

Frontend:

* `InterpretationPatternsSection` component tests

Then run the broader relevant test suites if available and feasible.

Do not invent new test commands if existing scripts exist.

Report every command run and its result.

---

# Stop conditions

STOP and report before implementation if:

* `ReportV1` is no longer present or no longer contains `top_findings` / `root_cause_v1`
* `root_cause_v1` has no typed contract
* `compile_narrative_report_v1()` cannot accept an optional typed payload without breaking existing call sites
* validator hardening requires broad LLM prompt restructuring beyond this work package
* the proving harness issue proves to be a production compiler defect rather than a harness extraction defect
* IDL frontend types do not expose `frontend_allowed_term`
* implementation requires modifying Knowledge Bus content
* implementation requires broad frontend redesign
* implementation requires adding `top_findings` or `root_cause_v1` directly to `AnalysisDTO`
* files outside the expected scope become necessary

If a stop condition is hit, do not work around it. Report the blocker and proposed revised scope.

---

# Expected files touched

Expected docs:

* `docs/architecture/ADR_WP2_layer_b_layer_c_contract_path_b.md`

Expected backend:

* `backend/core/contracts/narrative_payload_v1.py`
* `backend/core/analytics/narrative_report_compiler_v1.py`
* possible `backend/core/analytics/narrative_payload_builder_v1.py`
* `backend/core/pipeline/orchestrator.py`
* `backend/core/llm/validator_v2.py`
* `backend/tools/launch_core_proving_harness.py`
* relevant backend tests

Expected frontend:

* `frontend/app/components/results/InterpretationPatternsSection.tsx`
* `frontend/tests/components/InterpretationPatternsSection.test.tsx`

Expected generated proving artefacts only if harness run produces them:

* `docs/audit-papers/launch-core-proving/latest_fingerprints.json`
* `docs/audit-papers/launch-core-proving/PROVING_REPORT.md`

Not expected:

* `backend/core/models/results.py`
* `backend/ssot/`
* `knowledge_bus/`
* `backend/scripts/run_work_package.py`
* `backend/scripts/golden_gate_local.py`
* `backend/scripts/update_cursor_status.py`
* broad frontend page redesign
* Sprint 3 prompt files

---

# Explicit non-goals

Do not:

* author Sprint 3
* activate Gemini
* write final polished prose
* broaden the questionnaire
* reduce the questionnaire
* retire `insights[]`
* implement mock-mode honesty wording
* add new WHY assets
* change biomarker interpretation logic
* change signal ranking
* change confidence or banding
* change statin annotation logic
* change Knowledge Bus content
* add fallback parsers
* create duplicate SSOT authority sources

---

# Closure evidence required

Before finish, report:

* branch name
* work_id
* files changed
* summary of each implemented task
* whether Path B was implemented without `AnalysisDTO` restructuring
* whether `NarrativePayloadV1` exists and what it contains
* whether `compile_narrative_report_v1()` now accepts the typed payload
* validator checks added
* clinician proving harness result for `primary_concern_head`
* IDL `clinical_only` gate test result
* all commands run and pass/fail result
* confirmation no Knowledge Bus files were modified
* confirmation no SSOT files were modified
* confirmation no control-plane scripts were modified
* confirmation no Sprint 3 prompt was authored

## Final expected outcome

Sprint 3 remains blocked until this work package is complete and audited.

After successful completion, the programme should be able to author Sprint 3 against a typed `ReportV1` → `NarrativePayloadV1` → `NarrativeReportV1` contract.

````
