# HealthIQ AI — As-Is to Day-One Architecture Transition Plan v2

**Document purpose:**  
Define the corrected plan to move HealthIQ AI from the current fragmented research/runtime architecture to the proper day-one architecture before product launch.

**Version:** v2 — revised after Cursor and Claude Code architecture challenge  
**Status:** Draft for second-pass review  
**Implementation status:** No code changes authorised by this document  
**Intended reviewers:** GPT Head of Architecture, Claude Code, Cursor, human product/technical owner

---

## 1. Executive summary

HealthIQ should still move to a governed research-to-runtime architecture before launch.

The target architecture remains:

```text
canonical research spec
→ validation
→ deterministic compile
→ governed runtime artefacts
→ runtime loaders
→ structured DTOs
→ frontend render-only
```

However, v1 of this plan incorrectly treated some existing governed assets as if they did not exist. The most important correction is that HealthIQ already has a governed signal-intelligence artefact:

```text
Promoted Signal Intelligence / PSI
```

Therefore, this plan must not create a duplicate “Signal Intelligence Artefact” unless ADR-008 is explicitly reversed.

The corrected architecture is:

```text
investigation_spec v3
  ├─→ signal activation package                 [signal_library / research_brief]
  ├─→ promoted_signal_intelligence / PSI        [existing signal-layer semantics]
  ├─→ compiled hypothesis artefact              [NEW — WHY / root-cause]
  └─→ compiled Health Systems Card evidence     [NEW — UX projection]
```

The core issue is no longer “build a signal-intelligence layer from scratch.”  
The real issue is:

1. PSI exists but is not fully opted into or consumed across the runtime estate.
2. Hypothesis intelligence remains duplicated between Pass 3 and hand-authored root-cause YAML.
3. Health Systems Card evidence remains hard-coded in Python and does not consume governed research-derived intelligence.
4. Signal identity and duplicate signal_id behaviour remain unsafe.
5. Compile manifests, provenance enforcement and estate-wide drift controls are incomplete.

Because there are no live users, HealthIQ should not preserve bad runtime architecture for backward compatibility. Legacy assets should remain only for parity testing, comparison and adjudication, then be retired or demoted.

---

## 2. Corrected as-is diagnosis

### 2.1 Canonical research source exists

The upstream research source is the investigation spec v3 / Pass 3 corpus.

It contains the richest structured medical intelligence currently available to HealthIQ, including:

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
- mechanism / biological pathway / interpretation / implications narrative

This should remain the canonical upstream research authority.

Raw investigation specs must not be read at runtime.

---

### 2.2 Signal activation artefact already exists

The signal activation artefact is the current Knowledge Bus package structure, primarily:

```text
signal_library.yaml
research_brief.yaml
package_manifest.yaml
```

There appear to be at least two generations of package maturity:

1. older hand-authored or partially governed packages
2. newer governed `pkg_s24_*` / later packages backed by investigation specs

The plan must distinguish these generations because retirement and regeneration rules differ.

Package files should remain the activation/firing authority, not the whole medical intelligence warehouse.

---

### 2.3 Promoted Signal Intelligence already exists

The signal-layer intelligence artefact already exists and should be recognised as such.

Existing assets include:

```text
knowledge_bus/schema/promoted_signal_intelligence_schema_v1.yaml
backend/core/knowledge/investigation_spec_to_promoted_signal.py
backend/core/knowledge/load_promoted_signal_intelligence.py
signal_intelligence_translation_rules_v1.yaml
```

This means the transition plan should not propose a new generic signal-intelligence schema that competes with PSI.

The open questions are:

- which packages/specs have PSI coverage
- which packages opt into PSI through package manifests
- whether PSI is actually consumed in the relevant runtime paths
- whether PSI coverage is complete enough for the new day-one architecture
- what Sentinel guard is required where PSI exists but is not consumed

---

### 2.4 PSI is not the hypothesis layer

The current PSI contract intentionally excludes hypotheses, hypothesis ranking and narrative at the root level.

This reflects the existing ADR-008 architecture decision: signal-layer intelligence and hypothesis/WHY intelligence are separate.

This plan accepts ADR-008 unless a later architecture decision explicitly reverses it.

Therefore:

```text
PSI = signal-layer semantics
compiled hypothesis artefact = WHY / root-cause intelligence
Health Systems Card evidence = UX projection
```

Do not overload PSI with full hypothesis graphs.

---

### 2.5 IDL / presentation safety already exists

The Interpretation Display Layer and retail explainer safety layer already exist.

Relevant assets include, but may not be limited to:

```text
InterpretationDisplayLayerBundleV1
backend/ssot/retail_explainer_v1/registry.yaml
domain_narrative_wave1
interpretation_display_layer_publish_v1
```

The revised plan should treat IDL/presentation safety as an existing layer to coordinate with and extend where necessary, not as a greenfield layer.

IDL should govern how intelligence is shown. It should not become the source of clinical reasoning.

---

### 2.6 Root-cause YAML is a purpose-built WHY layer, not raw research

The current root-cause hypothesis YAML files are not raw research files.

They are a separate, hand-authored WHY layer under:

```text
knowledge_bus/root_cause/hypotheses/
```

They are loaded and registered through:

```text
load_root_cause_hypotheses.py
root_cause_registry_v1.py
root_cause_compiler_v1.py
```

They currently contain formatted interpretive material such as:

- hypothesis_id
- title
- summary_template
- evidence_for_rules
- evidence_against_rules
- missing data markers
- confirmatory test references

They are functional, but they are a duplicate authority where they overlap with investigation spec hypotheses.

Target state:

```text
investigation_spec hypotheses
→ compiled hypothesis artefact
→ root-cause / WHY compiler
```

Existing root-cause YAML should be retained temporarily for parity and divergence review, then retired from active authority.

---

### 2.7 Health Systems Card evidence is currently hard-coded Python

The current Health Systems Card evidence authority is not a governed YAML file.

It is hard-coded Python, likely in:

```text
backend/core/analytics/wave1_subsystem_evidence.py
```

This must be replaced with a compiled card evidence artefact and backend loader.

The replacement requires more than writing a YAML file. It requires:

- compiled card evidence schema
- validator
- loader
- assembler change
- DTO versioning
- tests
- Sentinel guard preventing Python map authority after cutover

---

### 2.8 Runtime duplicate signal behaviour is unsafe

The SignalRegistry currently appears to collapse duplicate `signal_id` entries by path/order policy.

This violates the target rule:

```text
No runtime registry may silently collapse multiple research frames into one signal identity.
```

This must be addressed before full regeneration.

The exact solution is not yet decided. The plan should not assume `activation_key` must be implemented, but it must require an early architecture decision on whether:

```text
signal_id + spec_id
```

is sufficient, or whether a new runtime firing identity such as:

```text
activation_key
```

is required.

---

## 3. Corrected target architecture

The day-one architecture should be:

```text
Canonical Research Spec
   ↓
Research Validator
   ↓
Compile / Translation Layer
   ├── Signal Activation Package
   ├── Promoted Signal Intelligence / PSI
   ├── Compiled Hypothesis Artefact
   └── Health System Card Evidence Artefact
   ↓
Runtime Loaders
   ↓
Analysis Orchestrator / Compilers / Assemblers
   ↓
Structured InsightGraph / Report / Card DTOs
   ↓
Frontend Render Only
```

The non-negotiable principles are:

1. one canonical upstream research authority
2. multiple purpose-specific compiled runtime views
3. no hand-authored duplicate medical authorities as active runtime sources
4. no raw research runtime reads
5. no frontend medical inference
6. no silent signal/spec identity collapse
7. every user-facing clinical claim traceable to source research and compiled runtime artefact

---

## 4. Corrected artefact model

### 4.1 Investigation spec v3

Role:

```text
canonical upstream research authority
```

Contains:

- signal identity
- biomarker relationships
- marker roles
- relationship_kind
- rationale
- hypotheses
- contradiction markers
- missing-data policy
- confirmatory tests
- evidence
- narrative research content

Runtime status:

```text
not runtime-read
compile-time only
```

---

### 4.2 Signal activation package

Role:

```text
runtime signal firing authority
```

Current artefact:

```text
signal_library.yaml
research_brief.yaml
package_manifest.yaml
```

Contains:

- primary marker
- activation logic
- threshold / lab-range condition
- dependencies
- override rules
- supporting marker IDs
- minimal signal metadata
- source_spec_id provenance where available

Should not contain:

- full ranked hypothesis graph
- contradiction graph
- card-specific evidence
- retail copy
- root-cause output templates

---

### 4.3 Promoted Signal Intelligence / PSI

Role:

```text
governed signal-layer semantics
```

Existing artefact:

```text
promoted_signal_intelligence.yaml
```

Existing schema:

```text
knowledge_bus/schema/promoted_signal_intelligence_schema_v1.yaml
```

Contains or should contain:

- signal-level semantic enrichment
- relationship_kind
- marker role/rationale where contract allows
- translation provenance
- source investigation spec link

Should not contain unless ADR-008 is reversed:

- full hypotheses
- hypothesis ranking
- root-cause narrative graph

---

### 4.4 Compiled hypothesis artefact

Role:

```text
NEW governed WHY/root-cause source
```

Purpose:

- represent investigation spec hypotheses in a deterministic runtime-compatible form
- replace or feed root-cause compiler inputs
- eliminate permanent hand-authored root-cause duplicate authority

Likely contains:

- source_spec_id
- signal_id
- hypothesis_id
- physiological_claim
- hypothesis rank
- evidence strength
- caveats
- contradiction markers
- missing-data policy
- confirmatory test references mapped to registry IDs
- deterministic evidence_for/evidence_against rule representation, if root-cause compiler still needs that shape

Open design question:

```text
Should root_cause_compiler_v1 consume this new hypothesis artefact directly,
or should a second compile step emit root-cause-compatible YAML from it?
```

This must be decided before implementation.

---

### 4.5 Health System Card Evidence artefact

Role:

```text
NEW compiled UX projection for Health Systems Cards
```

Purpose:

- replace hard-coded Python subsystem evidence
- make card evidence research-derived and governed
- keep frontend render-only

Likely contains:

- domain_id
- subsystem_id
- visibility_tier
- marker list
- marker_role
- relationship_kind
- rationale_short
- missing_policy_line
- mechanism_line
- contradiction caveat line
- optional follow-up test references
- source_spec_ids
- compile provenance

Visibility tiers should include:

```text
scored_subsystem
contextual_evidence
hidden_v1
```

Card evidence should be compiled from canonical research plus medical review/domain mapping policy. It should not be hand-authored as a new authority.

---

### 4.6 IDL / presentation safety

Role:

```text
presentation and retail-safety control
```

Existing IDL and retail explainer assets must remain part of the pathway.

IDL should:

- govern consumer-safe labels and language
- prevent over-claiming
- coordinate with card/report output
- sanitise or constrain surfaced prose

IDL should not:

- originate clinical reasoning
- infer hypotheses
- replace research-derived evidence
- become a parallel medical authority

---

### 4.7 DTOs

Role:

```text
versioned backend-to-frontend transport contract
```

Current DTOs likely need versioned extension rather than casual mutation.

Potential affected DTOs:

- `SubsystemEvidenceV1`
- `ConsumerDomainScoreV1`
- card marker display model
- report/root-cause output models if hypothesis compilation changes runtime output

Required fields for card evidence may include:

- marker_role
- relationship_kind
- rationale_short
- missing_policy_line
- mechanism_line
- visibility_tier

The frontend should render these fields only. It must not infer them.

---

## 5. Identity model decision

The target identity model must separate research frame, signal family and hypothesis meaning.

### Required identities

```text
spec_id / research_spec_id = unique research frame
signal_id = signal family / activation family
hypothesis_id = WHY interpretation frame
package_id = activation package identity
artefact_id = compiled artefact identity
compile_id = compile run identity
```

### Open decision: activation_key

The v1 plan introduced `activation_key` as a runtime firing identity.

Reviewers correctly identified that `activation_key` does not currently exist and may be expensive to introduce.

Therefore the revised position is:

```text
Do not assume activation_key implementation.
Do require an early architecture decision on duplicate signal_id behaviour.
```

The first architecture work package must answer:

1. Can `signal_id + spec_id` safely solve the multi-frame problem?
2. Does the SignalRegistry need a new keying policy?
3. Does SignalEvaluator need to emit frame-level identity?
4. Do InsightGraph, interaction maps, phenotype maps or report compilers depend on signal_id uniqueness?
5. If activation_key is required, what is its exact format and blast radius?

No full regeneration should occur until this is resolved.

---

## 6. Corrected transition strategy

Because HealthIQ has no live users, this should be a controlled replacement, not a backwards-compatibility migration.

However, replacement still requires a shadow/parity period.

Legacy assets should be retained temporarily for:

- diffing
- parity testing
- clinical adjudication
- regression evidence
- launch-readiness proof

Legacy assets should not remain active runtime authorities after replacement gates pass.

---

# 7. Revised phased plan

## Phase 0 — Inventory, authority map and corrected baseline

Objective:

Create a complete repo-reality inventory before writing implementation work packages.

This phase combines the previous v1 Phase 0 and Phase 1.

Actions:

1. Inventory all investigation specs.
2. Inventory all packages by generation:
   - pre-s24 / legacy
   - s24 / governed
   - later governed packages
3. Inventory all PSI artefacts and package manifest opt-ins.
4. Inventory all root-cause hypothesis YAML files.
5. Inventory root_cause_registry_v1.py registrations.
6. Inventory Health Systems Card hard-coded Python subsystem evidence.
7. Inventory IDL / retail explainer dependencies that affect cards and reports.
8. Inventory interaction map / phenotype map / calibration / confirmatory-test registry dependencies.
9. Produce traceability matrix:
   - spec → package
   - spec → PSI
   - spec → root-cause YAML
   - spec → card evidence
   - package → SignalRegistry
   - signal → DTO
   - DTO → frontend

Deliverables:

```text
docs/architecture/research_to_runtime_traceability_matrix.md
docs/architecture/intelligence_authority_inventory.md
docs/architecture/psi_coverage_and_manifest_opt_in_report.md
docs/architecture/root_cause_registry_inventory.md
docs/architecture/legacy_package_retirement_candidates.md
```

STOP conditions:

- Do not create new schemas before inventory confirms actual gaps.
- Do not create a duplicate signal-intelligence artefact.
- Do not proceed if PSI coverage and opt-in status are unknown.
- Do not proceed if duplicate signal_id behaviour is not documented.

---

## Phase 1 — Identity, ADR and governance decisions

Objective:

Resolve the architecture decisions that block safe compiler/runtime work.

Required decisions:

1. Accept or reverse ADR-008.
2. Confirm PSI remains signal-layer only.
3. Confirm hypotheses require a separate compiled hypothesis artefact.
4. Decide how duplicate signal_id / multi-frame signals are handled.
5. Decide whether activation_key is needed.
6. Decide how compiled artefacts are promoted and recorded in Knowledge Bus status.
7. Decide compile manifest storage convention.
8. Decide how root_cause_registry_v1.py transitions from manual tuple registration to compiled artefact discovery or generated registry.

Deliverables:

```text
docs/architecture/ADR-RT-001_research_to_runtime_day_one_architecture.md
docs/architecture/ADR-RT-002_signal_spec_identity_and_registry_policy.md
docs/architecture/ADR-RT-003_hypothesis_artefact_and_root_cause_transition.md
docs/architecture/compile_manifest_storage_policy.md
```

STOP conditions:

- No compiler/runtime work until signal/spec identity policy is approved.
- No hypothesis schema work until ADR-008 alignment is resolved.
- No registry refactor until blast radius across SignalRegistry, SignalEvaluator, InsightGraph and interaction maps is understood.

---

## Phase 2 — Fill existing signal-layer gaps before inventing new layers

Objective:

Use and complete existing PSI infrastructure rather than duplicating it.

Actions:

1. Validate determinism of existing PSI translator:
   - same spec input
   - repeated translator runs
   - identical output
2. Identify specs/packages without PSI.
3. Identify packages with PSI on disk but not opted into package manifests.
4. Identify runtime paths where PSI exists but is not consumed.
5. Add missing validation around source spec existence/hash where required.
6. Decide whether PSI loader is sufficient or needs runtime integration changes.

Deliverables:

```text
docs/architecture/psi_gap_analysis.md
docs/architecture/psi_runtime_consumption_gap_report.md
docs/architecture/promoted_signal_intelligence_validation_gap_report.md
```

Potential code deliverables, only after formal WP approval:

```text
validator updates for PSI provenance
Sentinel guard for PSI-present-but-not-consumed
manifest opt-in correction where appropriate
```

STOP conditions:

- Do not create a new signal intelligence schema.
- Do not hand-author PSI files where a valid investigation spec exists.
- Do not route PSI into retail output without IDL/presentation boundary review.

---

## Phase 3 — Compile manifest and provenance infrastructure

Objective:

Introduce compile manifest infrastructure that all generated runtime artefacts can share.

Actions:

1. Define compile manifest schema.
2. Define manifest storage convention:
   - per artefact directory
   - per compile run
   - or estate-level manifest
3. Define required manifest fields:
   - compile_id
   - compiler_version
   - source_spec_id
   - source_path
   - source_hash
   - output_path
   - output_hash
   - remap_contract_version
   - translation_rules_version
   - target_package_id
   - package_id
   - signal_id
   - hypothesis_id where relevant
   - compiled_at_utc
   - validator result
4. Add a validation layer that checks source spec still exists and hash still matches compiled output.

Deliverables:

```text
knowledge_bus/schema/compile_manifest_schema_v1.yaml
docs/architecture/compile_manifest_contract.md
```

STOP conditions:

- No full regeneration without manifest infrastructure.
- No compiled card/hypothesis artefacts without source hash traceability.
- No package promotion without validator result and manifest reference.

---

## Phase 4 — Pilot existing compile path using a real gap

Objective:

Prove compile/provenance mechanics on an actual gap, not a biomarker that is already fully covered.

Pilot selection rule:

Do not hardcode HbA1c, CRP, ALT or homocysteine as the first pilot.

Instead, Phase 0 inventory must identify a pilot candidate that has:

1. a valid investigation spec
2. an existing or expected package relationship
3. missing PSI opt-in or missing PSI artefact
4. simple single-frame identity where possible
5. low runtime blast radius

Possible example if inventory supports it:

```text
LDL or another clean single-frame marker
```

Actions:

1. Select pilot based on inventory evidence.
2. Run existing investigation_spec → PSI translator where applicable.
3. Compare generated PSI to package/research expectations.
4. Validate deterministic output.
5. Emit compile manifest.
6. Do not wire into runtime yet unless explicitly scoped.

Deliverables:

```text
pilot PSI artefact or manifest correction
compile manifest
determinism test
gap closure report
```

STOP conditions:

- No runtime wiring in this phase.
- No multi-frame signal pilot until duplicate signal_id policy is resolved.
- No CRP pilot if it forces activation compile, legacy retirement and registry change in the same work package.

---

## Phase 5 — Multi-frame identity pilot

Objective:

Prove the registry/identity model before full regeneration.

Recommended candidate:

```text
ALT multi-frame case
```

Rationale:

ALT can represent multiple interpretive frames and is useful for proving whether `signal_id + spec_id` is sufficient or whether a separate runtime firing identity is required.

Actions:

1. Select multi-frame case from inventory.
2. Identify all related investigation specs.
3. Identify all related packages.
4. Identify root-cause YAML overlap.
5. Identify SignalRegistry collision behaviour.
6. Test proposed identity policy.
7. Update registry/evaluator only if required by approved ADR.

Deliverables:

```text
multi_frame_identity_test_report.md
SignalRegistry collision report
approved implementation decision
```

STOP conditions:

- No full regeneration until duplicate signal handling is resolved.
- No silent lexicographic overwrite allowed in target state.
- No interaction map or phenotype map changes without review.

---

## Phase 6 — Health Systems Card evidence artefact

Objective:

Replace hard-coded Python subsystem evidence with compiled, research-derived card evidence.

Actions:

1. Define card evidence schema.
2. Define card role translation policy:
   - score_contributor
   - confidence_contributor
   - contextual_marker
   - mechanism_marker
   - differential_marker
   - exclusion_marker
   - missing_for_confidence
   - optional_deeper_marker
3. Define visibility-tier policy using medical review:
   - scored_subsystem
   - contextual_evidence
   - hidden_v1
4. Compile one card subsystem from research-derived inputs.
5. Validate against legacy hard-coded output.
6. Add loader.
7. Extend DTOs using versioned model if needed.
8. Update frontend only to render backend fields.

Recommended pilot:

```text
one Health Systems Card subsystem identified from Phase 0 inventory
```

Cursor suggests glycaemic subsystem; Claude suggests cardiovascular lipid transport. The final pilot should be chosen after inventory, based on cleanest authority chain.

Deliverables:

```text
knowledge_bus/schema/health_system_card_evidence_schema_v1.yaml
knowledge_bus/compiled/health_system_cards/<pilot>.yaml
backend loader
validator
DTO v2 or schema-versioned DTO extension
frontend render-only update if authorised
```

STOP conditions:

- No card role inference in frontend.
- No hard-coded Python subsystem authority after cutover.
- No retail hypothesis prose without IDL review.
- No DTO extension before artefact schema and validator pass.

---

## Phase 7 — Compiled hypothesis artefact and root-cause transition

Objective:

Eliminate permanent duplicate authority between investigation spec hypotheses and hand-authored root-cause YAML.

Actions:

1. Define compiled hypothesis artefact schema.
2. Map investigation spec hypotheses to runtime WHY/root-cause needs.
3. Decide whether to:
   - make root_cause_compiler consume compiled hypothesis artefact directly
   - or compile a root-cause-compatible view from the hypothesis artefact
4. Map Pass 3 confirmatory_tests to confirmatory test registry IDs.
5. Generate pilot compiled hypothesis artefact.
6. Compare against existing root-cause YAML.
7. Produce divergence report.
8. Adjudicate differences clinically/architecturally.
9. Replace or generate root-cause registry entries.
10. Plan transition from manual root_cause_registry_v1.py tuple to generated registry or auto-discovery.

Deliverables:

```text
knowledge_bus/schema/compiled_hypothesis_schema_v1.yaml
compiled hypothesis pilot artefact
root-cause divergence report
root_cause_registry transition design
confirmatory test mapping validation
```

STOP conditions:

- Do not switch root_cause_compiler to compiled artefacts until registry transition is solved.
- Do not discard useful root-cause YAML content without divergence adjudication.
- Do not allow Pass 3 and root-cause YAML to remain permanent competing authorities.
- Do not compile confirmatory tests unless test IDs map to registry or are explicitly flagged.

---

## Phase 8 — Runtime integration and shadow mode

Objective:

Wire compiled artefacts into runtime behind validation and shadow comparison.

Actions:

1. Runtime loader for card evidence.
2. Runtime loader or opt-in enforcement for PSI where applicable.
3. Runtime loader for compiled hypothesis artefact or generated root-cause view.
4. DTO extensions.
5. Shadow-mode comparison:
   - current output
   - compiled output
   - differences captured
6. Regression and golden fixture updates.
7. Sentinel guards registered.
8. Internal QA review before cutover.

Deliverables:

```text
runtime loaders
DTO updates
shadow comparison report
regression fixture updates
Sentinel guard registration
```

STOP conditions:

- No direct raw investigation spec runtime reads.
- No frontend clinical inference.
- No retail prose bypassing IDL.
- No runtime cutover until shadow diff is reviewed.

---

## Phase 9 — Full regeneration and legacy retirement

Objective:

Move the estate onto the corrected day-one architecture.

Actions:

1. Compile all valid investigation specs into required runtime artefacts.
2. Ensure all active packages have source_spec_id provenance or explicit legacy-retained classification.
3. Ensure PSI coverage/opt-in is complete where required.
4. Generate Health Systems Card evidence estate.
5. Generate compiled hypothesis/root-cause estate.
6. Retire hard-coded Python subsystem evidence as active authority.
7. Retire hand-authored root-cause YAML as active authority after divergence adjudication.
8. Retire packages that are legacy duplicates or unresolved authority conflicts.
9. Update latest knowledge status / estate manifest.

Deliverables:

```text
full compiled artefact estate
legacy retirement report
active authority manifest
launch architecture evidence pack
```

STOP conditions:

- Do not launch with unclassified active packages lacking provenance.
- Do not launch with manual card evidence as authority.
- Do not launch with duplicate active hypothesis authorities.
- Do not launch with unresolved duplicate signal_id collapse behaviour.

---

## Phase 10 — Day-one launch-readiness gate

Objective:

Prove that HealthIQ is ready to launch on the corrected architecture.

Required evidence:

1. Every user-facing clinical interpretation traces to:
   - investigation spec
   - compiled artefact
   - runtime loader
   - DTO
   - frontend component

2. No raw research runtime reads exist.

3. No frontend component creates medical meaning.

4. No duplicate active authority remains.

5. Signal/spec identity policy is enforced.

6. Compilers are deterministic.

7. Validators pass.

8. Compile manifests are present and hash-valid.

9. Sentinel guards pass.

10. IDL/presentation safety controls are applied to retail-facing prose.

11. Health Systems Cards are populated from compiled research-derived evidence.

Deliverables:

```text
docs/audit-papers/day_one_architecture_launch_readiness_audit.md
docs/audit-papers/research_to_runtime_traceability_audit.md
docs/audit-papers/active_intelligence_authority_manifest.md
```

Launch blockers include:

- untraced clinical claim
- duplicate active authority
- raw research runtime read
- frontend role inference
- hard-coded card evidence authority
- unresolved duplicate signal_id collapse
- missing validator
- missing compile manifest
- missing source_spec_id provenance on active package without legacy classification

---

## 8. Revised work-package sequence

This paper is not itself a work package.

Likely governed sequence:

### WP0 — Corrected inventory and authority trace

```yaml
work_id: ARCH-RT-0_inventory_authority_trace
risk_level: STANDARD
change_type: CONTENT
objective: Produce complete repo-reality inventory, PSI coverage, package generation classification, root-cause registry inventory and authority traceability matrix.
```

### WP1 — Identity and ADR alignment

```yaml
work_id: ARCH-RT-1_identity_adr_alignment
risk_level: HIGH
change_type: MIXED
objective: Resolve ADR-008 alignment, hypothesis artefact boundary, duplicate signal_id policy, possible activation_key need, and registry transition principles.
```

### WP2 — PSI gap closure and manifest foundation

```yaml
work_id: ARCH-RT-2_psi_gap_manifest_foundation
risk_level: HIGH
change_type: MIXED
objective: Reuse existing PSI infrastructure, close manifest/provenance validation gaps, and introduce compile manifest contract.
```

### WP3 — Single-frame compile/provenance pilot

```yaml
work_id: ARCH-RT-3_single_frame_compile_pilot
risk_level: HIGH
change_type: MIXED
objective: Use inventory-selected gap candidate to prove deterministic PSI/package provenance and manifest mechanics without runtime wiring.
```

### WP4 — Multi-frame identity pilot

```yaml
work_id: ARCH-RT-4_multi_frame_identity_pilot
risk_level: HIGH
change_type: MIXED
objective: Prove duplicate signal_id / multi-frame identity policy before full regeneration.
```

### WP5 — Health Systems Card evidence pilot

```yaml
work_id: ARCH-RT-5_card_evidence_compile_pilot
risk_level: HIGH
change_type: MIXED
objective: Compile one Health Systems Card evidence subsystem from governed research-derived assets and replace hard-coded card evidence for that pilot path.
```

### WP6 — Compiled hypothesis/root-cause pilot

```yaml
work_id: ARCH-RT-6_compiled_hypothesis_root_cause_pilot
risk_level: HIGH
change_type: MIXED
objective: Create compiled hypothesis artefact and transition one root-cause path from hand-authored YAML to compiled research-derived authority with divergence review.
```

### WP7 — Runtime integration shadow mode

```yaml
work_id: ARCH-RT-7_runtime_shadow_integration
risk_level: HIGH
change_type: BEHAVIOUR
objective: Wire compiled artefacts into runtime under shadow comparison and DTO versioning before cutover.
```

### WP8 — Full regeneration and legacy retirement

```yaml
work_id: ARCH-RT-8_full_regeneration_legacy_retirement
risk_level: HIGH
change_type: MIXED
objective: Regenerate the active intelligence estate and retire/demote legacy authorities.
```

### WP9 — Day-one architecture launch gate

```yaml
work_id: ARCH-RT-9_day_one_launch_gate
risk_level: STANDARD
change_type: CONTENT
objective: Produce launch-readiness architecture audit and active authority manifest.
```

---

## 9. Explicit non-goals

Unless specifically authorised in a later work package, this transition does not change:

- biomarker reference ranges
- unit conversion policy
- scoring rail weights
- cluster/burden scoring logic
- calibration rules
- frontend design language
- IDL wording
- retail explainer copy
- clinical thresholds
- medical claims outside the compiled research authority

---

## 10. Prohibited shortcuts

The following must not happen:

1. Do not create a duplicate signal-intelligence artefact beside PSI.
2. Do not reverse ADR-008 silently.
3. Do not stuff full hypothesis graphs into signal_library.yaml.
4. Do not read raw investigation specs at runtime.
5. Do not keep hand-authored root-cause YAML as a permanent independent authority.
6. Do not keep hard-coded Python subsystem evidence as a permanent authority.
7. Do not let frontend infer marker roles, rationales or clinical meaning.
8. Do not copy research prose into retail UX without IDL/presentation safety.
9. Do not launch with packages lacking either source_spec_id provenance or explicit legacy-retained classification.
10. Do not allow SignalRegistry to silently collapse duplicate signal_id frames in the target architecture.
11. Do not write work packages from this plan until second-pass review confirms the corrected baseline.

---

## 11. Key questions for second-pass review

Claude Code and Cursor should review this revised plan and answer:

1. Does v2 now correctly reflect the existing PSI / ADR-008 architecture?
2. Is accepting ADR-008 the right decision, or should it be reversed?
3. Is the proposed split correct:
   - packages = activation
   - PSI = signal-layer semantics
   - compiled hypothesis artefact = WHY/root-cause
   - card evidence artefact = UX projection
4. Is `activation_key` still needed, or can signal_id + spec_id safely resolve multi-frame identity?
5. What exactly must change in SignalRegistry to stop silent duplicate collapse?
6. What is the correct transition path for root_cause_registry_v1.py?
7. What is the correct pilot candidate after inventory?
8. Which runtime loaders or DTOs are missing from this plan?
9. Are compile manifests per artefact, per run, or estate-level?
10. Are any STOP conditions still missing?
11. Which phase is still too broad for a single Automation Bus work package?
12. What would block launch if unresolved?

---

## 12. Final architectural position

The strategic target remains unchanged:

```text
canonical research authority
→ deterministic compile
→ governed runtime artefacts
→ runtime loaders
→ structured DTOs
→ frontend render-only
```

The corrected implementation route is now different from v1:

```text
Do not build a new signal-intelligence layer.
Use and complete PSI.

Do not overload PSI with hypotheses.
Create a separate compiled hypothesis artefact.

Do not manually repair Health Systems Cards.
Replace Python subsystem evidence with compiled card evidence.

Do not preserve legacy root-cause YAML as authority.
Use it for parity, divergence review and adjudication, then retire it.

Do not ignore duplicate signal_id behaviour.
Resolve registry identity before full regeneration.
```

This is the right pre-launch correction. It should be completed before HealthIQ has a live user base.

