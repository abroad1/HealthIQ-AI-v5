---
work_id: LC-S16-17-19
branch: scaffold/lc-s16-17-19-kb-surface-payload-contract
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# LC-S16/17/19 — Knowledge Asset Frontend Surface, KB Framework and Payload Contract

## Classification

This is a HIGH-risk MIXED scaffold sprint.

Reason: this sprint may touch frontend result-surface auditing, Knowledge Bus lifecycle governance, DTO / Layer B → Layer C payload contract classification, regression tests, Sentinel packs, and documentation.

This sprint is part of the approved HealthIQ AI core scaffold completion programme.

This is not a frontend redesign sprint.  
This is not a Knowledge Bus content expansion sprint.  
This is not a root-cause / WHY registration migration sprint.  
This is not a Gemini/LLM sprint.  
This is not a launch-readiness sprint.

## Purpose

Understand exactly what governed intelligence is actually visible to the user, formalise the Knowledge Bus lifecycle needed to support future intelligence ingestion, and harden the Layer B → Layer C payload contract without breaking existing frontend consumers.

This sprint combines:

```text
LC-S16 — Knowledge Asset Frontend-Surface Audit
LC-S17 — Knowledge Bus Registration and Coverage Framework
LC-S19 — Structured Payload Contract Hardening
````

The sequence is mandatory:

```text
1. Audit what the user actually sees.
2. Classify whether each visible section is governed, DTO-backed, fallback, boilerplate, frontend-derived, or unsupported.
3. Review the audit findings.
4. Only then finalise the Knowledge Bus lifecycle and DTO contract work.
```

If the frontend-surface audit materially changes the assumed problem, implementation must STOP for GPT/human rescoping.

## Controlling authority

Read before doing anything:

```text
docs/planning-papers/HealthIQ_AI_core_scaffold_completion_definition_v1.md
docs/planning-papers/HealthIQ_AI_Core_Scaffold_Completion_Sprint_Plan_FINAL.md
docs/audit-papers/LC-S12B_core_scaffold_definition_notes.md
docs/audit-papers/LC-S13_lifestyle_coherence_narrative_notes.md
docs/audit-papers/LC-S14_direction_aware_scoring_notes.md
```

Also inspect if present:

```text
docs/audit-papers/LC-S12A_forensic_architecture_audit.md
docs/audit-papers/LC-S11_forensic_human_uat_audit.md
docs/audit-papers/LC-S11A_trust_blocker_correction_notes.md
docs/planning-papers/healthiq_launch_core_transformation_plan_FINAL.md
docs/governance/AUTOMATION_BUS_SOP_v1.3.1.md
docs/governance/KNOWLEDGE_BUS_SOP_v1.3.md
```

If the scaffold definition document is missing, STOP.

## Required output documentation

Create:

```text
docs/audit-papers/LC-S16_knowledge_asset_frontend_surface_audit.md
docs/audit-papers/LC-S17_knowledge_bus_lifecycle_framework.md
docs/audit-papers/LC-S19_payload_contract_hardening_notes.md
```

Also create one combined implementation note:

```text
docs/audit-papers/LC-S16_17_19_kb_surface_payload_contract_notes.md
```

The combined implementation note must include:

1. preflight results
2. prior scaffold guard results
3. frontend-surface audit summary
4. whether the internal STOP/rescope gate was triggered
5. Knowledge Bus lifecycle decisions
6. machine-enforced vs documentation-only controls
7. DTO field classification summary
8. frontend consumer impact assessment
9. files changed
10. tests added/updated
11. Sentinel updates
12. residual risks
13. recommendation for LC-S18

## Mandatory preflight

Run and record:

```powershell
git branch --show-current
git status --short
git log --oneline -n 8
git stash list
```

Verify work-package token:

```powershell
Test-Path automation_bus/state/work_package_active.json
```

Read `automation_bus/state/work_package_active.json` and confirm:

* `work_id` is `LC-S16-17-19`
* branch is `scaffold/lc-s16-17-19-kb-surface-payload-contract`

If token is missing or mismatched, STOP:

```text
Kernel start not executed or work package mismatch.
```

Confirm controlling docs exist:

```powershell
Test-Path docs/planning-papers/HealthIQ_AI_core_scaffold_completion_definition_v1.md
Test-Path docs/planning-papers/HealthIQ_AI_Core_Scaffold_Completion_Sprint_Plan_FINAL.md
```

If either is missing, STOP.

## Cross-sprint guard preflight

Before implementation, run prior scaffold / launch-core protections.

At minimum run the current equivalents of:

```powershell
python -m pytest backend/tests/regression/test_lc_s8f_phase_b_true_conversions.py -q
python -m pytest backend/tests/regression/test_lc_s8g_uploaded_unit_display_fidelity.py -q
python -m pytest backend/tests/regression/test_lc_s8d_unit_governance_sentinel.py -q
python -m pytest backend/tests/regression/test_lc_s10b_launch_core_protection.py -q
python -m pytest backend/tests/regression/test_lc_s11a_trust_blocker_correction.py -q
python -m pytest backend/tests/regression/test_lc_s13_lifestyle_coherence_narrative.py -q
python -m pytest backend/tests/regression/test_lc_s14_direction_aware_scoring.py -q
python -m pytest backend/tests/unit/test_scoring_rules.py -q
```

If one of these files has a different current name, find the current equivalent and record the substitution.

If a prior scaffold/launch-core guard fails, STOP unless the failure is already documented as unrelated and GPT/human authority explicitly permits continuation.

Do not proceed while prior protected behaviours are broken.

---

# Phase 1 — Authority and current-state inventory

Before making any changes, identify and record current authority paths for:

1. frontend results page entry point
2. frontend components rendering primary finding / WHY
3. frontend components rendering domain/system cards
4. frontend components rendering biomarker dials
5. frontend components rendering narrative/body overview
6. frontend components rendering uploaded-panel fidelity
7. frontend components rendering clinician/advanced sections
8. DTO builder / API payload authority
9. TypeScript analysis/result types
10. Knowledge Bus package loader
11. root-cause / WHY compiler
12. IDL/display-layer publisher
13. Sentinel packs covering launch-core output
14. tests covering frontend/result payload coherence

Known likely files to inspect:

```text
frontend/app/(app)/results/page.tsx
frontend/app/components/results/**/*
frontend/app/components/insights/**/*
frontend/app/components/biomarkers/**/*
frontend/app/lib/**/*
frontend/app/types/analysis.ts

backend/core/dto/**/*
backend/app/routes/analysis.py
backend/core/analytics/**/*
backend/core/pipeline/**/*
knowledge_bus/**/*
sentinel/packs/**/*
backend/tests/regression/**/*
frontend/tests/**/*
```

STOP if there are multiple competing DTO/result-surface authorities and the correct one cannot be established.

---

# Phase 2 — LC-S16 frontend-surface audit

## Mandatory rule

Complete this audit before implementing Knowledge Bus lifecycle or DTO contract hardening.

If the audit materially changes the problem, STOP for GPT/human rescoping.

## Audit objective

For representative outputs, map every visible frontend section to its source.

At minimum review:

* hero / primary finding
* “what’s driving this”
* body overview
* domain cards
* expanded domain details
* interpretation/pattern sections
* long-form WHY
* clinician/advanced sections
* biomarker dials
* uploaded-panel values
* next steps
* missing-data caveats
* trust/data-quality strip
* any footer/disclaimer/report-mode copy

For each visible content block, classify as one of:

```text
governed Knowledge Bus asset
governed DTO field
scoring/domain boilerplate
generic fallback
frontend-derived display text
internal/debug/governance leakage
unsupported or contradictory text
```

## Required audit output

Create:

```text
docs/audit-papers/LC-S16_knowledge_asset_frontend_surface_audit.md
```

Use this structure:

```md
# LC-S16 — Knowledge Asset Frontend-Surface Audit

## 1. Executive verdict

PASS / PASS WITH GAPS / FAIL

## 2. Sources inspected

## 3. Representative outputs reviewed

## 4. Frontend section map

| Frontend section | Visible content summary | DTO/API field | Runtime source | Classification | Evidence | Notes |
|---|---|---|---|---|---|---|

## 5. Governed asset-backed sections

## 6. DTO-backed but generic/boilerplate sections

## 7. Fallback-backed sections

## 8. Frontend-derived sections

## 9. Unsupported / contradictory / internal-leak sections

## 10. Knowledge Bus assets not surfaced despite being available

## 11. DTO fields consumed by frontend

## 12. DTO fields present but not surfaced

## 13. Implications for LC-S17

## 14. Implications for LC-S19

## 15. STOP / rescope recommendation
```

## Material mismatch STOP conditions

STOP before implementation if any of the following are true:

* a majority of visible content is generic fallback/boilerplate rather than governed assets
* frontend surfaces depend on fields not represented in the current DTO contract model
* major visible sections cannot be traced to stable DTO fields
* governed assets exist but are not reachable by the current frontend contract
* contract hardening would require breaking frontend consumers
* visible sections contain unsupported clinical claims
* visible sections expose raw internal/governance/debug strings

If STOP is triggered, Cursor may not self-rescope.

Report findings and wait for GPT/human authority.

## If no STOP is triggered

Proceed to Phase 3 and Phase 4.

---

# Phase 3 — LC-S17 Knowledge Bus registration and coverage framework

## Objective

Make future Knowledge Bus expansion systematic, repeatable and governable.

This is framework/governance work, not broad medical content authoring.

## Required lifecycle states

Define the Knowledge Bus lifecycle:

```text
draft
validated
runtime-loaded
signal-only
WHY-enabled
frontend-surfaced
Sentinel-protected
```

## Required lifecycle decisions

For each lifecycle state, define:

* entry criteria
* exit criteria
* required files
* validators/tests
* runtime effect
* documentation requirement
* Sentinel expectation
* owner/reviewer

## Required package types

Define requirements for at least:

1. signal-only package
2. WHY-enabled package
3. IDL/display-enabled package
4. lifestyle/modifier package
5. future medication-overlay package
6. combination-case package

## Required files by package type

Consider:

```text
signal_library.yaml
research_brief.yaml
root-cause hypothesis YAML
IDL/display metadata
test fixtures
validator outputs
Sentinel entries
documentation updates
```

## Machine-enforced vs documentation-only controls

For each lifecycle control, explicitly classify whether it is:

```text
machine-enforced now
documented now, machine-enforced later
advisory only
```

At minimum, these must be machine-enforced now or have a concrete validator backlog item:

* orphaned package detection
* package lifecycle state validity
* required file presence for WHY-enabled packages
* signal library schema validity
* root-cause hypothesis metadata validity
* asset coverage reporting for active signals
* frontend-surfacing status for WHY-enabled assets

Documentation-only lifecycle rules must be explicitly labelled as documentation-only and must not be described as gates.

## Required output

Create:

```text
docs/audit-papers/LC-S17_knowledge_bus_lifecycle_framework.md
```

Use this structure:

```md
# LC-S17 — Knowledge Bus Registration and Coverage Framework

## 1. Executive summary

## 2. Current runtime Knowledge Bus path

## 3. Lifecycle states

## 4. Package types

## 5. Required files by package type

## 6. Runtime loading expectations

## 7. WHY enablement expectations

## 8. Frontend surfacing expectations

## 9. Sentinel expectations

## 10. Machine-enforced controls

## 11. Documented-now / machine-enforced-later controls

## 12. Advisory-only guidance

## 13. Orphan package detection

## 14. Coverage reporting

## 15. How LC-S16 findings affected this framework

## 16. Required future validators / backlog items
```

---

# Phase 4 — LC-S19 structured payload contract hardening

## Objective

Ensure Layer B outputs structured truth in a form Layer C can reliably render without invention, contradiction or contract instability.

## Mandatory DTO constraint

Do not rename, restructure or remove DTO fields currently consumed by the frontend unless the corresponding frontend update is made and validated in this same sprint.

Field classification is governance work. It does not, by itself, require changing the serialisation shape.

Any DTO shape change must include:

* frontend consumer search
* TypeScript type update
* runtime rendering validation
* regression test
* stale-result compatibility assessment

If DTO hardening requires breaking changes, STOP for GPT/human authority.

## DTO sections to review

At minimum review:

* biomarkers
* top findings
* root cause
* consumer domain scores
* clinician report
* narrative report
* IDL bundle
* actions/interventions
* lifestyle context
* display fields
* uploaded-panel observations
* replay manifest
* meta fields

## Field classification categories

Classify fields as:

```text
analytical truth
explanatory evidence
display metadata
caveat
polishable prose
internal-only
legacy/compatibility-only
unknown / requires follow-up
```

## Required checks

For each field or field group, identify:

* producer
* consumer
* whether frontend currently renders it
* whether it is safe for consumer payload
* whether it is internal-only
* whether it is stable contract
* whether it is legacy/compatibility-only
* whether it is required for future Gemini-safe presentation
* whether stale-result compatibility is affected by changes

## Required output

Create:

```text
docs/audit-papers/LC-S19_payload_contract_hardening_notes.md
```

Use this structure:

```md
# LC-S19 — Structured Payload Contract Hardening

## 1. Executive verdict

## 2. DTO sources inspected

## 3. Frontend consumers inspected

## 4. Field classification table

| Field / section | Producer | Consumer(s) | Classification | Consumer-safe? | Stability requirement | Notes |
|---|---|---|---|---|---|---|

## 5. Analytical truth fields

## 6. Explanatory evidence fields

## 7. Display metadata fields

## 8. Caveat fields

## 9. Polishable prose fields

## 10. Internal-only fields

## 11. Legacy / compatibility-only fields

## 12. Unknown / follow-up fields

## 13. Consumer payload risks

## 14. DTO stability risks

## 15. Gemini-readiness implications

## 16. Recommended contract rules
```

## Implementation limits

This sprint may add tests, validators or documentation to harden the DTO contract.

It may make small non-breaking DTO hygiene changes only if:

* frontend consumer impact is fully traced
* TypeScript types are updated if needed
* compatibility impact is documented
* regression tests are added

Do not perform broad DTO restructuring.

---

# Potentially allowed files

Only edit what is necessary.

Potentially allowed docs:

```text
docs/audit-papers/LC-S16_knowledge_asset_frontend_surface_audit.md
docs/audit-papers/LC-S17_knowledge_bus_lifecycle_framework.md
docs/audit-papers/LC-S19_payload_contract_hardening_notes.md
docs/audit-papers/LC-S16_17_19_kb_surface_payload_contract_notes.md
```

Potentially allowed tests / validators:

```text
backend/tests/regression/**/*
backend/tests/unit/**/*
frontend/tests/**/*
sentinel/packs/**/*
sentinel/**/*
```

Potentially allowed runtime files only if a bounded non-breaking hardening change is clearly required and authorised by the internal audit gate:

```text
backend/core/dto/**/*
backend/core/analytics/**/*
backend/app/routes/analysis.py
frontend/app/types/**/*
frontend/app/lib/**/*
frontend/app/components/**/*
frontend/app/(app)/results/**/*
```

## Forbidden unless GPT explicitly approves

```text
backend/core/scoring/**/*
backend/core/units/**/*
backend/ssot/units.yaml
backend/ssot/scoring_policy.yaml
backend/ssot/biomarkers.yaml
knowledge_bus/**/*  # no new medical content in this sprint
automation_bus/state/*
automation_bus/latest_gate_evidence.json
automation_bus/latest_gate_output.txt
automation_bus/latest_cursor_status.json
backend/scripts/run_work_package.py
backend/scripts/golden_gate_local.py
backend/scripts/update_cursor_status.py
```

Do not modify scoring, unit governance, SSOT biomarker metadata, Knowledge Bus medical content, or Automation Bus scripts in this sprint.

If those appear necessary, STOP.

---

# Required tests

Add or update deterministic tests for:

## Frontend-surface / DTO source mapping

* visible key sections map to known DTO fields
* governed WHY exists where frontend claims governed explanation
* generic fallback is not used where governed asset is available
* raw signal IDs do not appear in user-facing fields
* internal governance/debug labels do not appear in user-facing fields

## Knowledge Bus lifecycle

* orphaned package detection or documented validator backlog exists
* WHY-enabled package requirements are represented
* signal-only vs WHY-enabled status can be distinguished
* lifecycle state values are valid if machine-enforced now

## Payload contract

* frontend-consumed DTO fields are classified
* no consumed DTO field is renamed/removed without test coverage
* internal-only fields are identified
* legacy/compatibility fields are identified
* payload shape remains compatible unless explicitly changed and tested

## Regression preservation

* LC-S8F/G unit and display fidelity still passes
* LC-S11A trust blockers remain fixed
* LC-S13 lifestyle/coherence/narrative protections still pass
* LC-S14 direction-aware scoring protections still pass
* homocysteine lead finding remains intact

---

# Required Sentinel / test harness obligations

Sentinel update is required.

At minimum add/update defect classes:

```text
frontend_section_not_backed_by_governed_source
knowledge_asset_not_surfaced_when_available
generic_fallback_used_when_governed_asset_exists
consumer_payload_internal_field_leakage
dto_frontend_contract_breakage
raw_signal_or_internal_id_visible
kb_lifecycle_required_file_missing
kb_orphan_package_unreported
```

Each must point to an active deterministic regression test, or the strongest available deterministic guard with documented limitation.

Do not add placeholder Sentinel entries unless clearly marked as not satisfying completion criteria.

---

# Required validation commands

Run prior scaffold guards and new tests.

At minimum:

```powershell
python -m pytest backend/tests/regression/test_lc_s8f_phase_b_true_conversions.py -q
python -m pytest backend/tests/regression/test_lc_s8g_uploaded_unit_display_fidelity.py -q
python -m pytest backend/tests/regression/test_lc_s8d_unit_governance_sentinel.py -q
python -m pytest backend/tests/regression/test_lc_s10b_launch_core_protection.py -q
python -m pytest backend/tests/regression/test_lc_s11a_trust_blocker_correction.py -q
python -m pytest backend/tests/regression/test_lc_s13_lifestyle_coherence_narrative.py -q
python -m pytest backend/tests/regression/test_lc_s14_direction_aware_scoring.py -q
python -m pytest backend/tests/unit/test_scoring_rules.py -q
```

Run the new LC-S16/17/19 tests explicitly, for example:

```powershell
python -m pytest backend/tests/regression/test_lc_s16_17_19_kb_surface_payload_contract.py -q
```

If frontend files changed:

```powershell
npm run type-check
npm run test
```

If Playwright/e2e files are added or changed, run the relevant Playwright command and record exact output.

If any required existing test file name differs, find and run the current equivalent, then record the substitution.

---

# Optional browser/API review

If feasible, inspect a rendered result page or API payload for a representative analysis.

Recommended check:

* use an existing post-LC-S13/LC-S14 analysis fixture or generate a fresh one
* inspect the DTO/API payload
* inspect the frontend rendering if browser tools are available
* confirm mapped sections in LC-S16 audit match what a user would actually see

Do not claim browser UAT passed unless browser rendering was actually inspected.

---

# Acceptance criteria

This sprint is complete only if:

* LC-S16 frontend-surface audit is completed first
* STOP/rescope gate is correctly handled
* visible frontend sections are mapped to DTO/runtime/governed/fallback sources
* Knowledge Bus lifecycle states are defined
* package types and required files are defined
* machine-enforced vs documentation-only lifecycle controls are distinguished
* DTO fields are classified without unsafe restructuring
* frontend-consumed fields are protected from accidental rename/removal
* Sentinel defect classes are active or limitations documented
* prior scaffold/launch-core guards still pass
* no scoring/unit/Knowledge Bus content expansion is smuggled into this sprint
* documentation clearly records residual risks and follow-up work

---

# Closure requirements

When complete:

1. Run:

```powershell
git branch --show-current
git status --short
git diff --name-only
git log --oneline -n 8
git stash list
```

2. Classify:

   * tracked modified files
   * staged files
   * untracked files
   * tooling files
   * out-of-scope files
   * stash entries

3. STOP if unrelated files, tooling leakage, dirty branch ambiguity, or stash ambiguity exists.

4. Run finish:

```powershell
python backend/scripts/run_work_package.py finish
```

5. Report whether finish completed or failed.

6. Do not merge.

7. Do not create `automation_bus/latest_audit_summary.md`.

8. Do not claim final approval.

## Cursor completion statement

Cursor implements and reports only.

Cursor may not self-certify clinical correctness, architecture correctness, scaffold completion, merge readiness, launch readiness, or permission to begin the next sprint.

```
```
