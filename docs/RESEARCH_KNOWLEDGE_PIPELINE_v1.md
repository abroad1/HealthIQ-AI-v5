# HealthIQ Research Knowledge Pipeline Architecture v1

> **Pipeline position:** The Knowledge Bus provides the **Evidence stage** of the
> HealthIQ canonical reasoning pipeline: `Evidence → Signal → Insight`.
> Signal libraries convert research evidence into deterministic biological detectors.
> The Signal stage (Signal Evaluation Engine) consumes Knowledge Bus outputs.
> See `architecture/HEALTHIQ_REASONING_PIPELINE.md` for the full pipeline definition.

## Purpose

This document defines the complete pipeline by which biomedical research is translated into deterministic analytics logic within the HealthIQ platform.

The architecture separates scientific discovery from system implementation so that research evidence can be safely converted into governed, validated platform behaviour.

The pipeline ensures:

- clear scientific lineage
- deterministic system behaviour
- governance of clinical logic
- separation between research, knowledge modelling, validation, and runtime implementation

The pipeline consists of four phases:

1. Research Generation
2. Research Translation
3. Knowledge Validation
4. Runtime Implementation

Each phase has a clearly defined responsibility, input, output, and governing contract.

---

# Architectural Principles

## Determinism

All executable analytics logic must originate from structured knowledge artefacts validated through the Knowledge Bus.

No runtime logic should be introduced without a validated knowledge source.

## Evidence Lineage

Every signal implemented in the analytics engine must trace back to documented research evidence.

Signals must have:

- research origin
- documented thresholds
- clinical rationale
- reference citations

## Separation of Concerns

The pipeline deliberately separates responsibilities across phases:

| Phase | Responsibility |
|-----|-----|
| Research | Discover and document biomedical relationships |
| Translation | Convert research into structured knowledge assets |
| Validation | Enforce schema and platform governance |
| Implementation | Integrate validated knowledge into runtime analytics |

This prevents scientific exploration from directly modifying production logic.

## Governance

All runtime changes must pass through Automation Bus governance.

Knowledge assets alone cannot modify runtime behaviour until implemented through governed development.

---

# Pipeline Overview

```
Scientific Literature
        ↓
Research LLM / Human Research
        ↓
research_study_<topic>.md
        ↓
Claude Translation
        ↓
Knowledge Bus Package
        ↓
Knowledge Bus Validator
        ↓
Validated Knowledge Package
        ↓
Automation Bus Sprint
        ↓
Runtime Analytics Engine
```

---

# Phase A — Research Generation

## Objective

Capture biomedical research and clinical evidence related to biomarker systems, physiological signals, and derived health metrics.

This phase produces research documentation but does not produce system artefacts.

## Input

Scientific literature including:

- peer reviewed studies
- meta analyses
- cohort studies
- clinical guidelines

## Tooling

Research LLM or manual research process.

The research LLM may search external sources and summarise primary literature.

## Output

```
research_study_<topic>.md
```

Example:

```
research_study_lipid_transport_dysfunction.md
```

## Governing Contract

Research documents must follow a consistent markdown structure to ensure they can be translated reliably.

## Required Sections

Research markdown files must include:

- Signal or biological topic
- Clinical question
- Biological rationale
- Biomarker relationships
- Derived metric formulas
- Evidence thresholds
- Limitations
- Supporting references

## Important Rule

Research markdown files are **human readable scientific documents**, not system contracts.

They may include explanatory context, interpretation, and narrative description.

---

# Phase B — Research Translation

## Objective

Convert research documents into deterministic Knowledge Bus assets that describe system logic.

## Tool

Claude Code

Claude operates as the translation engine between research narrative and structured system knowledge.

## Input

```
research_study_<topic>.md
```

## Governing Contract

Claude Research-to-Knowledge Translation Specification v1

This specification defines exactly how research documents are converted into Knowledge Bus packages.

## Responsibilities

Claude must extract from the research document:

- signal definition
- biological claim
- required biomarkers
- optional biomarkers
- derived metrics
- calculation formulas
- evidence anchored thresholds
- clinical guardrails
- evidence strength
- known limitations

Claude must then construct Knowledge Bus assets that follow the platform schema.

## Translation Modes

### Confirmation Mode

Research validates an existing signal.

In this case Claude documents the evidence supporting the existing signal and does not create new signal logic.

Example:

Signal already exists in KBP-0001 and research confirms thresholds.

### Creation Mode

Research introduces a new physiological signal.

Claude generates a new Knowledge Bus package describing that signal.

## Output

Knowledge Bus package assets including:

```
package_manifest.yaml
signal_library.yaml
clinical_signoff.md
supporting documentation
```

These artefacts represent deterministic system knowledge.

---

# Phase C — Knowledge Validation

## Objective

Ensure knowledge assets conform to platform governance rules and schema contracts.

## Tool

Knowledge Bus validator

## Input

Knowledge Bus package generated during Phase B.

## Validation Scope

Validator checks include:

- YAML schema compliance
- required fields
- signal identity rules
- dependency structure
- threshold definitions
- naming conventions

The validator ensures that knowledge assets are structurally correct before implementation.

## Output

Validated Knowledge Bus package.

Example identifier:

```
KBP-0002
```

Packages that fail validation must be corrected before continuing.

---

# Phase D — Runtime Implementation

## Objective

Integrate validated knowledge into the HealthIQ analytics engine.

## Tool

Automation Bus

## Input

Validated Knowledge Bus package.

## Responsibilities

Runtime implementation may include:

- implementing derived metrics
- implementing signal activation logic
- connecting signals to feature bundles
- integrating signals into analytics pipelines

Example runtime components affected:

```
ratio_registry.py
insight_graph_builder.py
future derived_metric_registry.py
```

All runtime changes must be governed through Automation Bus sprint workflows.

## Governance

No runtime change may bypass Automation Bus governance.

Knowledge packages alone do not modify system behaviour until implemented.

---

# Relationship Between Knowledge Bus and Runtime Pipeline

The Knowledge Bus describes physiological signals and system logic.

The runtime analytics pipeline computes derived metrics and generates user insights.

The two systems must eventually be connected so that runtime analytics consume Knowledge Bus signal outputs.

Until that connection exists the Knowledge Bus acts as a governed knowledge specification layer.

---

# Unit Canonicalisation Principle

The platform operates using a canonical unit system defined by the SSOT layer.

All biomarker values are normalised to SI units internally.

Example:

- Glucose stored internally in mmol/L
- External mg/dL inputs converted during ingestion

Derived metric calculations must operate on canonical units.

If a published formula requires alternate units (for example mg/dL), the derived metric function may perform internal conversion before applying the formula.

The canonical SSOT values remain unchanged.

---

# Example Flow

Example pipeline for a metabolic signal study:

```
Research study created
        ↓
research_study_insulin_resistance.md
        ↓
Claude translation
        ↓
KBP-0002 knowledge package
        ↓
Knowledge Bus validation
        ↓
Automation Bus sprint
        ↓
Derived metric implemented
        ↓
Signal integrated into analytics pipeline
```

---

# Implementation Roadmap

Phase A

Research generation already operational.

Research markdown reports are currently produced.

Phase B

Next implementation focus.

Claude translation specification must be implemented to convert research markdown into Knowledge Bus packages.

Phase C

Knowledge Bus validator already exists and enforces package contracts.

Phase D

Runtime integration performed through Automation Bus sprints when knowledge packages require new analytics logic.

---

# Immediate Development Focus

The current development focus is Phase B.

Deliverable:

Claude Research-to-Knowledge Translation Specification v1

This specification will allow research markdown files to be translated into Knowledge Bus packages deterministically.

Once this translation layer works reliably the full pipeline becomes operational.

---

# Long Term Vision

The Research Knowledge Pipeline provides a scalable pathway for expanding HealthIQ's biological intelligence.

New research can be continuously translated into system knowledge while maintaining deterministic governance and traceable scientific lineage.

This architecture allows HealthIQ to grow its clinical reasoning capability without compromising system stability.

