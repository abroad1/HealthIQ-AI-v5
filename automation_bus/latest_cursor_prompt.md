---
work_id: LC-S8F
branch: launch-core/lc-s8f-phase-b-uk-si-true-conversions
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# LC-S8F — Phase B UK/SI True Conversion Implementation

## Classification

This is a HIGH-risk MIXED implementation sprint.

Reason: this sprint may touch SSOT biomarker units, unit registry data, runtime unit-conversion dispatch, scoring-policy units, reference-range coherence behaviour, regression tests, and Sentinel protections.

This sprint implements the previously blocked LC-S8C / LC-S8D Phase B UK/SI true-conversion biomarkers after evidence review.

This sprint must not alter unrelated biomarkers, broaden unit policy, change questionnaire behaviour, alter Layer C narrative logic, add fallback/global reference ranges, or introduce frontend conversion logic.

## Purpose

Implement approved UK/SI canonical unit handling for the six Phase B biomarkers previously blocked pending evidence:

```text
calcium
corrected_calcium
magnesium
free_t4
hemoglobin / haemoglobin
urate / uric_acid
````

The evidence review approves implementation for all six, with mandatory controls:

* use UK/SI canonical units
* convert uploaded values only through governed backend registry/runtime paths
* convert uploaded lab-derived reference ranges coherently when source unit differs
* never substitute generic/global/default reference ranges where lab ranges exist
* preserve assay/lab-specific reference ranges, especially Free T4
* do not recompute corrected calcium unless formula and albumin unit are explicit and governed
* keep urate/uric acid completely separate from urea/BUN

## Non-negotiable reference-range policy

HealthIQ AI must use lab-derived reference ranges for biomarker interpretation.

```text
Use lab-derived reference ranges only.
Do not substitute generic/global/default ranges where the lab has supplied a range.
Only calculate/reference a derived range when HealthIQ must calculate a ratio or derived marker that the lab did not provide.
```

For this sprint:

1. If an uploaded value is converted from a non-UK unit into the UK/SI canonical unit, the uploaded lab reference range must be converted by the same governed backend conversion path.
2. If the uploaded lab provides a UK/SI value and UK/SI reference range, preserve both.
3. If no lab reference range is supplied, do not invent a universal range for interpretation.
4. Any fallback display range, if it already exists, must not be treated as interpretation authority.
5. Free T4 must preserve lab/assay-specific reference ranges.
6. Corrected calcium must preserve the lab’s corrected-calcium value/range.
7. Do not calculate corrected calcium from total calcium and albumin unless formula and albumin unit are explicit and already governed.

## Evidence-file prerequisite

Before execution, confirm this file exists in the repo and is committed on the work-package branch:

```text
docs/audit-papers/Phase_B_UK_SI_Biomarker_Unit_Evidence_Review.md
```

If the file is missing, untracked, unstaged, or only present outside the repo, STOP.

Do not implement from memory or from this prompt alone.

## Governing evidence

Read before editing:

```text
docs/audit-papers/LC-S8C_ssot_wide_unit_governance_preflight.md
docs/audit-papers/LC-S8D_uk_si_unit_governance_remediation_notes.md
docs/audit-papers/Phase_B_UK_SI_Biomarker_Unit_Evidence_Review.md
```

The evidence report approves:

| Biomarker                | UK/SI canonical unit | Input alternative | Conversion                |
| ------------------------ | -------------------- | ----------------- | ------------------------- |
| Calcium                  | `mmol/L`             | `mg/dL`           | `mmol/L = mg/dL × 0.2495` |
| Corrected calcium        | `mmol/L`             | `mg/dL`           | `mmol/L = mg/dL × 0.2495` |
| Magnesium                | `mmol/L`             | `mg/dL`           | `mmol/L = mg/dL × 0.4114` |
| Free T4                  | `pmol/L`             | `ng/dL`           | `pmol/L = ng/dL × 12.871` |
| Haemoglobin / Hemoglobin | `g/L`                | `g/dL`            | `g/L = g/dL × 10`         |
| Urate / Uric acid        | `µmol/L`             | `mg/dL`           | `µmol/L = mg/dL × 59.5`   |

Evidence caveats:

* corrected calcium is formula-derived and albumin-dependent; convert supplied values, do not recompute without explicit governed formula and albumin unit
* Free T4 conversion is arithmetically approved, but reference-range interpretation is assay/lab-specific
* urate/uric acid is not urea/BUN
* lab-supplied ranges override all generic/global ranges

## Real UK lab examples to preserve

Use these as sanity-check expectations and optional fixtures:

```text
Haemoglobin (HGB): 144 g/L, range 130–175 g/L
Uric Acid (Venous): 440 µmol/L, range 220–547 µmol/L
Free T4 (Venous): 16.8 pmol/L, range 12–22 pmol/L
Lab note: new reference range commencing 11/09/2024
```

Expected behaviour:

* these UK values pass through unchanged
* their lab reference ranges pass through unchanged
* Free T4 range note does not cause replacement with a generic range
* no US/default ranges override these lab-derived ranges

## Mandatory preflight before editing

Run and record:

```powershell
git branch --show-current
git status --short
git log --oneline -n 5
git ls-files --error-unmatch docs/audit-papers/Phase_B_UK_SI_Biomarker_Unit_Evidence_Review.md
```

Then verify:

```powershell
Test-Path automation_bus/state/work_package_active.json
```

Read `automation_bus/state/work_package_active.json` and confirm:

* `work_id` is `LC-S8F`
* branch is `launch-core/lc-s8f-phase-b-uk-si-true-conversions`

If the token is missing or mismatched, STOP:

```text
Kernel start not executed or work package mismatch.
```

## Authority preflight

Before modifying files, identify and record the authoritative paths for:

1. biomarker SSOT
2. unit registry data
3. runtime unit conversion logic
4. runtime conversion dispatch in `backend/core/units/registry.py`
5. scoring policy
6. alias registry
7. reference-range normalisation / value-range coherence logic
8. existing LC-S8D unit-governance Sentinel pack
9. existing tests for unit registry and scoring
10. existing tests for value/reference-range incoherence
11. BUN/urea/urate alias protection
12. frontend no-conversion Sentinel/static-scan patterns

STOP if any authority is ambiguous or duplicated.

Do not create a second authority source.

## Potentially allowed files

Only edit files required for this Phase B conversion implementation.

Potentially allowed:

```text
backend/ssot/biomarkers.yaml
backend/ssot/units.yaml
backend/ssot/scoring_policy.yaml
backend/ssot/biomarker_alias_registry.yaml

backend/core/units/registry.py
backend/core/scoring/rules.py
backend/core/**/* only if required for reference-range coherence

backend/tests/unit/test_unit_registry.py
backend/tests/unit/test_scoring_rules.py
backend/tests/regression/test_lc_s8_biomarker_unit_reference_incoherence_regression.py
backend/tests/regression/test_lc_s8d_unit_governance_sentinel.py
backend/tests/**/* only where directly relevant

sentinel/packs/lc_s8d_unit_governance_v1.json
sentinel/packs/**/* only if adding Phase B protection

docs/audit-papers/Phase_B_UK_SI_Biomarker_Unit_Evidence_Review.md
docs/audit-papers/LC-S8F_phase_b_true_conversion_implementation_notes.md
```

## Forbidden files and changes

Do not edit:

```text
frontend/**
backend/scripts/run_work_package.py
backend/scripts/golden_gate_local.py
backend/scripts/update_cursor_status.py
automation_bus/latest_gate_evidence.json
automation_bus/latest_gate_output.txt
automation_bus/latest_cursor_status.json
```

Do not:

* alter Layer C narrative
* alter launch-core proving harness unless a test path breaks because of unit changes
* change questionnaire logic
* change medication/statin logic
* change LC-S10B protection scope
* introduce generic/default reference ranges
* recompute corrected calcium without explicit governed formula and albumin unit
* map urate/uric acid to urea/BUN
* implement frontend conversion logic
* add fallback parser logic
* suppress failing biomarkers to pass tests

## Required implementation

### 1. SSOT canonical unit updates

Update SSOT canonical units for the approved Phase B biomarkers:

```text
calcium → mmol/L
corrected_calcium → mmol/L
magnesium → mmol/L
free_t4 → pmol/L
hemoglobin / haemoglobin → g/L
urate / uric_acid → µmol/L or existing repo-equivalent umol/L
```

Use the existing canonical biomarker IDs in the repo. Do not create duplicate biomarker IDs.

If the repo uses `hemoglobin` as the canonical ID with `haemoglobin` as an alias, preserve that structure.

If the repo uses `urate` as canonical with `uric_acid` as an alias, preserve that structure.

### 2. Unit definition prerequisite

Before adding any Free T4 conversion, verify both unit tokens are defined in `backend/ssot/units.yaml`:

```text
pmol/L
ng/dL
```

If the repo uses internal unit keys, add or verify coherent entries for:

```text
pmol_L
ng_dL
```

Do not add a conversion entry that references an undefined unit token.

Free T4 implementation is incomplete unless both the unit definitions and the `ng/dL ↔ pmol/L` conversion are registered and tested.

### 3. Critical runtime conversion dispatch requirement

Adding entries to `backend/ssot/units.yaml` is not sufficient.

Cursor must inspect and update the actual runtime conversion dispatch in:

```text
backend/core/units/registry.py
```

The implementation must ensure every Phase B conversion is reachable through the live conversion path, not merely declared in YAML.

The implementation must explicitly handle the current `registry.py` dispatch architecture.

Required `registry.py` work:

1. Add or verify `UnitEnum` / runtime unit-token support for:

```text
mg/dL
mmol/L
pmol/L
ng/dL
g/L
g/dL
µmol/L
umol/L
```

2. Add or verify frozen-set / grouping support for each Phase B biomarker group, using the style already present in `registry.py`:

```text
calcium / corrected_calcium
magnesium
free_t4
hemoglobin
urate / uric_acid
```

The groups must be used by runtime conversion dispatch, not only by tests.

3. Ensure every Phase B biomarker that uses strict unit conversion is included in `_STRICT_CONVERSION_BIOMARKERS` or the repo’s equivalent strict-conversion control set.

At minimum, verify or add:

```text
calcium
corrected_calcium
magnesium
free_t4
hemoglobin
urate
```

If aliases such as `uric_acid` or `haemoglobin` are handled before canonicalisation, ensure they resolve safely before conversion.

4. Add explicit `_get_conversion_factor()` branches, or the repo’s equivalent runtime dispatch branches, for:

```text
calcium / corrected_calcium: mg/dL ↔ mmol/L using 0.2495
magnesium: mg/dL ↔ mmol/L using 0.4114
free_t4: ng/dL ↔ pmol/L using 12.871
hemoglobin: g/dL ↔ g/L using 10, if not already active
urate: mg/dL ↔ µmol/L / umol/L using 59.5
```

5. Add tests proving the runtime conversion path is actually called.

Tests must fail if the implementation falls through to a generic passthrough path.

STOP if any Phase B conversion is only declared in YAML but not reachable through `registry.py` runtime dispatch.

### 4. Unit registry conversions

Add or verify governed conversions:

```text
calcium: mg/dL ↔ mmol/L using factor 0.2495
corrected_calcium: mg/dL ↔ mmol/L using factor 0.2495
magnesium: mg/dL ↔ mmol/L using factor 0.4114
free_t4: ng/dL ↔ pmol/L using factor 12.871
hemoglobin: g/dL ↔ g/L using factor 10
urate: mg/dL ↔ µmol/L using factor 59.5
```

Conversions must work for:

* value
* lower reference bound
* upper reference bound

where the uploaded reference range is in the same source unit.

### 5. Haemoglobin conversion status

The `g/dL ↔ g/L` conversion may already exist.

If present and correct:

* do not duplicate it
* verify it
* test it
* document it

### 6. Urate clarification

`urate` may already be recorded as `umol/L`. Treat this as the same unit family as `µmol/L`.

The main implementation work for urate is:

* add/verify `mg/dL ↔ µmol/L` conversion
* preserve or normalise `umol/L` / `µmol/L` equivalence
* verify `uric_acid → urate`
* verify BUN remains mapped to `urea`, not `urate`

This is not the same class of change as calcium, magnesium, Free T4, or haemoglobin. Do not overstate it in notes.

### 7. Reference-range coherence

Add or confirm tests that prove:

* value and reference range are converted coherently
* converted value and converted reference range end up in the same canonical unit
* incoherent value/reference families are rejected or marked unscored, not silently scored
* UK lab-derived ranges pass through unchanged
* Free T4 lab-specific range is preserved
* corrected calcium lab range is preserved

Do not use global fallback ranges to score these markers.

### 8. Scoring policy alignment

If these biomarkers are scored, align scoring policy units to the new UK/SI canonical unit only where the score bands are currently defined and safe to migrate.

Before changing any scoring band:

1. confirm the current band source unit
2. convert the band numerically using the same governed conversion
3. add before/after test vectors
4. confirm no polarity drift

If a biomarker has no scoring policy, do not invent one.

If scoring ranges are not lab-derived and the current HealthIQ policy requires lab-derived ranges, do not add generic scoring bands.

### 9. Haemoglobin atomicity requirement

Haemoglobin migration must be atomic.

Do not change `hemoglobin` canonical unit to `g/L` unless all of the following happen in the same sprint:

1. scoring policy unit changes to `g/L`
2. scoring band values are multiplied by 10
3. registry conversion supports `g/dL ↔ g/L`
4. tests prove `14.6 g/dL → 146 g/L`
5. tests prove UK pass-through `144 g/L` with range `130–175 g/L`
6. Sentinel/regression protection confirms haemoglobin scoring unit and band scale are aligned
7. `hemoglobin: "g/L"` is added to `LC_S8D_SSOT_SCORING_UNIT_ALIGNMENT` or the repo’s equivalent Sentinel alignment expectation

STOP if haemoglobin canonical unit and scoring bands would be left in different unit systems.

### 10. Alias protection

Ensure aliases remain correct:

```text
uric_acid → urate
urate ≠ urea
BUN → urea
blood urea nitrogen → urea
```

Add or update tests proving:

* `uric_acid` maps to `urate`
* `BUN` maps to `urea`
* `uric_acid` never maps to `urea`
* `BUN` never maps to `urate`

If these aliases already exist correctly, verify and document. Do not recreate unnecessarily.

### 11. Corrected calcium caveat

Implementation must allow conversion of a supplied corrected-calcium value.

Implementation must not calculate corrected calcium from total calcium and albumin unless there is already an explicit governed formula and albumin unit path.

Add a test or documentation note confirming:

```text
Corrected calcium unit conversion is implemented.
Corrected calcium recalculation is not implemented in this sprint.
```

### 12. Free T4 caveat

Implementation must allow `ng/dL → pmol/L` conversion.

Implementation must preserve lab/assay-specific reference ranges.

Add a test using:

```text
Free T4 16.8 pmol/L, range 12–22 pmol/L
```

Expected:

* value remains `16.8 pmol/L`
* range remains `12–22 pmol/L`
* no generic range replaces it

Add a test using:

```text
Free T4 1.2 ng/dL
```

Expected:

```text
15.45 pmol/L
```

with converted lab range if an uploaded ng/dL range is supplied.

### 13. Frontend conversion Sentinel/static-scan update

If LC-S8D / LC-S10B frontend no-conversion Sentinel patterns exist, update the relevant forbidden frontend conversion regex/pattern to include the new Phase B factors:

```text
0.2495
0.4114
12.871
59.5
```

Specifically inspect and update the repo’s `FORBIDDEN_FRONTEND_CONVERSION_RE` or equivalent frontend no-conversion Sentinel/static-scan pattern.

The purpose is to prevent these conversion constants from appearing in frontend code.

These constants are allowed only in backend registry/tests/docs/Sentinel metadata, not frontend runtime.

Do not edit frontend code.

### 14. Sentinel haemoglobin alignment update

Update `LC_S8D_SSOT_SCORING_UNIT_ALIGNMENT` or the repo’s equivalent Sentinel alignment expectation to include:

```text
hemoglobin: "g/L"
```

This must be done if haemoglobin scoring remains active and is migrated to `g/L`.

The Sentinel/regression expectation must protect against haemoglobin canonical unit and scoring-policy unit drifting apart.

## Required test vectors

Implement tests for at least:

| Biomarker         |       Input | Expected UK/SI output |
| ----------------- | ----------: | --------------------: |
| Calcium           | `9.4 mg/dL` |         `2.35 mmol/L` |
| Corrected calcium | `9.4 mg/dL` |         `2.35 mmol/L` |
| Magnesium         | `2.1 mg/dL` |         `0.86 mmol/L` |
| Free T4           | `1.2 ng/dL` |        `15.45 pmol/L` |
| Haemoglobin       | `14.6 g/dL` |             `146 g/L` |
| Urate / uric acid | `5.8 mg/dL` |        `345.1 µmol/L` |

Use appropriate tolerance for floating-point comparison.

Also test UK pass-through:

| Biomarker   |         Input |            Range | Expected  |
| ----------- | ------------: | ---------------: | --------- |
| Haemoglobin |     `144 g/L` |    `130–175 g/L` | unchanged |
| Uric Acid   |  `440 µmol/L` | `220–547 µmol/L` | unchanged |
| Free T4     | `16.8 pmol/L` |   `12–22 pmol/L` | unchanged |

## Phase gates

### Phase 1 — Inventory and mapping

Record current state for the six biomarkers:

* current SSOT unit
* current aliases
* current registry YAML support
* current runtime conversion dispatch support
* current `UnitEnum` / unit-token support
* current frozen-set / conversion-group support
* current `_STRICT_CONVERSION_BIOMARKERS` inclusion
* current scoring policy unit, if any
* current tests
* current Sentinel coverage
* whether conversion already exists or needs implementation
* whether unit definitions already exist or need creation
* whether the evidence report is committed in-repo

Output this to:

```text
docs/audit-papers/LC-S8F_phase_b_true_conversion_implementation_notes.md
```

Do not implement until inventory is complete.

### Phase 2 — Registry and SSOT conversion

Implement approved unit conversions, runtime conversion dispatch, and SSOT unit alignment.

STOP if:

* any factor differs from approved evidence
* any conversion references an undefined unit token
* any conversion is declared in YAML but not reachable in runtime dispatch
* any Phase B strict conversion biomarker is missing from `_STRICT_CONVERSION_BIOMARKERS` or equivalent control set
* any conversion requires assay-specific formula beyond approved arithmetic unit conversion
* any corrected-calcium recomputation is attempted
* urate/urea alias boundaries are unclear

### Phase 3 — Reference-range coherence

Implement or verify coherent conversion of lab-supplied reference ranges.

STOP if:

* a converted value can be scored against an unconverted range
* a lab-derived range can be overwritten by a generic range
* Free T4 reference range can be replaced by a universal range
* corrected calcium range handling is ambiguous

### Phase 4 — Scoring alignment

Align scoring-policy units only where applicable and safe.

STOP if:

* scoring bands lack clear current unit authority
* migration would introduce generic ranges contrary to lab-derived-range policy
* polarity changes unintentionally
* a biomarker without scoring policy would require inventing new generic bands
* haemoglobin canonical unit is changed to `g/L` while scoring bands remain numerically in `g/dL`
* haemoglobin Sentinel scoring-unit alignment is not updated to `g/L`

### Phase 5 — Sentinel and regression protection

Add or update Sentinel/regression protection for:

* Phase B canonical unit drift
* missing Phase B conversion authority
* runtime conversion dispatch reachability
* Phase B factors absent from frontend runtime
* urate/urea alias separation
* Free T4 assay/reference-range preservation
* corrected-calcium no-recompute rule
* lab-derived range preservation
* haemoglobin scoring unit/band alignment
* `FORBIDDEN_FRONTEND_CONVERSION_RE` or equivalent frontend no-conversion pattern includes:

  * `0.2495`
  * `0.4114`
  * `12.871`
  * `59.5`
* `LC_S8D_SSOT_SCORING_UNIT_ALIGNMENT` or equivalent includes:

  * `hemoglobin: "g/L"`

Do not duplicate existing Sentinel protections unnecessarily.

### Phase 6 — Final validation

Run required test commands and record outputs.

## Required validation commands

Run:

```powershell
python -m pytest backend/tests/unit/test_unit_registry.py -q
python -m pytest backend/tests/unit/test_scoring_rules.py -q
python -m pytest backend/tests/regression/test_lc_s8_biomarker_unit_reference_incoherence_regression.py -q
python -m pytest backend/tests/regression/test_lc_s8d_unit_governance_sentinel.py -q
python -m pytest backend/tests/unit/test_hba1c_governance.py -q
```

If a new dedicated Phase B test file is created, run it explicitly, for example:

```powershell
python -m pytest backend/tests/regression/test_lc_s8f_phase_b_true_conversions.py -q
```

Run a targeted alias scan or test proving:

```text
BUN → urea
uric_acid → urate
BUN ≠ urate
uric_acid ≠ urea
```

Run a repository scan for accidental frontend conversion if frontend files are unexpectedly touched or if Sentinel/static scan protection is updated:

```powershell
Select-String -Path frontend/app/**/*.ts,frontend/app/**/*.tsx -Pattern "0.2495|0.4114|12.871|59.5|mg/dL|g/dL|ng/dL|convert" -CaseSensitive:$false
```

Frontend changes should not occur.

## Acceptance criteria

This sprint is complete only if:

* the Phase B evidence report exists and is committed in-repo
* all six Phase B biomarkers have approved UK/SI canonical unit handling
* governed conversion factors are implemented exactly
* required unit definitions exist before conversion entries reference them
* runtime conversion dispatch actually reaches every Phase B conversion
* Phase B biomarkers are included in `_STRICT_CONVERSION_BIOMARKERS` or equivalent where required
* tests prove conversions do not fall through to passthrough behaviour
* lab-derived reference ranges are preserved
* converted lab reference ranges are converted coherently with values
* Free T4 preserves assay/lab-specific reference ranges
* corrected calcium is not recomputed
* urate/uric acid remains separate from urea/BUN
* UK lab examples pass through unchanged
* haemoglobin scoring bands are migrated to `g/L` if haemoglobin scoring is retained
* haemoglobin canonical unit and scoring bands are not left in different unit systems
* haemoglobin Sentinel scoring alignment expects `g/L`
* scoring policy is aligned only where safe and justified
* tests cover all approved conversion vectors
* Sentinel/regression protections are updated
* frontend no-conversion protection includes Phase B conversion factors
* no frontend conversion logic is introduced
* no Phase B global/default reference ranges are introduced
* no unrelated launch-core behaviours are changed

## Required documentation output

Create or update:

```text
docs/audit-papers/LC-S8F_phase_b_true_conversion_implementation_notes.md
```

It must include:

1. Phase 1 inventory
2. Evidence source used
3. Evidence file committed status
4. Files changed
5. Conversion factors implemented
6. Unit definitions added or verified
7. `UnitEnum` / unit-token updates
8. Frozen-set / biomarker-group updates
9. `_STRICT_CONVERSION_BIOMARKERS` updates
10. Runtime conversion dispatch changes
11. Reference-range handling decision
12. Scoring-policy decision per biomarker
13. Haemoglobin scoring migration result
14. Haemoglobin Sentinel scoring-alignment update
15. Corrected-calcium caveat
16. Free T4 assay/range caveat
17. Urate-vs-urea alias protection
18. Frontend no-conversion Sentinel/static-scan update
19. Tests run
20. Sentinel/protection changes
21. Deferred risks
22. Final implementation verdict

This document must map directly to implementation and tests. It is not a passive status artefact.

## Cursor completion requirements

When implementation is complete, Cursor must:

1. Run required validation commands.
2. Update the implementation notes.
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

Cursor may not self-certify clinical correctness, architecture correctness, merge readiness, launch readiness, or final approval.

````
