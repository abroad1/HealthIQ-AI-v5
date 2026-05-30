---
work_id: ARCH-RT-3_card_evidence_vertical_slice
branch: work/ARCH-RT-3-card-evidence-vertical-slice
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# ARCH-RT-3 — Card Evidence Vertical Slice

## Purpose

Replace hard-coded Wave 1 Health Systems Card evidence for one pilot subsystem with compiled, governed, research-derived card evidence.

This sprint must prove the end-to-end card-evidence architecture on one controlled vertical slice:

```text
research-derived card evidence artefact
→ backend loader
→ DTO v2 / schema-versioned DTO
→ frontend render-only display
````

This sprint must not attempt full card evidence estate regeneration.

## Baseline requirement

Start from clean `main`.

Expected prior completed work:

```text
WAVE1-EQUIV1_total_bilirubin_false_missing_fix — merged
ARCH-RT-0_inventory_and_identity_decisions — merged
ARCH-RT-1_contracts_and_compile_foundation — merged
ARCH-RT-2_identity_runtime_pilot — merged
```

Before creating or switching to the sprint branch, run and report:

```powershell
git branch --show-current
git status --short
git log --oneline -n 8
git rev-parse HEAD
git rev-parse origin/main
```

STOP if:

* current branch is not `main`
* local `main` does not equal `origin/main`
* working tree is not clean
* ARCH-RT-2 is not merged
* untracked or uncommitted files are present

## Governance classification

```yaml
risk_level: HIGH
change_type: MIXED
execution_model: TWO_PHASE_START_FINISH
```

Reason:

This sprint is expected to touch card evidence assembly, DTOs, schema/Knowledge Bus artefacts, tests and possibly frontend rendering. It affects user-facing analytical/card output and may touch `backend/core/analytics/`, which is HIGH risk under SOP.

HIGH-risk controls apply:

* Claude hardening required before kernel start
* Cursor implementation only after kernel start
* Claude audit after implementation
* GPT architectural review before merge
* dual approval before merge

## Authoritative inputs

Read these files before making any changes:

```text
docs/sprints/healthiq_day_one_architecture_rework_sprint_plan_FINAL.md
docs/sprints/healthiq_day_one_architecture_rework_sprint_plan_FINAL_updated.md
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
docs/architecture/compile_manifest_contract.md
docs/architecture/package_provenance_policy.md
docs/architecture/activation_compile_contract.md
docs/architecture/psi_gap_closure_mechanics.md
docs/architecture/psi_runtime_wiring_design.md
docs/architecture/ARCH-RT-1_single_frame_pilot_selection.md
docs/architecture/ARCH-RT-1_pilot_compile_provenance_evidence.md
docs/architecture/ARCH-RT-2_identity_runtime_pilot_report.md
docs/governance/KNOWLEDGE_BUS_SOP_v1.3.md
docs/governance/AUTOMATION_BUS_SOP_v1.3.1.md
```

STOP if any required file is missing.

If `healthiq_day_one_architecture_rework_sprint_plan_FINAL_updated.md` is not present at the exact path above, locate the saved updated sprint plan and report the path before proceeding.

## Mandatory inherited decisions and carry-forwards

The following are binding:

```text
ADR-RT-002 selected MULTI_FRAME_PER_DIRECTION.
activation_key is required.
signal_id remains signal-family identity.
SignalResult now carries activation_key, source_spec_id and package_id.
PSI is runtime-dead unless separately wired later.
Card evidence pilot must not depend on PSI runtime unless explicitly justified.
Root-cause compiler is not yet multi-frame aware.
Directory-derived source_spec_id is interim identity fallback only, not canonical provenance.
Future provenance work must distinguish explicit source_spec_id from inferred source_spec_id.
```

Carry-forward from WAVE1-EQUIV1:

```text
The bilirubin / total_bilirubin false-missing fix must be preserved.
The card evidence pilot must not reintroduce total_bilirubin as an independent required missing marker where bilirubin is canonical.
```

Carry-forward from ARCH-RT-1:

```text
compile_id is canonical.
compile_run_id is transitional only.
If both compile_id and compile_run_id are present, they must be equal.
compile_manifest_schema_v1 remains DRAFT unless explicitly tightened.
```

Do not reopen these decisions.

If repository evidence contradicts any inherited decision, STOP and report.

## Authority preflight

Before editing, verify and report the actual paths and current behaviour for:

1. Wave 1 Health Systems Card subsystem evidence implementation.
2. Hard-coded subsystem definition structure.
3. Current pilot candidate subsystem definitions.
4. Current DTO model for card subsystem evidence.
5. Current frontend component rendering subsystem evidence.
6. Current test coverage for subsystem evidence.
7. Current test coverage for the bilirubin / total_bilirubin fix.
8. Current way included and missing markers are partitioned.
9. Any existing card evidence schema or compiled card evidence artefacts.
10. Any existing card role / visibility-tier policy file.
11. Any existing IDL / retail prose safety path relevant to card text.
12. Whether the candidate pilot subsystem depends on PSI runtime.

If any authority path cannot be verified, STOP and report.

## Pilot selection

Select exactly one pilot subsystem.

Preferred candidates from the sprint plan:

```text
glycaemic control subsystem
lipid transport subsystem
```

Final selection must be evidence-based and justified from ARCH-RT-0 inventory and current code.

Selection criteria:

* cleanest authority chain
* lowest ambiguity
* limited marker set
* minimal dependency on unresolved PSI runtime wiring
* no unresolved multi-frame identity blocker
* no root-cause compiler dependency
* medically coherent as one subsystem
* manageable DTO/frontend impact

Do not select a subsystem if it depends on unresolved root-cause or PSI runtime semantics.

STOP if no safe pilot subsystem exists.

## Mandatory internal checkpoint

This sprint has a hard internal checkpoint.

Before implementing backend loader, DTO changes, or frontend changes:

```text
The compiled card evidence schema and pilot artefact must validate.
```

If the schema or pilot artefact cannot validate, STOP.

Do not proceed into backend/DTO/frontend implementation until the artefact validates.

## Scope

Allowed implementation scope:

1. Define card evidence schema.
2. Define card role translation policy.
3. Define visibility-tier policy.
4. Compile/create one pilot card evidence artefact.
5. Validate the pilot artefact.
6. Add backend loader for compiled card evidence.
7. Wire only the selected pilot subsystem through the compiled evidence path.
8. Add DTO v2 or schema-versioned DTO extension as needed.
9. Update frontend only to render backend-provided fields.
10. Add regression coverage.
11. Add legacy comparison evidence.
12. Preserve existing behaviour outside the pilot path.

## Required deliverables

Create or update:

```text
knowledge_bus/schema/health_system_card_evidence_schema_v1.yaml
docs/architecture/card_evidence_role_translation_policy.md
docs/architecture/card_visibility_tier_policy.md
knowledge_bus/compiled/health_system_cards/<pilot>.yaml
docs/architecture/ARCH-RT-3_card_evidence_vertical_slice_report.md
```

Implementation files may be added/updated only as required for:

```text
backend card evidence loader
backend assembler integration for pilot only
DTO v2 / schema-versioned DTO
frontend render-only display, if required
targeted tests
```

## Card evidence schema requirements

The schema must support at minimum:

```yaml
schema_version:
artefact_id:
domain_id:
subsystem_id:
subsystem_label:
visibility_tier:
source_spec_ids:
compile_manifest_ref:
markers:
  - marker_id:
    display_label:
    marker_role:
    relationship_kind:
    rationale_short:
    presence_policy:
missing_policy_line:
mechanism_line:
provenance:
```

Required role vocabulary must include, at minimum:

```text
score_contributor
confidence_contributor
contextual_marker
mechanism_marker
differential_marker
exclusion_marker
missing_for_confidence
optional_deeper_marker
```

Required visibility tiers must include:

```text
scored_subsystem
contextual_evidence
hidden_v1
```

If the pilot does not need all fields, fields may be optional only if the schema documents why.

## Card role translation policy requirements

`docs/architecture/card_evidence_role_translation_policy.md` must define:

* how research/package/PSI role concepts translate into card roles
* how marker roles differ from scoring rail participation
* how contextual markers differ from score contributors
* how missing-for-confidence differs from absent/not-uploaded
* how frontend must treat role fields
* rule that frontend must not infer clinical role from marker name

## Visibility-tier policy requirements

`docs/architecture/card_visibility_tier_policy.md` must define:

* `scored_subsystem`
* `contextual_evidence`
* `hidden_v1`
* how medical review controls visibility
* how thin evidence should be suppressed or shown as contextual
* how future full estate regeneration should apply the policy

## Pilot artefact requirements

The pilot artefact must:

* validate against schema
* include only the selected pilot subsystem
* include source/provenance fields available today
* not claim canonical source_spec_id where only inferred provenance exists
* not depend on raw investigation spec runtime reads
* not depend on PSI runtime unless explicitly justified
* not include retail prose that bypasses IDL / safety boundaries
* not reintroduce the `total_bilirubin` false-missing defect

## Backend loader requirements

If implementation proceeds past the validation checkpoint, the backend loader must:

* load compiled card evidence from the governed artefact path
* fail closed on invalid artefact structure
* expose card evidence to assembler for the pilot subsystem only
* not read raw investigation specs at runtime
* not infer marker roles from frontend or string matching
* preserve existing non-pilot subsystem behaviour

## DTO requirements

If DTO changes are required:

* use a v2 or schema-versioned DTO approach
* do not break existing consumers unnecessarily
* include marker-level role/relationship fields where needed
* include visibility tier where needed
* preserve existing fields where possible
* add tests proving serialisation shape

## Frontend requirements

If frontend changes are required:

* render backend-provided fields only
* do not infer marker roles
* do not infer clinical meaning
* respect visibility tier
* handle absent optional fields safely
* do not add new clinical prose beyond backend/IDL-approved fields

## Out of scope

Do not:

* perform full card evidence estate regeneration
* wire all subsystems
* modify root-cause compiler
* modify root-cause YAML
* modify PSI artefacts
* implement PSI runtime wiring
* modify SignalRegistry
* modify SignalEvaluator
* modify SignalResult unless strictly required and approved by hardening
* modify package files
* modify investigation specs
* modify biomarker SSOT
* modify scoring rails
* modify unit conversion
* modify clinical thresholds
* create compiled hypothesis artefacts
* change IDL copy/content
* introduce fallback parsers
* commit helper scripts

## Required tests

At minimum, add or update tests covering:

1. Schema validation for card evidence artefact.
2. Pilot artefact validation.
3. Backend loader success path.
4. Backend loader fail-closed behaviour for invalid artefact.
5. Pilot subsystem assembly using compiled evidence.
6. Non-pilot subsystem behaviour remains unchanged.
7. DTO serialisation for new fields.
8. Frontend render-only behaviour, if frontend is touched.
9. Regression that `total_bilirubin` is not falsely reported missing when `bilirubin` is present.
10. Regression that frontend or backend does not infer marker roles from names.

Run narrow tests first. Run broader relevant tests only if touched contracts require them.

## STOP conditions

STOP and report without implementing further if:

1. Required authoritative input files are missing.
2. No safe pilot subsystem can be selected.
3. Card evidence schema cannot be defined without unresolved medical policy.
4. Pilot artefact cannot validate.
5. Backend implementation would require raw investigation spec runtime reads.
6. Backend implementation would require PSI runtime wiring not approved in this sprint.
7. DTO change would require broad report/result contract redesign.
8. Frontend changes would introduce clinical inference.
9. The bilirubin / total_bilirubin fix would be reintroduced.
10. Root-cause or SignalRegistry changes appear necessary.
11. Scope expands beyond one pilot subsystem.
12. Tests cannot prove pilot/non-pilot separation.
13. Helper scripts would need to be committed.
14. Compile manifest carry-forward conditions would be violated.

## Required report

Create:

```text
docs/architecture/ARCH-RT-3_card_evidence_vertical_slice_report.md
```

The report must include:

* pilot selected and rationale
* alternatives rejected
* schema created
* artefact path
* validation result
* backend loader path
* DTO changes
* frontend changes, if any
* tests added/updated
* test commands and results
* confirmation that non-pilot subsystems are unchanged
* confirmation that the bilirubin fix is preserved
* confirmation that PSI runtime wiring was not introduced
* confirmation that root-cause / SignalRegistry were not modified
* remaining risks and carry-forwards

## Evidence required from Cursor

Cursor must report:

1. Baseline branch/status/HEAD evidence.
2. Authority preflight findings.
3. Pilot subsystem selected and rationale.
4. Files changed.
5. Internal checkpoint result proving artefact validation before backend/DTO/frontend implementation.
6. Exact implementation changes.
7. DTO/frontend impact.
8. Tests added/updated.
9. Test commands run.
10. Test results.
11. Confirmation that only one subsystem was piloted.
12. Confirmation that non-pilot subsystems are unchanged.
13. Confirmation that the `total_bilirubin` fix is preserved.
14. Confirmation that no PSI/root-cause/package/spec/SignalRegistry/SignalEvaluator work was included.
15. Confirmation that no helper scripts were committed.

## Closure requirements

Before `run_work_package.py finish`, complete the Automation Bus post-implementation closure protocol.

Run and report:

```powershell
git branch --show-current
git status --short
git log --oneline -n 5
git diff --name-only
git diff --cached --name-only
git stash list
```

Classify:

* tracked modified files
* staged files
* untracked files
* tooling files
* out-of-scope files
* stash entries

Do not run finish unless:

* current branch matches `work/ARCH-RT-3-card-evidence-vertical-slice`
* only in-scope files are changed
* no package files are changed
* no investigation specs are changed
* no PSI artefacts are changed
* no root-cause YAML is changed
* no SignalRegistry / SignalEvaluator files are changed
* no helper scripts are included
* no ambiguous stash exists
* latest commit contains only in-scope work

## Success criteria

This sprint is complete only if:

1. One pilot subsystem is powered by compiled governed card evidence.
2. Card evidence schema exists and validates.
3. Pilot artefact exists and validates.
4. Artefact validation occurred before backend/DTO/frontend work.
5. Backend loader works for pilot path.
6. DTO carries required card evidence fields.
7. Frontend, if touched, renders backend-provided fields only.
8. Non-pilot subsystem behaviour is unchanged.
9. `total_bilirubin` false-missing defect remains fixed.
10. No PSI runtime wiring is introduced.
11. No root-cause or SignalRegistry work is included.
12. Tests prove the new pilot path and regression boundaries.
13. Automation Bus gate passes.

```
```
