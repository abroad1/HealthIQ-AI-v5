# HealthIQ Research Authoring Pipeline — Proposed Architecture

## Purpose

This document proposes a revised architecture for how biomedical research is converted into deterministic HealthIQ signal artefacts.

The goal is to remove the fragility encountered when attempting to force research LLMs to directly generate structured YAML packages.

Instead, the system separates **research synthesis**, **translation**, **validation**, and **implementation** into distinct responsibilities.

This approach aligns with the deterministic governance already used in the Knowledge Bus and Automation Bus.

---

# Problem Statement

Attempts to have a research LLM produce fully structured YAML packages for the Research Ingestion Bus have proven unreliable.

Observed behaviour:

- Research LLM outputs high‑quality narrative analysis
- When asked to emit strict schema‑compliant YAML, output quality collapses
- Generated packages are often incomplete, inconsistent, or fail schema validation

The root cause is that research LLMs are optimized for:

- literature synthesis
- explanation
- narrative reasoning

They are **not optimized for deterministic schema emission**.

Attempting to combine both responsibilities in a single step introduces instability.

---

# Design Principle

Each stage of the system should perform **one task only**.

The revised pipeline follows this separation:

| Stage | Responsibility |
|-----|-----|
| Research LLM | Deep literature synthesis |
| Claude Translation Layer | Convert research into structured signal specification |
| Knowledge Bus | Validate structured knowledge artefacts |
| Automation Bus | Generate implementation code |

This keeps the deterministic components separate from the generative components.

---

# Revised Research Pipeline

The proposed architecture is:

```
Research LLM
↓
research_study.md
↓
Claude Translation Layer
↓
Signal Translation Block
↓
Knowledge Bus Package
↓
Knowledge Bus Validator
↓
Layer B Signal Implementation
↓
Automation Bus Validation
```

The research stage produces **structured markdown**, not governed YAML.

Claude performs the structured translation step.

---

# Stage 1 — Research Generation

## Output Artifact

```
research_study.md
```

This document contains:

- biological rationale
- literature evidence
- cohort findings
- thresholds discussed in literature
- biomarker explanations
- intervention evidence
- limitations

The document is intentionally narrative but structured with consistent headings.

Example sections:

- Bundle Summary
- Clinical Rationale
- Evidence Base
- Biomarkers and Calculations
- Output Tier Logic
- Actionable Recommendations
- Limitations

This stage focuses **only on scientific accuracy and completeness**.

No attempt is made to emit system‑level YAML structures.

---

# Stage 2 — Claude Translation Layer

Claude Code reads the research markdown and converts it into a structured intermediate representation.

This representation is called the **Signal Translation Block**.

Claude derives the following fields from the research document:

- signal_id
- biological_claim
- required_biomarkers
- optional_biomarkers
- derived_metrics
- formula
- thresholds
- clinical_guardrails
- primary_sources
- evidence_strength
- known_limitations

The translation block becomes the deterministic bridge between research prose and system artefacts.

Example structure:

```
Signal Translation Block

signal_id:

biological_claim:

required_biomarkers:

optional_biomarkers:

derived_metrics:

formula:

thresholds:

clinical_guardrails:

primary_sources:

limitations:
```

Claude generates this block as a separate artefact.

---

# Stage 3 — Knowledge Bus Package Generation

Once the translation block is produced, Claude generates the required Knowledge Bus artefacts.

These may include:

- knowledge package YAML
- signal specification
- derived metric definitions

These artefacts must conform to the Knowledge Bus schema.

---

# Stage 4 — Knowledge Bus Validation

The Knowledge Bus validator verifies:

- schema compliance
- biomarker references exist in SSOT
- derived metrics exist in the metric registry
- thresholds follow identifier rules

Failures are rejected before any implementation occurs.

---

# Stage 5 — Signal Implementation

Once validated, the Automation Bus generates the Layer B signal implementation.

This step converts the structured specification into executable logic.

---

# Advantages of the Proposed Architecture

## Stability

Research LLMs are allowed to focus on research rather than schema generation.

## Determinism

All structured artefacts are produced at the translation stage where tighter prompts and validation can be enforced.

## Modularity

Each stage can evolve independently:

- research prompts
- translation logic
- validation rules
- implementation code

## Reduced Failure Modes

The system avoids the brittle step where an LLM must simultaneously:

- perform literature research
- populate a strict schema

---

# Pilot Implementation Plan

The architecture should first be tested with a single signal.

Recommended pilot:

```
Insulin Resistance Detection
TyG Index Signal
```

Pilot workflow:

1. Produce research study markdown
2. Run Claude translation step
3. Generate translation block
4. Produce knowledge package
5. Run Knowledge Bus validator
6. Generate Layer B signal

This validates the full pipeline before scaling to additional research topics.

---

# Strategic Impact

This approach enables HealthIQ to build a large library of signals backed by structured scientific reasoning.

The research narrative becomes part of the product’s defensibility because every signal is traceable to published literature.

Over time this creates:

- a proprietary biological signal library
- transparent evidence lineage
- explainable health analytics

These characteristics strengthen both scientific credibility and long‑term competitive advantage.

---

# Summary

The research pipeline should be redesigned to separate research synthesis from structured signal generation.

The key change is introducing a **Claude Translation Layer** that converts research markdown into deterministic system artefacts.

This preserves research quality while maintaining the deterministic governance required by the HealthIQ architecture.

