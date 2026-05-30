---
work_id: LAUNCH-CORE-3_result_versioning_replay_and_regeneration_policy
branch: work/LAUNCH-CORE-3-result-versioning-replay-and-regeneration-policy
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# LAUNCH-CORE-3 — Result Versioning, Replay and Regeneration Policy

## Purpose

Define and, where safely bounded, implement the HealthIQ result-versioning policy required to preserve deterministic auditability while allowing users to regenerate old results using the current engine.

The core principle is:

```text
Never silently overwrite a generated result.
Preserve the old result as an immutable snapshot.
Allow deterministic regeneration as a new result version.
````

This sprint is required because multi-panel UAT found that old persisted result DTOs can still show stale completeness logic and, in older records, legacy defects such as `total_bilirubin` false-missing.

That must not be solved by destructive refresh.

## Baseline requirement

Start from clean `main`.

Expected prior completed work:

```text
ARCH-RT programme fully merged through ARCH-RT-6
LAUNCH-CORE-1 merged
LAUNCH-CORE-2 UAT completed
```

Before creating or switching branch, run and report:

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
* LAUNCH-CORE-1 is not merged
* LAUNCH-CORE-2 audit report is missing
* untracked or uncommitted files are present

## Governance classification

```yaml
risk_level: HIGH
change_type: MIXED
execution_model: TWO_PHASE_START_FINISH
```

Reason:

This sprint may touch persisted result metadata, API result retrieval, regeneration policy, database schema/migration design, audit documents and possibly backend persistence flow. Result immutability and deterministic replay are core product integrity surfaces.

## Standard rules

This work remains governed by the standard Knowledge Bus and Automation Bus SOPs already active in the repository.

Do not re-read SOPs unless the applicable governance requirement cannot be located.

## Authoritative inputs

Read these sprint-specific files before making changes:

```text
docs/audit-papers/LAUNCH-CORE-2_multi_panel_launch_readiness_uat.md
docs/audit-papers/LAUNCH-CORE-1_results_page_card_coherence_and_consumer_copy_report.md
docs/audit-papers/ARCH-RT-6_day_one_architecture_acceptance_audit.md
docs/audit-papers/active_intelligence_authority_manifest.md
docs/audit-papers/day_one_architecture_launch_readiness_audit.md
docs/architecture/ARCH-RT-6_day_one_architecture_guardrails_report.md
backend/scripts/validate_day_one_architecture.py
```

Also inspect as implementation authority:

```text
backend/api/**
backend/core/pipeline/**
backend/core/analytics/**
backend/core/models/**
backend/core/contracts/**
backend/db/**
backend/migrations/**
frontend/app/(app)/results/**
frontend/app/lib/**
```

If actual persistence/API paths differ, locate and report them.

## Problem statement

Fresh analyses generated after LAUNCH-CORE-1 behave correctly.

Older persisted analyses can still return stale DTOs:

```text
18e14232... → stale completeness maths
bb695d3c... → stale completeness maths + legacy total_bilirubin false-missing
```

This is not a current runtime assembly defect.

It is a persisted-result versioning/replay problem.

## Non-negotiable architectural rule

Generated result payloads are immutable.

Do not silently mutate or overwrite old generated results.

A regenerated result must be a new version linked to the same source input, not a destructive replacement.

Required model:

```text
same raw input + same questionnaire + same engine/estate/schema versions
→ reproducible original result

same raw input + same questionnaire + newer engine/estate/schema versions
→ new result version
```

## Required policy decisions

This sprint must define the policy for:

1. immutable result snapshots
2. deterministic result replay
3. versioned regeneration
4. stale-result detection
5. result lineage
6. user-facing stale-result messaging
7. launch handling for dev/test stale records
8. audit hash requirements

## Required metadata model

Investigate current available fields and propose or implement metadata equivalent to:

```text
analysis_id
result_version_id
parent_analysis_id or source_analysis_id
raw_input_hash
parsed_biomarker_payload_hash
questionnaire_hash
engine_version
pipeline_version
result_schema_version
knowledge_estate_version
active_authority_manifest_hash
compiled_estate_index_hash
compile_manifest_hashes
prompt_template_version/hash if applicable
generated_at
result_payload_hash
supersedes_result_version_id
superseded_by_result_version_id
regeneration_reason
```

Do not invent fields blindly. First inspect current persistence model.

If implementation is too broad, produce a migration/design plan rather than forcing code changes.

## Scope

Allowed scope:

1. Inspect current result persistence model.
2. Inspect current analysis/result API retrieval path.
3. Inspect whether raw input and parsed biomarker payload are available for deterministic regeneration.
4. Define immutable result snapshot policy.
5. Define result version metadata contract.
6. Define stale-result detection rule.
7. Define user-facing stale-result behaviour.
8. Define regeneration flow.
9. Implement minimal metadata/stale detection only if safely bounded.
10. Add tests if implementation occurs.
11. Produce design/audit report.
12. Update launch-readiness audit with the decision.

## Implementation boundary

This sprint may implement only if the required change is small and safe.

Allowed bounded implementation examples:

```text
- add result version/status classification helper
- add stale-result detection function
- add API metadata field showing result is legacy/stale
- add frontend warning/banner for stale result
- add tests for classification only
```

Do not implement full destructive refresh.

Do not implement broad database migration unless hardening confirms it is safe and bounded.

Do not implement full regeneration job unless explicitly approved after investigation.

## Required deliverables

Create:

```text
docs/architecture/LAUNCH-CORE-3_result_versioning_replay_and_regeneration_policy.md
docs/audit-papers/LAUNCH-CORE-3_result_versioning_replay_and_regeneration_audit.md
```

If implementation occurs, also update relevant tests and implementation files.

## Policy document requirements

`docs/architecture/LAUNCH-CORE-3_result_versioning_replay_and_regeneration_policy.md` must include:

* immutable result principle
* deterministic replay principle
* versioned regeneration model
* required metadata model
* current repository support/gaps
* stale-result detection rule
* UI behaviour for stale results
* API behaviour for stale results
* database/migration implications
* dev/test data handling
* production data handling
* recommended implementation sequence
* launch decision

## Audit report requirements

`docs/audit-papers/LAUNCH-CORE-3_result_versioning_replay_and_regeneration_audit.md` must include:

* current persistence paths
* current API result retrieval paths
* whether old results are immutable today
* whether raw source input is available
* whether deterministic regeneration is currently possible
* which version/hash fields exist today
* which fields are missing
* stale analysis examples:

  * `18e14232-9f93-45e6-820c-004ab5a16235`
  * `bb695d3c-453e-4e49-abff-ae80587b4248`
  * `746f2b0a-b470-4d87-8ed8-e2c3d1e68c02`
* recommended launch handling for stale records
* implementation performed, if any
* tests run
* remaining risks

## User-facing behaviour to define

Define one of these launch behaviours:

```text
A. Hide stale dev/test analyses from launch users.
B. Display stale result with “Generated using older engine” warning.
C. Offer “Regenerate with latest engine” and create a new result version.
D. Automatically create a new result version on access, preserving old version.
```

Preferred architecture:

```text
C first, D later only if fully auditable.
```

Do not silently overwrite.

## Out of scope

Do not:

* overwrite persisted result payloads
* delete historical results
* implement destructive refresh
* change clinical scoring logic
* change card evidence logic
* change root-cause logic
* change PSI status
* change SignalRegistry or SignalEvaluator
* change biomarker SSOT
* change unit conversion
* change frontend interpretation logic beyond stale-result messaging if implemented
* introduce fallback parsers
* create broad regeneration jobs without explicit approval

## Required tests

If implementation occurs, add or update tests for:

1. stale result classification
2. current result classification
3. immutable snapshot policy
4. result version metadata serialisation
5. API stale flag if added
6. frontend stale banner if added
7. no destructive overwrite behaviour

Always run:

```powershell
python backend/scripts/validate_day_one_architecture.py
python -m pytest backend/tests/architecture/test_day_one_architecture_guardrails.py -q
```

If no implementation occurs, run only relevant existing validators and document why no code tests were added.

## STOP conditions

STOP and report if:

1. raw input required for regeneration is not available
2. result persistence model is unclear
3. implementation would require broad schema migration
4. regeneration would overwrite old results
5. deterministic replay cannot be supported with current metadata
6. implementation would touch clinical interpretation logic
7. implementation would weaken ARCH-RT guardrails
8. stale-result UI requires broader product decision
9. tests cannot prove immutability if implementation occurs

## Evidence required from Cursor

Cursor must report:

1. baseline branch/status evidence
2. persistence model findings
3. API retrieval path findings
4. available metadata fields
5. missing metadata fields
6. stale result classification findings
7. deterministic replay feasibility
8. recommended policy
9. implementation changes, if any
10. tests run
11. test results
12. launch recommendation

## Closure requirements

Before finish, run and report:

```powershell
git branch --show-current
git status --short
git log --oneline -n 5
git diff --name-only
git diff --cached --name-only
git stash list
```

Do not run finish unless:

* current branch matches `work/LAUNCH-CORE-3-result-versioning-replay-and-regeneration-policy`
* all changed files are tied to this sprint
* no destructive refresh logic is included
* no clinical interpretation logic is changed
* no ambiguous stash exists
* latest commit contains only in-scope work

## Success criteria

This sprint is complete only if:

1. immutable result policy is defined
2. versioned regeneration policy is defined
3. deterministic replay requirements are documented
4. current repository gaps are documented
5. stale-result handling is explicitly decided
6. old results are not overwritten
7. launch handling for stale records is defined
8. ARCH-RT guardrails still pass
9. tests or audit evidence support the decision
10. Automation Bus gate passes

```
```
