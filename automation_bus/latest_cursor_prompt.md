---
work_id: N-4
branch: feature/n-4-lifestyle-interpretation-bridge-assets
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# N-4 — Lifestyle interpretation bridge assets

## Objective

Create the first governed deterministic lifestyle-to-interpretation bridge assets so HealthIQ can use lifestyle context in medically disciplined narrative interpretation rather than treating questionnaire data as passive intake only.

This is a HIGH-risk sprint because it is expected to touch governed interpretation logic and may touch backend analytical infrastructure.

This sprint is not a frontend sprint.
Do not redesign the results page.
Do not introduce Gemini or any other LLM dependency.
Do not widen into full narrative compilation.

The purpose of N-4 is to build the governed bridge layer between structured lifestyle inputs and interpretation outputs for the first benchmark-critical contexts:
- alcohol → homocysteine / macrocytosis / one-carbon context
- hydration / physical work pattern → renal interpretation context
- weight loss / fasting pattern → glycaemic improvement context

---

## Strategic context already settled

The following are already decided and are not open for reinterpretation in this sprint:

- The benchmark narrative is locked.
- The merged reverse-engineering matrix is locked.
- The narrative compiler architecture is locked.
- N-3 has now closed the longitudinal raw-value contract gap.
- One of the major remaining deterministic gaps is that HealthIQ captures lifestyle context but does not yet join it cleanly into interpretation.
- N-4 exists to create governed lifestyle-to-interpretation bridge assets before later narrative compiler work.

Your job is to implement the minimum clean governed bridge layer that makes these three classes of contextual interpretation deterministically supportable.

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

5. Relevant current runtime and authority files, at minimum:
- `backend/ssot/questionnaire.json`
- `backend/ssot/lifestyle_registry.yaml`
- `backend/core/pipeline/questionnaire_mapper.py`
- `backend/core/analytics/lifestyle_modifier_engine.py`
- `knowledge_bus/root_cause/hypotheses/hcy_hypotheses_v1.yaml`
- relevant macrocytosis / renal / glycaemic packages and hypotheses
- any intervention / confirmatory / report-support assets you determine are relevant

---

## Core problem this sprint must solve

HealthIQ already captures lifestyle inputs such as alcohol intake, fasting pattern, fluid intake, and work pattern.

But the current deterministic system does not yet translate those inputs into governed interpretation context for the benchmark narrative.

This sprint must create a medically disciplined bridge layer so that lifestyle context can:
- support interpretation
- shape uncertainty and plausibility
- influence contextual phrasing later
without becoming hand-wavy or speculative.

---

## Required outcome

Deliver a bounded HIGH-risk implementation that:

1. defines and implements governed lifestyle-to-interpretation bridge assets for the three priority domains
2. keeps lifestyle context as contextual interpretation support, not diagnosis inflation
3. preserves deterministic behaviour and traceability
4. makes later narrative compiler work able to consume these joins cleanly
5. adds or updates tests proving the bridges behave as intended

---

## In scope

### 1. Preflight verification
Before modifying code or governed assets, verify and cite:

- what lifestyle fields currently exist in SSOT and are relevant to the benchmark case
- how questionnaire responses are currently mapped into runtime lifestyle structures
- what the current `lifestyle_modifier_engine.py` actually does today
- whether existing root-cause or signal assets already partially support any of the intended joins
- what current deterministic path, if any, could already consume lifestyle context

You must confirm the exact current gap before patching it.

### 2. Alcohol → methylation / macrocytosis context
Build the first governed lifestyle interpretation bridge for alcohol intake.

The target is not:
- “alcohol causes the result”
The target is:
- alcohol is a plausible contextual modifier or contributor for interpreting homocysteine / macrocytosis / one-carbon pathway friction when the pattern is otherwise coherent

This bridge must remain bounded and medically disciplined.

### 3. Hydration / physical work → renal context
Build a governed deterministic bridge allowing hydration level and manual/physical work context to inform renal interpretation context where appropriate.

The target is not:
- “renal issue explained away”
The target is:
- hydration / work context can shape the interpretation of reassuring or borderline renal markers in a deterministic, bounded way

### 4. Weight loss / fasting → glycaemic improvement context
Build a governed deterministic bridge allowing reported weight loss and fasting pattern to support interpretation of favourable glycaemic direction-of-travel where appropriate.

The target is not:
- broad metabolic praise
The target is:
- contextual support for interpreting a more favourable glycaemic trend coherently

### 5. Governed asset placement
Implement these bridges in the correct governed location(s).

You must determine, repo-groundedly, whether the right home is:
- lifestyle registry extension
- root-cause hypothesis extension
- new bridge asset(s)
- another bounded governed structure

Do not scatter the logic casually across multiple layers without authority clarity.

### 6. Runtime consumption path
Ensure the new bridge assets are available to later deterministic narrative compilation.

This sprint does not need to produce the final prose narrative layer, but it must make the contextual bridge outputs accessible in a clean deterministic way.

### 7. Tests and regression coverage
Add or update tests covering at minimum:
- alcohol context bridge behaviour
- hydration/physical-work renal context bridge behaviour
- weight-loss/fasting glycaemic context bridge behaviour
- no speculative output when required context is absent
- no breakage of existing logic

### 8. Concise sprint note
Add a short implementation note documenting:
- what bridge assets were introduced
- what runtime path now exposes them
- what later sprint this unblocks

---

## Out of scope

The following are explicitly out of scope:

- full narrative prose compiler work
- frontend changes
- broad report compiler redesign
- new longitudinal contract work beyond consuming N-3 outputs where needed
- new IDL display-layer design
- broad phenotype/IDL expansion beyond what is strictly required for these bridge assets
- Gemini / LLM work

---

## Design rules

### Rule 1 — contextual, not causal overreach
Lifestyle context must support interpretation carefully.
Do not let the system make stronger causal claims than the evidence supports.

### Rule 2 — governed asset first
Do not bury interpretation joins in ad hoc code branches if they belong in a governed asset layer.

### Rule 3 — no silent narrative logic
The bridge outputs must be inspectable and traceable.
Do not create opaque “magic” lifestyle interpretation behaviour.

### Rule 4 — benchmark relevance first
Focus on the three priority joins identified by the benchmark and merged matrix.
Do not widen into a full lifestyle-intelligence platform.

### Rule 5 — HIGH-risk discipline
Touched-file scope should remain tight.
Any changes to:
- `backend/core/analytics/`
- `backend/core/pipeline/`
- rooted hypothesis/KB assets
must be justified and bounded.

### Rule 6 — no diagnosis inflation
These bridges are contextual modifiers and interpretation supports.
They must not become diagnostic declarations.

---

## Expected implementation shape

The expected shape is:

1. inspect current lifestyle intake and modifier paths
2. verify the missing deterministic joins
3. implement governed bridge assets in the correct authority layer
4. expose them to later compiler consumption
5. add regression tests
6. document the bridges briefly

This must remain a targeted enabling sprint.

---

## STOP conditions

STOP immediately and report if any of the following are true:

1. the relevant lifestyle fields are not actually available in structured runtime form
2. the correct solution would require a much wider redesign of questionnaire mapping
3. no clean governed asset location exists and architectural adjudication is needed first
4. the intended joins would force speculative or unsafe interpretation behaviour
5. touched-file scope expands materially beyond the expected lifestyle / bridge / hypothesis path
6. repo reality contradicts the N-2 architecture assumptions or merged matrix support diagnosis

If blocked, report:
- the exact blocker
- the affected files
- the smallest safe remediation path
- whether N-4 should be split before continuing

---

## Success criteria

This sprint is successful only if:

1. the three priority lifestyle interpretation bridges now exist deterministically
2. they are governed and traceable
3. they can be consumed by later narrative compiler work
4. they do not overclaim causality
5. tests prove the behaviour
6. the sprint remains bounded and does not become a broader lifestyle engine rewrite

---

## Deliverables

At finish, the sprint should leave behind:

- bounded code and/or governed asset changes implementing the bridge layer
- regression tests
- a short sprint note explaining:
  - what was added
  - what runtime path now exposes it
  - what future sprint it unblocks

Report back with:
- files touched
- bridge-asset design chosen
- how each of the three benchmark joins is now supported
- any remaining limitation later sprints must respect

---

## Evidence requirements

You must show, with exact file paths and grounded repo evidence:

- what lifestyle fields were used
- what new bridge assets or logic were introduced
- where they now live
- how runtime can consume them later
- how tests prove the change

Do not claim success merely because a few new rules exist.
Show that benchmark-critical lifestyle context is now deterministically supportable.