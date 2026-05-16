---
work_id: LC-S8B
branch: launch-core/lc-s8b-uk-canonical-unit-policy-validation
risk_level: HIGH
execution_model: SINGLE_PHASE
change_type: CONTENT
---

# LC-S8B — UK Canonical Unit Policy Validation

## Purpose

Create a governed, evidence-backed UK canonical biomarker unit policy table before any SSOT, registry, parser, scorer, fixture, Sentinel, or frontend implementation work is attempted.

This is a policy-validation sprint only.

The immediate issue is not simply that platelet count is unscored. The deeper issue is that HealthIQ AI does not yet have a locked, verified, UK-first canonical biomarker unit policy that is enforced consistently across:

- `backend/ssot/biomarkers.yaml`
- `backend/ssot/units.yaml`
- `backend/core/units/registry.py`
- Layer A unit/reference canonicalisation
- Layer B scoring coherence
- Layer C display behaviour
- tests and Sentinel guards

This sprint must produce the decision table that authorises later implementation.

## Absolute scope boundary

This sprint must not change runtime behaviour.

Allowed changes:

- Create one policy-validation document:
  - `docs/audit-papers/LC-S8B_uk_canonical_unit_policy_validation.md`

Prohibited changes:

- Do not edit `backend/ssot/biomarkers.yaml`
- Do not edit `backend/ssot/units.yaml`
- Do not edit `backend/core/units/registry.py`
- Do not edit parsers
- Do not edit scoring logic
- Do not edit frontend rendering
- Do not edit fixtures
- Do not edit Sentinel
- Do not add conversion factors
- Do not add aliases
- Do not “fix” platelet count directly
- Do not create a second SSOT
- Do not treat this document as runtime authority

If any implementation change appears necessary, STOP and report the proposed follow-on sprint rather than making the change.

## Governing architecture

HealthIQ AI is a deterministic metabolic / blood-panel intelligence platform.

Layer ownership remains:

- Layer A owns raw lab input handling, biomarker canonicalisation, unit normalisation, canonical value formation, and reference-range coherence.
- Layer B owns scoring, signal evaluation, ranking, and structured analytical truth.
- Layer C owns narrative and presentation only.
- Frontend is renderer-only.

Unit conversion and coherence repair must not move into Layer B, Layer C, or frontend.

## Required authority preflight

Before writing the policy document, verify the current branch and authority files.

Run and record:

```powershell
git branch --show-current
git status --short
git log --oneline -n 5
````

Then verify the following files exist and read their relevant content:

* `architecture/ADR-002-deterministic-analysis-engine.md`
* `architecture/ADR-001-platform-non-negotiables.md`
* `Master_PRD_v5.2.md`
* `backend/ssot/biomarkers.yaml`
* `backend/ssot/units.yaml`
* `backend/core/units/registry.py`
* `docs/audit-papers/LC-S8_biomarker_unit_range_normalisation_preflight.md`
* `docs/audit-papers/LC-S8A_uk_canonical_unit_ssot_lockdown_audit.md`

If any path has moved, locate the current equivalent and record the resolved path. If no equivalent exists, STOP.

## Baseline reality check

Before writing recommendations, confirm the current baseline still contains unresolved UK/SI canonical-unit policy issues.

At minimum, inspect `backend/ssot/biomarkers.yaml` for current canonical units containing:

* `K/μL`
* `K/uL`
* `g/dL`
* `mg/dL`
* `ng/dL`
* `mEq/L`
* `%`

PowerShell search pattern:

```powershell
Select-String -Path backend/ssot/biomarkers.yaml -Pattern "K/μL|K/uL|g/dL|mg/dL|ng/dL|mEq/L|%" -Context 3,3
```

Also inspect unit registration / equivalence coverage:

```powershell
Select-String -Path backend/ssot/units.yaml,backend/core/units/registry.py -Pattern "K/μL|K/uL|10\^9/L|x10\^9/L|g/dL|g/L|mg/dL|mmol/L|ng/dL|pmol/L|mEq/L|%" -Context 3,3
```

If the baseline no longer contains unresolved UK/SI canonical-unit policy issues, STOP and write a short no-op cancellation note instead of producing an implementation-style policy.

## Required evidence standard

Do not rely on Claude’s LC-S8A audit as implementation authority.

For every proposed unit policy row, provide evidence from at least one authoritative source, preferably:

* UK NHS laboratory test directory
* UK NHS Trust pathology handbook
* NICE / UK clinical standard
* professional clinical chemistry / haematology standard
* project-owned lab source panel where available

For higher-risk true conversion changes, also require conversion-factor validation from a reliable clinical or laboratory source.

If evidence cannot be found, mark the row:

`NEEDS_CONVERSION_FACTOR_VALIDATION`

or:

`BLOCKED`

Do not infer conversion factors.

## Required policy table

Create this table in:

`docs/audit-papers/LC-S8B_uk_canonical_unit_policy_validation.md`

Use this exact column structure:

| Biomarker ID | Display name | Current SSOT unit | Current accepted input units / aliases | Proposed UK canonical analytical unit | Proposed UK launch display unit | Evidence source(s) | Conversion type | Risk | Decision | Rationale | Follow-on sprint |
| ------------ | ------------ | ----------------- | -------------------------------------- | ------------------------------------- | ------------------------------- | ------------------ | --------------- | ---- | -------- | --------- | ---------------- |

Allowed `Conversion type` values:

* `LABEL_EQUIVALENCE_1_TO_1`
* `TRUE_SCALE_CONVERSION`
* `DUAL_REPRESENTATION_POLICY`
* `DISPLAY_ONLY_TRANSFORMATION`
* `NO_CHANGE_REQUIRED`
* `UNKNOWN_REQUIRES_VALIDATION`

Allowed `Risk` values:

* `LOW`
* `MEDIUM`
* `HIGH`
* `BLOCKED`

Allowed `Decision` values:

* `APPROVED_FOR_IMPLEMENTATION`
* `APPROVED_LABEL_EQUIVALENCE_ONLY`
* `NEEDS_POLICY_DECISION`
* `NEEDS_CONVERSION_FACTOR_VALIDATION`
* `DEFER_NOT_LAUNCH_CRITICAL`
* `BLOCKED`

## Required biomarker coverage

At minimum, evaluate all biomarkers flagged by LC-S8A and any equivalent marker names present in the current SSOT.

Required minimum set:

### Full blood count / haematology

* `hemoglobin`
* `haematocrit` / `hematocrit`
* `red_blood_cells`
* `white_blood_cells`
* `platelets`
* neutrophils
* lymphocytes
* monocytes
* eosinophils
* basophils
* any other absolute differential count currently present in SSOT

### Electrolytes / renal / mineral

* `sodium`
* `potassium`
* `chloride`
* bicarbonate / CO2 if present
* `calcium`
* `corrected_calcium` / `adjusted_calcium`
* `magnesium`
* phosphate if present
* urea if present
* creatinine if present

### Endocrine / metabolic

* `free_t4`
* TSH if present
* `hba1c`
* `hba1c_pct`
* glucose
* total cholesterol
* HDL
* LDL
* triglycerides

Do not limit the scan only to this list if the SSOT contains other obvious US-style units.

## Special policy handling

### HbA1c

Treat HbA1c as a dedicated policy decision.

The UK standard is generally IFCC `mmol/mol`, but HealthIQ may receive both:

* HbA1c %
* HbA1c mmol/mol

These are two representations of the same biomarker, not two independent findings.

Do not approve implementation unless the policy document explicitly decides:

* whether `hba1c` canonical analytical unit should be `mmol/mol`
* whether `%` remains accepted input
* whether `%` is allowed as secondary display
* how duplicate HbA1c representations are de-duplicated
* whether current HbA1c harmonisation code remains valid

Likely decision unless fully evidenced:

`NEEDS_POLICY_DECISION`

### Haematocrit

Distinguish analytical canonical unit from display unit.

UK source panels may report haematocrit as `L/L` or equivalent fraction.

Display as `%` may be acceptable only if value and reference range are both transformed coherently.

The policy must explicitly prevent:

* `0.438 %`
* `0.438` with `%` label
* value in fraction with reference range in percent
* value in percent with reference range in fraction

### Haemoglobin

UK lab panels commonly report haemoglobin as `g/L`.

Current SSOT may use `g/dL`.

Do not approve implementation unless the policy clearly separates:

* accepted input units
* canonical analytical unit
* launch display unit
* conversion direction
* fixture impact
* Sentinel impact

### Platelets / WBC / absolute differentials

These are likely label/equivalence issues because `K/μL` and `10^9/L` are numerically equivalent for cell counts.

However, do not assume.

Validate and classify as:

`APPROVED_LABEL_EQUIVALENCE_ONLY`

only if evidence confirms numerical equivalence and no scale conversion is needed.

### Calcium / magnesium / free T4

These are high-risk true conversion areas.

Do not approve implementation unless conversion factors are validated.

Likely decision unless fully evidenced:

`NEEDS_CONVERSION_FACTOR_VALIDATION`

## Required document structure

The document must contain:

1. Executive summary
2. Current defect statement
3. Authority files reviewed
4. Baseline SSOT unit inventory
5. Evidence methodology
6. Full policy-validation table
7. Rows approved for safe implementation
8. Rows requiring policy decision
9. Rows requiring conversion-factor validation
10. Rows deferred or blocked
11. Proposed follow-on sprint split
12. Required test and Sentinel guard recommendations
13. Explicit non-authority warning

## Required follow-on sprint split

The policy document must recommend a split like this, adjusting only if evidence demands:

### LC-S8C — Safe UK Unit Label/Equivalence Implementation

Scope likely limited to:

* platelets
* WBC
* absolute differential counts
* RBC if only representation/equivalence is needed

Only rows with `APPROVED_LABEL_EQUIVALENCE_ONLY` may enter LC-S8C.

### LC-S8D — True Conversion Unit Implementation

Scope likely includes:

* haemoglobin
* calcium
* corrected/adjusted calcium
* magnesium
* free T4
* electrolytes if actual conversion logic is needed

Only rows with fully validated conversion factors may enter LC-S8D.

### LC-S8E — HbA1c Dual-Representation Policy and Implementation

Scope:

* HbA1c mmol/mol versus %
* duplicate representation handling
* display policy
* harmonisation tests

### LC-S8F — Canonical Unit Sentinel Lockdown

Scope:

* Sentinel rule preventing forbidden UK-launch canonical units from re-entering SSOT
* fixture proving value/reference/unit coherence
* no frontend repair logic

## Required test and Sentinel recommendations

Do not implement tests in this sprint, but specify what later sprints must add.

At minimum, recommend:

* SSOT canonical-unit policy test
* unit registry equivalence test
* value/reference coherence tests
* UK sample panel regression test
* HbA1c dual-input de-duplication test
* Sentinel guard for forbidden canonical units
* Sentinel guard for mixed value/reference units
* frontend no-repair assertion

## STOP conditions

STOP immediately if:

* the branch does not match the front matter branch
* authority paths cannot be resolved
* `backend/ssot/biomarkers.yaml` is not the current biomarker SSOT
* `backend/ssot/units.yaml` or `backend/core/units/registry.py` are not the current unit authorities
* a duplicate unit authority exists and cannot be reconciled
* evidence cannot be found for a proposed policy row
* the work would require non-doc changes
* implementation changes are required to complete the task
* any conversion factor would need to be invented
* HbA1c policy cannot be resolved safely
* git diff shows any changed file outside `docs/audit-papers/LC-S8B_uk_canonical_unit_policy_validation.md`

## Validation commands before completion

Run:

```powershell
git diff --name-only
git diff -- docs/audit-papers/LC-S8B_uk_canonical_unit_policy_validation.md
git status --short
```

Expected changed file:

```text
docs/audit-papers/LC-S8B_uk_canonical_unit_policy_validation.md
```

If any other file is changed, STOP and report.

## Acceptance criteria

This sprint is complete only when:

* `docs/audit-papers/LC-S8B_uk_canonical_unit_policy_validation.md` exists
* the full required policy table is present
* every proposed unit change has evidence
* every row has a decision value
* no implementation files are changed
* rows approved for implementation are clearly separated from rows requiring further decision
* HbA1c is not casually folded into generic unit conversion
* calcium/magnesium/free T4 are not approved without conversion-factor validation
* platelet/WBC equivalence is validated before approval
* follow-on sprint split is explicit
* test and Sentinel recommendations are explicit
* git diff confirms docs-only scope

---