# HealthIQ AI — Phenotype Explanation Pattern v3
## How major findings must be written so the report feels phenotype-led, systems-led, consultation-grade, and educational

## Purpose

This document defines the required writing pattern for any major interpretive section in a gold-standard HealthIQ narrative.

Its purpose is to stop the narrative from collapsing into premium biomarker commentary, generic system language, or an exhaustive walk-through of every possible phenotype.

HealthIQ should not explain a blood panel as a sequence of isolated marker abnormalities.
It should explain the lead phenotype or system that best organises the panel, show that system in action, and identify the markers that support, restrain, or compensate within it.

Where a governed phenotype exists in the phenotype map, that phenotype should be the primary unit of explanation.
Where no governed phenotype exists, the report may use a broader system-level interpretation, but it must not pretend a governed phenotype exists when it does not.

The user should leave each major section understanding:
- what the lead phenotype or system is
- what that phenotype or system does
- which markers are carrying the signal
- which markers are protective, compensatory, or reassuring
- what the markers suggest about function
- why that matters elsewhere in the body
- how confident the interpretation is
- what would sharpen that confidence in future testing

This is the layer that creates the “this is how my body works” experience.

---

## Core rule

The primary unit of explanation is the lead governed phenotype or biological system, not the abnormal biomarker.

Biomarkers remain essential evidence.
But their job is to support the reading of a wider biological function, phenotype, pathway, or risk pattern.

The report should therefore read less like:
- marker
- interpretation
- next step

and more like:
- lead phenotype or system
- system in action
- supporting and compensatory markers
- functional reading
- body-wide significance
- confidence and missing evidence
- monitoring relevance

---

## Priority rule

Do not give full narrative weight to every phenotype.

The report should:
- explain the lead phenotype in depth
- explain a second phenotype only when it is genuinely near-tied, strongly interacting, or required to clarify the lead interpretation
- keep all other phenotypes in the background unless they materially change the reading

This is critical.

A gold-standard report should feel ranked and clinically prioritised, not encyclopaedic.

The narrative should sound like:
- this is the main pattern
- this is the main competing or interacting pattern
- this is why the first one leads
- this is what limits certainty

It should not sound like:
- here are all the phenotypes that could possibly be present

---

## Governed phenotype alignment rule

When a relevant governed phenotype exists in `phenotype_map_v1.yaml`, the narrative should align to that phenotype’s identity, signal logic, and systems framing.

This means the report should use the governed phenotype map as the anchor for:
- naming
- interpretation scope
- system grouping
- signal clustering
- monitoring relevance

Examples from the current governed map include:
- `ph_vascular_hcy_inflammation_v1` — "Vascular homocysteine inflammation pattern"
- `ph_renal_stress_v1` — "Renal stress pattern"
- `ph_metabolic_early_ir_v1` — "Early insulin resistance dyslipidaemia pattern"
- `ph_hba1c_metabolic_stress_v1` — "HbA1c metabolic stress pattern"
- `ph_hepatic_alt_inflammatory_v1` — "Hepatic ALT inflammatory pattern"
- `ph_tsh_axis_metabolic_v1` — "TSH axis metabolic context pattern"

If a phenotype is not actually present or not actually supported by the panel, do not force the label.

---

## Taxonomy rule

Not every meaningful section must be a phenotype.

The report may legitimately explain:
- a governed phenotype
- a broader system state
- a pathway interpretation
- a risk construct
- a compensatory pattern
- a resource-allocation trade-off

The rule is:
- use a governed phenotype where one truly exists and is supported
- use a broader system label where the biology is real but the governed phenotype layer is not yet available
- never blur the difference

---

## When to use this pattern

Use this pattern whenever the report is making a meaningful interpretive claim about:
- a governed phenotype
- a physiological system
- a pathway
- a risk construct
- a compensatory pattern
- a resource-allocation trade-off
- a recurring theme that connects multiple biomarkers

Typical examples include:
- vascular homocysteine inflammation
- renal stress
- early insulin resistance dyslipidaemia
- thyroid axis metabolic context
- lipid transport and cholesterol handling
- methylation and cellular maintenance
- iron transport and storage dynamics
- androgen signalling and binding balance
- inflammatory tone and immune activation
- liver processing and metabolic traffic

---

## Required eight-part pattern for a lead phenotype

Every major lead-phenotype or lead-system section should contain the following eight moves.

### 1. State the lead phenotype or system clearly

Start by naming the phenotype, system, pathway, or construct being discussed.

If a governed phenotype exists and is being used, name it explicitly.
If a broader system interpretation is being used, name the system honestly.

Examples:
- Vascular homocysteine inflammation pattern
- Renal stress pattern
- Lipid transport and cholesterol handling
- Methylation and cellular maintenance

Avoid headings like:
- Cholesterol
- Homocysteine issue
- Kidney markers
- Testosterone result

These are too marker-led and too flat.

---

### 2. Explain what that phenotype or system is for

Briefly explain what the phenotype or system represents biologically.

This is where the report creates the educational “wow” factor.
The user should understand why this system matters before being told whether it looks optimal or suboptimal.

This explanation should:
- be concise
- be physiologically accurate
- be written for an intelligent lay reader
- avoid fluff and metaphor

Examples:
- The vascular homocysteine phenotype is concerned with how efficiently homocysteine is being handled and whether that is creating a more adverse vascular maintenance environment.
- The renal stress phenotype captures the combined meaning of waste-clearance markers when filtration or concentration handling may be under pressure.
- The lipid transport system governs how cholesterol is carried between tissues, used for membrane and hormone biology, and returned to the liver for recycling or disposal.

This step should not become a textbook.
It should explain only enough to make the later interpretation meaningful.

---

### 3. Show the system in action

This is one of the most important additions in v3.

Do not move too quickly from system name to verdict.
Show how the system appears to be functioning in this panel.

This is where the narrative should explain:
- what the system appears to be doing
- which parts look efficient
- which parts look strained
- whether the system appears protective, compensatory, unresolved, or mixed

Examples:
- Cholesterol transport does not look uniformly adverse here; HDL-mediated protective transport appears relatively strong, while LDL-related exposure remains incompletely resolved.
- Homocysteine handling appears less clean than it should, while the inflammatory arm of the phenotype is not strongly activated on this draw.
- Renal filtration looks materially more reassuring than on the earlier panel, although interpretation still depends partly on hydration and body-composition context.

This is where the “wow” lives.
The report should read as an explanation of a system in motion, not a label applied to static numbers.

---

### 4. Identify the marker evidence, including protective or compensatory markers

State which markers are carrying the signal for the phenotype or system.

Do not only list the abnormal markers.
Also identify the markers that make the picture more reassuring, more compensatory, or more technically interesting.

This section should:
- reference the relevant biomarkers directly
- state whether they are high, low, in range, or mixed
- mention trend versus baseline when relevant
- include the protective or compensatory markers that change the interpretation
- avoid dumping every available value unless each one is doing interpretive work

Examples:
- Homocysteine is elevated and MCV is raised, while B12 has improved from the earlier panel and CRP remains low.
- LDL remains above the laboratory upper limit, but HDL is strong, triglycerides are low, and the ApoB:ApoA1 ratio is favourable.
- Creatinine has improved from the earlier panel and eGFR has risen, which materially changes the renal reading.

The data should feel selected and purposeful, not dumped.

---

### 5. Give the functional reading

After naming the phenotype or system and listing the evidence, the report must state what those markers most likely mean about function.

This is where the writing should sound most like a highly regarded clinician:
- technically confident
- precise
- calm
- qualified where appropriate

Examples:
- This is more consistent with incomplete methylation efficiency than with a simple persistent vitamin deficiency picture.
- This is not a uniformly adverse lipid pattern. The more precise reading is residual LDL-related exposure within an otherwise relatively favourable transport profile.
- The renal profile is materially more reassuring than the earlier panel, although creatinine-based interpretation still requires context.

This move should not simply repeat the biomarkers in words.
It should convert them into physiological meaning.

---

### 6. Explain body-wide significance

Explain why this phenotype or system matters beyond itself.

How does it alter the meaning of other systems, risks, or patterns?

Examples:
- This matters because methylation efficiency affects vascular signalling, red-cell quality, and the efficiency of routine cellular maintenance.
- This matters because lipid transport is not only about total cholesterol. It influences long-term arterial exposure and changes the meaning of apparently reassuring surface lipid numbers.
- This matters because renal filtration influences how confidently several other circulating markers can be read over time.

This is one of the most important “wow” moves in the whole report.
It shows the user that a single system can alter the meaning of several others.

---

### 7. State why this phenotype is leading, then explain confidence and what limits it

Confidence is essential, but it should come after the system reading, not before it.

The narrative should first explain the system in action.
Then it should explain:
- why this phenotype is the lead interpretation
- whether confidence is high, moderate, or limited
- what supporting evidence is present
- what key evidence is missing
- what future markers would sharpen or weaken the interpretation

This section should not sound defensive.
It should sound transparent and technically disciplined.

Examples:
- This phenotype leads because the signal is coherent across homocysteine and red-cell indices, while the inflammatory arm is quieter.
- Confidence is moderate rather than high because the pattern is biologically coherent but not fully confirmed by deeper nutrient or pathway markers.
- Confidence would increase if future testing included MMA, B6, repeat homocysteine, or a clearer nutrient-functional panel.

This is not a disclaimer.
It is part of what makes the report feel serious and trustworthy.

---

### 8. State why it is worth monitoring

End the section by explaining why the phenotype or system should or should not be monitored over time.

This should not be generic.
It should answer:
- what is worth watching
- why it is worth watching
- what would count as improvement, persistence, or escalation

Examples:
- Homocysteine is worth following here because it is acting as a functional readout of methylation efficiency rather than simply a one-off abnormality.
- LDL remains worth monitoring because the broader pattern is partly reassuring, but not sufficiently reassuring to make LDL exposure irrelevant.
- Renal markers are worth rechecking in context because the direction of travel is favourable, but creatinine-based interpretation remains sensitive to hydration and body-composition context.

Monitoring relevance helps the report feel longitudinal and serious, rather than descriptive and static.

---

## The writing order inside each lead phenotype section

Each lead-phenotype section should usually follow this sequence:

1. lead phenotype or system name
2. brief explanation of biological role
3. system in action
4. marker evidence, including compensatory/reassuring markers
5. technical interpretation of function
6. body-wide significance
7. why it leads + confidence + what is missing
8. monitoring relevance

This order matters.

If the report jumps straight to abnormal markers before explaining the phenotype or system, the user gets information but not understanding.
If the report explains the phenotype or system first, then shows the system in action, the markers feel more meaningful and the section becomes memorable.

---

## Rule for second phenotype coverage

A second phenotype may be expanded only when one of the following is true:
- it is close enough to the lead interpretation that hierarchy needs explaining
- it materially alters the reading of the lead phenotype
- it explains a tension, contradiction, or compensatory feature that the lead phenotype alone cannot explain
- it changes next-step or monitoring logic

The second phenotype should usually be shorter than the lead phenotype section.

It should answer:
- why it did not lead
- how it interacts with the lead phenotype
- whether additional markers would change the hierarchy

This helps the report feel ranked and confidence-aware.

---

## Good versus weak examples

### Weak example

Homocysteine is high and MCV is also raised. B12 has improved, so this may suggest a methylation issue. This should be monitored.

Why this is weak:
- marker-led
- does not explain the phenotype or system
- does not explain why it matters
- does not show the system in action
- does not explain why it leads
- sounds like commentary rather than consultation

### Better example

#### Vascular homocysteine inflammation pattern

This phenotype concerns how efficiently homocysteine is being handled and whether that handling is creating a more adverse vascular maintenance context.

In this panel, the system does not read as overtly inflammatory. CRP is low, which is reassuring. The more active signal sits in the homocysteine-handling side of the phenotype.

Homocysteine remains elevated and MCV is raised, while B12 has improved from the earlier test and folate remains technically in range. That combination is more consistent with incomplete methylation efficiency than with a simple persistent deficiency picture.

This matters because the signal is wider than one vitamin result. It touches vascular signalling, red-cell quality, and routine cellular maintenance.

This phenotype leads because the pattern is coherent across the available markers, although confidence remains moderate rather than high because deeper confirmatory markers such as MMA and B6 are not available.

Homocysteine is therefore worth monitoring here as a functional readout of how cleanly this system is running over time.

Why this is better:
- names the phenotype
- explains its role
- shows the system in action
- uses markers as evidence
- includes the reassuring marker
- gives a functional reading
- explains why it leads
- explains confidence and monitoring value

---

## Compensation and trade-off rule

When a section involves compensation, protection, buffering, or trade-off, explain that as a system-level or phenotype-level pattern.

Do not write compensation as a dramatic story.
Do not flatten it into vague hedging.

Use this pattern:
- what the phenotype or system appears to be maintaining
- which markers suggest that maintenance is being achieved
- which markers suggest the cost or inefficiency of that strategy
- what remains uncertain

Example direction:
- Lipid transport retains protective features through strong HDL, low triglycerides, and a favourable ApoB:ApoA1 ratio, but LDL-related exposure remains incompletely resolved.

The wow comes from showing the system in action and identifying the supportive or compensatory markers inside that system.

---

## Lifestyle integration rule

Lifestyle context must be integrated into lead phenotype sections where it materially changes interpretation.

Do not bolt lifestyle on as a separate afterthought.
Instead, use it to clarify:
- whether the biology matches the declared behaviour
- whether the biology is more or less reassuring in context
- whether there is tension between lifestyle and phenotype expression

Examples:
- In the context of a 13–14 hour fasting pattern and recent weight loss, the glucose profile is reassuring. The more informative remaining signal sits in lipid handling or methylation rather than glycaemic control.
- Given the reported alcohol intake, the combination of raised MCV and elevated homocysteine becomes more physiologically relevant.
- Despite the absence of formal exercise, the lipid profile still retains some protective features, which changes the tone of interpretation.

Lifestyle should refine the phenotype reading, not sit beside it.

---

## Longitudinal rule

For returning users, lead phenotype sections should refer to direction of travel where prior data exists.

The section should answer:
- is this phenotype or system more stable, less stable, or unchanged?
- has the meaning of the pattern changed over time?
- has a previous concern resolved, persisted, or evolved?

Examples:
- The methylation signal is still present, but the B12 line has improved compared with the earlier panel.
- Renal interpretation is materially more reassuring than four months earlier.
- The lipid transport pattern has not deteriorated substantially, but neither has it moved into a clearly optimised range.

Longitudinal comparison should support the system story, not interrupt it.

---

## Marker-alone rule

A biomarker may be discussed on its own only when:
- it is clinically important in isolation
- it acts as a key gateway marker
- it directly changes urgency or next-step logic
- there is not yet a governed phenotype or meaningful multi-marker system read available

Even then, the report should still try to answer:
- what function this marker belongs to
- why it matters beyond itself
- whether it should later be nested into a phenotype if coverage expands

This protects the report from collapsing back into flat report commentary.

---

## What must not happen

Do not write phenotype sections as:
- a string of abnormal results with brief comments
- a mini textbook chapter
- a dramatic narrative about the body “fighting” or “failing”
- a generic health explainer unrelated to the actual panel
- a lifestyle lecture
- a cautious non-interpretation that never states the likely functional reading
- a fake phenotype label that is not actually governed or supported
- a full walk-through of every possible phenotype in equal depth

Common failure examples:
- “This may suggest that there could possibly be some issue with…”
- “The body is borrowing from one system to rescue another.”
- “This is the hidden symphony of your metabolism.”
- “Your body is asking for support here.”
- “Marker X is high. Marker Y is low. Marker Z is normal.”
- “This is the early insulin resistance phenotype” when the required governed signals are not actually present.

These either sound weak, theatrical, generic, or architecturally sloppy.

---

## Final standard

A successful lead-phenotype section should make the user feel:
- I understand what phenotype or system is being discussed
- I understand what that phenotype or system is for
- I understand how that system appears to be functioning in my body
- I understand which markers are supporting, compensating, or limiting that system
- I understand why these markers belong together
- I understand why this phenotype leads over others
- I understand how confident that interpretation is
- I understand what would sharpen confidence next time
- I understand why this is or is not worth monitoring over time

If a section does not achieve that, it is not yet at HealthIQ gold-standard level.
