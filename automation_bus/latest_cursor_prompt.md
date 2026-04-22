---
work_id: N-9B
branch: feature/n-9b-post-validation-runtime-refinement
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# N-9B — Post-validation runtime refinement

## Objective

Implement the single bounded refinement sprint identified by N-9 so the deterministic runtime output is strong enough for controlled frontend re-entry.

This is a HIGH-risk sprint because it is expected to touch the narrative compiler and possibly bounded backend output assembly.

This is not a frontend redesign sprint.
Do not widen into broad UX work.
Do not introduce Gemini or any other LLM dependency.
Do not reopen the architecture from N-2.
Do not start broad new asset-authoring work unless a tiny patch-level governed content fix is strictly required and justified.

The purpose of N-9B is to close the specific runtime-quality gaps identified by N-9, not to invent a new narrative system.

---

## Strategic context already settled

The following are already decided and are not open for reinterpretation in this sprint:

- The benchmark narrative is locked.
- The merged reverse-engineering matrix is locked.
- The narrative compiler architecture is locked.
- N-3 through N-8 built the deterministic narrative support stack.
- N-9 validated the real runtime output and concluded:
  - the deterministic runtime is materially improved
  - but one bounded refinement sprint is still needed before broad frontend re-entry
- N-9B is that refinement sprint.

Your job is to refine the existing deterministic runtime output just enough to satisfy the N-9 findings and make frontend re-entry defensible.

---

## Required inputs

Treat the following as required inputs:

1. Benchmark target lock  
`docs/golden-narrative/AB_GOLD_STANDARD_NARRATIVE_TARGET_LOCK.md`

2. Locked benchmark narrative  
`docs/golden-narrative/AB_GOLD_STANDARD_NARRATIVE_REPORT_CHAT_2_FINAL.md`

3. Runtime validation authority  
`docs/golden-narrative/AB_BENCHMARK_RUNTIME_VALIDATION_N9.md`

4. Final sprint strategy  
`docs/golden-narrative/HealthIQ_Deterministic_Narrative_Sprint_Strategy_FINAL.md`

5. Narrative compiler architecture  
`docs/golden-narrative/HealthIQ_Deterministic_Narrative_Compiler_Architecture_v1.md`

6. Current runtime/compiler files, at minimum:
- `backend/core/analytics/narrative_report_compiler_v1.py`
- `backend/core/contracts/narrative_report_v1.py`
- `backend/core/pipeline/orchestrator.py`
- `backend/core/models/results.py`
- governed asset packs from N-4 to N-7
- the runtime artifact path used in N-9 validation

---

## Core problem this sprint must solve

N-9 concluded that the runtime is no longer structurally weak, but still has a small number of materially important gaps that prevent confident frontend re-entry.

This sprint must close those specific gaps only.

It must not become:
- a fresh compiler architecture sprint
- a broad content-authoring wave
- a frontend sprint
- a benchmark-perfection sprint

---

## Required refinement scope

Use N-9 as the authority for what must be improved.

At minimum, address the specific post-validation weak areas identified there, especially:

### 1. Retail summary / retail-facing interpretation quality
If N-9 found the retail summary weak, empty, gated off by IDL policy, or not fit for broad retail surfacing, refine this runtime path in the smallest safe way.

This may include:
- retail IDL policy alignment
- better bounded assembly from existing governed assets
- more usable summary generation within current authority boundaries

Do not invent ungoverned prose.

### 2. Body overview assembly quality
If N-9 found body overview too thin, generic, or under-assembled relative to available runtime supports, improve it in the smallest safe way.

This may include:
- better use of existing positive-context / reassurance supports
- better expression of “narrow lead issue against calmer background”
- better use of current runtime evidence without inventing new logic casually

### 3. Longitudinal / lifestyle runtime parity
If N-9 found that longitudinal or lifestyle context was only partly visible in the actual runtime case, close the parity gap where appropriate.

This may include:
- making sure the existing N-3 and N-4 supports are actually used when available
- tightening the runtime case path so the validated AB output reflects the intended deterministic stack more faithfully

Do not widen into new longitudinal or lifestyle architecture unless absolutely necessary.

### 4. Any one additional bounded runtime weakness explicitly identified in N-9
Only if N-9 clearly named one further bounded weakness that can be solved inside the current architecture.

Do not go beyond the validated recommendation.

---

## In scope

### 1. Preflight validation re-read
Before changing code, re-read N-9 and restate exactly which runtime gaps are being addressed.

Do not “improve things generally.”
State the bounded target list first.

### 2. Bounded compiler/runtime refinement
Modify the smallest correct part of the runtime/compiler path to close the approved weak areas.

### 3. Tiny governed asset patches only if strictly required
If one of the N-9 refinement goals cannot be achieved without a very small governed asset patch, keep it minimal and justify it explicitly.

Do not reopen N-5/N-6/N-7 as broad content sprints.

### 4. Tests and regression coverage
Add or update tests covering the refined runtime behaviour and ensuring existing sections do not regress.

### 5. Fresh runtime re-check
After implementation, validate the same AB runtime path again and confirm whether the specific N-9 weaknesses are materially improved.

### 6. Short sprint note
Add a concise implementation note documenting:
- what N-9 weaknesses were targeted
- what was changed
- whether the runtime is now ready for frontend re-entry

---

## Out of scope

The following are explicitly out of scope:

- frontend redesign
- broad new governed asset families
- new architecture design
- broad report compiler rewrite
- Gemini / LLM work
- trying to make runtime perfectly match the benchmark prose everywhere
- more than one bounded refinement wave inside this sprint

---

## Design rules

### Rule 1 — N-9 is the authority
Do not refine anything N-9 did not identify as a real weak area.

### Rule 2 — smallest effective change
Use the smallest bounded implementation that materially improves the validated weak area.

### Rule 3 — preserve architecture
Do not reopen the N-2/N-8 architecture unless repo reality forces it.

### Rule 4 — governed assets before handwritten prose
Do not slip ungoverned narrative strings into code to make the output look nicer.

### Rule 5 — refinement, not reinvention
This sprint exists to make the current deterministic runtime acceptable for frontend re-entry, not to chase benchmark perfection.

### Rule 6 — HIGH-risk discipline
Touched-file scope should remain tight and justified if compiler/runtime files are modified.

---

## Expected implementation shape

The expected shape is:

1. restate the exact N-9 runtime weaknesses being addressed
2. implement bounded compiler/runtime refinements
3. add regression tests
4. rerun the AB runtime path
5. document whether frontend re-entry is now justified

This must remain one bounded refinement sprint.

---

## STOP conditions

STOP immediately and report if any of the following are true:

1. the N-9 weaknesses cannot be fixed without broader architecture changes
2. the required refinement scope is materially larger than one bounded sprint
3. new governed asset work is more than tiny patch-level content support
4. the runtime still cannot fairly be judged against the same AB validation path
5. touched-file scope expands materially beyond the intended compiler/runtime refinement layer

If blocked, report:
- the exact blocker
- the affected files
- the smallest safe remediation path
- whether frontend re-entry should remain blocked

---

## Success criteria

This sprint is successful only if:

1. the specific N-9 runtime weaknesses targeted by the sprint are materially improved
2. the runtime remains deterministic and governed
3. no architecture boundary is broken
4. tests prove the refined behaviour
5. the AB runtime can be rechecked on the same path
6. a clear recommendation can be made on frontend re-entry

---

## Deliverables

At finish, the sprint should leave behind:

- bounded compiler/runtime refinements
- regression tests
- a short sprint note explaining:
  - what N-9 weaknesses were addressed
  - what changed
  - whether frontend re-entry is now justified

Report back with:
- files touched
- the exact N-9 weaknesses addressed
- how they were improved
- whether frontend re-entry is now recommended

---

## Evidence requirements

You must show, with exact file paths and grounded runtime evidence:

- which N-9 findings were selected
- what runtime/compiler changes were made
- how the same AB runtime path improved
- why the result is now sufficient, or still not sufficient, for frontend re-entry

Do not produce a vague “polish” pass.
Produce the bounded post-validation refinement the validation explicitly called for.