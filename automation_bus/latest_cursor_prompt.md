---
work_id: BE-W2-RQ2
branch: feature/results-why-contract-depth
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# BE-W2-RQ2 — Results contract depth: hero runner-up visibility and Why explanation

## Objective

Deliver the next bounded Wave 2 remediation pass to improve the explanatory depth of the results experience without changing analytical reasoning logic.

This sprint must address two confirmed UAT issues:

- UAT-027 — the hero says there was a close call between top findings but does not show the competing secondary finding
- UAT-028 — the root-cause / Why layer lacks a coherent explanatory narrative and feels like structured fragments rather than a consultant-style walkthrough

This is not a Gemini-enablement sprint.
This is not a ranking-policy sprint.
This is not a broad results-page redesign.

The required outcome is:

- when the hero indicates a close call / tie-break / ranked ambiguity, the user can see the competing finding and why it did not lead
- the Why layer becomes meaningfully more explanatory using governed existing deterministic evidence
- the default results experience remains deterministic and useful even when live Gemini narrative is not enabled

---

## Stage 1A — Authority Preflight (MANDATORY)

### Runtime truth already established

The current results experience is composed from these layers:

- default hero consumes:
  - `clinician_report_v1.sections.page1`
- clinician report consumes:
  - `clinician_report_v1`
- richer ranked finding detail exists in:
  - `meta.insight_graph.report_v1.top_findings`
- structured root-cause / Why data exists in:
  - `meta.insight_graph.report_v1.root_cause_v1`
  - mirrored into `clinician_report_v1.sections.root_cause`
- optional narrative summaries are separate:
  - `insights[]`
  - provenance recorded in `meta.narrative_runtime`

This sprint must not guess a different runtime truth.

### Authoritative backend files for this sprint

At minimum, inspect and use the actual current versions of:

- `backend/app/routes/analysis.py`
- `backend/core/dto/builders.py`
- `backend/core/analytics/report_compiler_v1.py`
- the module that defines `compile_clinician_report_v1(...)`
- the module that compiles or structures `report_v1`
- any directly related report / explainability helper modules actually used in the runtime path

### Authoritative frontend files for this sprint

At minimum, inspect and use the actual current versions of:

- `frontend/app/(app)/results/page.tsx`
- `frontend/app/components/insights/InsightPanel.tsx`
- `frontend/app/components/results/RootCauseEvidenceSummary.tsx`
- `frontend/app/components/results/ClinicianReportRenderer.tsx`

If hardening finds the active rendering paths differ, Claude must cite the exact actual files in evidence and hardening may narrow or correct touched-file scope. Cursor must not improvise beyond those verified files.

---

## Stage 1B — Reality Check

This sprint addresses real UAT and runtime-truth findings and is not a no-op.

Confirmed current issues:

- the hero can say “close call between top findings” while not showing the competing finding because the hero reads `clinician_report_v1.sections.page1`, not `meta.insight_graph.report_v1.top_findings`
- richer ranking detail already exists in payload storage under `top_findings`, but the default hero does not use it
- the current Why layer is structured compiler output, not a true explanatory walkthrough
- no separate deep Why narrative field exists today
- `meta.explainability_report` may exist in `meta`, but is not currently used as the default Why layer

---

## Stage 1C — Intelligence Preflight

This sprint changes emitted user-facing reasoning and report presentation.

It therefore affects:

- what explanation is shown for the lead concern
- how runner-up findings are surfaced
- how root-cause / Why reasoning is translated into user-visible output
- clinician-report explanatory depth

This is HIGH risk because it changes what the product says to the user, even though it must not change the underlying analytical logic.

No downgrade is permitted.

---

## Architectural Decisions Locked For This Sprint

Cursor must implement these decisions exactly.

### 1. Runner-up visibility must come from existing ranked data

When the current hero contract indicates a close call / technical tie-break / ranked ambiguity, the system must surface the competing finding using existing ranked data already present in runtime payloads.

The authoritative ranked source for this sprint is:

- `meta.insight_graph.report_v1.top_findings`

Cursor must not invent a second ranking source.

### 2. The hero contract must not rely only on `co_primary_signal_ids`

The current gap exists because the hero row for the competing finding is gated on `co_primary_signal_ids`, which may be empty even when `top_findings` contains a valid runner-up.

This sprint must resolve that contract gap explicitly.

Cursor must not leave the hero dependent on `co_primary_signal_ids` alone if that preserves the current failure mode.

### 3. Why depth must be improved using existing deterministic evidence

This sprint must deepen the Why layer using already-governed deterministic structures such as:

- `root_cause_v1`
- `report_v1`
- existing explainability structures actually present in the runtime path

Do not add a second narrative authority.
Do not invent speculative medical claims.
Do not require live Gemini.

### 4. No analytical reasoning changes

This sprint must not change:

- ranking logic
- tie-break logic
- signal evaluation
- hypothesis ordering rules
- cluster logic
- burden logic
- insight graph construction logic

It may change how the existing results are compiled and presented, not how they are decided.

### 5. Default results must remain consumer-safe

The default consumer-facing Why layer should feel like a competent consultant explanation, but it must remain bounded, evidence-led, and deterministic.

Technical/debug language must not return to the default layer as the price of adding depth.

### 6. Gemini enablement is not part of this sprint

Do not turn this into a narrative runtime / env sprint.

If the investigation found `insights[]` are mock/deterministic in this environment, accept that as current truth and do not couple this sprint to turning on live Gemini.

---

## Scope

## Required Changes

### A. Hero runner-up contract improvement

Update the backend/frontend contract so that when the hero indicates a close-call or ranked-ambiguity situation:

- the competing secondary finding is shown
- the user can understand what it was
- the user can understand, briefly, why it did not become the lead concern

This must be sourced from existing ranked data, not invented text.

### B. Why explanation depth improvement

Improve the current Why/root-cause output so it is more coherent and explanatory.

It must better answer:

- what pattern was seen
- why that pattern led to the current lead hypothesis
- which markers support it
- which markers pull against it
- what is missing and why that limits confidence

This may use richer deterministic fields already available in:
- `root_cause_v1`
- `report_v1`
- explainability structures already present in runtime payloads

### C. Compiler and renderer alignment

Update compiler and frontend rendering so that:

- the hero
- the lead hypothesis evidence / Why area
- the clinician report

all reflect the same improved explanatory contract without duplicating contradictory text.

### D. Preserve boundedness

Use the smallest safe change set needed to:
- expose runner-up context
- deepen Why explanation
- keep determinism
- avoid creating a new narrative authority

---

## Explicit Non-Goals

- no Gemini enablement / env toggle work
- no changes to analytical ranking policy
- no changes to signal evaluator or insight graph construction logic
- no upload/parser/questionnaire work
- no SSE/runtime transport work
- no broad redesign of the entire results page
- no second narrative authority source
- no broad clinician-report rearchitecture outside this bounded scope

---

## STOP Conditions (MANDATORY)

Cursor must STOP immediately if any of the following become true:

1. Exposing the runner-up finding requires changing ranking logic rather than using existing ranked payloads
2. Deepening the Why layer would require inventing new unsupported medical reasoning rather than reusing existing deterministic evidence
3. The existing result contract does not contain enough structured data to improve runner-up visibility or Why depth within this sprint
4. A second narrative authority source would be introduced
5. A touched file would cross into core analytical reasoning boundaries beyond output compilation/presentation
6. The only way to improve Why depth would be to enable live Gemini
7. The sprint would require broad redesign of the entire results page rather than targeted contract/presentation improvement

If any STOP condition triggers, do not improvise. Report the blocker.

---

## Phase Execution Model

### Phase 1 — Contract and presentation improvement

Implement the bounded backend/frontend changes required so that:

- close-call hero states show the competing finding
- the Why layer is more explanatory using existing deterministic evidence
- clinician and consumer presentation remain aligned
- no analytical logic changes occur

### Phase 2 — Validation

Verify with targeted tests and browser checks that:

- the competing finding is shown in close-call scenarios
- Why explanation is materially deeper and clearer
- deterministic reasoning is unchanged
- default consumer layer remains free of raw internal debug leakage

---

## Regression Targets

Must verify all of the following.

### Results contract

- `GET /api/analysis/result` still returns a valid DTO
- `clinician_report_v1` still compiles correctly
- no required fields for current results rendering are lost

### Hero runner-up visibility

- in a close-call / tie-break / ambiguity scenario, the hero now shows the competing finding
- the competing finding is sourced from existing ranked data
- the hero explains briefly why the lead concern won
- no raw policy IDs or raw signal IDs appear in the default hero

### Why depth

- Why output is materially richer than the current bullet-fragment experience
- supporting markers are shown clearly
- opposing / complicating markers are shown clearly
- missing markers / confidence limits are shown clearly
- no unsupported claims are introduced

### Clinician report

- report remains structurally valid
- Why-related sections are more coherent and readable
- output remains deterministic
- no raw floating artefacts or awkward formatting regressions

### Narrative runtime neutrality

- results remain acceptable whether live Gemini is enabled or not
- no new dependency on env-specific LLM runtime for core acceptance

### Determinism

- same result payload produces the same compiled/rendered output
- no randomness
- no hidden fallback content source
- no implicit dependence on runtime order or mutable global state

---

## Test Requirements

Minimum required tests must cover:

1. hero runner-up visibility in a representative close-call result payload
2. any compiler helpers changed by this sprint
3. Why-layer rendering / formatting improvements for representative root-cause payloads
4. targeted frontend rendering checks for hero and Why contract changes
5. no regression to results-page loading for an existing completed analysis result

Use the smallest relevant test scope.
Do not expand into broad unrelated suite creation.

---

## Execution Rules

- follow this prompt exactly
- do not turn this into a Gemini enablement sprint
- do not change analytical reasoning
- do not invent a second narrative source
- do not widen into upload/questionnaire/parser work
- do not perform broad redesign beyond the bounded contract/presentation improvement
- do not modify unrelated files

---

## Deliverables

Cursor must return:

1. files changed
2. exact backend compiler/presentation files touched
3. exact frontend rendering files touched
4. implementation summary
5. tests run and results
6. before/after evidence that:
   - the competing finding is shown in close-call states
   - Why output is deeper and clearer
   - consumer-facing explanation remains deterministic and clean
7. any blockers encountered

---

## Governance

This is HIGH-risk governed output work.

Requires:

- Claude hardening
- kernel start
- controlled execution
- kernel finish
- gate evidence
- Claude audit summary
- GPT architectural review
- dual approval before merge

No shortcuts permitted.