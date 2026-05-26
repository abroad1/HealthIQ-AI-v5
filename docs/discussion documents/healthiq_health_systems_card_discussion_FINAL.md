# HealthIQ AI — Health Systems Card UX Discussion Document v0.3

**Purpose:** Team discussion draft  
**Status:** Revised design-control discussion version — not final implementation specification  
**Focus:** Customer-facing Health Systems Card for the HealthIQ AI results experience  
**Intended next step:** Claude Code repo-grounded audit to confirm what can be surfaced immediately and what requires backend assembly or rebuilding

---

## 1. Why this card exists

HealthIQ AI should not feel like a prettier blood-test table.

The Health Systems Card is intended to translate HealthIQ’s deterministic biomarker, pathway and phenotype logic into a clear customer-facing view of how major biological systems appear to be reading from the user’s uploaded results.

The card must help users understand:

- this is a health-system-level judgement, not a one-marker flag
- the score is built from uploaded biomarker evidence
- the system may look strong, stable, optimised, or under strain
- the reliability of the score depends on marker coverage and signal quality
- HealthIQ is transparent about what it used and what was missing

The key differentiation is:

> HealthIQ scores are evidence-built, not opinion-generated.

The card must make that visible.

HealthIQ is a metabolic intelligence platform, not a disease platform. The card should support both:

- users concerned about possible system strain or suboptimal patterns
- users who want to understand whether their lifestyle, training, nutrition or supplement regime is producing strong metabolic patterns

The product should avoid feeling like it is only for fitness optimisation or only for disease-risk concern. It must work for both.

---

## 2. Core design principle

The collapsed card should sell the intelligence.

The expanded reveal should prove the intelligence.

In other words:

- the headline state gives instant understanding
- the reveal shows the biological systems, biomarker evidence and missing data behind the score

The card should feel premium, calm and visual. It should not become a prose-heavy report section.

### Prose-light design rule

Do not use a paragraph where a score, chip, biomarker card, mini-dial, evidence state, or missing-marker state can communicate the same point more clearly.

---

## 3. Headline / collapsed card

The collapsed card should provide a clear system-level read in a few seconds.

### Proposed elements

1. **Health system name**  
   Example: `Cardiovascular health`

2. **Plain-English system descriptor**  
   Example: `Heart, arteries and circulation`

3. **Large score visual**  
   A premium dial, gauge or score device.  
   Example: `88 / 100`

4. **Band label**  
   Example bands:
   - Strong
   - Stable
   - Watch
   - Needs attention

5. **Score reliability**  
   This tells the user how much trust to place in the score.  
   Example: `Good reliability`

6. **Evidence completeness**  
   This tells the user how much relevant marker evidence was available.  
   Example: `8 of 11 relevant markers included`

7. **Short health-system read**  
   One short sentence only.  
   Example:  
   `Your cardiovascular pattern looks well supported, with no major strain signals in the markers provided.`

8. **Supporting biological systems preview**  
   Small visual chips, bars or mini indicators.  
   Example:
   - Lipid transport
   - Vascular strain
   - Homocysteine pathway

9. **Expand action**  
   Example: `See what shaped this score`

---

## 4. Collapsed-card display flexibility

`Score reliability` and `Evidence completeness` are both required concepts in the product model, but the final UX does not have to give them equal weight in the collapsed card.

The design should test whether the collapsed card should show:

### Option A — both concepts explicitly

- `Score reliability: Good`
- `Evidence completeness: 8 of 11 markers included`

### Option B — reliability plus compact coverage

- `Good reliability`
- `8 / 11 markers included`

### Option C — reliability in headline, completeness in reveal

- collapsed card shows `Good reliability`
- reveal explains `8 of 11 relevant markers were included`

The product model should retain both concepts either way. The UX decision is only about where and how visibly they appear.

---

## 5. Score reliability vs evidence completeness

`Score reliability` and `Evidence completeness` should not be treated as the same thing.

### Evidence completeness answers

> How much of the expected marker set was uploaded?

Example:

`8 of 11 relevant markers included`

### Score reliability answers

> How much trust should the user place in this score?

Score reliability may be influenced by:

- relevant marker coverage
- presence of key confirming markers
- signal consistency
- contradictions between markers
- whether high-value biomarkers are missing
- whether the result pattern is simple or complex

This is more transparent than collapsing both concepts into one label.

---

## 6. Expanded / reveal card

The expanded reveal should explain the score transparently without overwhelming the user.

### Proposed elements

1. **What this score means**  
   A short explanation of the score band.  
   This title is acceptable for v0.3, but can be refined later.

2. **Supporting biological systems**  
   Each major subsystem or biological pathway contributing to the overall score should be shown as its own mini-section.

3. **Subsystem score or status**  
   Each supporting biological system may show a small bar, mini dial, or status label.

4. **Biomarker evidence cards**  
   Each subsystem should contain biomarker cards, not just text lists.

5. **Uploaded biomarkers**  
   Uploaded biomarkers should be active and colourised, showing:
   - biomarker name
   - result value
   - unit
   - reference range
   - status / score

6. **Missing relevant biomarkers**  
   Biomarkers that would strengthen the score but were not uploaded should still appear, but greyed out and marked:  
   `Not uploaded`

7. **Missing-marker explanation**  
   The reveal should include a short explanation such as:  
   `Markers marked “Not uploaded” were not included in your blood panel, so they did not contribute to this score.`

8. **Reliability explanation**  
   Explains why the score reliability is high, good, moderate or limited.

9. **What this may mean over time**  
   Calm, non-diagnostic consequence wording.  
   This should describe possible system strain or resilience implications, not disease claims.

10. **What to do next**  
   Contextual next-step guidance, such as lifestyle review, retesting, marker completion, or clinician discussion where appropriate.

---

## 7. Biomarker card consistency rule

A biomarker must have one canonical frontend card representation.

The same biomarker card used in the full biomarker view should also be used inside the Health Systems Card reveal.

The system card may group, miniaturise or grey out those cards, but it must not create a second visual language for biomarkers.

This is important because users may otherwise lose trust if the same biomarker appears differently in different parts of the product.

### Rule

- uploaded biomarker = active card
- missing relevant biomarker = greyed-out card
- missing marker label = `Not uploaded`
- irrelevant biomarker = not shown
- frontend must not invent interpretation
- all interpretation must come from governed backend output

---

## 8. Why missing biomarkers should be visible

Missing biomarkers should not be hidden.

If a system score is partly limited by the uploaded panel, the user should be able to see why.

Greyed-out missing biomarker cards help explain:

- why reliability is not higher
- what additional markers would improve interpretation
- that HealthIQ is not pretending to know more than the user uploaded
- that the score is evidence-bounded

This is central to trust.

The missing-marker state should be factual, not negative. The user should feel informed, not criticised for uploading an incomplete panel.

---

## 9. Disease-risk vs health-system-read framing

The card should not be framed primarily as a disease-risk card.

HealthIQ should avoid language such as:

- probability of dysfunction
- likely disease
- system failure
- diagnostic risk

The phrase `system performance` is useful, but should not be overused in a way that makes the product sound only like a fitness or optimisation tool.

Preferred language includes:

- health-system read
- system read
- well supported
- stable pattern
- strain signals
- may affect resilience over time
- worth understanding
- score reliability
- evidence completeness

This allows the card to support both:

- people trying to understand possible strain
- people optimising health, resilience, performance and longevity

---

## 10. Backend data requirements

The frontend must not infer the evidence model.

Before implementation, the backend should provide or confirm availability of the following fields for each Health Systems Card.

### Domain-level fields

- domain ID
- consumer-facing domain name
- plain-English descriptor
- score
- score band
- score reliability label
- score reliability explanation
- evidence completeness numerator
- evidence completeness denominator
- short health-system read
- supporting biological system labels
- expand/reveal content

### Supporting biological system fields

For each supporting biological system:

- subsystem ID
- subsystem label
- subsystem score or status, if available
- included biomarker IDs
- missing relevant biomarker IDs
- short subsystem explanation, if required

### Biomarker evidence fields

For each biomarker card shown inside the reveal:

- biomarker ID
- biomarker display name
- uploaded / not uploaded state
- value, where uploaded
- unit, where uploaded
- reference range, where uploaded
- biomarker score/status, where uploaded
- canonical colour/status state
- whether it contributed to score, reliability, or both

### Governance rule

The frontend may render, group and visually arrange data.

The frontend must not calculate:

- domain score
- score band
- score reliability
- evidence completeness
- expected marker set
- missing relevant markers
- subsystem interpretation
- consequence wording

These must be provided by governed backend output.

---

## 11. Example: strong / optimised card

### Collapsed card example

**Cardiovascular health**  
Heart, arteries and circulation

**88 / 100**  
Strong

**Score reliability:** Good  
**Evidence completeness:** 8 of 11 relevant markers included

**Health-system read:**  
Your cardiovascular pattern looks well supported, with favourable lipid transport and no major strain signals in the markers provided.

**Supporting biological systems:**  
Lipid transport · Vascular strain · Homocysteine pathway

**Action:**  
See what shaped this score

---

### Expanded reveal example

**What this score means**  
This score suggests your cardiovascular system looks well supported in the markers provided.

**Supporting biological systems**

#### Lipid transport
Mini score/status: Strong

Active biomarker cards:
- LDL cholesterol
- HDL cholesterol
- Triglycerides
- Total cholesterol

Greyed-out missing biomarker cards:
- ApoB — Not uploaded
- Lipoprotein(a) — Not uploaded

#### Vascular strain
Mini score/status: Stable

Active biomarker cards:
- Homocysteine
- CRP

Greyed-out missing biomarker cards:
- hs-CRP — Not uploaded

**Missing-marker explanation**  
Markers marked `Not uploaded` were not included in your blood panel, so they did not contribute to this score.

**Score reliability**  
Good reliability because the panel included most core cardiovascular markers, but some advanced markers were not uploaded.

**What this may mean over time**  
This pattern is broadly reassuring, although persistent strain signals may still be worth tracking over time.

**What to do next**  
Maintain the behaviours supporting this pattern and consider completing missing advanced markers if deeper cardiovascular optimisation is a goal.

---

## 12. Example: mixed / watch card

### Collapsed card example

**Cardiovascular health**  
Heart, arteries and circulation

**58 / 100**  
Watch

**Score reliability:** Good  
**Evidence completeness:** 8 of 11 relevant markers included

**Health-system read:**  
Several cardiovascular signals suggest this system may be under strain, mainly from the homocysteine pathway and vascular context markers.

**Supporting biological systems:**  
Lipid transport · Vascular strain · Homocysteine pathway

**Main contributor:**  
Homocysteine pathway strain

**Action:**  
See what shaped this score

---

### Expanded reveal example

**What this score means**  
This score suggests the cardiovascular system is not reading as optimally supported in the markers provided. It does not diagnose a condition, but it does indicate a pattern worth understanding.

**Supporting biological systems**

#### Lipid transport
Mini score/status: Stable

Active biomarker cards:
- LDL cholesterol
- HDL cholesterol
- Triglycerides
- Total cholesterol

Greyed-out missing biomarker cards:
- ApoB — Not uploaded
- Lipoprotein(a) — Not uploaded

#### Homocysteine pathway
Mini score/status: Watch

Active biomarker cards:
- Homocysteine
- Vitamin B12
- Folate

Greyed-out missing biomarker cards:
- Active B12 — Not uploaded

**Missing-marker explanation**  
Markers marked `Not uploaded` were not included in your blood panel, so they did not contribute to this score.

**Score reliability**  
Good reliability because several relevant markers were present and pointed toward a coherent pattern, although additional markers would improve completeness.

**What this may mean over time**  
If this pattern persists, it may suggest reduced cardiovascular resilience or increased metabolic strain. This should be interpreted as a health-system signal, not as a diagnosis.

**What to do next**  
Review relevant lifestyle context, nutrient status and repeat testing where appropriate. Consider clinician discussion if the pattern is persistent or clinically concerning.

---

## 13. Version 1 implementation position

For v1, the design should be reusable across all six launch-core domains.

However, the first live implementation should only surface the domains that are already repo-ready:

1. Cardiovascular health
2. Blood sugar control
3. Liver health

The remaining domains should use the same design model later, once their backend scoring, confidence/reliability and governed narrative support are ready:

4. Blood, iron & oxygen
5. Thyroid & energy regulation
6. Kidney function

---

## 14. Proposed Claude Code audit

Before implementation, Claude Code should complete a repo-grounded audit of existing assets.

The audit should answer:

1. Which Health Systems Card fields already exist in the current DTO?
2. Which fields exist but are hidden or poorly surfaced in the frontend?
3. Which fields can be surfaced immediately without backend changes?
4. Which fields require light backend assembly?
5. Which fields require new governed backend logic?
6. Whether current biomarker card components can be reused inside the expanded reveal
7. Whether missing biomarkers are already available as structured data
8. Whether evidence completeness can be calculated from existing backend fields or must be added
9. Whether score reliability already exists as a backend field or must be refined
10. Whether supporting biological systems/subsystems already exist in the DTO or only in backend logic

### Expected audit output

Claude should return a table with:

- proposed card field
- current source path / component / DTO field
- current availability
- frontend-ready status
- backend gap, if any
- implementation risk
- recommendation

The purpose of the audit is not to redesign the card. It is to determine what can be surfaced immediately and what requires governed rebuilding.

---

## 15. Open questions for team feedback

1. Is `What this score means` the right reveal-section title, or should it be softened?
2. Should the collapsed card show both score reliability and evidence completeness, or is that too much for the headline state?
3. Should supporting biological systems have their own mini score, or only a status label?
4. How many biomarker cards can be shown in the reveal before the UI feels too busy?
5. Should missing biomarkers be shown by default, or under a secondary toggle inside the reveal?
6. Should biohacker-oriented language differ from general-user language, or should the same card serve both groups?
7. What is the best visual form for the headline score: dial, gauge, radial score, or premium numeric card?
8. Is `Not uploaded` the right standard label for missing relevant biomarkers?
9. Should the card use `Health-system read`, `System read`, or another title for the short interpretation sentence?

---

## 16. Working conclusion

The Health Systems Card should give users an immediate understanding of how a major biological system appears to be reading from their uploaded results, then transparently reveal the evidence behind that judgement.

The card should be visual first, prose-light, and evidence-transparent.

It should make HealthIQ feel like a governed metabolic intelligence platform rather than a dashboard of isolated blood markers.

This v0.3 document is suitable for a repo-grounded codebase audit before implementation planning.
