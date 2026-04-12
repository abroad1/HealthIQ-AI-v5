---
work_id: BE-W2-RQ3
branch: feature/results-explanation-surfacing-balanced-systems
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# BE-W2-RQ3 — Results explanation surfacing and balanced systems narrative

## Objective

Deliver the next bounded Wave 2 remediation pass to materially improve the explanatory depth, balance, and confidence-building quality of the results experience using existing governed deterministic structures already present in the runtime result contract.

This sprint must not depend on live Gemini enablement.
This sprint must not change analytical reasoning logic.
This sprint must not introduce a second narrative authority.

The required outcome is:

- the results experience explains not only what appears suboptimal, but also which systems look stable / well-regulated / reassuring on this panel and why
- existing richer deterministic explanation structures already present in the stored result contract are selectively surfaced in a safe, bounded, user-facing way
- the default results experience becomes more metabolically intelligent and less one-sided without becoming alarmist or speculative
- the product moves closer to a true metabolic reasoning engine rather than a concern-only pattern detector

---

## Stage 1A — Authority Preflight (MANDATORY)

### Runtime truth already established

Repo/runtime investigation has established that:

- the results API carries a deep structured stack in `meta`, especially:
  - `meta.insight_graph`
  - `meta.explainability_report`
  - `meta.burden_vector`
  - `meta.narrative_runtime`
- the default results page currently leads with:
  - `clinician_report_v1`
  - `clusters`
  - `biomarkers`
- `meta.explainability_report` is stored on the result object but is not currently rendered by any frontend module
- the deterministic compiler/report layer is currently the main trustworthy explanation layer
- `insights[]` is often thin because the narrative runtime commonly resolves to mock/deterministic mode when live narrative LLM is not enabled

This sprint must not guess a different runtime truth.

### Authoritative backend files for this sprint

At minimum, inspect and use the actual current versions of:

- `backend/app/routes/analysis.py`
- `backend/core/dto/builders.py`
- `backend/core/pipeline/orchestrator.py`
- `backend/core/analytics/report_compiler_v1.py`
- `backend/core/analytics/explainability_builder.py`
- any contracts / helpers that define the explainability report and clinician report structures actually used in the runtime path

### Authoritative frontend files for this sprint

At minimum, inspect and use the actual current versions of:

- `frontend/app/(app)/results/page.tsx`
- `frontend/app/components/insights/InsightPanel.tsx`
- `frontend/app/components/results/RootCauseEvidenceSummary.tsx`
- `frontend/app/components/clusters/ClusterSummary.tsx`
- `frontend/app/components/results/ClinicianReportRenderer.tsx`

If hardening finds the active rendering/component paths differ, Claude must cite the exact actual files in evidence and hardening may narrow or correct touched-file scope. Cursor must not improvise beyond those verified files.

---

## Stage 1B — Reality Check

This sprint addresses real UAT and contract findings and is not a no-op.

Confirmed current gaps include:

- the product is still too heavily weighted toward lead concerns and weaker patterns
- the experience does not adequately explain which systems appear healthy / stable / well-regulated
- richer deterministic explanation structures exist in storage, especially `meta.explainability_report`, but are not currently surfaced
- the deterministic compiler layer is stronger than the current Layer C narrative cards in default gated environments
- the product therefore underuses existing governed explanation material that could improve confidence, balance, and credibility

---

## Stage 1C — Intelligence Preflight

This sprint changes emitted user-facing reasoning and explanation presentation.

It therefore affects:

- what explanatory content is surfaced from stored deterministic contracts
- how balanced system-level interpretation is presented
- how reassuring / stable system evidence is communicated
- how default results guide user trust

This is HIGH risk because it changes what the product says to the user, even though it must not change the underlying analytical logic.

No downgrade is permitted.

---

## Architectural Decisions Locked For This Sprint

Cursor must implement these decisions exactly.

### 1. Existing deterministic structures must remain the sole authority

This sprint must use only existing governed deterministic structures already produced in the runtime result contract, including where appropriate:

- `clinician_report_v1`
- `meta.insight_graph`
- `meta.explainability_report`
- existing cluster and biomarker evidence structures

Do not introduce a second narrative authority.
Do not invent a parallel summary engine.
Do not author new free-floating medical narrative disconnected from governed structures.

### 2. Balanced system narrative is required

The results experience must not only describe strain / concern / suboptimal patterns.

It must also surface, in a bounded and evidence-led way:

- systems or domains that appear reassuring / stable / well-regulated on this panel
- what marker evidence supports that interpretation
- how those strengths shape a more balanced reading of the overall panel

This is a product requirement for this sprint, not an optional enhancement.

### 3. Balanced narrative must remain evidence-led and non-alarmist

“Healthy systems” or “reassuring patterns” must only be surfaced where deterministic evidence supports that claim.

Do not produce generic positivity.
Do not overstate normal findings.
Do not imply diagnoses or guarantees.

### 4. `meta.explainability_report` is an eligible surfacing source

Because investigation confirmed that `meta.explainability_report` is stored but not rendered, it is in scope to selectively surface a sanitized, bounded subset of that structure if needed.

However:
- do not dump raw technical/explainability payloads directly into the UI
- do not expose arbitration/debug internals in consumer-facing language
- use it only through carefully shaped compiler/presentation logic

### 5. No analytical reasoning changes

This sprint must not change:

- ranking logic
- signal evaluation
- cluster logic
- burden logic
- insight graph construction logic
- phenotype firing logic
- any governed rule determining what the engine believes

It may change only how the existing governed output is compiled, shaped, and presented.

### 6. Gemini enablement is explicitly out of scope

Do not turn this into an env/config sprint.
Do not depend on live Gemini to satisfy acceptance.

This sprint must improve the product meaningfully using deterministic structures alone.

### 7. Default results remain consumer-safe

If richer internal explanation structures are surfaced, they must be translated into user-safe, plain-English presentation.

Technical/internal-only structures may be partially surfaced only through bounded compiler logic or advanced/clinician presentation where appropriate.

---

## Scope

## Required Changes

### A. Balanced systems narrative

Add a bounded explanation layer that explicitly identifies, where supported by existing deterministic evidence:

- systems or domains that appear broadly stable / reassuring / well-regulated on this panel
- the key evidence supporting that conclusion
- how those stronger systems temper or contextualise weaker findings

This may be a new bounded section on the results page or an enhancement to an existing section, but it must be driven by existing deterministic result data.

### B. Explainability surfacing

Selectively surface a sanitized subset of currently hidden deterministic explanation material, especially from `meta.explainability_report` if that is the best governed source, to deepen the results experience without exposing raw internal structures.

The sprint must decide at implementation time, based on actual repo truth, the smallest safe subset needed to improve:
- balance
- explanatory depth
- confidence-building interpretation

### C. Compiler / presentation alignment

Update the backend compiler and frontend rendering so that:

- hero
- Why / lead hypothesis explanation
- system-level interpretation
- clinician report, where relevant

all remain aligned and non-contradictory after balanced-system surfacing is added.

### D. Preserve boundedness

Use the smallest safe change set needed to:
- surface reassuring/healthy system interpretation
- surface richer deterministic explanation
- avoid raw explainability/debug leakage
- keep default results understandable and premium-feeling

---

## Explicit Non-Goals

- no Gemini enablement / env toggle work
- no changes to analytical ranking policy
- no changes to signal evaluator, clusters, burden logic, or insight graph construction
- no upload/parser/questionnaire work
- no broad redesign of the entire results page
- no second narrative authority source
- no speculative claims that exceed deterministic evidence
- no raw technical dump of `explainability_report`

---

## STOP Conditions (MANDATORY)

Cursor must STOP immediately if any of the following become true:

1. Surfacing balanced system narrative would require changing analytical logic rather than using existing deterministic outputs
2. `meta.explainability_report` or related structures cannot be surfaced safely without exposing internal/debug/arbitration material and no bounded shaping path exists
3. Existing result structures do not contain enough deterministic evidence to support a balanced healthy-system layer in this sprint
4. A second narrative authority source would be introduced
5. A touched file would cross into core analytical reasoning boundaries beyond output compilation/presentation
6. The only way to satisfy the sprint would be to enable live Gemini
7. The sprint would require broad redesign of the whole results page instead of bounded explanation surfacing

If any STOP condition triggers, do not improvise. Report the blocker.

---

## Phase Execution Model

### Phase 1 — Deterministic explanation surfacing

Implement the bounded backend/frontend changes required so that:

- reassuring / stable systems can be surfaced where deterministic evidence supports them
- richer deterministic explanation material already present in runtime is selectively surfaced
- default results become more balanced and confidence-building
- no analytical logic changes occur

### Phase 2 — Validation

Verify with targeted tests and browser checks that:

- the new balanced narrative is grounded in deterministic evidence
- no raw internal explainability/debug structures are exposed
- default results feel more balanced without becoming generic or hand-wavy
- existing hero / Why / clinician report layers remain valid and deterministic

---

## Regression Targets

Must verify all of the following.

### Results contract

- `GET /api/analysis/result` still returns a valid DTO
- `clinician_report_v1` still compiles correctly
- any newly surfaced explanation slice is sourced from existing deterministic result structures
- no required fields for current results rendering are lost

### Balanced systems narrative

- at least one reassuring / stable / healthy system-level interpretation can be surfaced when supported by the current panel
- the surfaced explanation names the evidence supporting that positive interpretation
- the new balanced layer does not contradict the lead concern or Why layer
- no unsupported positivity is introduced

### Explainability surfacing

- if `meta.explainability_report` or related structures are used, only a bounded sanitized subset is surfaced
- no raw arbitration/debug language appears in the default consumer-facing layer
- no second authority source is introduced

### Consumer safety and clarity

- the default results page remains readable and premium-feeling
- the new layer improves balance and confidence rather than cluttering the page
- no raw internal IDs, policy keys, or technical dump content appear

### Determinism

- same result payload produces the same surfaced balanced-system narrative
- no randomness
- no hidden fallback content source
- no implicit dependence on runtime order or mutable global state

### Narrative runtime neutrality

- the sprint still passes whether live Gemini is enabled or not
- no new dependency on `insights[]` quality for core acceptance

---

## Test Requirements

Minimum required tests must cover:

1. compiler/presentation helpers changed by this sprint
2. a representative payload where reassuring/stable system interpretation is surfaced from deterministic evidence
3. proof that surfaced explanation content comes from existing governed structures, not new hand-authored authority
4. targeted frontend rendering checks for the new balanced explanation layer
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
- do not perform broad redesign beyond the bounded explanation-surfacing improvement
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
   - balanced reassuring/stable system narrative is now surfaced
   - the results experience is less one-sided
   - surfaced explanation remains deterministic and consumer-safe
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