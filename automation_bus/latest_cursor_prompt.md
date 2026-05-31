---
work_id: ARCH-LEGACY-2_targeted_retirement_implementation
branch: work/ARCH-LEGACY-2-targeted-retirement-implementation
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# ARCH-LEGACY-2 — Targeted Legacy Pathway Retirement Implementation

## Purpose

Implement the targeted legacy-retirement actions recommended by ARCH-LEGACY-1.

ARCH-LEGACY-1 confirmed there are no launch blockers, but identified several dead, stale, or insufficiently guarded legacy pathways that should be cleaned up now that the Wave 1 medical model, card evidence, narrative brief, and guardrails are stable.

This sprint must be targeted. It must not become broad cleanup.

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
docs/sprints/launch_core_carry_forward_register.md present and updated
````

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
- working tree is not clean
- ARCH-LEGACY-1 is not merged
- docs/sprints/launch_core_carry_forward_register.md is missing
- untracked or uncommitted files are present
```

## Governance classification

```yaml
risk_level: HIGH
change_type: MIXED
execution_model: TWO_PHASE_START_FINISH
```

Reason:

This sprint may remove or alter legacy backend pathways and extend architectural validators. Even if the target code is dead or unreachable, this touches runtime-adjacent analytical code and guardrail enforcement.

## Standard rules

This work remains governed by the standard Knowledge Bus and Automation Bus SOPs already active in the repository.

Do not re-read SOPs unless the applicable governance requirement cannot be located.

## Carry-forward register handling

Before implementation, read:

```text
docs/sprints/launch_core_carry_forward_register.md
```

If this sprint resolves any carry-forward, update the register.

If this sprint creates new carry-forwards, add them to the register.

Expected relevant carry-forwards include:

```text
CF-MEDREV2-003
CF-ARCHLEG1-001
CF-ARCHLEG1-002
CF-ARCHLEG1-003
CF-ARCHLEG1-004
```

Do not leave carry-forwards only in chat, audit reports, or status summaries.

## Authoritative inputs

Read these sprint-specific files before making changes:

```text
docs/sprints/launch_core_carry_forward_register.md
docs/audit-papers/ARCH-LEGACY-1_pathway_retirement_audit.md
docs/audit-papers/PROGRAMME-STATUS-1_healthiq_launch_workstream_consolidation_audit.md
docs/audit-papers/MED-REV-1_wave1_subsystem_visibility_and_label_alignment_report.md
docs/audit-papers/MED-REV-2_wave1_domain_card_copy_alignment_and_result_regeneration_ux_report.md
docs/audit-papers/KB-UTIL-1_pass3_card_evidence_compile_and_consume_report.md
docs/audit-papers/LAYER-B-1_narrative_brief_maturity_report.md
docs/audit-papers/ARCH-RT-6_day_one_architecture_acceptance_audit.md
backend/scripts/validate_day_one_architecture.py
```

Inspect as implementation authority:

```text
backend/core/analytics/wave1_subsystem_evidence.py
backend/core/analytics/domain_narrative_wave1.py
backend/core/analytics/domain_score_assembler.py
backend/core/knowledge/health_system_card_evidence.py
backend/core/knowledge/domain_flat_card_evidence.py
backend/scripts/validate_day_one_architecture.py
backend/tests/architecture/test_day_one_architecture_guardrails.py
backend/tests/regression/test_kb_util1_pass3_card_evidence_compile_and_consume.py
backend/tests/regression/test_med_rev1_wave1_subsystem_visibility.py
backend/tests/regression/test_med_rev2_domain_card_copy_and_regeneration.py
```

If paths differ, locate and report the actual paths.

## Scope

Allowed scope:

```text
1. Remove or neutralise confirmed dead legacy cardiovascular contributor helper code.
2. Remove or neutralise unreachable hard-coded Wave 1 subsystem fallback definitions.
3. Extend ARCH-RT-6 validator coverage for guardrail gaps identified by ARCH-LEGACY-1.
4. Add/update regression tests proving the retired paths cannot re-enter user-facing output.
5. Update carry-forward register for resolved/deferred items.
6. Produce sprint report.
```

## Specific implementation targets

### Target 1 — Legacy cardiovascular contributor / homocysteine bridge cleanup

Investigate and remove or neutralise dead / edge-case legacy helper paths identified by ARCH-LEGACY-1 and MED-REV-2.

Known concern:

```text
Older CV helper logic can still refer to vascular inflammation / homocysteine framing in edge cases.
Current visible card basis should remain Atherogenic lipid pattern where the visible scored subsystem is lipid-only.
```

Allowed actions:

```text
- delete dead helper if genuinely unused
- replace edge-case call path with governed current helper
- keep function only if still required for non-card surfaces, but classify and guard it
- add tests proving CV card copy cannot regress to inflammation/homocysteine score-basis when lipid is the visible scored subsystem
```

STOP if removal would affect a live non-card surface in a way not covered by tests.

### Target 2 — Hard-coded Wave 1 subsystem fallback retirement

Investigate:

```text
backend/core/analytics/wave1_subsystem_evidence.py
```

Known concern:

```text
Legacy _Wave1SubsystemDef fallback labels are stale and should not be reachable for compiled Wave 1 card evidence.
```

Allowed actions:

```text
- remove unreachable fallback partition if safe
- reduce it to an explicit fail-closed path for Wave 1 compiled subsystems
- update stale labels only if removal is unsafe
- add tests proving compiled Wave 1 subsystems cannot fall back to hard-coded definitions
```

Required behaviour:

```text
For launch-active Wave 1 compiled subsystems, absence of compiled evidence should fail closed or be explicitly classified. It must not silently fall back to stale hard-coded subsystem definitions.
```

STOP if removing fallback requires broad assembler redesign.

### Target 3 — Validator / Sentinel guardrail extension

Extend `backend/scripts/validate_day_one_architecture.py` for ARCH-LEGACY-1 identified gaps where safely bounded.

At minimum assess and implement if appropriate:

```text
- guard that launch-active Wave 1 subsystem evidence cannot use hard-coded fallback definitions
- guard that dead/legacy CV contributor path is not used for visible card score basis
- guard that domain_flat_card_evidence.py remains in launch-critical runtime path checks
- guard that KB-UTIL-1 manifest hash integrity remains enforced
- guard that hidden_v1 support subsystems cannot re-enter as visible scored card basis
```

Do not add brittle source-text checks unless they are the existing validator pattern or clearly justified.

### Target 4 — CRP / s24 legacy path

ARCH-LEGACY-1 may identify CRP legacy package migration as a carry-forward.

This sprint may inspect and classify, but should not implement CRP package migration unless it is genuinely small and already bounded.

Default decision:

```text
Do not migrate CRP Pass 3 package path in this sprint unless hardening approves it as in scope.
```

If not implemented, ensure the carry-forward register retains the item.

## Out of scope

Do not:

```text
- migrate root-cause YAML estate
- implement multi-frame root-cause promotion
- implement full Pass 3 estate compiler
- surface hypotheses / contradiction markers / confirmatory tests
- change signal activation
- change scoring rails
- change clinical thresholds
- change biomarker SSOT
- change unit conversion
- change PSI runtime status
- implement LLM narrative translation
- implement UX redesign
- change frontend rendering unless required by a removed backend field and approved
- remove evidence from governed artefacts
- introduce fallback parsers
```

## Required tests

Add or update tests proving:

```text
1. CV visible card copy cannot use inflammation/homocysteine as score basis when lipid is the only visible scored subsystem.
2. Hidden MED-REV-1 subsystems remain hidden.
3. Hard-coded Wave 1 subsystem fallback cannot re-enter launch-active compiled subsystem path.
4. Removed/dead helper functions are not referenced.
5. Validator catches any attempted reactivation of retired pathway where practical.
6. domain_flat_card_evidence remains covered by launch-critical validator paths.
7. KB-UTIL-1 manifest hash integrity still passes.
8. total_bilirubin prohibition remains intact.
9. ARCH-RT-6 validator still passes.
```

Always run:

```powershell
python backend/scripts/validate_day_one_architecture.py
python -m pytest backend/tests/architecture/test_day_one_architecture_guardrails.py -q
```

Also run targeted tests for:

```text
test_kb_util1_pass3_card_evidence_compile_and_consume.py
test_med_rev1_wave1_subsystem_visibility.py
test_med_rev2_domain_card_copy_and_regeneration.py
any new ARCH-LEGACY-2 regression tests
```

## Manual validation

Manual browser UAT is not required unless a user-facing output path is changed.

If any user-facing output is changed, manually inspect a latest-engine regenerated result from:

```text
http://localhost:3000/results?analysis_id=746f2b0a-b470-4d87-8ed8-e2c3d1e68c02
```

Login:

```text
test-user3@example.com
Subaru@555
```

Confirm no regression in:

```text
- cardiovascular card basis
- blood sugar card copy
- liver flat evidence
- hidden subsystem suppression
- internal ID/source-trace protection
```

## STOP conditions

STOP and report if:

```text
1. ARCH-LEGACY-1 report is missing.
2. Carry-forward register is missing.
3. Removing legacy code would affect live untested paths.
4. Hard-coded fallback cannot be removed without broad redesign.
5. Validator extension would be brittle or misleading.
6. Any change would alter clinical thresholds, scoring, SignalEvaluator, or SSOT.
7. Any hidden subsystem would be reintroduced.
8. ARCH-RT-6 validator fails.
9. Sprint drifts into Pass 3 estate compile, LLM translation, or UX redesign.
```

## Required deliverable

Create:

```text
docs/audit-papers/ARCH-LEGACY-2_targeted_retirement_implementation_report.md
```

The report must include:

```text
- items retired
- items retained and why
- files changed
- validator changes
- tests added/updated
- carry-forward register updates
- confirmation no clinical/scoring logic changed
- confirmation hidden subsystems remain hidden
- confirmation no raw Pass 3 runtime reads introduced
- tests run
- results
- remaining risks / carry-forwards
```

## Evidence required from Cursor

Cursor must report:

```text
1. baseline branch/status evidence
2. carry-forward register read/update evidence
3. legacy paths targeted
4. exact code removed/neutralised
5. validator changes
6. tests added/updated
7. test commands run
8. test results
9. manual validation result if required
10. confirmation no production-facing clinical behaviour changed except intended retirement protection
11. confirmation ARCH-RT-6 validator still passes
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
- current branch matches work/ARCH-LEGACY-2-targeted-retirement-implementation
- all changed files are tied to this sprint
- carry-forward register has been updated if required
- no clinical thresholds or scoring rails are changed
- no SignalEvaluator / SignalRegistry / SSOT changes are included
- no hidden subsystem is reintroduced
- no ambiguous stash exists
- latest commit contains only in-scope work
```

## Success criteria

This sprint is complete only if:

```text
1. Targeted legacy paths are removed, neutralised, or explicitly retained with rationale.
2. Launch-active Wave 1 compiled subsystem path cannot silently fall back to stale hard-coded definitions.
3. CV legacy narrative path cannot re-enter visible card score-basis copy.
4. Validator/guardrail coverage is improved for identified gaps.
5. Carry-forward register is updated.
6. No clinical scoring or signal behaviour changes.
7. ARCH-RT-6 validator passes.
8. Tests prove the retirement protections.
9. Automation Bus gate passes.
```

```
```
