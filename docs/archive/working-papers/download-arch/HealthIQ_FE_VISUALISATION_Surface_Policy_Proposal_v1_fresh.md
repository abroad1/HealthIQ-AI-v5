# HealthIQ FE-VISUALISATION — Surface Policy Proposal
*Version 1.0 draft — team discussion paper*

## 1. Why this paper exists

This paper sets out a proposed product-surface policy for FE-VISUALISATION.

The purpose is not to decide final UI polish.
The purpose is to decide, at strategy level, what HealthIQ should surface to users, what it should reserve for advanced or clinician views, and what should remain internal.

FE-VISUALISATION is not a cosmetic frontend sprint.
It is the point where deterministic engine output becomes product reality.

If we do not decide this explicitly, implementation will make hidden product decisions by default.

---

## 2. Research background

To inform this decision, we reviewed:

- the FE-VISUALISATION background paper
- a GTM/product-surface response from GPT
- a strategy response from Gemini
- a strategic/frontend product response from Claude
- additional product-strategy discussion in strategy chat
- further strategic input on a possible educational phenotype narrative layer for retail users

The goal of this review was not to average opinions.
It was to gather inputs, test them against HealthIQ’s strategy, and decide what best fits the product we are actually building.

---

## 3. Who we polled for input

The following inputs were considered:

### 3.1 Internal background paper
This set out the initial decision frame:
- FE-VISUALISATION is product-definition work, not just implementation
- each component needs a clear purpose
- each component needs a surface policy
- the team should distinguish standard, advanced, and internal/debug layers

### 3.2 GPT feedback
This was strongest on:
- GTM logic
- buyer utility
- visible differentiation
- making the engine’s superiority legible rather than merely exposing more output

### 3.3 Gemini feedback
This offered:
- some useful thoughts on confidence/data-integrity presentation
- a stronger push toward quantified display concepts
- a draft idea for phenotype/system storytelling, although the draft itself was not judged strong enough to use directly

### 3.4 Claude feedback
This was strongest on:
- tiered disclosure
- product-surface architecture
- component discipline
- translation of backend sophistication into biological intelligence without exposing implementation plumbing

### 3.5 Strategy-chat follow-up
Additional strategy discussion clarified an important opportunity:
HealthIQ may benefit from a secondary educational layer for retail users that explains how a system or phenotype works in the human body, why its biomarkers matter, and how apparently small deviations can matter in a connected biological system.  According to the human, the vast majority of standard end users will have no idean what a phenotype is.  If the platform surfaces information back to them by phenotype it is more likely to confuse them than inform.  Therefore, some education is needed to ensure they understand and value the data that they are being presented with. 

This educational layer must be clearly separated from personalised interpretation.

---

## 4. Executive conclusion

The strategic decision is:

**HealthIQ should not surface everything the engine knows.  
It should surface the smallest governed set of things that makes the engine’s superiority visible, trustworthy, and useful.**

This means:

- the standard user surface should lead with interpretation, not internals
- the product should use a tiered disclosure model
- InsightPanel should be the hero component
- ClusterCard should be the translated systems-thinking surface
- BiomarkerChart should support trust and context, not dominate the experience
- PipelineStatus should not be shown as raw pipeline plumbing on the retail surface
- a separate educational phenotype/system narrative layer is worth pursuing for retail users as a secondary “wow” experience, provided it is explicitly educational and never presented as personalised proof

---

## 5. Key headlines from the research

### 5.1 What all inputs broadly agreed on
Across the papers, there was strong alignment that:

- FE-VISUALISATION is where engine capability becomes product reality
- the frontend must not leak implementation artefacts
- the product must not look like a generic biomarker dashboard
- system-level interpretation is strategically important
- the standard user does not benefit from raw pipeline detail
- tiered disclosure is better than one flat experience for all audiences

### 5.2 What mattered most strategically
The most important strategic points that emerged were:

1. **Lead with synthesis, not charts**  
   If HealthIQ leads with charts, it risks looking like every other blood app.

2. **Show systems, not just markers**  
   The product must make visible that HealthIQ understands panel-level and system-level meaning.

3. **Protect trust through translation**  
   Backend artefacts should never appear on the product surface un-translated.

4. **Use confidence honestly**  
   The product should show what is known, what is suggested, and what remains uncertain.

5. **Create a memorable educational experience**  
   A carefully governed phenotype/system explainer layer could make users feel they finally understand how their body works.

---

## 6. Surface philosophy

### 6.1 Standard user surface
The standard user surface should answer four questions:

1. What matters most?
2. What system or pattern does it belong to?
3. Which markers are driving that?
4. What should I do next, and how confident is this picture?

This surface should feel:
- clear
- biologically intelligent
- calm but not weak
- more meaningful than a lab report
- more trustworthy than a generic AI explainer

### 6.2 Advanced / clinician surface
This surface should allow more depth without corrupting the standard user experience.

It should expose:
- ranked ambiguity
- supporting vs conflicting evidence
- confirmatory tests
- richer biomarker detail
- more explicit confidence boundaries

### 6.3 Internal / debug surface
This should remain out of the user product unless explicitly translated.

It may contain:
- raw pipeline states
- implementation IDs
- debug status
- parser/runtime diagnostics
- engineering object detail

---

## 7. Governance decision by component

## 7.1 BiomarkerChart

### Purpose
BiomarkerChart is the atomic trust component.
It is the most direct visual anchor for a single marker.

### What it should show in standard mode
- biomarker name
- raw value and unit
- lab-specific range position
- interpreted state
- whether this marker materially contributes to a broader pattern
- an explainer of what the marker is responsible for and the phenotype contributing group it sits in

### What it should not show by default
- backend field names
- technical engine metadata
- raw implementation values
- excessive low-value detail

### Governance decision
BiomarkerChart is important, but it is a supporting component, not the hero.

**It should help the user trust the result, not define the whole product.**

---

## 7.2 ClusterCard

### Purpose
ClusterCard is the system-level interpretation surface.

This is where HealthIQ demonstrates that it understands systems, not just isolated markers.

### What it should show in standard mode
- translated system or pattern name
- interpreted state or severity
- top contributing markers/signals
- short explanation of why the system matters now

### What it should not show
- cluster IDs
- internal labels
- untranslated engineering objects
- implementation-native grouping artefacts

### Governance decision
ClusterCard should be a translated biological system card, not a wrapper around raw cluster computation.

**This is one of the main visible proof points of HealthIQ’s differentiation.**

---

## 7.3 InsightPanel

### Purpose
InsightPanel is the hero component.

It is the main structured interpretation surface and the primary commercial surface.

### What it should show in standard mode
- one lead concern
- concise explanation of why it matters
- system-level context
- next-step logic
- confidence/uncertainty in simple language where relevant

### What it should show in advanced/clinician mode
- ranked ambiguity
- supporting and conflicting evidence
- confirmatory tests
- more explicit differential framing

### Governance decision
InsightPanel is the most important product component in FE-VISUALISATION.

**If InsightPanel is weak, the product feels weak.  
If InsightPanel is strong, HealthIQ immediately feels more sophisticated than a generic report viewer.**

---

## 7.4 PipelineStatus / Confidence Layer

### Purpose
This should not be a raw engineering-status widget for retail users.

The user-facing version, if present, should be a translated confidence/data-quality layer.

### What it should show in standard mode
- analysis complete
- data-quality limitations in plain language
- confidence reduced by missing markers or missing context
- what additional tests or data would improve confidence

### What should remain internal
- raw pipeline stages
- runtime logs
- debug diagnostics
- engineering object states

### Governance decision
For user-facing product purposes, PipelineStatus should become a **confidence and data-quality surface**, not a pipeline monitor.

---

## 8. Priority order for FE-VISUALISATION

If sequencing trade-offs are needed, the priority order should be:

1. InsightPanel
2. ClusterCard
3. BiomarkerChart
4. Translated confidence/data-quality layer
5. Raw pipeline/admin tooling later or internal-only

This order reflects what most clearly demonstrates HealthIQ’s strategic value.

---

## 9. Educational phenotype/system narrative layer

## 9.1 Why this idea is valuable
A strong additional idea emerged during strategy discussion:

For retail users, there may be meaningful value in a secondary educational layer that explains:
- what a system or phenotype is
- how the relevant biomarkers interact
- why each biomarker matters
- what can go wrong when that system is under strain

The point of this layer is not diagnosis.
The point is to create a “wow” experience:
“I had no idea that was how my body worked.”
That educational effect can help users understand why even a seemingly minor suboptimal marker may matter in the wider system.

## 9.2 What this layer is
This layer should be:
- educational
- reusable
- phenotype/system-level
- clearly separate from the personalised interpretation layer

It should not be the lead concern.
It should not replace the personalised result.
It should not pretend the user’s panel proves every part of the phenotype story.

## 9.3 What it may do
It may:
- explain how a biological system works
- explain which biomarkers commonly belong to that system
- explain how those biomarkers interact
- explain why breakdown in that system can matter for overall health
- help the user understand the body as an interconnected system

## 9.4 What it must never imply
It must never imply:
- that the full phenotype is proven in that user
- that every biomarker in the narrative is abnormal in that user
- that a partial panel proves a complete system story
- that this educational layer is a diagnosis

## 9.5 Recommended positioning
This should be framed as:
- “Understanding this system”
- “How this pathway works”
- “Why these biomarkers matter together”
- “What can happen when this system is under strain”

It should not be framed as:
- “This is exactly what is happening in your body”

## 9.6 Governance decision
HealthIQ should pursue this as a **secondary educational narrative layer for retail users**, not as the lead product interpretation surface.

**This is a differentiator, not the main claim.**

---

## 10. What the product should never imply

The surfaced product must never imply:

- diagnosis
- certainty beyond the evidence
- that all computed signals are equally important
- that polished charts equal meaningful interpretation
- that a compelling system story is the same as user-specific proof
- that internal engine completeness equals user usefulness

These are non-negotiable boundaries.

---

## 11. Why we are choosing this surface policy

We are choosing this policy because it best protects the product we are actually building.

### 11.1 It protects strategic differentiation
HealthIQ should not collapse into a chart-first blood app.
This policy makes systems thinking, structured interpretation, and confidence handling visible.

### 11.2 It protects trust
By separating standard, advanced, and internal surfaces, we reduce noise and prevent leakage of technical artefacts.

### 11.3 It protects honesty
By keeping the educational phenotype narrative separate from user-specific interpretation, we preserve the distinction between explanation and evidence.

### 11.4 It improves user experience
The standard user should see the smallest high-value set of things that make the product feel intelligent and useful, not an overwhelming wall of widgets.

### 11.5 It supports later growth
This policy still leaves room for:
- advanced mode
- clinician mode
- enterprise surfaces
- deeper longitudinal education later

---

## 12. Final recommendation to the team

Approve the following as HealthIQ’s initial FE-VISUALISATION surface policy:

### Standard mode
- InsightPanel as hero
- ClusterCard as translated system summary
- BiomarkerChart only for priority markers
- translated confidence/data-quality context
- optional secondary educational system/phenotype explainer

### Advanced / clinician mode
- richer ambiguity
- supporting and conflicting evidence
- confirmatory tests
- fuller biomarker exploration

### Internal / admin mode
- pipeline status
- debug detail
- runtime diagnostics
- engineering object detail

### Final strategic rule
**HealthIQ should not surface everything the engine can compute.  
It should surface the smallest governed set of things that makes its deterministic, synthesised, traceable superiority obvious to the user.**
