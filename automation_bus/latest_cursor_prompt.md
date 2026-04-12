---
work_id: BE-W2-RQ1
branch: feature/wave2-results-contract-quality
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# BE-W2-RQ1 — Wave 2 Results Contract and Narrative Quality

## Objective

Deliver a single governable Wave 2 remediation pass that materially improves the quality, clarity, and trustworthiness of the results experience without changing analytical reasoning logic.

This sprint must correct the current gap where the core end-to-end journey works, but the returned results feel thin, overly technical, and insufficiently personalised because consumer-facing output is currently dominated by deterministic compiler text and governance/debug language.

This is not a transport/runtime sprint.
This is not a broad product redesign.
This is not a Gemini-enablement sprint.

The required outcome is:

- default consumer-facing results no longer expose internal governance/debug language
- hero interpretation explains the main health story in plain English
- system-group output is more pattern-specific and less boilerplate
- supporting / contradictory / missing markers are surfaced more clearly
- clinician report reads coherently and no longer leaks ugly raw formatting
- the page remains useful even when live Gemini narrative is not enabled

---

## Stage 1A — Authority Preflight (MANDATORY)

### Runtime truth already established

The current results experience is composed from these layers:

- `POST /api/analysis/start`
  - returns start metadata only
- `GET /api/analysis/result`
  - returns DTO built by `build_analysis_result_dto(...)`
- hero and clinician-facing copy are derived primarily from:
  - `meta.insight_graph.report_v1`
  - `compile_clinician_report_v1(...)`
- optional richer narrative summaries are sourced from:
  - `insights[]`
  - produced by `InsightSynthesizer`
  - which may use Gemini or may fall back to mock/deterministic clients depending on env

This sprint must not guess a different runtime truth.

### Authoritative backend files for this sprint

At minimum, inspect and use the actual current versions of:

- `backend/app/routes/analysis.py`
- `backend/core/dto/builders.py`
- `backend/core/reports/report_compiler_v1.py`
- the module that defines `compile_clinician_report_v1(...)`
- any directly related report-v1 assembly or presentation helper modules actually used in the runtime path

### Authoritative frontend files for this sprint

At minimum, inspect and use the actual current versions of:

- `frontend/app/(app)/results/page.tsx`
- `frontend` component(s) that render:
  - hero interpretation
  - system groups
  - insights / narrative summaries
  - clinician report
- current repo evidence previously identified `InsightPanel.tsx` as one leakage point for:
  - signal-derived badges
  - policy version badges
  - technical tie-break language

If hardening finds the active rendering component paths differ from this assumed set, Claude must cite the exact actual files in evidence and hardening may narrow or correct touched-file scope. Cursor must not improvise beyond those verified files.

### Non-governing facts to respect

- Gemini/live LLM output is env-gated and may be off in this path
- the hero is not the Gemini layer by default
- therefore this sprint must not rely on live Gemini being enabled in order to meet acceptance

---

## Stage 1B — Reality Check

This sprint addresses real UAT findings and is not a no-op.

Confirmed UAT problems in the current default results experience include:

- hero interpretation exposes internal governance language and signal IDs
- system-group explanations are too generic
- supporting / contradictory markers are not surfaced clearly enough
- clinician report is thin and awkwardly formatted
- output quality feels like structured backend text with light templating, not a polished end-user interpretation
- live Gemini is env-dependent and cannot be assumed

---

## Stage 1C — Intelligence Preflight

This sprint changes emitted user-facing reasoning and report presentation.

It therefore affects:

- output generation text
- ranking explanation presentation
- what evidence is shown to users
- clinician report wording and structure
- frontend presentation of backend-generated interpretation

This is HIGH risk because it changes what the product says to the user, even though it must not change the underlying analytical logic.

No downgrade is permitted.

---

## Architectural Decisions Locked For This Sprint

Cursor must implement these decisions exactly.

### 1. Default consumer layer must not expose internal governance/debug language

The default consumer-facing results layer must not display raw internal constructs such as:

- raw signal IDs
- raw policy IDs / ranking policy version strings
- “technical tie-break” as user-facing hero framing
- policy-ordered ambiguity/governance phrasing as the primary explanation

If such data must remain available for technical/advanced use, it must not dominate the default consumer layer.

### 2. Hero interpretation is a consumer summary, not a policy explanation

The hero must answer, in plain English:

- what the lead health concern/pattern is
- why it was selected
- which markers most strongly support it
- what the user should understand from it

The hero must not lead with ranking mechanics.

### 3. System-group text must become pattern-specific

System-group descriptions must be materially more tied to the actual marker pattern returned in that analysis.

Generic educational boilerplate may remain as secondary support, but it must not be the primary explanation when more specific deterministic evidence is already available.

### 4. Supporting / contradictory / missing marker transparency must improve

The sprint must use existing deterministic structured data where available to make it clearer:

- which markers support the current interpretation
- which markers weaken or complicate it
- which missing markers limit confidence

This must be done without exposing raw internal debugging structures.

### 5. Clinician report quality must improve without changing analytical logic

The clinician report may remain deterministic and compiler-driven in this sprint.
It does not need to become a separate Gemini document.

But it must:

- read coherently
- avoid raw floating-point artefacts
- avoid awkward duplication
- avoid raw signal/policy leakage in consumer-facing sections
- better reflect the structured evidence already present in `report_v1`

### 6. Gemini enablement is not part of this sprint

Do not turn this into an env/config sprint.

Do not require live Gemini for acceptance.

If the page contains runtime provenance indicators or empty-state logic related to narrative runtime, they may be softened or clarified, but this sprint must not be blocked on enabling Gemini.

### 7. Analytical reasoning must not change

This sprint must not change:

- ranking logic
- cluster logic
- signal evaluation
- burden calculations
- insight graph construction
- analytical hypotheses

The sprint changes presentation contract and report compiler output quality, not the engine’s reasoning.

---

## Scope

## Required Changes

### A. Consumer-facing hero cleanup

Update the backend/frontend contract so the default hero:

- no longer leads with governance/debug language
- does not expose raw signal IDs or policy IDs in primary consumer presentation
- provides a plain-English lead interpretation with evidence-aware explanation

This includes, where needed:

- compiler-side page 1 wording cleanup
- frontend hero badge/label cleanup
- removal or relocation of governance labels from default consumer view

### B. Clinician report v1 copy and formatting improvement

Improve `compile_clinician_report_v1(...)` and any directly related compiler/presentation helpers so that:

- confidence values are formatted cleanly
- duplicated or awkward phrasing is removed
- root-cause and confirmatory-test sections read coherently
- the report better reflects existing structured evidence without sounding like an internal debug artifact

### C. System-group presentation improvement

Improve the current system-group experience so the displayed explanation is more closely tied to the actual cluster pattern and contributing markers.

This must use existing deterministic data already present in the result contract where possible.
Do not invent a second narrative authority.

### D. Supporting-marker transparency

Improve the default results experience so supporting / opposing / missing evidence is clearer.
Use existing structured evidence in the returned result shape where available.

Do not expose raw internal payloads directly.
Do not invent speculative medical claims.

### E. Frontend consumer/advanced separation

If a distinction already exists between default results and advanced analysis, this sprint may move more technical material into the advanced/technical area rather than deleting it outright.

But the default consumer-facing layer must become cleaner.

---

## Explicit Non-Goals

- no Gemini enablement / env toggle work
- no changes to analytical ranking policy
- no changes to signal evaluator or insight graph construction logic
- no questionnaire redesign
- no upload/parser changes
- no SSE/runtime transport work
- no large visual redesign of the whole results page
- no new separate narrative authority source
- no hand-authored clinical prose outside the governed compiler/presentation path

---

## STOP Conditions (MANDATORY)

Cursor must STOP immediately if any of the following become true:

1. Improving consumer-facing results quality would require changing analytical ranking, signal evaluation, or cluster logic rather than presentation/compilation
2. The required quality improvement cannot be achieved without enabling live Gemini
3. The existing result contract lacks enough structured evidence to improve hero/system/supporting-marker output within this sprint
4. A second narrative authority source would be introduced
5. A touched file would cross into core analytical reasoning boundaries beyond output compilation/presentation
6. The only way to hide governance/debug language would be to remove data needed by clinician/advanced users with no bounded separation option
7. The sprint would require broad redesign of the entire results UI rather than targeted contract/presentation improvement

If any STOP condition triggers, do not improvise. Report the blocker.

---

## Phase Execution Model

### Phase 1 — Contract and presentation improvement

Implement the bounded backend/frontend changes required so that:

- consumer hero is plain English and evidence-aware
- governance/debug leakage is removed from default consumer presentation
- clinician report wording/formatting improves
- system-group and supporting-marker visibility improve using existing deterministic inputs

### Phase 2 — Validation

Verify with targeted tests and browser checks that:

- core analytical outputs still exist
- user-facing presentation quality is materially improved
- default consumer layer no longer shows internal policy/signal language
- advanced/technical layers still function as intended if present

---

## Regression Targets

Must verify all of the following.

### Results contract

- `GET /api/analysis/result` still returns a valid DTO
- `clinician_report_v1` still compiles correctly
- no required fields for current results rendering are lost

### Consumer hero

- no raw signal IDs in default hero
- no raw policy version strings in default hero
- no “technical tie-break” lead message in default hero
- hero now explains the actual concern in plain English

### System groups

- system-group card text is more specific to the actual pattern
- contributing markers are still shown
- no breakage in cluster rendering

### Supporting-marker transparency

- supporting / contradictory / missing markers are surfaced more clearly
- no unsupported claims are introduced
- no raw debug payload leakage

### Clinician report

- no raw floating confidence artefacts like `0.6000000000000001`
- duplicated/awkward phrasing removed
- sections remain structurally intact

### Narrative runtime neutrality

- page remains acceptable whether live Gemini is enabled or not
- no new dependency on env-specific LLM runtime for core acceptance

### Determinism

- same result payload produces the same compiled/rendered output
- no randomness
- no hidden fallback content source
- no implicit dependence on runtime order or mutable global state

---

## Test Requirements

Minimum required tests must cover:

1. consumer-facing hero no longer exposes raw internal governance language
2. clinician report formatting/copy improvements on representative report payloads
3. any compiler helpers changed by this sprint
4. targeted frontend rendering checks for the cleaned hero/presentation contract
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
   - default hero no longer shows internal governance language
   - system-group output is more specific
   - supporting-marker transparency is improved
   - clinician report formatting is improved
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