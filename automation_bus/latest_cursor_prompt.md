---
work_id: LC-S8D
branch: launch-core/lc-s8d-uk-si-unit-governance-remediation
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# LC-S8D — UK/SI Unit Governance Remediation

## Classification

This is a HIGH-risk MIXED work package.

Reason: this work may touch SSOT, unit registry, scoring policy, canonicalisation, Layer B scoring behaviour, backend display contracts, tests, and Sentinel guardrails. These surfaces can affect analytical correctness and emitted output.

This is one controlled HIGH-risk remediation sprint with internal phase gates.

It is not permission for an uncontrolled “fix all unit problems” pass.

## Purpose

Remediate the UK/SI unit-governance defects identified in LC-S8C-PREFLIGHT while preserving deterministic analytical behaviour.

Primary goals:

1. Implement safe Phase A unit equivalences.
2. Align SSOT unit labels only where safe and evidence-authorised.
3. Prevent Layer B from scoring unknown, mixed, or incoherent units.
4. Migrate Layer B scoring units only where authorised by evidence and phase gates.
5. Introduce a governed Layer C display policy model.
6. Preserve uploaded-panel fidelity for biomarker dials/upload review.
7. Collapse duplicate-equivalent biomarkers for Layer B and analytical-report interpretation.
8. Add regression tests for remediated unit paths.
9. Add Sentinel guardrails only after the relevant implementation phase is stable.

## Governing authority

Read these files before editing anything:

```text
docs/audit-papers/LC-S8C_ssot_wide_unit_governance_preflight.md
docs/audit-papers/LC-S8B_uk_canonical_unit_policy_validation.md
docs/audit-papers/LC-S8C_pre_sprint_unit_policy_validation_note.md

architecture/Master_PRD_v5.2.md
architecture/ADR-001-platform-non-negotiables.md
architecture/ADR-002-deterministic-analysis-engine.md

backend/ssot/biomarkers.yaml
backend/ssot/units.yaml
backend/ssot/scoring_policy.yaml
backend/ssot/biomarker_alias_registry.yaml
backend/ssot/system_burden_registry.yaml

backend/core/units/registry.py
backend/core/canonical/hba1c_layer_b_arbitration.py
````

If any path differs on the current branch, STOP and report the actual path before making changes.

LC-S8C-PREFLIGHT is a working architectural basis only. It is not final clinical evidence authority.

Do not treat any `REPO_POLICY_ONLY`, `CATEGORY_EVIDENCE_CITED`, or `BLOCKED_PENDING_EVIDENCE` row as final clinical proof unless the phase rules below explicitly allow that limited action.

## Architectural model

HealthIQ must preserve this boundary:

```text
raw uploaded biomarker + raw uploaded unit
→ Layer A canonicalisation and unit normalisation
→ Layer B calculation using one governed canonical analytical unit
→ Layer C governed presentation/display conversion
```

Layer C and frontend must not repair, infer, calculate, or clinically normalise units.

Frontend is renderer-only.

No fallback parser may be introduced.

No hidden conversion logic may be added to frontend code.

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

* `work_id` is `LC-S8D`
* branch is `launch-core/lc-s8d-uk-si-unit-governance-remediation`

If the token is missing or mismatched, STOP:

```text
Kernel start not executed or work package mismatch.
```

Before modifying files, confirm:

1. The authoritative biomarker SSOT is `backend/ssot/biomarkers.yaml`.
2. The authoritative unit registry data is `backend/ssot/units.yaml`.
3. The runtime unit normaliser is `backend/core/units/registry.py`.
4. The scoring bands are loaded from `backend/ssot/scoring_policy.yaml`.
5. No duplicate SSOT/unit/scoring authority exists for the same domain.

If any authority ambiguity exists, STOP and report it.

## Potentially allowed files

Only edit files required for authorised phase work.

Potentially allowed:

```text
backend/ssot/biomarkers.yaml
backend/ssot/units.yaml
backend/ssot/scoring_policy.yaml
backend/ssot/biomarker_alias_registry.yaml
backend/ssot/system_burden_registry.yaml
backend/ssot/display_unit_policy.yaml

backend/core/units/registry.py
backend/core/canonical/hba1c_layer_b_arbitration.py
backend/core/**/*
backend/app/**/*
backend/tests/**/*

frontend/app/types/**/*
frontend/app/queries/**/*
frontend/app/services/**/*
frontend/app/components/**/*
frontend/app/(app)/results/**/*

sentinel/packs/**/*
sentinel/**/*

docs/audit-papers/LC-S8D_uk_si_unit_governance_remediation_notes.md
```

Frontend edits are allowed only for renderer contract support and tests.

Frontend must not contain conversion constants or analytical unit-repair logic.

## Forbidden files

Do not edit:

```text
backend/scripts/run_work_package.py
backend/scripts/golden_gate_local.py
backend/scripts/update_cursor_status.py
automation_bus/latest_gate_evidence.json
automation_bus/latest_gate_output.txt
automation_bus/latest_cursor_status.json
```

Do not modify control-plane scripts.

Do not add tooling files such as:

```text
.codex/
.vscode/
AGENTS.md
```

unless explicitly authorised in a separate tooling sprint.

## Phase gates

This sprint has five internal phases.

Each phase must end with a checkpoint in:

```text
docs/audit-papers/LC-S8D_uk_si_unit_governance_remediation_notes.md
```

Each checkpoint must state:

* files changed
* tests run
* decisions made
* blocked rows
* whether the next phase is safe to enter

Do not skip phase checkpoints.

---

# Phase A — Safe equivalence remediation

## Scope

Authorised biomarkers:

```text
platelets
white_blood_cells
sodium
potassium
chloride
```

## Required work

1. Add explicit 1:1 equivalence support:

   * `K/μL`, `K/uL` ↔ `10^9/L` for platelets/WBC where appropriate.
   * `mEq/L` ↔ `mmol/L` for sodium, potassium, chloride as monovalent ions only.
2. Register equivalence in `units.yaml` and `registry.py`.
3. Update SSOT canonical labels only after equivalence support exists.
4. Align directly affected scoring unit labels for PLT/WBC only if numeric values remain equivalent and regression tests prove no scoring drift.
5. Add registry tests proving old and new labels normalise coherently.

## Phase A STOP conditions

STOP if:

* equivalence is not 1:1
* registry behaviour would change numeric values unexpectedly
* scoring bands would require numeric rebanding rather than label alignment
* any marker outside the five authorised Phase A markers is touched
* any frontend conversion is proposed

## Phase A required tests

At minimum, add or update:

```text
backend/tests/unit/test_unit_registry.py
backend/tests/unit/test_scoring_rules.py
```

Test examples must include:

```text
platelets 225 K/μL == 225 10^9/L
white_blood_cells 6.4 K/μL == 6.4 10^9/L
sodium 140 mEq/L == 140 mmol/L
potassium 4.3 mEq/L == 4.3 mmol/L
chloride 102 mEq/L == 102 mmol/L
```

---

# Phase B — True conversion evidence gate

## Scope

Blocked biomarkers:

```text
calcium
corrected_calcium
magnesium
free_t4
hemoglobin
urate
```

## Required action

Do not implement conversion changes for these rows unless primary evidence is present in-repo or directly cited in:

```text
docs/audit-papers/LC-S8D_uk_si_unit_governance_remediation_notes.md
```

Required evidence must include:

* source name
* URL or file path
* quoted unit/conversion statement or exact conversion factor
* biomarker ID
* conversion direction
* formula
* test vector

## Phase B allowed outcome

If evidence is missing, record:

```text
PHASE_B_BLOCKED_PENDING_EVIDENCE
```

and do not change those biomarkers.

Phase B being blocked must not prevent already-authorised Phase A changes from completing.

## Phase B STOP conditions

STOP if:

* any Phase B conversion is implemented without primary evidence
* any conversion factor is inferred from memory or LLM output
* value/reference-range conversion is not handled coherently
* calcium, corrected calcium, magnesium, free T4, haemoglobin, or urate are modified without evidence

---

# Phase C — Layer B scoring migration

## Scope

Only proceed row-by-row where authorised by LC-S8C §19/§20.

Potentially authorised rows:

```text
glucose
total_cholesterol
ldl_cholesterol
hdl_cholesterol
triglycerides
creatinine
hba1c
hematocrit
hba1c_pct merge/deprecation only
platelets after Phase A
white_blood_cells after Phase A
hemoglobin only if Phase B evidence passes
```

## Required work

1. Confirm current scoring unit per biomarker.
2. Confirm Layer A output unit per biomarker.
3. Migrate scoring bands only where source-supported.
4. Add golden before/after test vectors.
5. Prove no scoring drift except where explicitly intended.
6. Ensure Layer B never scores raw uploaded unit values directly.
7. Ensure HbA1c is scored once only.
8. Ensure haematocrit cannot be scored or displayed as `0.438 %`.

## HbA1c-specific requirements

* Canonical analytical identity: `hba1c`.
* UK Layer B unit: `mmol/mol`.
* `%` is accepted as legacy/secondary input.
* If both `mmol/mol` and `%` appear in one uploaded panel, Layer A must preserve both source observations but Layer B must score one HbA1c result only.
* `hba1c_pct` must not be independently scored.
* Do not remove user-visible upload provenance needed for Layer C Mode A.

## Haematocrit-specific requirements

* UK Layer B unit: `L/L`.
* `%` may be accepted only if value and reference range are coherently transformed.
* Never allow `0.438 %`.
* Never allow value and reference range in different unit families.

## Phase C STOP conditions

STOP if:

* primary scoring bands are not source-supported
* Layer A output unit and scoring-policy unit disagree
* `hba1c` and `hba1c_pct` can both be scored
* haematocrit fraction can be labelled as percent
* glucose/lipids/creatinine bands remain US `mg/dL` while Layer A emits UK/SI units
* any Phase B-blocked biomarker is scored in a migrated unit without evidence

---

# Phase D — Layer C display policy

## Scope

Introduce governed display policy support.

Proposed authority file:

```text
backend/ssot/display_unit_policy.yaml
```

If another display-policy authority already exists, STOP and report it.

## Required policy model

Layer C must support two governed presentation modes.

## Mode A — Uploaded-panel fidelity

Use for:

```text
biomarker dials
raw uploaded-results review
upload/edit flows
```

Rules:

* Preserve every uploaded biomarker row where safe.
* If the same canonical biomarker appears in current/canonical and legacy/equivalent units, show both uploaded representations back to the user.
* Visually link or annotate equivalent rows as the same biomarker.
* Do not imply the duplicate-equivalent row was ignored or lost.
* Frontend must display governed API fields only; no conversion constants.

## Mode B — Analytical-report

Use for:

```text
personalised observational report
narrative interpretation
burden summaries
signal summaries
```

Rules:

* Refer to each biomarker once by canonical biomarker identity.
* Use the Layer B analytical unit unless `display_unit_policy.yaml` authorises a governed secondary display.
* Do not duplicate equivalent biomarkers in prose or analytical summary tables.
* Narrative consumes collapsed Layer B input, not raw duplicate source rows.

General rule:

```text
Preserve duplicate-equivalent source observations for uploaded-results fidelity.
Collapse duplicate-equivalent observations for Layer B analysis and report interpretation.
```

## Required display-policy rows

At minimum cover:

```text
hba1c
hematocrit
urea / BUN display
vitamin_d
glucose
total_cholesterol
ldl_cholesterol
hdl_cholesterol
triglycerides
creatinine
platelets
white_blood_cells
hemoglobin if Phase B evidence passes
```

## Phase D STOP conditions

STOP if:

* frontend performs conversion maths
* display policy duplicates analytical authority
* display policy changes Layer B scoring unit
* uploaded-panel fidelity mode cannot preserve duplicate-equivalent source observations
* analytical-report mode still renders duplicate-equivalent biomarkers as separate findings

---

# Phase E — Sentinel lockdown

## Scope

Add Sentinel guardrails only after the relevant Phase A–D implementation is stable and tests pass.

Required guardrails:

```text
uk_layer_b_canonical_unit_drift
layer_b_unit_declared
input_unit_has_authority
unknown_unit_not_scored
biomarker_value_reference_unit_incoherence
hba1c_single_analytical_identity
hematocrit_fraction_percent_display
bun_not_uric_acid
frontend_no_unit_repair
new_biomarker_unit_metadata
```

Sentinel may be introduced in warn mode only where blocking would fail due to deferred Phase B evidence.

Blocking mode is required for completed Phase A and completed HbA1c/haematocrit protections.

## Phase E STOP conditions

STOP if:

* Sentinel blocks deferred evidence rows that were intentionally not remediated
* Sentinel allows completed Phase A drift
* Sentinel allows BUN to map to urate
* Sentinel allows frontend unit conversion constants
* Sentinel allows `hba1c` and `hba1c_pct` to both score

---

# Required validation commands

Run relevant targeted tests after each phase.

At minimum before Cursor completion, run:

```powershell
python -m pytest backend/tests/unit/test_unit_registry.py -q
python -m pytest backend/tests/unit/test_scoring_rules.py -q
python -m pytest backend/tests/unit/test_hba1c_governance.py -q
python -m pytest backend/tests/regression/test_lc_s8_biomarker_unit_reference_incoherence_regression.py -q
```

If any listed test file does not exist, either create it if in scope or record why it is not applicable.

Run frontend no-conversion scan:

```powershell
Select-String -Path frontend/app/**/*.ts,frontend/app/**/*.tsx -Pattern "mg/dL|mmol|umol|µmol|K/μL|K/uL|mEq|0.055|18.018|38.67|88.4|0.01|100" -CaseSensitive:$false
```

Any hit must be reviewed.

Conversion constants in frontend are blockers unless they are static text examples in tests/docs.

Run SSOT/unit/scoring scan:

```powershell
Select-String -Path backend/ssot/*.yaml,backend/core/**/*.py,backend/tests/**/*.py -Pattern "unit|units|mmol|mol|mg/dL|g/dL|mEq|K/μL|K/uL|HbA1c|hba1c|hematocrit|haematocrit|BUN|urea|uric" -CaseSensitive:$false
```

# Required documentation output

Create or update:

```text
docs/audit-papers/LC-S8D_uk_si_unit_governance_remediation_notes.md
```

It must include:

1. Phase A result.
2. Phase B evidence result or blocked status.
3. Phase C row-by-row scoring migration result.
4. Phase D display-policy result.
5. Phase E Sentinel result.
6. Files changed.
7. Tests run.
8. Deferred items.
9. Known residual risk.
10. Cursor completion recommendation.

# Acceptance criteria

The work is complete only if:

* Phase A equivalence is implemented and tested.
* Phase B blocked rows remain untouched unless evidence is attached.
* Layer B never scores unknown or incoherent units.
* HbA1c cannot be scored twice.
* Haematocrit cannot display or score incoherently.
* BUN cannot map to urate.
* Display policy separates uploaded-panel fidelity from analytical-report collapse.
* Frontend remains renderer-only.
* No fallback parser is introduced.
* No control-plane scripts are changed.
* Tests and Sentinel rules reflect completed scope.
* Deferred items are explicit and intentional.

# Cursor completion requirements

When implementation is complete, Cursor must:

1. Run all required targeted validation commands listed in this prompt.
2. Update `docs/audit-papers/LC-S8D_uk_si_unit_governance_remediation_notes.md` with:

   * phase results
   * files changed
   * tests run
   * blocked/deferred items
   * known residual risks
   * Cursor completion recommendation
3. Run the mandatory post-implementation closure audit required by Automation Bus SOP:

   * `git branch --show-current`
   * `git status --short`
   * `git log --oneline -n 5`
   * `git diff --name-only`
   * `git diff --cached --name-only`
   * `git stash list`
4. Classify:

   * tracked modified files
   * staged files
   * untracked files
   * tooling files
   * out-of-scope files
   * stash entries
5. STOP if there are unrelated files, tooling leakage, dirty branch ambiguity, or stash ambiguity.
6. If closure is clean, run:

```powershell
python backend/scripts/run_work_package.py finish
```

7. Report whether finish completed or failed.
8. Do not merge.
9. Do not create `automation_bus/latest_audit_summary.md`.
10. Do not claim final approval.

# Explicit non-authority statement

Cursor implements only.

Cursor may not self-certify clinical correctness, architecture correctness, merge readiness, or final approval.

Cursor must report evidence and stop at implementation completion.

````
