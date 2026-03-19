# KNOWLEDGE BUS SOP v1.3  
## Intelligence-Aligned Architecture Governance (Operationally Aligned — Final)

**Status:** APPROVED FOR USE (WITH KNOWN CONSTRAINTS — SEE §§5, 10, 14, 15)  
**Authority:** HealthIQ Intelligence Governance Layer  
**Supersedes:** v1.2  
**Alignment:** Automation Bus SOP v1.3  

---

# 1. Purpose

The Knowledge Bus governs the promotion of clinical research into deterministic signal architecture within HealthIQ AI.

Version 1.3 extends this role to include behavioural governance, recognising that signal definitions directly influence system reasoning and output behaviour.

This SOP reflects both the intended architecture and the current operational state of the system.

The Knowledge Bus ensures that:

- Clinical research is translated into deterministic, machine-readable architecture
- Signal definitions remain clinically traceable and scientifically grounded
- Architecture artefacts are validated before implementation
- Behavioural impact of signals is understood and controlled
- Signal interactions do not introduce unintended system behaviour
- Architecture promotion is auditable, reproducible, and deterministic

The Knowledge Bus operates as a control plane separate from the Automation Bus.

- Knowledge Bus governs what the system knows
- Automation Bus governs how the system behaves and executes

---

# 2. Architectural Principles

### Deterministic Promotion
All architecture artefacts must pass automated validation before promotion.

### Behavioural Awareness
Signal definitions must be evaluated for their impact on system behaviour.

### Immutable Packages
Packages are immutable once promoted.

### Evidence Traceability
All signals must map to clinical evidence.

### Validator Authority
Validators, not LLMs, determine correctness.

### Controlled Integration
Integration into runtime requires validated readiness state.

---

# 3. Repository Structure (Reconciled)

All Knowledge Bus artefacts are stored under:

```text
knowledge_bus/
````

### Directory Structure

```text
knowledge_bus/
  schema/
    signal_library_schema.yaml
    research_brief_schema.yaml
    package_manifest_schema.yaml

  current/
    active_package.json
    latest_knowledge_status.json

  packages/
    pkg_*
```

### Package Naming Convention

* `pkg_*` is the authoritative package naming standard
* `KBP-*` identifiers remain present in legacy tooling and some internal references
* Package directory naming and internal package identifiers are not currently fully unified

---

# 4. Package Structure

Each package contains:

### Mandatory

* `research_brief.yaml`
* `signal_library.yaml`
* `package_manifest.yaml`

### Optional

* `clinical_signoff.md`

### Forward Requirements

The following artefacts are defined architecturally but are not yet required for all existing packages:

* `signal_spec.md`
* `architecture_audit.md`

### Runtime Authority

There is no per-package `knowledge_status.json`.

The authoritative runtime state file is:

```text
knowledge_bus/current/latest_knowledge_status.json
```

---

# 5. Package Lifecycle

Lifecycle is executed via:

```text
backend/scripts/run_knowledge_package.py
```

Commands:

* `start`
* `finish`
* `status`

### Known Constraint (Critical)

The lifecycle controller currently enforces a `KBP-` package ID pattern internally.

This is not aligned with the current package naming convention:

```text
pkg_*
```

As a result:

* Lifecycle commands are not reliable for `pkg_*` packages
* Lifecycle behaviour may fail or behave incorrectly for the actual package store

### Operational Rule

Until reconciled:

* The lifecycle controller is non-authoritative
* The validator is the only trusted promotion gate

### Current Interim Promotion Process (Mandatory)

Until the lifecycle controller is fixed, all promotions must follow this exact process.

#### Step 1 — Validate Package

Run the canonical validator directly against the target package.

Example pattern:

```text
python backend/scripts/validate_knowledge_package.py --package-dir knowledge_bus/packages/<pkg_name>
```

#### Step 2 — Confirm PASS

Promotion is only permitted if:

* structural validation passes
* no validation failures remain
* the package is marked ready for implementation

#### Step 3 — Manual Promotion

Update:

```text
knowledge_bus/current/latest_knowledge_status.json
```

using the following minimum structure:

```json
{
  "active_package": "<pkg_name>",
  "ready_for_implementation": true
}
```

Where:

* `active_package` is the promoted package directory name
* `ready_for_implementation` must be `true` only after validator PASS

#### Step 4 — Record Promotion

The commit that performs promotion must include a reference to the validator result.

Current interim evidence standard:

* paste the validator stdout summary into the commit message body
* or save the validator stdout to:

```text
knowledge_bus/current/latest_validation_output.txt
```

and include that file in the promotion commit

At minimum, the evidence must show:

* target package path
* validator PASS result
* readiness for implementation

### Prohibitions

* Do not use the lifecycle script as the authoritative promotion mechanism
* Do not bypass the validator
* Do not promote a package without updating `latest_knowledge_status.json`

### Required Action

A reconciliation sprint must:

* update the lifecycle controller to support `pkg_*`
* or introduce explicit dual-pattern support for both `KBP-*` and `pkg_*`

---

# 6. Research Artefact

The research artefact is:

```text
research_brief.yaml
```

It must comply with:

```text
knowledge_bus/schema/research_brief_schema.yaml
```

Required fields include:

* `research_domain`
* `sources`
* `biomarkers`
* `derived_metrics`
* `physiological_claim`
* `evidence_strength`

This artefact ensures that all signal architecture remains clinically traceable and scientifically defensible.

---

# 7. Signal Library

The machine-readable signal architecture is:

```text
signal_library.yaml
```

It must comply with:

```text
knowledge_bus/schema/signal_library_schema.yaml
```

Each signal must include:

* `signal_id`
* `name`
* `description`
* `system`
* `primary_metric`
* `supporting_metrics`
* `dependencies`
* `thresholds`
* `activation_logic`

Rules:

* Each signal must declare exactly one primary metric
* Activation logic must be deterministic
* Weighted scoring systems are forbidden
* Signal structure must remain validator-compliant

---

# 8. Package Manifest

The package manifest is:

```text
package_manifest.yaml
```

### Required Fields (Current)

* `package_id`
* `version`
* `description`

### Forward Fields (v1.3)

The following fields are part of the v1.3 governance model but are not yet present in all existing manifests:

```yaml
behavioural_impact: NONE | LOW | HIGH
engine_compatibility: v5.x
```

### Behavioural Impact Definition

#### NONE

No behavioural effect.

#### LOW

Introduces isolated signals or limited extensions with constrained impact.

#### HIGH

Affects thresholds, dependencies, activation logic, cascade logic, or core signal behaviour.

### Additional Fields

The following fields may exist and are permitted:

* `author`
* `created_at`
* `source_document`
* `translation_mode`

These are allowed and do not affect compliance.

The validator enforces only required fields unless and until schema migration expands enforcement.

---

# 9. Validator Authority

The canonical validator is:

```text
backend/scripts/validate_knowledge_package.py
```

This is the only trusted promotion gate.

The file:

```text
backend/scripts/validate_signal_library.py
```

is treated as a supporting or legacy validator and is not the authoritative package-promotion mechanism.

---

# 10. Validation Responsibilities

### Structural Validation (Implemented)

The current validator performs structural checks including:

* schema validation
* signal ID uniqueness
* dependency resolution
* circular dependency detection
* SSOT validation
* package-level readiness determination

### Behavioural Validation

#### Implemented (Current)

* basic dependency validation
* structural relationship checks

#### Required (Not Yet Implemented)

The behavioural validation layer is expected to support:

* threshold overlap detection
* activation conflict detection
* dependency cascade amplification checks
* contradictory signal detection
* dominance and suppression conflict detection

These capabilities are not yet fully implemented.

They form part of the behavioural validation roadmap and must be delivered before the Knowledge Bus can be considered fully behaviourally safe.

---

# 11. Audit Outputs

The authoritative runtime status output is:

```text
knowledge_bus/current/latest_knowledge_status.json
```

### Forward Audit Output

A future behavioural audit layer should emit a structured assessment such as:

```yaml
behavioural_assessment:
  cascade_risk: LOW | MEDIUM | HIGH
  conflict_risk: LOW | MEDIUM | HIGH
  dominance_risk: LOW | MEDIUM | HIGH
```

This is forward architecture, not current enforced behaviour.

---

# 12. Promotion Rules

Promotion is allowed only if:

* the canonical validator returns PASS
* the research brief is valid
* the signal library is valid
* the interim promotion process in §5 is followed where lifecycle control is unavailable

No package may be treated as promoted merely because it exists in the package store.

---

# 13. No-op Protection

If a package introduces:

* no architectural change
* and no behavioural change

then promotion is prohibited.

The Knowledge Bus must not be used to create artificial or redundant promotions.

---

# 14. Automation Bus Integration

### Status

The following integration is architecturally defined but not yet implemented:

```yaml
knowledge_dependency: SIGNAL_LIBRARY
```

### Current State

* This field is not currently part of the Automation Bus front matter schema
* The Automation Bus kernel does not currently enforce Knowledge Bus readiness checks
* No runtime enforcement exists today

### Intended Future Integration

The Automation Bus must eventually:

* extend its front matter schema to include `knowledge_dependency`
* validate `knowledge_bus/current/latest_knowledge_status.json`
* enforce `ready_for_implementation: true` before allowing knowledge-dependent execution

### Current Rule

This integration is currently non-operative.

Responsibility remains with architectural review and manual gating.

---

# 15. Intelligence Core Coupling

### Status

This rule is architecturally defined but not yet enforced mechanically.

Reason:

* `behavioural_impact` is not yet present in all package manifests
* no runtime enforcement chain currently exists from Knowledge Bus manifests into Automation Bus risk classification

### Intended Rule (Future)

If:

```yaml
behavioural_impact: HIGH
```

then downstream Automation Bus work must be treated as HIGH risk.

### Current Rule

This must be applied manually during architectural review until manifest migration and enforcement are implemented.

---

# 16. Immutability

Once a package is promoted:

* it must not be modified
* corrections require a new package
* historical package state must remain intact for traceability

---

# 17. Governance Scope

The Knowledge Bus governs:

* signal definitions
* biomarker relationships
* derived metrics
* physiological system modelling
* behavioural impact of signal logic

It does not govern:

* UI
* frontend presentation
* visualisation
* general backend services outside signal architecture governance

---

# 18. System Lifecycle

```text
research
↓
research brief
↓
signal specification (forward requirement)
↓
signal library
↓
validation
↓
promotion
↓
automation bus
↓
runtime
```

This reflects both current operational flow and forward architectural intent.

---

# 19. Design Philosophy

The Knowledge Bus is:

* a deterministic architecture system
* a behavioural governance layer
* a safeguard against unsafe logic
* a control plane for clinical intelligence

The integrity of this system directly determines the clinical defensibility of every report delivered to users and their clinicians.

Knowledge defines intelligence.
Automation executes intelligence.

Together they ensure:

* correctness
* safety
* scalability

---

**Version:** v1.3 (Operationally Aligned — Final)
**Status:** Approved for Use with Explicit Constraints

```
```
