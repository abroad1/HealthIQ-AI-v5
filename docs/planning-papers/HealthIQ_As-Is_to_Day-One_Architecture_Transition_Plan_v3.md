# HealthIQ AI — As-Is to Day-One Architecture Transition Plan v3

**Document purpose:**  
Define the corrected plan to move HealthIQ AI from the current fragmented research/runtime architecture to the proper day-one architecture before product launch.

**Version:** v3 — revised after Cursor and Claude Code second-pass review  
**Status:** Draft for final confirmation before WP0 authoring  
**Implementation status:** No code changes authorised by this document  
**Intended reviewers:** GPT Head of Architecture, Claude Code, Cursor, human product/technical owner

---

## 1. Executive summary

HealthIQ should correct its research-to-runtime architecture before launch.

The target architecture remains:

```text
canonical research spec
→ validation
→ deterministic compile / translation
→ governed runtime artefacts
→ runtime loaders
→ structured DTOs
→ frontend render-only
```

The strategic direction is now agreed.

The remaining issue is not the destination. It is accurate scoping from the actual codebase baseline.

This v3 paper incorporates the key second-pass findings:

1. Promoted Signal Intelligence / PSI already exists, but it is consumed by zero runtime analytics paths.
2. Multi-frame signal collapse is not a theoretical risk; it is a live runtime defect caused by `signal_id`-only registry behaviour.
3. Package maturity is not a simple two-generation picture; the package estate spans multiple generations with different source and PSI coverage.
4. `SubsystemEvidenceV1` definitely lacks the fields needed for Health Systems Card intelligence; DTO versioning is mandatory.
5. Several proposed work packages in v2 were too broad and mixed CONTENT and BEHAVIOUR work.
6. The identity decision must explicitly answer whether HealthIQ supports one frame per biomarker direction or multiple frames per direction.

The corrected target compile graph is:

```text
investigation_spec v3
  ├─→ signal activation package                  [signal_library / research_brief]
  ├─→ promoted_signal_intelligence / PSI         [existing signal-layer semantics]
  ├─→ compiled hypothesis artefact               [NEW — WHY / root-cause]
  └─→ compiled Health Systems Card evidence      [NEW — UX projection]
```

The corrected implementation posture is:

```text
Do not invent a duplicate signal-intelligence layer.
Use and complete PSI.

Do not overload PSI with hypotheses.
Create a separate compiled hypothesis artefact.

Do not manually repair card evidence long-term.
Replace hard-coded Python subsystem evidence with compiled card evidence.

Do not leave root-cause YAML as permanent authority.
Use it for parity and divergence adjudication, then retire it.

Do not launch while signal_id-only registry behaviour silently discards valid research frames.
```

This plan should now be reviewed only for final confirmation that it is accurate enough to author WP0.

---

## 2. Current as-is baseline

### 2.1 Canonical research source

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

This remains the canonical upstream research authority.

Raw investigation specs must not be read at runtime.

---

### 2.2 Signal activation artefact already exists

The signal activation artefact is the Knowledge Bus package structure:

```text
signal_library.yaml
research_brief.yaml
package_manifest.yaml
```

These packages are used by the SignalRegistry / SignalEvaluator path and remain the runtime firing authority.

However, the package estate is heterogeneous. Second-pass review identified at least five generations:

| Generation | Approximate count | PSI on disk | PSI in manifest | Source pattern / note |
|---|---:|---|---|---|
| legacy `pkg_*` | ~12 | No | No | hand-authored or early package generation |
| `s24` | ~15 | No | No | investigation spec YAML / earlier translation tranche |
| `kb45` | 10 | No | No | batch JSON |
| `kb47` | 20 | Yes | Yes | investigation spec YAML; PSI generation present |
| `kb52c` | 67 | No | No | batch JSON, especially `Batch_5_Pass_3.json` |

This table must be verified by WP0 inventory before any implementation scope is finalised.

Important implication:

```text
The largest known package generation may source from batch JSON rather than individually traceable investigation specs.
```

Therefore, full regeneration cannot be scoped honestly until the inventory confirms which packages have:

- source_spec_id
- source_document only
- batch JSON source
- PSI
- PSI manifest opt-in
- root-cause overlap
- card evidence relevance

---

### 2.3 Promoted Signal Intelligence already exists but is runtime-dead

The signal-layer intelligence artefact already exists:

```text
knowledge_bus/schema/promoted_signal_intelligence_schema_v1.yaml
backend/core/knowledge/investigation_spec_to_promoted_signal.py
backend/core/knowledge/load_promoted_signal_intelligence.py
signal_intelligence_translation_rules_v1.yaml
```

This means HealthIQ must not create a duplicate generic “signal intelligence” schema beside PSI.

However, the critical corrected baseline is:

```text
PSI artefacts and loader exist.
PSI is consumed by zero runtime analytics paths.
```

The loader is currently used by validators/tests, not by the analytics pipeline.

Therefore, PSI is not a live runtime layer. It is governed infrastructure that has not yet been integrated into the runtime path.

This changes the remediation scope:

```text
PSI work is not just coverage and opt-in.
It includes first-time runtime consumption design and wiring.
```

---

### 2.4 PSI is not the hypothesis layer

ADR-008 is accepted in this plan.

The PSI schema intentionally excludes:

- hypotheses
- hypothesis_ranking
- full narrative / root-level WHY graph

Therefore:

```text
PSI = signal-layer semantics
compiled hypothesis artefact = WHY / root-cause intelligence
Health Systems Card evidence = UX projection
```

Do not reverse ADR-008 unless a new ADR explicitly supersedes it.

Do not stuff hypothesis graphs into PSI or signal_library.

---

### 2.5 IDL / presentation safety already exists

The Interpretation Display Layer and retail explainer safety layer already exist and affect user-facing output.

Relevant assets include, but may not be limited to:

```text
InterpretationDisplayLayerBundleV1
backend/ssot/retail_explainer_v1/registry.yaml
domain_narrative_wave1
interpretation_display_layer_publish_v1
consumer prose safety / retail explainer boundary assets
```

The plan does not create IDL. It coordinates compiled intelligence with existing presentation safety.

IDL should govern how intelligence is shown.  
IDL should not originate clinical reasoning.

---

### 2.6 Root-cause YAML is a purpose-built WHY layer, but a duplicate authority

The current root-cause hypothesis YAML files are not raw research.

They are a separate purpose-built WHY layer under:

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

They are functional, but they become a duplicate authority where they overlap with investigation spec hypotheses.

Target state:

```text
investigation_spec hypotheses
→ compiled hypothesis artefact
→ root-cause / WHY compiler
```

Existing root-cause YAML should be retained temporarily for:

- parity testing
- divergence review
- clinical adjudication

Then it should be retired from active authority once compiled replacement is validated.

---

### 2.7 root_cause_registry_v1.py is a manual registration authority

The root-cause registry is currently manual.

It contains a maintained tuple/list of root-cause target specifications, keyed by signal identity and bound to loader functions / asset filenames.

It does not currently provide source_spec_id provenance for all targets.

This must be treated as a first-class transition problem.

Replacing hand-authored root-cause YAML is not sufficient. The registry mechanism itself must transition.

Target direction:

```text
manual root_cause_registry_v1.py tuple
→ generated or manifest-backed root-cause target registry
→ compiled hypothesis artefact loading
```

---

### 2.8 Health Systems Card evidence is currently hard-coded Python

The current Health Systems Card evidence authority is hard-coded Python, likely in:

```text
backend/core/analytics/wave1_subsystem_evidence.py
```

This uses Python dataclass-style subsystem definitions rather than governed research-derived artefacts.

The current structure does not provide the intelligence needed by cards:

- marker_role
- relationship_kind
- rationale_short
- mechanism_line
- missing_policy_line
- visibility_tier
- contradiction caveat
- source_spec_id provenance

This must be replaced by a compiled Health Systems Card evidence artefact and runtime loader.

---

### 2.9 SubsystemEvidenceV1 definitely requires versioning

The existing card DTO does not carry the fields needed for research-derived Health Systems Card evidence.

This is not optional.

The card evidence work requires a versioned DTO extension or replacement, including fields such as:

```text
marker_role
relationship_kind
rationale_short
mechanism_line
missing_policy_line
visibility_tier
source_spec_id / provenance where appropriate
```

The frontend must render these backend-provided fields only.

---

### 2.10 Multi-frame signal collapse is a live runtime defect

The SignalRegistry / SignalEvaluator currently uses `signal_id` as the effective runtime key and applies a deterministic duplicate policy that keeps one package definition when multiple package files share the same `signal_id`.

Second-pass review identified ALT high as a live example:

```text
signal_alt_high
  ├─ hepatocellular injury frame
  ├─ hepatocellular injury pattern frame
  ├─ metabolic / steatotic liver pattern frame
  └─ muscle-source or exertional pattern frame
```

Current behaviour silently discards multiple frames and retains only one according to path/order policy.

This is not a future architecture risk. It is already present.

Target rule:

```text
No runtime registry may silently collapse multiple valid research frames into one signal_id.
```

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

Non-negotiable principles:

1. one canonical upstream research authority
2. multiple purpose-specific compiled runtime views
3. no hand-authored duplicate medical authorities as active runtime sources
4. no raw research runtime reads
5. no frontend medical inference
6. no silent signal/spec identity collapse
7. every user-facing clinical claim traceable to source research and compiled runtime artefact
8. PSI must either become a real runtime input or be removed from the architecture; it cannot remain governed-but-unused
9. package source provenance must be explicit, not inferred from filenames or batch paths

---

## 4. Corrected artefact model

### 4.1 Investigation spec v3

Role:

```text
canonical upstream research authority
```

Runtime status:

```text
compile-time only
not runtime-read
```

---

### 4.2 Signal activation package

Role:

```text
runtime signal firing authority
```

Current artefacts:

```text
signal_library.yaml
research_brief.yaml
package_manifest.yaml
```

Required target additions or classifications:

- source_spec_id or explicit legacy_retained classification
- compile_manifest_ref where generated
- package generation classification
- duplicate signal/frame handling policy
- manifest provenance that is stronger than `source_document` alone

---

### 4.3 Promoted Signal Intelligence / PSI

Role:

```text
signal-layer semantics
```

Existing artefacts:

```text
promoted_signal_intelligence.yaml
promoted_signal_intelligence_schema_v1.yaml
investigation_spec_to_promoted_signal.py
load_promoted_signal_intelligence.py
```

Required target work:

- coverage inventory
- manifest opt-in inventory
- runtime consumption design
- runtime loader integration
- provenance validation
- Sentinel guard for PSI present but not consumed

PSI should not contain full hypotheses or root-cause narrative graphs.

---

### 4.4 Compiled hypothesis artefact

Role:

```text
NEW governed WHY/root-cause source
```

Purpose:

- compile investigation spec hypotheses into deterministic runtime-compatible WHY assets
- replace permanent hand-authored root-cause YAML authority
- preserve hypothesis ranking, physiological claims, evidence strength, caveats, missing-data policy, contradiction markers and confirmatory tests
- support root_cause_compiler transition

Open design question:

```text
Should root_cause_compiler_v1 consume the compiled hypothesis artefact directly,
or should compiled hypothesis artefacts emit a temporary root-cause-compatible YAML view?
```

This must be decided before root-cause implementation.

---

### 4.5 Health System Card Evidence artefact

Role:

```text
NEW compiled UX projection for Health Systems Cards
```

Purpose:

- replace hard-coded Python subsystem evidence
- make card evidence research-derived and governed
- distinguish score contributors, confidence contributors, context markers and missing-for-confidence markers
- provide visibility tiers
- maintain frontend render-only boundary

Likely fields:

```text
domain_id
subsystem_id
visibility_tier
marker_id
marker_role
relationship_kind
rationale_short
mechanism_line
missing_policy_line
source_spec_ids
compile_manifest_ref
```

Visibility tiers:

```text
scored_subsystem
contextual_evidence
hidden_v1
```

---

### 4.6 IDL / presentation safety

Role:

```text
presentation and retail-safety control
```

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

Required target work:

- versioned Health Systems Card DTO extension
- marker-level role fields
- relationship kind fields
- rationale/missing-policy/mechanism fields
- visibility tier
- source/provenance metadata where appropriate
- SignalResult provenance fields if multi-frame firing is supported
- RootCause finding provenance if compiled hypotheses become frame-specific

---

## 5. Critical architecture decision: one-frame or multi-frame?

Before registry or evaluator work is scoped, HealthIQ must answer one foundational question:

```text
For a biomarker direction, should runtime fire one selected frame,
or can multiple valid interpretive frames fire simultaneously?
```

Example:

```text
ALT high
  → one selected active frame?
  → multiple concurrent frames, each with evidence and contradictions?
```

### Option A — One frame per direction

Runtime selects one active frame for a signal_id.

Requirements:

- deterministic arbitration policy
- declared priority / frame selection rule
- no lexicographic path overwrite
- audit trace explaining why a frame was selected
- non-selected frames not silently lost; they must be classified

Pros:

- smaller runtime change
- less DTO churn
- easier interaction map continuity

Cons:

- may suppress legitimate differential frames
- risks oversimplifying clinically complex signals
- requires robust arbitration logic

---

### Option B — Multiple frames per direction

Runtime allows multiple frames for one signal family.

Requirements:

- registry key change
- evaluator emits frame-level results
- SignalResult gains spec/frame provenance
- root-cause compiler handles frame-level findings
- interaction map / phenotype map reviewed for family-vs-frame semantics
- card evidence can show contextual/differential frames safely

Pros:

- medically richer
- preserves Pass 3 research fidelity
- avoids forced collapse of valid frames

Cons:

- larger behavioural change
- affects SignalRegistry, SignalEvaluator, InsightGraph, root-cause compiler, reports and DTOs
- requires stronger presentation safety

---

### Activation key position

Do not implement `activation_key` by assumption.

The identity ADR must decide whether the target key is:

```text
signal_id only with governed arbitration
signal_id + spec_id
activation_key = spec_id
activation_key = signal_id::spec_id
package_id-based frame identity
```

No full regeneration should occur until this is decided.

---

## 6. Transition strategy

Because there are no live users, this is a controlled replacement, not a backward-compatibility migration.

However, every replacement must run through a shadow/parity period.

Legacy assets remain temporarily only for:

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

Create the complete repo-reality inventory before any implementation WP.

Actions:

1. Inventory all investigation specs.
2. Inventory all packages by true generation:
   - legacy
   - s24
   - kb45
   - kb47
   - kb52c
   - any others found
3. Inventory all package `source_document` values.
4. Classify batch JSON source packages separately from individual investigation spec source packages.
5. Inventory all packages with PSI on disk.
6. Inventory all packages with PSI manifest opt-in.
7. Inventory all root-cause hypothesis YAML files.
8. Inventory root_cause_registry_v1.py registrations.
9. Inventory all duplicate signal_id collisions, naming the retained and discarded package paths.
10. Inventory hard-coded Health Systems Card subsystem evidence.
11. Inventory IDL / retail explainer / domain narrative dependencies.
12. Inventory interaction map / phenotype map / calibration / confirmatory-test registry dependencies.
13. Produce traceability matrix:
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
docs/architecture/package_generation_inventory.md
docs/architecture/psi_coverage_and_manifest_opt_in_report.md
docs/architecture/root_cause_registry_inventory.md
docs/architecture/signal_id_collision_inventory.md
docs/architecture/legacy_package_retirement_candidates.md
```

STOP conditions:

- Do not create new schemas before inventory confirms actual gaps.
- Do not create a duplicate signal-intelligence artefact.
- Do not proceed if PSI coverage and opt-in status are unknown.
- Do not proceed if duplicate signal_id behaviour is not fully inventoried.
- Do not scope kb52c regeneration until batch JSON traceability is resolved.

---

## Phase 1 — Identity, ADR and governance decisions

Objective:

Resolve architecture decisions that block safe implementation.

Required decisions:

1. Accept ADR-008.
2. Confirm PSI remains signal-layer only.
3. Confirm hypotheses require a separate compiled hypothesis artefact.
4. Decide one-frame-per-direction versus multi-frame-per-direction.
5. Decide registry keying policy.
6. Decide whether activation_key is required.
7. Decide SignalResult provenance fields.
8. Decide how interaction map / phenotype map / root-cause registry should treat signal families versus frames.
9. Decide compile manifest storage convention.
10. Decide how package provenance is enforced.
11. Decide how root_cause_registry_v1.py transitions from manual tuple registration.

Deliverables:

```text
docs/architecture/ADR-RT-001_research_to_runtime_day_one_architecture.md
docs/architecture/ADR-RT-002_signal_spec_identity_and_registry_policy.md
docs/architecture/ADR-RT-003_hypothesis_artefact_and_root_cause_transition.md
docs/architecture/ADR-RT-004_compile_manifest_and_package_provenance_policy.md
```

STOP conditions:

- No compiler/runtime work until signal/spec identity policy is approved.
- No hypothesis schema work until ADR-008 alignment is resolved.
- No registry refactor until one-frame vs multi-frame is decided.
- No full regeneration until duplicate signal_id behaviour has a replacement policy.

---

## Phase 2a — PSI gap analysis

Objective:

Establish the PSI coverage and consumption baseline.

Actions:

1. Confirm which specs/packages have PSI.
2. Confirm which packages opt into PSI through manifests.
3. Confirm PSI is not consumed by runtime analytics paths.
4. Identify where PSI should be consumed in target runtime.
5. Produce gap report.

Deliverables:

```text
docs/architecture/psi_gap_analysis.md
docs/architecture/psi_runtime_consumption_gap_report.md
```

Risk:

```text
CONTENT / STANDARD
```

STOP conditions:

- No runtime wiring in this phase.
- No hand-authored PSI.
- No new PSI schema.

---

## Phase 2b — Compile manifest schema and provenance policy

Objective:

Define compile manifest infrastructure without wiring runtime behaviour.

Actions:

1. Define compile manifest schema.
2. Define manifest storage convention:
   - per compile run
   - per artefact embedded reference
   - estate index
3. Define source hash / output hash rules.
4. Define required package provenance fields:
   - source_spec_id or legacy_retained classification
   - compile_manifest_ref where applicable
   - source_document status
5. Define validation requirements.

Deliverables:

```text
knowledge_bus/schema/compile_manifest_schema_v1.yaml
docs/architecture/compile_manifest_contract.md
docs/architecture/package_provenance_policy.md
```

Risk:

```text
CONTENT / STANDARD unless validators/scripts are changed
```

STOP conditions:

- No compiled artefacts without manifest convention.
- No package promotion without provenance classification.

---

## Phase 2c — PSI runtime wiring design

Objective:

Design, but not yet implement blindly, how PSI becomes a runtime input.

Actions:

1. Identify PSI runtime consumer:
   - orchestrator
   - signal evaluator
   - assembler
   - report compiler
   - card evidence assembly
2. Decide whether PSI is loaded package-scoped or estate-indexed.
3. Decide how PSI joins to fired results:
   - signal_id
   - spec_id
   - package_id
   - activation_key if adopted
4. Define runtime contract and tests.
5. Scope implementation WP.

Deliverables:

```text
docs/architecture/psi_runtime_wiring_design.md
```

Risk:

```text
CONTENT for design only
BEHAVIOUR/HIGH for implementation
```

STOP conditions:

- No PSI runtime implementation before identity decision.
- No PSI retail surfacing without IDL boundary review.

---

## Phase 3 — Single-frame compile/provenance pilot

Objective:

Prove compile/provenance mechanics on a real inventory-identified gap.

Pilot selection should be based on Phase 0 inventory.

Preferred characteristics:

- single frame
- valid investigation spec
- existing package relationship
- no duplicate signal_id collision
- missing PSI or missing PSI manifest opt-in
- low runtime blast radius

Current likely candidate, subject to inventory confirmation:

```text
LDL high / signal_ldl_cholesterol_high
```

Actions:

1. Select pilot based on inventory.
2. Run or reuse existing investigation spec → PSI translator.
3. Generate or verify PSI.
4. Emit compile manifest.
5. Validate deterministic output.
6. Compare to existing package/research expectations.
7. No runtime wiring.

Deliverables:

```text
pilot PSI artefact or corrected manifest opt-in
compile manifest
determinism test
pilot gap closure report
```

STOP conditions:

- No runtime wiring.
- No multi-frame pilot.
- No CRP pilot if it bundles legacy retirement, activation regeneration and registry change.

---

## Phase 4 — Multi-frame identity pilot

Objective:

Prove the selected identity model against a real collision.

Recommended candidate:

```text
ALT high
```

Actions:

1. Identify all ALT-high packages/specs.
2. Confirm current retained/discarded package behaviour.
3. Apply approved identity policy in controlled pilot.
4. Update registry/evaluator only if explicitly authorised.
5. Confirm downstream effects:
   - SignalResult
   - InsightGraph
   - interaction map
   - phenotype map
   - root-cause compiler
   - report compiler
6. Produce before/after collision behaviour report.

Deliverables:

```text
multi_frame_identity_test_report.md
SignalRegistry_collision_remediation_report.md
```

STOP conditions:

- No full regeneration until this is solved.
- No silent lexicographic overwrite in target state.
- No interaction map / phenotype map breakage without documented mitigation.

---

## Phase 5a — Card evidence schema and role policy

Objective:

Define card evidence artefact shape and role translation without runtime wiring.

Actions:

1. Define card evidence schema.
2. Define marker role vocabulary.
3. Define relationship_kind to card role mapping.
4. Define visibility-tier policy from medical review.
5. Define DTO requirements.

Deliverables:

```text
knowledge_bus/schema/health_system_card_evidence_schema_v1.yaml
docs/architecture/card_evidence_role_translation_policy.md
docs/architecture/card_visibility_tier_policy.md
```

Risk:

```text
CONTENT / STANDARD
```

---

## Phase 5b — Card evidence compile pilot

Objective:

Compile one subsystem artefact from governed research-derived inputs.

Pilot should be selected from Phase 0 inventory.

Possible candidates:

```text
glycaemic control subsystem
lipid transport subsystem
```

Actions:

1. Compile one subsystem card evidence artefact.
2. Validate schema.
3. Compare against hard-coded Python evidence.
4. Identify differences for adjudication.
5. Do not wire frontend.

Deliverables:

```text
knowledge_bus/compiled/health_system_cards/<pilot>.yaml
card evidence validation output
legacy comparison report
```

Risk:

```text
CONTENT / STANDARD unless runtime code changes
```

---

## Phase 5c — Backend card evidence loader, assembler and DTO v2

Objective:

Wire compiled card evidence into backend DTOs for the pilot path.

Actions:

1. Add loader.
2. Replace or bypass hard-coded Python evidence for pilot path.
3. Add DTO v2 / schema-versioned DTO extension.
4. Populate required fields.
5. Add backend tests.
6. Keep frontend render-only.

Deliverables:

```text
compiled card evidence loader
DTO v2 / card schema version
backend assembler update
tests
```

Risk:

```text
BEHAVIOUR / HIGH
```

STOP conditions:

- No frontend role inference.
- No DTO work before schema/validator pass.
- No retail prose bypassing IDL.

---

## Phase 5d — Frontend render update

Objective:

Render backend-provided card evidence fields only.

Actions:

1. Render marker_role.
2. Render relationship_kind / rationale where approved.
3. Respect visibility_tier.
4. No frontend inference.

Deliverables:

```text
frontend render-only update
component tests
```

Risk:

```text
BEHAVIOUR / HIGH or MIXED depending scope
```

---

## Phase 6a — Compiled hypothesis schema

Objective:

Define the new compiled hypothesis artefact.

Actions:

1. Define schema.
2. Define hypothesis identity.
3. Define mapping from investigation spec hypotheses.
4. Define confirmatory test registry mapping.
5. Define relationship to existing root-cause compiler shape.

Deliverables:

```text
knowledge_bus/schema/compiled_hypothesis_schema_v1.yaml
docs/architecture/compiled_hypothesis_contract.md
```

Risk:

```text
CONTENT / STANDARD
```

---

## Phase 6b — Hypothesis compile pilot and divergence report

Objective:

Compile one pilot hypothesis artefact and compare to existing root-cause YAML.

Actions:

1. Select pilot based on inventory.
2. Compile hypothesis artefact.
3. Validate.
4. Compare to hand-authored root-cause YAML.
5. Produce divergence report.
6. Do not switch compiler.

Deliverables:

```text
compiled hypothesis pilot artefact
root-cause divergence report
```

Risk:

```text
CONTENT / STANDARD
```

---

## Phase 6c — Root-cause registry transition pilot

Objective:

Introduce compiled hypothesis artefact into root-cause path in shadow or pilot mode.

Actions:

1. Add compiled hypothesis loader.
2. Update or extend root_cause_registry.
3. Preserve legacy YAML for comparison.
4. Run shadow comparison.
5. Decide replacement readiness.

Deliverables:

```text
compiled hypothesis loader
root_cause_registry transition pilot
shadow comparison report
```

Risk:

```text
BEHAVIOUR / HIGH
```

STOP conditions:

- Do not switch compiler before registry transition is solved.
- Do not discard YAML without divergence adjudication.
- Do not leave duplicate hypothesis authorities active without classification.

---

## Phase 7a — Runtime loaders and DTO integration

Objective:

Wire approved compiled artefacts into runtime behind explicit contracts.

Scope may include:

- PSI runtime loader
- card evidence loader
- hypothesis loader
- DTO extensions

This must be split further if it touches too many runtime surfaces.

Risk:

```text
BEHAVIOUR / HIGH
```

---

## Phase 7b — Shadow mode and golden comparison

Objective:

Compare current output to compiled output before cutover.

Actions:

1. Run existing fixtures.
2. Run compiled path.
3. Diff outputs.
4. Produce adjudication report.
5. Update golden fixtures only after approval.

Risk:

```text
BEHAVIOUR / HIGH
```

---

## Phase 7c — Sentinel and QA gate

Objective:

Register and enforce guards before wider cutover.

Required guards include:

```text
raw_research_runtime_read_forbidden
psi_present_but_not_consumed
manual_card_evidence_authority_forbidden
duplicate_signal_id_collapse_guard
package_without_source_spec_id_guard
root_cause_yaml_as_permanent_authority_guard
compiled_artifact_missing_manifest_guard
retail_prose_bypasses_idl_guard
```

Risk:

```text
MIXED / HIGH if Sentinel/control-plane surfaces touched
```

---

## Phase 8 — Full regeneration and legacy retirement

Objective:

Move the active intelligence estate onto the corrected day-one architecture.

Actions:

1. Compile all valid investigation specs into required runtime artefacts.
2. Resolve kb52c batch JSON source problem:
   - extract individual investigation specs
   - or classify as legacy_retained
   - or schedule regeneration
3. Ensure all active packages have source_spec_id or legacy_retained classification.
4. Ensure PSI coverage/opt-in is complete where required.
5. Generate Health Systems Card evidence estate.
6. Generate compiled hypothesis/root-cause estate.
7. Retire hard-coded Python subsystem evidence as active authority.
8. Retire hand-authored root-cause YAML as active authority after divergence adjudication.
9. Retire legacy duplicate packages.
10. Update estate index / knowledge status / authority manifest.

Deliverables:

```text
full compiled artefact estate
legacy retirement report
active authority manifest
launch architecture evidence pack
```

Risk:

```text
HIGH / MIXED
```

STOP conditions:

- Do not launch with unclassified active packages lacking provenance.
- Do not launch with manual card evidence as authority.
- Do not launch with duplicate active hypothesis authorities.
- Do not launch with unresolved duplicate signal_id collapse behaviour.
- Do not launch with PSI remaining runtime-dead if PSI is required for active claims.

---

## Phase 9 — Day-one launch-readiness gate

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
12. PSI is either runtime-consumed where required or explicitly removed from launch-critical architecture.

Deliverables:

```text
docs/audit-papers/day_one_architecture_launch_readiness_audit.md
docs/audit-papers/research_to_runtime_traceability_audit.md
docs/audit-papers/active_intelligence_authority_manifest.md
```

---

## 8. Revised work-package sequence

This paper is not itself a work package.

Likely governed sequence:

### WP0 — Corrected inventory and authority trace

```yaml
work_id: ARCH-RT-0_inventory_authority_trace
risk_level: STANDARD
change_type: CONTENT
objective: Produce complete repo-reality inventory, PSI coverage, package generation classification, root-cause registry inventory, signal_id collision inventory and authority traceability matrix.
```

### WP1 — Identity and ADR alignment

```yaml
work_id: ARCH-RT-1_identity_adr_alignment
risk_level: HIGH
change_type: MIXED
objective: Resolve ADR-008 alignment, one-frame vs multi-frame policy, registry keying, possible activation_key need, SignalResult provenance, and root-cause registry transition principles.
```

### WP2a — PSI gap analysis

```yaml
work_id: ARCH-RT-2a_psi_gap_analysis
risk_level: STANDARD
change_type: CONTENT
objective: Confirm PSI coverage, manifest opt-in and zero-runtime-consumption baseline.
```

### WP2b — Compile manifest schema

```yaml
work_id: ARCH-RT-2b_compile_manifest_schema
risk_level: STANDARD
change_type: CONTENT
objective: Define compile manifest schema and package provenance policy.
```

### WP2c — PSI runtime wiring design

```yaml
work_id: ARCH-RT-2c_psi_runtime_wiring_design
risk_level: STANDARD
change_type: CONTENT
objective: Design how PSI joins runtime outputs after identity policy is approved.
```

### WP3 — Single-frame compile/provenance pilot

```yaml
work_id: ARCH-RT-3_single_frame_compile_pilot
risk_level: HIGH
change_type: MIXED
objective: Use inventory-selected single-frame gap candidate to prove deterministic PSI/provenance and manifest mechanics without runtime wiring.
```

### WP4 — Multi-frame identity pilot

```yaml
work_id: ARCH-RT-4_multi_frame_identity_pilot
risk_level: HIGH
change_type: MIXED
objective: Prove duplicate signal_id / multi-frame identity policy using ALT or another inventory-confirmed collision.
```

### WP5a — Card evidence schema and role policy

```yaml
work_id: ARCH-RT-5a_card_evidence_schema_policy
risk_level: STANDARD
change_type: CONTENT
objective: Define card evidence schema, role translation and visibility-tier policy.
```

### WP5b — Card evidence compile pilot

```yaml
work_id: ARCH-RT-5b_card_evidence_compile_pilot
risk_level: STANDARD
change_type: CONTENT
objective: Compile one Health Systems Card evidence artefact and compare to legacy Python evidence.
```

### WP5c — Backend card evidence loader and DTO v2

```yaml
work_id: ARCH-RT-5c_card_backend_loader_dto_v2
risk_level: HIGH
change_type: BEHAVIOUR
objective: Wire compiled card evidence into backend assembler and versioned DTO for pilot path.
```

### WP5d — Frontend card render update

```yaml
work_id: ARCH-RT-5d_card_frontend_render_update
risk_level: HIGH
change_type: MIXED
objective: Render backend-provided card evidence fields only, without frontend inference.
```

### WP6a — Compiled hypothesis schema

```yaml
work_id: ARCH-RT-6a_compiled_hypothesis_schema
risk_level: STANDARD
change_type: CONTENT
objective: Define compiled hypothesis artefact schema and mapping policy from investigation specs.
```

### WP6b — Hypothesis compile pilot and divergence report

```yaml
work_id: ARCH-RT-6b_hypothesis_compile_pilot_divergence
risk_level: STANDARD
change_type: CONTENT
objective: Compile one pilot hypothesis artefact and compare to existing root-cause YAML.
```

### WP6c — Root-cause registry transition pilot

```yaml
work_id: ARCH-RT-6c_root_cause_registry_transition_pilot
risk_level: HIGH
change_type: BEHAVIOUR
objective: Introduce compiled hypothesis loading into root-cause registry path in shadow/pilot mode.
```

### WP7a — Runtime loaders and DTO integration

```yaml
work_id: ARCH-RT-7a_runtime_loaders_dto_integration
risk_level: HIGH
change_type: BEHAVIOUR
objective: Wire approved compiled artefacts into runtime behind explicit contracts.
```

### WP7b — Shadow mode and golden comparison

```yaml
work_id: ARCH-RT-7b_shadow_mode_golden_comparison
risk_level: HIGH
change_type: BEHAVIOUR
objective: Compare current output to compiled path output before cutover.
```

### WP7c — Sentinel and QA gate

```yaml
work_id: ARCH-RT-7c_sentinel_qa_gate
risk_level: HIGH
change_type: MIXED
objective: Register and enforce guards for research-to-runtime architecture defects.
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
11. Do not treat PSI as an architecture layer unless it is actually runtime-consumed.
12. Do not write implementation WPs until WP0 and WP1 close.
13. Do not combine CONTENT schema work and BEHAVIOUR runtime wiring in the same work package unless explicitly justified and classified HIGH.

---

## 11. Final confirmation questions for reviewers

Claude Code and Cursor should now answer only:

1. Is v3 accurate enough to author WP0?
2. Is v3 accurate enough to author WP1?
3. Is any material as-is baseline still wrong?
4. Are the WP0 and WP1 deliverables sufficient to prevent mis-scoped downstream work?
5. Are there any launch blockers still missing from the plan?

Do not re-review the whole strategy unless a material baseline error remains.

---

## 12. Final architectural position

The target remains:

```text
canonical research authority
→ deterministic compile / translation
→ governed runtime artefacts
→ runtime loaders
→ structured DTOs
→ frontend render-only
```

The immediate next step should not be implementation.

The immediate next step should be formalising WP0 and WP1 only:

```text
WP0: inventory and authority trace
WP1: identity / ADR / registry policy
```

No downstream implementation work should be authored until those close.

