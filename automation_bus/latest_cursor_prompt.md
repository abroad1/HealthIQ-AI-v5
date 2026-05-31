---
work_id: MED-REV-1_wave1_subsystem_visibility_and_label_alignment
branch: work/MED-REV-1-wave1-subsystem-visibility-and-label-alignment
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# MED-REV-1 — Wave 1 Subsystem Visibility and Label Alignment

## Purpose

Resolve the results-page UX hierarchy problem identified in LAUNCH-CORE-4.

The page is technically credible, but it currently reads as a stack of competent widgets rather than a guided health report. Users are exposed to too many competing scores, repeated lead-pattern language, and technical labels before they understand the main health story.

This sprint must improve narrative hierarchy and score clarity without discarding meaningful analysis.

The key audit finding is:

```text
The results page is technically credible but narratively immature. Users cannot quickly answer: “What is wrong, how sure are you, and what should I do?” without reading repetitive prose and reconciling competing scores.
````

Reference:

```text
docs/audit-papers/LAUNCH-CORE-4_results_page_narrative_hierarchy_and_score_rationalisation_audit.md
```

## Baseline requirement

Start from clean `main`.

Expected prior completed work:

```text
ARCH-RT programme fully merged through ARCH-RT-6
LAUNCH-CORE-1 merged
LAUNCH-CORE-2 UAT completed
LAUNCH-CORE-3 merged
LAUNCH-CORE-4 audit completed
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
* LAUNCH-CORE-3 is not merged
* LAUNCH-CORE-4 audit report is missing
* untracked or uncommitted files are present

## Governance classification

```yaml
risk_level: HIGH
change_type: MIXED
execution_model: TWO_PHASE_START_FINISH
```

Reason:

This sprint may touch backend result-presentation assembly, DTO shaping, frontend results layout, consumer copy helpers, stale/incompatible result messaging, and tests. It affects user-facing health interpretation and must be governed carefully.

## Standard rules

This work remains governed by the standard Knowledge Bus and Automation Bus SOPs already active in the repository.

Do not re-read SOPs unless the applicable governance requirement cannot be located.

## Authoritative inputs

Read these sprint-specific files before making changes:

```text
docs/audit-papers/LAUNCH-CORE-4_results_page_narrative_hierarchy_and_score_rationalisation_audit.md
docs/audit-papers/LAUNCH-CORE-2_multi_panel_launch_readiness_uat.md
docs/audit-papers/LAUNCH-CORE-1_results_page_card_coherence_and_consumer_copy_report.md
docs/architecture/LAUNCH-CORE-3_result_versioning_replay_and_regeneration_policy.md
docs/audit-papers/ARCH-RT-6_day_one_architecture_acceptance_audit.md
docs/architecture/ARCH-RT-6_day_one_architecture_guardrails_report.md
backend/scripts/validate_day_one_architecture.py
```

Also inspect as implementation authority:

```text
backend/app/routes/analysis.py
backend/core/dto/result_versioning_policy_v1.py
backend/core/analytics/domain_score_assembler.py
backend/core/analytics/report_compiler_v1.py
backend/core/analytics/domain_narrative_wave1.py
backend/core/models/**
backend/core/contracts/**
frontend/app/(app)/results/page.tsx
frontend/app/components/results/**
frontend/app/lib/resultsPageLayout.ts
frontend/app/lib/wave1HealthSystemCardDisplay.ts
frontend/app/lib/retailNarrativeSanitize.ts
frontend/app/lib/cardEvidenceConsumerCopy.ts
frontend/app/types/analysis.ts
```

If actual paths differ, locate and report them.

## Architectural principle: Layer A / B / C separation

This sprint must preserve the HealthIQ layer architecture.

```text
Layer A = raw / governed intelligence inputs
Layer B = interpretation, prioritisation, narrative assembly, DTO shaping
Layer C = presentation / rendering only
```

### Layer B responsibilities

Layer B should decide or expose:

```text
- primary story ordering
- section priority
- which sections are default-visible versus expandable
- consumer-safe narrative labels
- score hierarchy metadata
- confidence/completeness explanation fields
- stale/incompatible result messaging
- deduplicated consumer lead copy
- any meaning-changing narrative hierarchy decision
```

### Layer C responsibilities

Layer C may only:

```text
- render backend-provided DTO fields
- render sections in supplied or approved order
- collapse/expand sections
- display approved UI labels
- suppress raw/internal fields
- hide technical detail by default where instructed
```

Layer C must not infer:

```text
- which score matters most
- whether a clinical section is important
- which evidence is clinically meaningful
- what the main finding means
- how confidence should be interpreted clinically
- whether a marker is clinically relevant
```

STOP if completing the sprint would require the frontend to make clinical or interpretive prioritisation decisions that belong in Layer B.

## Non-negotiable content preservation rule

Do not simplify by deleting meaningful analysis.

The sprint may:

```text
- reorder
- collapse
- deduplicate
- rename
- summarise
- move technical detail behind expandable controls
```

The sprint must not:

```text
- remove clinically meaningful reasoning
- discard evidence-for / evidence-against
- delete marker evidence
- hide confidence limitations entirely
- remove missing-marker context
- remove root-cause reasoning
- remove next-step guidance
- weaken auditability
```

Definitions:

```text
Suppress = hide from default view, not remove from DTO or journey.
Merge = combine repeated presentation blocks into one clearer section while retaining source detail where useful.
Collapse = move into expandable detail.
```

The target is:

```text
same analytical richness
better narrative order
less repetition
clearer default view
technical depth still available on demand
```

## Core UX problems to fix

From LAUNCH-CORE-4:

```text
1. Main story not obvious within 30 seconds.
2. Page has weak narrative flow.
3. Health Systems Cards appear before Primary finding and why.
4. Too many score families compete without hierarchy.
5. Lead-pattern language repeats across hero, overview, primary finding and patterns.
6. “Strong Signal”, “Vascular Inflammation Risk”, “Trust strip”, and “Why this lead won” sound mechanical or internal.
7. Marker-level “Scored X/100” adds noise in the default marker view.
8. Result versioning status can be incompatible without a visible banner.
```

## Target default page hierarchy

Implement this default sequence unless preflight proves a safer alternative:

```text
1. Hero / main finding
2. Primary finding and why
3. What’s working well
4. Health Systems Cards
5. Patterns across your body
6. Marker-level evidence
7. What to do next
8. Technical / clinician / advanced detail collapsed
```

The current audit identified that `Wave1DomainCards` is rendered before `PrimaryFindingAndWhy`, interrupting the explanation journey. Correct this unless a better Layer B-driven section model already exists.

## Scope

Allowed scope:

1. Reorder results-page sections to create a clearer narrative journey.
2. Merge or suppress repeated hero/body overview/lead-pattern prose.
3. Show stale/incompatible result banner when result versioning metadata indicates either stale or incompatible status.
4. Hide marker-level numeric `Scored X/100` values by default, while preserving them in detail/advanced view.
5. Rename or soften obvious jargon:

   * `Trust strip` → `Data quality`
   * `Why this lead won` → `How confident is this read?`
   * `Strong Signal` → consumer-safe wording such as `Needs attention`, if safe and approved by existing copy pattern
   * `Main system context` → `Most relevant area`
6. Keep advanced/technical sections collapsed by default.
7. Add tests for page order, stale/incompatible banner display, and default hiding of noisy marker scores.
8. Produce a sprint report.

## Backend / Layer B implementation guidance

Prefer backend/DTO support where the change affects interpretation hierarchy.

Allowed Layer B changes include:

```text
- adding section ordering metadata
- adding consumer-safe section labels
- adding result versioning display state
- adding or refining presentation metadata
- producing deduplicated lead summary fields
```

Do not add clinical inference to frontend to compensate for missing backend hierarchy.

If a backend change would require broad narrative compiler redesign, STOP and propose a split.

## Frontend / Layer C implementation guidance

Allowed frontend changes include:

```text
- reordering rendered sections according to approved hierarchy
- moving repeated text into “Read more” / expandable detail
- using approved static UI labels for non-clinical section headings
- rendering stale/incompatible banner
- hiding marker numeric scores by default
- preserving access to detail via existing expand/advanced patterns
```

Frontend must not derive clinical priority from raw marker data, signal IDs, score values, or string matching.

## Stale / incompatible result banner requirement

LAUNCH-CORE-4 found that this analysis has:

```text
result_status: incompatible
regeneration_available: false
```

but no banner was shown because the banner only renders for `result_status === "stale"`.

Fix this.

Required behaviour:

```text
- show the banner for stale results
- show the banner for incompatible results
- use safe user-facing wording
- do not add a regenerate button in this sprint
- do not implement regeneration flow
```

## Score rationalisation requirement

The sprint should not change clinical scoring.

It should clarify presentation.

At minimum:

```text
- hide marker-level “Scored X/100” by default
- keep marker value and status visible
- keep system card scores visible
- keep completeness/reliability visible
- make it clearer that card scores are based on available markers where coverage is limited
```

If score cap / band downgrade policy is required, STOP and classify as product decision. Do not implement score-threshold changes in this sprint.

## Out of scope

Do not:

* implement refresh/regenerate button
* implement regeneration backend flow
* change clinical scoring thresholds
* change rail score calculations
* change biomarker SSOT
* change unit conversion
* modify SignalRegistry
* modify SignalEvaluator
* modify PSI status
* modify root-cause compiler logic
* modify compiled artefact clinical content
* modify package clinical content
* remove clinically meaningful analysis
* introduce frontend clinical inference
* expose raw internal IDs, source traces or compile refs
* introduce fallback parsers

## Required tests

Add or update tests for:

1. Results page renders Primary finding before Health Systems Cards.
2. Stale banner renders for `result_status === "stale"`.
3. Stale/incompatible banner renders for `result_status === "incompatible"`.
4. No regenerate button is introduced.
5. Marker-level numeric `Scored X/100` is hidden by default.
6. Health Systems Card completeness still displays.
7. Role chips remain consumer-safe.
8. Internal source traces remain hidden.
9. ARCH-RT-6 validator still passes.

Run at minimum:

```powershell
python backend/scripts/validate_day_one_architecture.py
python -m pytest backend/tests/architecture/test_day_one_architecture_guardrails.py -q
```

Run relevant frontend tests for touched components.

If no frontend test exists for section order, add one.

## Manual validation target

After implementation, manually inspect:

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
- main story is clearer within first 30 seconds
- Primary finding appears before Health Systems Cards
- repeated lead-pattern copy is reduced
- stale/incompatible banner behaviour is correct where metadata indicates it
- marker numeric scores are not noisy by default
- technical detail remains available
- no internal IDs/traces are visible
```

## STOP conditions

STOP and report if:

1. Required audit files are missing.
2. Completing the sprint requires frontend clinical inference.
3. Completing the sprint requires broad backend narrative compiler redesign.
4. Meaningful analysis would need to be removed rather than collapsed/reordered.
5. Score rationalisation requires changing clinical scoring semantics.
6. Stale/incompatible banner requires implementing regeneration flow.
7. ARCH-RT-6 validator fails.
8. Tests cannot prove the hierarchy and banner changes.

## Required deliverable

Create:

```text
docs/audit-papers/LAUNCH-CORE-5_results_page_narrative_hierarchy_and_score_rationalisation_report.md
```

Report must include:

```text
- issues addressed
- files changed
- Layer B changes
- Layer C changes
- confirmation no analysis was discarded
- before/after section order
- repeated content reduced or moved
- score display changes
- stale/incompatible banner behaviour
- tests run
- manual validation result
- remaining risks / carry-forwards
```

## Evidence required from Cursor

Cursor must report:

```text
1. baseline branch/status evidence
2. authority preflight findings
3. section-order changes
4. Layer B vs Layer C responsibility split
5. files changed
6. tests added/updated
7. test commands run
8. test results
9. manual browser validation result
10. confirmation no clinically meaningful analysis was removed
11. confirmation frontend did not infer clinical meaning
12. confirmation ARCH-RT-6 validator still passes
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

* current branch matches `work/LAUNCH-CORE-5-results-page-narrative-hierarchy-and-score-rationalisation`
* all changed files are tied to this sprint
* no clinical interpretation logic is changed
* no meaningful analysis is removed
* no helper scripts are committed
* no ambiguous stash exists
* latest commit contains only in-scope work

## Success criteria

This sprint is complete only if:

1. Results page has clearer default narrative hierarchy.
2. Primary finding appears before Health Systems Cards.
3. Repeated lead-pattern prose is reduced.
4. Meaningful analysis remains accessible.
5. Marker numeric scores are hidden by default or moved into detail.
6. Stale/incompatible banner behaviour is corrected.
7. Frontend remains presentation-only.
8. ARCH-RT-6 validator passes.
9. Tests prove the main UX changes.
10. Automation Bus gate passes.

```
```
