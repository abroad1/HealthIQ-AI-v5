---
work_id: ARCH-RT-5E_psi_runtime_wiring_decision
branch: work/ARCH-RT-5E-psi-runtime-wiring-decision
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# ARCH-RT-5E — PSI Runtime Wiring Decision

## Purpose

Close the remaining PSI question for the day-one architecture.

This sprint must decide, with repo evidence, whether Promoted Signal Intelligence / PSI must be runtime-consumed for any launch-critical claim.

If PSI is not required for launch-critical output, classify it as:

```text
deferred_non_launch_blocker
````

If PSI is required, implement the narrowest safe runtime wiring using the governed identity model:

```text
activation_key
source_spec_id
signal_id family
package_id where needed
```

This sprint must not expand PSI into hypotheses, card evidence, or frontend inference.

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
ARCH-RT-5B_card_evidence_estate_and_required_provenance — merged
ARCH-RT-5C_hypothesis_runtime_promotion — merged
ARCH-RT-5D_package_provenance_backfill — merged
```

Before creating or switching to the sprint branch, run and report:

```powershell
git branch --show-current
git status --short
git log --oneline -n 14
git rev-parse HEAD
git rev-parse origin/main
```

STOP if:

* current branch is not `main`
* local `main` does not equal `origin/main`
* working tree is not clean
* ARCH-RT-5D is not merged
* untracked or uncommitted files are present

## Governance classification

```yaml
risk_level: HIGH
change_type: MIXED
execution_model: TWO_PHASE_START_FINISH
```

Reason:

This sprint may touch PSI loader/validator paths, runtime join logic, DTO-adjacent semantics, tests, launch audit artefacts, and authority manifests. If runtime wiring is required, this touches Intelligence Core output semantics and must be HIGH risk.

## Standard rules

This work remains governed by the standard Knowledge Bus and Automation Bus SOPs already active in the repository.

Do not re-read SOPs unless the applicable governance requirement cannot be located.

## Authoritative inputs

Read these sprint-specific files before making changes:

```text
docs/sprints/healthiq_day_one_architecture_rework_sprint_plan_FINAL_updated.md
docs/architecture/psi_coverage_and_manifest_opt_in_report.md
docs/architecture/psi_gap_closure_mechanics.md
docs/architecture/psi_runtime_wiring_design.md
docs/architecture/ADR-RT-001_research_to_runtime_day_one_architecture.md
docs/architecture/ADR-RT-002_signal_spec_identity_and_registry_policy.md
docs/architecture/package_provenance_policy.md
docs/audit-papers/ARCH-RT-5_M4_psi_runtime_wiring_audit.md
docs/audit-papers/ARCH-RT-5D_package_provenance_backfill_audit.md
docs/audit-papers/ARCH-RT-5D_unresolved_provenance_register.md
docs/audit-papers/active_intelligence_authority_manifest.md
docs/audit-papers/day_one_architecture_launch_readiness_audit.md
knowledge_bus/compiled/estate_index_v1.yaml
```

Also inspect, as code authority:

```text
backend/core/knowledge/load_promoted_signal_intelligence.py
knowledge_bus/schema/promoted_signal_intelligence_schema_v1.yaml
```

STOP if any required authority file is missing.

## Mandatory inherited decisions and constraints

The following are binding:

```text
PSI is signal-layer semantics only.
PSI must not contain hypothesis graphs.
PSI must not become Health Systems Card evidence authority.
PSI must not become root-cause WHY authority.
Frontend must not infer PSI semantics.
activation_key is required for runtime activation identity.
signal_id remains signal-family identity.
source_spec_id must distinguish explicit from inferred provenance.
No inferred provenance may be treated as explicit provenance.
```

Carry-forward from ARCH-RT-5:

```text
PSI runtime wiring was deferred unless mandated by launch-critical claims.
```

Carry-forward from ARCH-RT-5D:

```text
Package provenance is classified.
Unresolved/deferred provenance items remain governed by the unresolved provenance register.
```

Do not reopen these decisions.

If repo evidence contradicts any inherited decision, STOP and report.

## Main decision

This sprint must answer one question:

```text
Is PSI runtime wiring required for launch-critical claims?
```

Permitted outcomes:

### Outcome A — PSI deferred

If PSI is not required for launch-critical claims:

* do not wire PSI into runtime
* classify PSI as `deferred_non_launch_blocker`
* update launch/audit/authority documents accordingly
* ensure no current user-facing claim incorrectly depends on PSI
* create tests/audit checks only as needed

### Outcome B — narrow PSI runtime wiring

If PSI is required for launch-critical claims:

* wire PSI narrowly
* join PSI to runtime results by governed identity
* keep PSI signal-layer only
* expose semantics only through backend-controlled DTO fields
* no frontend inference
* no hypothesis/root-cause/card-evidence conflation

If the required runtime wiring is broader than a narrow identity-safe join, STOP and propose a split.

## Authority preflight

Before implementation, verify and report:

1. PSI schema path and current version.
2. PSI loader path and current behaviour.
3. PSI artefact count.
4. PSI manifest opt-in count.
5. Whether PSI is currently runtime-consumed anywhere.
6. Which launch-included outputs currently rely on PSI, if any.
7. Which launch-included card evidence artefacts rely on PSI, if any.
8. Which root-cause outputs rely on PSI, if any.
9. Whether report compiler / DTO output has PSI fields today.
10. Whether frontend renders or infers PSI semantics today.
11. Whether activation_key/source_spec_id/package_id are sufficient to join PSI safely.
12. Whether unresolved provenance items block safe PSI wiring.

If PSI runtime consumption is already present, document exact paths and STOP if that contradicts current architecture assumptions.

## Scope

Allowed scope:

1. Produce PSI runtime decision audit.
2. Update active authority manifest and launch audit with final PSI classification.
3. If deferred, add a guard/test proving PSI is not required for launch-critical output, if practical.
4. If wired, add narrowly scoped runtime loader/join integration.
5. If wired, add DTO-safe backend fields only where required.
6. If wired, add tests proving:

   * activation_key/source_spec_id join
   * no hypothesis graph use
   * no card evidence authority use
   * no frontend inference
7. Update estate index / authority manifest only as needed.
8. Preserve all prior sprint behaviours.

## Required deliverables

Create or update:

```text
docs/audit-papers/ARCH-RT-5E_psi_runtime_wiring_decision_audit.md
docs/architecture/ARCH-RT-5E_psi_runtime_wiring_decision_report.md
docs/audit-papers/active_intelligence_authority_manifest.md
docs/audit-papers/day_one_architecture_launch_readiness_audit.md
```

If PSI is deferred, these documents must clearly state why it is non-launch-blocking.

If PSI is wired, also update relevant implementation/tests and document the exact runtime join contract.

## PSI wiring requirements if implemented

If wiring is required, the runtime join must use:

```text
activation_key as primary activation-frame identity where available
source_spec_id for provenance validation
signal_id for family-level grouping only
package_id for package provenance/debugging where needed
```

PSI must remain signal-layer semantics only.

Do not expose raw PSI artefact content to frontend.

Do not allow frontend to derive marker roles, hypotheses, card labels or root-cause claims from PSI.

## Out of scope

Do not:

* add hypotheses to PSI
* use PSI as root-cause WHY authority
* use PSI as Health Systems Card evidence authority
* modify card evidence artefacts
* modify compiled hypothesis artefacts
* modify package clinical content
* modify investigation specs
* modify SignalRegistry identity policy
* modify SignalEvaluator identity behaviour
* change clinical thresholds
* change scoring rails
* change biomarker SSOT
* change unit conversion
* change frontend to infer clinical meaning
* expose raw internal source traces or PSI IDs to consumers
* introduce fallback parsers

## Required tests

If PSI is deferred:

1. Add or update audit/test coverage proving no launch-critical output requires PSI, if this can be tested without brittle assertions.
2. Confirm existing card/root-cause/report tests still pass where relevant.

If PSI is wired:

1. PSI loader tests.
2. Runtime join tests using activation_key/source_spec_id.
3. Test that PSI does not change signal firing.
4. Test that PSI does not populate hypotheses.
5. Test that PSI does not populate card evidence authority.
6. DTO serialisation tests if DTO touched.
7. Frontend render-only tests if frontend touched.
8. Regression tests for card evidence and root-cause paths.

Run narrow tests first. Run broader tests only if touched contracts require them.

## STOP conditions

STOP and report if:

1. Required authority files are missing.
2. PSI is already runtime-consumed contrary to current audit state.
3. PSI is required for launch-critical claims but safe narrow wiring cannot be implemented.
4. PSI wiring would require hypothesis/root-cause/card-evidence conflation.
5. PSI wiring would require frontend inference.
6. PSI wiring would require modifying package clinical content.
7. PSI wiring would require modifying investigation specs.
8. PSI wiring would require changing SignalRegistry or SignalEvaluator identity policy.
9. Unresolved provenance blocks safe PSI join.
10. Tests cannot prove PSI separation from hypotheses/card/root-cause.
11. Scope expands beyond PSI decision/wiring.

## Required report

Create:

```text
docs/architecture/ARCH-RT-5E_psi_runtime_wiring_decision_report.md
```

The report must include:

* decision: deferred or wired
* rationale
* launch-critical claim assessment
* PSI artefact coverage
* runtime consumption status
* identity join assessment
* implementation changes, if any
* DTO/frontend impact, if any
* tests run
* remaining risks
* final carry-forward classification

Create:

```text
docs/audit-papers/ARCH-RT-5E_psi_runtime_wiring_decision_audit.md
```

The audit must classify PSI as one of:

```text
runtime_consumed_launch_required
deferred_non_launch_blocker
launch_blocker
blocked_pending_provenance
blocked_pending_identity_join
```

No ambiguous PSI status is allowed.

## Evidence required from Cursor

Cursor must report:

1. Baseline branch/status/HEAD evidence.
2. Authority preflight findings.
3. PSI decision outcome.
4. Files changed.
5. Runtime implementation changes, if any.
6. DTO/frontend impact, if any.
7. Tests added/updated.
8. Test commands run.
9. Test results.
10. Confirmation PSI remains signal-layer only.
11. Confirmation PSI is not used for hypotheses/root-cause/card evidence.
12. Confirmation frontend does not infer PSI semantics.
13. Confirmation prior card/root-cause/provenance behaviours remain protected.
14. Confirmation no helper scripts were committed.

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

* current branch matches `work/ARCH-RT-5E-psi-runtime-wiring-decision`
* all changed files are tied to PSI decision/wiring scope
* no package/spec/card/root-cause/frontend files are changed unless explicitly justified by hardening
* no helper scripts are included
* no ambiguous stash exists
* PSI status is not ambiguous
* latest commit contains only in-scope work

## Success criteria

This sprint is complete only if:

1. PSI launch status is decisively classified.
2. If deferred, rationale is evidence-based and non-launch-blocking.
3. If wired, runtime join is identity-safe and narrow.
4. PSI remains signal-layer semantics only.
5. PSI is not used as hypothesis/root-cause/card evidence authority.
6. Frontend does not infer PSI semantics.
7. Active authority manifest and launch audit reflect final PSI status.
8. Tests/audit evidence support the decision.
9. Prior card/root-cause/provenance protections remain intact.
10. Automation Bus gate passes.

```
```
