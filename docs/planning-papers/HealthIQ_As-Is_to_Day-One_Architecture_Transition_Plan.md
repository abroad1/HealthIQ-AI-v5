# HealthIQ AI — As-Is to Day-One Architecture Transition Plan

**Document purpose:**  
Define the plan to move HealthIQ AI from the current fragmented research/runtime architecture to the correct day-one architecture before product launch.

**Intended reviewers:**  
- GPT Head of Architecture  
- Claude Code  
- Cursor  
- Human product/technical owner

**Status:** Draft for architectural review  
**Implementation status:** No code changes authorised by this document  
**Primary decision:** HealthIQ must correct the research-to-runtime intelligence architecture before launch, while there are no live users and no backward-compatibility burden.

---

## 1. Executive summary

HealthIQ has not lost the ability to reach the correct day-one architecture. However, the current codebase contains architectural drift that must be corrected before launch.

The core issue is not the quality of the medical research. The research layer is rich. The issue is that the runtime and UX layers do not reliably consume that research through a governed, deterministic pipeline.

The correct target architecture is:

```text
canonical research spec
→ validation
→ deterministic compiler suite
→ governed runtime artefacts
→ thin runtime loaders
→ structured DTOs
→ frontend render-only
```

The current architecture must not be patched around indefinitely. Because there are no live users, the correct approach is not cautious coexistence. It is controlled replacement.

Legacy layers should be retained only where they help with parity testing, comparison, or evidence review. They should not remain long-term runtime authorities.

---

## 2. Current as-is state

The current system contains several fragmented intelligence paths.

### 2.1 Research source

The Pass 3 / investigation spec v3 corpus contains rich medical intelligence, including:

- marker roles
- relationship_kind
- per-marker rationale
- ranked hypotheses
- physiological claims
- caveats
- contradiction markers
- missing_data.policy
- confirmatory tests
- evidence strength
- biological pathway / mechanism / interpretation / implications narrative

This is the richest structured source of medical reasoning currently available to HealthIQ.

### 2.2 Package files

Packages currently act as runtime signal assets, but they are inconsistent in maturity.

Some preserve activation logic, overrides and explanation prose. Newer packages may preserve structured supporting marker metadata. Older packages are lossy and may only hold flat supporting-marker lists.

The package layer currently loses or fails to route much of the upstream research richness.

### 2.3 Root-cause YAML

The root-cause hypothesis YAML layer is hand-authored and partly overlaps with Pass 3 hypotheses.

It currently functions as a WHY/report layer, but it is not compiled from the canonical research source. It therefore creates a duplicate medical authority.

### 2.4 Health Systems Card evidence

The current Health Systems Card evidence layer relies on hard-coded subsystem marker maps rather than governed research-derived intelligence.

This creates several problems:

- marker roles are not properly surfaced
- relationship kinds are not consumed
- missing-marker explanations are thin
- contradictory/differential frames are absent
- frontend-facing subsystem evidence is weaker than the underlying research
- manual maps risk becoming another medical authority

### 2.5 DTO and frontend

The frontend is mostly a renderer, which is directionally correct. However, the DTOs currently do not carry enough structured intelligence for the frontend to show the true value of the medical research.

The issue is therefore backend intelligence assembly, not frontend creativity.

---

## 3. Architectural problem statement

HealthIQ currently has strong research assets but no fully governed research-to-runtime compiler that preserves medical intelligence into the runtime artefacts consumed by reports and Health Systems Cards.

The current system suffers from:

1. lossy translation from research into packages
2. duplicated hypothesis authorities
3. hard-coded subsystem evidence
4. orphaned explanation fields
5. weak marker-role semantics
6. unclear signal/spec identity
7. insufficient provenance from user-facing output back to research source
8. no single deterministic compile chain from clinical research to runtime DTO

This must be corrected before launch.

---

## 4. Day-one to-be architecture

The day-one architecture should be:

```text
Canonical Research Spec
   ↓
Research Validator
   ↓
Compiler Suite
   ├── Signal Activation Artefact
   ├── Signal Intelligence Artefact
   ├── Root-Cause / WHY Artefact
   ├── Health System Card Evidence Artefact
   └── Presentation Safety Metadata
   ↓
Runtime Loaders
   ↓
Analysis Orchestrator
   ↓
Structured InsightGraph / Report Assembly
   ↓
DTO Boundary
   ↓
Frontend Render
```

The key principle is:

```text
One canonical research authority.
Multiple compiled runtime views.
No hand-authored duplicate medical authorities.
No runtime reads of raw research files.
No frontend medical inference.
```

---

## 5. Source-of-truth decision

### 5.1 Canonical source

The canonical upstream medical research authority should be:

```text
investigation_spec v3 / Pass 3 research corpus
```

This does not mean the raw Pass 3 batch-file shape must exist forever. The file organisation can evolve. The contract matters more than the current folder layout.

### 5.2 Runtime source

Runtime should never read raw investigation specs directly.

Runtime should read only validated, compiled, immutable runtime artefacts.

### 5.3 Legacy source treatment

Existing packages, root-cause YAML and hard-coded subsystem maps should be treated as legacy runtime artefacts or scaffolding unless they are regenerated from the canonical research source.

---

## 6. Target artefact model

### 6.1 Canonical Research Spec

Purpose:

- full medical reasoning
- evidence citations
- ranked hypotheses
- contradiction markers
- caveats
- missing-data policy
- confirmatory tests
- marker roles
- relationship kinds
- biological narrative

Status:

```text
editable research authority
validated before compile
not runtime-read
```

### 6.2 Signal Activation Artefact

Purpose:

- deterministic signal firing
- activation logic
- lab-range / threshold rule
- primary marker
- dependencies
- override rules
- supporting marker IDs
- minimal marker semantics required for evaluation
- provenance back to source spec

This is the proper role of package files.

Packages should be regenerated from canonical research where possible.

### 6.3 Signal Intelligence Artefact

Purpose:

- ranked hypotheses
- physiological claims
- evidence strength
- contradiction markers
- missing-data policy
- confirmatory tests
- marker rationale
- pathway/mechanism explanation
- source_spec_id provenance

This artefact should be compiled from investigation specs.

It should not be hand-authored.

### 6.4 Root-Cause / WHY Artefact

Purpose:

- deterministic WHY compiler input
- root-cause/report reasoning
- structured hypothesis evaluation
- evidence-for/evidence-against logic
- missing-data handling

Target state:

```text
compiled from canonical research / signal intelligence artefact
```

Existing hand-authored root-cause YAML should be used only for comparison and adjudication, then archived or deleted from active runtime authority.

### 6.5 Health System Card Evidence Artefact

Purpose:

- domain and subsystem evidence
- marker role for card display
- score-contributor vs confidence-contributor vs contextual marker distinction
- rationale_short
- missing_policy_line
- mechanism_line
- visibility tier
- contradiction caveat lines
- suggested follow-up tests
- source_spec_id provenance

This should replace hard-coded subsystem maps.

### 6.6 Presentation Safety Metadata / IDL

Purpose:

- retail-safe wording
- phenotype and signal labels
- copy constraints
- diagnostic-safety boundaries
- suppression / softening of over-claiming language

IDL should govern how intelligence is presented. It should not be the source of clinical reasoning.

### 6.7 DTOs

Purpose:

- stable transport boundary
- carry structured intelligence from backend to frontend
- prevent frontend inference
- version user-facing contracts

DTOs should be extended only after the compiled backend artefacts are defined.

### 6.8 Frontend

Purpose:

- render DTOs
- provide layout, hierarchy and interaction
- no clinical logic
- no marker-role inference
- no fallback medical semantics

---

## 7. Identity model

The current architecture must stop treating `signal_id` as the sole identity of medical meaning.

A single biomarker direction may have multiple legitimate interpretive frames.

Example:

```text
ALT high
→ hepatocellular frame
→ metabolic / steatotic frame
→ muscle-source differential frame
```

Target identity model:

```text
research_spec_id / spec_id = unique research frame
signal_id = activation family
activation_key = runtime firing identity
hypothesis_id = interpretive frame
artefact_id = compiled runtime object
```

Required rule:

```text
No runtime registry may silently collapse multiple research frames into one signal_id.
```

---

## 8. Governance requirements

Every compiled artefact must have:

- schema
- validator
- source_spec_id traceability
- compile manifest
- input hash
- output hash
- deterministic ordering
- regression coverage
- drift detection
- Sentinel guard where appropriate

### Required schemas

Likely required new or updated schemas:

```text
knowledge_bus/schema/signal_activation_schema_v_next.yaml
knowledge_bus/schema/signal_intelligence_schema_v1.yaml
knowledge_bus/schema/root_cause_compiled_schema_v_next.yaml
knowledge_bus/schema/health_system_card_evidence_schema_v1.yaml
```

### Required validators

Likely required validators:

```text
backend/scripts/validate_signal_activation_artifact.py
backend/scripts/validate_signal_intelligence_artifact.py
backend/scripts/validate_compiled_root_cause_artifact.py
backend/scripts/validate_health_system_card_evidence.py
```

### Required compilers

Likely required compilers:

```text
backend/scripts/compile_research_to_signal_activation.py
backend/scripts/compile_research_to_signal_intelligence.py
backend/scripts/compile_signal_intelligence_to_root_cause.py
backend/scripts/compile_signal_intelligence_to_health_system_cards.py
```

### Required manifests

Each compile should emit:

```text
compile_manifest.yaml
```

Minimum fields:

```yaml
compile_id:
compiler_version:
source_contract_version:
source_specs:
  - source_spec_id:
    source_path:
    source_hash:
outputs:
  - output_path:
    output_hash:
compiled_at_utc:
compiled_by:
validator_results:
```

---

## 9. Sentinel and regression requirements

New guards should be added as the architecture is introduced.

Required Sentinel concepts:

```text
raw_research_runtime_read_forbidden
manual_card_evidence_authority_forbidden
frontend_medical_role_inference_forbidden
root_cause_pass3_drift_guard
signal_id_collision_guard
compiled_artifact_missing_source_spec_id_guard
package_without_research_provenance_guard
card_evidence_not_compiled_from_research_guard
idl_bypass_for_retail_prose_guard
```

Regression tests must prove:

- identical input produces identical output
- compiled artefacts are deterministic
- multiple research frames are not collapsed
- card evidence does not come from manual maps
- DTOs carry backend-provided roles
- frontend does not infer clinical meaning
- root-cause compiled output remains traceable to research source

---

## 10. Transition strategy

Because there are no live users, the transition should be a controlled replacement, not a compatibility-preserving migration.

Legacy layers should remain temporarily only for:

- comparison
- parity testing
- clinical adjudication
- evidence capture

They should not remain runtime authorities after the new compiled pipeline is validated.

---

# 11. Phased plan

## Phase 0 — Architectural freeze and inventory

Objective:

Establish the current baseline and prevent further drift while the replacement architecture is designed.

Actions:

1. Freeze new manual additions to:
   - root-cause YAML
   - hard-coded subsystem maps
   - package files not generated from research
   - frontend medical semantics

2. Inventory:
   - all investigation specs
   - all packages
   - all root-cause YAML files
   - all subsystem evidence maps
   - all DTO fields used by Health Systems Cards and reports
   - all runtime loaders

3. Produce a source-to-runtime traceability matrix:
   - research spec → package
   - research spec → root-cause hypothesis
   - research spec → card evidence
   - package → runtime signal
   - runtime signal → DTO field
   - DTO field → frontend component

Deliverables:

```text
docs/architecture/research_to_runtime_traceability_matrix.md
docs/architecture/legacy_intelligence_authority_inventory.md
```

STOP conditions:

- If any active runtime path cannot be traced to a source authority, record it as legacy/scaffold.
- Do not create new runtime intelligence assets during this phase.

---

## Phase 1 — Lock the canonical research contract

Objective:

Confirm the canonical research contract that all future runtime intelligence will compile from.

Actions:

1. Confirm investigation spec v3 is the accepted canonical contract.
2. Add or confirm fields required for compile provenance:
   - source_spec_id
   - signal_id
   - activation family
   - hypothesis IDs
   - relationship_kind
   - evidence source references
3. Validate all current Pass 3 specs.
4. Identify invalid, duplicate, incomplete or ambiguous specs.
5. Resolve signal/spec identity collisions at the contract level.

Deliverables:

```text
docs/architecture/canonical_research_contract_decision.md
docs/architecture/signal_spec_identity_resolution.md
```

STOP conditions:

- Do not build compilers until identity rules are decided.
- Do not continue if signal_id collision handling is undefined.
- Do not mutate v3 schema casually; schema changes require governed approval.

---

## Phase 2 — Define compiled artefact schemas

Objective:

Design the target runtime artefacts before writing compilers.

Actions:

1. Define signal activation artefact schema.
2. Define signal intelligence artefact schema.
3. Define health system card evidence schema.
4. Define compiled root-cause schema.
5. Define compile manifest schema.
6. Confirm how IDL/presentation safety metadata relates to compiled intelligence.

Deliverables:

```text
knowledge_bus/schema/signal_intelligence_schema_v1.yaml
knowledge_bus/schema/health_system_card_evidence_schema_v1.yaml
knowledge_bus/schema/compile_manifest_schema_v1.yaml
docs/architecture/compiled_runtime_artifact_model.md
```

STOP conditions:

- Do not compile overlay/card/root-cause artefacts before schemas exist.
- Do not create hand-authored compiled artefacts.
- Do not let schema design depend on frontend convenience rather than medical/runtime boundaries.

---

## Phase 3 — Build deterministic compiler foundation

Objective:

Build the research-to-runtime compile mechanism for a small pilot set.

Pilot candidates:

```text
HbA1c
CRP
ALT
homocysteine
```

Rationale:

- clinically rich
- direct Health Systems Card relevance
- known duplicate-frame/differential issues
- useful test of identity and contradiction handling

Actions:

1. Build research → signal activation compiler.
2. Build research → signal intelligence compiler.
3. Emit compile manifests.
4. Validate outputs.
5. Compare generated package/intelligence output against existing packages and root-cause YAML.
6. Capture mismatches for clinical/architecture adjudication.

Deliverables:

```text
compiled signal activation artefacts for pilot set
compiled signal intelligence artefacts for pilot set
compile manifests
compiler tests
validator tests
comparison report against legacy assets
```

STOP conditions:

- No runtime wiring in this phase.
- Do not edit existing runtime loaders.
- Do not replace root-cause/card evidence yet.
- Do not hand-correct compiler outputs except through source research or compiler logic.

---

## Phase 4 — Compile Health Systems Card evidence

Objective:

Replace hard-coded subsystem evidence with a compiled research-derived card evidence artefact.

Actions:

1. Design card-specific role translation:
   - score_contributor
   - confidence_contributor
   - contextual_marker
   - differential_marker
   - exclusion_marker
   - missing_for_confidence
   - optional_deeper_marker

2. Compile card evidence for pilot domains.
3. Add visibility tiers:
   - scored_subsystem
   - contextual_evidence
   - hidden_v1
4. Include source_spec_id traceability.
5. Validate marker inclusion/missing behaviour against legacy outputs.
6. Identify where legacy subsystem definitions are medically weak or misleading.

Deliverables:

```text
knowledge_bus/compiled/health_system_cards/wave1_health_system_evidence_v1.yaml
backend/scripts/validate_health_system_card_evidence.py
docs/architecture/card_evidence_role_translation_policy.md
```

STOP conditions:

- Do not let cards infer marker roles from scoring rails.
- Do not preserve legacy subsystem maps as authority.
- Do not expose hypothesis/contradiction text to users until IDL safety rules are agreed.

---

## Phase 5 — Runtime loader and DTO integration

Objective:

Wire runtime to compiled artefacts while keeping frontend renderer-only.

Actions:

1. Add backend loader for compiled signal intelligence.
2. Add backend loader for compiled Health Systems Card evidence.
3. Replace hard-coded card evidence assembly with compiled evidence.
4. Extend DTOs to carry:
   - marker_role
   - relationship_kind
   - rationale_short
   - missing_policy_line
   - mechanism_line
   - visibility_tier
   - source/provenance metadata where appropriate
5. Update frontend only to render new DTO fields.

Deliverables:

```text
compiled evidence loaders
updated DTO contracts
updated card assembler
frontend render-only updates
regression tests
```

STOP conditions:

- No frontend inference.
- No runtime read of raw investigation specs.
- No direct copying of research prose to retail UI without IDL control.
- No signal evaluator change unless explicitly required and classified HIGH.

---

## Phase 6 — Root-cause replacement

Objective:

Replace hand-authored root-cause YAML as a runtime authority.

Actions:

1. Compile root-cause-compatible artefacts from signal intelligence.
2. Compare with existing root-cause YAML.
3. Produce divergence report.
4. Adjudicate differences clinically/architecturally.
5. Switch root-cause compiler to compiled artefacts once coverage is sufficient.
6. Archive or delete legacy root-cause YAML from active runtime authority.

Deliverables:

```text
compiled root-cause artefacts
root-cause divergence report
root-cause compiler update
legacy root-cause archive plan
Sentinel drift guard
```

STOP conditions:

- Do not leave Pass 3 and root-cause YAML as permanent competing authorities.
- Do not switch root-cause compiler until compiled coverage is validated.
- Do not silently discard useful root-cause content; differences require adjudication.

---

## Phase 7 — Full regeneration and legacy retirement

Objective:

Move the full intelligence estate onto the day-one architecture.

Actions:

1. Compile all valid investigation specs into runtime artefacts.
2. Regenerate package/runtime activation assets.
3. Generate full signal intelligence artefacts.
4. Generate card evidence artefacts.
5. Generate root-cause artefacts.
6. Remove/deactivate hard-coded subsystem maps.
7. Remove/deactivate hand-authored root-cause YAML as active authority.
8. Remove/deactivate any packages that lack source_spec_id provenance unless explicitly retained as legacy with documented reason.

Deliverables:

```text
full compiled runtime artefact estate
legacy retirement report
runtime source authority report
launch-readiness architecture audit
```

STOP conditions:

- Do not launch with duplicate active authorities.
- Do not launch with manual subsystem maps as live authority.
- Do not launch with user-facing claims that cannot be traced to canonical research.
- Do not launch with unresolved signal_id/spec_id collision behaviour.

---

## Phase 8 — Launch-readiness gate

Objective:

Confirm the platform is architecturally safe to launch.

Required evidence:

1. Every user-facing interpretation traces to:
   - research spec
   - compiled artefact
   - runtime loader
   - DTO
   - frontend component

2. No raw research files are read at runtime.

3. No frontend component creates clinical meaning.

4. No duplicate medical authority remains active.

5. Signal/spec identity model is enforced.

6. Compilers are deterministic.

7. Validators pass.

8. Sentinel guards pass.

9. IDL/presentation safety controls are applied to retail-facing prose.

10. Health Systems Cards are populated from compiled research-derived evidence.

Deliverables:

```text
docs/audit-papers/day_one_architecture_launch_readiness_audit.md
docs/audit-papers/research_to_runtime_traceability_audit.md
```

Launch blocker examples:

- untraced clinical claim
- duplicate active authority
- raw research runtime read
- frontend role inference
- hand-authored card evidence authority
- unresolved signal/spec collision
- missing validator for compiled artefact
- missing compile manifest

---

## 12. Recommended work-package sequence

This document is not itself a work package. The likely governed sequence is:

### WP1 — Architecture inventory and traceability

```yaml
work_id: ARCH-RT-0_inventory_and_authority_trace
risk_level: STANDARD
change_type: CONTENT
objective: Produce traceability and authority inventory without code changes.
```

### WP2 — Research contract and identity lock

```yaml
work_id: ARCH-RT-1_research_contract_identity_lock
risk_level: HIGH
change_type: MIXED
objective: Resolve spec/signal/activation identity model and update governance documents/schemas if required.
```

### WP3 — Compiled artefact schema design

```yaml
work_id: ARCH-RT-2_compiled_artifact_schema_design
risk_level: HIGH
change_type: MIXED
objective: Define schemas and validators for compiled signal intelligence, card evidence and compile manifests.
```

### WP4 — Compiler pilot

```yaml
work_id: ARCH-RT-3_research_to_runtime_compiler_pilot
risk_level: HIGH
change_type: MIXED
objective: Compile pilot biomarkers from research specs into signal activation and signal intelligence artefacts.
```

### WP5 — Card evidence compiler

```yaml
work_id: ARCH-RT-4_health_system_card_evidence_compile
risk_level: HIGH
change_type: MIXED
objective: Compile Health Systems Card evidence for pilot domains and validate against legacy maps.
```

### WP6 — Runtime integration pilot

```yaml
work_id: ARCH-RT-5_runtime_loader_dto_card_integration
risk_level: HIGH
change_type: BEHAVIOUR
objective: Wire compiled card evidence into backend DTOs while preserving frontend render-only boundary.
```

### WP7 — Root-cause replacement pilot

```yaml
work_id: ARCH-RT-6_compiled_root_cause_pilot
risk_level: HIGH
change_type: MIXED
objective: Compile root-cause artefacts from signal intelligence and compare/replace pilot hand-authored YAML.
```

### WP8 — Full estate regeneration

```yaml
work_id: ARCH-RT-7_full_research_runtime_regeneration
risk_level: HIGH
change_type: MIXED
objective: Regenerate all runtime intelligence artefacts from canonical research and retire legacy authorities.
```

### WP9 — Launch-readiness audit

```yaml
work_id: ARCH-RT-8_day_one_architecture_launch_gate
risk_level: STANDARD
change_type: CONTENT
objective: Produce final traceability and architecture-readiness audit before launch.
```

---

## 13. What must not happen

The following are prohibited unless explicitly reversed by architectural decision:

1. Do not read Pass 3 / investigation specs directly at runtime.
2. Do not manually expand hard-coded subsystem evidence maps as the strategic solution.
3. Do not let frontend infer marker roles, rationales or clinical meaning.
4. Do not copy research prose directly into retail UX without IDL/presentation safety control.
5. Do not keep root-cause YAML as a permanent independent hypothesis authority.
6. Do not stuff full hypothesis graphs into signal activation package files.
7. Do not create hand-authored intelligence overlay files for specs that already exist in canonical research.
8. Do not launch with unresolved signal_id/spec_id collision behaviour.
9. Do not create new duplicate SSOTs for card evidence, marker roles or hypothesis framing.
10. Do not treat legacy runtime adjacency as proof of architectural correctness.

---

## 14. Long-term consequences avoided by this plan

Correcting the architecture before launch avoids:

- product quality ceiling
- clinically thin cards/reports
- silent divergence between medical authorities
- weak provenance for user-facing claims
- expensive post-launch migration
- polluted longitudinal dataset
- poor regulatory readiness
- reduced acquisition defensibility
- brittle frontend-driven semantics
- inability to prove deterministic reasoning

This is not a cosmetic refactor. It is foundational company architecture.

---

## 15. Review questions for Claude Code and Cursor

Reviewers should challenge this plan against the actual codebase.

Specific questions:

1. Does the proposed day-one architecture reflect the true current codebase constraints?
2. Are there any hidden runtime dependencies that make legacy authority retirement harder than described?
3. Are the proposed artefact boundaries correct?
4. Should signal intelligence and card evidence be separate artefacts, or should card evidence be a compiled projection from signal intelligence only?
5. Is the proposed identity model sufficient to resolve signal_id collision and multi-frame interpretation?
6. Which current packages cannot be regenerated from existing investigation specs?
7. Which root-cause YAML files contain content not present in Pass 3 and therefore require adjudication?
8. Which current DTOs need extension versus replacement?
9. What is the smallest safe compiler pilot that proves the architecture?
10. What hard STOP conditions are missing?

---

## 16. Final architectural position

HealthIQ should now return to the architecture it should have had from day one.

The target is not a patched version of the current system.

The target is:

```text
canonical research authority
→ deterministic compiler suite
→ governed runtime artefacts
→ runtime loaders
→ structured DTOs
→ frontend render-only
```

The current fragmented architecture should be treated as scaffolding. It should be used for comparison and evidence only, then retired.

This correction should happen before launch, while there are no live users and no backward-compatibility burden.

Once daily users exist, this correction becomes slower, riskier, more expensive and commercially more damaging.

