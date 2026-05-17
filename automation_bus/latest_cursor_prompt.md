---
work_id: LC-S10B
branch: launch-core/lc-s10b-protect-proven-launch-core-slice
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# LC-S10B — Protection of the Proven Launch-Core Slice

## Classification

This is a HIGH-risk MIXED protection sprint.

Reason: this work may touch regression tests, proving harnesses, Sentinel packs, frontend protection checks, backend launch-core report tests, fingerprint generation, and guardrail logic. These protect launch-core analytical and narrative behaviour.

This sprint is protection only.

It must not expand product scope, add new clinical reasoning, alter scoring, alter units, broaden the questionnaire, or build new user-facing features.

## Current programme state

Sprint 5 has been accepted as:

```text
SPRINT_5_PASS_WITH_GAPS
````

This is sufficient to progress into Sprint 6 protection, but it is not an unconditional launch PASS.

The following workstreams are now considered proven enough to protect:

* LC-S8D — UK/SI unit governance remediation
* FE-S8E — uploaded-panel fidelity / Layer C Mode A rendering
* LC-S9B — launch-core proving closeout checks
* LC-S9C — lifestyle visibility and copy hardening

The purpose of this sprint is to turn those proven behaviours into durable regression/Sentinel/fingerprint protection so future work cannot silently break them.

## Strategic rule

Do not document status for its own sake.

Do not create passive decision artefacts.

Any knowledge recorded in this sprint must be consumed by tests, Sentinel, harnesses, fingerprints, CI checks, or operational validation.

Audit notes are allowed only to explain what was protected and how.

## Governing evidence to read first

Read these before editing anything:

```text
docs/planning-papers/healthiq_launch_core_transformation_plan_FINAL.md

docs/audit-papers/LC-S9_launch_core_human_proving_closeout_review.md
docs/audit-papers/LC-S9B_launch_core_proving_closeout_notes.md
docs/audit-papers/LC-S9B_human_walkthrough_pack.md

docs/audit-papers/launch-core-proving/PROVING_REPORT.md
docs/audit-papers/launch-core-proving/latest_fingerprints.json

docs/audit-papers/FE-S8E_post_merge_comparison_uat.md
docs/audit-papers/FE-S8E_uploaded_panel_fidelity_uat_notes.md

docs/audit-papers/LC-S8D_uk_si_unit_governance_remediation_notes.md
docs/audit-papers/LC-S8D_frontend_layer_c_uat_report.md
```

If any path differs, locate the actual file and record the real path in the sprint notes.

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

* `work_id` is `LC-S10B`
* branch is `launch-core/lc-s10b-protect-proven-launch-core-slice`

If the token is missing or mismatched, STOP:

```text
Kernel start not executed or work package mismatch.
```

## Authority preflight

Before modifying files, identify and record the authoritative paths for:

1. launch-core proving harness
2. launch-core fingerprints
3. CHECK 2 / 4 / 5 / 6 regression tests
4. Sentinel pack registry
5. existing unit-governance Sentinel pack
6. frontend uploaded-panel fidelity tests or equivalent protection route
7. root-cause fallback tests
8. lifestyle-visible-payoff tests
9. statin bounded-intervention tests
10. Layer B → Layer C report contract tests

STOP if any authority is ambiguous or duplicated.

Do not create a second authority source.

## Additional hardening requirements

### CHECK 4 specificity

CHECK 4 must not only verify that an intervention is present.

It must specifically assert:

```text
lipid_lowering_statin
```

is present in the statin_on intervention classes and absent from statin_off.

Required protection:

```text
statin_off: intervention present = false and lipid_lowering_statin absent
statin_on: intervention present = true and lipid_lowering_statin present
```

CHECK 4 must fail unless:

* statin_on contains the specific intervention class `lipid_lowering_statin`
* statin_off does not contain `lipid_lowering_statin`
* analytical invariants are preserved
* cardiovascular consequence sentence visibly changes on statin_on
* statin copy does not claim scoring or ranking changed

### Frontend protection reality

There are currently no established frontend unit/integration tests outside existing repo tooling.

Do not create a new frontend testing architecture in this sprint unless a direct protection gap cannot otherwise be covered.

For this sprint, frontend protection may be satisfied by:

* existing LC-S8D Sentinel guardrails
* backend regression tests over payload/contract behaviour
* no-conversion static scan
* proving-harness evidence
* documented browser/UAT evidence already produced by FE-S8E

If frontend files are not changed, do not run `npm run test` merely to create noise.

If frontend files are changed, run available frontend validation commands and document if no test command exists or if existing environment debt prevents execution.

### Fingerprint field dependency

During Phase 2 authority preflight, explicitly confirm that:

```text
docs/audit-papers/launch-core-proving/latest_fingerprints.json
```

contains `consumer_domain_rows` for each AB/VR run.

If `consumer_domain_rows` is absent, STOP and report because CHECK 4 and CHECK 5 cannot be properly protected from compact fingerprints alone.

## Proven behaviours to protect

This sprint must protect the behaviours below.

### A. Unit-governance behaviours from LC-S8D

Protect:

* HbA1c has one analytical identity.
* HbA1c `%` must not be separately scored.
* HbA1c Layer B uses `mmol/mol`.
* Haematocrit Layer B uses `L/L`.
* Haematocrit must never render or score as `0.438 %`.
* Platelets and WBC treat `K/uL` / `K/μL` as equivalent to `10^9/L`.
* Sodium, potassium, and chloride treat `mEq/L` as equivalent to `mmol/L`.
* BUN maps to urea, not urate.
* Uric acid / urate remains separate from urea.
* Frontend must not perform unit conversions.

### B. Layer C Mode A from FE-S8E

Protect:

* `meta.upload_panel_observations` is consumed by the frontend.
* Uploaded source observations are visible.
* HbA1c `%` appears as uploaded/equivalent when present.
* Equivalent uploaded observations are not injected into analytical dials.
* Canonical dials continue to use `biomarkers[]`.
* Uploaded-panel fidelity remains renderer-only.

### C. Layer C Mode B analytical collapse

Protect:

* equivalent biomarkers collapse for analytical interpretation
* narrative/report does not duplicate HbA1c `%` and `mmol/mol`
* analytical surfaces use canonical identity and governed unit
* uploaded-panel provenance does not contaminate scoring or ranking

### D. Lifestyle-visible payoff from LC-S9C

Protect:

* AB and VR lifestyle_context scenarios show the plain-English alcohol / one-carbon / homocysteine sentence in `body_overview`
* baseline scenarios do not show that sentence
* internal slug `alcohol_intake_moderate_or_higher_with_one_carbon_lab_coherence` never appears in user-facing narrative fields
* lifestyle copy is visible without requiring the user to reach the end of a long lead narrative
* scoring and ranking are unchanged by the lifestyle copy

### E. Statin bounded modifier behaviour from LC-S9B

Protect:

* statin_off has no intervention object
* statin_off does not contain `lipid_lowering_statin`
* statin_on has `lipid_lowering_statin`
* statin_on/off preserve analytical invariants
* top findings remain stable
* signal states remain stable
* consumer band labels remain stable
* statin_on visibly changes or caveats the cardiovascular consequence sentence
* statin copy remains bounded and does not imply scoring was changed

### F. WHY fallback safety

Protect:

* no user-facing field shows `No governed WHY for signal_...`
* no user-facing field exposes raw `signal_*` IDs
* fallback title remains plain English:
  `Pattern noted — deeper causal explanation not yet available`
* fallback copy remains non-speculative
* fallback confidence remains unchanged
* fallback routing/ranking logic is not altered

### G. Launch-core CHECKs

Protect:

* CHECK 2 — lifestyle visible payoff
* CHECK 4 — statin bounded intervention with specific `lipid_lowering_statin` class assertion
* CHECK 5 — no band/consequence polarity contradiction
* CHECK 6 — primary concern and retail summary lead alignment

These must be executable on current proving outputs.

## Explicit non-scope

Do not do any of the following:

* Phase B true unit conversions
* Phase B evidence gathering
* broad WHY Wave 2 expansion
* broad medication ontology
* questionnaire expansion
* frontend redesign
* new clinical claims
* IDL consumer expansion
* PDF redesign
* generic narrative rewrite
* demo-only logic
* fake fixture-only shortcuts
* hiding failed findings
* suppressing outputs to pass tests
* adding fallback parser logic

## Potentially allowed files

Only edit files required for protection.

Potentially allowed:

```text
backend/tests/regression/**/*
backend/tests/unit/**/*
backend/tests/fixtures/**/*
backend/tools/launch_core_proving_harness.py

sentinel/packs/**/*
sentinel/**/*

frontend/tests/**/*
frontend/app/lib/**/*
frontend/app/components/**/*
frontend/app/(app)/results/**/*

docs/audit-papers/launch-core-proving/PROVING_REPORT.md
docs/audit-papers/launch-core-proving/latest_fingerprints.json
docs/audit-papers/LC-S10B_protection_of_proven_slice_notes.md
```

Code under `backend/core/**` or `frontend/app/**` may be edited only if a protection test exposes a real defect in the already-proven behaviour. Do not alter behaviour just to make tests easier.

## Forbidden files

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

## Phase 1 — Protection inventory

Create or update:

```text
docs/audit-papers/LC-S10B_protection_of_proven_slice_notes.md
```

Record:

* current branch / git state
* authority paths found
* existing tests that already protect each proven behaviour
* gaps where protection is missing
* proposed protection mechanism for each gap

Do not implement until this inventory is complete.

Required output table:

| Behaviour | Existing protection | Gap | Planned protection |
| --------- | ------------------- | --- | ------------------ |

## Phase 2 — Protect launch-core proving matrix

Ensure the launch-core proving harness and regression tests protect:

* AB baseline
* AB lifestyle_context
* AB statin_off
* AB statin_on
* VR baseline
* VR lifestyle_context
* VR statin_off
* VR statin_on

For each scenario, the protected fingerprint must include enough information to detect drift in:

* lead finding
* top findings order
* primary concern head
* retail summary head
* body overview head
* lead narrative head
* cardiovascular consequence sentence
* intervention classes
* consumer band labels
* internal fallback leakage
* `consumer_domain_rows`

If the existing fingerprints already contain these fields, document and test them.

If not, extend the harness output minimally.

STOP if the harness becomes non-deterministic.

## Phase 3 — Protect CHECK 2 / 4 / 5 / 6

Ensure regression tests exist and pass for:

### CHECK 2 — Lifestyle visible payoff

Must assert:

* baseline AB/VR do not include the lifestyle sentence
* lifestyle_context AB/VR include the plain-English lifestyle sentence in body overview
* internal lifestyle slug is absent from user-facing fields
* lifestyle_context narrative/body differs from baseline in a user-visible way

### CHECK 4 — Statin bounded intervention

Must assert:

* statin_off has no statin intervention
* statin_off does not contain `lipid_lowering_statin`
* statin_on has `lipid_lowering_statin`
* analytical invariants are preserved between statin_off and statin_on
* cardiovascular consequence sentence differs on statin_on
* statin copy does not claim scoring/ranking changed

### CHECK 5 — Band/consequence polarity

Must assert:

* no reassuring headline contradicts a concerning band
* no urgent/alarming wording is attached to stable bands
* launch-core surfaces are internally coherent

### CHECK 6 — Lead alignment

Must assert:

* primary concern and retail summary point to the same lead family
* AB/VR baseline remain homocysteine-led unless a future governed change updates the expected fingerprint intentionally

## Phase 4 — Protect unit and Layer C behaviours

Ensure regression/Sentinel/frontend-equivalent tests protect:

* HbA1c single analytical identity
* haematocrit `L/L`
* BUN→urea and urate separation
* uploaded-panel fidelity section
* HbA1c `%` visible only as uploaded/equivalent
* canonical dials from `biomarkers[]`
* frontend no conversion maths
* no duplicate equivalent analytical findings

If these already exist from LC-S8D/FE-S8E, do not duplicate unnecessarily. Add only missing coverage.

Frontend-specific protection does not require new frontend test infrastructure unless a clear gap cannot be protected through existing Sentinel/backend regression/static scan routes.

## Phase 5 — Sentinel promotion

Review whether any existing placeholder/status checks should become real blockers for the proven slice.

At minimum, assess:

* unit-governance Sentinel pack
* frontend no unit repair
* WHY fallback leakage
* lifestyle slug leakage
* CHECK 2/4/5/6 protection

If a Sentinel rule can be safely added without creating false positives, add it.

If not appropriate, document why pytest/regression/static-scan protection is sufficient for this sprint.

Do not create broad Sentinel Phase 2.

## Phase 6 — Final proof run

Run the refreshed proving harness and targeted test suite.

Required commands:

```powershell
python backend/tools/launch_core_proving_harness.py
python -m pytest backend/tests/regression/test_lc_s5_proving_checks.py -q
python -m pytest backend/tests/regression/test_lc_s8d_unit_governance_sentinel.py -q
python -m pytest backend/tests/unit/test_hba1c_governance.py -q
```

Run frontend validation only if frontend files are changed:

```powershell
npm run type-check
npm run test
```

If commands do not exist or fail due to known unrelated debt, record exact output and whether it blocks this sprint.

Run frontend no-conversion scan if frontend files are changed:

```powershell
Select-String -Path frontend/app/**/*.ts,frontend/app/**/*.tsx -Pattern "0.055|0.0555|18.018|38.67|88.4|0.02586|mg_dL|mmol_L|convert" -CaseSensitive:$false
```

Review all hits.

## Acceptance criteria

This sprint is complete only if:

* launch-core matrix protection exists for AB/VR baseline/lifestyle/statin scenarios
* `consumer_domain_rows` presence is verified in fingerprints where required by CHECK 4 / CHECK 5
* CHECK 2 / 4 / 5 / 6 are protected and passing
* CHECK 4 specifically verifies `lipid_lowering_statin`, not merely generic intervention presence
* lifestyle visible payoff is protected
* statin bounded intervention is protected
* unit-governance behaviours remain protected
* uploaded-panel fidelity remains protected
* no internal lifestyle rule slug can leak into user-facing fields
* no raw `signal_*` / `No governed WHY for signal_...` fallback can leak into user-facing fields
* proving fingerprints are refreshed on current code
* Sprint 6 protection notes state exactly what is now protected
* no feature expansion has occurred

## Required documentation output

Create or update:

```text
docs/audit-papers/LC-S10B_protection_of_proven_slice_notes.md
```

It must include:

1. protection inventory
2. files changed
3. tests added/updated
4. Sentinel changes, if any
5. proving harness result
6. refreshed fingerprint stamp/SHA
7. known deferred gaps
8. final protection verdict

This document is not a passive status artefact. It must map directly to tests and guards created or verified in this sprint.

## Cursor completion requirements

When implementation is complete, Cursor must:

1. Run required validation commands.
2. Update the protection notes.
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

Cursor implements and reports protection only.

Cursor may not self-certify Sprint 6 completion, launch readiness, architecture correctness, merge readiness, or final approval.

````