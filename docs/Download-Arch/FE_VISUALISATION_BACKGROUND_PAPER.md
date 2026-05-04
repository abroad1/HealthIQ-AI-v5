# FE-VISUALISATION — Background Paper for Team Input

## Purpose of this paper

This paper is intended to support a team decision on what the product should surface to end users in the first implementation of FE-VISUALISATION.

The immediate issue is not just technical delivery. It is product-definition work.

The adopted sprint plan identifies FE-VISUALISATION as:

- Core reusable product visualisation surfaces
- intended to implement the user-facing visualisation and structured-output surfaces necessary for a usable product
- bounded initially to four confirmed components:
  - `BiomarkerChart`
  - `ClusterCard`
  - `InsightPanel`
  - `PipelineStatus`

Before that sprint is implemented, the team should align on what each component is for, who it is for, and what should and should not be surfaced.

If we do not decide this explicitly, implementation will end up making hidden product decisions by default.

## Why this matters now

HealthIQ is no longer just a backend analysis engine.

With recent work completed, the product now has:

- deterministic report/runtime behaviour
- policy-backed handling for primary concern and ranked ambiguity
- clinician-facing contract improvements
- persistence foundations underway
- a growing gap between what the engine can compute and what the user should actually see

That means FE-VISUALISATION is not a UI polish sprint. It is the point where engine output starts turning into a true product surface.

This creates a risk:

- if we expose too much, the product becomes technical, noisy, and hard to trust
- if we expose too little, the product becomes generic and fails to demonstrate the value of the engine
- if we expose the wrong layer, we may show implementation artefacts instead of meaningful biological interpretation

So the core question is:

> What should HealthIQ surface to the user, in what form, and with what level of interpretation?

## The decision we need from the team

The team does not need to decide every final UI detail at this stage.

But the team does need to decide the following for each FE-VISUALISATION component:

1. What is the purpose of the component?
2. Who is the component for?
3. What approved data contract should feed it?
4. What should be visible on the standard user surface?
5. What should be reserved for advanced mode?
6. What should remain internal / debug only?
7. What should the component never imply?

This is the minimum level of agreement needed before implementation.

## The four components in scope

## 1. BiomarkerChart

### What it probably is for

This should likely be the user’s most direct visual anchor for understanding a single marker in context.

In plain terms, it should answer questions such as:

- Where does this value sit relative to the lab range?
- Is it low, normal, or high?
- Is it just outside range or substantially outside range?
- How important is it in the context of this panel?

### What needs deciding

The team should decide whether BiomarkerChart should show only:

- raw value + lab range

or:

- raw value + lab range + interpretation state

or:

- raw value + lab range + importance / contribution to broader patterns

It should also be decided whether future trend/history is conceptually part of this component or a later extension.

### Current recommendation for discussion

For first-release product clarity, BiomarkerChart should probably be:

- simple
- biologically legible
- tied to lab-specific ranges
- not overloaded with backend internals

It should likely not expose raw implementation fields that only make sense to developers.

## 2. ClusterCard

### What it probably is for

This appears to be the natural surface for system-level or pattern-level grouping.

Its purpose is likely to help the user understand:

- which biological systems appear most affected
- which group of markers/signals are contributing to that picture
- why that system matters

### Strategic risk

ClusterCard could become one of two wrong things:

- a useful system-level interpretation block
- or a frontend wrapper around raw internal cluster objects

Those are not the same thing.

### What needs deciding

The team should decide whether ClusterCard is meant to represent:

- a user-facing biological system summary
- an expert-mode pattern summary
- or a translated version of internal cluster computation

This matters because internal cluster IDs, engineering labels, or technical grouping artefacts should not automatically become product copy.

### Current recommendation for discussion

ClusterCard should probably surface:

- system/pattern name
- interpreted state
- top contributing markers/signals
- short explanation of why the cluster matters

It should probably avoid exposing implementation-native labels unless they are translated into product language.

## 3. InsightPanel

### What it probably is for

This is likely the most important component in the whole FE-VISUALISATION set.

InsightPanel is the natural place for:

- primary concern
- ranked ambiguity
- key interpretations
- hypotheses
- confirmatory next-step logic
- user-facing what-this-means synthesis

This is also where the recent ranked-ambiguity work becomes most visible.

### What needs deciding

The team should decide:

- whether this is the main narrative component
- whether it should surface only one lead concern or multiple plausible interpretations
- how much explanatory depth belongs here
- whether confirmatory tests belong here or elsewhere
- whether this should be user mode–dependent

### Current recommendation for discussion

InsightPanel should probably become the main structured interpretation surface.

That means it should not just repeat raw results. It should explain:

- what appears most important
- how certain that interpretation is
- what competing interpretations remain plausible
- what further tests might clarify uncertainty

This is likely where HealthIQ most clearly differentiates itself from a generic report viewer.

## 4. PipelineStatus

### What it probably is for

This component needs the most careful thought.

For internal teams, a pipeline-status view could be very useful. For general users, raw pipeline states are likely to be confusing.

### What needs deciding

The team should decide whether PipelineStatus is:

- genuinely end-user-facing
- advanced-mode only
- or internal/admin/debug only

A standard end user probably does not benefit from raw pipeline internals.

But the user may benefit from translated reassurance such as:

- analysis complete
- data quality checks passed
- some results had limited range context
- interpretation confidence is limited by missing supporting markers

### Current recommendation for discussion

PipelineStatus should probably not be a raw engineering status component on the standard user surface.

If included for end users, it should be translated into a data-quality / confidence-context component, not an implementation-status widget.

## A proposed surface-policy framework

To avoid implementation-led drift, the team may want to classify future FE-VISUALISATION content into three layers:

### 1. Standard user surface
What an ordinary user should see by default.

Criteria:

- easy to understand
- directly useful
- low noise
- aligned to product trust

### 2. Advanced mode
What a more medically literate or optimisation-oriented user may want to explore.

Criteria:

- still product-legible
- more detailed
- acceptable if somewhat more technical
- not required for baseline comprehension

### 3. Internal / debug / admin
What should remain out of the standard product altogether.

Criteria:

- engineering-oriented
- useful for QA, validation, support, or internal review
- not necessary for normal users
- may harm clarity if exposed

This framework may be the simplest way to decide what belongs where.

## Suggested discussion questions for the team

The most useful team input would likely come from answering questions such as:

1. What is the minimum set of information a standard user must see to feel the app is genuinely useful?
2. Which of the four components are truly user-facing, and which are partially internal by nature?
3. What should be visible in default mode versus advanced mode?
4. Do we want to show only biomarker-level information, or also system-level interpretation from day one?
5. How much of the ranked-ambiguity/uncertainty model should be visible to users versus hidden behind clinician/advanced layers?
6. How do we stop technical implementation artefacts leaking onto the product surface?
7. What would make these four components feel like a coherent product rather than four disconnected widgets?

## Current recommendation

Current recommendation for team review:

- BiomarkerChart should be standard user-facing and simple
- ClusterCard should be user-facing, but only in translated biological language
- InsightPanel should be the main structured interpretation surface
- PipelineStatus should either be translated into data-quality/confidence language or be restricted to advanced/internal use

More broadly:

> We should decide FE-VISUALISATION as a product surface policy first, and only then implement the components.

That will reduce drift and make the frontend sprint much more likely to produce a coherent user experience.

## Decision requested from the team

Please provide input on:

1. the purpose of each of the four components
2. what each should show
3. what each should not show
4. which components belong on the default user surface
5. which content should be reserved for advanced mode or internal/debug use

Once that is agreed, FE-VISUALISATION can be implemented against a clear product surface policy rather than inferred assumptions.
