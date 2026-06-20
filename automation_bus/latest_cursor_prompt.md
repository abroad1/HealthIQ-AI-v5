---
work_id: P1-2
branch: work/P1-2-kidney-function-domain-card
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# P1-2 — Kidney Function Domain Card

## Objective

Implement the first missing launch-core domain selected by P1-1:

```text
Kidney function
```

This sprint must implement a bounded, non-diagnostic kidney function domain card / domain output using existing governed assets identified by P1-1.

The purpose is to move HealthIQ AI from three visible launch-core domains towards complete launch-core system coverage, while preserving the corrected Layer A / Layer B / Layer C architecture.

This is a controlled HIGH-risk implementation sprint because it may touch Layer B runtime behaviour, domain assembly, scoring/display integration and tests.

---

## Prerequisite

Do not start unless P1-1 has been merged to `main`.

Required file on `main`:

```text
docs/sprints/beta_readiness/P1-1_launch_core_domain_build_materials_map.md
```

If this file is not present on `main`, stop and report:

```text
P1-1 is not present on main. P1-2 must not proceed.
```

---

## Critical architectural boundary

This sprint is Layer B implementation work.

Layer B owns:

```text
biomarker interpretation
signal activation/suppression
domain/system reasoning
subsystem reasoning
WHY/root-cause
hierarchy
surfacing decisions
clinician-report content
prose/explainer selection
safety
provenance
```

Layer C, Gemini and frontend must not perform kidney-function reasoning.

Do not create frontend medical inference.

Do not use Gemini.

Do not create or rely on fallback parser logic.

Do not substitute global/default ranges where lab-provided ranges exist.

Do not create diagnostic CKD language unless it is already governed, explicitly supported, non-diagnostic, and safe. The default posture is educational kidney-function interpretation, not diagnosis.

---

## Branch and state checks

Start from `main`.

```powershell
git switch main
git pull
git status --short
git switch -c work/P1-2-kidney-function-domain-card
```

Do not proceed if the working tree is dirty.

Confirm the Automation Bus active work package/state file if required by SOP.

---

## First authority documents

Read these first, in this order:

```text
docs/strategy/beta_readiness/HEALTHIQ_AI_BETA_READINESS_DEFINITIVE_STRATEGY_FINAL_2026-06-20.md
docs/sprints/beta_readiness/P1-1_launch_core_domain_build_materials_map.md
docs/architecture/ADR-LAYER-BOUNDARY-RECONCILIATION-1.md
docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md
```

P1-1 is the immediate scope authority for this implementation sprint.

Do not exceed the kidney-function scope proven by P1-1.

---

## Additional authority and reference files

Read as relevant:

```text
docs/strategy/eight_block_beta_readiness/EIGHT_BLOCK_BETA_READINESS_COMPARISON_AND_PROGRAMME_RECOMMENDATION_2026-06-18.md
docs/strategy/LAYER_ARCHITECTURE_AUTHORITY_INDEX_2026-06-17_r2.md
docs/architecture/User Health to Systems Map_FINAL.md
docs/AUTHORITY_MAP.md
backend/ssot/scoring_policy.yaml
backend/core/analytics/domain_score_assembler.py
backend/core/analytics/wave1_subsystem_evidence.py
backend/core/contracts/narrative_payload_v1.py
backend/core/analytics/report_compiler_v1.py
backend/core/analytics/root_cause_compiler_v1.py
backend/ssot/retail_explainer_v1/registry.yaml
knowledge_bus/
knowledge_bus/compiled/
knowledge_bus/pathway_explainers_v1/
backend/tests/
docs/testing/
docs/intelligence/
docs/architecture/
```

If a path listed by P1-1 no longer exists or differs from the map, record that honestly and adjust only within the authorised scope.

---

## Implementation scope

Implement a bounded kidney function domain card / domain output using existing repository patterns.

The sprint may include, if required by the existing architecture:

```text
- domain assembler wiring for kidney function
- domain score/card output wiring
- subsystem evidence wiring where supported
- DTO/report inclusion where existing Layer B contracts require it
- deterministic tests for the kidney function domain output
- minimal documentation of implementation decisions
- build deliverable register update
```

The sprint must stay inside the kidney-function scope identified by P1-1.

---

## Kidney-function biomarker scope

Use only biomarkers supported by P1-1 and repository evidence.

Likely candidate markers to verify from P1-1 and existing assets:

```text
creatinine
eGFR
urea, only if supported
electrolytes, only where clearly relevant and supported
albumin/creatinine ratio, only if present and governed
```

Do not invent additional renal markers.

Do not create new interpretation logic for unavailable markers.

If a marker is absent from an uploaded panel, handle it through existing missing-marker patterns only where those patterns are already governed.

---

## Clinical safety rules

Kidney-function output must remain:

```text
educational
non-diagnostic
cautious
lab-range grounded
traceable
proportionate
```

Do not state or imply a diagnosis of CKD, kidney disease, renal failure or acute kidney injury unless an existing governed source explicitly allows the wording and the output remains non-diagnostic.

Preferred framing:

```text
kidney filtration markers
kidney function context
markers that can relate to filtration or renal handling
this may be worth discussing with a clinician if out of range
```

Avoid:

```text
you have CKD
this proves kidney disease
renal failure
diagnostic staging
urgent disease claims
```

If existing governed assets already include more specific wording, preserve the safety constraints around that wording.

---

## Lab-range rules

Use lab-provided reference ranges where available.

Do not hardcode global/default reference ranges.

Do not introduce new global reference intervals.

Derived calculations may only be used if already governed by existing code/policy and supported by P1-1.

If implementation would require new range policy, stop and report that a separate safety/scoring/range sprint is required.

---

## Scoring and policy rules

Inspect existing scoring rails before modifying anything.

If kidney function scoring is already present in `backend/ssot/scoring_policy.yaml`, reuse it.

Do not rewrite scoring policy broadly.

Do not create a new scoring model from memory.

If a minimal scoring-policy update appears necessary, only proceed if:

```text
- P1-1 identified it as required or expected;
- the existing scoring-policy structure clearly supports the change;
- the change is bounded to kidney function;
- tests are added or updated;
- the final report explains the policy change.
```

If scoring-policy ambiguity is significant, stop and report the blocker rather than improvising.

---

## Subsystem rules

Only implement kidney subsystem groupings that are supported by P1-1 and repository evidence.

Possible subsystem candidates must be evidence-backed.

Do not invent polished subsystem names solely for UX.

Subsystems remain Layer B.

Frontend must only render governed outputs.

---

## Prose, explainer and clinician-report rules

This sprint may wire existing kidney-function material into governed Layer B surfaces if that is required by the runtime pattern.

Do not create a broad prose expansion sprint inside P1-2.

Do not write a full new kidney explainer estate.

Do not use Gemini to produce prose.

If existing retail explainer, pathway explainer or clinician-report assets are insufficient, record the gap as a carry-forward to P2-1 or later Layer B prose work.

---

## Runtime constraints

Do not:

```text
- read raw Pass 3 material at runtime
- read raw Knowledge Bus research files at runtime
- modify Knowledge Bus packages
- promote Pass 3 material
- activate blocked/context-dependent signals
- add frontend medical inference
- add Gemini runtime calls
- add fallback parser logic
```

---

## Required deliverables

### 1. Runtime/domain implementation

Implement the bounded kidney-function domain output according to existing architecture and P1-1 evidence.

The exact files are not prescribed because Cursor must inspect the current codebase and follow existing patterns.

Expected candidate areas may include:

```text
backend/core/analytics/domain_score_assembler.py
backend/core/analytics/wave1_subsystem_evidence.py
backend/core/analytics/report_compiler_v1.py
backend/core/contracts/
backend/ssot/scoring_policy.yaml
backend/tests/
```

Only modify what is necessary.

### 2. Tests

Add or update targeted tests proving the kidney-function domain output works.

Tests should verify, as applicable:

```text
- kidney function domain appears in the expected output surface
- relevant biomarkers map correctly
- missing biomarkers do not create fabricated claims
- lab-provided ranges are respected
- output remains non-diagnostic
- no Layer C/Gemini/frontend inference is required
- existing domains are not regressed
```

Run the most relevant existing test suite for affected files.

If a test cannot be run in the environment, state that honestly and provide the reason.

### 3. Implementation note

Create:

```text
docs/sprints/beta_readiness/P1-2_kidney_function_domain_card.md
```

This should be concise and include:

```markdown
# P1-2 — Kidney Function Domain Card

## 1. Summary
- what was implemented
- what remains out of scope

## 2. P1-1 evidence used
- key evidence from P1-1 that justified kidney function as first implementation domain

## 3. Runtime changes
- concise description of the domain/card/scoring/report/test changes

## 4. Safety boundaries
- non-diagnostic wording
- lab-range use
- avoided unsupported CKD claims
- no Gemini / no frontend inference

## 5. Tests and validation
- tests added/updated
- commands run
- result

## 6. Carry-forwards
- prose/explainer gaps
- clinician-report gaps
- UX/display implications
- safety/provenance gaps
```

Do not turn this into a large audit paper.

### 4. Build deliverable register update

At closure, update:

```text
docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md
```

Append a short entry:

```markdown
## P1-2 — Kidney function domain card

**Status:** Complete / Partial / Blocked  
**Date closed:** <YYYY-MM-DD>  
**Programme block(s):** Block 1 Core health systems model; Block 2 Subsystems and depth model; Block 3 Layer B intelligence/prose substrate  

### Delivered / ticked off
- <what this sprint completed against the beta-readiness programme>
- <major implementation or validation outcome>

### Carry-forwards
- <what still needs to be done later>
- <known gaps exposed by this sprint>

### Blockers / risks
- <only material blockers or risks that affect future work>

### Recommended next sprint
- <next work package recommendation>
```

Keep the register entry short.

Do not list every file touched.

Do not duplicate the full implementation note or audit.

---

## Expected changed file categories

Expected categories may include:

```text
backend/core/analytics/
backend/core/contracts/
backend/ssot/
backend/tests/
docs/sprints/beta_readiness/
automation_bus/
```

Do not change frontend files unless the existing architecture requires a purely render-only snapshot/test update. If any frontend file appears necessary, stop and explain why before making the change if the workflow allows; otherwise record it as a blocker.

Do not change Knowledge Bus packages or Pass 3 source material.

Do not update the final strategy baseline.

Do not update AUTHORITY_MAP.

---

## Validation

Run:

```powershell
git diff --stat
git diff --name-only
git status --short
```

Run relevant tests.

Suggested test discovery commands:

```powershell
python -m pytest --collect-only
```

Then run the smallest relevant tests for the touched backend/analytics/report/DTO paths.

If existing project test commands are documented, use the documented commands.

At minimum, the final report must state:

```text
- tests run
- whether they passed
- any tests not run
- reason any tests could not be run
```

If tests fail because of pre-existing unrelated failures, isolate and document the failure.

If tests fail because of this sprint, fix or report the sprint as blocked.

---

## Required final report

Return:

```text
- branch name
- files changed
- summary of kidney-function implementation
- whether scoring policy changed
- whether report/DTO/compiler surfaces changed
- tests run and results
- safety constraints applied
- carry-forwards
- recommended next sprint
- confirmation no frontend inference added
- confirmation no Gemini added
- confirmation no fallback parser added
- confirmation no Knowledge Bus packages or Pass 3 artefacts changed
- validation output
- git status --short
```

Do not merge until Claude audit, GPT architectural review and human approval.

---

## Acceptance criteria

This sprint is complete only if:

```text
1. Kidney function is implemented as a bounded launch-core domain/card output using existing governed assets and P1-1 evidence.

2. The implementation remains Layer B governed and does not move medical reasoning into Layer C, Gemini or frontend.

3. The output is non-diagnostic and does not make unsupported CKD/kidney disease claims.

4. Lab-provided reference ranges remain authoritative where available.

5. No fallback parser logic is introduced.

6. No Gemini runtime or prompt path is introduced.

7. No Knowledge Bus packages or raw Pass 3 artefacts are modified or read at runtime.

8. Targeted tests are added or updated and run.

9. Existing implemented domains are not regressed by the kidney-function addition.

10. `docs/sprints/beta_readiness/P1-2_kidney_function_domain_card.md` is created.

11. `docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md` is updated with a short P1-2 entry.

12. The final report clearly states carry-forwards into P2 prose/explainer work, P3 safety/provenance work, and P5 UX work where relevant.
```
