---
work_id: LC-S9B
branch: launch-core/lc-s9b-proving-closeout
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# LC-S9B — Launch-Core Proving Closeout

## Classification

This is a HIGH-risk MIXED work package.

Reason: this sprint may touch launch-core proving harnesses, behavioural checks, frontend/report carriage, fallback copy, report compilation, context/medication visibility, and regression coverage. These surfaces affect emitted output and launch-core trust.

This sprint is not a broad redesign or WHY Wave 2 expansion.

It is a targeted proving closeout sprint before full Sprint 6 protection.

## Purpose

Close the remaining Sprint 5 launch-core human proving gaps identified in LC-S9.

LC-S8D and FE-S8E have already cleared the unit-governance and Layer C Mode A/B blocker. Do not reopen that work.

This sprint must determine whether the current launch-core personalised pipeline now passes the Sprint 5 bar, and must make only the minimum targeted corrections required to reach a defensible pass/fail decision.

Primary goals:

1. Refresh launch-core proving harness evidence on current `main`.
2. Re-run AB/VR launch-core matrix on the current build.
3. Prove or disprove visible lifestyle payoff.
4. Prove or disprove visible statin/medication payoff.
5. Identify active launch-core leads without governed WHY.
6. Replace unacceptable raw fallback strings on user-facing surfaces with governed, honest fallback copy.
7. Add or complete binary checks for CHECK 2, CHECK 5, and CHECK 6.
8. Produce a named human walkthrough pack for final review.
9. Decide whether Sprint 5 can close as PASS, PASS_WITH_GAPS, or FAIL.

## Governing context

Read these files before editing anything:

```text
docs/planning-papers/healthiq_launch_core_transformation_plan_FINAL.md
docs/audit-papers/LC-S9_launch_core_human_proving_closeout_review.md
docs/audit-papers/lc_s5_proving_readiness_preflight_audit.md
docs/audit-papers/launch-core-proving/PROVING_REPORT.md
docs/audit-papers/launch-core-proving/latest_fingerprints.json
docs/audit-papers/LAUNCH_GRADE_ANALYTICAL_GAP_MAP_2026-05.md

docs/audit-papers/LC-S8D_uk_si_unit_governance_remediation_notes.md
docs/audit-papers/FE-S8E_post_merge_comparison_uat.md
````

If any file path differs, locate the actual file and record it in the sprint notes.

## Mandatory architectural boundaries

The launch-core plan remains governing:

* prove the real production path, not demo-only pathways
* do not broaden the questionnaire
* do not expand full WHY Wave 2
* do not build temporary narrative bridges
* do not add LLM reasoning to the analytical core
* do not change unit-governance or Phase B conversion state
* do not reopen LC-S8D or FE-S8E unless a direct regression is proven

Layer B produces governed structured truth.

Layer C may translate or polish governed payloads, but must not invent analytical reasoning.

## Mandatory preflight before editing

Run and record:

```powershell
git branch --show-current
git status --short
git log --oneline -n 5
```

Then verify:

```powershell
Test-Path automation_bus/state/work_package_active.json
```

Read `automation_bus/state/work_package_active.json` and confirm:

* `work_id` is `LC-S9B`
* branch is `launch-core/lc-s9b-proving-closeout`

If the token is missing or mismatched, STOP:

```text
Kernel start not executed or work package mismatch.
```

## Authority preflight

Before modifying files, identify and record the authoritative paths for:

1. launch-core proving harness
2. AB/VR fixture definitions
3. questionnaire/profile fixtures
4. statin/medication/intervention fixture source
5. lifestyle modifier source
6. root-cause / WHY compiler or fallback source
7. report compiler / primary hero payload source
8. frontend results surface consuming the relevant fields
9. existing CHECK 2 / CHECK 5 / CHECK 6 logic, if present

STOP if any authority path is ambiguous or duplicated.

Do not create a second authority source.

## Potentially allowed files

Only edit files required to close the LC-S9 gaps.

Potentially allowed:

```text
backend/core/analytics/**/*
backend/core/contracts/**/*
backend/core/pipeline/**/*
backend/ssot/lifestyle_registry.yaml
backend/ssot/questionnaire.json
backend/ssot/display_unit_policy.yaml
backend/tests/**/*

frontend/app/(app)/results/**/*
frontend/app/components/**/*
frontend/app/types/**/*
frontend/app/lib/**/*
frontend/tests/**/*

docs/audit-papers/launch-core-proving/**/*
docs/audit-papers/LC-S9B_launch_core_proving_closeout_notes.md
docs/audit-papers/LC-S9B_human_walkthrough_pack.md
```

Only touch `backend/ssot/lifestyle_registry.yaml` or `backend/ssot/questionnaire.json` if the sprint proves that visible lifestyle payoff cannot work because the existing governed mapping is incomplete or broken.

## Forbidden files and changes

Do not edit:

```text
backend/ssot/biomarkers.yaml
backend/ssot/units.yaml
backend/ssot/scoring_policy.yaml
backend/core/units/registry.py
backend/core/scoring/rules.py
backend/core/canonical/hba1c_layer_b_arbitration.py
backend/scripts/run_work_package.py
backend/scripts/golden_gate_local.py
backend/scripts/update_cursor_status.py
automation_bus/latest_gate_evidence.json
automation_bus/latest_gate_output.txt
automation_bus/latest_cursor_status.json
```

Do not:

* introduce fallback parsers
* change canonical units
* change Phase B unit conversions
* perform frontend unit conversions
* broaden medication coverage beyond the bounded statin proving path
* broaden questionnaire scope
* add generic placeholder narrative
* hide failed checks by suppressing outputs
* treat stale proving artefacts as current evidence

## Phase gates

This sprint has five internal phases.

Each phase must update:

```text
docs/audit-papers/LC-S9B_launch_core_proving_closeout_notes.md
```

Each phase checkpoint must record:

* command(s) run
* files inspected
* findings
* failures
* changes made, if any
* whether the next phase is safe to enter

---

# Phase 1 — Refresh current proving evidence

## Required work

Run the current launch-core proving harness on the current branch.

Locate and run the canonical harness. Likely candidates include files under:

```text
docs/audit-papers/launch-core-proving/
backend/tests/
scripts/
```

If no runnable harness exists, STOP and record the exact missing harness path / missing command.

Refresh or regenerate, as appropriate:

```text
docs/audit-papers/launch-core-proving/PROVING_REPORT.md
docs/audit-papers/launch-core-proving/latest_fingerprints.json
```

Do not manually edit generated evidence unless the harness explicitly writes it.

## Required checks

The refreshed proving evidence must include, or explicitly state absence of:

* AB baseline
* AB lifestyle_context
* AB statin_off
* AB statin_on
* VR baseline
* VR lifestyle_context
* VR statin_off
* VR statin_on

For each run capture:

* lead finding / primary concern
* runner-up if present
* clinician report primary finding
* retail summary lead
* narrative body or governed payload summary
* lifestyle context presence
* statin/medication intervention presence
* fingerprints for deterministic comparison

## Phase 1 STOP conditions

STOP if:

* harness cannot be located
* harness cannot run on current branch
* regenerated artefacts are non-deterministic across identical inputs
* AB/VR fixtures are missing
* statin/lifestyle fixtures are missing
* the current branch is not the declared LC-S9B branch

---

# Phase 2 — Binary CHECK automation

## Required work

Implement or complete binary checks required by LC-S9:

```text
CHECK 2 — lifestyle visible payoff
CHECK 4 — statin/medication intervention presence and bounded isolation
CHECK 5 — no band/headline polarity contradiction
CHECK 6 — primary_concern and retail_summary agree on same lead
```

If CHECK 4 already exists and passes, document it rather than rewriting it.

The checks must operate on the real launch-core proving outputs, not hardcoded demo strings.

## Expected pass/fail behaviour

CHECK 2 must fail if lifestyle_context produces no user-visible difference.

CHECK 4 must fail if statin_on/statin_off does not change or caveat at least one relevant user-visible field where the intervention is expected to matter, while preserving analytical invariants where required.

CHECK 5 must fail if any launch-core surface says a marker/system is reassuring while another surface says it is concerning for the same lead without explanation.

CHECK 6 must fail if the hero/primary concern and retail summary disagree on the lead finding.

## Phase 2 STOP conditions

STOP if:

* a check can pass without reading real proving outputs
* a check depends on stale fingerprints
* a check is implemented as string theatre rather than contract verification
* the only way to pass is to hide a problematic surface

---

# Phase 3 — WHY / fallback trust correction

## Required work

Inspect current proving outputs for active lead findings without governed WHY or acceptable fallback.

Specifically check for raw or unacceptable copy such as:

```text
No governed WHY for signal_...
```

If present on user-facing surfaces, replace with governed, honest fallback copy that:

* does not pretend to know a causal mechanism
* does not use internal signal IDs
* explains that the system has detected a pattern but lacks enough governed evidence to provide a deeper causal explanation
* directs the user to the relevant missing-data or clinician-context framing where appropriate
* remains deterministic and source-controlled

## Preferred fix hierarchy

1. If a governed WHY asset already exists but is not being loaded, fix the loader/wiring.
2. If no governed WHY exists and the signal is inside the launch-core lead set, use a governed fallback template.
3. If the signal is outside the launch-core lead set and should not be surfaced as primary, document and gate it from key launch-core ranking surfaces only if this is already allowed by policy.

Do not create new clinical WHY claims in this sprint unless the governed source already exists.

## Phase 3 STOP conditions

STOP if:

* fixing the issue requires new clinical research or new WHY asset creation
* fallback copy would become speculative
* internal signal IDs remain visible in consumer hero/report surfaces
* suppression would hide clinically relevant findings without policy authority

---

# Phase 4 — Visible lifestyle/statin payoff verification

## Required work

Using the refreshed harness outputs and browser/API inspection where possible, verify whether:

1. lifestyle_context changes at least one user-visible field compared with baseline
2. alcohol/lifestyle bridge appears in user-readable language when active
3. statin_on/statin_off changes or caveats at least one relevant user-visible field
4. statin behaviour is bounded and does not alter raw biomarker chemistry incorrectly
5. medication handling remains caveat/modifier-based, not drug-library reasoning

If the behaviour does not visibly differ, implement the smallest correction only if the architecture already supports the modifier but it is not surfaced.

If architecture support is missing, STOP and record a blocker instead of inventing a new modifier system.

## Phase 4 STOP conditions

STOP if:

* lifestyle/stain payoff requires broad questionnaire expansion
* statin support would require building a broad drug database
* medication logic changes analytical thresholds without explicit governed authority
* visibility is created with fake or demo-only copy

---

# Phase 5 — Human walkthrough pack and closeout decision

## Required work

Create:

```text
docs/audit-papers/LC-S9B_human_walkthrough_pack.md
```

The pack must allow a named human tester to review:

* AB baseline
* AB lifestyle_context
* AB statin_off
* AB statin_on
* VR baseline
* VR lifestyle_context
* VR statin_off
* VR statin_on

For each scenario include:

* report URL or command to generate report
* expected lead finding
* expected visible lifestyle/statin behaviour
* known acceptable caveats
* pass/fail checklist
* screenshots or payload excerpts if available
* binary CHECK results

## Required final closeout decision

Update:

```text
docs/audit-papers/LC-S9B_launch_core_proving_closeout_notes.md
```

with one of:

```text
SPRINT_5_PASS
SPRINT_5_PASS_WITH_GAPS
SPRINT_5_FAIL
```

If not `SPRINT_5_PASS`, state the exact next blocker and recommended next work package.

## Phase 5 STOP conditions

STOP if:

* human walkthrough cannot be performed because reports cannot be generated
* the pack lacks enough evidence for human review
* CHECK 2/4/5/6 are not present or not executable
* generated evidence is stale or not tied to current commit

---

# Required validation commands

Run relevant targeted tests and harness commands discovered during preflight.

At minimum, run:

```powershell
python -m pytest backend/tests -q
```

If full backend tests are too broad or fail due to unrelated known debt, run the smallest targeted launch-core proving/check test suite and document why.

Run frontend validation if frontend files are changed:

```powershell
npm run type-check
npm run test
npm run lint
```

If commands do not exist or fail due to known environment debt, record the exact output.

Run no-forbidden-unit-regression scan if frontend files are changed:

```powershell
Select-String -Path frontend/app/**/*.ts,frontend/app/**/*.tsx -Pattern "0.055|0.0555|18.018|38.67|88.4|0.02586|mg_dL|mmol_L|convert" -CaseSensitive:$false
```

Review all hits.

## Required documentation outputs

Create or update only as justified:

```text
docs/audit-papers/LC-S9B_launch_core_proving_closeout_notes.md
docs/audit-papers/LC-S9B_human_walkthrough_pack.md
docs/audit-papers/launch-core-proving/PROVING_REPORT.md
docs/audit-papers/launch-core-proving/latest_fingerprints.json
```

If code changes are made, the notes file must include:

* files changed
* reason for each change
* phase mapping
* tests run
* before/after evidence
* residual risk

## Acceptance criteria

The work package is complete only if:

* current proving artefacts are refreshed or the missing harness is explicitly documented as a blocker
* CHECK 2, CHECK 4, CHECK 5, and CHECK 6 are implemented or explicitly shown to already exist and pass
* AB/VR launch-core matrix is evaluated on the current build
* visible lifestyle payoff is proven or explicitly fails
* visible statin payoff is proven or explicitly fails
* user-facing raw fallback strings are removed or explicitly blocked for policy reasons
* no demo-only narrative is introduced
* no broad WHY expansion occurs
* no Phase B unit work occurs
* a human walkthrough pack is created
* the final Sprint 5 verdict is explicit

## Cursor completion requirements

When implementation is complete, Cursor must:

1. Run the validation commands relevant to changed files.
2. Update required documentation outputs.
3. Run closure audit:

```powershell
git branch --show-current
git status --short
git log --oneline -n 5
git diff --name-only
git diff --cached --name-only
git stash list
```

4. Classify:

   * tracked modified files
   * staged files
   * untracked files
   * tooling files
   * out-of-scope files
   * stash entries
5. STOP if unrelated files, tooling leakage, dirty branch ambiguity, or stash ambiguity exists.
6. If closure is clean, run:

```powershell
python backend/scripts/run_work_package.py finish
```

7. Report whether finish completed or failed.
8. Do not merge.
9. Do not create `automation_bus/latest_audit_summary.md`.
10. Do not claim final approval.

## Explicit non-authority statement

Cursor implements and reports only.

Cursor may not self-certify Sprint 5 closure, Sprint 6 authorisation, architecture correctness, merge readiness, or final approval.

````