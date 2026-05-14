---
work_id: LC-S8-BIOMARKER-UNIT-RANGE-NORMALISATION-QA
branch: sprint8/biomarker-unit-range-normalisation-qa
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# LC-S8 — Biomarker Unit / Range Normalisation QA

## Objective

Fix the biomarker value/unit/reference-range coherence defect class and add permanent guardrails so Layer B can never silently score mixed-unit biomarker data.

This sprint addresses the post-UAT issues where the frontend showed examples such as:

- Haemoglobin `144 g/dL` with reference range `130–175 g/L`
- Haematocrit `0.4 %` with reference range `0.35–0.48 L/L`
- HbA1c appearing in both `%` and `mmol/mol`
- ratio and biomarker display unit inconsistencies

This is not a frontend polish sprint.

The architectural rule is:

> Mixed input units are allowed. Mixed-unit scoring is not allowed.

Layer A must normalise biomarker values and reference ranges into coherent canonical analytical units before Layer B performs scoring or interpretation.

## Authority and evidence

Primary implementation authority:

- this LC-S8 SOP prompt

Primary architecture authorities:

- `architecture/ADR-002-deterministic-analysis-engine.md`
- `architecture/ADR-001-platform-non-negotiables.md`
- `Master_PRD_v5.2.md`

Primary investigation evidence:

- `docs/audit-papers/LC-S8_biomarker_unit_range_normalisation_preflight.md`

Key authority principles:

- Layer A is responsible for canonicalisation and unit normalisation.
- Layer B performs calculations only on canonical/base units.
- Layer C/frontend must not perform analytical unit conversion.
- Lab-provided reference ranges remain sovereign, but only after value/range unit coherence is established.
- Unknown or incompatible units must not be silently scored.

Master PRD v5.2 states that all biomarker values must be converted through a deterministic two-step unit model, with internal base-unit standardisation before Layer B calculations and presentation conversion only afterwards. It also explicitly says Layer B performs all mathematical operations exclusively on base units. :contentReference[oaicite:0]{index=0}

The LC-S8 preflight found that current scoring can compare numeric values to numeric lab bounds without a general unit-coherence guard, except for HbA1c-specific harmonisation. It also found that non-strict biomarkers and one-sided reference ranges can allow value/reference unit splits through to scoring and display. :contentReference[oaicite:1]{index=1}

## Risk classification

Risk level: HIGH.

Reason:

This package may touch:

- `backend/core/units/`
- `backend/core/pipeline/orchestrator.py`
- `backend/core/scoring/`
- `backend/ssot/`
- canonicalisation-adjacent behaviour
- scoring/reference-range logic
- Sentinel regression coverage

These are HIGH-risk surfaces under the Automation Bus SOP.

Claude audit and GPT architectural review are required before merge.

## Strategic principle

Layer A must produce unit-coherent analytical input.

Layer B must never score a biomarker unless:

1. the biomarker value unit and reference range unit are identical, or
2. both have been deterministically converted into the same canonical analytical unit.

If unit coherence cannot be proven, the marker must be unscored with an explicit reason. It must not receive a normal-looking score or status.

## Task 1 — Confirm authoritative unit policy before changing code

Inspect and record the current authority chain:

- `architecture/ADR-002-deterministic-analysis-engine.md`
- `architecture/ADR-001-platform-non-negotiables.md`
- `Master_PRD_v5.2.md`
- `backend/ssot/biomarkers.yaml`
- `backend/ssot/units.yaml`
- `backend/core/units/registry.py`

Required:

- confirm current canonical unit source
- confirm conversion matrix source
- identify any SSOT unit entries that conflict with ADR/Master PRD principles
- specifically inspect:
  - haemoglobin
  - haematocrit
  - HbA1c
  - testosterone
  - core lipid markers
  - common ratios

Do not create a second SSOT.

## Task 2 — Define and enforce value/reference unit coherence

Implement backend unit-coherence protection before scoring.

Required behaviour:

A biomarker may proceed to scoring only if:

- value unit and reference range unit are coherent after Layer A normalisation, or
- reference range is absent and the marker is explicitly treated as unscored / range-missing according to existing policy.

A biomarker must not be scored if:

- value unit and reference range unit differ and are not deterministically converted
- either unit is missing or ambiguous and no governed inference is available
- only one side was converted and the other remains raw
- one-sided reference range unit cannot be made coherent with value unit

Required output:

- deterministic unscored reason, for example:
  - `unit_reference_range_incoherent`
  - or an existing naming pattern if one already exists

Do not silently coerce.

Do not invent clinical conversions outside the governed unit registry.

## Task 3 — Fix haemoglobin unit coherence

Known UK AB source:

- Haemoglobin should be treated as `144 g/L` against `130–175 g/L`.

Current defect:

- Browser showed `144 g/dL` with `130–175 g/L`.

Required:

- inspect `backend/ssot/biomarkers.yaml` haemoglobin unit
- inspect `backend/ssot/units.yaml` for haemoglobin-compatible mass concentration conversions
- decide whether canonical internal unit should be `g/L` in alignment with ADR/Master PRD and UK lab source
- ensure value and reference range emerge coherent
- ensure scoring uses coherent units
- ensure frontend display does not show `144 g/dL` for this UK panel

If changing SSOT unit would cause broad historical fixture drift, STOP and report before proceeding.

## Task 4 — Fix haematocrit unit coherence

Known UK AB source:

- Haematocrit: `0.438 L/L`
- Reference range: `0.35–0.48 L/L`

Current defect:

- Browser showed `0.4 %` with range `0.35–0.48 L/L`.

Required:

- define canonical analytical unit for haematocrit
- preferred for this UK panel: preserve `L/L` as canonical/display unless a governed `%` conversion is implemented
- never display `0.438` as `%`
- if display is `%`, convert both value and range together:
  - `0.438 L/L` → `43.8%`
  - `0.35–0.48 L/L` → `35–48%`

Do not implement frontend-only clinical conversion unless backend supplies coherent display values or an existing governed conversion utility is used.

## Task 5 — Fix HbA1c dual-unit handling

Known UK AB source includes both:

- HbA1c `%`: `4.53%`, reference `0–5.7%`
- HbA1c `mmol/mol`: `26 mmol/mol`, with UK threshold bands:
  - normal `<39`
  - prediabetes `39–47`
  - diabetes `≥48`

Required:

- treat these as dual-unit representations of one biomarker, not separate independent findings
- define canonical analytical unit for UK internal scoring, preferably `mmol/mol`
- preserve `%` as source/display secondary metadata if supplied
- never score `%` value against `mmol/mol` thresholds
- never score `mmol/mol` value against `%` bounds
- ensure duplicate HbA1c entries do not produce duplicate or contradictory output

If the current schema cannot preserve secondary display values safely, STOP and report a recommended contract extension rather than hacking around it.

## Task 6 — Ratios and derived markers

Inspect and protect:

- `tc_hdl_ratio`
- `tg_hdl_ratio`
- `ldl_hdl_ratio`
- `apob_apoa1_ratio`
- `urea_creatinine_ratio`
- `testosterone_free_testosterone_ratio`
- `non_hdl_cholesterol`

Required:

- ratios should be unitless or `ratio`
- `non_hdl_cholesterol` is not unitless; it is a concentration marker
- computed ratios must run only after unit normalisation
- lab-supplied ratios must not be overwritten
- ratio reference bounds must not inherit inappropriate concentration units

Add tests for ratio unit handling.

## Task 7 — Unit normalisation audit trail

Ensure the backend records enough audit information to prove what happened.

Required audit metadata, where supported by existing structures:

- source value
- source unit
- canonical value
- canonical unit
- source reference range
- canonical/reference range used for scoring
- conversion applied
- unit registry version
- unscored reason if unit coherence fails

Do not introduce a large DTO/schema change unless necessary. If schema change is needed, STOP and report.

## Task 8 — Frontend display policy alignment

Frontend must remain renderer-only.

Required:

- keep LC-S7 defensive display handling
- ensure frontend does not perform clinical unit conversion
- ensure frontend displays the coherent value/range supplied by backend
- where backend marks a marker unscored due to unit incoherence, frontend should show clear neutral wording rather than a misleading score

Allowed frontend work:

- label display improvements
- neutral display of unscored reason
- suppression of incompatible reference range if backend still flags it

Not allowed:

- frontend converting `g/dL` to `g/L` for scoring purposes
- frontend converting haematocrit fraction to percent unless backend provides the display value or a governed display field
- frontend hiding backend scoring errors in a way that makes the result look normal

## Task 9 — Tests

Add or update tests for:

### Unit registry / Layer A

- haemoglobin `144 g/L` with `130–175 g/L` stays coherent
- haemoglobin `14.4 g/dL` with `13–17.5 g/dL` stays coherent
- haemoglobin mixed `14.4 g/dL` with `130–175 g/L` converts coherently or becomes unscored
- haematocrit `0.438 L/L` with `0.35–0.48 L/L` stays coherent
- haematocrit `%` input converts only through governed conversion
- one-sided ranges do not silently create incoherent scoring

### HbA1c

- `%` and `mmol/mol` dual reporting maps to one canonical biomarker
- canonical scoring uses one governed unit
- incompatible HbA1c unit/range combinations become unscored with explicit reason
- display metadata does not create duplicate findings

### Scoring

- no marker is scored if value unit and reference range unit are incoherent
- status is not calculated from incoherent numerics
- unscored reason is explicit and deterministic

### Ratios

- derived ratios are unitless / `ratio`
- ratio policy bounds use `ratio`
- non-HDL remains a concentration marker
- lab-supplied ratios are not overwritten

### Frontend

- biomarker cards do not display incoherent value/range unit pairs
- haemoglobin displays coherently
- haematocrit displays coherently
- HbA1c does not mix `%` value with `mmol/mol` range
- unscored unit-coherence markers do not show normal-looking scores

## Task 10 — Sentinel defect class

Add a new Sentinel defect class:

```text
biomarker_value_reference_unit_incoherence
````

Purpose:

Prevent silent regression where value, unit, reference range and scoring become incoherent.

Required:

* backend deterministic regression test
* Sentinel pack entry
* runner mapping
* must detect at least:

  * haemoglobin mixed-unit case
  * haematocrit fraction/percent case
  * HbA1c dual-unit safety
  * incompatible unit pair not silently scored

Run Sentinel for the new defect class and report 0 issues / 0 gaps.

## Expected files touched

Expected backend:

* `backend/core/units/registry.py`
* `backend/core/pipeline/orchestrator.py`
* `backend/core/scoring/rules.py`
* `backend/core/scoring/engine.py`
* `backend/core/analytics/primitives.py`
* possibly `backend/core/analytics/ratio_registry.py`
* `backend/ssot/biomarkers.yaml`
* `backend/ssot/units.yaml`
* relevant backend unit/regression tests

Expected frontend:

* `frontend/app/components/biomarkers/BiomarkerDials.tsx`
* possibly frontend biomarker display tests

Expected Sentinel:

* `sentinel/packs/escaped_defects_v1.json`
* `sentinel/sentinel_runner.py`
* new backend regression test under `backend/tests/regression/`

Expected docs:

* `docs/sprints/LC-S8_biomarker_unit_range_normalisation_qa_completion_2026-05.md`

Not expected:

* Knowledge Bus packages
* questionnaire files
* narrative compiler files
* report retail components unrelated to biomarker cards
* Automation Bus control-plane scripts
* database migrations unless STOP and approved

## Stop conditions

STOP and report before implementation if:

* authoritative canonical unit policy cannot be resolved
* fixing haemoglobin requires broad SSOT migration beyond this sprint
* fixing haematocrit requires choosing between `L/L` and `%` without clear policy
* HbA1c dual-unit handling requires DTO/schema extension
* correcting unit normalisation would change scores across many fixtures without a migration/replay policy
* frontend conversion is the only available fix
* unit conversion factor is missing and cannot be added safely
* lab-range sovereignty conflicts with canonical unit coherence
* any Knowledge Bus change appears necessary
* any Automation Bus control-plane script change appears necessary
* old analyses require migration before new analyses can be made safe

## Explicit non-goals

Do not:

* change clinical interpretation thresholds except where unit conversion makes existing thresholds coherent
* change signal ranking logic
* change signal activation logic except to prevent incoherent scoring
* change questionnaire logic
* change Knowledge Bus assets
* change narrative/report prose
* implement US/customer locale display conversion broadly
* build a full locale-preference system
* migrate historical stored analyses unless explicitly approved
* add fallback parsers
* silently coerce unsupported units

## Validation

Run targeted backend tests first:

* unit registry tests
* scoring rules tests
* orchestrator DTO tests
* HbA1c tests
* ratio registry tests
* new regression tests

Run targeted frontend biomarker display tests if frontend touched.

Run Sentinel for:

```bash
python sentinel/sentinel_runner.py --defect-class biomarker_value_reference_unit_incoherence
```

Run existing relevant Sentinel guards if touched paths overlap.

Run Automation Bus finish:

```bash
python backend/scripts/run_work_package.py finish
```

Report all commands and results.

## Completion note

Create:

`docs/sprints/LC-S8_biomarker_unit_range_normalisation_qa_completion_2026-05.md`

It must record:

* canonical unit policy confirmed
* SSOT unit changes made
* unit conversion changes made
* haemoglobin outcome
* haematocrit outcome
* HbA1c outcome
* ratio outcome
* scoring safety outcome
* Sentinel defect class added
* tests run
* known limitations
* deferred items, especially US/customer display conversion if not implemented
* confirmation whether old analyses are affected or only new analyses

## Closure evidence required

Before finish, report:

* branch
* work_id
* files changed
* canonical unit policy confirmed
* whether Layer B now receives only unit-coherent values/ranges
* whether incoherent markers become unscored
* haemoglobin test outcome
* haematocrit test outcome
* HbA1c test outcome
* ratio test outcome
* frontend display outcome
* Sentinel outcome
* tests run and results
* confirmation no Knowledge Bus files changed
* confirmation no questionnaire files changed
* confirmation no narrative compiler files changed
* confirmation no Automation Bus control-plane scripts changed

## Final expected outcome

After LC-S8, HealthIQ AI must no longer silently score or display biomarker value/reference-range pairs with incoherent units.

Layer A must enforce unit coherence.

Layer B must calculate only on coherent canonical analytical values.

Layer C/frontend must render coherent backend output and must not perform analytical unit conversion.

````