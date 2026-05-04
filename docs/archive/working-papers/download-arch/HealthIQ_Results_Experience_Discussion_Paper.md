# HealthIQ AI — Results Experience Discussion Paper
## Educate first, interpret second: a front-end journey grounded in existing narrative assets

**Status:** Discussion document for team review  
**Purpose:** To align product, UX, and engineering on how HealthIQ AI should present interpretation so users are educated before they are overwhelmed, and so the front end is deliberately powered by the narrative assets already present in the codebase.

---

## 1. Why this paper exists

HealthIQ AI is no longer at the stage where the main question is whether we can analyse a panel.  
The more important question is now:

**How do we present the output of a highly sophisticated metabolic reasoning engine so that a user feels informed, reassured where appropriate, intellectually engaged, and confident that the system genuinely understands the deeper story of their body?**

The current product experience still leans too heavily toward “results presentation” rather than “guided interpretation”.  
That is the wrong frame for HealthIQ AI.

A user opening their results is not just looking at data. They are trying to answer questions such as:

- What is my body actually telling me?
- What is working well?
- What needs attention?
- Why did the system conclude that?
- How do these markers connect?
- What should I do next?

A good front-end experience must therefore do three things repeatedly:

1. **Introduce** what the user is about to see  
2. **Show** them the interpretation or evidence in that frame  
3. **Summarise** what that means for them

This is especially important because HealthIQ AI is surfacing a systems-based model of biology that most users will not have seen before. We cannot simply show sophisticated outputs and assume they will interpret them correctly. We must teach them how to read the experience as they move through it.

---

## 2. The strategic shift we need

The front end should stop behaving like a “lab report plus widgets”.

It should become a **guided interpretation journey** built on a strong deterministic narrative spine.

This means:

- not leading with biomarker tables
- not forcing the user to infer meaning from generic system buckets
- not hiding the reasoning in advanced tabs
- not relying on Gemini to create the core value of the product

Instead, we should:

- orient the user first
- explain how HealthIQ thinks about the body
- show the high-level body story before the data
- reassure the user with what is strong or stable
- explain the lead pattern and why it matters
- show the evidence only after the user understands the frame
- keep the clinician handoff separate from the retail journey

This is not only a UX preference. It is a product strategy decision.  
If HealthIQ is meant to feel like a world-class metabolic reasoning engine, the journey itself must make that reasoning visible.

---

## 3. What we already have in the codebase

The good news is that we do **not** have a major missing-data problem.  
We already have a large number of explanation-bearing assets that could support a much richer journey than the current one.

Below is the practical inventory that matters for the front end.

### 3.1 Primary deterministic explanation assets

#### A. `clinician_report_v1`
**What it is:** The richest deterministic explanation artifact currently produced for user-facing interpretation.  
**Where it is built:**  
- `backend/core/dto/builders.py`  
- compiled via `compile_clinician_report_v1(...)`

**What it contains:**  
- primary concern statement  
- ranked key findings  
- top hypothesis line  
- confidence and missing-data statements  
- runner-up / competing finding explanation  
- confirmatory test rationale  
- full structured clinician summary

**Why it matters:**  
This is currently the strongest text asset in the system for shaping the main user story, yet much of its reasoning depth is either buried or underused in the current front end.

---

#### B. `root_cause_v1`
**What it is:** Structured deterministic root-cause hypotheses with evidence for, evidence against, missing data, and confirmatory tests.  
**Where it lives:** Under the report/clinician compilation path, surfaced through the analysis result payload.

**What it contains:**  
- hypothesis titles  
- short hypothesis summaries  
- evidence for  
- evidence against  
- missing data reasons  
- confirmatory test suggestions with rationale

**Why it matters:**  
This is one of the strongest “Why did we conclude this?” assets in the system. It should be central to the lead interpretation section, not treated as a technical afterthought.

---

#### C. `balanced_systems_v1`
**What it is:** Deterministic “what is working well / what appears stable” summary layer.  
**Where it is built:**  
- compiled in the DTO build stage  
- surfaced to the front end as a dedicated results structure

**What it contains:**  
- introductory line  
- stable system topics  
- evidence lines  
- capacity notes

**Why it matters:**  
This is the basis of a first-class reassurance layer. It should not be buried. It should appear early in the experience to balance the interpretation.

---

#### D. `report_v1`
**What it is:** Intermediate deterministic explanation contract sitting beneath `clinician_report_v1`.  
**Where it lives:**  
- `backend/core/contracts/report_v1.py`  
- nested under `meta.insight_graph.report_v1`

**What it contains:**  
- top findings  
- chain summaries  
- actions / recommendations  
- root cause structures  
- intervention / follow-up annotations

**Why it matters:**  
This includes some of the most useful reasoning assets, particularly the chain-style connection narratives that can help users understand how findings relate to each other.

---

### 3.2 Explainability and reasoning assets

#### E. `meta.explainability_report`
**What it is:** Deterministic explainability and arbitration artifact.  
**Where it is built:**  
- `backend/core/analytics/explainability_builder.py`  
- contract in `backend/core/contracts/explainability_report_v1.py`

**What it contains:**  
- arbitration logic  
- dominance / precedence reasoning  
- causal/explanatory trace structures  
- burden / competition reasoning

**Why it matters:**  
This should not be dumped raw into the UI.  
But it is the strongest source for a user-facing “Why this lead won” / “Why the system prioritised this pattern” layer.

---

#### F. `meta.insight_graph`
**What it is:** The main deterministic analytical artifact produced by the engine.  
**Where it lives:**  
- `backend/core/contracts/insight_graph_v1.py`

**What it contains:**  
- report_v1  
- signal results  
- system burden vectors  
- arbitration results  
- biomarker context  
- cluster/system state  
- optional Layer C feature bundle

**Why it matters:**  
This is the deep reasoning substrate for the whole experience.  
It is not a front-end surface in itself, but it powers the outputs that matter.

---

### 3.3 Educational and explanatory assets

#### G. Retail educational explainers
**What they are:** Long-form educational content for biomarkers and systems.  
**Where they live:**  
- `backend/ssot/retail_explainer_v1/registry.yaml`

**What they contain:**  
- biomarker education blocks  
- system education blocks  
- contribution context statements

**Why they matter:**  
These are already governed and consumer-safe. They are ideal for “learn more” layers, deeper biomarker drawers, and optional educational expansions.

---

#### H. Signal-library explanation fields
**What they are:** Rich explanation-bearing fields within knowledge bus signal packages.  
**Where they live:**  
- `knowledge_bus/packages/**/signal_library.yaml`

**What they contain:**  
Depending on package quality, examples include:
- `explanation.mechanism`
- `explanation.biological_pathway`
- `explanation.interpretation`
- `explanation.implications`
- structured supporting metric roles / rationales

**Why they matter:**  
These are one of the most important underused sources of narrative depth in the system.  
They should not be surfaced raw, but they should feed compiler-mediated front-end copy for system/pattern explanation and “why it matters” text.

---

### 3.4 Optional / future-facing narrative assets

#### I. `insights[]`
**What it is:** Narrative / summary cards produced by the insight synthesis layer.  
**Where it is built:**  
- `backend/core/insights/synthesis.py`

**What it contains:**  
- category summaries  
- interpretation text  
- confidence  
- next steps

**Important note:**  
This layer is currently governed behind runtime policy and may be off or thin depending on environment. It should not be treated as the core narrative spine of the product yet.

---

#### J. `layer_c_features`
**What they are:** Deterministically computed higher-order insight features.  
**Where they live:**  
- within `InsightGraphV1` contract structures  
- examples include metabolic age, heart resilience, inflammation burden, fatigue feature, detox feature

**Why they matter:**  
These are potentially very powerful “wow” assets, but they should only be made prominent if they are:
- robust
- explainable
- clinically defendable
- clearly integrated into the wider reasoning story

---

## 4. The current front-end problem

The current product tends to surface interpretation in a way that feels like a collection of sections rather than a coherent reasoning journey.

The practical front-end problems are:

- the user is not properly taught how to read the output
- the product still reveals too much complexity too early
- what is working well is not given enough importance
- why the lead pattern won is not surfaced clearly enough
- phenotype/system names are too generic or weak
- the evidence layer appears before the reasoning is fully understood
- educational assets are hidden too deep
- the richest deterministic assets are not mapped clearly enough to the most important UX moments

This is a hierarchy problem more than a pure content problem.

---

## 5. The experience principle we should adopt

For every major front-end section, we should follow this structure:

### 1. Introduce
Briefly explain what this section is and how to read it.

### 2. Show
Present the user’s specific interpretation, system, or evidence.

### 3. Summarise
Tell the user what they should take away from it.

This should be repeated throughout the page so the user is guided rather than overwhelmed.

---

## 6. Proposed results journey

What follows is the concrete front-end journey I recommend.

---

### Section 1 — How to read your body map
**Purpose:** Educate the user before interpretation begins.

**What this section should do:**  
Introduce the core concept that HealthIQ is grouping markers into systems and patterns, because the body is best understood as interacting systems rather than isolated numbers.

**Sample content direction:**  
- your blood panel is more than a list of numbers  
- each marker offers clues about how different systems are functioning  
- HealthIQ groups these markers into patterns so you can understand the body as a whole  
- first we will show the big picture, then the main findings, then the underlying evidence

**Primary assets:**  
This is mainly a product-authored explanatory block, but it should be written to align with:
- phenotype model
- system grouping logic
- deterministic engine framing

**Front-end requirement:**  
Short, calm, educational, confidence-building. No heavy data here.

---

### Section 2 — Your body overview
**Purpose:** Give the user an immediate whole-body orientation.

**What this section should answer:**  
- what the main areas of strain are  
- what looks stable  
- what the primary driver system is  
- whether the lead concern was obvious or a close call

**Primary assets to surface:**  
- `arbitration_result`
- `system_capacity_scores`
- primary concern fields from `clinician_report_v1.sections.page1`
- selected top-level report metadata

**Why this section matters:**  
This is the first place the user should feel that the product understands their body as a whole.

**What not to surface here:**  
- long biomarker lists
- raw tables
- dense technical explanation

---

### Section 3 — What’s working well
**Purpose:** Anchor the user in strengths before discussing weaknesses.

**What this section should answer:**  
- which systems appear resilient or stable
- what evidence supports that
- why that matters

**Primary assets to surface:**  
- `balanced_systems_v1`
- selected burden/capacity evidence
- low-strain deterministic system facts
- optional system explainers where useful

**Why this matters:**  
A product that only shows problems feels alarming.  
A product that can show strengths as well as strain feels more intelligent and trustworthy.

**Important rule:**  
Only present reassuring interpretation where deterministic evidence genuinely supports it.

---

### Section 4 — Primary finding and why
**Purpose:** Deliver the lead interpretation with depth and reasoning.

**What this section should answer:**  
- what the lead pattern is
- what it means
- why the system selected it
- what supports it
- what complicates it

**Primary assets to surface:**  
- `clinician_report_v1.sections.page1.primary_concern`
- `top_hypothesis_line`
- `chains[]`
- `root_cause_v1`
- evidence-for / evidence-against / missing-data / confirmatory-tests
- selected compiler-mediated signal explanation snippets where available

**Why this matters:**  
This is one of the highest-value sections in the whole experience.

**What the user should feel:**  
“I understand not just what the lead pattern is, but why the engine thinks it matters.”

---

### Section 5 — Key body-level insights
**Purpose:** Create the “wow” moment without becoming gimmicky.

**What this section should answer:**  
- what broader derived insights the engine has found
- what those mean about the user’s body overall

**Primary assets to surface:**  
- `layer_c_features`
- selected deterministic higher-order feature summaries
- only those that are robust enough for user-facing display

**Caution:**  
These should not dominate the experience unless their computation and explanation are exceptionally strong.  
They should support the body story, not replace it.

---

### Section 6 — Why this lead won / uncertainty
**Purpose:** Build trust through transparency.

**What this section should answer:**  
- what nearly became the lead
- why it did not
- what data is missing
- how certain the engine is
- what would change the conclusion

**Primary assets to surface:**  
- `runner_up_topic_line`
- `runner_up_why_not_lead_line`
- `confidence_and_missing_data`
- `data_quality.confidence_caveat`
- selected explainability/arbitration outputs, but compiler-shaped for users
- missing-data logic from root cause / report structures

**Why this matters:**  
This is the trust layer.  
It should feel like the product is intellectually honest, not defensive or vague.

---

### Section 7 — Patterns across your body
**Purpose:** Show the structured interpretation layer beneath the lead finding.

**What this section should do:**  
Surface phenotype/pattern-level outputs in a way that is medically meaningful and understandable.

**Primary assets to surface:**  
- governed phenotype outputs
- `knowledge_bus/phenotypes/phenotype_map_v1.yaml` aligned pattern logic
- system/cluster outputs
- system explainers
- supporting biomarker summaries

**Naming principle:**  
Do not use generic labels like:
- Metabolic Health
- Organ Health
- Hormonal Health

Use:
- clinical display name
- plain-English subtitle
- short why-it-matters line

Example:
**Early Insulin Resistance Pattern**  
Early blood sugar regulation strain  
This pattern looks for signs that your body may be needing more insulin effort to manage glucose effectively.

---

### Section 8 — Marker-level evidence
**Purpose:** Give the user the data after they understand the frame.

**What this section should answer:**  
- what the biomarker is
- what the value means relative to the range
- how it contributes to the wider pattern
- how to learn more

**Primary assets to surface:**  
- `biomarkers[]`
- `contribution_context`
- `biomarker_educational_explainer`
- reference range data
- scores / interpretations

**Why this matters:**  
This is the evidence vault, but it should come after the reasoning journey has already been established.

---

### Section 9 — What to do next
**Purpose:** Move the user from understanding to action.

**What this section should answer:**  
- what confirmatory tests might help
- what should be discussed with a clinician
- what monitoring / next steps matter
- what the priority order is

**Primary assets to surface:**  
- `confirmatory_tests[]`
- `actions`
- `next_steps[]`
- selected intervention or follow-up fields from report structures

**Important note:**  
This should feel like a prioritised roadmap, not generic self-help.

---

### Section 10 — Clinician summary
**Purpose:** Keep the professional handoff clearly separated from the retail interpretation journey.

**Primary assets to surface:**  
- full `ClinicianReportV1`

**Why this should remain separate:**  
The retail experience and clinician handoff serve different purposes.  
We should not try to live-transform the page into “professional mode”.  
A distinct lower-page / exportable clinician section is stronger and cleaner.

---

## 7. Recommended data-asset-to-UX mapping

| UX section | Main purpose | Primary text assets | Supporting assets | Notes |
|---|---|---|---|---|
| How to read your body map | educate before interpretation | product-authored boilerplate aligned to phenotype/system model | panel completeness / counts if helpful | no heavy data |
| Your body overview | body-level orientation | `primary_concern`, selected page1 summary fields | `arbitration_result`, `system_capacity_scores` | calm, concise |
| What’s working well | reassurance | `balanced_systems_v1` | low-burden evidence, capacity notes | first-class |
| Primary finding and why | explain the lead | `top_hypothesis_line`, `chains[]`, `root_cause_v1` | selected signal explanation snippets, confirmatory test rationale | key section |
| Key body-level insights | create wow moments | `layer_c_features` summaries | selected derived metrics | use cautiously |
| Why this lead won / uncertainty | build trust | `runner_up_topic_line`, `runner_up_why_not_lead_line`, `confidence_and_missing_data` | explainability/arbitration outputs, missing-data logic | must be user-readable |
| Patterns across your body | pattern-level structure | phenotype display names, subtitles, why-it-matters explainers | clusters, system explainers | rename strongly |
| Marker-level evidence | evidence depth | `biomarkers[]`, contribution context | retail explainers | deeper layer |
| What to do next | action | confirmatory test rationale, actions, next_steps | follow-up logic | prioritised |
| Clinician summary | professional handoff | full `ClinicianReportV1` | optional export metadata | separate section |

---

## 8. How we should use signal-library explanation assets

This is important.

The signal packages in:
- `knowledge_bus/packages/**/signal_library.yaml`

contain some of the richest explanation-bearing content in the system.

However, I do **not** recommend surfacing these raw strings directly as front-end copy.

Instead, I recommend:

### Use them as governed source material for compiler-mediated copy

For example:
- use `explanation.mechanism` to help generate a short “why this matters biologically” statement
- use `explanation.interpretation` to support pattern-level explanatory text
- use `supporting_metrics` roles/rationales to enrich evidence summaries
- use `explanation.implications` to support next-step or significance framing

This gives you:
- consistency
- tone control
- versionability
- freedom to shape the front end around user comprehension rather than YAML structure

---

## 9. Deterministic vs Gemini recommendation

My recommendation is clear:

### Deterministic assets should form the narrative spine
The main journey should be powered by:
- `clinician_report_v1`
- `root_cause_v1`
- `balanced_systems_v1`
- phenotype/pattern outputs
- explainability-derived rationales
- deterministic educational explainers
- compiler-mediated signal explanation excerpts

### Gemini should remain supplementary
Use Gemini later for:
- smoothing category summaries
- improving connective tissue between sections
- optional polished summary layers

But Gemini should **not** be the authority for:
- clinical reasoning
- lead interpretation
- confidence
- prioritisation
- confirmatory tests
- core body story

The wow factor should come from governed truth, not from stylistic flourish.

---

## 10. Naming recommendation for phenotype/pattern presentation

The current broad group names are too weak.

You already have governed phenotype ids such as:
- `ph_metabolic_early_ir_v1`
- `ph_vascular_hcy_inflammation_v1`
- `ph_renal_stress_v1`
- etc.

The front end should display these using a three-part naming model:

1. **Clinical display name**  
2. **Plain-English subtitle**  
3. **Why-it-matters explainer**

Example:

**Early Insulin Resistance Pattern**  
Early blood sugar regulation strain  
This pattern looks for signs that your body may be needing more insulin effort to manage glucose effectively.

This is much stronger than:
- Metabolic Health
- Cardiovascular Health
- Organ Health

---

## 11. Immediate practical conclusions

If the team asks, “What should we do next?” my answer is:

### Do not start with more abstract ideation
We now have enough understanding.

### We should move into concrete architecture work on three fronts

#### A. Results page section specification
Define for each section:
- purpose
- intro message
- show layer
- summary layer
- exact data assets
- expanded / hidden content

#### B. Pattern naming framework
For each current governed phenotype:
- internal id
- clinical display name
- plain-English subtitle
- why-it-matters explainer
- likely supporting markers/signals

#### C. Deterministic narrative spine specification
Define exactly which existing assets drive:
- body overview
- reassurance layer
- lead interpretation
- why / uncertainty
- action layer

That should happen before any major front-end redesign build.

---

## 12. Final recommendation to the team

HealthIQ should now move from “results interface” thinking to **guided reasoning journey** thinking.

The most important principles are:

- educate before showing
- reassure before alarming
- explain before drowning the user in evidence
- use strong pattern names, not generic health buckets
- surface deterministic reasoning assets more boldly
- use signal-library explanation prose through compilers, not raw
- make balanced systems first-class
- add a visible “why this lead won” layer
- let Gemini polish later, not define the product now

If we do this well, HealthIQ will stop feeling like a sophisticated report and start feeling like what it is supposed to be:

**a clinically grounded, systems-level interpretation experience that helps a user understand their body in a way they have likely never experienced before.**
