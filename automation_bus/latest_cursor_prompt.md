---
work_id: ARCH-RT-1_contracts_and_compile_foundation
branch: work/ARCH-RT-1-contracts-and-compile-foundation
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# ARCH-RT-1 — Contracts and Compile Foundation

## Purpose

Create the minimum governance contracts and compile/provenance foundation needed for the HealthIQ day-one research-to-runtime architecture.

This sprint follows the completed and merged `ARCH-RT-0_inventory_and_identity_decisions` sprint.

It must use the ARCH-RT-0 inventory and ADR outputs as authority.

This sprint must not perform runtime wiring.

## Baseline requirement

Start from clean `main`.

Before creating or switching to the sprint branch, run and report:

```powershell
git branch --show-current
git status --short
git log --oneline -n 8
git rev-parse HEAD
git rev-parse origin/main
````

STOP if:

* current branch is not `main`
* local `main` does not equal `origin/main`
* working tree is not clean
* ARCH-RT-0 is not merged
* untracked or uncommitted files are present

## Governance classification

```yaml
risk_level: HIGH
change_type: MIXED
execution_model: TWO_PHASE_START_FINISH
```

Reason:

This sprint may introduce or update governed Knowledge Bus schema / contract artefacts and compile-provenance foundations that downstream Intelligence Core work will rely on.

It must be treated as HIGH risk even though runtime behaviour must not change in this sprint.

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
docs/governance/KNOWLEDGE_BUS_SOP_v1.3.md
docs/governance/AUTOMATION_BUS_SOP_v1.3.1.md
```

STOP if any file is missing.

## Critical decisions inherited from ARCH-RT-0

The following decisions are binding for this sprint:

```text
ADR-RT-002 selected MULTI_FRAME_PER_DIRECTION.
activation_key is required.
signal_id alone is not sufficient as runtime identity.
source_spec_id is absent from current active packages.
PSI exists but is runtime-dead.
PSI is signal-layer semantics only.
PSI must not be expanded to contain full hypothesis graphs.
Activation compile is distinct from PSI compile.
No governed investigation_spec → signal_library / research_brief / package_manifest compiler currently exists for the full estate.
```

Do not reopen these decisions.

If repository evidence contradicts any of these decisions, STOP and report the contradiction.

## Authority preflight

Before editing, verify and report:

1. Existing Knowledge Bus schema directory.
2. Existing package manifest schema location and current required fields.
3. Existing signal library schema location and current version/shape.
4. Existing research brief schema location and current required fields.
5. Existing promoted signal intelligence schema location.
6. Existing PSI translator path.
7. Existing PSI validator path.
8. Existing investigation spec validator path.
9. Existing package validator path.
10. Whether any compile manifest schema already exists.
11. Whether any activation compile contract already exists.
12. Whether any package provenance policy already exists outside ADR-RT-004.
13. Whether any script currently claims to compile `investigation_spec` into:

    * `signal_library.yaml`
    * `research_brief.yaml`
    * `package_manifest.yaml`

This preflight is mandatory.

If any existing authority already covers a proposed deliverable, extend or reference that authority rather than creating a duplicate.

## Scope

This sprint creates the contract foundation for later compile work.

Allowed scope:

1. Create compile manifest schema.
2. Create or update architecture documentation for compile manifest contract.
3. Create or update package provenance policy documentation.
4. Create activation compile contract documentation.
5. Create PSI gap closure mechanics documentation.
6. Create PSI runtime wiring design documentation only.
7. Create pilot compile/provenance evidence documentation using one inventory-selected single-frame candidate.
8. Add narrowly scoped schema tests or validation tests only if required to prove new schemas parse/validate.
9. Add narrowly scoped validator support only if necessary to validate the new compile manifest schema, provided this is explicitly justified and does not touch runtime behaviour.

## Required deliverables

Create or update the following deliverables:

```text
knowledge_bus/schema/compile_manifest_schema_v1.yaml
docs/architecture/compile_manifest_contract.md
docs/architecture/package_provenance_policy.md
docs/architecture/activation_compile_contract.md
docs/architecture/psi_gap_closure_mechanics.md
docs/architecture/psi_runtime_wiring_design.md
docs/architecture/ARCH-RT-1_single_frame_pilot_selection.md
docs/architecture/ARCH-RT-1_pilot_compile_provenance_evidence.md
```

If adding tests or validator support, justify them explicitly in the implementation summary.

No other deliverables are allowed without STOP and approval.

## Deliverable requirements

### 1. `knowledge_bus/schema/compile_manifest_schema_v1.yaml`

Must define a schema for compile manifests covering at minimum:

```yaml
compile_id:
compiler_name:
compiler_version:
compile_mode:
source_contract_version:
source_specs:
  - source_spec_id:
    source_path:
    source_hash:
    source_hash_algorithm:
outputs:
  - output_type:
    output_path:
    output_hash:
    output_hash_algorithm:
    package_id:
    signal_id:
    activation_key:
    source_spec_id:
translation_rules_version:
remap_contract_version:
compiled_at_utc:
compiled_by:
validator_results:
provenance_status:
```

Must support the day-one identity model:

```text
activation_key required for activation artefacts
signal_id retained as signal family
source_spec_id required for research-derived artefacts
legacy_retained classification permitted only when explicitly justified
```

Must not introduce runtime logic.

### 2. `docs/architecture/compile_manifest_contract.md`

Must explain:

* manifest purpose
* per-run versus per-artefact versus estate-index approach
* where manifests should be stored
* required fields
* hash rules
* deterministic ordering expectations
* how manifests support package promotion
* how manifests support later launch-readiness audit
* how manifests relate to `latest_knowledge_status.json`
* how manifests relate to legacy-retained artefacts

Must align with ADR-RT-004.

### 3. `docs/architecture/package_provenance_policy.md`

Must define:

* `source_spec_id` requirement for new generated packages
* `activation_key` requirement for new generated activation artefacts
* handling of existing packages with no `source_spec_id`
* permitted classifications:

  * `active_current`
  * `legacy_retained`
  * `deferred_for_regeneration`
  * `blocked_pending_spec_extraction`
  * `retire_candidate`
  * `unknown_requires_review`
* rules for batch JSON source packages
* rules for architecture-doc-sourced packages
* rules for packages with PSI
* rules for packages without PSI
* how provenance must be validated before launch

### 4. `docs/architecture/activation_compile_contract.md`

Must define the target governed activation compile path:

```text
investigation_spec
→ signal_library.yaml
→ research_brief.yaml
→ package_manifest.yaml
```

Must explicitly distinguish this from PSI:

```text
investigation_spec → promoted_signal_intelligence
```

Must define expected output responsibilities:

| Output                              | Responsibility                                                               |
| ----------------------------------- | ---------------------------------------------------------------------------- |
| `signal_library.yaml`               | activation / firing / thresholds / dependencies / overrides / activation_key |
| `research_brief.yaml`               | evidence traceability / biomarker context                                    |
| `package_manifest.yaml`             | package identity / source_spec_id / compile manifest reference / PSI opt-in  |
| `promoted_signal_intelligence.yaml` | signal-layer semantics only                                                  |

Must state that no activation compiler currently exists for full estate regeneration unless implementation discovers otherwise.

Must define what a future activation compiler must prove:

* deterministic output
* source hash preservation
* source_spec_id propagation
* activation_key propagation
* no silent signal_id collapse
* package validator compatibility
* no PSI/hypothesis/card evidence conflation

### 5. `docs/architecture/psi_gap_closure_mechanics.md`

Must define:

* current PSI coverage state from ARCH-RT-0
* what PSI already does
* what PSI does not do
* why PSI is not the activation compiler
* how PSI opt-in should be validated
* how PSI coverage gaps should be classified
* how PSI should join later runtime outputs
* how PSI remains separate from hypothesis artefacts and card evidence artefacts

### 6. `docs/architecture/psi_runtime_wiring_design.md`

Design only.

Must define:

* where PSI could be loaded in the future
* whether PSI should be package-scoped or estate-indexed
* how PSI should join to runtime fired results using:

  * activation_key
  * source_spec_id
  * signal_id family
  * package_id where needed
* which future sprint should implement PSI runtime wiring
* what must not happen:

  * no raw research runtime reads
  * no PSI expansion into hypothesis graph
  * no frontend PSI inference
  * no runtime wiring in this sprint

### 7. `docs/architecture/ARCH-RT-1_single_frame_pilot_selection.md`

Must select one pilot candidate for this sprint’s compile/provenance evidence.

Candidate must be selected from ARCH-RT-0 inventory evidence.

Preferred candidate characteristics:

```text
single-frame
valid investigation spec
no duplicate signal_id collision
existing or expected package relationship
PSI missing or manifest opt-in gap useful to test
activation package relationship is clear
low runtime blast radius
```

The document must justify the selected candidate and explicitly reject unsuitable candidates such as ALT, CRP, or homocysteine if they remain unsuitable.

If no safe candidate exists, STOP and report.

### 8. `docs/architecture/ARCH-RT-1_pilot_compile_provenance_evidence.md`

This sprint must not implement a full compiler.

This document should provide pilot evidence using existing translators/scripts where available and read-only/manual evidence where implementation is not yet available.

Must include:

* selected source spec
* related package, if any
* current manifest provenance
* whether PSI exists
* whether activation package exists
* whether source_spec_id exists
* whether activation_key exists
* whether compile manifest could represent the required provenance
* what exact future implementation gap remains
* whether the PSI translator output is deterministic if run
* whether activation compile is currently manual/scripted/missing

If running existing translator or validator commands, report command and output summary.

Do not create committed generated runtime artefacts unless explicitly in scope and validated.

## Out of scope

Do not:

* modify runtime analytics code
* modify SignalRegistry
* modify SignalEvaluator
* modify SignalResult model
* modify InsightGraph runtime contracts
* modify package files
* modify existing package manifests
* modify investigation specs
* modify PSI artefacts
* modify root-cause YAML
* modify root_cause_registry
* modify Health Systems Card runtime assembler
* modify frontend
* modify IDL content
* wire PSI into runtime
* create full activation compiler implementation
* regenerate packages
* create card evidence artefacts
* create compiled hypothesis artefacts
* change biomarker canonicalisation
* change scoring logic
* introduce fallback parsers
* commit local helper scripts

## Existing translator / validator commands

Cursor may run existing validation/translation commands only if they are read-only or write to a temporary location that is removed before closure.

If a command writes generated artefacts into governed directories, STOP unless the output path is explicitly in the allowed deliverables.

If temporary output is needed, use a clearly temporary path and delete it before closure.

## Required tests / validation

At minimum:

1. Validate YAML syntax for the new schema/docs where applicable.
2. If a schema validation test pattern exists, add or run the narrowest relevant test.
3. If no test exists, document validation method in implementation summary.
4. Run any existing compile manifest / schema validation tests if present.
5. If the existing PSI translator is run for pilot evidence, run it at least twice and confirm deterministic output, or document why this cannot be done safely.

Do not run broad test suites unless required by touched files.

## STOP conditions

STOP and report if:

1. ARCH-RT-0 deliverables are missing.
2. ADR-RT-002 does not decisively select `MULTI_FRAME_PER_DIRECTION`.
3. `activation_key` requirement is not confirmed in ADR-RT-002.
4. Existing repository already contains a compile manifest schema that would be duplicated.
5. Existing repository already contains an activation compile contract that would be duplicated.
6. A safe single-frame pilot cannot be selected.
7. Pilot evidence would require runtime wiring.
8. Pilot evidence would require modifying package files or generated artefacts outside allowed deliverables.
9. PSI translator is non-deterministic.
10. Activation compile cannot be described separately from PSI.
11. Any runtime/code/package/frontend/root-cause changes appear necessary.
12. Any helper scripts would need to be committed.
13. Scope expands into ARCH-RT-2 identity runtime pilot, ARCH-RT-3 card evidence, or ARCH-RT-4 root-cause work.

## Evidence required from Cursor

Cursor must report:

1. Baseline branch/status/HEAD evidence.
2. Authority preflight findings.
3. Existing schema/validator/translator paths found.
4. Whether compile manifest schema already existed.
5. Whether activation compile contract already existed.
6. Files changed.
7. Pilot candidate selected and rationale.
8. Commands run.
9. Validation/test results.
10. Confirmation that no runtime wiring occurred.
11. Confirmation that no package/investigation spec/PSI/root-cause YAML files were modified.
12. Confirmation that no helper scripts were committed.
13. Confirmation that activation compile and PSI compile are treated separately.

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

* current branch matches `work/ARCH-RT-1-contracts-and-compile-foundation`
* only approved files are changed
* no runtime/code/package/frontend/root-cause files are changed
* no tooling files are included
* no ambiguous stash exists
* latest commit contains only in-scope contract/foundation work

## Success criteria

This sprint is complete only if:

1. Compile manifest schema exists and aligns with ADR-RT-004.
2. Compile manifest contract documentation exists.
3. Package provenance policy exists.
4. Activation compile contract exists.
5. PSI gap closure mechanics document exists.
6. PSI runtime wiring design exists as design-only.
7. Single-frame pilot selection is evidence-based.
8. Pilot compile/provenance evidence is documented.
9. Activation compile and PSI compile are explicitly separated.
10. No runtime wiring occurs.
11. No package files are modified.
12. No investigation specs are modified.
13. No PSI artefacts are modified.
14. No root-cause YAML is modified.
15. No frontend is modified.
16. No helper scripts are committed.
17. Automation Bus gate passes.

```
```
