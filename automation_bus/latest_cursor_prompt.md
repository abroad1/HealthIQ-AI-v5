---
work_id: FE-S8E
branch: launch-core/fe-s8e-uploaded-panel-fidelity-rendering
risk_level: STANDARD
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# FE-S8E — Uploaded-Panel Fidelity Rendering for Layer C Mode A

## Classification

This is a STANDARD-risk MIXED frontend/display-contract work package.

Reason: LC-S8D backend unit governance is already passing. This sprint must not alter analytical logic, unit conversion, scoring, canonicalisation, SSOT unit policy, or Layer B behaviour.

This sprint implements frontend rendering of the already-delivered backend contract for Layer C Mode A uploaded-panel fidelity.

## Purpose

Implement the frontend/upload-review presentation layer required by LC-S8D.

LC-S8D correctly preserves original uploaded biomarker observations in:

```text
meta.upload_panel_observations
````

and exposes display policy metadata in:

```text
meta.display_unit_policy
```

However, the current frontend dials/results surface renders only canonical analytical `biomarkers[]`, so duplicate-equivalent source observations such as HbA1c `%` are not visible to the user. This creates a user-trust gap: users may think uploaded rows were ignored or lost.

The goal is to show uploaded source observations where appropriate, while preserving the analytical-report rule that equivalent biomarkers are analysed once only.

## Governing context

Read before editing:

```text
docs/audit-papers/LC-S8C_ssot_wide_unit_governance_preflight.md
docs/audit-papers/LC-S8D_uk_si_unit_governance_remediation_notes.md
docs/audit-papers/LC-S8D_frontend_layer_c_uat_report.md

frontend/app/(app)/results/page.tsx
frontend/app/components/biomarkers/BiomarkerDials.tsx
frontend/app/types/analysis.ts
frontend/app/queries/analysisResult.ts

backend/app/routes/analysis.py
backend/core/units/display_policy.py
backend/ssot/display_unit_policy.yaml
```

LC-S8D UAT found:

* backend analytical payload passes
* Layer B canonicalisation passes
* HbA1c is scored once only
* haematocrit is correctly `L/L`
* BUN maps to urea, not urate
* backend preserves `upload_panel_observations`
* frontend does not yet render uploaded-panel fidelity mode

## Architectural rule

Layer C has two presentation modes.

### Mode A — Uploaded-panel fidelity

Used for:

```text
biomarker dials
raw uploaded-results review
upload/edit confirmation surfaces
```

Rules:

* Preserve every uploaded biomarker row where safe.
* If the same canonical biomarker appears in current/canonical and legacy/equivalent units, show both uploaded representations.
* Visually link or annotate equivalent rows as the same biomarker.
* Do not imply duplicate-equivalent rows were ignored or lost.
* Do not perform frontend conversion maths.

### Mode B — Analytical-report mode

Used for:

```text
personalised observational report
narrative interpretation
burden summaries
signal summaries
```

Rules:

* Refer to each biomarker once by canonical identity.
* Use canonical Layer B analytical unit unless governed display policy says otherwise.
* Do not duplicate equivalent biomarkers in narrative/prose.
* Do not change report interpretation behaviour in this sprint.

General rule:

```text
Preserve duplicate-equivalent source observations for uploaded-results fidelity.
Collapse duplicate-equivalent observations for Layer B analysis and report interpretation.
```

## Scope

Implement frontend support for Mode A display only.

Allowed files:

```text
frontend/app/(app)/results/page.tsx
frontend/app/components/biomarkers/BiomarkerDials.tsx
frontend/app/types/analysis.ts
frontend/app/queries/analysisResult.ts
frontend/app/services/*
frontend/app/components/*
backend/tests/* only if needed for contract fixture coverage
frontend tests if present
```

Backend code may be read but must not be changed unless a type/contract mismatch prevents frontend rendering and the required change is purely DTO typing or fixture support.

## Forbidden changes

Do not edit:

```text
backend/ssot/biomarkers.yaml
backend/ssot/units.yaml
backend/ssot/scoring_policy.yaml
backend/core/units/registry.py
backend/core/scoring/rules.py
backend/core/canonical/hba1c_layer_b_arbitration.py
sentinel/*
automation_bus/*
```

Do not:

* add frontend conversion constants
* calculate unit conversions in React/TypeScript
* alter scoring
* alter canonical units
* hide failed biomarkers
* remove canonical biomarker dials
* reintroduce `hba1c_pct` as an analytical biomarker
* add fallback parser logic

## Required implementation

### 1. Extend frontend types

Update frontend result types so they recognise:

```text
meta.upload_panel_observations
meta.display_unit_policy
```

The type should tolerate absence of these fields for older results.

### 2. Render uploaded-panel fidelity information

On the results page or biomarker dial section, add a clear uploaded-panel fidelity surface.

Acceptable implementation options:

Option A — preferred:

Add a compact “Uploaded panel” or “Uploaded values” section near the biomarker dials showing the original uploaded rows.

Option B:

Within each biomarker dial/card, show an “Uploaded as” line where the uploaded unit differs from the canonical analytical unit.

Option C:

Group equivalent uploaded observations beneath the canonical dial.

Use the least disruptive UI that proves the contract.

### 3. Duplicate-equivalent handling

For this test case, confirm:

* HbA1c canonical dial remains `42 mmol/mol`.
* HbA1c uploaded `%` row remains visible somewhere in Mode A as `6 %`.
* It is clearly annotated as an equivalent representation of HbA1c, not a separate scored biomarker.
* Haematocrit canonical display remains `0.438 L/L`, but uploaded `43.8 %` may be shown as uploaded source observation.
* Platelets uploaded `K/uL` may be shown as uploaded source observation while analytical value remains `10^9/L`.
* WBC uploaded `K/uL` may be shown as uploaded source observation while analytical value remains `10^9/L`.
* Sodium/potassium/chloride uploaded `mEq/L` may be shown while analytical values remain `mmol/L`.

### 4. Renderer-only requirement

Frontend must display values supplied by the API only.

Do not calculate:

```text
mg/dL ↔ mmol/L
% ↔ mmol/mol
% ↔ L/L
K/uL ↔ 10^9/L
mEq/L ↔ mmol/L
```

Any transformation must already exist in backend payload.

### 5. Fix small visible label issue if trivial

If the display-name map is local and safe to update, add a friendly label for:

```text
white_blood_cells → White Blood Cells
```

Do not widen into a general label-cleanup sprint.

## Test case

Use the existing analysis:

```text
http://localhost:3000/results?analysis_id=e4dc8e59-2588-4943-b37b-a299c89f9442
```

Login:

```text
test-user3@example.com
Subaru@555
```

Expected observations:

* Page loads.
* API returns 200.
* Biomarker dials still show canonical analytical values.
* Uploaded-panel fidelity surface shows original uploaded observations.
* HbA1c `%` is visible as uploaded/equivalent, not scored independently.
* No frontend conversion maths is added.
* No console errors.
* No failed network calls.

## Required validation

Run frontend checks available in the repo, for example:

```powershell
npm run lint
npm run typecheck
npm run test
```

If a command does not exist, record that clearly.

Run no-conversion scan:

```powershell
Select-String -Path frontend/app/**/*.ts,frontend/app/**/*.tsx -Pattern "0.055|0.0555|18.018|38.67|88.4|0.02586|0.01|100|mg_dL|mmol_L|convert" -CaseSensitive:$false
```

Review all hits. Frontend conversion constants are blockers unless they are static copy, tests, or pre-existing unrelated dev tooling.

Manual browser validation required:

* open the report URL
* inspect dials/results area
* confirm uploaded-panel fidelity display
* confirm HbA1c `%` source row is visible
* confirm canonical analytical report still collapses HbA1c
* capture screenshots or concise written observations in the completion report

## Required documentation output

Create:

```text
docs/audit-papers/FE-S8E_uploaded_panel_fidelity_uat_notes.md
```

Include:

1. files changed
2. UI behaviour before
3. UI behaviour after
4. how `upload_panel_observations` is rendered
5. how duplicate-equivalent biomarkers are annotated
6. confirmation frontend remains renderer-only
7. validation commands run
8. browser UAT result
9. known gaps deferred

## Acceptance criteria

This sprint is complete only if:

* frontend consumes `meta.upload_panel_observations`
* uploaded source observations are visible in the results experience
* HbA1c `%` appears as uploaded/equivalent when present
* equivalent rows are not represented as separate analytical findings
* canonical biomarker dials still use analytical `biomarkers[]`
* no frontend conversion logic is introduced
* no backend scoring/unit/canonicalisation files are changed
* no console/network errors are introduced
* browser UAT confirms the report still loads

## Cursor completion requirements

When complete, Cursor must:

1. Run relevant validation commands.
2. Complete browser UAT on the specified report.
3. Update the required documentation note.
4. Run closure audit:

```powershell
git branch --show-current
git status --short
git log --oneline -n 5
git diff --name-only
git diff --cached --name-only
git stash list
```

5. Classify tracked, staged, untracked, tooling, out-of-scope, and stash items.
6. STOP if unrelated files, tooling leakage, dirty branch ambiguity, or stash ambiguity exists.
7. If closure is clean, run:

```powershell
python backend/scripts/run_work_package.py finish
```

8. Report whether finish completed or failed.
9. Do not merge.
10. Do not create `automation_bus/latest_audit_summary.md`.
11. Do not claim final approval.

## Explicit non-authority statement

Cursor implements only.

Cursor may not self-certify architecture correctness, merge readiness, or final approval.

````