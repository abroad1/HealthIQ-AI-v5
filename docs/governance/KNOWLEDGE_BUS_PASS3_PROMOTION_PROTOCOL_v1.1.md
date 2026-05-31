# KNOWLEDGE BUS PASS3 PROMOTION PROTOCOL v1.1
## Canonical Research → Package / Compiled Artefact Promotion Governance

**Status:** DRAFT FOR GOVERNANCE REVIEW  
**Authority:** HealthIQ Knowledge Governance  
**Companion To:** `KNOWLEDGE_BUS_SOP_v1.3.md`, `AUTOMATION_BUS_SOP_v1.3.1.md`  
**Purpose:** Define the deterministic promotion pathway from upstream investigation-spec / Pass_3-style research into governed package and compiled runtime artefacts.

---

# 1. Purpose

This protocol defines how canonical upstream research is promoted into runtime-safe HealthIQ artefacts.

It exists because the current Knowledge Bus SOP governs package validation and promotion, but does not yet fully govern the upstream transformation from rich research specifications into the package layer and adjacent compiled intelligence artefacts.

This protocol closes that gap.

It ensures that:

- canonical research authority is explicit
- package files are not mistaken for the full intelligence source
- compiled runtime views are deterministic and auditable
- source lineage is preserved end-to-end
- runtime components remain thin loaders rather than interpreters of raw research
- frontend remains render-only

---

# 2. Scope

This protocol governs the promotion path from:

- `*_Pass_3.json`
- investigation spec v3 YAML / JSON
- equivalent upstream canonical research specifications

into:

- Knowledge Bus packages
- compiled signal intelligence artefacts
- compiled WHY / root-cause artefacts
- compiled evidence artefacts
- runtime-safe metadata artefacts

It does **not** govern:

- frontend rendering
- LLM narrative generation
- manual ad hoc reasoning outside the governed pipeline
- runtime analytics implementation sprints themselves

Those remain governed by the Automation Bus and downstream runtime architecture.

---

# 3. Authority Hierarchy

The authoritative hierarchy is:

## 3.1 Canonical Research Layer

Canonical upstream medical research authority consists of:

- Pass_3 research artefacts
- investigation spec v3 artefacts
- future equivalent governed research contracts explicitly approved by governance

These artefacts are the source of medical reasoning authority.

They define:

- biomarker relationships
- derived metric logic
- hypotheses
- contradiction markers
- confirmatory tests
- override rules
- evidence strength
- narrative support material

They are the only layer allowed to carry the full richness of upstream medical reasoning.

## 3.2 Package Layer

Knowledge Bus package files are compiled runtime signal-activation views of upstream research.

They are not the full medical reasoning layer.

They exist to govern:

- signal activation
- dependencies
- signal packaging
- runtime readiness
- package-level promotion control

Current canonical package artefacts include:

- `research_brief.yaml`
- `signal_library.yaml`
- `package_manifest.yaml`

Optional package artefacts may include:

- `clinical_signoff.md`
- `intelligence_model.yaml`
- `promoted_signal_intelligence.yaml`

## 3.3 Compiled Intelligence Artefact Layer

Some upstream research content must compile into separate governed artefacts rather than being forced into package files.

These may include:

- signal intelligence artefacts
- promoted signal intelligence artefacts
- root-cause / WHY artefacts
- health-system card evidence artefacts
- presentation-safety metadata
- compile manifests

These artefacts are downstream compiled views of canonical research and must never become independent hand-authored medical authorities.

## 3.4 Runtime Layer

Runtime components must consume governed compiled artefacts only.

Runtime must not read raw Pass_3 / investigation spec files directly.

Runtime loaders must be thin, deterministic, and non-inferential.

## 3.5 Frontend Layer

Frontend remains render-only.

No frontend component may infer medical meaning.

---

# 4. Core Promotion Model

The intended promotion chain is:

```text
canonical research spec
↓
validation
↓
deterministic compiler / promotion process
↓
package files + compiled intelligence artefacts
↓
thin runtime loaders
↓
structured Layer B / report DTOs
↓
frontend render-only
```

This means:

- one canonical research authority
- multiple compiled runtime views
- no duplicate long-term medical authority
- no runtime reads of raw research sources
- no frontend medical inference

---

# 5. Canonical Research Inputs

## 5.1 Accepted Canonical Inputs

For the purposes of this protocol, accepted canonical research inputs are:

- investigation spec v3 artefacts validated against `investigation_spec_schema_v3.0.0.yaml`
- legacy Pass_3 artefacts that have been classified and explicitly accepted as canonical upstream research until migrated
- future governed research contracts explicitly approved by architecture governance

## 5.2 Validation Requirement

Canonical research must pass the relevant upstream validator before promotion begins.

For investigation spec v3 this is:

- `backend/scripts/validate_investigation_spec.py`

The promotion process must not begin from invalid upstream research.

## 5.3 Canonical Research Rule

Canonical research is the only medically authoritative source in the promotion chain.

Package files and compiled artefacts may only express, reduce, or reorganise canonical research.
They must not silently invent new medical meaning.

---

# 6. Promotion Targets

Upstream research may promote into one or more of the following target classes.

## 6.1 Package Promotion Target

Used for runtime signal activation packaging.

Typical outputs:

- `research_brief.yaml`
- `signal_library.yaml`
- `package_manifest.yaml`

## 6.2 Compiled Signal Intelligence Target

Used when a richer governed signal-intelligence representation is needed beyond package activation logic.

Typical outputs:

- `promoted_signal_intelligence.yaml`
- future signal intelligence derivatives

## 6.3 Compiled WHY / Root-Cause Target

Used when upstream hypotheses, contradictions, and confirmatory logic need a runtime-safe WHY representation.

Typical outputs:

- root-cause YAML / JSON artefacts
- compiler-ready WHY bundles
- structured downstream DTO-safe artefacts

## 6.4 Compiled Evidence / Card Target

Used when upstream evidence must be transformed into card-level or presentation-safe evidence structures.

Typical outputs:

- health-system card evidence artefacts
- presentation-safety metadata
- bounded explanation maps

---

# 7. Promotion Rules

## 7.1 Deterministic Compilation

All promotion from canonical research into packages or compiled artefacts must be deterministic.

Identical source input must produce identical compiled output.

No randomness, heuristic improvisation, or undocumented inference is permitted.

## 7.2 Source Preservation

Every promoted artefact must preserve traceability to its canonical source.

At minimum each promoted artefact or compile manifest must carry:

- `source_spec_id`
- source path
- source hash
- compiler or promoter version
- output hash
- validation result

## 7.3 No Duplicate Authority Rule

No hand-authored duplicate medical authority may remain permanently active where canonical research already exists.

If a manually created package or compiled artefact exists and canonical research becomes available, the manual authority must be:

- regenerated from canonical source
- accepted with explicit rationale
- retired
- or deferred with explicit classification

## 7.4 No Raw Runtime Reads

Raw Pass_3 / investigation spec files must not be read directly by runtime logic.

All runtime reads must go through governed promoted artefacts.

## 7.5 Thin Loader Rule

Runtime loaders may:

- load governed artefacts
- map fields into DTOs
- perform deterministic selection

Runtime loaders may not:

- reinterpret canonical research
- recompute medical meaning from raw research
- apply hidden medical heuristics

---

# 8. Compile Manifest Requirements

Every promotion run must emit a compile manifest or equivalent metadata record once the compiler/promoter exists. During interim/manual promotion, equivalent lineage metadata must be recorded in the package manifest, governance register, or sprint audit report.

Minimum required fields:

```yaml
source_spec_id:
source_path:
source_hash:
compiler_version:
output_artifacts:
output_hashes:
validation_result:
promoted_utc:
promotion_mode:
```

Where:

- `source_spec_id` identifies the canonical upstream research asset
- `promotion_mode` identifies what kind of output was produced, such as:
  - `PACKAGE`
  - `PROMOTED_SIGNAL_INTELLIGENCE`
  - `ROOT_CAUSE`
  - `CARD_EVIDENCE`
  - `MIXED`

---

# 9. Legacy Package Reconciliation Rules

Existing packages that do not clearly derive from canonical research must be classified.

Each legacy package must be assigned one of:

- `MAPPED_TO_CANONICAL_RESEARCH`
- `REGENERATED_FROM_CANONICAL_RESEARCH`
- `ACCEPTED_WITH_RATIONALE`
- `RETIRED`
- `DEFERRED_WITH_EXPLICIT_REASON`

No legacy package should remain indefinitely in ambiguous provenance state.

---

# 10. Transition-State Classification (Temporary Until Legacy Reconciliation Completes)

This section exists to govern the current mixed estate while legacy runtime packages and upstream research assets are being reconciled.

These states are operational transition classifications, not permanent long-term doctrine.

Use the following temporary states where needed:

- `research_missing`
- `research_present_unmapped`
- `research_present_uncompiled`
- `compiled_not_promoted`
- `runtime_active_legacy`
- `accepted_with_rationale`
- `retired`

Definitions:

## 10.1 `research_missing`

No canonical upstream research has yet been identified for the package or runtime artefact.

## 10.2 `research_present_unmapped`

Canonical research exists, but no explicit mapping has yet been made between that research and the current package or runtime artefact.

## 10.3 `research_present_uncompiled`

Canonical research exists and is mapped conceptually, but has not yet been compiled into the required package or compiled artefact layer.

## 10.4 `compiled_not_promoted`

A compiled artefact or package exists, but has not yet been formally promoted into runtime authority.

## 10.5 `runtime_active_legacy`

A legacy runtime package or artefact remains active without fully governed canonical lineage.

This state is temporary and must not be treated as acceptable long-term architecture.

## 10.6 `accepted_with_rationale`

A legacy artefact is being retained temporarily or longer-term with explicit documented rationale.

## 10.7 `retired`

The artefact is no longer active and should not be treated as runtime authority.

### Transition-State Rule

These states must be used to prevent future agents from confusing:

- missing research
with
- existing research that has not yet been mapped, compiled, or promoted

No team should conclude that research is absent if the real condition is that promotion work is incomplete.

---

# 11. Relationship to Knowledge Bus SOP

This protocol does not replace `KNOWLEDGE_BUS_SOP_v1.3.md`.

The division is:

## Knowledge Bus SOP
Governance of package validation, promotion readiness, package lifecycle, and package-layer operational controls.

## Pass3 Promotion Protocol
Governance of canonical research promotion into packages and compiled intelligence artefacts.

The Knowledge Bus SOP remains the operational package-governance document.

This protocol governs the upstream promotion architecture feeding it.

---

# 12. Relationship to Automation Bus SOP

This protocol does not replace `AUTOMATION_BUS_SOP_v1.3.1.md`.

Automation Bus remains the governance layer for implementation work.

However, this protocol establishes the future dependency model that Automation Bus must eventually respect.

Future Automation Bus integration may include a front matter field such as:

```yaml
knowledge_dependency: PASS3_PROMOTION | SIGNAL_LIBRARY | COMPILED_INTELLIGENCE | NONE
```

This is not active enforcement today.
It is a future governance integration point.

---

# 13. Validation and Enforcement Boundaries

## 13.1 What is currently operational

Currently operational and trusted:

- package validation via `validate_knowledge_package.py`
- investigation spec validation via `validate_investigation_spec.py`
- package promotion readiness via Knowledge Bus current status
- manual architecture review of cross-bus dependency decisions

## 13.2 What is not yet fully operational

Not yet fully operational:

- full deterministic compilation chain from all canonical research inputs into all runtime artefact classes
- universal compile manifest enforcement
- automation-bus kernel enforcement of upstream knowledge dependency
- runtime-wide promotion lineage checks

These remain forward governance requirements.

---

# 14. Interim Operational Rule

Until the full compiler / promotion chain is implemented, the following interim rule applies:

- new package promotion requires explicit lineage to canonical research
- existing legacy runtime packages without that lineage may remain temporarily only if they are:
  - classified
  - risk-assessed
  - and scheduled for mapping, regeneration, acceptance with rationale, or retirement

Teams must not infer that package validation alone proves full upstream research-governance correctness.

Teams must not infer that research is absent where the actual state is unmapped, uncompiled, or unpromoted research.

---

# 15. Governance Decision Record

This protocol adopts the following decisions:

1. Canonical research authority sits upstream of package authority
2. Package files are runtime signal-activation artefacts, not the full intelligence layer
3. Rich upstream research may compile into multiple governed artefact classes
4. Runtime must never read raw canonical research directly
5. Frontend must remain render-only
6. Promotion lineage must be explicit and auditable
7. Legacy ambiguous packages must be classified and reconciled

---

# 16. Future Migration Path

This protocol is intended to be a companion governance document in the short term.

Planned evolution:

1. Stabilise the protocol against live codebase execution
2. Implement the required promotion-chain artefacts and compiler lineage controls
3. Update Knowledge Bus operational controls where needed
4. Fold settled rules into `KNOWLEDGE_BUS_SOP v1.4` when mature

Until then, this protocol remains the authoritative document for Pass_3 / investigation-spec to package / compiled artefact promotion governance.

---

# 17. Design Philosophy

HealthIQ must not allow rich research, package activation, compiled WHY logic, and runtime presentation artefacts to become competing medical authorities.

The system must preserve a single truth hierarchy:

canonical research  
→ deterministic promotion  
→ governed runtime artefacts  
→ thin loaders  
→ structured outputs  
→ render-only frontend

This is the only architecture that remains:

- deterministic
- clinically traceable
- auditable
- scalable
- defensible under future regulatory scrutiny

---

**Version:** v1.1  
**Status:** Draft for Governance Review
