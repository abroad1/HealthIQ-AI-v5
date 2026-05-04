# HealthIQ AI
## Strategic Architecture Paper
### The Signal Architecture Pivot

Version: Draft v1.0  
Related Documents: Master PRD v5.2, Delivery Sprint Plan v5.2, Automation Bus SOP v1.2

---

# 1. Executive Summary

HealthIQ AI is currently transitioning from an early analytical system based primarily on biomarker scoring into a deterministic biological intelligence platform.

The architectural pivot proposed in this paper is that **biological signals must become the primary analytical unit of the HealthIQ platform rather than individual biomarkers.**

This shift converts the platform from a blood report explanation tool into a scalable biological reasoning engine.

Signals represent physiological states derived from structured biomarker patterns. Instead of interpreting biomarkers independently, the system detects biological conditions such as:

- insulin resistance
- hepatic stress
- chronic inflammation
- methylation stress
- atherogenic lipoprotein burden

These signals become the deterministic intelligence layer of the system.

The signal library therefore becomes the central intellectual property of the HealthIQ platform.

---

# 2. Current Platform State

The existing platform represents a transitional architecture.

Current runtime behaviour can be simplified as:

API → Normalizer → Scoring Engine → Clustering Engine → Insight Generation

This pipeline produces biomarker scoring combined with narrative explanations.

While this provides useful outputs, it does not yet fully realise the deterministic architecture defined in the Master PRD.

The PRD defines a three-layer system:

Layer A: Canonical data ingestion

Layer B: Deterministic biological intelligence

Layer C: Narrative translation

At present, analytical reasoning is partially distributed between scoring logic and insight modules.

The pivot proposed in this document consolidates all biological reasoning into Layer B via a deterministic signal detection architecture.

---

# 3. The Strategic Architecture Pivot

## Signals as the Core Analytical Primitive

Traditional blood analysis software treats biomarkers as the primary analytical objects.

HealthIQ should instead treat **biological signals** as the core analytical primitive.

A signal represents a physiologically meaningful state detected through deterministic biomarker patterns.

Example:

Signal: insulin_resistance

Primary metric:
- tyg_index

Supporting metrics:
- fasting_glucose
- fasting_insulin
- triglycerides
- hdl

The system therefore detects the signal "insulin resistance" rather than reporting individual marker deviations.

This allows the platform to reason about physiology rather than laboratory numbers.

---

# 4. Architectural Benefits

## 4.1 System-Level Reasoning

Signals enable the platform to reason about biological systems rather than isolated markers.

Multiple signals can interact to produce higher-order physiological interpretations.

Example:

insulin_resistance + hepatic_stress → metabolic syndrome precursor state

---

## 4.2 Research Integration

Signals provide a structured mechanism for incorporating biomedical research.

New research findings can be converted into new signals or refinements of existing signals.

This enables the platform to evolve continuously as new research emerges.

---

## 4.3 Intellectual Property

A large curated library of physiological signal definitions becomes a defensible intellectual asset.

Competitors can replicate biomarker explanations, but replicating a comprehensive signal detection library is significantly more difficult.

---

# 5. Signal Architecture Model

Signals must follow a deterministic contract.

Each signal must define:

- signal_id
- primary_metric
- supporting_metrics
- activation_rules
- override_rules
- research_sources

Signals must never rely on probabilistic reasoning or weighted heuristics.

Activation must always be traceable to deterministic logic.

---

# 6. Multi-Layer Signal Architecture

The platform will eventually support three signal layers.

## Layer 1: Primary Physiological Signals

Examples:

- insulin_resistance
- hepatic_stress
- vascular_inflammation
- methylation_stress

These represent direct physiological states.

---

## Layer 2: Composite Signals

Composite signals detect higher-order patterns formed by multiple primary signals.

Example:

cardiometabolic_acceleration

Triggered by:

- insulin_resistance
- vascular_inflammation

---

## Layer 3: System Burden Signals

System burden signals represent the cumulative stress placed on major biological systems.

Examples:

- metabolic_system_burden
- cardiovascular_system_burden

These signals integrate outputs from multiple composite and primary signals.

---

# 7. Alignment with Master PRD v5.2

The signal architecture described in this paper directly supports the architecture defined in the Master PRD.

The PRD specifies that:

Layer A performs canonical data ingestion.

Layer B performs deterministic biological intelligence.

Layer C performs narrative translation.

The signal detection engine becomes the core component of Layer B.

This ensures that the LLM operates purely as a narrative translation layer rather than an analytical reasoning engine.

---

# 8. Integration with Sprint Plan v5.2

The current sprint plan already contains the major infrastructure work required to enable signal architecture.

Key sprints include:

Sprint 4
Derived Ratio Registry

Sprint 5
Ratio centralisation

Sprint 6
Cluster schema refactor

Sprint 7
InsightGraph contract

Sprint 8
InsightGraph freeze

Sprint 9
cluster_engine_v2 migration

These sprints collectively establish the deterministic analytical infrastructure required for signal detection.

---

# 9. Proposed Signal Architecture Implementation Sprints

Following completion of the current sprint roadmap, the following signal-specific sprints are proposed.

## Sprint S10
Signal Schema Contract

Define the canonical YAML schema for signal definitions.

---

## Sprint S11
Signal Engine

Implement the deterministic signal evaluation engine.

---

## Sprint S12
Signal Registry

Introduce a registry for loading signal definitions from the knowledge bus.

---

## Sprint S13
Signal Interaction Engine

Enable detection of composite signals from primary signals.

---

## Sprint S14
System Burden Integration

Integrate signal outputs into system burden models.

---

# 10. Role of the Knowledge Bus

The Knowledge Bus becomes the primary research ingestion pipeline.

Scientific research papers are converted into structured knowledge packages which generate signal definitions.

The platform therefore evolves through the continuous addition of new signals derived from biomedical research.

---

# 11. Strategic Outcome

Adopting signal architecture transforms HealthIQ from a reporting application into a biological intelligence platform.

This platform architecture can support multiple product categories including:

- consumer health applications
- clinical decision support tools
- longevity medicine platforms
- research analytics systems

The signal library becomes the core intellectual property of the platform.

---

# 12. Next Steps

1. Team review of the signal architecture proposal.
2. Validation against Master PRD v5.2.
3. Claude codebase audit to map current architecture to proposed signal components.
4. Definition of implementation work packages under Automation Bus SOP v1.2.

