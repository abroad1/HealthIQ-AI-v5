# RESEARCH INGESTION BUS SOP v1.0

**Status:** LOCKED  
**Authority:** HealthIQ Development Governance  
**Effective Date:** 2026-03-08

---

## 1. Purpose

The Research Ingestion Bus governs the discovery, extraction, validation, and promotion of biomedical research evidence into HealthIQ.

Its purpose is to ensure that research entering the platform is:

- derived from credible primary research
- emitted in deterministic machine-readable format
- traceable to source literature
- validated before influencing signal architecture

The Research Ingestion Bus is the upstream evidence control plane for HealthIQ.

---

## 2. Governance Boundary

HealthIQ operates three control planes:

- **Research Ingestion Bus** -> governs research discovery and structured evidence extraction
- **Knowledge Bus** -> governs signal architecture design and promotion
- **Automation Bus** -> governs implementation execution

The Research Ingestion Bus must not generate signal architecture.  
It produces validated research evidence only.

---

## 3. Research Generation Model

Research generation is performed by a dedicated research LLM operating in web research mode.

The research LLM must:

- search the internet for relevant biomedical literature
- prioritise primary and high-quality evidence
- extract structured research findings
- emit a structured YAML package only

The research LLM must not produce prose reports, markdown briefs, or architectural recommendations.

The only authoritative output is a structured YAML package conforming to:

`research_ingestion_bus/schema/research_package_schema.yaml`

Future versions may replace the web interface with an API-based research service without changing the governance model.

---

## 4. Evidence Standards

Research must prioritise:

1. meta-analyses and systematic reviews
2. prospective cohort studies
3. randomised controlled trials
4. major clinical guideline documents

Unacceptable source classes include:

- blogs
- opinion pieces
- non-scientific summaries
- uncited claims

All extracted claims must be linked to identifiable source references.

---

## 5. Repository Structure

```text
research_ingestion_bus/
  RESEARCH_INGESTION_BUS_SOP_v1.md

  schema/
    research_package_schema.yaml

  prompts/
    research_generation_prompt_v1.md
    clinical_validation_prompt_v1.md

  examples/
    example_research_package.yaml

  packages/
    RIB-0001/
```

Each archived package contains the structured research artefacts for one research topic / ingestion run.

---

## 6. Structured Output Requirement

The research LLM must produce:

`extracted_research_package.yaml`

The output must conform exactly to the research package schema.

The package may contain:

- multiple source papers
- multiple physiological claims
- optional formulas
- optional thresholds
- source-linked verbatim evidence quotes
- optional excluded findings that were reviewed but not promoted as validated claims

---

## 7. Validation Stages

Research packages must pass two validation stages.

### Stage 1 - Schema Validation

Validator checks:

- schema compliance
- required field presence
- identifier format validity
- source reference structure
- SSOT alignment

Packages failing schema validation must be rejected.

### Stage 2 - Clinical Validation

A second LLM validation stage verifies:

- claims accurately reflect cited research
- formulas match the literature
- thresholds are explicitly supported
- quotes are faithful and relevant
- unsupported inference has not been introduced

Packages failing clinical validation must be rejected.

---

## 8. SSOT Alignment

All referenced entities must align with HealthIQ registries.

These include:

- canonical biomarker registry
- derived metric registry

If a package references an unknown biomarker or derived metric, validation must fail.

Novel entities must follow the SSOT expansion process before the package may be promoted.

---

## 9. Promotion

Only packages that pass both validation stages may be promoted.

Promotion produces:

`validated_research_package.yaml`

This becomes the authoritative research artefact available for downstream Knowledge Bus use.

The Knowledge Bus must not process raw research output that has not been promoted.

---

## 10. Immutability

Once a research package is promoted and archived:

- files must not be modified
- corrections require a new package ID
- historical packages must remain accessible

This preserves a complete lineage of research evidence.

---

## 11. Lifecycle

```text
internet research
↓
research LLM structured extraction
↓
extracted_research_package.yaml
↓
schema validation
↓
clinical validation
↓
validated_research_package.yaml
↓
Knowledge Bus
↓
signal architecture
↓
Automation Bus
↓
implementation
```

This ensures research evidence is validated before influencing architecture or code.

---

END OF DOCUMENT