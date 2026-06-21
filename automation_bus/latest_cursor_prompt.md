---
work_id: P1-16
branch: sprint/P1-16-psi-identity-blocker-remediation
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# P1-16 — PSI Identity & Blocker Remediation Pack with Opt-In STOP Gate

You are Cursor, implementing a governed HealthIQ AI Automation Bus work package.

This is one outcome-based SOP package. Do not split package identity adjudication, biomarker identity adjudication, validation, and newly cleared PSI opt-in into separate work packages unless a STOP gate fires.

This sprint must push the product forward with governable speed.

## Purpose

Resolve identity/provenance blockers preventing staged Promoted Signal Intelligence from moving into governed production package opt-in.

This package covers:

1. The 4 P1-15 deferred `BLOCKED_AMBIGUOUS_PACKAGE_MAPPING` candidates.
2. The 9 P1-14/P1-15 biomarker-identity blocked PSI candidates.
3. Same-sprint production opt-in for any candidates safely resolved by this work package.

This sprint must not become a report-only sprint.

## Current baseline

P1-15 has been merged.

Known baseline:

- 18 clean, ID-matched production PSI opt-ins were completed.
- 4 activation-ready candidates were deferred as `BLOCKED_AMBIGUOUS_PACKAGE_MAPPING`.
- The 4 deferred candidates were not opted into production packages.
- 9 staged PSI candidates remain blocked by biomarker identity issues.
- 7 staged PSI candidates remain blocked by derived-marker dependency.
- 3 staged PSI candidates remain blocked pending medical review.
- No runtime behaviour was introduced by P1-15.
- PSI remains non-user-facing unless explicitly activated later.

P1-16 must only address identity/provenance blockers. Do not address derived-marker blockers or medical-review blockers in this sprint.

## Strategic outcome

By the end of this sprint, HealthIQ should have:

- a clear adjudication outcome for the 4 package-identity candidates;
- a clear adjudication outcome for the 9 biomarker-identity candidates;
- production package opt-in completed for any candidates safely cleared;
- unresolved candidates explicitly classified with blocker reason;
- no cross-ID PSI placement;
- no runtime/user-facing activation.

## Mandatory files to read before editing

Read these files before making repository changes:

- docs/sprints/beta_readiness/P1-15_production_psi_opt_in_mapping.yaml
- docs/sprints/beta_readiness/P1-15_first_production_psi_opt_in_pilot.md
- docs/sprints/beta_readiness/P1-14_activation_readiness_cohort_manifest.yaml
- docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md
- docs/governance/KNOWLEDGE_BUS_SOP_v1.3.1.md
- docs/governance/KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL_v1.1.md
- backend/ssot/biomarkers.yaml
- knowledge_bus/schema/package_manifest_schema.yaml
- knowledge_bus/schema/promoted_signal_intelligence_schema_v1.yaml
- backend/scripts/validate_knowledge_package.py
- backend/scripts/validate_promoted_signal_intelligence.py
- backend/scripts/validate_staged_psi_activation_readiness.py

Use targeted search rather than broad historic reading.

Only read historic P1-10, P1-11, P1-12 or P1-13 sprint artefacts if the P1-14/P1-15 artefacts are missing, inconsistent, or insufficient to identify the staged PSI source artefacts.

Use search to identify current SSOT and package validation consumers:

- rg "biomarkers.yaml" backend knowledge_bus docs
- rg "canonical" backend/ssot backend/scripts knowledge_bus
- rg "alias" backend/ssot backend/scripts knowledge_bus
- rg "promoted_signal_intelligence" backend knowledge_bus docs
- rg "source_spec_id" knowledge_bus docs backend

Inspect relevant hits before editing.

## Files in scope

Permitted files, if justified by the STOP gates:

- docs/sprints/beta_readiness/P1-16_psi_identity_blocker_remediation.md
- docs/sprints/beta_readiness/P1-16_identity_adjudication_manifest.yaml
- docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md
- backend/ssot/biomarkers.yaml
- knowledge_bus/packages/<resolved_package>/package_manifest.yaml
- knowledge_bus/packages/<resolved_package>/promoted_signal_intelligence.yaml

Production PSI opt-in is allowed only for candidates cleared by this sprint.

## Files out of scope

Do not modify:

- backend/core/
- backend/scripts/
- backend/tests/
- frontend/
- knowledge_bus/research/
- knowledge_bus/generated_pilot/**/*
- scoring policy files
- Gemini files
- DTO/report compiler/orchestrator files
- docs/strategy/beta_readiness/HEALTHIQ_AI_BETA_READINESS_DEFINITIVE_STRATEGY_FINAL_2026-06-20.md
- automation_bus/latest_gate_evidence.json
- automation_bus/latest_gate_output.txt

Do not allow tooling files into the sprint branch:

- .codex/
- .cursor/
- .vscode/
- AGENTS.md

## Critical prohibitions

Do not:

- introduce fallback or dummy parsers;
- substitute global/default biomarker ranges;
- alter lab-range interpretation policy;
- activate PSI at runtime;
- make frontend, Gemini, DTO, report compiler, scoring or orchestrator consume PSI;
- promote derived-marker blocked PSI;
- promote medical-review blocked PSI;
- cross-place PSI into a package whose manifest `package_id` differs from the PSI internal `package_id`;
- hand-edit medical content to force validation;
- create duplicate active medical authority;
- create new production packages without explicit STOP-gate approval inside this sprint;
- treat `source_spec_id` alone as sufficient for production identity if `package_id` conflicts remain unresolved.

## Phase 0 — Branch and Automation Bus preflight

Before implementation:

1. Confirm current branch is:

`sprint/P1-16-psi-identity-blocker-remediation`

2. Confirm `automation_bus/state/work_package_active.json` exists.
3. Confirm active token has `work_id: P1-16`.
4. Confirm active token branch matches this branch.
5. Confirm working tree is clean.

If any condition fails, STOP.

## Phase 1 — Build the identity blocker working set

Create an initial working set from current artefacts.

The working set must include:

1. The 4 P1-15 candidates classified as `BLOCKED_AMBIGUOUS_PACKAGE_MAPPING`.
2. The 9 P1-14/P1-15 candidates classified as biomarker-identity blocked.

Create:

- docs/sprints/beta_readiness/P1-16_identity_adjudication_manifest.yaml

For each candidate, record:

- staged package ID
- staged PSI path
- staged compile manifest path if available
- source spec ID if available
- signal ID if available
- activation key if available
- primary metric biomarker ID
- supporting biomarker IDs
- blocker class at sprint start
- proposed resolution path
- adjudication status
- production package candidate if any
- validation status
- opt-in status

Allowed adjudication statuses:

- READY_FOR_PRODUCTION_OPT_IN
- RESOLVED_ALREADY_OPTED_IN
- BLOCKED_PACKAGE_IDENTITY_UNRESOLVED
- BLOCKED_BIOMARKER_IDENTITY_UNRESOLVED
- BLOCKED_REQUIRES_DERIVED_MARKER_POLICY
- BLOCKED_REQUIRES_MEDICAL_REVIEW
- BLOCKED_REQUIRES_SOURCE_RESEARCH_ADJUDICATION
- BLOCKED_VALIDATION_FAILURE
- OUT_OF_SCOPE_FOR_P1_16

Do not guess missing mappings.

## Phase 2 — Package identity adjudication for the 4 deferred candidates

Adjudicate the four package-identity candidates:

- pkg_kb52c_rbc_high_erythrocytosis_pattern
- pkg_kb52c_rbc_low_iron_restricted_anemia_pattern
- pkg_kb52c_rdw_cv_high_iron_deficiency_anisocytosis
- pkg_kb52c_rdw_cv_high_mixed_red_cell_population_pattern

For each, determine from repository evidence whether:

A. the correct production home is an existing `pkg_kb58_*` package;
B. a `pkg_kb52c_*` production package should exist but is missing;
C. the staged PSI artefact should be re-staged/regenerated under the `pkg_kb58_*` identity;
D. the candidate must remain blocked pending package provenance/compile adjudication.

Evidence must include actual package manifest content, source document/source spec references, signal IDs, primary biomarker IDs, and any source provenance fields available.

### STOP gate 1 — Package identity safety

STOP before any production opt-in for the 4 package-identity candidates if:

- the host production package ID would differ from the PSI internal `package_id`;
- resolving the mismatch would require unsupported hand editing of medical content;
- creating a new production package would duplicate an existing active signal package;
- the correct production home cannot be proven from repository evidence;
- `source_spec_id` is the only link and package identity remains inconsistent;
- compile/provenance evidence is insufficient to justify identity migration.

If STOP gate 1 fires for a candidate, leave that candidate blocked as `BLOCKED_PACKAGE_IDENTITY_UNRESOLVED`.

Do not cross-place PSI into `pkg_kb58_*` unless the PSI internal `package_id` is also validly aligned to the host package identity through a deterministic, documented, non-medical identity-normalisation process.

If such deterministic identity-normalisation support does not exist in the repository, do not invent it. Block the candidate.

## Phase 3 — Biomarker identity adjudication for the 9 identity-blocked candidates

For each biomarker-identity blocked candidate:

1. Identify every non-canonical or unresolved biomarker ID.
2. Determine whether the issue is:
   - simple alias/synonym mismatch;
   - outdated package/staged ID naming;
   - missing SSOT alias;
   - missing SSOT canonical biomarker;
   - ambiguous medical concept;
   - supporting-marker identity issue;
   - derived-marker issue incorrectly classified as identity;
   - medical-review issue incorrectly classified as identity.
3. Check `backend/ssot/biomarkers.yaml`.
4. Check relevant validators and SSOT lookup behaviour.
5. Decide whether a safe one-to-one identity correction exists.

Permitted resolutions:

- add or correct a one-to-one alias in `backend/ssot/biomarkers.yaml`;
- update a production PSI copy to use an already-established canonical biomarker ID, only if this is pure identity normalisation and does not change medical meaning;
- classify as blocked where identity cannot be proven safely.

### STOP gate 2 — Biomarker identity safety

STOP for the affected candidate if:

- the biomarker maps to more than one plausible canonical ID;
- the proposed mapping changes medical meaning;
- the marker is a derived metric requiring calculation/parsing policy;
- the marker requires medical authority review;
- the SSOT lacks enough evidence to add an alias safely;
- resolving it would require backend parser/runtime changes outside this sprint;
- resolving it would require global/default reference ranges;
- resolving it would affect runtime interpretation beyond deterministic identity normalisation.

If STOP gate 2 fires for a candidate, classify it clearly and do not opt it in.

## Phase 4 — Implement safe identity resolutions

Apply only adjudicated safe changes.

Allowed implementation actions:

1. Add or correct SSOT aliases in `backend/ssot/biomarkers.yaml` where a one-to-one identity mapping is proven.
2. Create production PSI artefacts for resolved candidates only where:
   - the host production package exists;
   - the host manifest `package_id` matches the PSI internal `package_id`;
   - package identity is not ambiguous;
   - biomarker identity is canonical or safely normalised;
   - no medical content change is required.
3. Add `promoted_signal_intelligence:` to the production package manifest for resolved candidates only.
4. Update the P1-16 adjudication manifest.

Do not modify staged PSI files under `knowledge_bus/generated_pilot/`.

If production PSI content differs from staged PSI because of identity normalisation, the sprint report must include an explicit field-level diff showing:

- old ID
- new ID
- reason
- SSOT evidence
- confirmation that medical meaning did not change

### STOP gate 3 — Production content integrity

STOP or block the candidate if production PSI creation requires:

- changing medical claims;
- changing thresholds;
- changing activation logic;
- changing supporting marker relationships;
- changing evidence strength;
- changing interpretation text;
- changing runtime behaviour;
- unsupported package ID migration.

Identity metadata and biomarker canonicalisation are the only content changes allowed, and only with evidence.

## Phase 5 — Same-sprint opt-in for newly cleared candidates

For any candidate classified `READY_FOR_PRODUCTION_OPT_IN`:

1. Validate the host production package before opt-in if feasible.
2. Add the production PSI artefact.
3. Add the manifest opt-in.
4. Validate the production PSI.
5. Validate the production package.
6. Rerun staged activation-readiness validation.

Preferred outcome:

- Opt in every candidate safely cleared by P1-16.
- Do not arbitrarily defer safe opt-ins to a future sprint.
- Leave unresolved candidates explicitly blocked.

### STOP gate 4 — Opt-in safety

STOP or block the affected candidate if:

- production package validation fails;
- direct PSI validation fails;
- staged activation-readiness validation regresses unexpectedly;
- host package identity differs from PSI package identity;
- opt-in causes runtime/user-facing behaviour;
- validation failure would require medical content edits;
- validation failure would require backend/core, backend/scripts, backend/tests, frontend, DTO, scoring or Gemini changes.

## Phase 6 — Validation

Required validation after changes:

1. Validate every changed production package:

`python backend/scripts/validate_knowledge_package.py --package-dir knowledge_bus/packages/<pkg_name>`

2. Validate every newly opted-in PSI artefact using the repository-supported CLI for:

`backend/scripts/validate_promoted_signal_intelligence.py`

Inspect the script for exact supported arguments if necessary.

3. Rerun:

`python backend/scripts/validate_staged_psi_activation_readiness.py`

4. Run any existing SSOT/biomarker validation script if one exists and is discoverable without adding new code.

Do not edit validators or tests in this sprint.

### STOP gate 5 — Validation failure

If validation fails:

- fix only if the fix is within this sprint scope and does not require medical-content changes;
- otherwise revert/exclude the affected candidate and classify it as blocked;
- continue with other candidates only if safe.

## Phase 7 — Documentation and register update

Create:

- docs/sprints/beta_readiness/P1-16_psi_identity_blocker_remediation.md

The report must include:

1. start-state blocker summary;
2. package identity adjudication for the 4 deferred candidates;
3. biomarker identity adjudication for the 9 identity-blocked candidates;
4. SSOT changes made, if any;
5. production PSI artefacts created or opted in, if any;
6. candidates newly cleared;
7. candidates still blocked and exact blocker class;
8. validation commands and results;
9. confirmation that no derived-marker or medical-review blocked PSI was promoted;
10. confirmation that no runtime/user-facing activation occurred;
11. recommended next outcome-based work package.

Update:

- docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md

Keep the register entry lightweight.

## Expected deliverables

Expected files may include:

- docs/sprints/beta_readiness/P1-16_psi_identity_blocker_remediation.md
- docs/sprints/beta_readiness/P1-16_identity_adjudication_manifest.yaml
- docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md
- backend/ssot/biomarkers.yaml
- knowledge_bus/packages/<resolved_pkg>/package_manifest.yaml
- knowledge_bus/packages/<resolved_pkg>/promoted_signal_intelligence.yaml

Only include production package changes for candidates that pass all STOP gates.

## Acceptance criteria

This sprint passes only if:

1. All 4 P1-15 package-identity candidates are adjudicated.
2. All 9 biomarker-identity blocked candidates are adjudicated.
3. No candidate is cross-placed into a mismatched package ID.
4. No derived-marker blocked PSI is promoted.
5. No medical-review blocked PSI is promoted.
6. Every SSOT change, if any, is a proven one-to-one identity correction.
7. Every newly opted-in production PSI validates.
8. Every changed production package validates.
9. Staged activation-readiness validation runs successfully.
10. No staged generated-pilot files are modified.
11. No medical meaning is changed.
12. No biomarker mapping is guessed.
13. No backend/core, backend/scripts, backend/tests, frontend, DTO, scoring, Gemini or report compiler files are modified.
14. No runtime/user-facing activation is introduced.
15. P1-16 adjudication manifest exists and is complete.
16. Sprint report exists and explains cleared and blocked candidates.
17. BUILD_DELIVERABLE_REGISTER is updated.
18. The final report recommends the next outcome-based package.

## Classification note

This sprint is HIGH / MIXED.

HIGH applies because this sprint may touch `backend/ssot/biomarkers.yaml` and production Knowledge Bus medical-intelligence assets.

MIXED applies because SSOT identity changes may affect downstream validation and potentially runtime canonicalisation, even if no runtime code is changed.

If Phase 1 or Phase 3 proves that the required work would alter emitted reasoning, scoring, report output, DTOs, frontend output, Gemini output, or runtime signal activation, STOP before implementation and escalate.

## Closure requirements

Before finish, perform the mandatory Post-Implementation Closure Protocol.

Run and report:

- git branch --show-current
- git status --short
- git log --oneline -n 5
- git diff --name-only
- git diff --cached --name-only
- git stash list

Confirm:

- branch matches this sprint branch
- working tree is clean before finish
- no unrelated tracked modifications remain
- no stray tooling files are present
- no ambiguous stash exists
- latest commit contains only in-scope work

Then run:

- python backend/scripts/run_work_package.py finish

After successful finish, handle `automation_bus/latest_cursor_status.json` under Automation Bus SOP v1.3.1.

Do not merge. Human merge authority is required.
```
