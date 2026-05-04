# HealthIQ FE-VISUALISATION — Surface Policy
*Final draft for strategic sign-off*

## 1. Purpose of this paper

This paper sets out the proposed **surface policy** for FE-VISUALISATION.

Its purpose is not to decide final UI polish, styling, or page layout.
Its purpose is to decide, at product-strategy level:

- what HealthIQ should surface to standard users
- what should be reserved for advanced or clinician views
- what should remain internal
- how the four FE-VISUALISATION components should function as product surfaces

FE-VISUALISATION is not a cosmetic frontend sprint.
It is the point where deterministic engine output becomes user-facing product reality.

If this is not decided explicitly, implementation will make hidden product decisions by default.

---

## 2. Strategic context

HealthIQ is no longer just building analytical capability.
It is now deciding how that capability appears as a product.

Recent delivery has increased the importance of this decision because the platform now has:

- structured interpretation
- policy-backed primary concern handling
- ranked ambiguity foundations
- clinician-facing contract improvements
- persistence foundations in progress
- growing distance between what the engine can compute and what should be shown to a user

That means the FE-VISUALISATION decision is not about “which widgets look good.”
It is about product truth.

The product now needs to decide:

> What is the smallest governed set of things that should be surfaced to users in order to make HealthIQ feel clearly more intelligent, more trustworthy, and more useful than a generic blood-report viewer?

---

## 3. Strategic conclusion

The recommended strategic decision is:

**HealthIQ should not surface everything the engine can compute.  
It should surface the smallest governed set of things that makes its deterministic, synthesised, traceable superiority obvious to the user.**

This means:

- the standard user surface should lead with interpretation, not internals
- the product should use a tiered disclosure model
- InsightPanel should be the hero component
- ClusterCard should be the translated systems-thinking surface
- BiomarkerChart should support trust and context, not dominate the product
- PipelineStatus should not appear as raw pipeline plumbing on the retail surface
- a secondary educational biological-system explainer layer is worth pursuing for retail users, provided it is clearly educational and never presented as personalised proof

---

## 4. Surface philosophy

## 4.1 Standard user surface

The standard user surface should answer four questions:

1. What matters most?
2. What body system or pattern does it belong to?
3. Which markers are driving that picture?
4. What should I do next, and how confident is this interpretation?

This surface should feel:

- clear
- biologically intelligent
- calm but not weak
- more meaningful than a lab report
- more trustworthy than a generic AI explainer

The standard surface must not feel like:
- a data dump
- an engineering dashboard
- a chart-first commodity blood app

---

## 4.2 Advanced / clinician surface

The advanced or clinician-facing surface should allow more depth without corrupting the standard experience.

It should allow explicit access to:

- ranked ambiguity
- supporting vs conflicting evidence
- confirmatory tests
- richer biomarker detail
- more explicit confidence boundaries
- stronger explanation of why one interpretation is foregrounded over another

This surface should deepen understanding, not simply expose raw internal objects.

---

## 4.3 Internal / debug surface

Internal/debug surfaces should remain outside the standard product unless explicitly translated.

These may include:

- raw pipeline stages
- runtime/debug state
- parser diagnostics
- engineering object detail
- internal IDs and intermediate representations

These may be useful operationally, but they are not product surfaces by default.

---

## 5. Governance decision by component

## 5.1 InsightPanel

### Purpose
InsightPanel is the **hero component**.

It is the main structured interpretation surface and the clearest commercial proof that HealthIQ is more than a biomarker dashboard.

### What it should do in standard mode
It should surface:

- one lead concern
- a concise explanation of why it matters
- body-system context
- next-step logic
- confidence/uncertainty in simple, non-technical language where relevant

### Important policy condition
A lead concern in standard mode must **not** imply false singular certainty.

Where ambiguity exists, InsightPanel may still lead with one concern, but it should make clear that:
- this is the lead interpretation under the governed policy
- alternative plausible interpretations may still exist where the evidence is incomplete

It must not silently behave as though “one lead concern” means “single proven truth.”

### What it may show in advanced/clinician mode
- ranked ambiguity
- supporting and conflicting evidence
- confirmatory tests
- more explicit differential framing

### Governance decision
InsightPanel should be treated as the **primary product surface** in FE-VISUALISATION.

**If InsightPanel is weak, the product feels weak.  
If InsightPanel is strong, HealthIQ immediately feels more sophisticated than a generic report viewer.**

---

## 5.2 ClusterCard

### Purpose
ClusterCard is the **translated systems-thinking surface**.

This is where HealthIQ shows that it understands system-level or pattern-level meaning rather than only isolated lab values.

### What it should show in standard mode
- translated body-system or pattern name
- interpreted state or severity
- top contributing markers/signals
- short explanation of why that system matters now

### What it must not show
- raw cluster IDs
- internal grouping labels
- untranslated engineering objects
- implementation-native grouping artefacts

### Governance decision
ClusterCard should be a **translated biological system card**, not a frontend wrapper around internal cluster computation.

This is one of the strongest visible proof points of HealthIQ’s differentiation.

---

## 5.3 BiomarkerChart

### Purpose
BiomarkerChart is the **atomic trust component**.

It is the user’s clearest visual anchor for a single marker in context.

### What it should show in standard mode
- biomarker name
- raw value and unit
- lab-specific range position
- interpreted state
- whether this marker materially contributes to a broader body-system pattern
- a brief explainer of what the marker is responsible for in plain biological language

### Important language rule
For standard users, this component should talk in terms of:
- body systems
- biological processes
- what the marker does

It should avoid relying on the word **phenotype** as a default user-facing term unless it is clearly translated or taught.

### What it should not show by default
- backend field names
- implementation metadata
- raw engine-specific technical outputs
- large amounts of low-value detail

### Governance decision
BiomarkerChart is important, but it is a **supporting component**, not the hero.

It should help the user trust and understand the result, not define the whole product experience.

---

## 5.4 PipelineStatus / Confidence Layer

### Purpose
This should **not** be a raw engineering-status widget on the retail surface.

For user-facing purposes, this should function as a **translated confidence and data-quality layer**.

### What it should show in standard mode
- analysis complete
- plain-language data-quality limitations
- confidence reduced by missing markers, missing context, or partial range quality
- what additional tests or data would improve confidence

### What should remain internal
- raw pipeline stages
- runtime logs
- parser/debug diagnostics
- engineering state objects

### Governance decision
The user-facing version of this component should be treated as a **translation layer**, not a repackaged pipeline monitor.

Its job is to help the user understand how confident the platform is in the interpretation, not how the software happened to execute.

---

## 6. Surface priority order

If sequencing trade-offs are needed, the recommended priority order is:

1. InsightPanel
2. ClusterCard
3. BiomarkerChart
4. Translated confidence/data-quality layer
5. Internal/admin pipeline tooling later or internal-only

This order reflects what most directly demonstrates HealthIQ’s strategic value.

---

## 7. Educational biological-system explainer layer

## 7.1 Why this is strategically valuable

A meaningful opportunity exists for a **secondary educational layer** for retail users.

Its purpose would be to help users understand:

- how a body system works
- how relevant biomarkers interact
- why apparently small marker shifts can matter in a wider system
- why HealthIQ is surfacing a particular system as important

The value of this layer is not diagnostic precision.
Its value is educational impact and perceived depth:

> “I finally understand how this part of my body works.”

That is potentially a strong differentiator.

---

## 7.2 What this layer is

This layer should be:

- educational
- reusable
- system-level
- clearly separate from personalised interpretation

It should sit behind or beneath the primary personalised interpretation, not replace it.

---

## 7.3 What it may do

It may:
- explain how a body system works
- explain which biomarkers commonly belong to that system
- explain how those biomarkers interact
- explain why breakdown in that system can matter for broader health

---

## 7.4 What it must never imply

It must never imply:
- that the full system story is proven in the user
- that every marker in the educational narrative is abnormal in that user
- that a partial panel proves a complete mechanistic story
- that this educational explainer is a diagnosis

---

## 7.5 Recommended positioning

This layer should be framed as:
- “Understanding this system”
- “How this pathway works”
- “Why these markers matter together”
- “What can happen when this system is under strain”

It should not be framed as:
- “This is exactly what is happening in your body”

### Governance decision
HealthIQ should pursue this as a **secondary educational narrative layer**, not as the lead interpretation surface.

It is a differentiator, not the main claim.

---

## 8. What the product must never imply

The surfaced product must never imply:

- diagnosis
- certainty beyond the evidence
- that all computed signals are equally important
- that polished charts equal meaningful interpretation
- that a compelling body-system story is the same as personalised proof
- that internal engine completeness equals user usefulness

These are non-negotiable boundaries.

---

## 9. Why this surface policy is recommended

## 9.1 It protects strategic differentiation
HealthIQ should not collapse into a chart-first blood app.
This policy makes system-level interpretation, structured synthesis, and confidence handling visible.

## 9.2 It protects trust
By separating standard, advanced, and internal surfaces, it reduces noise and prevents leakage of technical artefacts.

## 9.3 It protects honesty
By separating the educational body-system explainer from personalised interpretation, it preserves the difference between explanation and evidence.

## 9.4 It improves user experience
The standard user sees the smallest high-value set of things that make the product feel intelligent and useful, rather than an overwhelming wall of widgets.

## 9.5 It supports growth
This policy leaves room for:
- advanced mode
- clinician mode
- enterprise/internal tooling
- richer educational or longitudinal layers later

---

## 10. Final recommendation

Approve the following as HealthIQ’s working FE-VISUALISATION surface policy:

### Standard mode
- InsightPanel as hero
- ClusterCard as translated body-system summary
- BiomarkerChart only for priority markers
- translated confidence/data-quality context
- optional secondary educational body-system explainer

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
