---
work_id: DOMAIN-UX1A
branch: domain-ux/domain-ux1a-wave1-card-scaffold-contract
risk_level: STANDARD
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# DOMAIN-UX1A — Wave 1 Health Systems Card Scaffold + Contract Hardening

## Classification

This is a STANDARD-risk MIXED sprint.

Reason: this sprint surfaces existing Wave 1 Health Systems Card outputs in the main results journey and adds light DTO/contract hardening for evidence completeness and card display fields.

This sprint must not alter clinical scoring logic, signal activation, root-cause reasoning, Knowledge Bus content, IDL records, or subsystem interpretation logic.

Escalate to HIGH and STOP if implementation requires changing:

- expected marker sets
- scoring policy
- missing-marker logic
- reliability/confidence rules
- domain scoring behaviour
- signal evaluation
- root-cause/arbitration
- Knowledge Bus assets
- IDL records
- pipeline output construction beyond adding explicit DTO fields for existing domain-card evidence

## Purpose

Build the first working slice of the Health Systems Card scaffold for the three Wave 1 domains already supported by the repo:

1. Cardiovascular health
2. Blood sugar control
3. Liver health

This is not a quick hidden-card exposure sprint.

The purpose is to begin implementing the agreed Health Systems Card architecture by:

- surfacing the existing Wave 1 cards in the main results journey
- hardening the DTO contract for evidence completeness
- aligning frontend wording with the agreed card model
- ensuring frontend remains renderer-only
- preventing fake subsystem evidence or frontend-invented biological grouping

## Controlling authority

Read before doing anything:

```text
docs/planning-papers/DOMAIN_UX_health_systems_card_scaffold_sprint_plan_FINAL.md
docs/discussion documents/healthiq_health_systems_card_discussion_FINAL.md
docs/architecture/User Health to Systems Map_FINAL.md
docs/audit-papers/DOMAIN-UX1_health_systems_card_codebase_reality_audit.md
docs/audit-papers/DOMAIN-R1_launch_core_health_domain_readiness_audit.md
docs/governance/AUTOMATION_BUS_SOP_v1.3.1.md
```

If any of the first four files are missing, STOP.

## Required output documentation

Create:

```text
docs/audit-papers/DOMAIN-UX1A_wave1_health_systems_card_scaffold_notes.md
```

This document must include:

1. preflight results
2. source documents reviewed
3. exact DTO fields added or confirmed
4. exact frontend components changed
5. evidence completeness implementation
6. card placement decision
7. label/wording changes
8. prose quality gate findings
9. explicit confirmation that no subsystem labels/groupings were invented
10. tests added/updated
11. residual gaps deferred to DOMAIN-UX1B / DOMAIN-UX1C
12. recommendation for next sprint

## Mandatory preflight

Run and record:

```powershell
git branch --show-current
git status --short
git log --oneline -n 12
git stash list
```

Verify work-package token:

```powershell
Test-Path automation_bus/state/work_package_active.json
```

Read `automation_bus/state/work_package_active.json` and confirm:

* `work_id` is `DOMAIN-UX1A`
* branch is `domain-ux/domain-ux1a-wave1-card-scaffold-contract`

If token is missing or mismatched, STOP:

```text
Kernel start not executed or work package mismatch.
```

## Baseline verification

Before implementation, confirm current repo reality:

* `Wave1DomainCards.tsx` exists
* `consumer_domain_scores` exists in frontend type contract
* existing Wave 1 domains are present:

  * `wave1_cardiovascular`
  * `wave1_blood_sugar`
  * `wave1_liver`
* existing cards are currently hidden, buried, or not prominent in the main results journey
* existing backend assembler is `backend/core/analytics/domain_score_assembler.py`

If any of these assumptions are false, STOP and report.

## Implementation scope

### A. Surface Wave 1 Health Systems Cards in the main journey

Move or reposition the existing Wave 1 Health Systems Cards so they are visible in the main results journey without the user needing to open a low-priority disclosure section.

The placement should make them feel like part of the primary results experience, not a supplementary technical section.

Do not redesign the whole results page.

Do not move clinician-facing content upward.

### B. Add / confirm plain-English domain descriptor

Each Wave 1 card should have a short descriptor:

* Cardiovascular health → Heart, arteries and circulation
* Blood sugar control → Sugar and insulin balance
* Liver health → Liver strain and processing load

This may be implemented as backend DTO field or a small frontend display map if kept strictly presentational.

If implemented in frontend, it must be limited to these fixed Wave 1 domain IDs and must not become interpretation logic.

### C. Add evidence completeness fields

Add backend-emitted evidence completeness fields to the Wave 1 domain card DTO.

Required fields:

```text
evidence_completeness_numerator
evidence_completeness_denominator
```

These must be emitted by the backend.

The frontend must not calculate expected marker sets, included marker counts, or missing marker counts.

Implementation should derive these only from existing Wave 1 rail marker sets and existing missing-marker logic.

Expected principle:

```text
denominator = expected marker count for the domain rail
numerator = denominator - missing marker count
```

Only use existing governed rail/assembler state. Do not change expected marker sets.

### D. Reliability wording

Map current confidence wording into the agreed score reliability vocabulary.

Allowed examples:

```text
high → Good reliability
medium → Moderate reliability
low → Limited reliability
```

Do not change backend confidence logic.

Do not reinterpret confidence as evidence completeness.

### E. Band wording

Align consumer-facing band wording with the agreed UX language.

Target vocabulary:

```text
Strong
Stable
Watch / Worth watching
Needs attention
```

Use the existing backend band values. Do not change scoring thresholds.

### F. Prose quality gate

Because these cards will become more prominent, inspect the visible card text, especially:

* `headline_sentence`
* `contributor_sentence`
* `confidence_sentence`
* `consequence_sentence`
* `next_step_sentence`

Remove or improve obviously mechanical consumer-facing wording only if it can be done safely in the existing domain narrative assembly without changing clinical meaning.

Specifically check for repetitive or weak language such as:

```text
on this panel
main pattern to discuss first
mechanical compiler phrasing
internal/model/process language
```

If safe copy cleanup requires backend narrative file changes within the existing Wave 1 domain narrative layer, this is allowed only if tightly scoped and regression-tested.

Do not author new medical claims.

Do not expand Knowledge Bus content.

### G. Forward-compatible subsystem placeholder

If a forward-compatible subsystem field is added, it must be nullable/empty only and not rendered as a visible “coming soon” UI.

Allowed:

```text
subsystems?: null
subsystems?: []
```

Forbidden:

```text
Visible placeholder subsystem section
"More subsystem detail coming soon"
Frontend-hardcoded subsystem chips
Frontend-invented marker groupings
```

## Explicitly forbidden in this sprint

Do not implement:

* subsystem chips unless backend-governed subsystem data already exists
* per-subsystem biomarker grouping
* greyed-out biomarker cards
* domain score dial/gauge
* compact biomarker card variant
* Wave 2 domains
* frontend-invented biological groupings
* subsystem score/status
* Knowledge Bus content changes
* scoring policy changes
* IDL content changes
* root-cause/arbitration changes
* clinician report redesign

## Potentially allowed files

```text
frontend/app/(app)/results/page.tsx
frontend/app/components/results/Wave1DomainCards.tsx
frontend/app/components/results/**/*
frontend/app/types/analysis.ts
frontend/tests/**/*
backend/core/models/results.py
backend/core/analytics/domain_score_assembler.py
backend/core/analytics/domain_narrative_wave1.py
backend/tests/regression/**/*
backend/tests/unit/**/*
sentinel/packs/**/*
docs/audit-papers/DOMAIN-UX1A_wave1_health_systems_card_scaffold_notes.md
```

Only touch `domain_narrative_wave1.py` if needed for tightly scoped prose cleanup of existing Wave 1 card sentences.

## Forbidden unless GPT explicitly approves

```text
backend/ssot/**/*
backend/core/scoring/**/*
backend/core/pipeline/**/*
backend/core/units/**/*
backend/core/analytics/root_cause*
backend/core/analytics/report_compiler*
backend/core/analytics/narrative_report_compiler*
knowledge_bus/**/*
frontend clinician report components
automation_bus/state/*
backend/scripts/run_work_package.py
backend/scripts/golden_gate_local.py
backend/scripts/update_cursor_status.py
```

## Required tests

Add or update deterministic tests proving:

### Backend contract

* each Wave 1 domain emits `evidence_completeness_numerator`
* each Wave 1 domain emits `evidence_completeness_denominator`
* numerator and denominator are integers
* numerator is not greater than denominator
* missing-marker IDs remain backend-emitted
* evidence completeness is derived from existing rail/missing-marker data
* no score, threshold, marker-set or confidence rule changed

### Frontend rendering

* Wave 1 Health Systems Cards render in the main results journey
* cards are not hidden only behind a low-priority closed disclosure
* card displays consumer label
* card displays plain-English descriptor
* card displays score and band
* card displays score reliability wording
* card displays evidence completeness using backend-supplied fields
* card does not render clinical label in consumer view
* card does not render subsystem placeholder UI
* card does not invent subsystem chips or marker groupings

### Prose safety

* visible card copy does not include obvious internal/process language
* no raw signal IDs are visible
* no internal cluster names are visible
* no “Functional read —” style labels leak
* no “governed”, “compiler”, “model”, or “structured ranking” language appears in the consumer card

### Regression preservation

* FE-R1 prose safety still passes
* FE-R6A fresh UAT guard still passes
* MAP-R1A mapping guard still passes
* existing domain score assembler tests still pass, if present

## Required Sentinel obligations

Add or update active deterministic Sentinel defect classes as appropriate, for example:

```text
health_system_card_hidden_from_main_journey
health_system_card_frontend_calculates_evidence_completeness
health_system_card_clinical_label_visible
health_system_card_subsystem_placeholder_visible
health_system_card_internal_language_visible
```

Each Sentinel class must point to an active deterministic test.

No placeholder Sentinel entries.

## Required validation commands

Run:

```powershell
python -m pytest backend/tests/regression/test_fe_r1_consumer_prose_cleanup.py -q
python -m pytest backend/tests/regression/test_fe_r6a_fresh_uat_defect_cleanup.py -q
python -m pytest backend/tests/regression/test_canonical_mapping_star_suffix_failure.py -q
python -m pytest backend/tests/regression/test_lc_s16_17_19_kb_surface_payload_contract.py -q
python -m pytest backend/tests/regression/test_lc_s20_22_persisted_replay_sentinel_phase2.py -q
python -m pytest backend/tests/unit/test_scoring_rules.py -q
```

Also run any new DOMAIN-UX1A tests added by this sprint.

If frontend files changed:

```powershell
npm run type-check
```

If browser tools are available, inspect a fresh or current result page and confirm the Wave 1 cards are visible in the main journey.

Do not claim browser UAT passed unless actually inspected.

## Acceptance criteria

This sprint is complete only if:

* Wave 1 Health Systems Cards are visible in the main results journey
* backend emits evidence completeness numerator/denominator
* frontend uses backend-supplied completeness values
* frontend does not calculate governed evidence logic
* score reliability wording is aligned
* band wording is aligned
* plain-English descriptors are present
* `clinical_label` is not shown in the consumer card
* no visible subsystem placeholder UI is rendered
* no subsystem labels or biomarker groupings are invented in frontend
* newly prominent prose passes consumer-quality safety checks
* all required regression tests pass
* notes document what remains for DOMAIN-UX1B and DOMAIN-UX1C

## Closure requirements

Before finish, run:

```powershell
git branch --show-current
git status --short
git diff --name-only
git log --oneline -n 8
git stash list
```

Then run:

```powershell
python backend/scripts/run_work_package.py finish
```

After finish, follow SOP v1.3.1:

* if `automation_bus/latest_cursor_status.json` is the only dirty file and shows kernel-generated COMPLETE status for `DOMAIN-UX1A`, commit it automatically as:
  `chore(bus): DOMAIN-UX1A kernel COMPLETE status`
* if any other Automation Bus artefact is dirty, STOP and escalate

Do not merge.

Do not start DOMAIN-UX1B.

## Cursor completion statement

Cursor implements DOMAIN-UX1A only.

Cursor may not self-certify clinical correctness, merge readiness, or permission to begin DOMAIN-UX1B.
