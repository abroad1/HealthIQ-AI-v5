---
work_id: CRP-PASS3-MIGRATION_crp_legacy_s24_package_and_signal_naming_alignment
branch: work/CRP-PASS3-MIGRATION-crp-legacy-s24-package-and-signal-naming-alignment
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# CRP-PASS3-MIGRATION — CRP Legacy s24 Package and Signal Naming Alignment

## Purpose

Resolve the remaining CRP legacy package / signal naming carry-forward identified by ARCH-LEGACY-1 and ARCH-LEGACY-2.

ARCH-LEGACY-2 retired several stale Wave 1 pathways, but left open:

```text
CF-ARCHLEG1-002 — CRP legacy s24 package / signal naming split
CF-ARCHLEG1-004 — partial: CRP migration status and root-cause promotion inventory validator guards
````

This sprint must investigate and, if safely bounded, align the CRP / systemic inflammation pathway with the current governed research-to-runtime architecture.

The goal is to remove or explicitly classify legacy CRP runtime dependency without destabilising signal activation or user-facing interpretation.

## Baseline requirement

Start from clean `main`.

Expected prior completed work:

```text
ARCH-RT programme fully merged through ARCH-RT-6
MED-REV-1 merged
MED-REV-2 merged
KB-UTIL-1 merged
LAYER-B-1 merged
ARCH-LEGACY-1 merged
ARCH-LEGACY-2 merged
docs/sprints/launch_core_carry_forward_register.md present and updated
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

```text
- current branch is not main
- local main does not equal origin/main
- working tree contains unrelated changes
- ARCH-LEGACY-2 is not merged
- docs/sprints/launch_core_carry_forward_register.md is missing
```

Important:

```text
docs/sprints/launch_core_carry_forward_register.md may contain carry-forward updates made after ARCH-LEGACY-2 merge.

Cursor must inspect it before starting. If it is modified but uncommitted, preserve it according to Automation Bus rules before running the work package. Do not discard it.
```

## Governance classification

```yaml
risk_level: HIGH
change_type: MIXED
execution_model: TWO_PHASE_START_FINISH
```

Reason:

This sprint may touch signal package authority, CRP/systemic inflammation signal naming, package provenance, runtime package references, validator guards and tests. This is runtime-adjacent medical interpretation logic.

## Standard rules

This work remains governed by the standard Knowledge Bus and Automation Bus SOPs already active in the repository.

Do not re-read SOPs unless the applicable governance requirement cannot be located.

## Carry-forward register handling

Before implementation, read:

```text
docs/sprints/launch_core_carry_forward_register.md
```

Relevant carry-forwards:

```text
CF-ARCHLEG1-002 — CRP legacy s24 package / signal naming split
CF-ARCHLEG1-004 — partial: CRP migration status and root-cause promotion inventory validator guards
```

If this sprint resolves or reclassifies these items, update the register.

If this sprint creates new carry-forwards, add them to the register.

Do not leave carry-forwards only in chat, audit reports or status summaries.

## Authoritative inputs

Read these sprint-specific files before making changes:

```text
docs/sprints/launch_core_carry_forward_register.md
docs/audit-papers/ARCH-LEGACY-1_pathway_retirement_audit.md
docs/audit-papers/ARCH-LEGACY-2_targeted_retirement_implementation_report.md
docs/audit-papers/PROGRAMME-STATUS-1_healthiq_launch_workstream_consolidation_audit.md
docs/audit-papers/PASS3_research_asset_utilisation_investigation_cursor.md
docs/architecture/ARCH-R1_research_asset_to_runtime_intelligence_architecture_review_cursor.md
docs/audit-papers/active_intelligence_authority_manifest.md
docs/audit-papers/ARCH-RT-5D_unresolved_provenance_register.md
docs/audit-papers/KB-UTIL-1_pass3_card_evidence_compile_and_consume_report.md
backend/scripts/validate_day_one_architecture.py
```

Inspect as implementation authority:

```text
knowledge_bus/packages/**
knowledge_bus/research/investigation_specs/multi_llm_research/*_Pass_3.json
knowledge_bus/compiled/estate_index_v1.yaml
backend/core/analytics/signal_evaluator.py
backend/core/analytics/domain_score_assembler.py
backend/core/analytics/domain_narrative_wave1.py
backend/core/knowledge/**
backend/scripts/validate_day_one_architecture.py
backend/tests/**
```

If paths differ, locate and report the actual paths.

## Problem statement

Current audits indicate that CRP / systemic inflammation may still depend on a legacy package path:

```text
pkg_s24_crp_high_inflammation
```

There may also be a naming split between:

```text
signal_crp_high
signal_systemic_inflammation
```

This needs to be resolved or explicitly classified so future work does not accidentally rely on stale package authority.

## Required preflight

Before making implementation changes, verify and report:

```text
1. Which CRP-related signals exist.
2. Which CRP-related packages exist.
3. Which CRP-related Pass 3 specs exist.
4. Which CRP package/signals are currently used at runtime.
5. Whether pkg_s24_crp_high_inflammation is still active.
6. Whether signal_crp_high and signal_systemic_inflammation are distinct, aliases, duplicates or different clinical concepts.
7. Whether CRP is visible to users after MED-REV-1/2/KB-UTIL-1.
8. Whether CRP affects hero, pattern, root-cause, health-system card or marker-level surfaces.
9. Whether a dedicated Pass 3 CRP package/spec already exists and can replace the legacy s24 path.
10. Whether migration can be safely bounded to CRP only.
```

STOP if CRP usage is broader than expected or cannot be safely classified.

## Scope

Allowed scope:

```text
1. Classify CRP-related signals/packages/specs.
2. Resolve or explicitly document signal_crp_high vs signal_systemic_inflammation naming.
3. Migrate CRP runtime package pointer from legacy s24 to governed Pass 3 package only if a suitable governed package/spec exists.
4. If migration is unsafe, classify the legacy path with validator/report evidence rather than forcing implementation.
5. Add guardrails/tests preventing accidental ambiguity or duplicate CRP authority.
6. Update carry-forward register.
7. Produce sprint report.
```

## Out of scope

Do not:

```text
- change CRP clinical thresholds
- change signal activation mathematics
- change scoring rails
- change biomarker SSOT
- change unit conversion
- change SignalEvaluator behaviour beyond package authority/naming alignment
- implement broad Pass 3 estate compiler
- implement hypothesis/contradiction/confirmatory test surfacing
- change root-cause promotion policy
- change PSI runtime status
- change frontend UX
- re-surface MED-REV-1 hidden subsystems as scored findings
- introduce fallback parsers
```

## Implementation guidance

Preferred outcomes in order:

```text
A. If governed Pass 3 CRP package/spec exists and is semantically equivalent:
   migrate runtime authority to the governed package/spec and guard it.

B. If governed Pass 3 CRP package/spec exists but is not semantically equivalent:
   do not migrate; classify the distinction and retain legacy path explicitly.

C. If no governed Pass 3 CRP package/spec exists:
   retain legacy path temporarily but classify it as a migration target and guard against accidental user-facing over-surfacing.

D. If signal_crp_high and signal_systemic_inflammation are actually different clinical concepts:
   document and test the distinction.

E. If they are duplicate/alias concepts:
   define the canonical naming policy and guard against duplicate authority drift.
```

Do not guess. Base the decision on repo evidence.

## Required tests

Add or update tests proving:

```text
1. CRP package/signal authority is explicitly classified.
2. signal_crp_high and signal_systemic_inflammation cannot silently drift as duplicate competing authorities.
3. If migrated, runtime uses the governed CRP package/spec.
4. If retained, legacy CRP path is explicitly classified and guarded.
5. CRP does not re-enter hidden MED-REV-1 subsystem surfaces as a scored finding.
6. No raw Pass 3 runtime reads are introduced.
7. No clinical thresholds/scoring rails are changed.
8. ARCH-RT-6 validator still passes.
```

Always run:

```powershell
python backend/scripts/validate_day_one_architecture.py
python -m pytest backend/tests/architecture/test_day_one_architecture_guardrails.py -q
```

Also run targeted tests for CRP/signal/package paths and any new regression tests.

## Validator / guardrail requirements

If the CRP authority decision is resolved, update `backend/scripts/validate_day_one_architecture.py` or an appropriate regression test so that:

```text
- CRP authority classification cannot silently regress
- duplicate CRP/systemic-inflammation signal authority cannot silently reappear
- hidden MED-REV-1 subsystem policy remains protected
```

Do not add brittle source-text checks unless this is already the repository pattern or clearly justified.

## Manual validation

Manual browser UAT is not required unless user-facing output changes.

If user-facing output changes, inspect a latest-engine regenerated result from:

```text
http://localhost:3000/results?analysis_id=746f2b0a-b470-4d87-8ed8-e2c3d1e68c02
```

Login:

```text
test-user3@example.com
Subaru@555
```

Confirm:

```text
- CRP/vascular strain is not surfaced as a scored subsystem
- cardiovascular card remains lipid-led
- no internal IDs/traces are visible
- no stale snapshot is mistaken for latest output
```

## STOP conditions

STOP and report if:

```text
1. CRP-related authority cannot be determined from repo evidence.
2. Migration would require clinical threshold changes.
3. Migration would change signal activation behaviour beyond package authority alignment.
4. CRP Pass 3 package/spec is absent or not semantically equivalent.
5. Duplicate signal naming cannot be safely resolved in one sprint.
6. Root-cause or PSI changes would be required.
7. Frontend changes would be required.
8. ARCH-RT-6 validator fails.
9. Sprint drifts into full Pass 3 compiler, LLM, UX or regeneration work.
```

## Required deliverable

Create:

```text
docs/audit-papers/CRP-PASS3-MIGRATION_crp_legacy_s24_package_and_signal_naming_alignment_report.md
```

The report must include:

```text
- CRP signal inventory
- CRP package inventory
- CRP Pass 3 spec inventory
- current runtime authority
- signal_crp_high vs signal_systemic_inflammation decision
- migration performed or deferred
- files changed
- validator/test changes
- carry-forward register updates
- confirmation no thresholds/scoring rails changed
- tests run
- results
- remaining risks / carry-forwards
```

## Evidence required from Cursor

Cursor must report:

```text
1. baseline branch/status evidence
2. carry-forward register read/update evidence
3. CRP package/signal/spec inventory
4. runtime reachability findings
5. authority decision
6. migration or deferral rationale
7. files changed
8. tests added/updated
9. test commands run
10. test results
11. manual validation result if required
12. confirmation no clinical thresholds/scoring rails changed
13. confirmation ARCH-RT-6 validator still passes
```

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

```text
- current branch matches work/CRP-PASS3-MIGRATION-crp-legacy-s24-package-and-signal-naming-alignment
- all changed files are tied to this sprint
- carry-forward register has been updated if required
- no clinical thresholds or scoring rails are changed
- no SignalEvaluator behavioural changes are introduced beyond declared authority alignment
- no hidden subsystem is reintroduced
- no ambiguous stash exists
- latest commit contains only in-scope work
```

## Success criteria

This sprint is complete only if:

```text
1. CRP legacy s24 package status is explicitly resolved or classified.
2. signal_crp_high / signal_systemic_inflammation naming relationship is clear.
3. Runtime authority cannot silently drift.
4. No CRP hidden subsystem re-surfacing occurs.
5. Carry-forward register is updated.
6. ARCH-RT-6 validator passes.
7. Tests prove the authority decision.
8. Automation Bus gate passes.
```

```
```
