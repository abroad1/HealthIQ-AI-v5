---
work_id: ARCH-RT-4_compiled_hypothesis_root_cause_slice
branch: work/ARCH-RT-4-compiled-hypothesis-root-cause-slice
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# ARCH-RT-4 — Compiled Hypothesis / Root-Cause Slice

## Purpose

Create the first governed compiled hypothesis artefact and prove how HealthIQ will transition away from hand-authored root-cause YAML as a permanent WHY authority.

This sprint must prove one controlled pilot path:

```text
investigation-spec hypothesis intelligence
→ compiled hypothesis artefact
→ validation
→ divergence comparison against existing root-cause YAML
→ shadow/pilot root-cause registry loading
````

This sprint must not perform full root-cause estate migration.

## Baseline requirement

Start from clean `main`.

Expected prior completed work:

```text
WAVE1-EQUIV1_total_bilirubin_false_missing_fix — merged
ARCH-RT-0_inventory_and_identity_decisions — merged
ARCH-RT-1_contracts_and_compile_foundation — merged
ARCH-RT-2_identity_runtime_pilot — merged
ARCH-RT-3_card_evidence_vertical_slice — merged
```

Before creating or switching to the sprint branch, run and report:

```powershell
git branch --show-current
git status --short
git log --oneline -n 10
git rev-parse HEAD
git rev-parse origin/main
```

STOP if:

* current branch is not `main`
* local `main` does not equal `origin/main`
* working tree is not clean
* ARCH-RT-3 is not merged
* untracked or uncommitted files are present

## Governance classification

```yaml
risk_level: HIGH
change_type: MIXED
execution_model: TWO_PHASE_START_FINISH
```

Reason:

This sprint introduces governed hypothesis/root-cause artefact structures and may touch root-cause registry/loading paths. It affects the WHY interpretation layer and is downstream of Intelligence Core signal identity changes.

HIGH-risk controls apply:

* Claude hardening required before kernel start
* Cursor implementation only after kernel start
* Claude audit after implementation
* GPT architectural review before merge
* dual approval before merge

## Authoritative inputs

Read these files before making any changes:

```text
docs/sprints/healthiq_day_one_architecture_rework_sprint_plan_FINAL_updated.md
docs/architecture/ADR-RT-001_research_to_runtime_day_one_architecture.md
docs/architecture/ADR-RT-002_signal_spec_identity_and_registry_policy.md
docs/architecture/ADR-RT-003_hypothesis_artefact_and_root_cause_transition.md
docs/architecture/ADR-RT-004_compile_manifest_and_package_provenance_policy.md
docs/architecture/research_to_runtime_traceability_matrix.md
docs/architecture/intelligence_authority_inventory.md
docs/architecture/root_cause_registry_inventory.md
docs/architecture/signal_id_collision_inventory.md
docs/architecture/package_generation_inventory.md
docs/architecture/activation_compile_gap_report.md
docs/architecture/compile_manifest_contract.md
docs/architecture/package_provenance_policy.md
docs/architecture/activation_compile_contract.md
docs/architecture/psi_gap_closure_mechanics.md
docs/architecture/psi_runtime_wiring_design.md
docs/architecture/ARCH-RT-2_identity_runtime_pilot_report.md
docs/architecture/ARCH-RT-3_card_evidence_vertical_slice_report.md
docs/architecture/card_evidence_role_translation_policy.md
docs/architecture/card_visibility_tier_policy.md
docs/governance/KNOWLEDGE_BUS_SOP_v1.3.md
docs/governance/AUTOMATION_BUS_SOP_v1.3.1.md
```

If the updated sprint plan has a different filename/path, locate and report it before proceeding.

STOP if any required authority file is missing.

## Mandatory inherited decisions and carry-forwards

The following are binding:

```text
ADR-008 is accepted.
PSI remains signal-layer semantics only.
Hypothesis graphs must not be placed into PSI.
Health Systems Card evidence remains separate from hypothesis/root-cause artefacts.
ADR-RT-002 selected MULTI_FRAME_PER_DIRECTION.
activation_key is required.
signal_id remains signal-family identity.
Root-cause compiler is not yet multi-frame aware.
```

Carry-forward from ARCH-RT-1:

```text
compile_id is canonical.
compile_run_id is transitional only.
If both compile_id and compile_run_id are present, they must be equal.
compile_manifest_schema_v1 remains DRAFT unless explicitly tightened.
```

Carry-forward from ARCH-RT-2:

```text
Directory-derived source_spec_id is interim identity fallback only.
Directory-derived source_spec_id is not canonical research provenance.
Future provenance work must distinguish explicit source_spec_id from inferred source_spec_id.
Root-cause compiler signal_id-only first-match behaviour is acceptable temporarily only.
This sprint must explicitly assess and constrain that first-match behaviour.
```

Carry-forward from ARCH-RT-3:

```text
Raw internal source_trace strings must not be shown directly to consumers.
compile_manifest_ref may still be pilot/manual only unless this sprint explicitly creates a real manifest.
Inferred source_spec_ids are acceptable for pilot only.
Full estate compile must resolve explicit versus inferred provenance before launch-critical use.
```

Do not reopen these decisions.

If repository evidence contradicts any inherited decision, STOP and report.

## Authority preflight

Before editing, verify and report the actual repository paths and current behaviour for:

1. root-cause hypothesis YAML directory.
2. root_cause_registry implementation.
3. root-cause hypothesis loader(s).
4. root_cause_compiler implementation.
5. confirmatory test registry / loader.
6. current root-cause DTO/result model.
7. current report compiler path that consumes root-cause output.
8. current SignalResult fields after ARCH-RT-2.
9. existing tests for root-cause registry/loading/compiler.
10. existing tests for confirmatory test mapping.
11. existing investigation spec source for the selected pilot.
12. existing root-cause YAML for the selected pilot.
13. whether selected pilot has explicit source_spec_id or only inferred/source_document provenance.
14. whether selected pilot is affected by multi-frame signal identity.

If any authority path cannot be verified, STOP and report.

## Pilot selection

Select exactly one pilot hypothesis/root-cause pathway.

Preferred candidate characteristics:

```text
single or manageable signal family
existing investigation spec hypothesis content
existing root-cause YAML to compare against
registered in root_cause_registry today
low downstream blast radius
confirmatory tests either absent or mappable to registry
no unresolved multi-frame ambiguity unless explicitly selected for that reason
```

Do not select a pilot that requires broad root-cause compiler redesign.

Candidate should be selected from ARCH-RT-0 inventory and justified.

If the selected pilot is multi-frame, the report must explain why that is safe and how frame selection is governed.

STOP if no safe pilot exists.

## Mandatory internal checkpoint

This sprint has a hard internal checkpoint.

Before adding or changing any root-cause registry/runtime loader behaviour:

```text
The compiled hypothesis schema and pilot artefact must validate.
The divergence comparison against existing root-cause YAML must be produced.
```

If the schema or pilot artefact cannot validate, STOP.

If divergence is clinically/materially unresolved, STOP before runtime/registry wiring.

## Scope

Allowed implementation scope:

1. Define compiled hypothesis schema.
2. Define compiled hypothesis contract documentation.
3. Create one pilot compiled hypothesis artefact.
4. Validate the pilot artefact.
5. Map confirmatory tests to registry IDs where applicable.
6. Compare the compiled artefact against existing root-cause YAML.
7. Produce a divergence report.
8. Add a compiled hypothesis loader only if the artefact validates.
9. Add a root_cause_registry pilot/shadow pathway only for the selected pilot.
10. Preserve existing hand-authored YAML for comparison.
11. Add targeted tests.
12. Document remaining risks and carry-forwards.

## Required deliverables

Create or update:

```text
knowledge_bus/schema/compiled_hypothesis_schema_v1.yaml
docs/architecture/compiled_hypothesis_contract.md
knowledge_bus/compiled/hypotheses/<pilot>.yaml
docs/architecture/ARCH-RT-4_root_cause_divergence_report.md
docs/architecture/ARCH-RT-4_compiled_hypothesis_root_cause_slice_report.md
```

Implementation files may be added/updated only as required for:

```text
compiled hypothesis validation
compiled hypothesis loading
pilot root_cause_registry shadow path
targeted tests
```

## Compiled hypothesis schema requirements

The schema must support at minimum:

```yaml
schema_version:
artefact_id:
hypothesis_set_id:
signal_id:
activation_key:
source_spec_ids:
source_spec_provenance:
compile_manifest_ref:
hypotheses:
  - hypothesis_id:
    rank:
    title:
    physiological_claim:
    evidence_strength:
    evidence_for:
    evidence_against:
    contradiction_markers:
    missing_data_policy:
    caveats:
    confirmatory_tests:
provenance:
```

The schema must distinguish:

```text
explicit source_spec_id
source_document-derived source_spec_id
package-id-inferred source_spec_id
manual pilot provenance
```

If the pilot cannot populate a field explicitly, the field may be optional only if the schema and contract document explain why.

## Compiled hypothesis contract requirements

`docs/architecture/compiled_hypothesis_contract.md` must define:

* artefact purpose
* relationship to investigation specs
* relationship to PSI
* relationship to existing root-cause YAML
* relationship to root_cause_registry
* relationship to confirmatory test registry
* relationship to multi-frame signal identity
* how activation_key is used or not used
* how signal_id family identity is retained
* how divergence against existing root-cause YAML is handled
* what must be resolved before estate-wide migration

## Divergence report requirements

`docs/architecture/ARCH-RT-4_root_cause_divergence_report.md` must compare pilot compiled hypothesis artefact against current root-cause YAML.

Must include:

* matching hypothesis IDs or title equivalents
* claims present in both
* claims present only in investigation spec / compiled artefact
* claims present only in root-cause YAML
* evidence_for / evidence_against differences
* missing-data handling differences
* confirmatory test differences
* contradiction marker differences
* retail wording / summary_template differences
* whether divergence blocks runtime pilot
* recommendation:

  * acceptable
  * acceptable with carry-forward
  * blocks runtime pilot
  * requires clinical adjudication

Do not hide divergence.

## Root-cause registry pilot requirements

If implementation proceeds past the validation/divergence checkpoint:

* add compiled hypothesis loading in shadow/pilot mode only
* preserve existing YAML loader
* do not remove existing manual registry entries
* do not switch the full root-cause estate
* do not claim root-cause compiler is fully multi-frame aware
* if root-cause compiler still matches by signal_id family only, document that explicitly
* if selected pilot has multiple activation_key frames, do not silently select one without explicit policy

## Out of scope

Do not:

* migrate full root-cause estate
* delete or rewrite existing root-cause YAML
* modify PSI artefacts
* modify package files
* modify investigation specs
* modify SignalRegistry
* modify SignalEvaluator
* modify Health Systems Card evidence
* modify frontend
* modify IDL copy/content
* modify biomarker SSOT
* modify scoring logic
* modify unit conversion
* modify clinical thresholds
* perform full compile-manifest production locking
* create activation compiler
* wire PSI into runtime
* introduce fallback parsers
* commit helper scripts

## Tests required

At minimum, add or update tests covering:

1. compiled hypothesis schema validation.
2. pilot artefact validation.
3. loader success path.
4. loader fail-closed behaviour for invalid artefact.
5. confirmatory test registry mapping, if pilot uses confirmatory tests.
6. divergence comparison logic, if implemented as code.
7. pilot registry/shadow loading path, if implemented.
8. existing root-cause YAML path remains available.
9. no full root-cause estate switch occurs.
10. multi-frame ambiguity is handled or explicitly blocked.

Run narrow tests first. Run broader root-cause/report tests only if touched contracts require them.

## STOP conditions

STOP and report without implementing further if:

1. Required authority files are missing.
2. No safe pilot can be selected.
3. Compiled hypothesis schema cannot represent necessary WHY content.
4. Pilot artefact cannot validate.
5. Confirmatory test IDs cannot map to registry where required.
6. Divergence with existing root-cause YAML is material and unresolved.
7. Runtime/registry pilot would silently select one frame from multiple activation_keys.
8. Root-cause compiler changes would require broad report/IDL/frontend changes.
9. Work would require modifying package files or investigation specs.
10. Work would require modifying SignalRegistry or SignalEvaluator.
11. Work would require changing PSI.
12. Work would require changing Health Systems Card evidence.
13. Scope expands beyond one pilot pathway.
14. Compile manifest carry-forward conditions would be violated.
15. Tests cannot prove legacy YAML remains available.

## Required report

Create:

```text
docs/architecture/ARCH-RT-4_compiled_hypothesis_root_cause_slice_report.md
```

The report must include:

* pilot selected and rationale
* alternatives rejected
* schema created
* artefact path
* validation result
* divergence report summary
* loader path, if added
* registry/shadow path, if added
* tests added/updated
* test commands and results
* confirmation that legacy YAML remains available
* confirmation that full root-cause estate was not migrated
* confirmation that SignalRegistry/SignalEvaluator were not modified
* confirmation that PSI/card/frontend files were not modified
* remaining risks and carry-forwards

## Evidence required from Cursor

Cursor must report:

1. Baseline branch/status/HEAD evidence.
2. Authority preflight findings.
3. Pilot selected and rationale.
4. Files changed.
5. Internal checkpoint result proving artefact validation and divergence review before runtime/registry work.
6. Exact implementation changes.
7. Confirmatory test mapping outcome.
8. Tests added/updated.
9. Test commands run.
10. Test results.
11. Confirmation that only one pilot pathway was included.
12. Confirmation that existing YAML remains available.
13. Confirmation that no package/spec/PSI/card/frontend/SignalRegistry/SignalEvaluator work was included.
14. Confirmation that root-cause compiler multi-frame limitation is documented.
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

* current branch matches `work/ARCH-RT-4-compiled-hypothesis-root-cause-slice`
* only in-scope files are changed
* no package files are changed
* no investigation specs are changed
* no PSI artefacts are changed
* no Health Systems Card evidence files are changed
* no SignalRegistry / SignalEvaluator files are changed
* no frontend files are changed
* no helper scripts are included
* no ambiguous stash exists
* latest commit contains only in-scope work

## Success criteria

This sprint is complete only if:

1. One pilot compiled hypothesis artefact exists and validates.
2. Compiled hypothesis schema exists and validates.
3. Compiled hypothesis contract exists.
4. Divergence report exists.
5. Existing root-cause YAML remains available.
6. Any registry/root-cause loading is pilot/shadow only.
7. No full root-cause estate migration occurs.
8. Confirmatory tests are mapped or explicitly documented as not applicable.
9. Root-cause compiler multi-frame limitation is explicitly documented.
10. No SignalRegistry / SignalEvaluator work is included.
11. No PSI/card/frontend work is included.
12. Tests prove the pilot path and legacy preservation boundaries.
13. Automation Bus gate passes.

```
```
