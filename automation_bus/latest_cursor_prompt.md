---
work_id: LC-S11A
branch: launch-core/lc-s11a-trust-blocker-correction
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# LC-S11A — Launch-Core Trust Blocker Correction

## Classification

This is a HIGH-risk MIXED correction sprint.

Reason: this sprint may touch signal logic, scoring behaviour, domain-card narrative gating, legacy output gating, regression tests, Sentinel protections, and launch-core report payload behaviour.

This is not a product expansion sprint.

This sprint fixes four trust-blocking defects found during LC-S11 forensic human UAT before external human testing can proceed. The forensic audit judged the current launch-core result as `PASS WITH GAPS`, with specific blockers around legacy `insights[]`, unsupported blood sugar narrative, ApoA1 directionality, and low-ALT liver severity. :contentReference[oaicite:0]{index=0}

## Purpose

Correct the four bounded trust blockers identified in:

```text
docs/audit-papers/LC-S11_forensic_human_uat_audit.md
````

The four defects are:

1. Legacy `insights[]` placeholder surface still active.
2. Blood sugar domain card presents “early impaired sugar and lipid handling” despite no active blood sugar signals.
3. ApoA1 elevated is being treated as a cardiovascular risk driver.
4. Low ALT is driving an alarming liver score / “Needs review” state.

The goal is to remove false confidence, unsupported narrative, clinically wrong marker directionality, and disproportionate false alarms before external user testing.

## Governing evidence

Read before editing:

```text
docs/audit-papers/LC-S11_forensic_human_uat_audit.md
docs/planning-papers/healthiq_launch_core_transformation_plan_FINAL.md
docs/audit-papers/LC-S10B_protection_of_proven_slice_notes.md
docs/audit-papers/LC-S8F_phase_b_unit_conversion_uat.md
docs/audit-papers/LC-S8G_uploaded_unit_display_fidelity_notes.md
```

Also inspect the downloaded/live analysis payload or regenerated equivalent for:

```text
analysis_id=c440dfa2-12a1-4e29-95a5-ee07a2397c59
```

If the exact analysis is not locally available, use the saved JSON artefact if present, or regenerate an equivalent AB panel output. Do not invent evidence.

## Strategic boundaries

This sprint must not:

* broaden WHY Wave 2
* introduce Gemini/LLM narrative generation
* redesign the frontend
* rewrite domain scoring globally
* add new clinical claims without existing governed support
* suppress real clinically relevant findings just to improve appearance
* change unit governance
* change LC-S8F / LC-S8G display fidelity
* change lifestyle/statin modifier behaviour
* create demo-only logic
* add fallback parser logic

Every change must be tied to one of the four LC-S11A trust blockers.

## Mandatory preflight before editing

Run and record:

```powershell
git branch --show-current
git status --short
git log --oneline -n 8
```

Then verify:

```powershell
Test-Path automation_bus/state/work_package_active.json
```

Read `automation_bus/state/work_package_active.json` and confirm:

* `work_id` is `LC-S11A`
* branch is `launch-core/lc-s11a-trust-blocker-correction`

If the token is missing or mismatched, STOP:

```text
Kernel start not executed or work package mismatch.
```

## Authority preflight

Before modifying files, identify and record authoritative paths for:

1. Legacy `insights[]` generation and frontend/API exposure.
2. Consumer domain score/card generation.
3. Blood sugar/metabolic domain card narrative source.
4. ApoA1 signal definition, directionality, and display/framing.
5. ALT scoring/status/domain contribution logic.
6. Domain score aggregation logic.
7. Sentinel/regression tests protecting launch-core outputs.
8. JSON/API result DTO path.
9. Frontend result card/domain-card rendering path.
10. Knowledge Bus or SSOT assets backing ApoA1, liver, metabolic, and cardiovascular domain logic.

STOP if an authority source is ambiguous or duplicated.

Do not create a second authority source.

## Potentially allowed files

Only edit files needed for these four trust blockers.

Potentially allowed:

```text
backend/core/analytics/**/*
backend/core/scoring/**/*
backend/core/pipeline/**/*
backend/core/dto/**/*
backend/app/routes/analysis.py

backend/ssot/**/*
knowledge_bus/**/* only if correcting existing governed metadata, not broad enrichment

frontend/app/(app)/results/**/*
frontend/app/components/**/*
frontend/app/lib/**/*
frontend/app/types/**/*

backend/tests/unit/**/*
backend/tests/regression/**/*
frontend/tests/**/*

sentinel/packs/**/*
docs/audit-papers/LC-S11A_trust_blocker_correction_notes.md
```

## Forbidden changes

Do not edit:

```text
backend/scripts/run_work_package.py
backend/scripts/golden_gate_local.py
backend/scripts/update_cursor_status.py
automation_bus/latest_gate_evidence.json
automation_bus/latest_gate_output.txt
automation_bus/latest_cursor_status.json
```

Do not:

* alter LC-S8F unit conversion factors
* alter LC-S8G uploaded-unit display fidelity
* change haemoglobin/urate/Free T4/calcium/magnesium conversion behaviour
* introduce generic reference ranges
* recompute corrected calcium
* map urate to urea
* add frontend conversion maths
* remove domain cards wholesale to hide defects
* delete evidence rather than fixing logic/gating
* create broad new scoring framework

## Phase 1 — Investigation and correction plan

Create or update:

```text
docs/audit-papers/LC-S11A_trust_blocker_correction_notes.md
```

Record:

* current branch / git state
* files inspected
* exact authority source for each defect
* proposed correction
* planned tests
* STOP risks

Required table:

| Defect | Current evidence | Authority source | Proposed fix | Tests |
| ------ | ---------------- | ---------------- | ------------ | ----- |

Do not implement until this inventory is complete.

---

# Defect 1 — Gate or remove legacy `insights[]`

## Problem

The LC-S11 audit found legacy `insights[]` placeholder entries still active, including generic text such as:

```text
Metabolic focus: summarise structured signals; review with your clinician
Cardiovascular focus: summarise structured signals; review with your clinician
Inflammatory focus: summarise structured signals; review with your clinician
```

with empty `biomarkers_involved`. The planning paper explicitly required this surface to be removed or gated before launch. 

## Required behaviour

For the launch-core results path:

* legacy placeholder `insights[]` must not be visible to users
* placeholder insight entries must not be emitted in the public launch-core API response unless explicitly gated off from UI and marked internal
* no generic “summarise structured signals” text should appear
* if a compatibility field must remain, it should be empty or explicitly disabled for launch-core path
* do not replace it with new generic filler

## STOP conditions

STOP if:

* another active frontend surface depends on `insights[]` for real governed content
* removing/gating it would break backwards compatibility without an agreed DTO strategy
* the only available fix is to replace placeholder text with another placeholder

## Tests

Add or update tests proving:

* `insights[]` placeholder text is absent from launch-core API payload
* no frontend surface renders legacy placeholder insight text
* existing governed narrative/report fields still render

---

# Defect 2 — Suppress unsupported blood sugar narrative

## Problem

The blood sugar domain card shows:

```text
early impaired sugar and lipid handling
```

despite JSON showing:

```text
active_signal_ids: []
primary_idl_record_id: null
```

HbA1c is optimal, and glucose/insulin are missing. The audit classed this as unsupported narrative / fabricated confidence. 

## Required behaviour

If a domain has no active signals and no governed IDL record:

* do not present a pattern label implying pathology
* do not say “early impaired sugar and lipid handling”
* do not show confident contributor wording unsupported by signals
* use honest fallback language, for example:

```text
HbA1c is within range on this panel. Glucose and insulin were not included, so a fuller glycaemic read would require those markers.
```

The exact wording may differ, but it must be:

* governed/deterministic
* non-alarming
* evidence-aligned
* clear that missing glucose/insulin limits interpretation

## STOP conditions

STOP if:

* fixing this requires broad metabolic WHY expansion
* there is no clear way to distinguish “no active signals” from “low-risk but sufficiently assessed”
* the current domain card model cannot represent an honest insufficient-evidence state

## Tests

Add or update tests proving:

* metabolic/blood sugar domain with HbA1c optimal and no glucose/insulin does not show “early impaired sugar and lipid handling”
* no active signal domain does not receive a pattern contributor sentence
* missing glucose/insulin produces honest limitation wording
* band/headline polarity remains coherent

---

# Defect 3 — Correct ApoA1 directionality / framing

## Problem

ApoA1 1.73 g/L, slightly above lab max, is flagged as:

```text
signal_apoa1_cardio_risk
```

and appears as a cardiovascular risk driver. The audit states elevated ApoA1 is generally protective/reverse-cholesterol-transport related and should not be framed as a negative cardiovascular risk driver. 

## Required behaviour

ApoA1 must not be presented to users as a negative cardiovascular risk driver solely because it is above the lab upper range.

Allowed correction options:

1. Reframe elevated ApoA1 as protective/contextual rather than risk-driving.
2. Remove elevated ApoA1 from “what’s driving this” negative-risk consumer surface.
3. Rename/reclassify signal directionality if the existing signal is wrongly defined.
4. If ApoA1 contributes to a ratio such as ApoB/ApoA1, ensure the risk interpretation comes from the ratio, not elevated ApoA1 alone.

Preferred behaviour:

```text
Elevated ApoA1 should be treated as favourable/contextual unless a governed combined-risk construct says otherwise.
```

## STOP conditions

STOP if:

* ApoA1 signal logic is entangled with ApoB/ApoA1 ratio in a way that cannot be safely separated
* changing ApoA1 would alter a broad lipid scoring framework without sufficient authority
* there is no governed source supporting the new wording

## Tests

Add or update tests proving:

* elevated ApoA1 alone does not appear as a negative cardiovascular risk driver
* ApoA1 may appear as favourable/contextual where appropriate
* ApoB/ApoA1 ratio logic, if present, still behaves correctly
* lead homocysteine finding remains unchanged
* cardiovascular domain remains coherent

---

# Defect 4 — Fix low ALT liver false alarm

## Problem

ALT 7 U/L, below a reference range of 10–49 U/L, drives liver score to 5/100 and “Needs review”. The audit classed this as clinically disproportionate because low ALT is generally a weak/non-finding and should not be scored like dangerously high ALT. 

## Required behaviour

ALT below the lower reference bound must not generate an alarming liver score or “critical” severity equivalent to high ALT.

Allowed correction options:

1. Apply direction-aware scoring for ALT:

   * high ALT may be concerning
   * low ALT should be capped at low/no severity unless governed evidence says otherwise
2. Suppress low-ALT contribution to liver domain score.
3. Mark low ALT as informational/low-priority rather than critical.
4. Keep high ALT behaviour unchanged.

Preferred behaviour:

```text
Low ALT should not drive a 5/100 liver score or alarming liver “Needs review” card.
```

## STOP conditions

STOP if:

* ALT scoring is globally range-distance based with no directionality mechanism
* fixing ALT requires redesigning all enzyme scoring
* high ALT severity would be weakened unintentionally
* there is no way to isolate low-bound ALT handling safely

## Tests

Add or update tests proving:

* ALT below lower range does not drive critical/alarming liver score
* high ALT still triggers appropriate concern
* liver domain does not show 5/100 “Needs review” solely due to low ALT
* no unrelated hepatic markers regress

---

# Cross-cutting requirements

## Layer B / Layer C fidelity

For all four fixes:

* Layer C must not invent unsupported interpretation
* UI wording must be backed by JSON/Layer B truth
* no internal sprint strings should leak into consumer JSON
* no raw signal IDs should be user-facing
* report coherence must improve, not hide findings

## Existing protected behaviours must remain intact

Do not regress:

* LC-S8F Phase B unit conversion
* LC-S8G uploaded-unit display fidelity
* LC-S10B CHECK 2/4/5/6
* homocysteine lead finding
* alcohol lifestyle bridge
* statin bounded modifier
* uploaded-panel fidelity
* Sentinel no-conversion frontend guard

## Required validation commands

Run targeted tests for changed areas.

At minimum run:

```powershell
python -m pytest backend/tests/regression/test_lc_s10b_launch_core_protection.py -q
python -m pytest backend/tests/regression/test_lc_s5_proving_checks.py -q
python -m pytest backend/tests/regression/test_lc_s8f_phase_b_uk_si_true_conversions.py -q
python -m pytest backend/tests/regression/test_lc_s8g_uploaded_unit_display_fidelity.py -q
python -m pytest backend/tests/regression/test_lc_s8d_unit_governance_sentinel.py -q
```

If scoring files are changed, also run:

```powershell
python -m pytest backend/tests/unit/test_scoring_rules.py -q
```

If unit/scoring/domain aggregation code is touched, run relevant broader backend tests and record why selected.

If frontend files are changed, run:

```powershell
npm run type-check
npm run test
```

If frontend test infrastructure is unavailable or noisy, record exact output and rely on backend/API regression tests plus type-check.

## Required new or updated tests

Add regression coverage for:

1. `insights[]` placeholder not emitted/rendered on launch-core path.
2. blood sugar domain with no active signals uses honest insufficient-evidence wording.
3. elevated ApoA1 does not become a negative cardiovascular risk driver.
4. low ALT does not produce critical/alarming liver score.
5. homocysteine lead finding remains intact on AB panel.
6. no internal sprint-management strings leak into consumer JSON.
7. no raw signal IDs leak into user-facing fields.

## Sentinel / guardrail update

Add or update Sentinel coverage for these defect classes:

```text
legacy_insights_placeholder_leakage
domain_narrative_without_active_signal
apoa1_directionality_misclassification
low_alt_false_alarm
consumer_payload_internal_sprint_string_leakage
```

If a defect is better protected by deterministic regression tests than Sentinel metadata, document the reason. Prefer adding Sentinel metadata where an existing pack pattern is available.

## Human UAT replay

After implementation, replay or regenerate the AB analysis equivalent to:

```text
analysis_id=c440dfa2-12a1-4e29-95a5-ee07a2397c59
```

Check:

* no placeholder `insights[]` text visible
* blood sugar domain no longer claims impaired sugar handling without active signals
* ApoA1 is not shown as a negative risk driver
* liver domain is not alarmed by low ALT alone
* homocysteine lead finding remains coherent
* lifestyle alcohol bridge remains visible
* units/display labels remain correct

## Acceptance criteria

This sprint is complete only if:

* all four trust blockers are corrected
* no broad scope expansion occurred
* no LC-S8F/LC-S8G regression occurred
* no homocysteine lead regression occurred
* every correction is protected by a deterministic test
* Sentinel/guardrail metadata is updated or explicitly justified
* live/replayed AB output is suitable for external human testing
* implementation notes clearly map each fix to evidence and tests

## Required documentation output

Create or update:

```text
docs/audit-papers/LC-S11A_trust_blocker_correction_notes.md
```

It must include:

1. defect inventory
2. files changed
3. fix per defect
4. tests added/updated
5. Sentinel/guardrail changes
6. before/after behaviour
7. residual risks
8. UAT replay result
9. final recommendation

This document must map directly to implementation and tests. It is not a passive status artefact.

## Cursor completion requirements

When complete:

1. Run required validation commands.
2. Update the LC-S11A notes.
3. Run closure audit:

```powershell
git branch --show-current
git status --short
git log --oneline -n 8
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

Cursor may not self-certify clinical correctness, architecture correctness, external-user readiness, merge readiness, launch readiness, or final approval.

```
```
