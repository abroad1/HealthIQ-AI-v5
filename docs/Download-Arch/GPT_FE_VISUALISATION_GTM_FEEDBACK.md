# FE-VISUALISATION — GTM and Product-Surface Feedback

## Executive view

The paper asks the right question: FE-VISUALISATION is not a UI sprint, it is product-definition work. That is correct. If the team does not decide explicitly what should be surfaced, implementation will silently make product decisions by default. fileciteturn18file0

My view is that the product surface should be designed around **buyer utility**, not around engine completeness.

HealthIQ does not win because it can compute more.
HealthIQ wins if the surfaced product helps a target user:

- understand what matters faster
- trust the output more
- take a better next step
- justify using HealthIQ again
- justify deploying HealthIQ at scale

That means the product surface must differ by audience.

The same raw engine should support different surface policies for:

1. retail end user
2. clinician / medically literate user
3. enterprise / screening / operations user

The default mistake would be building one generic surface for all three.

---

## Core GTM position this surface must support

HealthIQ should not present as:

- another biomarker dashboard
- another AI report viewer
- another chart-heavy health app

The surface must make visible that HealthIQ is:

- deterministic
- synthesised
- traceable
- scalable
- useful at individual and population level

If FE-VISUALISATION only surfaces biomarker charts and generic interpretation panels, the product will collapse back into the same visual category as weaker competitors.

So the frontend should not be designed merely to "show outputs".
It should be designed to make the following differentiators visible:

1. HealthIQ understands the **panel as a system**, not just isolated markers
2. HealthIQ can state **what matters most now**
3. HealthIQ can show **why** that interpretation is being made
4. HealthIQ can communicate **uncertainty and missingness** without looking weak
5. HealthIQ can support both **single-user interpretation** and **large-cohort screening logic**

---

## The strategic rule for what to surface

A surface should only exist if it does at least one of these jobs:

1. builds trust
2. compresses decision-making
3. differentiates the engine
4. creates a reason to retest or act
5. makes enterprise value legible

If a component only exposes internal computation because it is available, it should not be surfaced.

---

## Audience-by-audience surface policy

## 1. Retail end user

### What this user actually needs

The retail user is not trying to inspect engine internals.
They want answers to five questions:

1. what matters most?
2. how serious is it?
3. what seems connected?
4. what should I do next?
5. should I retest or speak to someone?

### What the default surface should optimise for

- clarity
- reassurance without softness
- prioritisation
- visible intelligence
- low cognitive load

### What this user should see by default

- a ranked summary of the most important findings
- panel-level synthesis before marker-level detail
- clear biological system summaries
- simple biomarker charts for the few markers that matter most
- short next-step logic
- confidence / uncertainty translated into plain language

### What this user should not see by default

- raw cluster IDs
- pipeline internals
- engineering status
- excessive commentary on normal markers
- full ambiguity trees
- every computed object the engine can produce

### Strategic note

For this user, **InsightPanel** matters far more than **BiomarkerChart**.
If the product leads with charts instead of synthesis, it will look like a commodity app.

---

## 2. Clinician / medically literate user

### What this user actually needs

This user is trying to compress review time without surrendering judgement.
They want:

1. what is the leading concern?
2. what supports it?
3. what weakens it?
4. what else is plausible?
5. what would clarify the picture?

### What the surface should optimise for

- rapid synthesis
- traceability
- confidence boundaries
- differential usefulness
- low fluff density

### What this user should see

- prioritised interpretation
- system-level summaries
- lead hypothesis with supporting and conflicting evidence
- plausible alternative explanations where relevant
- confirmatory tests / follow-up logic
- the specific markers driving the interpretation
- confidence or evidence-strength language that is disciplined

### What this user should not see

- consumer wellness copy
- motivational language
- decorative graphs with no decision value
- hidden uncertainty
- overlong explanation of normal markers

### Strategic note

For this audience, the product wins when it behaves like a **pre-diagnostic synthesis layer**, not a chart viewer.

---

## 3. Enterprise / screening / operations user

### What this user actually needs

This audience is not reviewing one person first.
They are trying to understand:

- who needs attention?
- which cohorts matter?
- what patterns are surfacing?
- what is the operational value of screening?

### What the surface should optimise for

- triage
- segmentation
- batch legibility
- population usefulness
- confidence in scale deployment

### What this user should see

- ranked individuals or cohorts by concern level
- major affected systems / phenotype groups
- proportion of population in each concern bucket
- retest / follow-up opportunity flags
- trend movement over time at population level later

### What this user does not need on the main surface

- a beautiful single-patient biomarker chart as the primary object
- raw pipeline states
- verbose narrative per normal marker

### Strategic note

This matters because HealthIQ’s market opportunity is not just individual interpretation. It is also scalable screening and triage. FE-VISUALISATION should not accidentally lock the product into a single-user consumer shape.

---

## Feedback on the four components

## 1. BiomarkerChart

### My view

The paper is right that this should be simple and biologically legible. fileciteturn18file0

But strategically, BiomarkerChart should be a **supporting component**, not the hero component.

If BiomarkerChart becomes the dominant visual object, the product will look like every other blood panel interface.

### Recommendation

For v1, BiomarkerChart should show:

- raw value
- lab range
- position relative to range
- interpreted state
- whether it is a major contributor to a broader pattern

### It should not show in v1

- detailed technical engine metadata
- full history unless it is genuinely useful
- more than the user needs for decision-making

### GTM judgement

Necessary, but not differentiating by itself.
Charts are parity, not moat.

---

## 2. ClusterCard

### My view

This is potentially one of the most commercially important surfaces.

Why?
Because it is the most natural bridge between:

- raw biomarker data
- metabolic reasoning
- visible product differentiation

This is where HealthIQ can prove that it understands systems, not just markers.

### Recommendation

ClusterCard should become a **translated biological system card**, not a wrapper around internal cluster objects.

It should show:

- system / pattern name
- interpreted state
- short explanation of why it matters
- top contributing markers / signals
- what makes this system worth attention now

### It should not show

- engineering-native labels
- raw internal cluster IDs
- implementation language

### GTM judgement

This is one of the strongest places to make the engine feel different from weaker competitors.

---

## 3. InsightPanel

### My view

The paper is correct: this is the most important component. fileciteturn18file0

This is the primary commercial surface.

If InsightPanel is weak, the product is weak.
If InsightPanel is strong, the rest of the surface can be relatively simple.

### Recommendation

InsightPanel should be the main structured interpretation surface and should answer:

- what appears most important
- why that interpretation is leading
- what else remains plausible
- what evidence supports and weakens the leading view
- what next test or action would reduce uncertainty

### Default mode

For standard users:

- one lead concern
- one or two supporting system summaries
- simplified uncertainty language
- concise next-step logic

### Advanced / clinician mode

- ranked ambiguity
- supporting vs conflicting evidence
- confirmatory tests
- more explicit differential framing

### GTM judgement

This is the key component for proving HealthIQ is more than a report explainer.

---

## 4. PipelineStatus

### My view

The paper is right to be cautious. A raw pipeline widget should not be on the standard surface. fileciteturn18file0

### Recommendation

PipelineStatus should be split conceptually into two different things:

#### A. User-facing trust / confidence layer
For end users and clinicians:

- analysis complete
- result quality limitations
- interpretation limited by missing markers
- confidence reduced because of missing context or uncertainty

#### B. Internal / admin pipeline status
For ops, QA, support:

- real pipeline stages
- parsing state
- contract / status internals
- debug information

### GTM judgement

A translated confidence/data-quality component is valuable.
A raw engineering status component is not.

---

## What should be visible on the standard surface

My recommended default surface for first product release is:

1. **InsightPanel** — hero
2. **ClusterCard** — system-level support
3. **BiomarkerChart** — limited to priority markers
4. **Confidence / data quality notice** — translated PipelineStatus

That gives a coherent surface:

- what matters
- what system it belongs to
- which markers drive it
- how confident we are

That is a product.

Anything else risks becoming widget assembly.

---

## What should be advanced mode only

Advanced mode should contain the detail that proves depth without overwhelming the default product.

Recommended advanced-mode items:

- ranked ambiguity / alternative interpretations
- supporting vs conflicting evidence detail
- full marker list
- more extensive biomarker charting
- richer confirmatory test logic
- more detailed confidence explanation

This allows the product to serve more sophisticated users without making the default experience noisy.

---

## What should remain internal / debug only

These should not be surfaced in the user product unless explicitly translated:

- raw pipeline states
- internal object IDs
- implementation-native cluster labels
- parser/debug status
- loader/runtime diagnostics
- any engineering object that does not correspond to a meaningful biological concept

---

## What the product should never imply

This is important.

The surface should never imply:

- formal diagnosis
- certainty beyond the evidence
- that all computed signals are equally important
- that technical completeness equals user usefulness
- that a polished chart is the same as meaningful interpretation

---

## The most important strategic adjustment to the paper

The paper asks what each component is for and who it is for. That is correct. fileciteturn18file0

But I would add one more mandatory decision question for every component:

**What commercial job does this component do?**

For example:

- does it build trust?
- does it demonstrate differentiation?
- does it create retest logic?
- does it help a clinician move faster?
- does it make enterprise-scale deployment more legible?

That question will stop the team surfacing nice-looking but strategically weak objects.

---

## My final recommendation

### Product surface policy

The product should be designed around a **three-layer surfaced-intelligence policy**:

1. **Standard mode**
   - prioritised interpretation
   - system-level summaries
   - limited high-value charts
   - translated confidence/data quality

2. **Advanced / clinician mode**
   - richer ambiguity
   - supporting and conflicting evidence
   - confirmatory tests
   - full biomarker exploration

3. **Internal / ops mode**
   - true pipeline status
   - contract and debug detail
   - QA/support surfaces

### Component priority for v1

If trade-offs are needed, prioritise in this order:

1. InsightPanel
2. ClusterCard
3. BiomarkerChart
4. Translated confidence layer
5. Raw pipeline/admin tooling only later or internal-only

### Core strategic point

HealthIQ should not surface everything the engine knows.
It should surface the smallest set of things that make the engine’s superiority visible to the target buyer.

That means the frontend should make obvious that HealthIQ is:

- more synthesised than chart-first competitors
- more traceable than LLM-first competitors
- more useful to clinicians than wellness apps
- more scalable to enterprise use cases than consumer-only blood dashboards

That is the product-surface standard FE-VISUALISATION should be built against.
