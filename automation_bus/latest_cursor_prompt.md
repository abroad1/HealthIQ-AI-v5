---
work_id: LC-S3-LAYER-C-PAYLOAD-IMPLEMENTATION
branch: sprint3/layer-c-payload-implementation
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: BEHAVIOUR
---

# LC-S3 — Layer B → Layer C Payload Implementation

## Objective

Implement Sprint 3: make the narrative layer use the governed `NarrativePayloadV1` contract as the authoritative Layer B → Layer C input.

This sprint must make the report feel more composed, coherent, and governed without allowing Layer C to invent medical reasoning.

Layer B decides. Layer C synthesises.

## Authority documents

Read before implementation:

- `docs/planning-papers/healthiq_launch_core_transformation_plan_FINAL.md`
- `docs/planning-papers/healthiq_pre_sprint1_decision_pack_FINAL.md`
  - especially §3.9 Layer B → Layer C boundary
- `docs/planning-papers/healthiq_pre_sprint3_closure_pack_FINAL.md`
- `docs/audit-papers/gate_compliance_audit_sprint3_readiness_second_pass.md`
- `docs/architecture/ADR_WP2_layer_b_layer_c_contract_path_b.md`
- `docs/audit-papers/wp2_layer_b_layer_c_implementation_readiness_audit.md`
- `docs/AUTOMATION_BUS_SOP_v1.3.1.md`

## Current approved architecture

Sprint 3 must build on the approved Path B contract:

`ReportV1 → NarrativePayloadV1 → NarrativeReportV1`

- `ReportV1` is the typed Layer B source.
- `NarrativePayloadV1` is the formal Layer B → Layer C handoff.
- `NarrativeReportV1` remains the Layer C prose output.
- `AnalysisDTO` restructuring is not Sprint 3 scope.
- Layer C must not access arbitrary `meta` fields for medical meaning.

## Scope

Implement governed narrative generation for the existing five `NarrativeReportV1` fields:

- `retail_summary`
- `lead_narrative`
- `body_overview`
- `next_steps_narrative`
- `clinician_synthesis`

The implementation must use `NarrativePayloadV1` as the primary source of truth where available.

## Required behaviour

Layer C may:

- translate structured Layer B truth into natural prose
- combine deterministic facts into coherent sentences
- improve readability, flow, tone, and audience fit
- use fired deterministic modifiers for emphasis
- use section intents to shape each narrative section
- use claim boundaries to avoid unsafe wording

Layer C must not:

- invent new medical reasoning
- change lead finding or ranking
- alter confidence or banding
- add causal claims beyond Layer B evidence
- introduce new evidence
- reinterpret absent data
- invent confounders or next steps
- produce claims outside the allowed wording boundaries
- recommend medicines, supplements, or treatment
- diagnose or rule out disease

## Task 1 — Make `NarrativePayloadV1` the primary narrative input

Update the narrative compiler path so `compile_narrative_report_v1()` uses `narrative_payload_v1` as the primary governed input.

Expected file:

- `backend/core/analytics/narrative_report_compiler_v1.py`

Required:

- preserve backwards compatibility where `narrative_payload_v1` is absent
- prefer `narrative_payload_v1.report_v1`, `.top_findings`, `.root_cause_v1`, `.section_intents`, and `.claim_boundaries` where present
- avoid uncontrolled traversal of `meta` / raw `insight_graph` for medical meaning
- keep deterministic fallback safe

Do not remove existing deterministic-mock support.

## Task 2 — Implement section-specific governed prose assembly

For each of the five narrative fields, use the section intent and permitted source fields from `NarrativePayloadV1`.

Minimum expectations:

### `retail_summary`

Purpose:

- concise user-facing overview
- identify the main pattern
- avoid over-claiming
- acknowledge uncertainty where relevant

Must use:

- lead finding from `top_findings[0]`
- domain / pattern context where available
- claim boundaries

Must not:

- introduce diagnosis
- imply all-clear if Layer B is uncertain
- invent future risk

### `lead_narrative`

Purpose:

- explain the lead finding and biological mechanism
- use governed WHY / root-cause evidence
- explain why it matters

Must use:

- lead finding
- `root_cause_v1`
- evidence-for
- evidence-against / limiting factors
- missing data / confirmatory tests where available

Must not:

- invent a cause
- ignore evidence-against
- convert “suggests” into “confirms”

### `body_overview`

Purpose:

- summarise relevant system-level patterns
- explain how the lead finding fits into the wider panel

Must use:

- available `ReportV1` / IDL / domain-level context where already available to the compiler
- only deterministic system/pattern data

Must not:

- invent cross-system connections
- overstate weak or missing patterns

### `next_steps_narrative`

Purpose:

- frame safe next steps

Allowed next-step styles:

- discuss with clinician
- monitor
- retest
- review lifestyle context
- consider confirmatory testing where Layer B lists it

Prohibited:

- medication advice
- supplement advice
- treatment recommendations
- urgent escalation unless already present in governed Layer B safety data

### `clinician_synthesis`

Purpose:

- clinician-facing fast-read

Must include where available:

- lead concern
- top hypothesis
- key supporting evidence
- evidence-against / uncertainty
- missing confirmatory markers
- medication/context caveats

Must not:

- create new clinical interpretation outside Layer B
- include consumer-only simplification if clinician detail is available

## Task 3 — Enforce claim boundaries in deterministic prose

Use `NarrativePayloadV1.claim_boundaries` to prevent unsafe deterministic prose.

Required:

- avoid prohibited claim patterns in generated deterministic output
- use allowed claim strength wording such as “suggests”, “may reflect”, “is consistent with” where appropriate
- keep clinician-only content out of consumer sections unless explicitly allowed

If the existing `claim_boundaries` model is insufficient for this task, STOP and report the missing field. Do not invent a parallel boundary system.

## Task 4 — Preserve validator compatibility

Ensure the output remains compatible with `validate_llm_output_v2` and the validator prompt envelope.

Expected files may include:

- `backend/core/analytics/narrative_report_compiler_v1.py`
- `backend/core/insights/synthesis.py`
- `backend/core/llm/validator_v2.py`

Do not widen `synthesis.py` unless strictly required. If a change to `synthesis.py` is required, explicitly explain why and keep it additive.

Do not activate Gemini.

## Task 5 — Tests

Add/update focused tests.

Required backend tests:

- narrative compiler uses `NarrativePayloadV1` when provided
- all five `NarrativeReportV1` fields are populated from governed payload input
- lead finding in narrative output matches Layer B lead finding
- deterministic prose does not include prohibited claim language
- root-cause evidence / hypothesis information is reflected without invention
- missing-data / uncertainty is handled safely
- next steps do not include treatment, medication, or supplement advice
- clinician synthesis includes clinician-facing lead concern when available
- backwards compatibility remains when `narrative_payload_v1` is absent

Likely test files:

- existing narrative compiler tests, if present
- otherwise create a focused unit test under `backend/tests/unit/`

Run relevant existing tests, including:

- narrative payload WP-2 tests
- validator v2 tests
- clinician report runtime alignment tests
- launch-core proving harness tests

## Task 6 — Documentation note

Create a short Sprint 3 completion note under:

`docs/sprints/LC-S3_layer_c_payload_implementation_completion_2026-05.md`

It must record:

- what changed
- how `NarrativePayloadV1` is now used
- how claim boundaries are respected
- tests run
- known limitations
- confirmation that questionnaire sharpening, `insights[]` retirement, and mock-mode honesty were not part of this sprint

## Stop conditions

STOP and report before implementation if:

- `NarrativePayloadV1` does not exist
- ADR Path B is missing
- `NarrativePayloadV1` does not include section intents or claim boundaries
- `ReportV1` does not expose `top_findings` or `root_cause_v1`
- using `NarrativePayloadV1` requires adding `top_findings` / `root_cause_v1` to `AnalysisDTO`
- the implementation would require questionnaire changes
- the implementation would require Knowledge Bus content changes
- the implementation would require SSOT changes
- the implementation would require frontend redesign
- Gemini activation becomes necessary
- claim boundaries cannot be enforced with the current contract
- narrative output would require invented medical reasoning

## Expected files touched

Expected backend:

- `backend/core/analytics/narrative_report_compiler_v1.py`
- relevant backend narrative compiler tests
- possibly `backend/core/insights/synthesis.py` only if strictly required for validator compatibility
- possibly `backend/core/llm/validator_v2.py` only if strictly required for compatibility

Expected docs:

- `docs/sprints/LC-S3_layer_c_payload_implementation_completion_2026-05.md`

Not expected:

- `backend/core/models/results.py`
- `backend/ssot/`
- `knowledge_bus/`
- frontend report pages
- questionnaire files
- `insights[]` retirement files
- mock-mode honesty UI files
- Automation Bus control-plane scripts
- Sprint 4 or Sprint 5 planning files

## Explicit non-goals

Do not:

- restructure `AnalysisDTO`
- sharpen or reduce the questionnaire
- retire `insights[]`
- implement mock-mode honesty wording
- redesign frontend report carriage
- add new WHY assets
- alter signal ranking
- alter confidence or banding
- alter statin annotation logic
- activate Gemini
- add fallback parsers
- create duplicate SSOT authority sources

## Validation commands

Inspect project scripts and run the narrowest relevant tests first.

At minimum, run targeted backend tests for:

- narrative compiler
- narrative payload WP-2
- validator v2
- clinician report runtime alignment
- proving harness

Then run the broader backend test command if feasible.

Report every command and result.

## Closure evidence required

Before finish, report:

- branch name
- work_id
- files changed
- summary of narrative compiler changes
- confirmation `NarrativePayloadV1` is used as governed input
- confirmation all five narrative sections are covered
- confirmation claim boundaries are enforced
- confirmation no questionnaire files were changed
- confirmation no Knowledge Bus files were changed
- confirmation no SSOT files were changed
- confirmation no `AnalysisDTO` restructuring occurred
- tests run and results
- known limitations
- whether Sprint 3 completion criteria are satisfied

## Final expected outcome

After this sprint, HealthIQ AI should have a governed deterministic Layer C implementation that uses:

`ReportV1 → NarrativePayloadV1 → NarrativeReportV1`

Sprint 4 may then focus on report carriage, `insights[]` retirement, mock-mode honesty, and user-facing coherence.