# HealthIQ AI — Customer-Facing Health Scores Mapping Matrix v0.3

## Purpose

This document proposes a translation layer between HealthIQ’s internal deterministic phenotype/system architecture and a simpler customer-facing score model.

The goal is not to replace the phenotype engine. The goal is to make the engine legible to ordinary users by mapping complex phenotype states onto a small set of health domains that people intuitively understand and care about.

This is a product/translation layer proposal, not a final medical ontology.

---

## Core principle

HealthIQ’s internal system is strong because it models real biological pathways and syndrome-state constructs. However, many of those constructs are too medical or too machine-shaped to work as top-level consumer UX labels.

Example:

- Internal phenotype: `ph_iron_deficiency_inflammation_v1`
- Strong internal meaning: syndrome-state in the iron-to-oxygen pathway
- Weak consumer UX label: too technical, too indirect

Users do not primarily think in phenotype language. They think in terms of:

- what might be going wrong
- what part of the body is under strain
- what they are safe from
- what could make them ill
- what explains how they feel

Therefore the customer-facing layer should present a small number of health scores, each powered by one or more existing phenotypes and systems.

---

## Strategic review update

This version incorporates the following architectural recommendation:

- keep the customer-facing score model as a translation layer above the deterministic engine
- do not treat customer-facing domains as identical to internal phenotypes or pathways
- use separate naming layers for consumer UX and clinician-facing outputs
- only split a top-level domain into sub-scores if those sub-scores are biologically distinct, user-understandable, and genuinely supported by deterministic logic

This means the document should now be read as a customer-facing score architecture, not as a full pathway map.

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

These are not diagnoses.
They are top-level health-domain scores powered by deterministic phenotype logic.

---

## Naming architecture

Each visible score should use three distinct naming layers:

1. **Consumer label** — calm, simple, emotionally legible
2. **Clinical handout label** — medically grounded and suitable for clinician-facing material
3. **Internal mapping** — phenotype/system architecture and deterministic constructs

### Important rule

Consumer labels must never replace the clinical labels in the clinician PDF/handout.

The safe structure is:

- Dashboard / customer UI → **Consumer label**
- Clinician handout / PDF → **Clinical label**
- Engine / architecture / mapping docs → **Internal mapping**

---

## Recommended score architecture

The preferred model is a layered one:

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

This is preferable because routine bloods often support vascular and cardiometabolic interpretation more directly than they support a narrow “heart” score in the sense of cardiac function.

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

These are currently at higher risk of becoming fuzzy or weakly supported if broken into multiple visible sub-scores too early.

---

## Final draft 8-domain score set

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

## Additional architecture rule: domain vs pathway vs outcome

Each visible score should keep these layers distinct internally:

- **Pathway domain** — the biological system being modelled
- **Interpretation construct** — the syndrome-state / risk frame / organ-pattern the engine has detected
- **User-facing score** — the simplified customer label
- **Outcome translation** — what this may mean over time if the pattern persists

### Example: blood, iron & oxygen

- Pathway domain: iron availability → erythropoiesis → oxygen transport
- Interpretation construct: functional iron deficiency / iron-restricted erythropoiesis / anaemia-adjacent state
- User-facing score: Blood, iron & oxygen
- Outcome translation: this may affect stamina, recovery, concentration, or longer-term anaemia risk if it persists

This helps preserve biological truth while still giving the user a simple first-screen experience.

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

### 1. What this score means
One short paragraph in plain English.

### 2. Why your score looks like this
A short explanation based on the contributing phenotype/pathway.

### 3. What contributed most
Key biomarkers and signals.

### 4. Contributing systems
Where appropriate, show 2–3 subdomains underneath the top score.

### 5. How confident we are
Confidence label plus explanation.

### 6. What this may mean over time
A calm, non-alarmist translation into real-world consequence.

### 7. What you can do next
Action-oriented, not fear-oriented.

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

## Candidate current-fit assessment

This is an early judgement of likely current platform readiness.

| Customer-facing score | Likely current readiness | Comment |
|---|---|---|
| Cardiovascular health | Strong | Best used hierarchically rather than as a flat “heart” score |
| Blood sugar control | Strong | Clean current fit if insulin-resistance logic is mature |
| Liver health | Moderate to strong | Strong if wording remains careful and non-diagnostic |
| Silent inflammation | Moderate | Valuable but at risk of becoming too broad |
| Blood, iron & oxygen | Strong | One of the clearest pathway-to-user translations |
| Hormone balance | Moderate | Confidence handling and subgroup logic are critical |
| Thyroid & energy regulation | Moderate to strong | Good user-facing label if the underlying model is coherent |
| Kidney function | Moderate | Needs careful handling of mild abnormalities and confidence |

This suggests HealthIQ does not need to force all domains equally hard at launch.
A smaller initial set of strongest domains may still produce a better first UX.

---

## Suggested launch strategy

### Option A — Start with 6 strongest domains
Recommended if product clarity matters more than breadth.

Possible first-release set:
1. Cardiovascular health
2. Blood sugar control
3. Liver health
4. Blood, iron & oxygen
5. Thyroid & energy regulation
6. Kidney function

### Option B — Add one broader context layer
If the team wants stronger whole-body context, consider adding:
7. Silent inflammation

### Option C — Add hormone balance once confidence handling is strong enough
8. Hormone balance

At present, a staged launch is likely wiser than forcing weaker domains into the first customer-facing score model.

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

---

## Questions for medical/strategy review

1. Are these 8 domains the right top-level customer-facing categories?
2. Which existing phenotypes map cleanly into each domain today?
3. Which domains are strong enough to launch now?
4. Which domains need further governed work before becoming customer-facing scores?
5. Are any of these domains too broad, too overlapping, or too anxiety-provoking?
6. Should some domains be merged, split, or renamed?
7. Which domains warrant visible sub-scores and which should remain flat at launch?
8. What should be the final user-facing wording for each domain?
9. How should confidence be calculated and displayed at the domain-score level?
10. For each top-level score, what is the underlying pathway, the interpretation construct, and the outcome translation?

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

The strongest next step is not to expand the domain list further. It is to take the strongest candidate domains and define, for each one:

1. the underlying biological pathway
2. the interpretation constructs that feed it
3. the user-facing score label
4. the optional sub-systems, if justified
5. the confidence logic
6. the calm explanation of what that score may mean over time

That is the point where this translation layer becomes a true product architecture rather than just a naming proposal.
