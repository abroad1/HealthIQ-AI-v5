---
work_id: MED-FRAME-1_signal_family_contextual_frame_architecture
branch: work/MED-FRAME-1-signal-family-contextual-frame-architecture
risk_level: STANDARD
execution_model: TWO_PHASE_START_FINISH
change_type: CONTENT
---

# MED-FRAME-1 — Signal Family and Contextual Medical Frame Architecture

## Purpose

Define the architecture HealthIQ needs to support medically rich, personalised interpretation without collapsing complex biomarker meaning into single flat signals.

This sprint is architecture/design only.

It must establish how HealthIQ represents:

```text
primary biomarker signals
→ multiple medically distinct interpretive frames
→ supporting / contradicting / contextual evidence
→ questionnaire modifiers
→ medication / drug-category modifiers
→ personalised Layer B analysis
→ frontend render-only output
````

This is not a runtime implementation sprint.

## Strategic framing

HealthIQ must not become a flat blood-marker interpretation engine.

The already-agreed product architecture depends on three core input classes:

```text
1. biomarker results
2. health/lifestyle questionnaire context
3. medication / drug-category context
```

These are not optional UX extras.

They are essential structured medical-context inputs that affect interpretation, confidence, explanation, escalation and personalisation.

The current Pass_3/package promotion work must not accidentally create a biomarker-only architecture that later struggles to incorporate questionnaire or medication context.

## Baseline requirement

Start from clean `main`.

Expected prior completed work:

```text
KB-MAP-1 merged
KB-UTIL-2-PILOT merged
KB-UTIL-2-PROMOTE-PILOT merged
KB-UTIL-2-ACTIVATION-READINESS merged
KB-UTIL-2-PROMOTE-WIRE-1 merged or its audit outcome available
KNOWLEDGE_BUS_SOP_v1.3.1 committed
KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL_v1.1 committed
```

Before starting, run and report:

```powershell
git branch --show-current
git status --short
git log --oneline -n 12
git rev-parse HEAD
git rev-parse origin/main
```

STOP if:

```text
- current branch is not main
- local main does not equal origin/main
- working tree is not clean
- governance documents are missing
```

## Governance classification

```yaml
risk_level: STANDARD
change_type: CONTENT
execution_model: TWO_PHASE_START_FINISH
```

Reason:

This sprint produces architecture documentation and governance recommendations only. It must not alter runtime behaviour.

## Required inputs

Read:

```text
docs/governance/KNOWLEDGE_BUS_SOP_v1.3.1.md
docs/governance/KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL_v1.1.md
docs/audit-papers/KB-MAP-1_pass3_to_legacy_package_mapping_and_promotion_plan.md
docs/audit-papers/KB-UTIL-2-PILOT_pass3_to_runtime_artifact_compiler_pilot_report.md
docs/audit-papers/KB-UTIL-2-PROMOTE-WIRE-1_creatinine_runtime_authority_switch_report.md
docs/sprints/launch_core_carry_forward_register.md
knowledge_bus/governance/pass3_legacy_package_mapping_plan_v1.yaml
knowledge_bus/governance/pass3_promotion_decision_register_v1.yaml
```

Also inspect if present:

```text
frontend or backend questionnaire schemas
medication / drug category schemas
analysis input DTOs
InsightGraph / report DTOs
any existing health-context or lifestyle-context models
```

If paths differ, locate and report actual paths.

## Core architectural problem

A biomarker signal may have many medically valid downstream frames.

Example:

```text
signal_creatinine_high
  ├── reduced glomerular filtration
  ├── albuminuric kidney damage
  ├── acute electrolyte risk
  ├── creatinine distortion / muscle mass context
  ├── dehydration / volume context
  ├── medication-associated renal strain
  └── future medically valid frames
```

These frames must not be collapsed into one flat “creatinine high” meaning.

They also must not become uncontrolled duplicate runtime authorities.

The architecture must support:

```text
one signal family
many research frames
clear activation identities
contextual modifiers
safe personalised interpretation
no frontend inference
```

## Required design questions

Answer these explicitly:

```text
1. What is a signal family?
2. What is an interpretive medical frame?
3. How does a frame differ from a signal_id?
4. How does a frame differ from a hypothesis?
5. How should activation_key / spec_id / hypothesis_id relate?
6. How do questionnaire inputs modify a frame?
7. How do medication/drug-category inputs modify a frame?
8. Where should context modifiers live in the architecture?
9. What should be compiled from Pass_3?
10. What should remain Layer B runtime assembly?
11. What must never be inferred by the frontend?
```

## Required model

Propose a model that distinguishes:

```text
signal_id
signal_family_id
primary_biomarker_id
research_spec_id
activation_key
medical_frame_id
hypothesis_id
context_modifier_id
evidence_role
visibility_tier
presentation_safety_status
```

Do not invent runtime implementation details unless needed for architecture clarity.

## Context modifier scope

The architecture must explicitly support at least:

```text
Questionnaire context:
- age
- sex
- symptoms if collected
- health goals if used
- alcohol
- smoking
- exercise
- hydration
- diet
- sleep
- stress
- known conditions
- family history
- supplement use

Medication / drug-category context:
- NSAIDs
- ACE inhibitors / ARBs
- diuretics
- statins
- metformin
- thyroid medication
- steroids
- testosterone / hormones if declared
- nephrotoxic medication categories
- liver-impacting medication categories
```

This sprint must not design every rule. It must define where these rules belong and how they should be governed.

## Required example

Use `signal_creatinine_high` as the worked example.

Show how the architecture would represent:

```text
primary signal:
- creatinine high

frames:
- reduced glomerular filtration
- albuminuric kidney damage
- acute electrolyte risk
- creatinine distortion / muscle mass or supplement context
- medication-associated renal strain

biomarker evidence:
- eGFR
- UACR
- potassium
- cystatin C

questionnaire context:
- hydration
- exercise/muscle mass
- creatine supplement use
- known kidney disease
- diabetes / hypertension if captured

drug-category context:
- NSAIDs
- ACE inhibitors / ARBs
- diuretics
```

The example must show how valid medical context is preserved without creating duplicate co-equal disease claims.

## Required deliverable

Create:

```text
docs/architecture/MED-FRAME-1_signal_family_contextual_frame_architecture.md
```

Optional machine-readable sketch if useful:

```text
knowledge_bus/governance/medical_frame_identity_model_draft_v1.yaml
```

The YAML must be marked draft / non-runtime if created.

## Required report content

The architecture paper must include:

```text
- executive summary
- problem statement
- why flat signal modelling is insufficient
- signal family vs frame vs hypothesis definitions
- identity model
- context modifier model
- questionnaire role
- medication/drug-category role
- Pass_3/package/compiled artefact relationship
- Layer B role
- frontend boundary
- worked creatinine example
- implications for current creatinine promotion work
- recommended next sprint
- risks if ignored
```

## Important architectural principles

The paper must preserve these principles:

```text
- Do not collapse medically distinct frames into one flat signal.
- Do not create uncontrolled duplicate runtime authority.
- Do not let developers resolve medical truth ad hoc.
- Do not let frontend infer clinical meaning.
- Do not treat questionnaire/drug context as UX-only data.
- Do not manually invent context rules without governance.
- Do preserve medically valid edge cases as structured frames or modifiers.
- Do allow thousands of future edge cases without making runtime chaotic.
```

## Out of scope

Do not:

```text
- change code
- change runtime loading
- change package files
- change SignalEvaluator
- change SignalRegistry
- change frontend
- change questionnaire schema
- change drug-category schema
- implement frame evaluation
- implement LLM narrative generation
- activate any package
```

## Required checks

Run:

```powershell
python backend/scripts/validate_day_one_architecture.py
python -m pytest backend/tests/architecture/test_day_one_architecture_guardrails.py -q
```

If these fail, STOP and report.

## Carry-forward register

Update:

```text
docs/sprints/launch_core_carry_forward_register.md
```

only if this sprint creates or reframes future work.

Likely carry-forward:

```text
MED-FRAME-2 — implement medical frame identity/index model
CONTEXT-MOD-1 — questionnaire and drug-category modifier governance
```

Do not mark existing package-promotion work resolved.

## Evidence required from Cursor

Cursor must report:

```text
1. baseline branch/status evidence
2. files inspected
3. current questionnaire/context artefacts found
4. current medication/drug-category artefacts found
5. architecture paper path
6. carry-forward updates if any
7. validation commands run
8. validation results
9. confirmation no code/runtime/frontend/package changes were made
```

## Closure requirements

Before finish, run and report:

```powershell
git branch --show-current
git status --short
git log --oneline -n 5
git diff --name-only
git diff --cached --name-only
git stash list
```

Do not run finish unless:

```text
- current branch matches work/MED-FRAME-1-signal-family-contextual-frame-architecture
- only documentation/governance draft files changed
- no runtime/package/frontend/code files changed
- no ambiguous stash exists
```

## Success criteria

This sprint is complete only if:

```text
1. architecture supports one biomarker signal with many medical frames
2. questionnaire context is included as a structured medical input
3. medication/drug-category context is included as a structured medical input
4. signal/frame/hypothesis/activation identity boundaries are clear
5. creatinine example is worked through
6. frontend remains render-only
7. Pass_3/package promotion architecture remains aligned
8. future implementation sprints are clearly identified
9. no runtime behaviour changes occur
10. validators pass
```

```
```
