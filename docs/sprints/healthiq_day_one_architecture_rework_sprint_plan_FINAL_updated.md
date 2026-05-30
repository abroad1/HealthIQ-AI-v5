# HealthIQ AI — Day-One Architecture Rework Sprint Plan FINAL

**Updated status note:** This version includes delivered-sprint status notes and the carry-forward register created after ARCH-RT-2 GPT architectural review.

**Intended repository location:**  
`C:\Users\abroa\HealthIQ-AI-v5\docs\sprints\healthiq_day_one_architecture_rework_sprint_plan_FINAL.md`

**Status:** FINAL sprint plan for governance use  
**Purpose:** Define the fewest sensible, governable sprint sequence to move HealthIQ AI from the current fragmented research/runtime architecture to the correct day-one architecture before launch.  
**Implementation status:** This document does not authorise implementation. Each sprint still requires a formal Automation Bus work package.

---

## 1. Executive summary

HealthIQ AI has a strategic architecture problem that must be corrected before launch.

The agreed target architecture is:

```text
canonical research authority
→ deterministic compile / translation
→ governed runtime artefacts
→ runtime loaders
→ structured DTOs
→ frontend render-only
```

The current system has several known issues:

- Promoted Signal Intelligence / PSI exists but is consumed by zero runtime analytics paths.
- Multi-frame signal collapse is live; valid research frames can be silently discarded by `signal_id`-only registry behaviour.
- Health Systems Card evidence is hard-coded in Python rather than compiled from governed research-derived assets.
- Root-cause YAML is a functional WHY layer but remains a duplicate authority where it overlaps with investigation spec hypotheses.
- Package provenance is inconsistent across generations.
- Some packages source from batch JSON rather than individually traceable investigation specs.
- The liver-card `total_bilirubin` false-missing defect remains unresolved.
- The governed activation compile path from `investigation_spec` to `signal_library` / package artefacts is distinct from PSI and must be made explicit.
- PSI runtime consumption timing must be governed, not implied.

Because there are no live users, the correct posture is controlled replacement, not backward-compatibility preservation.

This plan intentionally avoids unnecessary micro-sprints, but does not combine work that would create unsafe governance risk.

---

## 2. Sprint philosophy

The plan uses the fewest sensible sprint sequence.

Do not reduce further by combining:

```text
decision work
runtime behaviour changes
schema / validator changes
card DTO and frontend changes
root-cause compiler changes
full estate regeneration
```

Combining those into fewer packages would recreate the governance failures this architecture rework is intended to correct.

The sequence keeps the sprint count low while preserving the key safety boundaries:

- known tactical defect first
- inventory and architecture decisions before implementation
- contracts before runtime change
- identity runtime behaviour before full regeneration
- one card evidence vertical slice before estate-wide replacement
- one hypothesis/root-cause slice before estate-wide replacement
- full regeneration only after the pilots prove the architecture

---

## 3. Sprint sequence overview

```text
0. WAVE1-EQUIV1_total_bilirubin_false_missing_fix        [DELIVERED]
1. ARCH-RT-0_inventory_and_identity_decisions            [DELIVERED]
2. ARCH-RT-1_contracts_and_compile_foundation            [DELIVERED AS DRAFT FOUNDATION]
3. ARCH-RT-2_identity_runtime_pilot                      [AUDIT PASSED / GPT APPROVED; MERGE STATUS TO CONFIRM]
4. ARCH-RT-3_card_evidence_vertical_slice                [NEXT IMPLEMENTATION STREAM]
5. ARCH-RT-4_compiled_hypothesis_root_cause_slice        [PENDING]
6. ARCH-RT-5_full_regeneration_and_launch_gate           [PENDING]
```

Sprint 0 is deliberately separate because it fixes a known false-missing defect that would otherwise pollute the evidence baseline.

---

# Sprint 0 — WAVE1-EQUIV1_total_bilirubin_false_missing_fix

## Delivery status

**Delivered and merged.**

The original plan classified this sprint as STANDARD / BEHAVIOUR because the change was narrow. During hardening this was correctly escalated to HIGH because `backend/core/analytics/wave1_subsystem_evidence.py` is an unconditional HIGH-risk path under the Automation Bus SOP.

Outcome:

- `total_bilirubin` was removed from the Wave 1 liver processing expected-marker tuple.
- `bilirubin` remains the canonical expected marker.
- Regression coverage was updated so `total_bilirubin` is not falsely reported missing when `bilirubin` is present.
- `domain_score_assembler.py` and `backend/ssot/biomarkers.yaml` were intentionally not modified.
- This correction must be preserved by Sprint 4 when hard-coded card evidence is replaced.

## Purpose

Fix the known `total_bilirubin` / `bilirubin` false-missing defect in the Wave 1 liver card.

This is a confirmed overhang from previous audits and should not be buried inside the architecture programme.

## Rationale

The current hard-coded liver subsystem evidence appears to expect `total_bilirubin` even though canonical SSOT resolution treats this as display/rail-only or equivalent to `bilirubin`.

This causes false missing-marker behaviour in the liver card.

Leaving this unresolved would:

- reduce trust in card evidence
- pollute the baseline used by the architecture inventory
- create noisy diffs during later card-evidence replacement work

## Scope

- Verify the current defect still exists.
- Fix `total_bilirubin` / `bilirubin` equivalence in Wave 1 liver subsystem evidence.
- Ensure canonical SSOT resolution is respected.
- Remove `total_bilirubin` from expected marker logic if it is display-only / rail-only.
- Add or update regression coverage.
- Confirm the liver card no longer reports `total_bilirubin` as missing when `bilirubin` is present.

## Likely touched areas

Final file list must be verified by Cursor during hardening, but likely areas include:

```text
backend/core/analytics/wave1_subsystem_evidence.py
backend/tests/**/*
```

## Classification

```yaml
risk_level: HIGH
change_type: BEHAVIOUR
execution_model: TWO_PHASE_START_FINISH
```

Note: HIGH applies by path because `backend/core/analytics/` was touched.

## STOP conditions

- Stop if the defect no longer exists.
- Stop if the issue is not local to Wave 1 subsystem evidence and instead exposes a broader canonical resolver defect.
- Stop if the fix would require changing biomarker canonicalisation policy rather than correcting a false expected-marker list.
- Stop if regression coverage cannot demonstrate the before/after behaviour.

## Success criteria

- `bilirubin` is accepted as the canonical expected marker.
- `total_bilirubin` is not falsely reported missing.
- Liver-card evidence remains otherwise unchanged.
- Regression tests prove the defect is fixed.

---

# Sprint 1 — ARCH-RT-0_inventory_and_identity_decisions

## Delivery status

**Delivered and merged.**

Outcome:

- All 12 required inventory and ADR artefacts were delivered under `docs/architecture/`.
- `ADR-RT-002` decisively selected `MULTI_FRAME_PER_DIRECTION`.
- `activation_key` was confirmed as required.
- `signal_id` remains signal-family identity and is not sufficient as runtime frame identity.
- PSI was confirmed as runtime-dead.
- All 186 packages were inventoried and `source_spec_id` was confirmed absent across the active package estate.
- The collision estate was inventoried: 45 duplicate `signal_id` families / 96 package rows, including explicit ALT and homocysteine cases.
- The activation compile gap was confirmed: no governed estate-wide `investigation_spec → signal_library / research_brief / package_manifest` compiler exists.

These outputs are authoritative inputs for all later ARCH-RT work.

## Purpose

Combine the confirmed-safe WP0 and WP1 work into one documentation/decision sprint.

This sprint inventories the current intelligence estate and makes the blocking architecture decisions needed before implementation work begins.

## Rationale

Claude Code and Cursor confirmed that WP0 and WP1 are safe to author, provided WP1 remains documentation/ADR-only and is classified as CONTENT / STANDARD.

Combining them avoids unnecessary governance overhead while staying safe, because this sprint does not modify runtime behaviour.

## Scope

### Inventory work

Produce a complete repo-reality inventory covering:

- investigation spec corpus
- package generations
- all package-generation prefixes found, including but not limited to:
  - legacy
  - s24
  - kb45
  - kb47
  - kb52 / kb52c / kb52d
  - kb58
  - kb59
  - kb60
  - kb61
  - any other package generations found in the repository
- package `source_document` values
- packages with individual investigation spec provenance
- packages sourcing from batch JSON
- packages with `source_spec_id` if present
- packages without source provenance
- PSI artefacts on disk
- PSI package-manifest opt-ins
- runtime-dead PSI status
- root-cause hypothesis YAML files
- root_cause_registry registrations
- duplicate `signal_id` collisions
- current retained/discarded package behaviour where detectable
- Health Systems Card hard-coded evidence
- IDL / retail explainer dependencies
- interaction map / phenotype map / calibration / confirmatory-test registry dependencies
- DTO/frontend traceability for user-facing claims
- whether existing translators/compilers have been tested against candidate inventory entries

### Decision / ADR work

Produce architecture decisions covering:

- ADR-008 acceptance
- PSI scope confirmation
- compiled hypothesis artefact boundary
- one-frame versus multi-frame runtime policy
- registry keying policy
- whether `activation_key` is required
- SignalResult provenance requirements
- interaction map / phenotype map / root-cause registry family-vs-frame policy
- package provenance policy
- activation compile policy:
  - `investigation_spec` → `signal_library.yaml`
  - `investigation_spec` → `research_brief.yaml`
  - `investigation_spec` → `package_manifest.yaml`
- root_cause_registry transition direction
- compile manifest convention

## Deliverables

```text
docs/architecture/research_to_runtime_traceability_matrix.md
docs/architecture/intelligence_authority_inventory.md
docs/architecture/package_generation_inventory.md
docs/architecture/psi_coverage_and_manifest_opt_in_report.md
docs/architecture/root_cause_registry_inventory.md
docs/architecture/signal_id_collision_inventory.md
docs/architecture/legacy_package_retirement_candidates.md
docs/architecture/activation_compile_gap_report.md
docs/architecture/ADR-RT-001_research_to_runtime_day_one_architecture.md
docs/architecture/ADR-RT-002_signal_spec_identity_and_registry_policy.md
docs/architecture/ADR-RT-003_hypothesis_artefact_and_root_cause_transition.md
docs/architecture/ADR-RT-004_compile_manifest_and_package_provenance_policy.md
```

## Classification

```yaml
risk_level: STANDARD
change_type: CONTENT
execution_model: TWO_PHASE_START_FINISH
```

## Constraints

- Documentation and inventory only.
- No runtime code changes.
- No schema changes unless explicitly re-scoped.
- No package edits.
- No SignalRegistry / SignalEvaluator changes.
- No compiler implementation.
- No card evidence implementation.

## STOP conditions

- Stop if inventory requires code changes outside docs.
- Stop if ADRs cannot make a decisive one-frame versus multi-frame recommendation.
- Stop if package-generation counts materially differ from the working assumptions in a way that changes the sprint sequence.
- Stop if PSI runtime-dead status is not verifiable.
- Stop if duplicate `signal_id` collision inventory cannot identify current retained/discarded behaviour.
- Stop if the activation compile gap cannot be clearly separated from PSI.
- Stop if batch JSON source packages cannot be classified as traceable, untraceable, or requiring later extraction.

## Success criteria

- Exact package-generation inventory exists.
- Inventory includes kb58/kb59/kb60/kb61 and any other generations found.
- PSI coverage and opt-in status are known.
- Runtime-dead PSI status is confirmed or corrected.
- Duplicate signal collisions are inventoried.
- ADR-008 is formally accepted or explicitly challenged.
- ADR-RT-002 decisively chooses one-frame or multi-frame; it must not leave both options open.
- Registry keying policy is decided.
- Package provenance and compile manifest policies are defined.
- Activation compile gap is explicitly documented.
- Downstream implementation sprints can be scoped from evidence, not assumptions.

---

# Sprint 2 — ARCH-RT-1_contracts_and_compile_foundation

## Delivery status

**Delivered and merged as DRAFT foundation work.**

Outcome:

- `compile_manifest_schema_v1.yaml` was created as a DRAFT schema.
- Compile manifest, package provenance, activation compile, PSI gap closure, and PSI runtime wiring design documents were delivered.
- `validate_compile_manifest.py` and unit smoke tests were added as narrow validation support.
- The pilot selection changed from the earlier possible LDL candidate to `pkg_s24_vitamin_d_low_deficiency` / `inv_vitamin_d_low_deficiency_v1.yaml`, based on repository evidence.
- No runtime wiring occurred.
- No package, investigation spec, PSI, root-cause YAML, frontend, or runtime behaviour files were modified.

Carry-forward decisions from GPT review:

- `compile_id` is canonical.
- `compile_run_id` is transitional only.
- If both `compile_id` and `compile_run_id` are present, the validator must enforce equality.
- `activation_keys_emitted`, `collisions_detected`, and `policy_version` may remain optional only while the schema is DRAFT.
- Before production compiler use, schema lock, or launch-critical compile manifest use, ADR-required manifest fields must become required.
- Any `ARCH-RT-2b` reference should be normalised to `ARCH-RT-2` unless a formal split is approved.

## Purpose

Create the minimum governance contracts and compile/provenance foundation needed for the day-one architecture.

## Rationale

After Sprint 1 has confirmed the estate and identity decisions, HealthIQ needs the formal contract layer that enables generated runtime artefacts to be validated, traced and governed.

This sprint combines schema/provenance foundation with one low-blast-radius compile pilot, but does not include runtime wiring.

This sprint must explicitly distinguish:

```text
activation compile:
investigation_spec → signal_library / research_brief / package_manifest

PSI compile:
investigation_spec → promoted_signal_intelligence
```

The existing PSI translator does not replace the need for a governed activation package compiler.

## Scope

- Define compile manifest schema.
- Define manifest storage convention.
- Define package provenance policy/schema updates if required.
- Define source hash / output hash rules.
- Define active package provenance requirements.
- Define activation compile foundation:
  - `investigation_spec` → `signal_library.yaml`
  - `investigation_spec` → `research_brief.yaml`
  - `investigation_spec` → `package_manifest.yaml`
- Confirm how activation compile differs from PSI.
- Confirm PSI gap closure mechanics.
- Test existing PSI translator determinism.
- Produce `psi_runtime_wiring_design.md` as design only.
- Select one inventory-confirmed single-frame compile/provenance pilot.
- Generate or verify pilot activation package/provenance output where appropriate.
- Generate or verify pilot PSI/provenance output where appropriate.
- Produce compile manifest for pilot.
- Confirm deterministic repeatability.

## Likely pilot

The pilot must be selected from Sprint 1 inventory.

Preferred candidate characteristics:

- single-frame
- valid investigation spec
- no duplicate `signal_id` collision
- package relationship already exists
- PSI missing or manifest opt-in gap exists
- activation package relationship is clear
- low runtime blast radius

Potential candidate, subject to inventory confirmation:

```text
LDL high / signal_ldl_cholesterol_high
```

## Deliverables

```text
knowledge_bus/schema/compile_manifest_schema_v1.yaml
docs/architecture/compile_manifest_contract.md
docs/architecture/package_provenance_policy.md
docs/architecture/activation_compile_contract.md
docs/architecture/psi_gap_closure_mechanics.md
docs/architecture/psi_runtime_wiring_design.md
pilot activation compile/provenance evidence
pilot PSI compile/provenance evidence
pilot compile manifest
pilot determinism test evidence
pilot gap closure report
```

## Classification

```yaml
risk_level: HIGH
change_type: MIXED
execution_model: TWO_PHASE_START_FINISH
```

## Constraints

- No runtime wiring.
- No SignalRegistry / SignalEvaluator changes.
- No card evidence runtime work.
- No root-cause compiler changes.
- No full estate regeneration.
- PSI runtime wiring is design-only in this sprint.
- Activation compile must not be conflated with PSI.

## STOP conditions

- Stop if Sprint 1 has not approved identity and provenance policy.
- Stop if compile manifest convention is still undecided.
- Stop if activation compile scope cannot be separated from PSI.
- Stop if the selected pilot has unresolved duplicate `signal_id` behaviour.
- Stop if the PSI translator is non-deterministic.
- Stop if activation compile output requires hand-editing rather than source/compiler correction.
- Stop if pilot output requires hand-editing rather than source/compiler correction.
- Stop if package provenance cannot be represented without schema decisions not authorised in this sprint.

## Success criteria

- Compile manifest contract exists.
- Package provenance policy exists.
- Activation compile contract exists.
- PSI runtime wiring design exists.
- Pilot activation/provenance path is deterministic where in scope.
- Pilot PSI/provenance path is deterministic where in scope.
- Pilot output is traceable to source research.
- No runtime behaviour changes occur.

---

# Sprint 3 — ARCH-RT-2_identity_runtime_pilot

## Delivery status

**Audit passed and GPT approved for merge. Merge status must be confirmed in the repository before later sprints rely on it.**

Outcome from audit/GPT review:

- Silent lexicographic `signal_id` overwrite was removed for the ALT pilot.
- Runtime registry identity was changed to use `activation_key`.
- Four ALT-high frames are loaded without collapse in the pilot.
- Duplicate `activation_key` now fails closed.
- `SignalResult` now carries `activation_key`, `source_spec_id`, and `package_id`.
- Single-frame signal behaviour remained stable in tests.
- No package files, investigation specs, PSI artefacts, root-cause YAML, card evidence, frontend, IDL, or compile manifest files were modified.

Carry-forward constraints from GPT review:

- Directory-derived `source_spec_id` is acceptable only as an interim runtime identity fallback. It is not canonical research provenance.
- Future provenance work must distinguish explicit source-spec provenance from inferred source-spec provenance.
- Root-cause compiler remains signal-family-only and is not multi-frame aware.
- Root-cause first-match behaviour is acceptable temporarily but must be fixed in the compiled hypothesis / root-cause transition stream.

## Purpose

Fix the live multi-frame signal-collapse problem using one controlled runtime pilot.

## Rationale

The current system can silently discard valid research frames when multiple packages share a `signal_id`.

This is a launch blocker. The identity model must be proven before full regeneration.

## Scope

- Implement the approved identity/registry policy from Sprint 1.
- Use one controlled multi-frame case, likely ALT if confirmed by Sprint 1.
- Stop silent lexicographic overwrite / silent duplicate collapse.
- Add SignalRegistry tests.
- Update SignalEvaluator behaviour if required.
- Add SignalResult provenance fields if approved.
- Assess downstream effects:
  - InsightGraph
  - interaction map
  - phenotype map
  - root-cause compiler
  - report compiler
  - persisted fixtures

## Likely pilot

```text
ALT high multi-frame case
```

Final pilot must be confirmed by Sprint 1 collision inventory.

## Deliverables

```text
multi_frame_identity_test_report.md
SignalRegistry collision remediation
SignalEvaluator tests
SignalResult provenance update if approved
downstream impact report
```

## Classification

```yaml
risk_level: HIGH
change_type: BEHAVIOUR
execution_model: TWO_PHASE_START_FINISH
```

## Constraints

- Do not combine with card evidence work.
- Do not combine with root-cause replacement work.
- Do not perform full estate regeneration.
- Do not alter medical thresholds unless explicitly authorised.

## STOP conditions

- Stop if Sprint 1 did not make a decisive one-frame versus multi-frame policy.
- Stop if registry/evaluator changes require unplanned interaction map or phenotype map redesign.
- Stop if persisted results or golden fixtures reveal broader contract breakage than the sprint can govern.
- Stop if the selected pilot requires unrelated package regeneration.

## Success criteria

- Silent duplicate `signal_id` collapse is prevented for the pilot.
- Runtime identity behaviour follows approved ADR.
- Signal results carry the required provenance.
- Tests prove the intended behaviour.
- Downstream impact is documented.

---

# Sprint 4 — ARCH-RT-3_card_evidence_vertical_slice

## Purpose

Replace hard-coded Health Systems Card evidence for one subsystem with compiled, research-derived evidence end-to-end.

## Rationale

Health Systems Cards currently do not consume governed medical intelligence properly. This sprint proves the replacement architecture through one vertical slice.

It is intentionally larger than a micro-sprint because the value is only proven when compiled evidence reaches the card DTO and frontend render path safely.

## Scope

- Define or finalise card evidence schema.
- Define card role translation policy.
- Define visibility-tier policy.
- Compile one subsystem evidence artefact.
- Validate the artefact.
- Add backend loader.
- Replace or bypass hard-coded Python evidence for pilot subsystem.
- Add DTO v2 / schema-versioned DTO extension.
- Update frontend to render backend-provided fields only, if required.
- Add regression coverage.

## Pilot selection

Select from Sprint 1 inventory.

Possible candidates:

```text
glycaemic control subsystem
lipid transport subsystem
```

Final choice should be based on:

- cleanest authority chain
- medical review support
- lowest ambiguity
- clear marker set
- manageable DTO/frontend impact

## Internal checkpoint

This sprint must include a mandatory internal checkpoint:

```text
The compiled card evidence artefact must validate before backend loader, DTO, or frontend implementation begins.
```

If the artefact schema or compiled artefact fails validation, implementation must stop and the schema/compile issue must be resolved first.

## PSI dependency rule

The card evidence pilot must not depend on PSI runtime consumption unless the approved identity/PSI runtime design explicitly requires it.

The card pilot may use compiled card evidence derived from research and policy artefacts without waiting for PSI runtime wiring, provided provenance and IDL/presentation safety boundaries are respected.

## Sprint 0 dependency

This sprint must preserve the Sprint 0 `bilirubin` / `total_bilirubin` correction.

The replacement of `wave1_subsystem_evidence.py` or any pilot card evidence path must not reintroduce the false-missing `total_bilirubin` defect.

## Deliverables

```text
knowledge_bus/schema/health_system_card_evidence_schema_v1.yaml
docs/architecture/card_evidence_role_translation_policy.md
docs/architecture/card_visibility_tier_policy.md
knowledge_bus/compiled/health_system_cards/<pilot>.yaml
card evidence validator
backend card evidence loader
DTO v2 or schema-versioned DTO update
frontend render-only update if required
regression tests
legacy comparison report
```

## Classification

```yaml
risk_level: HIGH
change_type: MIXED
execution_model: TWO_PHASE_START_FINISH
```

## Constraints

- Frontend must not infer marker roles.
- No raw research runtime reads.
- No retail prose bypassing IDL.
- No full card estate regeneration.
- No root-cause compiler changes.
- Card evidence pilot must not depend on PSI runtime unless explicitly decided.
- Preserve Sprint 0 bilirubin fix.

## STOP conditions

- Stop if card evidence schema cannot be validated.
- Stop if compiled artefact validation fails.
- Stop before backend/DTO/frontend work if the artefact has not validated.
- Stop if DTO versioning is not agreed.
- Stop if frontend changes would introduce medical logic.
- Stop if the selected subsystem requires unresolved identity/registry work.
- Stop if research-derived wording cannot be safely presented under IDL/retail boundaries.
- Stop if the bilirubin false-missing defect would be reintroduced.

## Success criteria

- One card subsystem is powered by compiled governed evidence.
- Required marker-role and relationship fields reach the DTO.
- Frontend renders backend-provided values only.
- Legacy hard-coded evidence is bypassed or replaced for the pilot path.
- Sprint 0 bilirubin fix remains protected.
- Regression tests pass.

---

# Sprint 5 — ARCH-RT-4_compiled_hypothesis_root_cause_slice

## Purpose

Replace one hand-authored root-cause path with compiled hypothesis intelligence in a governed pilot.

## Rationale

Root-cause YAML currently works, but it is an independent WHY authority where it overlaps with investigation spec hypotheses.

This sprint proves the replacement model without attempting a full estate migration.

## Scope

- Define compiled hypothesis schema.
- Map investigation spec hypotheses into compiled runtime-compatible form.
- Map confirmatory tests to confirmatory test registry IDs.
- Select one pilot pathway.
- Generate compiled hypothesis artefact.
- Compare to existing root-cause YAML.
- Produce divergence report.
- Add compiled hypothesis loader.
- Pilot root_cause_registry transition in shadow mode.
- Preserve legacy YAML for comparison.

## Deliverables

```text
knowledge_bus/schema/compiled_hypothesis_schema_v1.yaml
docs/architecture/compiled_hypothesis_contract.md
compiled hypothesis pilot artefact
root-cause divergence report
compiled hypothesis loader
root_cause_registry transition pilot
shadow comparison report
confirmatory test mapping validation
```

## Classification

```yaml
risk_level: HIGH
change_type: MIXED
execution_model: TWO_PHASE_START_FINISH
```

## Constraints

- Do not discard legacy YAML without divergence adjudication.
- Do not switch the full root-cause compiler estate.
- Do not combine with card evidence work.
- Do not change hypothesis medical content without source research or documented adjudication.

## STOP conditions

- Stop if compiled hypothesis schema cannot represent necessary WHY content.
- Stop if confirmatory test IDs cannot map to the registry.
- Stop if divergence with existing YAML requires clinical adjudication beyond sprint scope.
- Stop if root_cause_registry transition requires wider runtime redesign.

## Success criteria

- One compiled hypothesis path exists.
- It is source-traceable.
- It can be compared against existing root-cause YAML.
- Divergence is explicit and reviewable.
- Shadow root-cause path proves feasibility.

---

# Sprint 6 — ARCH-RT-5_full_regeneration_and_launch_gate

## Purpose

Scale the proven architecture across the estate and produce launch-readiness evidence.

## Rationale

Once the compile foundation, identity model, card evidence slice and hypothesis slice have been proven, HealthIQ can regenerate the active intelligence estate and retire legacy authorities.

This sprint is necessarily large. It is retained as one sprint in this high-level plan to avoid premature micro-splitting, but it must be governed by explicit internal milestones and split criteria in the formal work package.

## Scope

- Compile all valid investigation specs into required runtime artefacts.
- Resolve kb52c batch JSON source problem:
  - extract individual investigation specs
  - classify as legacy_retained
  - or schedule regeneration
- Ensure all active packages have:
  - source_spec_id provenance
  - or explicit legacy_retained classification
- Complete PSI coverage or exception classification.
- Implement PSI runtime wiring where required for launch-critical claims.
- Generate Health Systems Card evidence estate.
- Generate compiled hypothesis/root-cause estate.
- Retire hard-coded Python subsystem evidence as active authority.
- Retire hand-authored root-cause YAML as active authority where replaced.
- Retire/demote legacy duplicate packages.
- Update active authority manifest.
- Produce launch-readiness audit.

## Required internal milestones

The formal Sprint 6 work package must include these internal milestones:

```text
M1 — provenance + collision-safe packages
M2 — card evidence estate
M3 — hypothesis / root-cause estate
M4 — PSI opt-in + runtime wiring
M5 — launch gate
```

## Required split criteria

The formal Sprint 6 work package must include explicit split criteria.

At minimum:

- If kb52c source resolution cannot be completed in-sprint, each affected package must be classified as:
  - `legacy_retained`
  - `deferred_for_regeneration`
  - or `blocked_pending_spec_extraction`
- No affected package may remain unclassified.
- The launch-readiness audit must not run until classification is complete.
- If card evidence estate generation cannot be completed safely, launch gate must treat remaining manual card evidence as a blocker unless explicitly hidden or excluded.
- If hypothesis/root-cause estate generation cannot be completed safely, remaining hand-authored YAML must be explicitly classified and justified.
- If PSI runtime wiring cannot be completed where required for launch-critical claims, either PSI must be classified non-launch-critical for those claims or launch must block.
- If full estate regeneration becomes too wide for one governed package, Sprint 6 must split along the milestone boundaries above rather than smuggling scope.

## Deliverables

```text
full compiled artefact estate
activation package regeneration / exception report
PSI coverage / exception report
PSI runtime wiring evidence where required
legacy package classification
card evidence estate
compiled hypothesis/root-cause estate
active authority manifest
legacy retirement report
day-one launch-readiness audit
research-to-runtime traceability audit
Sentinel/gate evidence
```

## Classification

```yaml
risk_level: HIGH
change_type: MIXED
execution_model: TWO_PHASE_START_FINISH
```

## Constraints

- Do not launch with duplicate active authorities.
- Do not launch with unresolved `signal_id` collapse.
- Do not launch with manual card evidence as active authority.
- Do not launch with PSI runtime-dead where PSI is required for active claims.
- Do not launch with unclassified packages lacking provenance.
- Do not alter unrelated scoring, reference ranges or unit conversion policy.
- Do not leave kb52c / batch JSON source packages unclassified.

## STOP conditions

- Stop if full estate regeneration cannot trace outputs to research sources.
- Stop if kb52c batch JSON source problem cannot be resolved or classified.
- Stop if active package provenance is incomplete.
- Stop if generated card evidence cannot replace manual authority safely.
- Stop if root-cause divergence requires unresolved clinical adjudication.
- Stop if PSI runtime wiring remains unresolved for launch-critical claims.
- Stop if launch-readiness audit cannot prove source → artefact → runtime → DTO → frontend traceability.
- Stop if any milestone exposes scope too large for one governed sprint; split rather than smuggle scope.

## Success criteria

- Active intelligence estate is source-traceable.
- Activation package regeneration path is complete or exceptions are classified.
- Legacy authorities are retired, demoted or explicitly classified.
- Health Systems Cards consume compiled governed evidence.
- Root-cause path has compiled authority where replaced.
- PSI is runtime-consumed where required or explicitly classified as non-launch-critical.
- kb52c / batch JSON packages are resolved or classified.
- Launch-readiness audit passes.

---

## 4. Recommended immediate action

Author Sprint 0 first:

```text
WAVE1-EQUIV1_total_bilirubin_false_missing_fix
```

Then author Sprint 1:

```text
ARCH-RT-0_inventory_and_identity_decisions
```

Do not author Sprint 2+ until Sprint 1 closes and the identity/provenance ADRs are approved.

---

---

# Addendum — Day-One Architecture Carry-Forward Register

This section captures decisions, residual risks and completion conditions that must not be lost between sprint agents.

The day-one architecture must not be declared fully delivered until every item below is either completed, deliberately retired, or explicitly classified as non-launch-critical in the launch-readiness audit.

## A. Provenance and compile-manifest carry-forwards

1. `compile_id` is the canonical compile identifier.
2. `compile_run_id` is transitional only.
3. If both `compile_id` and `compile_run_id` are present, validation must enforce:

```text
compile_run_id == compile_id
```

4. The following fields are allowed to remain optional only while `compile_manifest_schema_v1.yaml` is DRAFT:

```text
activation_keys_emitted
collisions_detected
policy_version
```

5. Before any production compiler use, schema lock, or launch-critical compile-manifest use, ADR-required manifest fields must become required.
6. Any stale `ARCH-RT-2b` reference must be normalised to `ARCH-RT-2` unless a formal sprint split is approved.
7. Compile manifests must support activation-frame identity and package provenance, not merely file-level hashing.

## B. Source provenance carry-forwards

1. `source_spec_id` inferred from package directory names is only an interim identity fallback.
2. Inferred `source_spec_id` must not be treated as canonical research provenance.
3. Later provenance work must distinguish provenance source, for example:

```text
explicit_manifest
source_document_inv_path
inferred_package_id
batch_json_source
unknown
```

4. All active packages must eventually have either:

```text
source_spec_id with source hash / compile manifest evidence
```

or an explicit classification:

```text
legacy_retained
deferred_for_regeneration
blocked_pending_spec_extraction
retire_candidate
```

5. The kb52c / batch JSON package estate must be resolved or classified before launch readiness can pass.

## C. Runtime identity carry-forwards

1. `MULTI_FRAME_PER_DIRECTION` is the selected runtime policy.
2. `activation_key` is required as runtime activation-frame identity.
3. `signal_id` remains signal-family identity and must not be overloaded as frame identity.
4. Duplicate `activation_key` must fail closed.
5. Duplicate `signal_id` across distinct activation frames is valid in the target architecture.
6. Downstream consumers must be reviewed and updated where they assume one fired result per `signal_id`.
7. Interaction map, phenotype map, root-cause compiler and reporting paths must be explicitly reviewed for family-vs-frame semantics.

## D. Root-cause carry-forwards

1. Root-cause compiler remains signal-family-only after ARCH-RT-2.
2. Root-cause first-match behaviour is a temporary tolerated gap, not target architecture.
3. Root-cause must become multi-frame aware or consume compiled hypothesis artefacts using activation-frame identity.
4. Hand-authored root-cause YAML remains a duplicate authority until replaced or explicitly classified.
5. The compiled hypothesis / root-cause sprint must preserve useful existing root-cause content through divergence review before retirement.

## E. PSI carry-forwards

1. PSI exists but was confirmed runtime-dead during ARCH-RT-0.
2. PSI is signal-layer semantics only.
3. PSI must not be expanded to carry full hypothesis graphs.
4. PSI runtime wiring remains pending after ARCH-RT-2.
5. PSI must either be runtime-consumed where needed for launch-critical claims or explicitly classified as non-launch-critical before launch.

## F. Activation compile carry-forwards

1. PSI translation is not activation compile.
2. The governed activation compile path is still required:

```text
investigation_spec
→ signal_library.yaml
→ research_brief.yaml
→ package_manifest.yaml
```

3. Activation compile must propagate:

```text
activation_key
signal_id
source_spec_id
package_id
compile_manifest_ref
```

4. No full estate regeneration can be considered governed until this activation compile path exists or exceptions are classified.

## G. Card evidence carry-forwards

1. Sprint 0 bilirubin correction must not be reintroduced when card evidence is replaced.
2. Hard-coded `wave1_subsystem_evidence.py` remains active until Sprint 4 replaces the pilot path and later Sprint 6 retires or classifies the estate.
3. Card evidence must be compiled from governed research/domain policy artefacts, not hand-authored as a new authority.
4. Frontend must remain render-only and must not infer marker roles, rationales or clinical meaning.
5. DTO versioning is mandatory before card marker-role / relationship-kind / rationale fields can be safely surfaced.

## H. Day-one completion criteria

The day-one architecture is not complete until:

1. Active package provenance is explicit or classified.
2. Compile manifest schema is locked or explicitly approved for launch use.
3. Activation compile exists or all exceptions are classified.
4. Multi-frame runtime identity is accepted by all affected downstream consumers.
5. PSI runtime use is implemented or classified non-launch-critical.
6. Card evidence is compiled/governed or manual paths are hidden/classified.
7. Root-cause/hypothesis authority is compiled/governed or legacy YAML is classified.
8. kb52c / batch JSON source packages are resolved or classified.
9. Launch-readiness audit proves:

```text
source research → compiled artefact → runtime loader → DTO → frontend component
```

for every launch-critical user-facing clinical claim.

## 5. Active Carry-Forward Register

These items must be resolved before the day-one architecture can be declared fully delivered.

### From ARCH-RT-2 — Identity Runtime Pilot

- Directory-derived `source_spec_id` is acceptable only as interim runtime identity fallback.
- It is not canonical research provenance.
- Future provenance work must distinguish explicit `source_spec_id` from inferred `source_spec_id`.
- Root-cause compiler remains signal-family-only and is not yet multi-frame aware.
- Root-cause first-match behaviour is acceptable temporarily only.
- The compiled hypothesis / root-cause transition sprint must make root-cause multi-frame aware or explicitly govern frame selection.

### From ARCH-RT-3 — Card Evidence Vertical Slice

- Raw internal `source_trace` strings must not be shown directly to consumers.
- Any future consumer-facing source/evidence label must be separately designed and retail-safe.
- `compile_manifest_ref` is acceptable as a pilot audit string only.
- Before estate-wide regeneration, `compile_manifest_ref` must resolve to a real manifest file or governed estate index entry.
- Inferred `source_spec_ids` are acceptable for pilot only.
- Full estate compile must resolve explicit versus inferred provenance before launch-critical use.
- Remaining Wave 1 subsystems still on the hard-coded evidence path must be addressed in ARCH-RT-5 or explicitly launch-classified.

### From ARCH-RT-4 — Compiled Hypothesis / Root-Cause Slice

- Compiled hypotheses are currently shadow-only.
- `compile_root_cause_v1()` has not yet been wired to consume compiled hypothesis artefacts.
- ARCH-RT-5 must decide when and how compiled hypotheses begin influencing runtime `RootCauseV1` output.
- `physiological_claim` must not be treated as direct retail/runtime summary text.
- `physiological_claim` is the governed clinical reasoning claim.
- `summary_template` remains the presentation/runtime wording field unless superseded by an explicit mapping policy.
- Before estate migration, ARCH-RT-5 must define the compiled hypothesis → `RootCauseHypothesisV1` presentation mapping.
- The compiled hypothesis artefact must either carry a separate presentation-safe `summary_template` field or emit a root-cause-compatible view that preserves runtime summary semantics.
- Root-cause compiler remains not fully multi-frame aware.
- Multi-frame root-cause selection must be explicitly governed before any multi-frame hypothesis path is promoted.
- Stronger direct cross-load / fail-closed boundary tests should be added before full migration if legacy and compiled loaders remain side-by-side.
- `compile_manifest_ref` remains pilot/manual only until real manifest linkage is implemented.
- `source_spec_provenance: source_document_derived` remains acceptable for pilot only and is not canonical explicit provenance.

## 6. Final note

This is the fewest sensible sprint sequence currently recommended.

Reducing below this would combine fundamentally different risk classes and likely recreate the architecture drift this programme is intended to correct.

The final plan incorporates the Cursor and Claude Code review points:

- explicit activation compile track
- explicit PSI runtime wiring design
- broader package-generation inventory
- decisive ADR-RT-002 requirement
- Sprint 4 internal validation checkpoint
- Sprint 4 protection of the Sprint 0 bilirubin fix
- Sprint 6 milestone governance
- Sprint 6 split criteria and kb52c classification requirement
