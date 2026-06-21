---
work_id: P1-17
branch: sprint/P1-17-remaining-psi-blocker-resolution
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# P1-17 — Remaining PSI Blocker Resolution Pack with Agent-Boundary STOP Gates

You are Cursor, acting as the Medical Intelligence / Knowledge Bus implementation agent.

Implement this work package under Automation Bus SOP v1.3.1.

This is one outcome-based package with internal STOP gates. Do not split package-identity adjudication, derived-marker adjudication, blocker classification, and safe opt-in into separate work packages unless a STOP gate fires.

## Purpose

Resolve the remaining non-medical-review PSI blocker cohort where this can be done safely within Medical Intelligence / Knowledge Bus authority.

This sprint covers:

1. The 4 `BLOCKED_PACKAGE_IDENTITY_UNRESOLVED` candidates carried forward from P1-16.
2. The 7 transferrin-saturation / derived-marker blocked candidates carried forward from P1-14/P1-16.
3. Same-sprint production PSI opt-in for any candidate safely resolved without crossing agent boundaries.

This sprint must not become report-only unless all candidates hit STOP gates.

## Agent boundary

This sprint is assigned to the Medical Intelligence / Knowledge Bus agent.

You may edit:

* Knowledge Bus package manifests
* Knowledge Bus production PSI artefacts
* Knowledge Bus sprint documentation
* beta-readiness deliverable register
* blocker/adjudication manifests

You may read, but must not edit:

* backend/ssot/
* backend/core/
* backend/scripts/
* backend/tests/
* frontend/
* DTO/report/orchestrator/scoring/Gemini files
* parser/runtime/derived-metric implementation files

If a candidate requires edits to backend logic, parser logic, derived-marker calculation, SSOT canonicalisation, validators, runtime loaders, tests, DTOs, frontend, scoring, report compilation, Gemini, or orchestration, classify it as:

`BLOCKED_REQUIRES_CORE_BACKEND_AGENT`

Do not implement core backend work in this sprint.

## Current baseline

P1-15 completed 18 clean production PSI opt-ins.

P1-16 completed 4 additional production PSI opt-ins and left:

* 4 package-identity unresolved candidates:

  * `pkg_kb52c_rbc_high_erythrocytosis_pattern`
  * `pkg_kb52c_rbc_low_iron_restricted_anemia_pattern`
  * `pkg_kb52c_rdw_cv_high_iron_deficiency_anisocytosis`
  * `pkg_kb52c_rdw_cv_high_mixed_red_cell_population_pattern`

* 7 derived-marker / transferrin-saturation candidates still blocked.

Medical-review blocked candidates remain out of scope.

## Mandatory files to read before editing

Read:

* docs/sprints/beta_readiness/P1-16_identity_adjudication_manifest.yaml
* docs/sprints/beta_readiness/P1-16_psi_identity_blocker_remediation.md
* docs/sprints/beta_readiness/P1-15_production_psi_opt_in_mapping.yaml
* docs/sprints/beta_readiness/P1-14_activation_readiness_cohort_manifest.yaml
* docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md
* docs/governance/KNOWLEDGE_BUS_SOP_v1.3.1.md
* docs/governance/KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL_v1.1.md
* knowledge_bus/schema/package_manifest_schema.yaml
* knowledge_bus/schema/promoted_signal_intelligence_schema_v1.yaml
* backend/scripts/validate_knowledge_package.py
* backend/scripts/validate_promoted_signal_intelligence.py
* backend/scripts/validate_staged_psi_activation_readiness.py

You may inspect backend/SSOT/runtime files only to understand authority and blocker boundaries. Do not edit them.

Use targeted search:

* `rg "transferrin_saturation" knowledge_bus backend docs`
* `rg "pkg_kb52c_rbc|pkg_kb52c_rdw_cv|pkg_kb58_rbc|pkg_kb58_rdw_cv" knowledge_bus docs`
* `rg "BLOCKED_PACKAGE_IDENTITY_UNRESOLVED|BLOCKED_REQUIRES_DERIVED_MARKER_POLICY|derived" docs/sprints/beta_readiness`
* `rg "promoted_signal_intelligence" knowledge_bus backend docs`
* `rg "source_spec_id" knowledge_bus docs backend`

Inspect relevant hits before editing.

## Files in scope

Permitted, if justified:

* docs/sprints/beta_readiness/P1-17_remaining_psi_blocker_resolution.md
* docs/sprints/beta_readiness/P1-17_blocker_resolution_manifest.yaml
* docs/sprints/beta_readiness/P1-17_core_backend_handoff_manifest.yaml
* docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md
* knowledge_bus/packages/<resolved_package>/package_manifest.yaml
* knowledge_bus/packages/<resolved_package>/promoted_signal_intelligence.yaml

## Files out of scope

Do not modify:

* backend/ssot/
* backend/core/
* backend/scripts/
* backend/tests/
* frontend/
* knowledge_bus/research/
* knowledge_bus/generated_pilot/**/*
* DTO/report compiler/orchestrator files
* scoring files
* Gemini files
* parser files
* runtime loader files
* validator files
* automation_bus/latest_gate_evidence.json
* automation_bus/latest_gate_output.txt

Do not allow tooling files into the sprint branch:

* .codex/
* .cursor/
* .vscode/
* AGENTS.md

## Critical prohibitions

Do not:

* implement derived-marker calculation logic
* edit backend validators
* edit backend SSOT files
* edit runtime loaders
* edit parser behaviour
* edit tests to make validation pass
* create fallback or dummy parsers
* cross-place PSI into a package whose manifest `package_id` differs from the PSI internal `package_id`
* hand-edit medical content to force validation
* alter thresholds, activation logic, evidence strength, interpretation text, or medical meaning
* promote medical-review blocked PSI
* introduce runtime/user-facing activation
* create duplicate active medical authority

## Phase 0 — Automation Bus preflight

Before implementation:

1. Confirm current branch is:

`sprint/P1-17-remaining-psi-blocker-resolution`

2. Confirm `automation_bus/state/work_package_active.json` exists.
3. Confirm active token has `work_id: P1-17`.
4. Confirm token branch matches current branch.
5. Confirm working tree and stash state are governed.

If any condition fails, STOP.

## Phase 1 — Build blocker working set

Create:

* docs/sprints/beta_readiness/P1-17_blocker_resolution_manifest.yaml

Include all 11 candidates:

* 4 package-identity unresolved candidates
* 7 transferrin-saturation / derived-marker candidates

For each candidate record:

* candidate ID
* staged package ID
* staged PSI path
* staged compile manifest path if available
* source spec ID if available
* signal ID
* activation key if available
* package ID in staged PSI
* proposed production package ID
* primary metric
* supporting markers
* derived metric dependency if any
* blocker at sprint start
* adjudication result
* opt-in status
* validation result
* core-backend handoff required: yes/no

Allowed adjudication results:

* READY_FOR_PRODUCTION_OPT_IN
* OPTED_IN
* BLOCKED_PACKAGE_IDENTITY_UNRESOLVED
* BLOCKED_DERIVED_MARKER_POLICY_UNRESOLVED
* BLOCKED_REQUIRES_CORE_BACKEND_AGENT
* BLOCKED_REQUIRES_MEDICAL_REVIEW
* BLOCKED_REQUIRES_SOURCE_RESEARCH_ADJUDICATION
* BLOCKED_VALIDATION_FAILURE
* OUT_OF_SCOPE_FOR_P1_17

## Phase 2 — Package identity adjudication

For the 4 package-identity candidates, determine whether a safe Knowledge Bus-only resolution exists.

Allowed safe outcomes:

1. A matching production package exists with the same `package_id` as the staged PSI.
2. A deterministic existing repository artefact proves that the staged PSI can be regenerated or represented under the production package identity without medical content change.
3. Candidate remains blocked.

### STOP gate 1 — Package identity boundary

STOP for the candidate if:

* the production package ID differs from the PSI internal `package_id`
* only `source_spec_id` links the staged PSI to a different production package ID
* a new production package would need to be created
* medical content would need to be edited
* deterministic identity-normalisation tooling does not exist
* package provenance cannot be proven from repository evidence
* resolution requires backend/core/backend/scripts/backend/ssot edits

If STOP fires, classify the candidate as either:

* `BLOCKED_PACKAGE_IDENTITY_UNRESOLVED`
* `BLOCKED_REQUIRES_CORE_BACKEND_AGENT`
* `BLOCKED_REQUIRES_SOURCE_RESEARCH_ADJUDICATION`

Do not cross-place PSI.

## Phase 3 — Derived-marker blocker adjudication

For the 7 transferrin-saturation / derived-marker candidates:

1. Identify exactly what derived marker is required.
2. Determine whether `transferrin_saturation` is already represented as a governed Knowledge Bus/package-level concept.
3. Determine whether the blocker is:

   * package/PSI identity only
   * missing production PSI artefact only
   * missing Knowledge Bus package authority only
   * missing backend derived-marker calculation
   * missing parser/canonicalisation support
   * missing validator support
   * medical-review issue
4. Do not change backend logic.

### STOP gate 2 — Derived-marker agent boundary

STOP for the candidate if resolving it requires:

* backend derived-marker calculation
* parser changes
* SSOT canonicalisation changes
* validator changes
* runtime loader changes
* test changes
* frontend/DTO/report/scoring/Gemini changes
* global/default reference ranges
* medical authority review
* new calculation policy

If STOP fires because core backend work is required, classify:

`BLOCKED_REQUIRES_CORE_BACKEND_AGENT`

If STOP fires because medical authority is required, classify:

`BLOCKED_REQUIRES_MEDICAL_REVIEW`

If STOP fires because Knowledge Bus authority is insufficient, classify:

`BLOCKED_DERIVED_MARKER_POLICY_UNRESOLVED`

## Phase 4 — Safe Knowledge Bus-only implementation

For candidates classified `READY_FOR_PRODUCTION_OPT_IN`, implement only Knowledge Bus-safe changes:

1. Add production `promoted_signal_intelligence.yaml` to the correct matching production package.
2. Add `promoted_signal_intelligence:` to that package manifest.
3. Preserve `behavioural_impact: NONE` unless existing value differs.
4. Do not alter medical meaning.

Production PSI content may differ from staged PSI only where the difference is a documented package identity/provenance normalisation supported by repository evidence and not medical content.

For each production PSI created, document field-level differences versus staged PSI.

### STOP gate 3 — Content integrity

STOP for the candidate if opt-in requires changing:

* medical claims
* thresholds
* activation logic
* evidence strength
* contradiction logic
* supporting marker relationships
* interpretation text
* runtime behaviour
* package identity without deterministic support

## Phase 5 — Validation

For each newly opted-in candidate:

1. Validate PSI using the repository-supported CLI for `validate_promoted_signal_intelligence.py`.
2. Validate the package:

`python backend/scripts/validate_knowledge_package.py --package-dir knowledge_bus/packages/<package>`

3. Rerun:

`python backend/scripts/validate_staged_psi_activation_readiness.py`

Do not edit validators or tests.

### STOP gate 4 — Validation failure

If validation fails:

* fix only if the fix is Knowledge Bus-only and does not alter medical meaning
* otherwise revert/exclude the candidate
* classify as `BLOCKED_VALIDATION_FAILURE` or `BLOCKED_REQUIRES_CORE_BACKEND_AGENT`

## Phase 6 — Core backend handoff manifest

Create this only if one or more candidates requires core backend work:

* docs/sprints/beta_readiness/P1-17_core_backend_handoff_manifest.yaml

For each handoff candidate record:

* candidate ID
* blocking reason
* exact file/domain likely requiring core backend ownership
* evidence from repository inspection
* why Medical Intelligence agent did not edit it
* expected backend-agent outcome
* whether PSI opt-in should be attempted after backend resolution

Do not write backend implementation instructions beyond the blocker boundary.

## Phase 7 — Sprint report and register

Create:

* docs/sprints/beta_readiness/P1-17_remaining_psi_blocker_resolution.md

Report must include:

1. start-state candidate list
2. package-identity adjudication results
3. derived-marker adjudication results
4. candidates opted in, if any
5. candidates blocked
6. candidates requiring core backend handoff
7. validation commands and results
8. confirmation that no backend/SSOT/runtime/frontend/test files were edited
9. confirmation that no staged generated-pilot files were edited
10. confirmation that no medical-review blocked candidates were promoted
11. confirmation that no runtime/user-facing activation occurred
12. recommended next outcome-based package

Update:

* docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md

Keep the register entry lightweight.

## Acceptance criteria

P1-17 passes only if:

1. All 11 candidates are adjudicated.
2. All 4 package-identity candidates are either safely resolved and opted in, or explicitly blocked.
3. All 7 derived-marker candidates are either safely resolved and opted in, or explicitly blocked/handoff-classified.
4. No cross-ID PSI placement occurs.
5. No backend/ssot, backend/core, backend/scripts, backend/tests, frontend, DTO, scoring, Gemini, parser, runtime loader, or validator files are modified.
6. No generated-pilot files are modified.
7. No medical-review blocked PSI is promoted.
8. Every newly opted-in PSI validates.
9. Every changed package validates.
10. Staged activation-readiness validator runs successfully.
11. Core backend handoff manifest exists if core backend work is required.
12. Sprint report exists.
13. Build register is updated.
14. No runtime/user-facing activation is introduced.
15. Final report recommends the next outcome-based package.

## Closure requirements

Before finish, perform the mandatory Post-Implementation Closure Protocol.

Run and report:

* `git branch --show-current`
* `git status --short`
* `git log --oneline -n 5`
* `git diff --name-only`
* `git diff --cached --name-only`
* `git stash list`

Confirm:

* branch matches this sprint branch
* no unrelated tracked/untracked files
* no tooling leakage
* no stash ambiguity
* no parked files outside the repository
* latest commit contains only in-scope work

Then run:

* `python backend/scripts/run_work_package.py finish`

After successful finish, handle `automation_bus/latest_cursor_status.json` under Automation Bus SOP v1.3.1.

Do not merge. Human merge authority is required.
