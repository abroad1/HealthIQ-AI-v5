# HealthIQ AI — Customer-Facing Health Scores Mapping Matrix v0.2

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
- use a hierarchical score model rather than a flat one where that better reflects the biology
- only split a top-level domain into sub-scores if those sub-scores are biologically distinct, user-understandable, and genuinely supported by deterministic logic

This means the document should now be read as a customer-facing score architecture, not as a full pathway map.

---

## Product framing recommendation

Each customer-facing domain should be shown as:

- a score out of 100
- a confidence level
- a one-line plain-English meaning
- an expandable explanation showing:
  - why the score is what it is
  - which biomarkers and patterns contributed
  - what would improve confidence
  - what this may mean over time

These are not “diagnoses.”
They are top-level health-domain scores powered by deterministic phenotype logic.

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

- Lipid transport = 80
- Artery / vascular strain = 60
- Homocysteine-related vascular risk = 68

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
- Oxygen & energy support
  - iron availability
  - red-cell production
  - oxygen-carrying support
- Thyroid & body speed
  - thyroid axis
  - thyroid-linked metabolic effects
- Kidney health
  - filtration
  - renal strain
  - hydration-context, if governable and robust

### Poor candidates for early splitting

- Inflammation & body stress
- Nutrient status & recovery
- Recovery & resilience

These are currently broad and at higher risk of becoming fuzzy or weakly supported if broken into multiple visible sub-scores too early.

---

## Proposed customer-facing health score set

These are intentionally user-readable, outcome-relevant, and less medical than the internal phenotype layer.

1. Cardiovascular health
2. Blood sugar stability
3. Liver & metabolic load
4. Inflammation & body stress
5. Oxygen & energy support
6. Hormone balance
7. Thyroid & body speed
8. Kidney health
9. Nutrient status & recovery
10. Recovery & resilience

### Naming note

“Cardiovascular health” is preferred to “Heart & artery health” if the domain is primarily being driven by vascular, lipid, and metabolic risk logic rather than direct heart-function measurement.

If the team prefers to keep “Heart & artery health” for consumer warmth, the expanded view should still make clear that the visible subdomain logic is more vascular / lipid / cardiometabolic than direct cardiac-function scoring.

---

## Mapping matrix

| Customer-facing health score | What it means to a user | Likely contributing phenotypes / syndrome-states | Likely contributing systems | Recommended hierarchy approach | Notes on current strength |
|---|---|---|---|---|---|
| Cardiovascular health | How healthy your cardiovascular risk picture looks overall, including lipids, artery strain, and vascular risk burden | Lipid transport dysfunction; vascular inflammation burden; homocysteine / endothelial stress; atherogenic transport patterns | Cardiovascular, metabolic, inflammatory, nutritional | Strong candidate for visible sub-scores | Likely one of HealthIQ’s strongest current domains |
| Blood sugar stability | How well your body appears to regulate blood sugar and whether you may be drifting toward insulin resistance or diabetes | Insulin resistance phenotype; glycaemic dysregulation patterns; triglyceride / HDL metabolic coupling | Metabolic, hepatic, cardiovascular | May remain a single top-level domain initially | Very strong existing fit if insulin resistance work is mature |
| Liver & metabolic load | Whether your liver appears under strain from metabolic overload, fat handling issues, or broader processing burden | Hepatic stress patterns; fatty-liver-adjacent patterns; metabolic overload constructs | Hepatic, metabolic, inflammatory | Can remain top-level initially; sub-splitting may come later | Probably strong but may need careful wording to avoid overstatement |
| Inflammation & body stress | Whether your body looks calm and balanced or more inflamed and biologically stressed than ideal | Systemic inflammation patterns; vascular inflammation phenotype; stress-response related burden states | Immune, inflammatory, cardiovascular, metabolic | Keep broad for now; avoid early over-splitting | Strong candidate, but must avoid becoming too vague |
| Oxygen & energy support | How well your blood appears able to carry oxygen and support energy, stamina, and recovery | Iron deficiency / inflammation; anaemia-adjacent states; one-carbon / macrocytosis patterns where relevant | Hematological, nutritional, inflammatory | Strong candidate for visible sub-scores | Strong user-facing translation of iron/oxygen phenotypes |
| Hormone balance | Whether hormone-related pathways look balanced or whether there are signals of disruption affecting libido, fertility, cycles, mood, or body composition | Sex hormone imbalance patterns; gonadal-axis disturbance; LH/FSH/testosterone/oestrogen related patterns | Hormonal, reproductive, thyroid, metabolic | Probably keep top-level until sex-specific logic is strong enough | Likely variable by sex, age, and marker coverage; confidence handling critical |
| Thyroid & body speed | Whether your thyroid-related signals suggest the body is running at a healthy pace or tending too slow / too fast | Thyroid-axis disturbance; thyroid-linked lipid disturbance; low FT4/FT3/TSH-context patterns | Thyroid, metabolic, cardiovascular, hormonal | Good candidate for limited sub-scores | Strong user-facing label if the thyroid model is coherent |
| Kidney health | Whether filtration and fluid-balance signals look reassuring or under strain | Renal strain constructs; eGFR / creatinine / urea patterns; hydration-related renal context | Renal, cardiovascular, metabolic | Candidate for limited sub-scores | May need careful distinction between mild signal noise and true concern |
| Nutrient status & recovery | Whether the body appears to have the nutritional building blocks needed for repair, blood formation, immunity, and recovery | B12/folate pathway strain; vitamin D deficiency; iron-support states; broader nutrient insufficiency patterns | Nutritional, hematological, immune, hormonal | Keep broad for now; may need later internal sub-bucketing before visible sub-scores | Broad but highly meaningful; may need internal sub-bucketing |
| Recovery & resilience | Whether the body appears robust and resilient or under cumulative strain from inflammation, hormone issues, poor recovery, or overload | Stress-load constructs; inflammation + nutrient depletion combinations; hormonal stress states | Multi-system composite: inflammatory, hormonal, nutritional, metabolic | Do not split early; may be premature as a launch domain | Likely useful as a synthetic consumer layer, but must not become too fuzzy |

---

## Important translation rule

The customer-facing score should not be a direct rename of a phenotype.

Bad:
- “Iron deficiency inflammation phenotype”

Better:
- “Oxygen & energy support”

Then inside the expanded explanation:
- explain that this score is being influenced by iron-related and inflammation-related blood patterns

This preserves engine truth while making the product understandable.

---

## Additional architecture rule: domain vs pathway vs outcome

Each visible score should keep these layers distinct internally:

- **Pathway domain** — the biological system being modelled
- **Interpretation construct** — the syndrome-state / risk frame / organ-pattern the engine has detected
- **User-facing score** — the simplified customer label
- **Outcome translation** — what this may mean over time if the pattern persists

### Example: oxygen & energy support

- Pathway domain: iron availability → erythropoiesis → oxygen transport
- Interpretation construct: functional iron deficiency / iron-restricted erythropoiesis / anaemia-adjacent state
- User-facing score: Oxygen & energy support
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
  - Oxygen & energy support
  - Nutrient status & recovery
  - Recovery & resilience

The customer layer exists to simplify interpretation, not to mirror the engine exactly.

---

## Candidate current-fit assessment

This is an early judgement of likely current platform readiness.

| Customer-facing score | Likely current readiness | Comment |
|---|---|---|
| Cardiovascular health | Strong | Best used hierarchically rather than as a flat “heart” score |
| Blood sugar stability | Strong | Clean current fit if insulin-resistance logic is mature |
| Liver & metabolic load | Moderate to strong | Strong if wording remains careful and non-diagnostic |
| Inflammation & body stress | Moderate | Valuable but at risk of becoming too broad |
| Oxygen & energy support | Strong | One of the clearest pathway-to-user translations |
| Hormone balance | Moderate | Confidence handling and subgroup logic are critical |
| Thyroid & body speed | Moderate to strong | Good user-facing label if the underlying model is coherent |
| Kidney health | Moderate | Needs careful handling of mild abnormalities and confidence |
| Nutrient status & recovery | Moderate | Potentially useful, but broad |
| Recovery & resilience | Moderate / composite, may be premature | The weakest current domain and most at risk of fuzziness |

This suggests HealthIQ may not need to launch all 10 at once.
A smaller initial set of strongest domains may produce a better first UX.

---

## Suggested launch strategy

### Option A — Start with 6 strongest domains
Recommended if product clarity matters more than breadth.

Possible first-release set:
1. Cardiovascular health
2. Blood sugar stability
3. Liver & metabolic load
4. Oxygen & energy support
5. Thyroid & body speed
6. Kidney health

### Option B — Start with 6 strongest domains plus one broad context layer
If the team wants a stronger sense of whole-body context, consider adding:
7. Inflammation & body stress

### Option C — Launch all 10
Only advisable if the mapping and confidence logic is sufficiently robust in every domain.

At present, a staged launch is likely wiser than forcing weaker or more composite domains into the first customer-facing score model.

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
If the labels become too broad (“wellness”, “vitality”), the system loses explanatory power.

3. Overstated disease claims  
Top-layer scores must suggest risk direction or pathway strain without implying diagnosis.

4. Fake scoring  
No score should appear unless it is genuinely supported by deterministic logic and confidence logic.

5. Over-breadth too early  
A smaller number of strong, legible health scores may beat a larger but weaker set.

6. Unsupported sub-scores  
Do not show visible sub-scores such as “Heart” or “Vascular” unless those are genuinely distinct, biologically supportable, and not merely cosmetic splits.

7. Mixing pathway, state, and outcome  
Do not let the user-facing layer blur together the biological pathway, the detected interpretation construct, and the eventual health consequence.

---

## Questions for medical/strategy review

1. Are these 10 domains the right top-level customer-facing categories?
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
