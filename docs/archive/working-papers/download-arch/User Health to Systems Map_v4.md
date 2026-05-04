# HealthIQ AI — Customer-Facing Health Scores Mapping Matrix v0.4

## Purpose

This document defines the strategic background for HealthIQ’s customer-facing health score model.

It is not a medical ontology and it is not a direct implementation spec.
Its purpose is to keep architecture, research, and implementation work aligned while the repo is assessed against a new translation layer.

The central question is:

How do we translate HealthIQ’s deterministic phenotype/system engine into a small number of customer-facing health scores that feel intuitive, reassuring, and actionable without weakening medical credibility?

---

## Why this work exists

HealthIQ’s internal engine is strong because it models real biological pathways, syndrome-states, and cross-system interpretation constructs.

However, many of those constructs are too medical, too machine-shaped, or too indirect to work as top-level consumer UX labels.

Example:

- Internal phenotype: `ph_iron_deficiency_inflammation_v1`
- Strong internal meaning: syndrome-state in the iron-to-oxygen pathway
- Weak consumer UX label: too technical, too indirect

Users do not primarily think in phenotype language.
They think in terms of:

- what part of the body is doing well
- what part of the body is under strain
- what this may explain
- what this could lead to over time
- what they should do next

So the customer-facing layer must act as a translation layer above the engine, not a replacement for it.

---

## Core architectural rule

HealthIQ must operate with three distinct naming layers:

1. **Consumer label**  
   Calm, simple, emotionally legible dashboard language

2. **Clinical handout label**  
   Medically grounded language suitable for clinician-facing output

3. **Internal engine mapping**  
   Phenotypes, systems, signal groups, clusters, and governed interpretation assets

These three layers must not be conflated.

### Non-negotiable

Consumer labels must never replace the clinical labels in the clinician PDF/handout.

The safe structure is:

- Dashboard / customer UI → **Consumer label**
- Clinician handout / PDF → **Clinical label**
- Engine / mapping docs → **Internal phenotype/system logic**

---

## Strategic framing

This score model is not meant to flatten HealthIQ into a traffic-light dashboard.

Its role is to create a more intuitive first-screen experience while preserving the deterministic moat underneath.

The health scores should help the user answer:

- where do I look strong?
- where am I under strain?
- how confident is the platform in that judgement?
- what may this mean if it persists?
- what should I do next?

The health scores should not pretend to be diagnoses.

---

## Product framing recommendation

Each customer-facing domain should be shown as:

- a score out of 100
- a confidence level
- a short explainer line
- an expandable explanation showing:
  - why the score is what it is
  - which biomarkers and patterns contributed
  - what would improve confidence
  - what this may mean over time
  - what to do next

These are not diagnoses.
They are top-level health-domain scores powered by deterministic phenotype logic.

---

## Domain / pathway / state / outcome rule

Each visible score should keep these layers distinct internally:

- **Pathway domain** — the biological system being modelled
- **Interpretation construct** — the syndrome-state / risk frame / organ-pattern detected by the engine
- **User-facing score** — the simplified customer label
- **Outcome translation** — what this may mean over time if the pattern persists

### Example: Blood, iron & oxygen

- Pathway domain: iron availability → erythropoiesis → oxygen transport
- Interpretation construct: functional iron deficiency / iron-restricted erythropoiesis / anaemia-adjacent state
- User-facing score: Blood, iron & oxygen
- Outcome translation: this may affect stamina, recovery, concentration, or longer-term anaemia risk if it persists

This distinction prevents shallow wellness language from replacing biological truth.

---

## Score architecture rule

The preferred structure is:

1. **Top-level customer-facing health domain**
2. **Contributing systems or subdomains** where justified
3. **Underlying deterministic phenotype / pathway constructs**
4. **Biomarkers and confidence logic**

### Example

Instead of:

- Heart = 80
- Vascular = 60

Use:

- Cardiovascular health = 75

And beneath it show contributing systems such as:

- Lipid transport
- Vascular strain / inflammation
- Homocysteine-related vascular risk

This is preferable because routine bloods usually support vascular and cardiometabolic interpretation more directly than narrow cardiac-function scoring.

---

## Splitting rule

A top-level health category should only be split into visible sub-scores if the proposed sub-scores are:

- biologically distinct
- understandable to a user
- supported by real deterministic logic
- not heavily overlapping

### Good candidates for hierarchical sub-scores

- Cardiovascular health
  - lipid transport
  - vascular strain / inflammation
  - homocysteine-related vascular risk

- Blood, iron & oxygen
  - iron availability
  - red-cell production
  - oxygen-carrying support

- Thyroid & energy regulation
  - thyroid axis
  - thyroid-linked metabolic effects

- Kidney function
  - filtration
  - renal strain
  - hydration-context, if governable and robust

### Poor candidates for early splitting

- Silent inflammation
- Hormone balance
- Liver health

These are currently at higher risk of becoming fuzzy or weakly supported if broken into visible sub-scores too early.

---

## Agreed launch strategy — Strategy A

### Launch-core six domains

These are the agreed first-wave customer-facing domains:

1. **Cardiovascular health**
2. **Blood sugar control**
3. **Liver health**
4. **Blood, iron & oxygen**
5. **Thyroid & energy regulation**
6. **Kidney function**

### Second-wave only for now

These remain outside the launch-core set unless repo-grounded evidence strongly justifies promoting them:

7. **Silent inflammation**
8. **Hormone balance**

The burden of proof is now on implementation research to show whether the six launch-core domains are genuinely supported by the codebase today, and where gaps still exist.

---

## Final draft 8-domain translation table

| Consumer label | Short explainer | Clinical handout label | Internal phenotype / system mapping | Likely launch readiness |
|---|---|---|---|---|
| **Cardiovascular health** | Heart, arteries, and circulation | **Cardiometabolic / Vascular Risk Status** | Lipid transport dysfunction; vascular inflammation burden; homocysteine / endothelial strain; atherogenic transport patterns | **Strong** |
| **Blood sugar control** | Sugar and insulin balance | **Glycaemic Regulation / Insulin Resistance Status** | Insulin resistance phenotype; glycaemic dysregulation patterns; triglyceride / HDL metabolic coupling | **Strong** |
| **Liver health** | Liver strain and processing load | **Hepatic-Metabolic Strain Status** | Hepatic stress patterns; fatty-liver-adjacent patterns; metabolic overload constructs | **Moderate to strong** |
| **Silent inflammation** | Hidden internal body stress | **Systemic Inflammatory Activity** | Systemic inflammation patterns; vascular inflammation phenotype; chronic inflammatory burden states | **Moderate** |
| **Blood, iron & oxygen** | Oxygen delivery and energy support | **Iron-Erythropoietic / Oxygen-Carrying Status** | Iron deficiency / inflammation; anaemia-adjacent states; one-carbon / macrocytosis patterns where relevant | **Strong** |
| **Hormone balance** | Sex-hormone balance and function | **Gonadal / Sex-Hormone Balance** | Sex hormone imbalance patterns; gonadal-axis disturbance; LH / FSH / testosterone / oestrogen related patterns | **Moderate** |
| **Thyroid & energy regulation** | Thyroid-driven energy balance | **Thyroid Axis Status** | Thyroid-axis disturbance; thyroid-linked lipid disturbance; low FT4 / FT3 / TSH-context patterns | **Moderate to strong** |
| **Kidney function** | Filtration and fluid balance | **Renal Filtration / Renal Strain Status** | Renal strain constructs; eGFR / creatinine / urea patterns; hydration-context renal interpretation where governed | **Moderate** |

---

## Research-grounded medical review conclusion

External medical review judged the following as the strongest launch-core domains because they are the most clearly anchored to real current or near-term governed systems:

- Cardiovascular health
- Blood sugar control
- Blood, iron & oxygen
- Thyroid & energy regulation
- Kidney function

It also judged:

- Liver health = credible, but wording must stay clearly blood-based and strain-oriented
- Silent inflammation = plausible but at risk of fuzziness
- Hormone balance = plausible but at risk of weak support/confidence if launched too early

The six launch-core domains remain the correct Strategy A implementation target.

---

## Candidate current-fit assessment

This is the current strategic judgement before repo-grounded implementation research.

| Customer-facing score | Likely current readiness | Comment |
|---|---|---|
| Cardiovascular health | Strong | Best used hierarchically rather than as a flat “heart” score |
| Blood sugar control | Strong | Clean current fit if insulin-resistance logic is mature |
| Liver health | Moderate to strong | Strong if wording remains careful and non-diagnostic |
| Blood, iron & oxygen | Strong | One of the clearest pathway-to-user translations |
| Thyroid & energy regulation | Moderate to strong | Good user-facing label if the underlying model is coherent |
| Kidney function | Moderate | Needs careful handling of mild abnormalities and confidence |
| Silent inflammation | Moderate | Valuable but at risk of becoming too broad |
| Hormone balance | Moderate | Confidence handling and subgroup logic are critical |

This suggests the launch-core six are the right focus for implementation research.

---

## Draft score interpretation framework

This is a UX proposal only.

| Score band | Label | Meaning |
|---|---|---|
| 80–100 | Strong | This area looks reassuring and relatively well supported |
| 65–79 | Stable | Broadly okay, but not necessarily perfect |
| 45–64 | Watch | Some signals suggest mild or emerging strain |
| 0–44 | Needs attention | This area looks materially less robust and deserves review |

These thresholds are placeholders.
Final thresholds should be determined by deterministic scoring logic and clinical review.

---

## Draft confidence framework

Each customer-facing score should also display confidence, for example:

- High confidence
- Good confidence
- Moderate confidence
- Limited confidence

Confidence should be driven by:

- number of relevant markers present
- consistency of signal direction
- absence of contradiction
- support from multiple systems
- whether key confirming markers are missing

Expanded view should explain:

- why confidence is what it is
- what additional markers would strengthen it

---

## Proposed expanded card structure

Each health score card could expand to show:

1. What this score means
2. Why your score looks like this
3. What contributed most
4. Contributing systems
5. How confident we are
6. What this may mean over time
7. What you can do next

The objective is to make the first screen intuitive without severing the score from the underlying engine truth.

---

## Many-to-many mapping principle

This translation layer is not expected to be one-to-one.

That is normal and acceptable.

### One customer-facing score may be powered by multiple phenotypes
Example:
- Cardiovascular health may draw from lipid transport dysfunction, vascular inflammation, and homocysteine-related endothelial strain.

### One phenotype may feed multiple customer-facing scores
Example:
- an iron-related syndrome-state may influence:
  - Blood, iron & oxygen
  - Silent inflammation
  - broader recovery or nutrient context later

The customer layer exists to simplify interpretation, not to mirror the engine exactly.

---

## What implementation research must now answer

This background document does not assume the launch-core six are fully implemented already.

The next task is to assess the repo-grounded reality for each of the six launch-core domains.

For each domain, implementation research must determine:

1. Which existing phenotypes, systems, signal groups, clusters, or governed assets already map to it
2. Which parts of that mapping are already strong in the codebase today
3. Which parts are partial, missing, or too weak to support launch
4. Whether the domain is:
   - launch-ready now
   - launchable with light assembly work
   - launchable only with medium backend/governed work
5. What confidence inputs already exist in the current system
6. What score-band interpretation could plausibly be derived from current logic
7. What the expanded card could truthfully say today without inventing unsupported claims
8. What exact codebase paths would likely need to change to implement this domain as a real product score

---

## Key product benefits of this model

If implemented well, this model should:

- make the first screen far more reassuring and understandable
- preserve HealthIQ’s deterministic moat instead of flattening it into traffic lights
- let users see where they are strong, where they are strained, and where confidence is high or low
- link deep phenotype/pathway logic to real-world health concerns people understand
- reduce the sense that HealthIQ is “just another biomarker table”
- make it easier to explain the body as a set of connected systems rather than isolated biomarker abnormalities

---

## Key risks to avoid

1. Over-medical naming  
If the labels are too close to phenotype language, the UX will remain too abstract.

2. Over-vague naming  
If the labels become too broad, the system loses explanatory power.

3. Overstated disease claims  
Top-layer scores must suggest risk direction or pathway strain without implying diagnosis.

4. Fake scoring  
No score should appear unless it is genuinely supported by deterministic logic and confidence logic.

5. Over-breadth too early  
A smaller number of strong, legible health scores may beat a larger but weaker set.

6. Unsupported sub-scores  
Do not show visible sub-scores unless they are genuinely distinct, biologically supportable, and not merely cosmetic splits.

7. Mixing pathway, state, and outcome  
Do not let the user-facing layer blur together the biological pathway, the detected interpretation construct, and the eventual health consequence.

8. Consumer labels leaking into clinician outputs  
Consumer labels must remain a dashboard/patient-experience layer, not the language of the clinical handout.

9. Premature promotion of second-wave domains  
Do not elevate Silent inflammation or Hormone balance into launch-core status without strong repo-grounded evidence.

---

## Questions for implementation review

1. Are the six launch-core domains genuinely supported by today’s codebase?
2. Which internal systems and governed constructs map cleanly to each one?
3. Which domains are strong enough to implement first with the least risk?
4. Which domains need further governed work before they can be made user-facing?
5. Which domains can support hierarchical sub-scores now, and which should stay flat?
6. What confidence logic already exists and what still needs to be built?
7. What exact DTO/contract/code surfaces would need to change to support Strategy A?
8. Is the most realistic implementation:
   - flat 6-score launch
   - phased 3-score then 6-score
   - or another sequence?

---

## Working conclusion

HealthIQ should not discard its phenotype architecture.

Instead, it should place a more human translation layer above it:

- a small set of understandable health-domain scores
- each powered by deterministic phenotype/pathway logic
- each explained with confidence, evidence, and next steps
- with hierarchical sub-scores shown only where they are biologically justified and genuinely useful

This gives the user what they actually want:

- reassurance
- explanation
- control
- a sense of where they stand

while preserving the engine strength that competitors do not have.

The strongest next step is not more naming iteration.
It is repo-grounded implementation research on the six launch-core domains, followed by a synthesised implementation blueprint and sprint plan.
