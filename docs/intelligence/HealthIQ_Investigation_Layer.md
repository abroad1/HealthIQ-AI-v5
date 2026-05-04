
---

# HealthIQ Investigation Layer

State of the Architecture and Proposed Path Forward

## 1. Purpose of This Document

HealthIQ has reached a critical stage in its evolution.

The core deterministic analysis engine is now operational and capable of:

* canonical biomarker ingestion
* derived metric computation
* deterministic signal evaluation
* reproducible golden panel analysis
* InsightGraph synthesis

The next strategic step is to introduce an **Investigation Layer** capable of transforming abnormal biomarker findings into **mechanistic biological narratives**.

This document explains:

1. The current architecture
2. What the platform can already support
3. What it cannot yet support
4. The minimal architectural extension required
5. The recommended implementation path

This document proposes the introduction of an Investigation Layer within the HealthIQ architecture.

The investigation layer is intended to transform isolated biomarker abnormalities into structured physiological explanations by linking primary biomarkers with contextual biomarkers and known biological mechanisms.

The immediate objective of this document is not simply to describe the concept, but to enable the team to make a clear architectural decision.

Specifically, the team must determine whether the proposed investigation layer can be implemented using the existing signal architecture with a small extension, or whether a deeper architectural change is required before investigation signals are added to the knowledge bus.

To support this decision, this document provides:

a description of the proposed investigation layer

an example of a full biomarker investigation (homocysteine)

a proposed investigation signal template

a minimal architectural extension for carrying explanatory metadata

## Decision Requested

The team is asked to evaluate whether the proposed architecture is the correct foundation for implementing biomarker investigation signals within HealthIQ.

In particular, reviewers should determine:

Whether the existing SignalRegistry / SignalEvaluator architecture can support investigation signals without modifying the core evaluation engine.

Whether the proposed explanation metadata extension is the minimal and safest way to propagate biological reasoning through the pipeline.

Whether investigation signals should be implemented as extensions of the current signal package model, or whether they should be represented as a distinct knowledge object within the knowledge bus.

## Requested Reviewer Output

Reviewers are asked to return a structured response addressing the following.

Architectural Validation

Confirm whether the proposed investigation signal template can be supported by the current runtime architecture.

If not, identify the minimal architectural changes required.

Contract Review

Evaluate whether the proposed extension to the signal contract is sufficient for carrying biological explanation metadata through the pipeline.

If improvements are required, propose a revised schema.

Implementation Risk

Identify any risks to:

deterministic replay

golden panel stability

signal registry governance

signal package compatibility

Alternative Architecture

If a significantly better architectural approach exists, propose it and explain why it would be superior to the current proposal.

## Expected Outcome

Following review, the team should reach consensus on one of the following implementation paths:

Option A
Proceed with the proposed investigation signal template and minimal schema extension, and begin populating investigation signals.

Option B
Refine the investigation signal template before implementation.

Option C
Introduce a new architectural layer for investigation logic separate from the current signal architecture.

## Architectural Constraints That Must Not Be Broken

The following architectural properties of the HealthIQ platform are considered stable foundations and must not be compromised by the proposed Investigation Layer.

Reviewers should assume these constraints are non-negotiable design principles unless a compelling and clearly justified alternative is proposed.

Deterministic Signal Evaluation

Signal activation must remain deterministic.

Signal outcomes must be reproducible from identical input data and must not rely on probabilistic or non-deterministic reasoning.

The investigation layer must therefore operate on top of deterministic signal activation rather than replacing it.

## Golden Panel Replay Stability

Golden panel runs currently provide deterministic replay validation for the entire analysis pipeline.

Changes introduced by the investigation layer must preserve the ability to reproduce identical outputs when the same input panel is processed.

If additional metadata fields are introduced, their inclusion must not introduce non-deterministic output.

## Canonical Biomarker Pipeline

The canonical biomarker ingestion and derived metric computation pipeline is governed by the SSOT registry and must not be altered by the investigation layer.

Investigation signals must consume canonical biomarker values rather than introduce alternative computation pathways.

## Signal Registry Governance

Signal definitions are currently loaded from the Knowledge Bus packages and governed through the signal registry.

The investigation layer must integrate with this mechanism rather than introduce an alternative signal loading system.

Signal identifiers must remain globally unique and version-controlled through the existing registry framework.

## Separation of Detection and Explanation

The deterministic signal engine should remain responsible only for detecting biological signals.

The investigation layer should extend the explanatory context associated with signals rather than embed narrative logic directly inside the evaluation engine.

Maintaining this separation preserves architectural clarity and reduces the risk of signal logic becoming entangled with narrative generation.

## Minimal Architectural Change Principle

The preferred solution is the one that introduces the smallest possible change to the current architecture while enabling the investigation layer.

Reviewers should prioritize solutions that:

extend the existing signal contract

preserve deterministic evaluation

avoid introducing new runtime subsystems unless absolutely necessary.

## Reviewer Context

Reviewers (Claude and Cursor) have full access to the HealthIQ codebase and should use the repository to validate the feasibility of the proposed architecture.

Responses should reference specific code locations where relevant.

---

# 2. The Strategic Goal

HealthIQ must move beyond identifying abnormal biomarkers and begin explaining **why they may be abnormal and what they imply biologically**.

For example:

Input (raw biomarker findings)

Homocysteine ↑
Transferrin ↓
Vitamin B12 borderline

Traditional blood report interpretation:

* Elevated homocysteine

HealthIQ target interpretation:

Evidence of impaired methylation metabolism possibly linked to B-vitamin insufficiency and reduced nutrient transport capacity. Elevated homocysteine may contribute to endothelial oxidative stress and vascular inflammation.

This type of synthesis is what differentiates HealthIQ from:

* simple biomarker dashboards
* lab range flagging systems
* generic LLM explanations

To achieve this consistently, the platform must support **biomarker-anchored investigation signals**.

---

# 3. Current Signal Architecture

The HealthIQ signal engine currently operates through a deterministic pipeline.

### Signal Definition

Signals are defined in:

```
knowledge_bus/packages/*/signal_library.yaml
```

Each signal defines:

* primary_metric
* thresholds
* optional override_rules
* supporting markers

### Runtime Evaluation

The runtime components include:

SignalRegistry
SignalEvaluator
SignalResult
InsightGraphBuilder

Signals are evaluated deterministically based on:

```
primary_metric
thresholds
override_rules
```

Signal outputs include:

* signal_id
* system
* signal_state
* signal_value
* primary_metric
* supporting_markers

These outputs are injected into:

```
insight_graph.signal_results
```

### Determinism

The architecture already guarantees:

* deterministic evaluation
* reproducible golden panel results
* stable registry hashes

This deterministic design is a major strength and must be preserved.

---

# 4. What the Current System Already Supports

The audit confirms the following capabilities already exist.

### Primary biomarker anchoring

Signals can already be anchored to a single abnormal biomarker:

```
primary_metric: homocysteine
```

### Contextual marker branching

Supporting biomarkers can influence signal state through:

```
override_rules.conditions
```

This means signals can already encode patterns like:

```
homocysteine high
+ B12 low
+ folate low
```

### Supporting marker attachment

Signals can return contextual markers via:

```
output.supporting_markers
```

### Deterministic downstream carriage

Signal results are serialized into InsightGraph and captured in golden panel artifacts.

This means investigation signals will automatically integrate into the platform's deterministic analysis pipeline.

---

# 5. What the Current System Cannot Yet Support

The audit identifies one important limitation.

The system currently cannot carry **structured explanatory knowledge**.

Specifically, the runtime does not preserve fields for:

* biological mechanism descriptions
* causal explanations
* clinical implications
* narrative guidance

Even though the schema allows many descriptive fields, the evaluator ignores them and the output model (`SignalResult`) does not carry them forward.

As a result, the platform can currently detect signals but cannot yet provide the deeper interpretation layer needed for HealthIQ’s intended product experience.

---

# 6. The Investigation Layer Concept

The Investigation Layer sits above the current signal detection logic.

Its purpose is to transform abnormal biomarkers into structured biological explanations.

Conceptually:

```
abnormal biomarker
↓
signal activation
↓
supporting biomarker context
↓
biological mechanism explanation
↓
human-readable narrative
```

Example signal:

```
signal_homocysteine_elevation_context
```

Primary trigger:

```
homocysteine
```

Supporting markers:

```
vitamin_b12
folate
transferrin
mcv
crp
```

Mechanistic interpretation:

* impaired methylation cycle
* B-vitamin insufficiency
* endothelial oxidative stress

This signal produces a coherent biological explanation rather than a simple abnormal result.

---

# 7. Minimum Viable Architectural Extension

The audit correctly concludes that only a **small extension** is required.

The evaluator logic does **not** need to change.

Instead we need a structured way to carry explanatory metadata through the pipeline.

### Proposed addition to the signal contract

Add an optional section to signal definitions:

```
explanation:
  mechanism: >
    Biological pathway explanation.

  interpretation:
    High homocysteine may indicate impaired methylation
    and reduced B-vitamin availability.

  implications:
    Potential endothelial dysfunction and vascular stress.

  supporting_marker_roles:
    vitamin_b12: methylation cofactor
    folate: methyl donor availability
    transferrin: nutrient transport capacity
```

### Runtime propagation

This metadata should be attached to the output structure:

```
SignalResult
```

and passed through to:

```
insight_graph.signal_results
```

No change is required to the deterministic evaluation logic.

The engine still evaluates signals the same way.

The only change is that explanatory metadata becomes **first-class output**.

---

# 8. Why This Extension Is Safe

This extension is safe because it does not alter:

* signal activation logic
* derived metric calculations
* SSOT scoring
* replay determinism

It only enriches the output payload.

Replay hashes will naturally change once the metadata appears in the output, but that change will be deterministic.

---

# 9. Implementation Path

The recommended path is deliberately incremental.

### Phase 1 — schema extension

Add structured explanatory fields to the signal package contract.

### Phase 2 — output propagation

Extend `SignalResult` and InsightGraph serialization to preserve explanation metadata.

### Phase 3 — pilot investigation signals

Create the first investigation signals:

* homocysteine context
* ferritin context
* CRP context
* ALT context
* HbA1c context

These signals will validate the architecture.

### Phase 4 — knowledge expansion

Once validated, expand to a broader set of biomarker-anchored investigation signals.

---

# 10. Strategic Importance

This layer is where HealthIQ’s real intellectual property will emerge.

Many companies can:

* display biomarker charts
* flag abnormal values
* generate generic explanations

Very few systems can **deterministically synthesize physiological insight from complex biomarker interactions**.

The Investigation Layer transforms HealthIQ from a lab report viewer into a **biological interpretation engine**.

---

# 11. Final Conclusion

The audit result is clear.

HealthIQ already has the core architecture necessary to support biomarker-led investigation signals.

However, the platform currently lacks a structured way to carry explanatory biological knowledge through the runtime pipeline.

The required change is small:

A minimal extension to the signal contract and output model to propagate explanation metadata.

Once this is implemented, the system can begin populating investigation signals that convert abnormal biomarkers into meaningful biological narratives.

---

Below is the **Addendum Example** you requested. It is written as if it will be appended to the Investigation Layer document and circulated internally. It demonstrates the **depth of causal reasoning** the system should ultimately be able to represent and synthesize from the biomarker network.

---

# Addendum A

## Reference Investigation Model

### Homocysteine Elevation — Mechanistic Context Analysis

This addendum provides a concrete example of the level of biological reasoning the HealthIQ Investigation Layer is designed to capture.

The goal of the investigation layer is not simply to identify abnormal biomarkers, but to interpret **why those abnormalities may be occurring and what physiological systems may be implicated**.

Homocysteine provides a useful reference example because it sits at the intersection of several major metabolic systems.

These include:

* methylation metabolism
* B-vitamin availability
* nutrient transport
* oxidative stress
* endothelial function
* vascular inflammation

An elevation in homocysteine rarely exists in isolation and is typically the result of disruption within one or more of these systems.

The investigation model therefore treats homocysteine as a **primary signal anchor** and then evaluates contextual biomarkers to determine the most plausible physiological explanation.

---

# 1. Primary Biomarker

Primary marker

Homocysteine

Example value

```
Homocysteine: 16.23 μmol/L
Reference range: 3.7 – 13.9 μmol/L
```

This represents a moderate elevation above the laboratory reference range and suggests **hyperhomocysteinemia**.

Elevated homocysteine is clinically associated with:

* impaired methylation metabolism
* endothelial oxidative stress
* increased cardiovascular risk
* reduced nitric oxide signalling
* increased inflammatory signalling

However, homocysteine elevation itself does not identify the root cause. Investigation must therefore proceed through the metabolic pathways that regulate homocysteine concentration.

---

# 2. Core Biochemical Pathway

Homocysteine sits within the **one-carbon metabolism cycle**, also known as the methylation cycle.

The core pathway operates as follows:

```
Methionine
↓
S-adenosylmethionine (SAM)
↓
S-adenosylhomocysteine
↓
Homocysteine
```

Homocysteine can then follow two main metabolic fates:

### Remethylation pathway

Homocysteine is converted back into methionine.

This requires:

* vitamin B12
* folate (5-methyl tetrahydrofolate)

This reaction is catalyzed by the enzyme:

Methionine synthase

### Transsulfuration pathway

Homocysteine is converted into cystathionine and eventually cysteine.

This requires:

* vitamin B6

This reaction is catalyzed by:

Cystathionine β-synthase

When either of these pathways becomes inefficient, homocysteine begins to accumulate in the bloodstream.

---

# 3. Supporting Biomarker Context

To understand the origin of elevated homocysteine, the investigation layer examines several contextual biomarkers.

These markers help distinguish between possible biological explanations.

Relevant contextual markers include:

Vitamin B12
Folate
Transferrin
MCV
CRP

Each of these markers provides clues about the underlying metabolic environment.

---

# 4. B-Vitamin Availability

Vitamin B12

Example result:

```
Vitamin B12: 336 pg/mL
Reference range: 211 – 911 pg/mL
```

Although this value lies within the laboratory reference range, it sits in the **lower portion of the distribution**.

In clinical practice, homocysteine elevation is often one of the earliest indicators of **functional B12 insufficiency**.

Functional insufficiency occurs when B12 availability is not adequate for optimal methylation activity, even though serum concentrations remain within conventional laboratory limits.

When B12 availability is suboptimal, methionine synthase activity slows, preventing efficient remethylation of homocysteine back into methionine.

This causes homocysteine to accumulate.

---

# 5. Nutrient Transport Capacity

Transferrin

Example result

```
Transferrin: 2.00 g/L
Reference range: 2.15 – 3.65 g/L
```

Transferrin is primarily known for its role in iron transport.

However, transferrin also functions as a broader indicator of **nutrient transport capacity and hepatic protein synthesis**.

Low transferrin may suggest:

* reduced hepatic protein production
* altered nutrient transport capacity
* chronic inflammatory signalling

Reduced nutrient transport capacity may impair the availability of micronutrients required for metabolic reactions, including B-vitamins involved in methylation.

In this context, low transferrin may therefore represent an indirect contributor to impaired homocysteine metabolism.

---

# 6. Red Blood Cell Indices

Mean Corpuscular Volume (MCV)

Although not elevated in this specific example, MCV is often examined when homocysteine is high.

Elevated MCV can indicate:

* B12 deficiency
* folate deficiency
* impaired DNA synthesis during erythropoiesis

If MCV were elevated alongside homocysteine, this would strengthen the hypothesis of **B-vitamin-driven methylation disruption**.

---

# 7. Inflammatory Context

C-reactive protein (CRP)

CRP provides information about systemic inflammatory activity.

Inflammation is relevant to homocysteine metabolism for several reasons.

Inflammatory signalling can:

* increase oxidative stress
* impair endothelial nitric oxide signalling
* alter hepatic protein synthesis
* reduce micronutrient transport capacity

If CRP is elevated, homocysteine elevation may be partially driven by **inflammatory metabolic stress** rather than purely micronutrient insufficiency.

---

# 8. Vascular and Endothelial Effects

Elevated homocysteine can influence vascular health through several mechanisms.

### Oxidative stress

Homocysteine promotes the formation of reactive oxygen species (ROS), which damage endothelial cells lining the blood vessels.

### Nitric oxide suppression

Nitric oxide is required for normal vascular relaxation.

Homocysteine interferes with nitric oxide signalling, potentially contributing to endothelial dysfunction.

### Protein homocysteinylation

Homocysteine can bind to proteins, altering their structure and impairing their biological function.

This process may contribute to structural changes within the vascular wall.

### Smooth muscle proliferation

Homocysteine can stimulate proliferation of vascular smooth muscle cells, contributing to plaque formation.

These mechanisms help explain why elevated homocysteine has historically been associated with cardiovascular risk.

---

# 9. System-Level Interpretation

When evaluated together, the following biomarker pattern emerges:

```
Homocysteine: elevated
Vitamin B12: borderline
Transferrin: low
```

This pattern is consistent with a physiological state characterized by:

* reduced methylation efficiency
* marginal B-vitamin availability
* reduced nutrient transport capacity

The combined effect of these factors may impair homocysteine metabolism, leading to its accumulation.

Persistently elevated homocysteine may contribute to endothelial oxidative stress and vascular inflammation if not corrected.

---

# 10. Investigation Layer Role

The HealthIQ Investigation Layer uses this type of reasoning to transform isolated biomarker findings into **mechanistic biological narratives**.

Instead of simply reporting:

```
Homocysteine: high
```

the system produces a structured explanation:

Elevated homocysteine may indicate reduced methylation efficiency, potentially influenced by marginal B-vitamin availability and reduced nutrient transport capacity. Elevated homocysteine can contribute to oxidative stress within vascular endothelial cells and may increase inflammatory signalling if persistent.

This synthesis provides users with a far clearer understanding of what their biomarker pattern may represent biologically.

---

# 11. Implications for Signal Design

This example demonstrates how a single biomarker-anchored investigation signal should be structured.

The signal must capture:

Primary trigger

```
homocysteine
```

Supporting context markers

```
vitamin_b12
folate
transferrin
mcv
crp
```

Mechanistic explanation

* impaired methylation cycle
* B-vitamin insufficiency
* oxidative endothelial stress

System implications

* vascular signalling
* inflammation
* nutrient metabolism

This structure allows the system to produce coherent explanations while maintaining deterministic signal activation logic.

---

# 12. Strategic Significance

This level of contextual biological reasoning is central to the long-term vision of HealthIQ.

Most blood test platforms identify abnormal values.

HealthIQ is designed to identify **biological mechanisms**.

The Investigation Layer is therefore the component that transforms HealthIQ from a laboratory reporting tool into a **systems-level biological interpretation engine**.

---

If you want, the next step I would recommend is something that will massively accelerate the build:

we define a **standard Investigation Signal Template** so every biomarker investigation (homocysteine, ferritin, ALT, HbA1c, CRP, etc.) follows exactly the same structure in the knowledge bus. That will make the next 50 investigation signals far easier to generate consistently.
# Addendum B

## Proposed Architectural Solution

### Investigation Signal Template and Knowledge Encoding Framework

This addendum proposes the architectural mechanism that will allow the HealthIQ platform to consistently encode, evaluate, and interpret biomarker-driven investigations at scale.

The goal is to enable the platform to move from isolated biomarker interpretation toward **structured physiological investigation**, while preserving the deterministic architecture that currently underpins the analysis engine.

---

# 1. Architectural Objective

The HealthIQ Investigation Layer must support the following capability:

When a biomarker exceeds its expected physiological range, the system should:

1. Detect the abnormal biomarker deterministically
2. Evaluate contextual biomarkers that influence interpretation
3. Identify plausible biological mechanisms
4. Generate a structured explanation of what may be occurring physiologically

To achieve this reliably, investigation logic must be encoded using a **consistent and repeatable knowledge structure**.

Without such a structure, signal definitions would become inconsistent and difficult to maintain as the knowledge base grows.

The proposed solution is the introduction of a **standard Investigation Signal Template**.

---

# 2. Concept of an Investigation Signal

An investigation signal differs from existing system-state signals.

Current signals answer questions such as:

* Is there systemic inflammation?
* Is there lipid transport dysfunction?

Investigation signals instead answer:

* Why might this biomarker be abnormal?
* What biological systems may be responsible?
* What secondary biomarkers help explain the abnormality?

An investigation signal therefore has three conceptual components.

Primary biomarker trigger
Contextual biomarkers
Mechanistic explanation

Conceptually:

```
abnormal biomarker
↓
investigation signal
↓
context biomarker evaluation
↓
mechanistic explanation
```

This structure allows the system to transform abnormal laboratory values into biologically meaningful interpretations.

---

# 3. Investigation Signal Template

To ensure consistency across the platform, every investigation signal should follow the same structural template.

The template is divided into two major sections:

Detection Logic
Investigation Knowledge

Detection logic controls when the signal activates.

Investigation knowledge defines the biological reasoning associated with that signal.

---

# 4. Detection Logic Structure

Detection logic remains fully deterministic and compatible with the existing signal evaluator.

The following fields are required.

```
signal_id
system
primary_metric
thresholds
override_rules
output.supporting_markers
```

Primary metric

The biomarker that triggers the investigation.

Example:

```
primary_metric: homocysteine
```

Thresholds

Define when the investigation becomes relevant.

Example:

```
thresholds:
  - level: suboptimal
    operator: ">"
    value: 14
```

Override rules

Allow supporting markers to influence signal interpretation.

Example:

```
override_rules:
  - conditions:
      vitamin_b12: "< 350"
    resulting_state: at_risk
```

Supporting markers

Markers that help contextualize the investigation.

```
output:
  supporting_markers:
    - vitamin_b12
    - folate
    - transferrin
    - mcv
    - crp
```

---

# 5. Investigation Knowledge Structure

Detection logic identifies the signal.

Investigation knowledge explains **why the signal matters biologically**.

The proposed template introduces a structured explanation block.

```
explanation:
  mechanism
  biological_pathway
  interpretation
  implications
  supporting_marker_roles
```

Each section captures a different aspect of the investigation logic.

---

## Mechanism

Describes the physiological mechanism linking the biomarker to biological processes.

Example:

Elevated homocysteine indicates disruption of one-carbon metabolism, which regulates methylation reactions across the body.

---

## Biological pathway

Documents the metabolic pathway responsible for the biomarker.

Example:

Homocysteine is produced during methionine metabolism and can be recycled through remethylation or converted through the transsulfuration pathway.

---

## Interpretation

Provides the high-level meaning of the signal.

Example:

Elevated homocysteine may indicate impaired methylation metabolism or reduced availability of B-vitamin cofactors.

---

## Implications

Describes potential physiological consequences.

Example:

Persistently elevated homocysteine can contribute to endothelial oxidative stress, impaired nitric oxide signaling, and vascular inflammation.

---

## Supporting marker roles

Defines how contextual biomarkers influence interpretation.

Example:

```
supporting_marker_roles:
  vitamin_b12: required for homocysteine remethylation
  folate: methyl donor for methionine regeneration
  transferrin: indicator of nutrient transport capacity
  crp: inflammatory context influencing endothelial stress
```

This structure allows the investigation engine to link biomarkers to biological meaning in a systematic way.

---

# 6. Runtime Integration

The investigation signal template integrates with the existing pipeline as follows.

Signal evaluation remains unchanged.

The evaluator continues to compute:

```
SignalResult
```

The result is then extended with explanatory metadata.

```
SignalResult
  signal_id
  signal_state
  primary_metric
  signal_value
  supporting_markers
  explanation
```

The explanation block is serialized into:

```
insight_graph.signal_results
```

This allows the narrative layer of the platform to generate structured interpretations without altering the deterministic signal engine.

---

# 7. Knowledge Bus Organization

Each investigation signal should live within its own knowledge package.

Example:

```
knowledge_bus/packages/pkg_homocysteine_context/
```

Package structure:

```
pkg_homocysteine_context
  signal_library.yaml
  evidence.md
  clinical_signoff.md
```

signal_library.yaml contains the investigation template.

evidence.md documents supporting literature.

clinical_signoff.md records expert review and governance approval.

This structure preserves scientific transparency and traceability.

---

# 8. Example Signals Enabled by This Architecture

Once the investigation template exists, the system can easily encode additional biomarker investigations.

Examples include:

Homocysteine investigation
Ferritin investigation
CRP investigation
ALT investigation
HbA1c investigation
TSH investigation
Triglyceride investigation
Uric acid investigation
Vitamin D investigation

Each investigation signal follows the same template while referencing different biological pathways.

---

# 9. Advantages of the Template Approach

The investigation signal template provides several major benefits.

Consistency

Every investigation follows the same knowledge structure.

Scalability

Dozens or hundreds of biomarker investigations can be added without architectural drift.

Scientific transparency

Biological reasoning is explicitly documented rather than hidden inside narrative text.

Separation of concerns

The signal engine remains deterministic while biological knowledge evolves independently.

Future extensibility

The same template can support more advanced reasoning engines, including mechanistic modeling or probabilistic inference layers.

---

# 10. Long-Term Knowledge Architecture

Over time the investigation layer will form a **structured knowledge network** linking biomarkers, pathways, and physiological systems.

Conceptually:

```
biomarkers
↓
investigation signals
↓
biological pathways
↓
physiological systems
↓
clinical implications
```

This knowledge network will ultimately allow HealthIQ to provide highly sophisticated biological insight from routine blood tests.

---

# 11. Implementation Recommendation

The recommended next step is to implement the investigation signal template and then create the first pilot investigation signals.

Initial candidates include:

Homocysteine
Ferritin
CRP
ALT
HbA1c

These biomarkers frequently trigger follow-up investigations in clinical practice and will provide strong validation for the investigation architecture.

---

# 12. Conclusion

The investigation signal template provides a scalable method for encoding biological reasoning within the HealthIQ platform.

It allows abnormal biomarkers to be interpreted within their metabolic context, transforming raw laboratory data into coherent physiological insight.

By separating deterministic signal detection from biological explanation, the platform can preserve architectural stability while continuously expanding its scientific knowledge base.

This architecture will enable HealthIQ to build a comprehensive investigation framework capable of interpreting the complex biological relationships present in human blood chemistry.
