---
work_id: ARCH-RT-5_full_regeneration_and_launch_gate
branch: work/ARCH-RT-5-full-regeneration-and-launch-gate
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# ARCH-RT-5 — Full Regeneration and Launch Gate

## Purpose

Scale the proven day-one architecture across the active intelligence estate and produce launch-readiness evidence.

This sprint must move HealthIQ from isolated pilots to a governed launch posture, or explicitly classify anything not ready for launch.

The target architecture remains:

```text
canonical research authority
→ deterministic compile / translation
→ governed runtime artefacts
→ runtime loaders
→ structured DTOs
→ frontend render-only
````

This sprint must not smuggle unresolved architecture risk into launch. If the full scope proves too wide, split cleanly along the milestone boundaries defined below.

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
* ARCH-RT-4 is not merged
* untracked or uncommitted files are present

## Governance classification

```yaml
risk_level: HIGH
change_type: MIXED
execution_model: TWO_PHASE_START_FINISH
```

Reason:

This sprint may touch Knowledge Bus packages, compiled artefacts, schema/validator surfaces, analytics runtime loaders, root-cause pathways, Health Systems Card evidence, DTOs, Sentinel guards, launch audit artefacts and estate manifests.

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
docs/architecture/ARCH-RT-3_card_evidence_vertical_slice_report.md
docs/architecture/ARCH-RT-4_compiled_hypothesis_root_cause_slice_report.md
docs/architecture/ARCH-RT-4_root_cause_divergence_report.md
docs/architecture/card_evidence_role_translation_policy.md
docs/architecture/card_visibility_tier_policy.md
docs/architecture/compiled_hypothesis_contract.md
docs/governance/KNOWLEDGE_BUS_SOP_v1.3.md
docs/governance/AUTOMATION_BUS_SOP_v1.3.1.md
```

STOP if any required authority file is missing.

If the updated sprint plan has a different path, locate it and report the path before proceeding.

## Mandatory inherited decisions

The following decisions are binding:

```text
ADR-008 is accepted.
PSI remains signal-layer semantics only.
Hypothesis graphs must not be placed into PSI.
Health Systems Card evidence remains separate from hypothesis/root-cause artefacts.
ADR-RT-002 selected MULTI_FRAME_PER_DIRECTION.
activation_key is required.
signal_id remains signal-family identity.
compile_id is canonical.
compile_run_id is transitional only.
If both compile_id and compile_run_id are present, they must be equal.
```

## Mandatory carry-forwards to resolve or explicitly classify

This sprint must resolve, implement, or explicitly launch-classify the following carry-forwards.

### From ARCH-RT-1

* `compile_manifest_schema_v1.yaml` was DRAFT.
* `compile_id` is canonical.
* `compile_run_id` is transitional only.
* If both are present, validator must enforce `compile_run_id == compile_id`.
* `activation_keys_emitted`, `collisions_detected`, and `policy_version` were permitted as optional only while DRAFT.
* Before production compiler use, schema lock, or launch-critical compile manifest use, ADR-required manifest fields must become required.
* Any stale `ARCH-RT-2b` reference must be normalised to `ARCH-RT-2` unless a formal split exists.

### From ARCH-RT-2

* Directory-derived `source_spec_id` is interim identity fallback only.
* Directory-derived `source_spec_id` is not canonical research provenance.
* Future provenance work must distinguish explicit `source_spec_id` from inferred `source_spec_id`.
* Root-cause compiler signal-family first-match behaviour was temporarily accepted only.
* Root-cause compiler is not fully multi-frame aware.
* Multi-frame root-cause frame selection must be explicitly governed before any multi-frame hypothesis path is promoted.

### From ARCH-RT-3

* Raw internal `source_trace` strings must not be shown directly to consumers.
* Any future consumer-facing source/evidence label must be separately designed and retail-safe.
* `compile_manifest_ref` was pilot audit string only.
* Before estate-wide regeneration, `compile_manifest_ref` must resolve to a real manifest file or governed estate index entry.
* Inferred `source_spec_ids` were acceptable for pilot only.
* Full estate compile must resolve explicit versus inferred provenance before launch-critical use.
* Remaining Wave 1 subsystems still on hard-coded evidence path must be addressed or explicitly launch-classified.

### From ARCH-RT-4

* Compiled hypotheses are currently shadow-only.
* `compile_root_cause_v1()` has not yet been wired to consume compiled hypothesis artefacts.
* ARCH-RT-5 must decide when and how compiled hypotheses begin influencing runtime `RootCauseV1` output.
* `physiological_claim` must not be treated as direct retail/runtime summary text.
* `physiological_claim` is the governed clinical reasoning claim.
* `summary_template` remains the presentation/runtime wording field unless superseded by explicit mapping policy.
* Before estate migration, define the compiled hypothesis → `RootCauseHypothesisV1` presentation mapping.
* The compiled hypothesis artefact must either carry a separate presentation-safe `summary_template` field or emit a root-cause-compatible view that preserves runtime summary semantics.
* Stronger direct cross-load / fail-closed boundary tests should be added if legacy and compiled loaders remain side-by-side.
* `compile_manifest_ref` remains pilot/manual only until real manifest linkage is implemented.
* `source_spec_provenance: source_document_derived` remains acceptable for pilot only and is not canonical explicit provenance.

If any carry-forward cannot be resolved in this sprint, it must be explicitly classified in the launch-readiness audit as:

```text
resolved
deferred_non_launch_blocker
launch_blocker
legacy_retained_with_justification
blocked_pending_spec_extraction
```

Do not leave carry-forwards ambiguous.

## Required internal milestones

This sprint must be governed by these milestones.

```text
M1 — provenance + collision-safe packages
M2 — card evidence estate
M3 — hypothesis / root-cause estate
M4 — PSI opt-in + runtime wiring
M5 — launch gate
```

Do not run the launch gate until M1–M4 are complete or explicitly classified.

## Required split criteria

Split rather than smuggle scope if any milestone becomes too large for one governed package.

Mandatory split triggers:

* kb52c / batch JSON source resolution cannot be completed or classified.
* package provenance cannot be resolved or classified.
* compile manifest schema tightening causes broad validator fallout.
* card evidence estate cannot be generated safely.
* hypothesis/root-cause estate migration requires unresolved clinical/presentation adjudication.
* PSI runtime wiring requires broader DTO/frontend/report changes than expected.
* root-cause multi-frame policy requires broader compiler redesign.
* launch audit cannot prove source → artefact → runtime → DTO → frontend traceability.

If a split is required, STOP and report the proposed split boundary.

## Scope

Allowed scope:

1. Tighten compile manifest schema and validator where required for launch-critical use.
2. Create real compile manifest files or governed estate index entries where generated artefacts require them.
3. Resolve or classify package provenance gaps.
4. Resolve or classify kb52c / batch JSON packages.
5. Regenerate or classify activation packages according to provenance policy.
6. Complete or classify PSI coverage.
7. Implement PSI runtime wiring only if required for launch-critical card/report claims.
8. Generate card evidence artefacts for launch-included Wave 1 subsystems.
9. Retire, bypass, or classify hard-coded card evidence by subsystem.
10. Generate compiled hypothesis artefacts for launch-included root-cause pathways.
11. Define and implement compiled hypothesis → runtime summary mapping where promoted.
12. Add or update root-cause registry/compiler path where explicitly governed.
13. Add fail-closed loader boundary tests.
14. Produce active authority manifest.
15. Produce launch-readiness audit.
16. Produce research-to-runtime traceability audit.
17. Add required Sentinel / regression guards where necessary for launch gate.
18. Preserve prior fixes and pilot behaviour.

## Explicit non-goals

Do not:

* change clinical thresholds
* change reference ranges
* change unit conversion policy
* change biomarker canonicalisation policy
* change scoring rails unless an explicit launch blocker proves they are structurally incompatible
* change IDL copy/content unless required for safety mapping and explicitly documented
* introduce fallback parsers
* hide unresolved provenance by treating inferred IDs as explicit
* remove legacy YAML without divergence/adjudication evidence
* expose raw internal source trace strings to consumers

## Milestone M1 — provenance + collision-safe packages

M1 must address:

* all active packages have `source_spec_id` or an explicit classification
* activation_key is present or derivable according to ADR-RT-002
* no silent `signal_id` collapse exists in active runtime
* duplicate activation_key conflicts fail closed
* kb52c / batch JSON packages are resolved or classified
* architecture-doc-sourced packages are resolved or classified
* compile_manifest_ref is real or the package is not launch-critical

Required output:

```text
docs/audit-papers/ARCH-RT-5_M1_package_provenance_and_collision_audit.md
```

## Milestone M2 — card evidence estate

M2 must address:

* each launch-included Wave 1 subsystem is either:

  * powered by compiled card evidence
  * hidden_v1
  * contextual_evidence only
  * or explicitly legacy_retained with launch justification
* hard-coded Python card evidence is not an unclassified active authority
* bilirubin / total_bilirubin fix remains protected
* raw internal source_trace is not shown directly to consumers
* compile_manifest_ref resolves or is explicitly classified

Required output:

```text
docs/audit-papers/ARCH-RT-5_M2_card_evidence_estate_audit.md
```

## Milestone M3 — hypothesis / root-cause estate

M3 must address:

* compiled hypothesis artefacts for promoted root-cause pathways
* legacy YAML retained only where explicitly justified
* divergence report for each promoted replacement or grouped evidence where safe
* compiled hypothesis → `RootCauseHypothesisV1` presentation mapping
* `physiological_claim` not used as direct retail summary text unless explicitly transformed
* root-cause multi-frame policy defined before any multi-frame hypothesis path is promoted
* shadow-only compiled hypotheses either promoted or classified

Required output:

```text
docs/audit-papers/ARCH-RT-5_M3_hypothesis_root_cause_estate_audit.md
```

## Milestone M4 — PSI opt-in + runtime wiring

M4 must address:

* PSI remains signal-layer semantics only
* PSI runtime wiring implemented only where required for launch-critical claims
* PSI not used as hypothesis graph
* PSI not used as card evidence authority directly
* runtime joins use activation_key/source_spec_id/signal family as governed
* DTO/frontend does not infer PSI semantics
* PSI gaps classified

Required output:

```text
docs/audit-papers/ARCH-RT-5_M4_psi_runtime_wiring_audit.md
```

If PSI is not required for launch-critical claims, explicitly document that and classify PSI wiring as deferred_non_launch_blocker.

## Milestone M5 — launch gate

M5 must produce:

```text
docs/audit-papers/day_one_architecture_launch_readiness_audit.md
docs/audit-papers/research_to_runtime_traceability_audit.md
docs/audit-papers/active_intelligence_authority_manifest.md
```

The launch gate must prove:

* every user-facing clinical interpretation traces to research/source authority
* compiled artefacts have manifest/provenance linkage or explicit classification
* no raw research runtime reads
* no frontend medical inference
* no duplicate unclassified active authority
* no unclassified legacy card evidence
* no unclassified legacy root-cause authority
* no unresolved silent signal collapse
* PSI either runtime-consumed where needed or classified non-launch-critical
* all carry-forwards are resolved or classified

## Likely touched areas

Final list must be established by hardening/preflight, but likely areas may include:

```text
knowledge_bus/schema/**/*
knowledge_bus/compiled/**/*
knowledge_bus/packages/**/*
backend/core/knowledge/**/*
backend/core/analytics/**/*
backend/core/models/**/*
backend/scripts/**/*
backend/tests/**/*
frontend/app/components/results/**/*
frontend/app/types/**/*
docs/audit-papers/**/*
docs/architecture/**/*
sentinel/**/*
```

Every touched file must be justified by milestone.

## Authority preflight

Before implementation, verify and report:

1. current package count and provenance status
2. current activation_key/runtime identity state
3. current compile manifest schema and validator state
4. current card evidence compiled artefacts
5. current hard-coded card evidence remaining
6. current compiled hypothesis artefacts
7. current root-cause YAML and registry state
8. current PSI artefacts and runtime usage
9. current frontend render surface for card evidence
10. current source trace display behaviour
11. current Sentinel guards relevant to this architecture
12. current test coverage for each milestone
13. exact scope required to complete each milestone

If preflight shows this sprint cannot safely cover all milestones, STOP and propose the split.

## Required tests

Run targeted tests for each touched area.

At minimum, where applicable:

* compile manifest schema/validator tests
* package provenance validation tests
* SignalRegistry / activation_key regression tests
* card evidence loader/schema/assembler/frontend tests
* bilirubin regression tests
* compiled hypothesis loader/schema/registry tests
* root-cause compiler/report tests if runtime path changes
* PSI loader/runtime wiring tests if PSI is wired
* DTO serialisation tests
* Sentinel tests if guards added
* launch audit generation tests if scripted

Do not rely only on narrow unit tests if runtime output contracts are changed.

## STOP conditions

STOP if:

1. any required authority file is missing
2. preflight shows full scope is too broad and needs split
3. package provenance cannot be resolved or classified
4. kb52c / batch JSON packages cannot be resolved or classified
5. compile manifest schema cannot be tightened without unresolved ADR conflict
6. card evidence estate cannot replace/classify hard-coded authority
7. root-cause mapping from compiled hypothesis to runtime summary cannot be governed
8. multi-frame root-cause selection remains unresolved for any promoted multi-frame path
9. PSI wiring is needed but cannot be implemented safely
10. launch audit cannot prove traceability
11. frontend would need to infer medical meaning
12. raw internal source_trace would be exposed to consumers
13. regression coverage cannot prove prior fixes are preserved
14. any carry-forward remains unclassified

## Required reports

Create/update the following:

```text
docs/audit-papers/ARCH-RT-5_M1_package_provenance_and_collision_audit.md
docs/audit-papers/ARCH-RT-5_M2_card_evidence_estate_audit.md
docs/audit-papers/ARCH-RT-5_M3_hypothesis_root_cause_estate_audit.md
docs/audit-papers/ARCH-RT-5_M4_psi_runtime_wiring_audit.md
docs/audit-papers/day_one_architecture_launch_readiness_audit.md
docs/audit-papers/research_to_runtime_traceability_audit.md
docs/audit-papers/active_intelligence_authority_manifest.md
docs/architecture/ARCH-RT-5_full_regeneration_and_launch_gate_report.md
```

If sprint splits before completion, produce:

```text
docs/architecture/ARCH-RT-5_split_recommendation.md
```

instead of incomplete launch-gate artefacts.

## Evidence required from Cursor

Cursor must report:

1. baseline branch/status/HEAD evidence
2. authority preflight findings
3. milestone-by-milestone implementation summary
4. files changed by milestone
5. tests run by milestone
6. test results
7. unresolved carry-forwards and their classification
8. launch blockers found
9. whether sprint completed or split
10. confirmation that no raw research runtime reads were introduced
11. confirmation that no frontend medical inference was introduced
12. confirmation that no internal source trace strings are exposed to consumers
13. confirmation that prior bilirubin/card/identity pilots remain protected

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

* current branch matches `work/ARCH-RT-5-full-regeneration-and-launch-gate`
* all changed files are tied to a milestone
* no ambiguous stash exists
* no helper scripts are committed unless explicitly in scope
* no unresolved carry-forward is left unclassified
* latest commit contains only in-scope work

## Success criteria

This sprint is complete only if:

1. M1 package provenance and collision-safe package evidence is complete.
2. M2 card evidence estate evidence is complete.
3. M3 hypothesis/root-cause estate evidence is complete.
4. M4 PSI wiring/classification evidence is complete.
5. M5 launch-readiness audit is complete.
6. all carry-forwards are resolved or explicitly classified.
7. no duplicate unclassified active authority remains.
8. no raw research runtime reads exist.
9. no frontend medical inference exists.
10. no unresolved signal collapse exists.
11. compile manifests/provenance are real or non-launch-critical exceptions are classified.
12. prior WAVE1-EQUIV1, ARCH-RT-2, ARCH-RT-3 and ARCH-RT-4 protections remain intact.
13. Automation Bus gate passes.

```
```
