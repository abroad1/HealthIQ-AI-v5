---
work_id: DOMAIN-UX1A-PATCH
branch: domain-ux/domain-ux1a-card-labels-low-evidence
risk_level: STANDARD
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# DOMAIN-UX1A-PATCH — Health Systems Card Label Hierarchy and Low-Evidence State

## Classification

This is a STANDARD-risk MIXED sprint.

Reason: this sprint corrects the consumer-facing presentation of the Wave 1 Health Systems Cards after DOMAIN-UX1A. It should update frontend display semantics and, only if required, add tightly scoped DTO/display fields to distinguish insufficient evidence from true adverse scoring.

This sprint must not alter scoring thresholds, signal activation, Knowledge Bus content, IDL records, root-cause logic, clinical interpretation logic, or subsystem grouping.

Escalate to HIGH and STOP if implementation requires changes to:

- scoring policy
- expected marker sets
- signal evaluation
- root-cause/arbitration
- Knowledge Bus assets
- IDL records
- domain confidence/reliability rules
- marker-to-subsystem grouping
- analytical pipeline behaviour

## Purpose

DOMAIN-UX1A successfully surfaced the Wave 1 Health Systems Cards, but post-merge UAT showed three presentation problems:

1. `Limited reliability` is visible, but the field label `Score reliability` is not.
2. evidence completeness is visible, but the field label `Evidence completeness` is not.
3. cards with `0 of N` expected markers currently show `0 / 100` and `Needs attention`, which looks like a poor result rather than insufficient evidence.

The purpose of this patch is to make the Health Systems Card scaffold more truthful and legible before visual polish begins.

## Controlling authority

Read before doing anything:

```text
docs/planning-papers/DOMAIN_UX_health_systems_card_scaffold_sprint_plan_FINAL.md
docs/discussion documents/healthiq_health_systems_card_discussion_FINAL.md
docs/audit-papers/DOMAIN-UX1A_wave1_health_systems_card_scaffold_notes.md
docs/audit-papers/DOMAIN-UX1_health_systems_card_codebase_reality_audit.md
docs/governance/AUTOMATION_BUS_SOP_v1.3.1.md
````

Also use the post-merge verification finding from the user:

```text
Cards are mounted and schema 1.2 is present, but UX hierarchy is incomplete.
Reliability renders value-only: “Limited reliability”.
Evidence completeness renders value-only: “Based on X of Y expected markers on your panel”.
Blood sugar and liver show 0 / 100 + Needs attention when evidence completeness is 0 of N.
```

If the DOMAIN-UX1A notes file is missing, STOP.

## Required output documentation

Create:

```text
docs/audit-papers/DOMAIN-UX1A_PATCH_card_labels_low_evidence_notes.md
```

This document must include:

1. preflight results
2. source documents reviewed
3. exact visible issue confirmed
4. label hierarchy changes made
5. low-evidence state rule implemented
6. files changed
7. tests added/updated
8. Sentinel updates
9. confirmation that scoring logic was not changed
10. residual gaps for DOMAIN-UX1B and DOMAIN-UX1C
11. browser/UAT status if performed
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

* `work_id` is `DOMAIN-UX1A-PATCH`
* branch is `domain-ux/domain-ux1a-card-labels-low-evidence`

If token is missing or mismatched, STOP:

```text
Kernel start not executed or work package mismatch.
```

## Baseline verification

Before implementation, confirm the current issue exists in code and/or test fixture:

* `Wave1DomainCards.tsx` renders reliability value without visible `Score reliability` label
* `Wave1DomainCards.tsx` renders evidence completeness without visible `Evidence completeness` label
* zero-evidence cards can render `0 / 100` and `Needs attention`
* there is no current insufficient-data display state for cards with `evidence_completeness_numerator === 0` and `evidence_completeness_denominator > 0`

If these issues are not present, STOP and report no-op risk.

## Required implementation

### A. Add visible field labels

Update the collapsed Health Systems Card so reliability and evidence completeness are clearly labelled.

Required visible wording:

```text
Score reliability: Limited reliability
Evidence completeness: 0 of 3 expected markers included
```

or equivalent wording that clearly includes both labels:

```text
Score reliability
Limited reliability

Evidence completeness
0 of 3 expected markers included
```

Do not rely on value-only lines.

### B. Correct zero-evidence state

If:

```text
evidence_completeness_numerator === 0
and evidence_completeness_denominator > 0
```

the card must not present this as a true adverse score.

Required behaviour:

* do not show `0 / 100` as the primary score
* do not show `Needs attention` as the primary band
* show a clear insufficient-evidence state, for example:

  * `Not enough data`
  * `Insufficient marker evidence`
  * `More markers needed`
* retain evidence completeness, e.g.:

  * `Evidence completeness: 0 of 3 expected markers included`
* show a short consumer-safe explanation, for example:

  * `This area needs more marker evidence before HealthIQ can score it meaningfully.`

The exact wording can be refined, but it must clearly distinguish absent evidence from a poor health-system score.

### C. Partial-evidence state

If numerator is greater than zero but reliability is limited, such as:

```text
100 / 100
Limited reliability
1 of 5 expected markers included
```

the card may still show the score, but reliability and evidence completeness must be visually clear enough to avoid overconfidence.

Do not suppress partial-evidence scores in this sprint unless a clear safety issue is found.

### D. No subsystem work

Do not add supporting-system chips, subsystem sections, or marker-to-subsystem grouping in this patch.

The current `Based mainly on...` evidence anchor may remain, but do not pretend it is a governed subsystem preview.

Subsystem work remains DOMAIN-UX1C.

### E. No scoring changes

Do not alter the backend score itself.

This sprint changes presentation semantics only.

If backend emits `score = 0` because no biomarkers contributed, frontend may render that as insufficient data. The backend score calculation must remain unchanged.

## Potentially allowed files

```text
frontend/app/components/results/Wave1DomainCards.tsx
frontend/app/lib/wave1HealthSystemCardDisplay.ts
frontend/app/types/analysis.ts
frontend/tests/components/Wave1DomainCards.test.tsx
backend/tests/regression/**/*
backend/tests/unit/**/*
sentinel/packs/escaped_defects_v1.json
docs/audit-papers/DOMAIN-UX1A_PATCH_card_labels_low_evidence_notes.md
```

Backend model/assembler files are allowed only if a tiny display-state field is strictly necessary and justified:

```text
backend/core/models/results.py
backend/core/analytics/domain_score_assembler.py
```

Prefer frontend presentation handling using existing backend-emitted `evidence_completeness_numerator` and `evidence_completeness_denominator`.

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

### Label hierarchy

* collapsed card renders `Score reliability`
* collapsed card renders reliability value
* collapsed card renders `Evidence completeness`
* collapsed card renders backend-supplied numerator/denominator
* tests verify label + value, not just value

### Zero-evidence state

Given a domain card with:

```text
evidence_completeness_numerator = 0
evidence_completeness_denominator > 0
score = 0
band_label = review
```

the rendered card must:

* show insufficient-data wording
* not show `0 / 100` as the primary score
* not show `Needs attention` as the primary band
* show evidence completeness
* show a short explanation that more marker evidence is needed

### Partial-evidence state

Given:

```text
evidence_completeness_numerator = 1
evidence_completeness_denominator = 5
score = 1.0
band_label = strong
confidence_tier = low
```

the rendered card may show `100 / 100` and `Strong`, but must also clearly show:

* `Score reliability: Limited reliability`
* `Evidence completeness: 1 of 5 expected markers included`

### Guard preservation

* `clinical_label` is not shown in consumer card
* frontend does not calculate evidence completeness from `missing_marker_ids`
* no subsystem placeholder UI appears
* no frontend-invented subsystem chips appear
* no raw signal IDs or internal process language appears

## Required Sentinel obligations

Add or update active deterministic Sentinel defect classes as appropriate:

```text
health_system_card_reliability_label_missing
health_system_card_evidence_completeness_label_missing
health_system_card_zero_evidence_shows_needs_attention
health_system_card_zero_evidence_shows_primary_zero_score
```

Each Sentinel class must point to an active deterministic test.

No placeholder Sentinel entries.

## Required validation commands

Run:

```powershell
python -m pytest backend/tests/regression/test_domain_ux1a_wave1_health_systems_card_scaffold.py -q
python -m pytest backend/tests/regression/test_fe_r1_consumer_prose_cleanup.py -q
python -m pytest backend/tests/regression/test_fe_r6a_fresh_uat_defect_cleanup.py -q
python -m pytest backend/tests/regression/test_canonical_mapping_star_suffix_failure.py -q
python -m pytest backend/tests/regression/test_lc_s16_17_19_kb_surface_payload_contract.py -q
python -m pytest backend/tests/regression/test_lc_s20_22_persisted_replay_sentinel_phase2.py -q
python -m pytest backend/tests/unit/test_scoring_rules.py -q
python -m pytest backend/tests/unit/test_domain_score_assembler_v1.py -q
```

Also run any new DOMAIN-UX1A-PATCH tests added by this sprint.

If frontend files changed:

```powershell
npm run type-check
```

If frontend component tests are available, run them.

If browser tools are available, inspect:

```text
http://localhost:3000/results?analysis_id=d7417288-7e11-48da-8716-d0f63f77c491
```

Confirm:

* `Score reliability` label is visible
* `Evidence completeness` label is visible
* Blood sugar and Liver no longer present `0 / 100 Needs attention` as if this were a true adverse score when evidence completeness is 0 of N

Do not claim browser UAT passed unless actually inspected.

## Acceptance criteria

This patch is complete only if:

* reliability label and value are both visible
* evidence completeness label and value are both visible
* zero-evidence cards render as insufficient-data / not-enough-marker-evidence state
* zero-evidence cards do not show `0 / 100` as primary score
* zero-evidence cards do not show `Needs attention` as primary band
* partial-evidence score remains allowed but reliability/completeness are clear
* frontend still does not calculate evidence completeness
* no subsystem labels or marker groupings are invented
* clinical label remains hidden in consumer view
* Sentinel guards are active
* regression tests pass

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

* if `automation_bus/latest_cursor_status.json` is the only dirty file and shows kernel-generated COMPLETE status for `DOMAIN-UX1A-PATCH`, commit it automatically as:
  `chore(bus): DOMAIN-UX1A-PATCH kernel COMPLETE status`
* if any other Automation Bus artefact is dirty, STOP and escalate

Do not merge.

Do not start DOMAIN-UX1B.

## Cursor completion statement

Cursor implements DOMAIN-UX1A-PATCH only.

Cursor may not self-certify merge readiness, clinical correctness, or permission to begin DOMAIN-UX1B.

```
```
