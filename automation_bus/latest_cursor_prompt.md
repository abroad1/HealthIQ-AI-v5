---
work_id: LC-S8G
branch: launch-core/lc-s8f-phase-b-uk-si-true-conversions
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# LC-S8G — Uploaded-Unit Display Fidelity Contract and SSOT-Wide Guardrail

## Classification

This is a HIGH-risk MIXED blocker-fix sprint on top of the unmerged LC-S8F branch.

Reason: LC-S8F backend Phase B conversion is correct, but human UAT exposed a customer-facing display contract failure. This sprint may touch backend DTO output, frontend result rendering, TypeScript result types, regression tests, Sentinel/static guardrails, and UAT documentation.

This is not a new feature sprint.

This sprint completes the display contract required before LC-S8F can merge.

## Current branch context

Work on the existing unmerged branch:

```text
launch-core/lc-s8f-phase-b-uk-si-true-conversions
````

Do not create a new branch unless explicitly instructed.

Do not undo LC-S8F.

Do not alter Layer B canonical UK/SI conversion.

## Problem

LC-S8F correctly converts Phase B biomarkers into UK/SI canonical units for Layer B analysis.

However, human UAT found that when a user uploads US/non-UK units, the main customer-facing biomarker dials display the internal UK/SI analytical units back to the user.

That is wrong.

Example:

```text
Uploaded:
Calcium 9.4 mg/dL, range 8.6–10.2 mg/dL

Internal analytical:
Calcium 2.3453 mmol/L, range 2.1457–2.5449 mmol/L

Current main display:
2.3453 mmol/L

Required main display:
9.4 mg/dL, range 8.6–10.2 mg/dL
with optional transparency note: analysed internally as mmol/L
```

The separate “Uploaded panel values” section is not sufficient. The main customer-facing biomarker display must preserve the user’s uploaded unit family where safe and governed.

## Investigation finding

The defect is pre-existing from the FE-S8E Mode A / Mode B split, but exposed by LC-S8F.

Current behaviour:

* main dials render from canonical `biomarkers[]`
* uploaded source observations are preserved only in `meta.upload_panel_observations`
* `BiomarkerResult` has no governed per-biomarker `display_value`, `display_unit`, or `display_reference_range`
* frontend dials have no display override path
* LC-S8F did not touch frontend, but made the gap visible because Phase B conversions now occur correctly

## Correct architecture

Layer B:

```text
Always analyse using canonical UK/SI units.
```

Customer-facing Layer C / frontend display:

```text
Display the uploaded unit family where safe and governed.
```

Frontend:

```text
Renderer only.
No conversion maths.
No unit inference.
No hidden calculation.
Render backend-supplied display fields.
```

## Required behaviour

For each biomarker:

1. Backend keeps analytical fields:

   * canonical analytical value
   * canonical analytical unit
   * canonical analytical reference range

2. Backend also emits display fields:

   * `display_value`
   * `display_unit`
   * `display_reference_range`
   * optional `analytical_value`
   * optional `analytical_unit`
   * optional `analytical_reference_range`
   * optional `display_is_uploaded_unit` / `unit_display_mode`

3. Frontend main dials/cards prefer display fields:

   * `display_value ?? value`
   * `display_unit ?? unit`
   * `display_reference_range ?? reference_range`

4. If display and analytical units differ, frontend shows a non-technical transparency note supplied or inferable from backend fields, for example:

   * `Analysed internally as mmol/L`
   * `Analysed internally as pmol/L`
   * `Analysed internally as g/L`

5. Frontend must not calculate conversions.

6. Uploaded-panel fidelity section remains, but it is not the only place uploaded units appear.

## Display field source rules

Use `meta.upload_panel_observations` or the backend’s equivalent source-observation structure.

### Single uploaded source observation

If a canonical biomarker has one uploaded source observation and that unit is authorised/governed:

* use the uploaded value/unit/range for `display_*`
* use canonical UK/SI value/unit/range for analytical fields

### UK/SI uploaded source observation

If user uploaded canonical UK/SI unit:

* `display_*` should equal analytical display where appropriate
* do not add unnecessary conversion notes

### Multiple equivalent uploaded observations

If a canonical biomarker has multiple equivalent uploaded observations, for example HbA1c in both `mmol/mol` and `%`:

* do not duplicate analytical scoring
* preserve all rows in uploaded-panel fidelity section
* main dial should use the safest governed display choice:

  * prefer uploaded canonical unit if present
  * otherwise prefer the primary uploaded source observation
* document this choice in tests/notes

### Unsupported or unsafe source unit

If uploaded unit is unsupported or not governed:

* do not invent display conversion
* do not silently score if conversion authority is missing
* preserve existing unscored/error behaviour

## Phase B UAT cases to fix

Use the two existing human UAT reports where possible:

US/non-UK conversion panel:

```text
analysis_id=7cc8b2d5-c8f0-4138-ba18-8540eece06a1
```

UK/SI pass-through panel:

```text
analysis_id=b24ce358-02e3-4058-a667-34328a4168a2
```

The earlier brief labels were swapped. Treat:

```text
7cc8b2d5... = US/non-UK conversion panel
b24ce358... = UK/SI pass-through panel
```

## Required examples

### US/non-UK uploaded panel

Main customer-facing display must show:

| Biomarker         | Uploaded display expected        | Internal analytical expected |
| ----------------- | -------------------------------- | ---------------------------- |
| Calcium           | `9.4 mg/dL`, RR `8.6–10.2 mg/dL` | `2.3453 mmol/L`              |
| Corrected calcium | `9.4 mg/dL`, RR `8.6–10.2 mg/dL` | `2.3453 mmol/L`              |
| Magnesium         | `2.1 mg/dL`, RR `1.7–2.4 mg/dL`  | `0.86394 mmol/L`             |
| Free T4           | `1.2 ng/dL`, RR `0.8–1.8 ng/dL`  | `15.4452 pmol/L`             |
| Haemoglobin       | `14.6 g/dL`, RR `13.0–17.5 g/dL` | `146 g/L`                    |
| Uric acid / urate | `5.8 mg/dL`, RR `3.5–7.2 mg/dL`  | `345.1 µmol/L`               |

### UK/SI pass-through panel

Main customer-facing display must remain:

| Biomarker         | Display expected                     |
| ----------------- | ------------------------------------ |
| Haemoglobin       | `144 g/L`, RR `130–175 g/L`          |
| Uric acid / urate | `440 µmol/L`, RR `220–547 µmol/L`    |
| Free T4           | `16.8 pmol/L`, RR `12–22 pmol/L`     |
| Calcium           | `2.33 mmol/L`, RR `2.15–2.57 mmol/L` |
| Corrected calcium | `2.25 mmol/L`, RR `2.20–2.60 mmol/L` |
| Magnesium         | `0.89 mmol/L`, RR `0.73–1.06 mmol/L` |

## Mandatory preflight

Run and record:

```powershell
git branch --show-current
git status --short
git log --oneline -n 5
```

Confirm you are on:

```text
launch-core/lc-s8f-phase-b-uk-si-true-conversions
```

Confirm LC-S8F changes are present.

Confirm the Phase B evidence file is committed:

```powershell
git ls-files --error-unmatch docs/audit-papers/Phase_B_UK_SI_Biomarker_Unit_Evidence_Review.md
```

If the evidence file is not tracked, STOP.

## Authority preflight

Before editing, identify and record authoritative paths for:

1. backend analysis result DTO builder
2. `BiomarkerResult` Python/DTO model if present
3. frontend `BiomarkerResult` TypeScript type
4. frontend biomarker dial/card data mapping
5. uploaded-panel observation structure
6. display unit policy file
7. unit registry / conversion authority
8. Sentinel pack registry
9. existing FE-S8E uploaded-panel fidelity tests
10. LC-S8D/LC-S8F unit-governance tests

Known likely files:

```text
backend/core/dto/builders.py
frontend/app/types/analysis.ts
frontend/app/(app)/results/page.tsx
frontend/app/components/biomarkers/BiomarkerDials.tsx
frontend/app/lib/uploadPanelFidelity.ts
backend/ssot/display_unit_policy.yaml
backend/core/units/registry.py
backend/tests/regression/test_lc_s8f_phase_b_true_conversions.py
backend/tests/regression/test_lc_s8d_unit_governance_sentinel.py
sentinel/packs/lc_s8d_unit_governance_v1.json
```

STOP if there are multiple competing DTO/display authorities.

## Potentially allowed files

Only edit files required to implement and protect the display contract:

```text
backend/core/dto/builders.py
backend/core/contracts/**/*
backend/app/routes/analysis.py only if DTO wiring requires it
backend/tests/unit/**/*
backend/tests/regression/**/*

frontend/app/types/analysis.ts
frontend/app/(app)/results/page.tsx
frontend/app/components/biomarkers/BiomarkerDials.tsx
frontend/app/lib/**/*
frontend/tests/**/*

backend/ssot/display_unit_policy.yaml only if needed to declare display policy
sentinel/packs/**/*
sentinel/**/*

docs/audit-papers/LC-S8G_uploaded_unit_display_fidelity_notes.md
docs/audit-papers/LC-S8F_phase_b_unit_conversion_uat.md only if updating UAT interpretation
```

## Forbidden files and changes

Do not edit:

```text
backend/ssot/biomarkers.yaml
backend/ssot/units.yaml
backend/ssot/scoring_policy.yaml
backend/core/units/registry.py
backend/core/scoring/rules.py
frontend code that performs conversion maths
backend/scripts/run_work_package.py
backend/scripts/golden_gate_local.py
backend/scripts/update_cursor_status.py
automation_bus/latest_gate_evidence.json
automation_bus/latest_gate_output.txt
automation_bus/latest_cursor_status.json
```

Exception:

* You may read these files.
* Do not modify LC-S8F backend conversion implementation unless a test proves it is broken.
* The aim is display-contract completion, not conversion changes.

Do not:

* undo LC-S8F
* change Layer B canonical UK/SI analysis
* introduce frontend conversion constants
* recompute corrected calcium
* map urate to urea
* introduce generic/default reference ranges
* hide uploaded observations
* suppress biomarkers to pass tests
* add fallback parser logic

## Phase 1 — Contract inventory

Create:

```text
docs/audit-papers/LC-S8G_uploaded_unit_display_fidelity_notes.md
```

Record:

* current DTO fields
* current frontend dial fields
* current uploaded observation fields
* whether backend has enough data to construct display fields
* where display fields will be added
* which tests will protect them

Required table:

| Surface | Current field source | Defect | Fix |
| ------- | -------------------- | ------ | --- |

Do not implement until this inventory is complete.

## Phase 2 — Backend DTO display contract

Add backend display fields to each biomarker result row.

Required fields, unless an equivalent existing contract is discovered:

```text
display_value
display_unit
display_reference_range
analytical_value
analytical_unit
analytical_reference_range
display_is_uploaded_unit
```

Rules:

* analytical fields reflect canonical Layer B values
* display fields reflect uploaded source unit/value/range where safe
* if uploaded source unavailable, display fields fall back to analytical fields
* if source uploaded range exists, display range uses source uploaded range
* if source uploaded range is unavailable, do not invent a generic range
* no clinical interpretation should depend on display fields
* no scoring should use display fields

STOP if display fields cannot be populated deterministically from stored payload/source observations.

## Phase 3 — Frontend render change

Update main biomarker dial/card rendering so user-facing value/unit/range use display fields first.

Required frontend behaviour:

```text
shown_value = display_value ?? value
shown_unit = display_unit ?? unit
shown_range = display_reference_range ?? reference_range
```

If display and analytical units differ, show a short transparency note:

```text
Analysed internally as [analytical_unit]
```

Rules:

* frontend must not calculate conversions
* frontend must not infer display units
* frontend must not contain conversion constants
* frontend must not lose existing uploaded-panel section
* frontend must not duplicate equivalent biomarkers as scored findings

## Phase 4 — SSOT-wide uploaded-unit display guardrail

Create or update regression/Sentinel coverage so this problem cannot recur.

This guard must be SSOT-driven, not limited to the six Phase B examples.

Guard concept:

```text
For every biomarker in SSOT with authorised alternative input units / governed conversion paths:
Layer B may canonicalise internally.
Main customer-facing display must preserve uploaded value/unit/range where safe.
Frontend must not perform conversion maths.
```

Required dynamic checks:

1. Read biomarker/unit/conversion authority from SSOT/registry where possible.
2. Identify biomarkers with authorised non-canonical input units.
3. For each eligible biomarker, assert there is either:

   * an automated display-fidelity test case, or
   * an explicit documented exclusion with reason.

At minimum, the guard must cover:

```text
calcium
corrected_calcium
magnesium
free_t4
hemoglobin
urate
hba1c / hba1c_pct
hematocrit
platelets
white_blood_cells
sodium
potassium
chloride
glucose
total_cholesterol
ldl_cholesterol
hdl_cholesterol
triglycerides
creatinine
bun / urea
vitamin_d
```

The guard must fail if:

* a biomarker has an authorised alternative input unit but no display-fidelity coverage
* main display shows only canonical UK/SI units for a non-UK upload
* source uploaded range is dropped while display claims uploaded unit
* value and displayed range are in different unit families
* frontend conversion constants are added
* uploaded units appear only in the secondary uploaded-panel section and not in the main customer-facing display

If full dynamic generation is too large for this sprint, implement the dynamic coverage inventory plus a hard minimum fixture set covering Phase B and previously remediated LC-S8D conversions. Document any explicit exclusions.

## Phase 5 — Tests

Add or update tests for:

### Backend DTO

* US upload produces canonical analytical fields and uploaded display fields
* UK upload produces analytical/display fields that match
* source uploaded reference range is preserved in display range
* analytical reference range remains canonical/internal
* no generic display range is invented

### Frontend rendering

* dials prefer display fields
* dials show uploaded units for US panel
* dials show analytical transparency note when units differ
* dials show UK/SI units unchanged for UK panel
* frontend contains no conversion constants

### Sentinel/regression

* SSOT-wide or SSOT-inventory guard exists
* Phase B examples protected
* LC-S8D examples protected
* unsupported biomarkers/units do not silently pass

## Required validation commands

Run relevant backend tests:

```powershell
python -m pytest backend/tests/regression/test_lc_s8f_phase_b_true_conversions.py -q
python -m pytest backend/tests/regression/test_lc_s8d_unit_governance_sentinel.py -q
python -m pytest backend/tests/regression/test_lc_s8_biomarker_unit_reference_incoherence_regression.py -q
python -m pytest backend/tests/unit/test_unit_registry.py -q
python -m pytest backend/tests/unit/test_scoring_rules.py -q
```

Run new LC-S8G tests explicitly, for example:

```powershell
python -m pytest backend/tests/regression/test_lc_s8g_uploaded_unit_display_fidelity.py -q
```

Run frontend validation if frontend files are changed:

```powershell
npm run type-check
npm run test
```

If frontend test infrastructure is limited or broken, record exact output and add the strongest available static/backend regression coverage.

Run frontend no-conversion scan:

```powershell
Select-String -Path frontend/app/**/*.ts,frontend/app/**/*.tsx -Pattern "0.2495|0.4114|12.871|59.5|0.055|0.0555|18.018|38.67|88.4|0.02586|mg/dL|g/dL|ng/dL|convert" -CaseSensitive:$false
```

Review all hits. Conversion constants in frontend runtime are blockers unless they are static copy/tests and clearly not calculation logic.

## Human UAT replay

After implementation, re-check the two existing reports or regenerate equivalent reports:

US/non-UK conversion panel:

```text
7cc8b2d5-c8f0-4138-ba18-8540eece06a1
```

UK/SI pass-through panel:

```text
b24ce358-02e3-4058-a667-34328a4168a2
```

Expected:

* US panel main dials show uploaded US units/ranges
* US panel also indicates internal analytical UK/SI unit where appropriate
* UK panel main dials show UK/SI units/ranges
* uploaded-panel section remains present
* no frontend conversion maths

## Acceptance criteria

This sprint is complete only if:

* backend DTO emits governed display fields
* frontend main dials use display fields
* US/non-UK uploaded units display back to the user on main result cards
* UK/SI uploaded units pass through unchanged
* Layer B analytical values remain UK/SI canonical
* scoring/ranking remain based on analytical fields only
* uploaded-panel fidelity section remains intact
* reference ranges shown to users match displayed unit family
* no generic/default ranges are introduced
* frontend performs no conversion maths
* SSOT-wide display-fidelity guard or coverage-inventory guard exists
* Phase B and LC-S8D conversion families are protected
* human UAT defect is resolved
* LC-S8F backend conversion remains passing

## Required documentation output

Create or update:

```text
docs/audit-papers/LC-S8G_uploaded_unit_display_fidelity_notes.md
```

Must include:

1. defect origin
2. files changed
3. DTO fields added
4. frontend rendering change
5. SSOT-wide guardrail approach
6. test coverage
7. UAT replay result
8. known exclusions or deferred items
9. final merge recommendation

This note must map directly to implementation and tests. It is not a passive decision document.

## Cursor completion requirements

When complete:

1. Run required validation commands.
2. Update the LC-S8G notes.
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

6. Do not merge.

7. Do not create `automation_bus/latest_audit_summary.md`.

8. Do not claim final approval.

## Explicit non-authority statement

Cursor implements and reports only.

Cursor may not self-certify architecture correctness, clinical correctness, merge readiness, launch readiness, or final approval.

```
```
