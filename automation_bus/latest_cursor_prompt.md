---
work_id: ARCH-RT-5B_card_evidence_estate_and_required_provenance
branch: work/ARCH-RT-5B-card-evidence-estate-and-required-provenance
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# ARCH-RT-5B — Card Evidence Estate and Required Provenance

## Purpose

Extend the successful ARCH-RT-3 card evidence vertical slice across the remaining Wave 1 Health Systems Card subsystems, or explicitly classify any subsystem that cannot safely move to compiled card evidence yet.

This sprint must resolve the card-evidence estate position for Wave 1:

```text
compiled card evidence artefacts
→ governed backend loader
→ DTO v2 / schema-versioned DTO
→ frontend render-only display
→ launch classification for every Wave 1 subsystem
````

This sprint also includes the minimum package/source provenance work required to support the Wave 1 card evidence estate.

It must not attempt full 186-package provenance backfill unless required for Wave 1 card evidence.

## Baseline requirement

Start from clean `main`.

Expected prior completed work:

```text
WAVE1-EQUIV1_total_bilirubin_false_missing_fix — merged
ARCH-RT-0_inventory_and_identity_decisions — merged
ARCH-RT-1_contracts_and_compile_foundation — merged
ARCH-RT-2_identity_runtime_pilot — merged
ARCH-RT-3_card_evidence_vertical_slice — merged
ARCH-RT-4_compiled_hypothesis_root_cause_slice — merged
ARCH-RT-5_full_regeneration_and_launch_gate — merged
```

Before creating or switching to the sprint branch, run and report:

```powershell
git branch --show-current
git status --short
git log --oneline -n 12
git rev-parse HEAD
git rev-parse origin/main
```

STOP if:

* current branch is not `main`
* local `main` does not equal `origin/main`
* working tree is not clean
* ARCH-RT-5 is not merged
* untracked or uncommitted files are present

## Governance classification

```yaml
risk_level: HIGH
change_type: MIXED
execution_model: TWO_PHASE_START_FINISH
```

Reason:

This sprint may touch compiled Knowledge Bus artefacts, schema/validator surfaces, Health Systems Card backend loader/assembler paths, DTOs, frontend render-only card components, tests and audit artefacts. It may touch `backend/core/analytics/`, which is an unconditional HIGH-risk path.

HIGH-risk controls apply:

* Claude hardening required before kernel start
* Cursor implementation only after kernel start
* Claude audit after implementation
* GPT architectural review before merge
* dual approval before merge

## Authoritative inputs

Read these files before making changes:

```text
docs/sprints/healthiq_day_one_architecture_rework_sprint_plan_FINAL_updated.md
docs/architecture/ADR-RT-001_research_to_runtime_day_one_architecture.md
docs/architecture/ADR-RT-002_signal_spec_identity_and_registry_policy.md
docs/architecture/ADR-RT-003_hypothesis_artefact_and_root_cause_transition.md
docs/architecture/ADR-RT-004_compile_manifest_and_package_provenance_policy.md
docs/architecture/card_evidence_role_translation_policy.md
docs/architecture/card_visibility_tier_policy.md
docs/architecture/ARCH-RT-3_card_evidence_vertical_slice_report.md
docs/audit-papers/ARCH-RT-5_M1_package_provenance_and_collision_audit.md
docs/audit-papers/ARCH-RT-5_M2_card_evidence_estate_audit.md
docs/audit-papers/day_one_architecture_launch_readiness_audit.md
docs/audit-papers/research_to_runtime_traceability_audit.md
docs/audit-papers/active_intelligence_authority_manifest.md
docs/architecture/ARCH-RT-5_full_regeneration_and_launch_gate_report.md
docs/architecture/ARCH-RT-5_split_recommendation.md
knowledge_bus/schema/health_system_card_evidence_schema_v1.yaml
knowledge_bus/compiled/health_system_cards/wave1_met_glycaemic_control.yaml
knowledge_bus/compiled/estate_index_v1.yaml
docs/governance/KNOWLEDGE_BUS_SOP_v1.3.md
docs/governance/AUTOMATION_BUS_SOP_v1.3.1.md
```

STOP if any required authority file is missing.

If the updated sprint plan has a different path, locate it and report the path before proceeding.

## Mandatory inherited decisions and carry-forwards

The following are binding:

```text
Health Systems Card evidence is separate from hypothesis/root-cause artefacts.
PSI remains signal-layer semantics only and must not be used directly as card evidence authority.
Frontend must render backend-provided card evidence only.
Frontend must not infer clinical role from marker name or marker id.
Raw internal source_trace strings must not be displayed directly to consumers.
compile_id is canonical.
compile_run_id is transitional only.
If both compile_id and compile_run_id are present, they must be equal.
activation_key is required for runtime activation identity.
signal_id remains signal-family identity.
```

Carry-forward from WAVE1-EQUIV1:

```text
The bilirubin / total_bilirubin false-missing fix must be preserved.
No compiled card evidence artefact may reintroduce total_bilirubin as an independent required missing marker where bilirubin is canonical.
```

Carry-forward from ARCH-RT-3:

```text
wave1_met_glycaemic_control is already on the compiled card evidence path.
The compiled card evidence loader and DTO v2 path already exist.
Non-pilot subsystems remained on legacy hard-coded evidence after ARCH-RT-3.
```

Carry-forward from ARCH-RT-5:

```text
Six hard-coded Wave 1 card subsystems remained launch-classified legacy, not resolved.
ARCH-RT-5B must complete or further classify the remaining card evidence estate.
compile_manifest_ref must resolve to a real manifest file or governed estate index entry for any promoted compiled artefact.
Inferred source_spec_ids are acceptable only if explicitly declared as inferred, not explicit canonical provenance.
```

Do not reopen these decisions.

If repository evidence contradicts any inherited decision, STOP and report.

## Current estate to resolve

ARCH-RT-5 identified seven Wave 1 subsystems.

One is already compiled:

```text
wave1_met_glycaemic_control
```

Six remained hard-coded legacy at ARCH-RT-5:

```text
wave1_cv_lipid_transport
wave1_cv_homocysteine_pathway
wave1_cv_vascular_strain
wave1_met_insulin_metabolic
wave1_liv_enzyme_pattern
wave1_liv_processing_context
```

This sprint must resolve each of those six as one of:

```text
compiled_card_evidence
contextual_evidence
hidden_v1
legacy_retained_with_justification
blocked_pending_provenance
blocked_pending_medical_review
```

No subsystem may remain unclassified.

## Authority preflight

Before implementation, verify and report:

1. Current compiled card evidence artefacts.
2. Current health system card evidence schema.
3. Current card evidence loader.
4. Current Wave 1 subsystem hard-coded definitions.
5. Current DTO model for subsystem evidence.
6. Current frontend component rendering subsystem evidence.
7. Current estate index and compile manifest structure.
8. Current source trace display behaviour.
9. Current bilirubin / total_bilirubin regression tests.
10. Current test coverage for ARCH-RT-3 compiled card evidence.
11. Current package/source provenance for each marker in the six unresolved subsystems.
12. Whether any unresolved subsystem requires PSI runtime to produce safe card evidence.
13. Whether any unresolved subsystem requires root-cause/hypothesis output to produce safe card evidence.

If any authority path cannot be verified, STOP and report.

## Mandatory internal checkpoint

Before backend/DTO/frontend changes, complete and validate the compiled artefact/classification plan.

Checkpoint requirements:

1. Each of the six unresolved Wave 1 subsystems has a proposed classification.
2. Any subsystem moving to compiled card evidence has a draft artefact.
3. Draft artefacts validate against schema.
4. Required compile_manifest_ref values are either real or explicitly classified.
5. Required provenance is explicit or clearly marked inferred.
6. No artefact reintroduces the bilirubin / total_bilirubin defect.
7. No artefact depends on PSI runtime unless explicitly justified.

If this checkpoint fails, STOP before implementation wiring.

## Scope

Allowed scope:

1. Generate compiled card evidence artefacts for remaining Wave 1 subsystems where safe.
2. Create real compile manifests for promoted card evidence artefacts.
3. Update estate index for promoted card evidence artefacts.
4. Extend or adjust card evidence schema only if required and backward-compatible.
5. Extend loader/assembler only as needed to support multiple compiled subsystems.
6. Preserve legacy hard-coded path only for classified retained subsystems.
7. Update DTO/frontend only if required to handle estate-wide card evidence fields already designed in ARCH-RT-3.
8. Produce card evidence estate audit.
9. Produce required provenance classification for card-related sources/packages only.
10. Add regression and boundary tests.

## Required deliverables

Create or update:

```text
knowledge_bus/compiled/health_system_cards/*.yaml
knowledge_bus/compiled/manifests/*.yaml
knowledge_bus/compiled/estate_index_v1.yaml
docs/audit-papers/ARCH-RT-5B_card_evidence_estate_audit.md
docs/audit-papers/ARCH-RT-5B_card_evidence_provenance_audit.md
docs/architecture/ARCH-RT-5B_card_evidence_estate_report.md
```

Implementation files may be updated only as required for:

```text
card evidence loader multi-subsystem support
Wave 1 subsystem assembler compiled-path expansion
DTO/front-end render-only support if required
targeted tests
```

## Artefact requirements

Each compiled card evidence artefact must:

* validate against `health_system_card_evidence_schema_v1.yaml`
* include one subsystem only
* declare `domain_id`
* declare `subsystem_id`
* declare `visibility_tier`
* include marker roles
* include relationship kinds where available
* include source/provenance status
* include `compile_manifest_ref`
* not use raw internal source trace as consumer-facing copy
* not use PSI as direct card authority
* not use root-cause/hypothesis text as card authority
* not claim explicit `source_spec_id` where provenance is inferred
* not include `total_bilirubin` as an independent required missing marker where `bilirubin` is canonical

## Provenance requirements

For each card artefact, classify source provenance as one of:

```text
explicit_source_spec_id
source_document_derived
package_manifest_inferred
package_id_inferred
legacy_retained_with_justification
blocked_pending_spec_extraction
blocked_pending_medical_review
```

If provenance is inferred, it must be explicitly declared as inferred.

Do not treat inferred provenance as canonical explicit provenance.

## Compile manifest requirements

For every promoted compiled card artefact:

* `compile_manifest_ref` must resolve to a real manifest file or governed estate index entry.
* Manifest must include `compile_id`.
* If `compile_run_id` exists, it must equal `compile_id`.
* Manifest must include or explicitly classify:

  * `activation_keys_emitted`
  * `collisions_detected`
  * `policy_version`
* Any DRAFT permissiveness must be documented and justified.

## Backend behaviour requirements

If compiled evidence is promoted for a subsystem:

* backend loader must load from compiled artefact path
* invalid artefact must fail closed
* assembler must route that subsystem through compiled path
* non-promoted subsystems must either remain legacy with classification or be hidden/contextual
* no raw investigation spec runtime reads
* no role inference from marker id or marker name
* no PSI runtime dependency unless justified

## DTO/frontend requirements

If touched:

* DTO fields must remain backward-compatible
* frontend must render backend-provided fields only
* frontend must not infer clinical meaning
* frontend must not display raw internal `source_trace`
* consumer-facing wording must remain retail-safe
* optional fields must be handled safely

## Out of scope

Do not:

* perform hypothesis/root-cause runtime promotion
* modify root-cause YAML
* modify compiled hypothesis runtime behaviour
* modify SignalRegistry
* modify SignalEvaluator
* implement PSI runtime wiring unless a STOP condition proves card evidence cannot proceed without it
* perform full 186-package provenance backfill
* modify investigation specs
* modify package files unless hardening explicitly approves a narrow manifest-only change
* modify biomarker SSOT
* change scoring rails
* change clinical thresholds
* change unit conversion
* add fallback parsers
* expose raw source trace to consumers
* commit helper scripts

## Required tests

At minimum:

1. Schema validation for every promoted card artefact.
2. Manifest resolution test for every promoted card artefact.
3. Estate index test covering all Wave 1 subsystems.
4. Loader success path for every promoted artefact.
5. Loader fail-closed path for invalid artefact.
6. Assembler test proving promoted subsystems use compiled path.
7. Assembler test proving retained legacy subsystems remain classified and stable.
8. Regression that `total_bilirubin` false-missing is not reintroduced.
9. DTO serialisation tests if DTO touched.
10. Frontend render-only tests if frontend touched.
11. Test that raw internal source trace is not consumer-rendered.
12. Test that frontend/backend does not infer marker roles from names.

Run narrow tests first. Run broader tests if touched contracts require them.

## STOP conditions

STOP and report if:

1. Required authority files are missing.
2. Any of the six unresolved Wave 1 subsystems cannot be classified.
3. Artefact validation fails.
4. Compile manifest refs cannot resolve and cannot be explicitly classified.
5. Provenance cannot be classified.
6. Card evidence requires unresolved PSI runtime wiring.
7. Card evidence requires root-cause/hypothesis text.
8. Backend changes would require raw investigation spec runtime reads.
9. Frontend changes would infer medical meaning.
10. The bilirubin / total_bilirubin fix would be reintroduced.
11. Scope expands into root-cause, PSI, SignalRegistry or full package backfill.
12. Tests cannot prove compiled/legacy separation.

## Required reports

Create:

```text
docs/audit-papers/ARCH-RT-5B_card_evidence_estate_audit.md
docs/audit-papers/ARCH-RT-5B_card_evidence_provenance_audit.md
docs/architecture/ARCH-RT-5B_card_evidence_estate_report.md
```

The estate audit must include every Wave 1 subsystem and classify it.

The provenance audit must classify every source/provenance dependency used for promoted card evidence.

The architecture report must include:

* subsystems promoted
* subsystems retained/classified
* artefacts created
* manifests created
* estate index changes
* backend changes
* DTO/frontend changes, if any
* tests run
* remaining risks
* carry-forwards

## Evidence required from Cursor

Cursor must report:

1. Baseline branch/status/HEAD evidence.
2. Authority preflight findings.
3. Subsystem classification table.
4. Internal checkpoint result.
5. Files changed.
6. Artefacts created/updated.
7. Manifests created/updated.
8. Estate index changes.
9. Backend/DTO/frontend changes.
10. Tests added/updated.
11. Test commands run.
12. Test results.
13. Confirmation that bilirubin fix is preserved.
14. Confirmation that no PSI/root-cause/SignalRegistry/SignalEvaluator work was included.
15. Confirmation that no raw source trace is consumer-rendered.
16. Confirmation that no helper scripts were committed.

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

* current branch matches `work/ARCH-RT-5B-card-evidence-estate-and-required-provenance`
* all changed files are tied to this sprint
* no package/spec/PSI/root-cause/SignalRegistry/SignalEvaluator files are changed unless explicitly approved by hardening
* no helper scripts are included
* no ambiguous stash exists
* all six unresolved Wave 1 subsystems are classified
* latest commit contains only in-scope work

## Success criteria

This sprint is complete only if:

1. All seven Wave 1 subsystems are classified.
2. Promoted subsystems are powered by compiled governed card evidence.
3. Retained/non-promoted subsystems are explicitly classified.
4. No unclassified hard-coded card evidence remains.
5. Required compile manifests resolve or are explicitly classified.
6. Required provenance is explicit or clearly marked inferred.
7. Bilirubin / total_bilirubin fix remains protected.
8. Frontend remains render-only.
9. Raw internal source trace is not consumer-rendered.
10. No PSI/root-cause/SignalRegistry/SignalEvaluator work is included.
11. Tests prove compiled/legacy separation and card estate classification.
12. Automation Bus gate passes.

```
```
