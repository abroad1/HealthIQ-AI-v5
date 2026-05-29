---
work_id: ARCH-RT-2_identity_runtime_pilot
branch: work/ARCH-RT-2-identity-runtime-pilot
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: BEHAVIOUR
---

# ARCH-RT-2 — Identity Runtime Pilot

## Purpose

Implement the approved multi-frame runtime identity policy from `ADR-RT-002` using one controlled pilot.

This sprint addresses the live defect where multiple medically distinct packages can share the same `signal_id`, causing valid research frames to be silently collapsed by current registry behaviour.

The sprint must prove the new identity model on one governed multi-frame case before any full estate regeneration.

## Baseline requirement

Start from clean `main`.

Expected prior completed work:

```text
WAVE1-EQUIV1_total_bilirubin_false_missing_fix — merged
ARCH-RT-0_inventory_and_identity_decisions — merged
ARCH-RT-1_contracts_and_compile_foundation — merged
````

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
* ARCH-RT-1 is not merged
* untracked or uncommitted files are present

## Governance classification

```yaml
risk_level: HIGH
change_type: BEHAVIOUR
execution_model: TWO_PHASE_START_FINISH
```

Reason:

This sprint is expected to touch Intelligence Core runtime identity behaviour, likely including:

```text
SignalRegistry
SignalEvaluator
SignalResult / fired signal model
InsightGraph-facing signal result payloads
tests / persisted fixtures where required
```

HIGH-risk controls apply:

* Claude hardening required before kernel start
* Cursor implementation only after kernel start
* Claude audit after implementation
* GPT architectural review before merge
* dual approval before merge

## Mandatory inherited decisions from ARCH-RT-0

The following decisions are binding and must not be reopened:

```text
ADR-RT-002 selected MULTI_FRAME_PER_DIRECTION.
ONE_FRAME_PER_DIRECTION was rejected.
activation_key is required.
signal_id alone is not sufficient as runtime identity.
signal_id must remain the signal family identifier.
activation_key must identify the runtime activation frame.
SignalResult must carry sufficient provenance to distinguish frames.
ALT high is the preferred multi-frame pilot unless preflight proves a better/safer candidate.
```

If repository evidence contradicts any of these decisions, STOP and report.

## Mandatory inherited conditions from ARCH-RT-1 GPT review

These conditions must be carried forward into this sprint context.

They are not optional and must not be lost:

1. `compile_id` is the canonical compile identifier.
2. `compile_run_id` is transitional only.
3. If both `compile_id` and `compile_run_id` are present anywhere this sprint touches or validates, enforce or preserve the rule:

```text
compile_run_id == compile_id
```

4. The following compile manifest fields may remain optional only while the schema is DRAFT:

```text
activation_keys_emitted
collisions_detected
policy_version
```

5. Before any production compiler use, schema lock, or launch-critical compile manifest use, ADR-required manifest fields must become required.

6. The reference to `ARCH-RT-2b` should be normalised to `ARCH-RT-2` unless a formal split is later approved.

7. This sprint must not treat `compile_manifest_schema_v1.yaml` as locked or production-ready.

8. If this sprint touches compile manifest validation, compile manifest schema, or package provenance logic, it must apply the above decisions or STOP.

These carry-forward items do not expand the sprint into compile-manifest work. They are mandatory constraints if the sprint encounters or touches that area.

## Authoritative inputs

Read these files before making any changes:

```text
docs/sprints/healthiq_day_one_architecture_rework_sprint_plan_FINAL.md
docs/architecture/ADR-RT-001_research_to_runtime_day_one_architecture.md
docs/architecture/ADR-RT-002_signal_spec_identity_and_registry_policy.md
docs/architecture/ADR-RT-003_hypothesis_artefact_and_root_cause_transition.md
docs/architecture/ADR-RT-004_compile_manifest_and_package_provenance_policy.md
docs/architecture/signal_id_collision_inventory.md
docs/architecture/package_generation_inventory.md
docs/architecture/activation_compile_gap_report.md
docs/architecture/compile_manifest_contract.md
docs/architecture/package_provenance_policy.md
docs/architecture/activation_compile_contract.md
docs/architecture/ARCH-RT-1_single_frame_pilot_selection.md
docs/architecture/ARCH-RT-1_pilot_compile_provenance_evidence.md
docs/governance/KNOWLEDGE_BUS_SOP_v1.3.md
docs/governance/AUTOMATION_BUS_SOP_v1.3.1.md
```

STOP if any required file is missing.

## Authority preflight

Before editing, verify and report the actual repository paths and current behaviour for:

1. SignalRegistry implementation.
2. SignalEvaluator implementation.
3. Current duplicate `signal_id` handling logic.
4. SignalResult model.
5. InsightGraph or result payload structure that receives fired signals.
6. Root-cause compiler code path that consumes signal IDs.
7. Interaction map code path that consumes signal IDs.
8. Phenotype / IDL code path that consumes signal IDs.
9. Existing tests covering SignalRegistry / SignalEvaluator.
10. Existing persisted/golden fixtures affected by fired signal identity.
11. ALT high package paths and current lexicographic winner.
12. Whether ALT remains the safest multi-frame pilot.

If any authority path cannot be verified, STOP and report.

## Pilot scope

Preferred pilot:

```text
signal_alt_high
```

Known expected multi-frame family from ARCH-RT-0:

```text
ALT high hepatocellular frame
ALT high metabolic / steatotic frame
ALT high muscle-source / exertional frame
other ALT high duplicates identified in collision inventory
```

The pilot must focus on preventing silent collapse and proving multi-frame runtime identity.

## Scope

Allowed implementation scope:

1. Replace silent duplicate `signal_id` collapse with governed multi-frame support.
2. Introduce or wire `activation_key` as the runtime activation-frame identity, as required by ADR-RT-002.
3. Preserve `signal_id` as the signal-family identifier.
4. Update SignalRegistry so duplicate `signal_id` entries are allowed only when activation keys are distinct.
5. Prevent duplicate `activation_key` collisions.
6. Update SignalEvaluator so all valid activation frames can be evaluated.
7. Update SignalResult / fired signal output to carry required provenance.
8. Add regression coverage proving ALT high no longer silently collapses to one lexicographic winner.
9. Add tests proving duplicate `activation_key` conflicts fail closed.
10. Update downstream test expectations only where required by the new identity contract.
11. Produce a downstream impact report documenting affected or unaffected paths.

## Required runtime identity model

Unless preflight finds a contradiction and STOPs, implement the ADR-approved shape:

```text
activation_key = runtime activation-frame identity
signal_id = signal family
source_spec_id = research provenance where available
package_id = package provenance where available
```

SignalResult or equivalent fired signal payload must expose enough information for downstream systems to distinguish:

```text
which signal family fired
which frame fired
which package/spec produced the frame
```

Do not remove `signal_id`.

Do not rename existing signal families as a workaround.

## Required behaviour

After the sprint:

1. Multiple packages with the same `signal_id` must not silently overwrite each other.
2. Multiple medically distinct frames must be able to exist under one signal family.
3. ALT high pilot frames must be visible to the evaluator/registry as distinct activation frames.
4. Duplicate `activation_key` must fail closed.
5. Existing single-frame signals must continue to behave as before except for additional provenance fields.
6. Downstream systems that still consume signal family identity must be protected or explicitly documented.
7. Runtime must remain deterministic.

## Required deliverables

Create or update:

```text
docs/architecture/ARCH-RT-2_identity_runtime_pilot_report.md
```

The report must include:

* pilot selected
* package paths involved
* previous runtime behaviour
* new runtime behaviour
* activation_key format used
* SignalResult provenance fields added or confirmed
* tests added/updated
* downstream impact assessment
* remaining risks
* explicit statement that compile manifest carry-forward decisions were observed and not modified unless in scope

## Likely touched areas

Final file list must be established by preflight, but likely areas include:

```text
backend/core/analytics/**/*
backend/core/models/**/*
backend/tests/**/*
docs/architecture/ARCH-RT-2_identity_runtime_pilot_report.md
```

Do not assume these are the only files. Justify every touched file.

## Out of scope

Do not:

* Regenerate packages.
* Modify package files.
* Modify investigation specs.
* Modify PSI artefacts.
* Modify root-cause YAML.
* Modify Health Systems Card evidence.
* Create card evidence schemas.
* Create compiled hypothesis artefacts.
* Implement PSI runtime wiring.
* Implement activation compiler.
* Modify compile manifest schema unless unavoidable; if unavoidable, STOP first.
* Modify compile manifest validator unless unavoidable; if unavoidable, STOP first.
* Modify frontend.
* Modify IDL content.
* Modify biomarker SSOT.
* Modify reference ranges.
* Modify unit conversion policy.
* Modify scoring rails.
* Modify clinical thresholds.
* Introduce fallback parsers.
* Commit helper scripts.

## Tests required

At minimum:

1. Existing SignalRegistry / SignalEvaluator tests.
2. New regression test proving duplicate `signal_id` frames no longer silently collapse.
3. New regression test proving duplicate `activation_key` fails closed.
4. ALT high pilot test proving more than one valid frame can be represented/evaluated under the same `signal_id`.
5. Existing tests for single-frame signal evaluation.
6. Any root-cause / interaction / IDL tests needed if fired signal payload shape affects those paths.
7. Any persisted/golden fixture tests required by changed output structure.

Use narrow tests first.

Run broader tests only if changed contracts require them.

## STOP conditions

STOP and report without implementing if:

1. ADR-RT-002 is missing or does not clearly select `MULTI_FRAME_PER_DIRECTION`.
2. `activation_key` requirement is not clear.
3. ALT high collision no longer exists.
4. A safer pilot is required but cannot be justified from inventory.
5. Registry/evaluator changes require package regeneration.
6. Runtime identity cannot be changed without modifying package files.
7. Downstream breakage requires broad root-cause, card, frontend, or IDL changes.
8. Compile manifest schema or validator changes appear necessary.
9. Any carry-forward ARCH-RT-1 condition would be violated.
10. Deterministic ordering of evaluated frames cannot be guaranteed.
11. Test coverage cannot prove no silent collapse.
12. Scope expands into card evidence, root-cause replacement, PSI wiring, or full estate regeneration.

## Evidence required from Cursor

Cursor must report:

1. Baseline branch/status/HEAD evidence.
2. Authority preflight findings.
3. Exact current duplicate-collapse behaviour found.
4. Pilot selected and rationale.
5. Activation key format used.
6. Files changed.
7. Exact implementation changes.
8. Tests added/updated.
9. Test commands run.
10. Test results.
11. Downstream impact assessment.
12. Confirmation that package files were not modified.
13. Confirmation that PSI/root-cause/card/frontend files were not modified.
14. Confirmation that compile manifest carry-forward constraints were not violated.
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

* current branch matches `work/ARCH-RT-2-identity-runtime-pilot`
* only in-scope files are changed
* no package files are changed
* no investigation specs are changed
* no PSI artefacts are changed
* no root-cause YAML is changed
* no frontend files are changed unless explicitly approved by hardening
* no tooling files are included
* no ambiguous stash exists
* latest commit contains only in-scope work

## Success criteria

This sprint is complete only if:

1. Silent duplicate `signal_id` collapse is eliminated for the pilot.
2. Multi-frame runtime identity is implemented according to ADR-RT-002.
3. `activation_key` is present where required.
4. `signal_id` remains available as signal-family identity.
5. ALT high or approved pilot frames no longer silently overwrite each other.
6. Duplicate `activation_key` collisions fail closed.
7. Single-frame signal behaviour remains stable.
8. Downstream impact is documented.
9. Tests prove the new identity behaviour.
10. No package/spec/PSI/root-cause/card/frontend scope is included.
11. ARCH-RT-1 carry-forward conditions are preserved.
12. Automation Bus gate passes.

```
```
