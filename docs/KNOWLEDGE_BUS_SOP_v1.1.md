KNOWLEDGE BUS SOP v1.1

Status: LOCKED
Authority: HealthIQ Development Governance
Scope: Research → Architecture Promotion
Effective Date: 2026-03-07

---

1. Purpose

The Knowledge Bus governs the promotion of research and signal architecture before implementation begins.

Its purpose is to ensure that:

• clinical research is translated into deterministic architecture
• biomarker reasoning remains clinically traceable
• signal definitions remain consistent across the platform
• architecture artefacts are validated before implementation
• signal intelligence promotion is auditable and reproducible

The Knowledge Bus operates as a control plane separate from the Automation Bus.

Automation Bus governs code execution.
Knowledge Bus governs research and architecture promotion.

---

2. Architectural Principles

The Knowledge Bus operates under five principles.

Deterministic Promotion
All architecture artefacts must pass automated validation before promotion.

Immutable Packages
Architecture packages are immutable once validated.

Evidence Traceability
Signal definitions must be traceable to documented clinical evidence.

Validator Authority
Architecture validation is performed by automated validators, not chat systems.

Minimal Coupling
The Knowledge Bus integrates with the Automation Bus through a single readiness flag.

---

3. Repository Structure

All Knowledge Bus artefacts exist under:

knowledge_bus/

Structure:

knowledge_bus/

schema/
signal_library_schema.yaml
research_brief_schema.yaml

current/
active_package.json
latest_knowledge_status.json

packages/
KBP-0001/

Each architecture promotion package is stored in:

knowledge_bus/packages/KBP-xxxx/

Example:

knowledge_bus/packages/KBP-0001/

research_brief.yaml
signal_spec.md
signal_library.yaml
architecture_audit.md
knowledge_status.json

Packages are immutable once validated.

---

4. Package Lifecycle

Knowledge packages follow a deterministic lifecycle.

States:

RESEARCH_COMPLETE
SIGNAL_SPEC_COMPLETE
SIGNAL_LIBRARY_COMPLETE
ARCHITECTURE_AUDITED
READY_FOR_IMPLEMENTATION

Promotion is performed using:

backend/scripts/run_knowledge_package.py

Commands:

start
finish
status

---

5. Research Artefact

The first artefact in a knowledge package is:

research_brief.yaml

This document captures the clinical evidence supporting the signal architecture.

It must comply with:

knowledge_bus/schema/research_brief_schema.yaml

Required fields include:

research_domain
sources
biomarkers
derived_metrics
physiological_claim
evidence_strength

This artefact ensures signal definitions remain clinically traceable and scientifically defensible.

---

6. Signal Specification

Signal design is written in:

signal_spec.md

This document describes:

• physiological interpretation
• biomarker dependencies
• derived metric logic
• activation thresholds
• clinical meaning

This document is human readable and used to design the machine architecture.

---

7. Signal Library

Machine-readable signal architecture is stored in:

signal_library.yaml

Each signal must include:

signal_id
name
description
system
primary_metric
supporting_metrics
dependencies
thresholds
activation_logic

Signals must declare a single primary metric.

Weighted scoring models are forbidden.

Signal definitions must comply with:

knowledge_bus/schema/signal_library_schema.yaml

---

8. Architecture Validator

Signal libraries are validated using:

backend/scripts/validate_signal_library.py

Validator responsibilities:

• schema validation
• signal ID uniqueness
• dependency resolution
• circular dependency detection
• SSOT biomarker validation
• derived metric validation
• threshold logic validation

Validator outputs:

architecture_audit.md
knowledge_status.json

Example status file:

{
"package_id": "KBP-0001",
"status": "READY_FOR_IMPLEMENTATION",
"validator_status": "PASS",
"ready_for_implementation": true,
"validated_utc": "2026-03-07T12:00:00Z",
"errors": [],
"warnings": []
}

---

9. Promotion Rules

A knowledge package may only be promoted when:

• validator passes
• research brief complies with schema
• signal library complies with schema
• architecture audit contains no errors

Promotion writes:

knowledge_bus/current/latest_knowledge_status.json

This file represents the active architecture state.

---

10. Automation Bus Integration

The Automation Bus must enforce Knowledge Bus readiness.

If a work package declares:

knowledge_dependency: SIGNAL_LIBRARY

the Automation Bus must verify:

knowledge_bus/current/latest_knowledge_status.json

contains:

ready_for_implementation: true

If the readiness flag is not true:

Kernel start FAIL.

This rule prevents signal implementation before architecture validation.

---

11. Immutability Rules

Once a knowledge package is promoted:

• files may not be modified
• corrections require a new package ID
• historical packages must remain accessible

This creates a complete lineage of signal architecture evolution.

---

12. Governance Scope

The Knowledge Bus governs:

• signal definitions
• biomarker relationships
• derived metrics
• physiological system models

It does not govern:

• application UI
• analytics visualisation
• frontend code
• general backend services

Those remain under the Automation Bus.

---

13. System Lifecycle

HealthIQ development now follows this lifecycle:

clinical research
↓
research brief
↓
signal specification
↓
signal library
↓
knowledge bus validation
↓
architecture promotion
↓
automation bus execution
↓
application runtime

This ensures architecture remains deterministic as the biomarker system expands.

END OF DOCUMENT
