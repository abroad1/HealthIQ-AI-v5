# Claude Research-to-Knowledge Translation Specification v1

## Purpose

This specification defines how Claude Code converts biomedical research markdown documents into deterministic Knowledge Bus packages for the HealthIQ platform.

Claude acts as the translation layer between human-readable scientific research and structured system knowledge.

The goal is to ensure that research evidence can be safely transformed into governed system artefacts while preserving scientific traceability and preventing unsupported logic from entering the system.

This document governs **Phase B — Research Translation** of the HealthIQ Research Knowledge Pipeline.

---

# Architectural Context

Pipeline context:

```
Scientific Literature
        ↓
Research LLM / Human Research
        ↓
research_study_<topic>.md
        ↓
Claude Translation (THIS SPECIFICATION)
        ↓
Knowledge Bus Package
        ↓
Knowledge Bus Validator
        ↓
Automation Bus Implementation
```

Claude is responsible only for translating research markdown into Knowledge Bus assets.

Claude does not implement runtime code and does not bypass Knowledge Bus validation.

---

# Input Contract

Claude receives a research markdown document.

Example:

```
research_study_insulin_resistance.md
```

The research document must follow the **Research Study Markdown Template** defined in the pipeline architecture document.

Minimum expected sections include:

- signal or research topic
- biological question
- clinical rationale
- biomarker relationships
- derived metric formulas
- threshold evidence
- supporting references
- limitations

Claude must not assume additional structure beyond the defined research template.

---

# Claude Responsibilities

Claude must extract structured knowledge from the research document.

The following information must be identified where present:

## Signal Definition

- signal identifier
- physiological system
- biological claim

Example:

```
signal_insulin_resistance
```

## Biomarker Dependencies

Claude must identify biomarkers referenced by the research.

Biomarkers must match canonical identifiers used by the SSOT registry.

Example:

```
triglycerides
glucose
insulin
```

## Derived Metrics

Claude must extract derived metrics referenced in the research.

Example:

```
derived.tyg_index
derived.homa_ir
```

Claude must not invent derived metrics.

Derived metrics must only appear if supported by the research document.

## Formulas

Claude must extract the mathematical formula used for derived metrics.

Example:

```
TyG = ln((triglycerides_mg_dL × glucose_mg_dL) / 2)
```

Claude must preserve the formula exactly as presented in research.

## Evidence Thresholds

Claude must extract thresholds supported by literature.

Example:

```
TyG < 8.30
TyG 8.30–8.49
TyG ≥ 8.50
```

Thresholds must include the evidence basis where possible.

Claude must not invent thresholds.

## Clinical Guardrails

Claude must identify population limitations.

Examples include:

- non-fasting samples
- pregnancy
- specific disease populations

## Evidence Strength

Claude should classify evidence strength where appropriate.

Example categories:

- cohort study
- meta analysis
- guideline recommendation

## References

Claude must capture supporting research references including:

- paper title
- journal
- year
- DOI or URL

---

# Translation Modes

Claude must determine whether the research corresponds to an existing signal.

Two modes exist.

## Confirmation Mode

The research validates an existing signal already present in the Knowledge Bus.

Claude must:

- confirm the signal identifier
- document supporting evidence
- avoid modifying signal logic unless explicitly supported

Example:

```
signal_insulin_resistance already exists in KBP-0001
research confirms thresholds
```

## Creation Mode

The research introduces a new physiological signal.

Claude must generate a new Knowledge Bus package describing that signal.

This includes:

- new signal identifier
- derived metric dependencies
- thresholds
- biological claim

---

# Output Contract

Claude must generate Knowledge Bus package assets.

Minimum required files include:

```
package_manifest.yaml
signal_library.yaml
clinical_signoff.md
```

## package_manifest.yaml

Defines package metadata including:

- package identifier
- description
- package scope

## signal_library.yaml

Defines the signal logic including:

- signal identifier
- dependencies
- derived metrics
- thresholds
- activation logic

## clinical_signoff.md

Documents human review of signal thresholds and clinical interpretation.

Contents must include:

- reviewer name
- review date
- acknowledgement of research evidence
- documented limitations

---

# Determinism Rules

Claude must follow strict determinism rules when translating research.

Claude must not:

- invent biomarkers
- invent derived metrics
- invent thresholds
- modify formulas

If research evidence is ambiguous or incomplete, Claude must record the uncertainty instead of filling gaps.

Example:

```
threshold evidence inconclusive
additional validation required
```

---

# Naming Conventions

Claude must follow platform naming conventions.

Examples:

Signals

```
signal_insulin_resistance
```

Derived metrics

```
derived.tyg_index
```

Biomarkers

```
triglycerides
glucose
insulin
```

Identifiers must follow snake_case.

---

# Evidence Traceability

Each signal must maintain traceability back to the research document.

The generated package must reference the originating research markdown file.

Example:

```
source_document: research_study_insulin_resistance.md
```

This ensures scientific lineage for every system signal.

---

# Error Handling

If Claude encounters unsupported research content it must record the issue rather than attempting correction.

Examples include:

- unknown biomarker
- unsupported derived metric
- missing threshold evidence

Claude must flag the issue for manual review.

---

# Validation Boundary

Claude does not perform final validation.

All generated Knowledge Bus packages must pass the Knowledge Bus validator before being accepted.

If validation fails the package must be corrected.

---

# Output Example

Example result of translation process:

```
research_study_insulin_resistance.md
        ↓
Claude translation
        ↓
KBP-0002
        ├ package_manifest.yaml
        ├ signal_library.yaml
        └ clinical_signoff.md
```

---

# Implementation Scope

This specification governs only the research translation stage.

Claude does not:

- modify runtime analytics code
- bypass Knowledge Bus governance
- implement derived metrics directly

Runtime changes occur only through Automation Bus workflows.

---

# Versioning

Document Version

```
Claude Research-to-Knowledge Translation Specification v1
```

Future versions may expand support for:

- automated evidence classification
- multi-paper aggregation
- automated derived metric registry updates

---

# Strategic Role

This translation layer enables HealthIQ to scale its biological intelligence safely.

Research can be continuously incorporated into the system while maintaining deterministic governance and clinical traceability.

