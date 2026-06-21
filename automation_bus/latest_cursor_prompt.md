---
work_id: P1-15
branch: sprint/P1-15-first-production-psi-opt-in-pilot
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: CONTENT
---

# P1-15 — First Production PSI Opt-In Pilot with Contract STOP Gate

You are Cursor, implementing a governed HealthIQ AI Automation Bus work package.

This is one outcome-based SOP package. Do not split contract verification and production opt-in into separate work packages. Use the internal STOP gates below.

## Purpose

Move the first activation-ready Promoted Signal Intelligence cohort from generated-pilot staging into governed production Knowledge Bus package manifest opt-in, only if repository evidence proves that production PSI opt-in remains validation-governed and does not currently create runtime, user-facing, scoring, DTO, Gemini, report, or frontend behaviour.

## Current baseline

P1-14 has been merged.

Known baseline:

* 41 staged compile-manifest hashes repaired.
* P1-13 activation-readiness validator reran with zero hash mismatches.
* Confirmed cohort split:

  * 22 activation-ready candidates
  * 9 biomarker-identity blocked
  * 7 derived-marker blocked
  * 3 medical-review required
* No staged PSI content changed.
* No medical content changed.
* No production package manifests changed.
* No runtime activation occurred.

This sprint must start from that clean state.

## Mandatory files to read before editing

Read these files before any repository change:

* docs/sprints/beta_readiness/P1-14_activation_readiness_cohort_manifest.yaml
* docs/sprints/beta_readiness/P1-14_staged_psi_hash_repair_and_activation_cohort_lock.md
* docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md
* docs/governance/KNOWLEDGE_BUS_SOP_v1.3.1.md
* knowledge_bus/schema/package_manifest_schema.yaml
* knowledge_bus/schema/promoted_signal_intelligence_schema_v1.yaml
* backend/scripts/validate_knowledge_package.py
* backend/scripts/validate_promoted_signal_intelligence.py
* backend/scripts/validate_staged_psi_activation_readiness.py

Do not read historic P1-10, P1-11, P1-12, or P1-13 sprint files unless the P1-14 cohort manifest or sprint report is missing, inconsistent, or insufficient to identify source staged PSI artefacts.

Use search, not broad manual reading, to discover actual current consumers/loaders:

* rg "promoted_signal_intelligence" .
* rg "validate_promoted_signal_intelligence" .
* rg "promoted_signal_intelligence_validation" .
* rg "runtime_active" knowledge_bus backend docs

Inspect every relevant hit before deciding whether production opt-in is safe.

## Authority preflight

Before editing, verify and report:

1. Authoritative production package store path.
2. Authoritative package manifest schema path.
3. Authoritative promoted signal intelligence schema path.
4. Validator that enforces production package readiness.
5. Validator that enforces PSI schema compliance.
6. Whether any runtime loader currently consumes production package PSI.
7. Whether adding `promoted_signal_intelligence:` to a production manifest currently has any effect beyond validation/status reporting.
8. Whether production PSI placement would create a duplicate authority source.
9. Whether production opt-in requires compile manifest regeneration.

If any answer is uncertain, STOP before production package edits.

## Phase 0 — Branch and Automation Bus preflight

Confirm:

* current branch is `sprint/P1-15-first-production-psi-opt-in-pilot`
* `automation_bus/state/work_package_active.json` exists
* active token has `work_id: P1-15`
* active token branch matches this branch
* working tree is clean

If any condition fails, STOP.

## Phase 1 — Production PSI opt-in contract verification

Determine from repository evidence whether adding a production manifest field equivalent to:

`promoted_signal_intelligence: promoted_signal_intelligence.yaml`

would currently:

* only trigger package validation/status reporting; or
* alter runtime behaviour, emitted reasoning, scoring, DTOs, reports, frontend output, Gemini wording, or user-visible behaviour.

This decision must be made from actual schema, validator, loader and consumer code.

### STOP gate 1 — Runtime boundary

STOP before editing production packages if production PSI opt-in currently affects or may affect:

* signal activation
* InsightGraph construction
* root-cause output
* report/compiler output
* scoring
* DTOs
* frontend output
* Gemini wording
* user-visible behaviour
* any backend/core runtime path

If STOP gate 1 fires, create:

* docs/sprints/beta_readiness/P1-15_production_psi_opt_in_contract_blocker.md

Do not edit production package manifests.

## Phase 2 — Existing production opt-in overlap check

Find all current production package manifests containing `promoted_signal_intelligence:`.

Confirm:

1. package ID
2. PSI path
3. whether the PSI path exists
4. whether the package validates
5. whether it overlaps with any of the 41 staged P1-10/P1-11/P1-12 PSI artefacts
6. whether it overlaps with any of the 22 activation-ready P1-14 candidates

### STOP gate 2 — Existing opt-in conflict

STOP before new opt-ins if:

* any existing production opt-in ambiguously overlaps with the staged P1-10/P1-11/P1-12 PSI estate
* any existing production opt-in is invalid in a way that makes this sprint unsafe
* existing opt-ins create runtime behaviour not fully understood by Phase 1
* the same staged PSI would be opted into multiple production packages without explicit rationale

If STOP gate 2 fires, document the blocker and do not add new production opt-ins.

## Phase 3 — Map activation-ready candidates to production packages

Using P1-14 cohort manifest, classify each of the 22 activation-ready candidates.

Create:

* docs/sprints/beta_readiness/P1-15_production_psi_opt_in_mapping.yaml

For each candidate record:

* staged PSI path
* staged compile manifest path if available
* source spec ID if available
* signal ID if available
* activation key if available
* primary metric biomarker ID
* production package directory
* production package manifest path
* pre-opt-in package validation status
* classification

Allowed classifications:

* READY_FOR_OPT_IN
* ALREADY_OPTED_IN
* BLOCKED_NO_PRODUCTION_PACKAGE
* BLOCKED_AMBIGUOUS_PACKAGE_MAPPING
* BLOCKED_EXISTING_CONFLICT
* BLOCKED_VALIDATION_PRECHECK
* BLOCKED_CONTRACT_UNSAFE

Do not guess production package mappings.

### STOP gate 3 — No safe cohort

STOP before production edits if zero candidates are classified as READY_FOR_OPT_IN.

If some candidates are ready and others are blocked, proceed only with READY_FOR_OPT_IN candidates.

## Phase 4 — Production PSI opt-in

For each READY_FOR_OPT_IN candidate only:

1. Place the corresponding PSI artefact inside the mapped production package using the path required by the production manifest contract.
2. Preserve PSI content exactly.
3. Add the explicit `promoted_signal_intelligence:` entry to the production package manifest.
4. Do not edit medical content.
5. Do not edit staged PSI files.
6. Do not edit staged compile manifests.
7. Do not edit research_brief.yaml or signal_library.yaml.
8. Do not edit schemas, validators, runtime code, frontend code, scoring, DTOs, Gemini, or report compilers.

Preferred outcome:

* Opt in all 22 activation-ready candidates if all 22 pass the STOP gates and mapping checks.
* If only a subset passes, opt in the passing subset and document blockers for the rest.
* Do not arbitrarily limit the cohort once safety is proven.

### STOP gate 4 — Content integrity

STOP or exclude the affected candidate if any opted-in PSI file would require content modification to pass validation.

The correct response is to block the candidate, not edit the PSI medical content.

## Phase 5 — Validation

Run:

* package validation for every changed production package
* direct PSI validation for each opted-in PSI, using the actual validator CLI supported by the repository
* staged activation-readiness validation:

  * python backend/scripts/validate_staged_psi_activation_readiness.py

Record exact commands and results in the sprint report.

Do not modify validators or tests.

### STOP gate 5 — Validation failure

STOP or exclude the affected candidate if:

* package validation fails
* PSI validation fails
* staged activation-readiness validation regresses
* validation requires schema, validator, runtime, frontend, DTO, scoring or test changes
* validation requires PSI content edits

If only one candidate fails, revert/exclude that candidate and continue with the remaining passing candidates if safe.

## Phase 6 — Documentation and register

Create:

* docs/sprints/beta_readiness/P1-15_first_production_psi_opt_in_pilot.md

The report must include:

1. contract verification evidence
2. existing production opt-in overlap findings
3. candidate mapping summary
4. final opted-in cohort
5. blocked candidates and blocker class
6. validation commands and outputs
7. confirmation that no runtime/user-facing activation occurred
8. confirmation that no medical content changed
9. confirmation that no blocked PSI cohorts were promoted
10. recommended next product-forward package

Update:

* docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md

Keep the register entry lightweight.

## Expected deliverables

Expected files may include:

* docs/sprints/beta_readiness/P1-15_first_production_psi_opt_in_pilot.md
* docs/sprints/beta_readiness/P1-15_production_psi_opt_in_mapping.yaml
* docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md
* knowledge_bus/packages/<selected_pkg>/package_manifest.yaml
* knowledge_bus/packages/<selected_pkg>/promoted_signal_intelligence.yaml

If STOP gate 1 or 2 fires before opt-in, expected files may instead include:

* docs/sprints/beta_readiness/P1-15_production_psi_opt_in_contract_blocker.md
* docs/sprints/beta_readiness/P1-15_production_psi_opt_in_mapping.yaml, if mapping could be safely performed
* docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md

## Forbidden files

Do not modify:

* backend/core/
* backend/scripts/
* backend/tests/
* backend/ssot/
* frontend/
* knowledge_bus/generated_pilot/**/promoted_signal_intelligence.yaml
* knowledge_bus/generated_pilot/**/compile_manifest.yaml
* knowledge_bus/research/
* docs/strategy/beta_readiness/HEALTHIQ_AI_BETA_READINESS_DEFINITIVE_STRATEGY_FINAL_2026-06-20.md
* automation_bus/latest_gate_evidence.json
* automation_bus/latest_gate_output.txt

Do not allow tooling files into the sprint branch, including:

* .codex/
* .cursor/
* .vscode/
* AGENTS.md

## Acceptance criteria

This sprint passes only if:

1. Production PSI opt-in contract is verified from repository evidence.
2. Existing production opt-ins are inventoried and overlap-checked.
3. All 22 activation-ready candidates are mapped or explicitly blocked.
4. Only activation-ready candidates are opted in.
5. No identity-blocked, derived-marker-blocked or medical-review-blocked PSI is opted in.
6. Every changed production package validates.
7. Every opted-in PSI validates.
8. Staged activation-readiness validation still passes.
9. No staged PSI content is modified.
10. No medical content is changed.
11. No biomarker IDs are changed.
12. No runtime, frontend, Gemini, DTO, scoring, report compiler, orchestrator or backend/core code is changed.
13. No user-facing behaviour is introduced.
14. Mapping and sprint report files are created.
15. BUILD_DELIVERABLE_REGISTER is updated.
16. The final report recommends the next outcome-based work package.

## Classification note

This sprint is HIGH / CONTENT.

HIGH is required because production Knowledge Bus medical-intelligence assets are being opted into package manifests.

CONTENT is valid only if Phase 1 proves production PSI opt-in does not alter emitted reasoning, runtime behaviour, ranking, scoring, output construction, or user-visible behaviour.

If Phase 1 proves behaviour changes, STOP. Do not reclassify inside the sprint.

## Closure requirements

Before finish, perform the mandatory Post-Implementation Closure Protocol.

Run and report:

* git branch --show-current
* git status --short
* git log --oneline -n 5
* git diff --name-only
* git diff --cached --name-only
* git stash list

Confirm:

* branch matches this sprint branch
* working tree is clean before finish
* no unrelated tracked modifications remain
* no stray tooling files are present
* no ambiguous stash exists
* latest commit contains only in-scope work

Then run:

* python backend/scripts/run_work_package.py finish

After successful finish, handle `automation_bus/latest_cursor_status.json` under Automation Bus SOP v1.3.1.

Do not merge. Human merge authority is required.
