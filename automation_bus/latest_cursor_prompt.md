---
work_id: LAUNCH-CORE-2_multi_panel_launch_readiness_uat
branch: work/LAUNCH-CORE-2-multi-panel-launch-readiness-uat
risk_level: STANDARD
execution_model: TWO_PHASE_START_FINISH
change_type: CONTENT
---

# LAUNCH-CORE-2 — Multi-Panel Launch Readiness UAT

## Purpose

Run a broader launch-readiness UAT pass across multiple analysis results to confirm the post-ARCH-RT and LAUNCH-CORE-1 results page is stable across different blood panels.

This is an investigation/audit sprint only.

Do not modify production code, compiled artefacts, backend logic, frontend components, schemas, packages, investigation specs, or tests unless explicitly approved after the audit.

## Baseline requirement

Start from clean `main`.

Before creating or switching branch, run and report:

```powershell
git branch --show-current
git status --short
git log --oneline -n 10
git rev-parse HEAD
git rev-parse origin/main
````

STOP if:

* current branch is not `main`
* local `main` does not equal `origin/main`
* working tree is not clean
* LAUNCH-CORE-1 is not merged
* untracked or uncommitted files are present

## Standard rules

This work remains governed by the standard Knowledge Bus and Automation Bus SOPs already active in the repository.

Do not re-read SOPs unless the applicable governance requirement cannot be located.

## Context

Recent UAT confirmed LAUNCH-CORE-1 fixed the main results-page defects:

* card summary completeness now aligns with expanded subsystem detail
* role chips use consumer-safe wording
* “Homocysteine Elevation Context” no longer appears in the UI
* MCV displays correctly
* mojibake is not visible in rendered body text
* ARCH-RT-6 validator passes

Remaining reservations are mostly polish/hygiene:

* “Vascular Inflammation Risk” may still read like an internal construct
* “Strong Signal” may feel mechanical
* raw Homocysteine wording and mojibake still exist in API payload but are scrubbed from UI
* 100/100 score with limited reliability remains a product judgement issue
* HbA1c upload-fidelity wording may need softer alignment

## Target analyses

Use the following known analysis IDs first:

```text
18e14232-9f93-45e6-820c-004ab5a16235
746f2b0a-b470-4d87-8ed8-e2c3d1e68c02
```

Also identify and test at least one additional recent analysis result if available locally.

If no additional analysis is available, report that and continue with the two known analyses.

Login:

```text
test-user3@example.com
Subaru@555
```

Base URL:

```text
http://localhost:3000/results?analysis_id=<analysis_id>
```

## Required checks per analysis

For each analysis:

1. Open the results page in browser.
2. Capture screenshots of:

   * hero / main summary
   * all expanded Health Systems Cards
   * primary finding / why section
   * interpretation patterns if present
3. Inspect console errors/warnings.
4. Fetch and inspect API payload:

   * `GET /api/analysis/result?analysis_id=<analysis_id>`
5. Confirm all Health Systems Cards:

   * render correctly
   * show summary completeness matching expanded subsystem included/missing markers
   * do not show false-missing markers
   * do not show raw internal IDs
   * do not show raw source traces
   * do not show raw marker-role enums
6. Confirm all Wave 1 subsystems use compiled card evidence.
7. Confirm `total_bilirubin` is not reintroduced as an expected missing marker.
8. Confirm consumer-facing text does not show:

   * `signal_*`
   * `pkg_*`
   * `wave1_*`
   * `source_trace`
   * `compile_manifest_ref`
   * `artefact_id`
   * `source_spec_id`
   * `activation_key`
   * raw snake_case marker roles
9. Confirm known copy fixes:

   * no visible “Homocysteine Elevation Context”
   * MCV displays as `MCV`
   * no mojibake characters such as `â`
   * role chips use consumer-safe wording
10. Record any remaining visible wording that feels mechanical, confusing, contradictory, or unlaunchworthy.

## Required validator checks

Run:

```powershell
python backend/scripts/validate_day_one_architecture.py
python -m pytest backend/tests/architecture/test_day_one_architecture_guardrails.py -q
```

If frontend tests are available and quick, also run the relevant results-page/component tests from LAUNCH-CORE-1.

## Required deliverable

Create:

```text
docs/audit-papers/LAUNCH-CORE-2_multi_panel_launch_readiness_uat.md
```

The report must include:

* overall verdict:

  * `PASS`
  * `PASS_WITH_RESERVATIONS`
  * `FAIL`
* analysis IDs tested
* screenshots or screenshot references
* console/network findings
* card completeness table per analysis
* subsystem included/missing comparison per analysis
* false-missing marker check
* internal ID visibility check
* copy/prose issues found
* severity of each issue:

  * blocker
  * launch polish
  * post-launch hygiene
* recommended next action:

  * no fix needed
  * fix before launch
  * post-launch backlog
  * needs product decision
* tests/validators run and results

## Out of scope

Do not:

* modify production code
* modify frontend components
* modify backend logic
* modify compiled artefacts
* modify package files
* modify investigation specs
* modify schemas
* modify tests
* change scoring logic
* change clinical thresholds
* change copy unless explicitly approved later

## STOP conditions

STOP and report if:

1. app cannot be accessed
2. login fails
3. API payload cannot be fetched
4. results page fails to render
5. ARCH-RT-6 validator fails
6. a launch-blocking clinical display defect is found
7. a false-missing marker defect is found
8. raw internal IDs/source traces are visible to users

## Evidence required from Cursor

Cursor must report:

1. baseline branch/status evidence
2. analyses tested
3. browser screenshots captured
4. console/network findings
5. API payload inspection summary
6. card-by-card findings
7. defects found and severity
8. validator/test commands run
9. validator/test results
10. final launch-readiness recommendation

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

* current branch matches `work/LAUNCH-CORE-2-multi-panel-launch-readiness-uat`
* only the audit report and expected screenshot/API artefacts are changed
* no production code is changed
* no helper scripts are committed
* no ambiguous stash exists

## Success criteria

This sprint is complete only if:

1. at least two analyses are manually audited
2. card completeness matches expanded subsystem evidence on tested analyses
3. no false-missing marker defects are found
4. no raw internal IDs/source traces are visible
5. ARCH-RT-6 validator passes
6. findings are classified by severity
7. clear launch-readiness recommendation is produced

```
```
