# HealthIQ AI — Customer-Facing Health Scores Mapping Matrix v0.1

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

## Proposed customer-facing health score set

These are intentionally user-readable, outcome-relevant, and less medical than the internal phenotype layer.

1. Heart & artery health
2. Blood sugar stability
3. Liver & metabolic load
4. Inflammation & body stress
5. Oxygen & energy support
6. Hormone balance
7. Thyroid & body speed
8. Kidney health
9. Nutrient status & recovery
10. Recovery & resilience

---

## Mapping matrix

| Customer-facing health score | What it means to a user | Likely contributing phenotypes / syndrome-states | Likely contributing systems | Notes on current strength |
|---|---|---|---|---|
| Heart & artery health | How healthy your cardiovascular risk picture looks overall, including lipids, vascular irritation, and artery stress | Lipid transport dysfunction; vascular inflammation burden; homocysteine / endothelial stress; atherogenic transport patterns | Cardiovascular, metabolic, inflammatory, nutritional | Likely one of HealthIQ’s strongest current domains |
| Blood sugar stability | How well your body appears to regulate blood sugar and whether you may be drifting toward insulin resistance or diabetes | Insulin resistance phenotype; glycaemic dysregulation patterns; triglyceride / HDL metabolic coupling | Metabolic, hepatic, cardiovascular | Very strong existing fit if insulin resistance work is mature |
| Liver & metabolic load | Whether your liver appears under strain from metabolic overload, fat handling issues, or broader processing burden | Hepatic stress patterns; fatty-liver-adjacent patterns; metabolic overload constructs | Hepatic, metabolic, inflammatory | Probably strong but may need careful wording to avoid overstatement |
| Inflammation & body stress | Whether your body looks calm and balanced or more inflamed and biologically stressed than ideal | Systemic inflammation patterns; vascular inflammation phenotype; stress-response related burden states | Immune, inflammatory, cardiovascular, metabolic | Strong candidate, but must avoid becoming too vague |
| Oxygen & energy support | How well your blood appears able to carry oxygen and support energy, stamina, and recovery | Iron deficiency / inflammation; anaemia-adjacent states; one-carbon / macrocytosis patterns where relevant | Hematological, nutritional, inflammatory | Strong user-facing translation of iron/oxygen phenotypes |
| Hormone balance | Whether hormone-related pathways look balanced or whether there are signals of disruption affecting libido, fertility, cycles, mood, or body composition | Sex hormone imbalance patterns; gonadal-axis disturbance; LH/FSH/testosterone/oestrogen related patterns | Hormonal, reproductive, thyroid, metabolic | Likely variable by sex, age, and marker coverage; confidence handling critical |
| Thyroid & body speed | Whether your thyroid-related signals suggest the body is running at a healthy pace or tending too slow / too fast | Thyroid-axis disturbance; thyroid-linked lipid disturbance; low FT4/FT3/TSh-context patterns | Thyroid, metabolic, cardiovascular, hormonal | Strong user-facing label if the thyroid model is coherent |
| Kidney health | Whether filtration and fluid-balance signals look reassuring or under strain | Renal strain constructs; eGFR / creatinine / urea patterns; hydration-related renal context | Renal, cardiovascular, metabolic | May need careful distinction between mild signal noise and true concern |
| Nutrient status & recovery | Whether the body appears to have the nutritional building blocks needed for repair, blood formation, immunity, and recovery | B12/folate pathway strain; vitamin D deficiency; iron-support states; broader nutrient insufficiency patterns | Nutritional, hematological, immune, hormonal | Broad but highly meaningful; may need internal sub-bucketing |
| Recovery & resilience | Whether the body appears robust and resilient or under cumulative strain from inflammation, hormone issues, poor recovery, or overload | Stress-load constructs; inflammation + nutrient depletion combinations; hormonal stress states | Multi-system composite: inflammatory, hormonal, nutritional, metabolic | Likely useful as a synthetic consumer layer, but must not become too fuzzy |

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

### 4. How confident we are
Confidence label plus explanation.

### 5. What this may mean over time
A calm, non-alarmist translation into real-world consequence.

### 6. What you can do next
Action-oriented, not fear-oriented.

---

## Many-to-many mapping principle

This translation layer is not expected to be one-to-one.

That is normal and acceptable.

### One customer-facing score may be powered by multiple phenotypes
Example:
- Heart & artery health may draw from lipid transport dysfunction, vascular inflammation, and homocysteine-related endothelial strain.

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

| Customer-facing score | Likely current readiness |
|---|---|
| Heart & artery health | Strong |
| Blood sugar stability | Strong |
| Liver & metabolic load | Moderate to strong |
| Inflammation & body stress | Moderate to strong |
| Oxygen & energy support | Strong |
| Hormone balance | Moderate |
| Thyroid & body speed | Moderate to strong |
| Kidney health | Moderate |
| Nutrient status & recovery | Moderate |
| Recovery & resilience | Moderate / composite, may be premature |

This suggests HealthIQ may not need to launch all 10 at once.
A smaller initial set of strongest domains may produce a better first UX.

---

## Suggested launch strategy

### Option A — Start with 6 strongest domains
Recommended if product clarity matters more than breadth.

Possible first-release set:
1. Heart & artery health
2. Blood sugar stability
3. Liver & metabolic load
4. Inflammation & body stress
5. Oxygen & energy support
6. Nutrient status & recovery

### Option B — Launch all 10
Only advisable if the mapping and confidence logic is sufficiently robust in every domain.

At present, a staged launch may be wiser than forcing weak domains into the first customer-facing score model.

---

## Key product benefits of this model

If implemented well, this model should:

- make the first screen far more reassuring and understandable
- preserve HealthIQ’s deterministic moat instead of flattening it into traffic lights
- let users see where they are strong, where they are strained, and where confidence is high or low
- link deep phenotype/pathway logic to real-world health concerns people understand
- reduce the sense that HealthIQ is “just another biomarker table”

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

---

## Questions for medical/strategy review

1. Are these 10 domains the right top-level customer-facing categories?
2. Which existing phenotypes map cleanly into each domain today?
3. Which domains are strong enough to launch now?
4. Which domains need further governed work before becoming customer-facing scores?
5. Are any of these domains too broad, too overlapping, or too anxiety-provoking?
6. Should some domains be merged, split, or renamed?
7. What should be the final user-facing wording for each domain?
8. How should confidence be calculated and displayed at the domain-score level?

---

## Working conclusion

HealthIQ should not discard its phenotype architecture.

Instead, it should place a more human translation layer above it:
- a small set of understandable health-domain scores
- each powered by deterministic phenotype/pathway logic
- each explained with confidence, evidence, and next steps

This gives the user what they actually want:
- reassurance
- explanation
- control
- a sense of where they stand

while preserving the engine strength that competitors do not have.