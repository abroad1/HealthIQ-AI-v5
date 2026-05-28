---
work_id: ARCH-RT-0_inventory_and_identity_decisions
branch: work/ARCH-RT-0-inventory-and-identity-decisions
risk_level: STANDARD
execution_model: TWO_PHASE_START_FINISH
change_type: CONTENT
---

# ARCH-RT-0 — Inventory and Identity Decisions

## Purpose

Produce the authoritative inventory and architecture decision set required before any further day-one architecture implementation work begins.

This sprint combines the confirmed-safe WP0 and WP1 work:

1. inventory and authority trace
2. identity / ADR / registry policy decisions

This is a documentation and architecture-decision sprint only.

No runtime code, schema, package, compiler, validator, frontend, or control-plane changes are authorised.

## Current baseline

Start from clean `main`.

Expected latest confirmed baseline:

```text
main == origin/main at eb44cf4
WAVE1-EQUIV1_total_bilirubin_false_missing_fix merged and closed
````

Before creating the sprint branch, run and report:

```powershell
git branch --show-current
git status --short
git log --oneline -n 5
git rev-parse HEAD
git rev-parse origin/main
```

STOP if:

* current branch is not `main`
* local `main` does not equal `origin/main`
* working tree is not clean
* HEAD is not at or after `eb44cf4`
* unresolved untracked planning, audit, sprint, or architecture documents remain

## Governance classification

```yaml
risk_level: STANDARD
change_type: CONTENT
execution_model: TWO_PHASE_START_FINISH
```

Reason:

This sprint creates documentation and ADR outputs only under `docs/architecture/`.

It must not modify files consumed by the Intelligence Core.

If Cursor determines that any required work would touch:

```text
backend/core/**
backend/ssot/**
knowledge_bus/**
automation_bus/**
frontend/**
sentinel/**
```

then STOP and report. Do not widen the sprint.

## Authoritative planning inputs

Read the following planning/audit documents before producing outputs:

```text
docs/sprints/healthiq_day_one_architecture_rework_sprint_plan_FINAL.md
docs/planning-papers/HealthIQ_As-Is_to_Day-One_Architecture_Transition_Plan_v3.md
docs/planning-papers/HealthIQ_As-Is_to_Day-One_Architecture_Transition_Plan_v3_review_cursor.md
docs/planning-papers/HealthIQ_As-Is_to_Day-One_Architecture_Transition_Plan_v3_review_claude.md
docs/architecture/ARCH-R1_research_asset_to_runtime_intelligence_architecture_review_cursor.md
docs/architecture/ARCH-R1_research_asset_to_runtime_intelligence_architecture_review.md
docs/governance/KNOWLEDGE_BUS_SOP_v1.3.md
docs/governance/AUTOMATION_BUS_SOP_v1.3.1.md
```

If any file is missing, STOP and report the missing path.

If equivalent files exist under a different path, report the candidate path and STOP for human/GPT confirmation before proceeding.

## Authority preflight

Before authoring documents, inspect the repository and report the actual locations for:

1. investigation spec corpus
2. Knowledge Bus package directories
3. package manifest files
4. promoted signal intelligence schema / translator / loader
5. existing PSI artefacts
6. root-cause hypothesis YAML files
7. root_cause_registry implementation
8. Wave 1 subsystem evidence implementation
9. SignalRegistry / SignalEvaluator implementation
10. SignalResult model
11. Health Systems Card DTO models
12. frontend Health Systems Card components
13. IDL / retail explainer assets
14. interaction map / phenotype map / calibration / confirmatory-test registry assets

This preflight is read-only.

Do not edit any of those files.

## Scope

Produce a complete repo-reality inventory and decisive architecture decision set.

### Inventory scope

Inventory must cover:

* investigation spec corpus
* package generations
* all package-generation prefixes found, including but not limited to:

  * legacy
  * s24
  * kb45
  * kb47
  * kb52
  * kb52c
  * kb52d
  * kb58
  * kb59
  * kb60
  * kb61
  * any other package generations found in the repository
* package `source_document` values
* packages with individual investigation spec provenance
* packages sourcing from batch JSON
* packages with `source_spec_id` if present
* packages without source provenance
* packages requiring `legacy_retained`, `deferred_for_regeneration`, or `blocked_pending_spec_extraction` classification later
* PSI artefacts on disk
* PSI package-manifest opt-ins
* confirmation that PSI is runtime-dead, or correction if that is no longer true
* root-cause hypothesis YAML files
* root_cause_registry registrations
* duplicate `signal_id` collisions
* current retained/discarded package behaviour where detectable
* Health Systems Card hard-coded evidence
* IDL / retail explainer dependencies
* interaction map / phenotype map / calibration / confirmatory-test registry dependencies
* DTO/frontend traceability for user-facing claims
* whether existing translators/compilers have been tested against candidate inventory entries
* activation compile gap:

  * whether governed `investigation_spec → signal_library.yaml` compile exists
  * whether governed `investigation_spec → research_brief.yaml` compile exists
  * whether governed `investigation_spec → package_manifest.yaml` compile exists
  * how this differs from PSI translation

### ADR / decision scope

Produce architecture decisions covering:

* ADR-008 acceptance
* PSI scope confirmation
* compiled hypothesis artefact boundary
* one-frame versus multi-frame runtime policy
* registry keying policy
* whether `activation_key` is required
* SignalResult provenance requirements
* interaction map / phenotype map / root-cause registry family-vs-frame policy
* package provenance policy
* activation compile policy:

  * `investigation_spec → signal_library.yaml`
  * `investigation_spec → research_brief.yaml`
  * `investigation_spec → package_manifest.yaml`
* root_cause_registry transition direction
* compile manifest convention

## Required deliverables

Create the following files only:

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

No other committed files are allowed unless explicitly justified and approved before implementation.

## Deliverable requirements

### 1. `research_to_runtime_traceability_matrix.md`

Must map, as far as repo evidence allows:

```text
investigation spec → package
investigation spec → PSI
investigation spec → root-cause YAML
investigation spec → card evidence
package → SignalRegistry
signal → DTO
DTO → frontend component
```

Where traceability is missing, state one of:

```text
MISSING
UNKNOWN
BATCH_JSON_ONLY
LEGACY_RETAINED_CANDIDATE
BLOCKED_PENDING_SPEC_EXTRACTION
```

Do not guess.

### 2. `intelligence_authority_inventory.md`

Must list current active and candidate authorities for:

* research source
* signal activation
* signal semantics / PSI
* hypothesis / WHY
* Health Systems Card evidence
* IDL / presentation safety
* DTO boundary
* frontend rendering

For each authority, state:

```text
current role
runtime consumed: YES/NO/UNKNOWN
source provenance status
duplicate authority risk
target-state recommendation
```

### 3. `package_generation_inventory.md`

Must include exact counts by package generation/prefix.

Must include at minimum:

```text
generation/prefix
count
source_document pattern
schema_version if available
PSI on disk count
PSI manifest opt-in count
source_spec_id present count
batch JSON source count
individual spec source count
unknown source count
```

Do not rely on approximate counts from planning papers.

### 4. `psi_coverage_and_manifest_opt_in_report.md`

Must confirm:

* PSI schema path
* PSI translator path
* PSI loader path
* number of PSI artefacts on disk
* number of packages with PSI manifest opt-in
* whether PSI is consumed by runtime analytics paths
* where PSI is used today, if anywhere
* which packages/specs are candidates for PSI gap closure
* whether PSI runtime wiring is required for launch-critical claims or can be deferred

### 5. `root_cause_registry_inventory.md`

Must include:

* root-cause YAML file count
* registered root-cause target count
* registry implementation path
* loader paths
* signal IDs registered
* duplicate or shared YAML usage
* missing source_spec_id / provenance issues
* proposed transition direction:

  * manual tuple retained temporarily
  * generated registry
  * manifest-backed registry
  * compiled hypothesis loader

### 6. `signal_id_collision_inventory.md`

Must include:

* every duplicate `signal_id` found across packages
* package paths involved
* current retained/discarded behaviour where detectable
* whether collision affects live runtime
* whether collision is single-frame duplicate or multi-frame medical case
* specific explicit row for ALT high collision
* homocysteine-related cases if present
* recommended handling category:

  * hard error
  * governed arbitration
  * multi-frame support
  * legacy duplicate retirement

### 7. `legacy_package_retirement_candidates.md`

Must classify packages as far as evidence allows:

```text
active_current
legacy_retained_candidate
deferred_for_regeneration
blocked_pending_spec_extraction
retire_candidate
unknown_requires_review
```

Must identify packages lacking sufficient provenance.

### 8. `activation_compile_gap_report.md`

Must answer:

1. Does a governed `investigation_spec → signal_library.yaml` compiler exist?
2. Does a governed `investigation_spec → research_brief.yaml` compiler exist?
3. Does a governed `investigation_spec → package_manifest.yaml` compiler exist?
4. What scripts currently generate or ingest package artefacts?
5. How do those differ from the PSI translator?
6. What is missing before full estate regeneration can be governed?
7. Which later sprint should own activation compile implementation?

### 9. `ADR-RT-001_research_to_runtime_day_one_architecture.md`

Must decide:

* canonical research authority
* compiled runtime artefact model
* accepted target pipeline
* no raw research runtime reads
* no frontend medical inference
* relationship to final sprint plan

### 10. `ADR-RT-002_signal_spec_identity_and_registry_policy.md`

This ADR must be decisive.

It must choose one:

```text
ONE_FRAME_PER_DIRECTION
MULTI_FRAME_PER_DIRECTION
```

It must not leave both options open.

It must also decide:

* registry keying policy
* whether `activation_key` is required
* whether `signal_id + spec_id` is sufficient
* SignalResult provenance requirements
* how interaction map / phenotype map / root-cause registry relate to signal family versus frame identity
* implications for Sprint 3 identity runtime pilot

If evidence is insufficient to choose, STOP and report exactly what evidence is missing. Do not write an indecisive ADR.

### 11. `ADR-RT-003_hypothesis_artefact_and_root_cause_transition.md`

Must decide:

* ADR-008 accepted or challenged
* PSI remains signal-layer only or not
* hypothesis artefact boundary
* relationship between investigation spec hypotheses and root-cause YAML
* whether compiled hypothesis artefact should be consumed directly or emit root-cause-compatible view
* root_cause_registry transition direction

### 12. `ADR-RT-004_compile_manifest_and_package_provenance_policy.md`

Must decide:

* compile manifest convention
* per-run / per-artefact / estate index approach
* required provenance fields
* `source_spec_id` policy
* `legacy_retained` classification policy
* batch JSON source handling
* package promotion / traceability expectations

## Out of scope

Do not:

* modify runtime code
* modify package files
* modify investigation specs
* modify PSI artefacts
* modify root-cause YAML
* modify schemas
* modify validators
* modify Sentinel packs
* modify frontend
* modify `wave1_subsystem_evidence.py`
* modify `SignalRegistry`
* modify `SignalEvaluator`
* run package regeneration
* run compiler implementation
* create new runtime artefacts
* create helper scripts committed to the repository
* introduce fallback parsers

Read-only shell/Python commands are allowed for inventory if they do not modify the repository.

If temporary helper scripts are needed, create them outside the repository or remove them before closure. Do not commit tooling files.

## Required evidence from Cursor

Cursor must report:

1. Baseline branch/status/HEAD evidence.
2. Authority preflight findings.
3. File/path evidence for all inventoried authorities.
4. Exact commands used for package counts and collision detection.
5. Exact counts found.
6. Confirmation that no runtime/code/schema/package files were modified.
7. Confirmation that all deliverables were created under `docs/architecture/`.
8. Any uncertainty or missing evidence.
9. Whether ADR-RT-002 was able to make a decisive one-frame versus multi-frame decision.

## STOP conditions

STOP and report without completing if:

1. The repository baseline is not clean.
2. `main` does not equal `origin/main`.
3. Required planning/audit source documents are missing.
4. Inventory cannot distinguish package generations.
5. PSI runtime consumption status cannot be verified.
6. Duplicate `signal_id` collision detection cannot be performed.
7. ADR-RT-002 cannot decisively choose one-frame or multi-frame.
8. Work would require editing code, schemas, packages, PSI, root-cause YAML, frontend, or control-plane files.
9. Work would require creating committed helper scripts.
10. Any deliverable would require unsupported assumptions instead of repo evidence.

## Tests / validation

Because this is documentation-only, no runtime test suite is required.

However, Cursor must validate the documentation outputs by checking:

```powershell
git diff --name-only
```

Only the approved `docs/architecture/*.md` deliverables should appear.

If read-only scripts/commands are used for counts, include command output summaries in the relevant documents.

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

* current branch matches `work/ARCH-RT-0-inventory-and-identity-decisions`
* only approved `docs/architecture/*.md` deliverables are changed
* no runtime/code/schema/package files are changed
* no tooling files are included
* no ambiguous stash exists
* latest commit contains only in-scope documentation outputs

## Success criteria

This sprint is complete only if:

1. All required inventory documents are created.
2. All required ADR documents are created.
3. Package generations are exactly counted from repo evidence.
4. PSI coverage, manifest opt-in and runtime consumption status are documented.
5. Root-cause registry and YAML inventory is documented.
6. Duplicate `signal_id` collisions are documented.
7. ALT high collision is explicitly addressed.
8. Activation compile gap is explicitly documented.
9. ADR-RT-002 decisively chooses one-frame or multi-frame.
10. Package provenance policy is defined.
11. Root-cause transition direction is defined.
12. No runtime/code/schema/package files are modified.
13. Automation Bus gate passes.

```
```
