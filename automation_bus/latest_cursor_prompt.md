---
work_id: P1-6R
branch: work/P1-6R-thyroid-scoring-architecture-recovery
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: CONTENT
---

# P1-6R — Thyroid Scoring Architecture Recovery and Lab-Range Rail Decision

## Objective

Recover from the failed P1-6 attempt and establish the correct architecture decision for thyroid / hormonal scoring.

The failed P1-6 branch must not be reused, merged, cherry-picked, or salvaged.

This sprint starts clean from `main`.

The purpose is to answer one architecture-critical question:

```text
Can the current scoring architecture support thyroid / hormonal scoring using lab-provided reference ranges without hardcoded biomarker bands?
```

If the answer is yes, this sprint must define the exact safe scoring-policy pattern that a future implementation sprint may use.

If the answer is no, this sprint must define the exact scoring architecture change required before thyroid scoring or thyroid domain implementation can proceed.

This is a recovery and architecture-decision sprint, not a runtime implementation sprint.

---

## Strategic framing

This sprint exists because the previous P1-6 attempt violated the STOP gate by:

```text
- adding hardcoded TSH / FT3 / FT4 scoring bands;
- modifying prohibited Intelligence Core files;
- creating a thyroid domain card;
- creating compiled thyroid card artefacts;
- extending DTO/domain pipeline output;
- producing deliverables at the wrong paths.
```

Do not repeat that failure.

The correct response is not to abandon outcome-based delivery. The correct response is to establish the scoring architecture truth before any further thyroid runtime work.

---

## Critical scope rule

This sprint must not implement thyroid runtime behaviour.

Do not modify:

```text
backend/ssot/scoring_policy.yaml
backend/core/analytics/domain_score_assembler.py
backend/core/analytics/domain_narrative_wave1.py
backend/core/analytics/wave1_subsystem_evidence.py
backend/core/dto/persisted_replay_contract_v1.py
backend/core/knowledge/health_system_card_evidence.py
knowledge_bus/compiled/
frontend/
Gemini paths
fallback parser paths
Knowledge Bus source packages
Pass 3 source material
```

Do not create:

```text
- thyroid domain row
- thyroid compiled card
- thyroid narrative helpers
- thyroid subsystem evidence wiring
- thyroid DTO/replay contract entry
- thyroid frontend rendering
- thyroid Gemini prompt
- thyroid scoring-policy bands
```

Do not activate:

```text
- FT3 low
- FT3 high
- FT4 high
- FT4 low
- TSH high
- TSH low
- thyroid antibodies
```

This sprint is CONTENT only.

If Cursor believes a code change is required to answer the question, stop and report why. Do not make the code change.

---

## Branch and state checks

Start from `main`.

```powershell
git switch main
git pull origin main
git status --short
git rev-parse main
git rev-parse origin/main
```

Confirm:

```text
- current branch is main;
- local main == origin/main;
- working tree is clean;
- failed branch work/P1-6-thyroid-launch-core-unlock-and-domain-card is not merged.
```

Then create:

```powershell
git switch -c work/P1-6R-thyroid-scoring-architecture-recovery
```

Do not proceed if the working tree is dirty.

Do not cherry-pick or copy any file from:

```text
work/P1-6-thyroid-launch-core-unlock-and-domain-card
```

---

## Required prerequisites on main

These files must exist on `main`:

```text
docs/sprints/beta_readiness/P1-1_launch_core_domain_build_materials_map.md
docs/sprints/beta_readiness/P1-4_thyroid_energy_regulation_domain_card.md
docs/sprints/beta_readiness/P1-5_ft3_thyroid_authority_reconciliation.md
docs/architecture/ADR-THYROID-FT3-AUTHORITY-RECONCILIATION-1.md
docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md
```

If any are missing, stop and report:

```text
P1-6R prerequisite governance evidence is not present on main. P1-6R must not proceed.
```

---

## First authority documents

Read these first, in this order:

```text
docs/strategy/beta_readiness/HEALTHIQ_AI_BETA_READINESS_DEFINITIVE_STRATEGY_FINAL_2026-06-20.md
docs/sprints/beta_readiness/P1-1_launch_core_domain_build_materials_map.md
docs/sprints/beta_readiness/P1-4_thyroid_energy_regulation_domain_card.md
docs/sprints/beta_readiness/P1-5_ft3_thyroid_authority_reconciliation.md
docs/architecture/ADR-THYROID-FT3-AUTHORITY-RECONCILIATION-1.md
docs/architecture/ADR-LAYER-BOUNDARY-RECONCILIATION-1.md
docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md
```

P1-5 and its ADR are authoritative for FT3 low.

Do not contradict them.

FT3 low remains deferred/inactive.

---

## Files to inspect for scoring architecture truth

Inspect actual implementation files, but do not modify them:

```text
backend/ssot/scoring_policy.yaml
backend/core/scoring/
backend/core/analytics/
backend/tests/unit/test_scoring_rules.py
backend/tests/
docs/architecture/
docs/intelligence/
docs/testing/
```

If scoring code is elsewhere, locate it using repository search.

Search terms:

```text
scoring_policy
BiomarkerRule
calculate_biomarker_score
reference_range
range_low
range_high
lab_range
bands
direction_class
system_weight
min_biomarkers_required
biomarkers
unit
hormonal
thyroid
TSH
free_t4
free_t3
FT4
FT3
```

The report must cite source paths for every architectural claim.

---

## Phase 1 — Recovery verification

Confirm and document:

```text
1. Failed P1-6 branch is not merged to main.
2. No failed P1-6 thyroid files exist on main.
3. Main is clean before this sprint begins.
4. No failed P1-6 files are copied or reused.
```

Specifically verify absence on main of:

```text
docs/sprints/beta_readiness/P1-6_thyroid_launch_core_unlock_and_domain_card.md
docs/architecture/ADR-THYROID-LAUNCH-CORE-UNLOCK-1.md
knowledge_bus/compiled/health_system_cards/wave1_thy_thyroid_axis.yaml
knowledge_bus/compiled/manifests/p1_6_thyroid_energy_axis_card_evidence.yaml
```

If any are present on main, stop and report contamination.

---

## Phase 2 — Scoring architecture audit

Determine how the current scoring engine works.

The report must answer:

```text
1. Does scoring_policy.yaml require biomarker bands for every scored biomarker?
2. Are bands used only as fallback, or are they required to construct scoring rules?
3. Does the scoring engine already support lab-range-only scoring without bands?
4. Does the scoring engine already support directionality-only scoring without bands?
5. Can a biomarker be listed under a system without a biomarker-specific bands block?
6. What happens if a biomarker is present in the panel with lab-provided range but absent from scoring_policy.yaml biomarkers?
7. What happens if a biomarker is present in scoring_policy.yaml with directionality but no bands?
8. What tests currently prove this behaviour?
9. What would happen if TSH / FT4 / FT3 were added to the hormonal rail without hardcoded bands?
10. Is there any safe existing policy pattern that allows thyroid scoring now?
```

Do not infer. Inspect code and tests.

If behaviour is ambiguous, say so.

---

## Phase 3 — Thyroid scoring feasibility decision

Based on Phase 2, decide one of the following:

```text
A. Existing architecture already supports safe lab-range-only thyroid scoring without hardcoded bands.
B. Existing architecture does not support safe lab-range-only thyroid scoring because bands are required to construct scoring rules.
C. Existing architecture is ambiguous and requires a dedicated scoring-engine architecture change before thyroid scoring can proceed.
```

Expected safe default:

```text
If biomarker bands are required anywhere in the scoring-policy construction path, do not author thyroid scoring policy yet.
```

Do not choose the permissive interpretation unless the implementation clearly supports it.

---

## Phase 4 — Future implementation decision

Define the next safe implementation path.

If Phase 3 outcome is A, recommend a future bounded scoring-policy sprint that may enable the hormonal rail without hardcoded bands.

If Phase 3 outcome is B or C, recommend a future scoring-engine architecture sprint to add a governed lab-range-only biomarker scoring rule pattern before any thyroid scoring rail or thyroid domain card is attempted.

The future implementation decision must state:

```text
- whether scoring_policy.yaml can be changed safely in the next sprint;
- whether scoring-engine code must change first;
- whether thyroid domain card implementation remains blocked;
- whether TSH package authority remains a separate blocker;
- whether P1-4 retry remains blocked.
```

---

## Required deliverable 1 — Recovery and architecture report

Create:

```text
docs/sprints/beta_readiness/P1-6R_thyroid_scoring_architecture_recovery.md
```

Use this structure exactly:

```markdown
# P1-6R — Thyroid Scoring Architecture Recovery and Lab-Range Rail Decision

## 1. Summary
- why this recovery sprint was required
- whether main was confirmed clean
- whether current scoring architecture supports lab-range-only thyroid scoring
- whether thyroid scoring/domain implementation remains blocked
- recommended next sprint

## 2. Recovery verification
- starting branch / main SHA
- confirmation failed P1-6 branch not merged
- confirmation failed P1-6 files absent from main
- confirmation no failed branch files were reused

## 3. Authority baseline
- final beta-readiness strategy baseline
- P1-1 map
- P1-4 blocker report
- P1-5 reconciliation report
- ADR-THYROID-FT3-AUTHORITY-RECONCILIATION-1
- Layer boundary ADR

## 4. Scoring architecture audit
- scoring files inspected
- how scoring_policy.yaml is loaded
- how BiomarkerRule objects are constructed
- whether bands are schema/constructor-required
- whether lab-provided ranges are used during scoring
- whether a lab-range-only path exists at system-orchestration level
- whether directionality-only scoring exists
- source paths for each claim

## 5. Thyroid marker scoring feasibility table
| Marker | Authority position | Signal status | Can be scored now without hardcoded bands? | Reason | Remaining blocker |
|---|---|---|---|---|---|

Must include:
- TSH
- FT4 / free_t4
- FT3 / free_t3
- thyroid antibodies

## 6. Architectural decision
State one:
- Existing architecture supports safe lab-range-only thyroid scoring.
- Existing architecture does not support safe lab-range-only thyroid scoring yet.
- Existing architecture is ambiguous and requires further scoring-engine work.

Explain why.

## 7. P1-4 / thyroid domain-card status
State:
- whether P1-4 retry is permitted
- whether thyroid domain card remains blocked
- whether TSH authority remains a blocker
- whether hormonal scoring rail remains a blocker

## 8. Future implementation recommendation
Define the next sprint:
- title
- risk level
- change type
- what it may change
- what it must not change
- STOP gates

## 9. Safety and architecture boundaries
Confirm:
- no runtime code changed
- no scoring_policy.yaml changed
- no thyroid compiled card created
- no thyroid domain row created
- no DTO/replay contract changed
- no frontend/Gemini/fallback parser introduced
- no Knowledge Bus source packages changed
- no Pass 3 material changed

## 10. Validation
- commands run
- results
- git diff/stat/status

## 11. Recommended next sprint
State the recommended next sprint and rationale.
```

---

## Required deliverable 2 — ADR

Create:

```text
docs/architecture/ADR-THYROID-SCORING-LAB-RANGE-ARCHITECTURE-1.md
```

Use this structure exactly:

```markdown
# ADR-THYROID-SCORING-LAB-RANGE-ARCHITECTURE-1

## Status
Accepted / Blocked

## Context
Explain:
- P1-4 stopped on thyroid authority;
- P1-5 reconciled FT3 low conservatively;
- failed P1-6 introduced prohibited hardcoded bands and was abandoned;
- P1-6R determines the correct scoring architecture path.

## Decision
State whether current scoring architecture can support thyroid scoring without hardcoded bands.

## Non-negotiable constraints
- lab-provided reference ranges remain authoritative
- no global/default thyroid ranges
- no placeholder bands in clinical units
- no diagnostic thyroid thresholds
- no FT3 low activation
- no thyroid signal activation from scoring
- no Layer C/Gemini/frontend reasoning
- no fallback parser

## Consequences
State:
- whether thyroid scoring remains blocked
- whether hormonal scoring rail may be enabled later
- whether scoring-engine architecture must change first
- whether P1-4 retry remains blocked

## Files reviewed
List files inspected.

## Files changed
List files changed.
```

Use `Status: Accepted` if the architecture decision is clear, even if the decision is that thyroid scoring remains blocked.

Use `Status: Blocked` only if the scoring architecture cannot be understood from the repository.

---

## Required deliverable 3 — Build deliverable register update

At closure, update:

```text
docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md
```

Append a short entry:

```markdown
## P1-6R — Thyroid scoring architecture recovery

**Status:** Complete / Partial / Blocked  
**Date closed:** <YYYY-MM-DD>  
**Programme block(s):** Block 1 Core health systems model; Block 3 Layer B intelligence/prose substrate; Block 6 Medical safety, research provenance and governance  

### Delivered / ticked off
- <what this sprint completed against the beta-readiness programme>
- <major architecture decision or blocker outcome>

### Carry-forwards
- <what still needs to be done later>
- <known gaps exposed by this sprint>

### Blockers / risks
- <only material blockers or risks that affect future work>

### Recommended next sprint
- <next work package recommendation>
```

Keep the entry short.

Do not list every file touched.

Do not duplicate the full report.

---

## Expected changed files

Only these product documentation files are expected:

```text
docs/sprints/beta_readiness/P1-6R_thyroid_scoring_architecture_recovery.md
docs/architecture/ADR-THYROID-SCORING-LAB-RANGE-ARCHITECTURE-1.md
docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md
```

Bus files may change as part of SOP lifecycle.

No code files should change.

No YAML governance/register files should change.

No `scoring_policy.yaml` change is allowed.

---

## Validation

Run:

```powershell
git diff --stat
git diff --name-only
git status --short
```

No runtime tests are required because this is CONTENT-only.

If any code, scoring, runtime, frontend, Gemini, compiled Knowledge Bus, source package, or Pass 3 file is changed, stop and report failure.

---

## Required final report

Return:

```text
- branch name
- main SHA used as baseline
- whether failed P1-6 branch was confirmed unmerged
- whether failed P1-6 files are absent from main
- scoring architecture decision
- whether current architecture supports thyroid scoring without hardcoded bands
- FT3 low final position
- TSH scoring position
- FT4 scoring position
- FT3 scoring position
- thyroid antibody scoring position
- whether P1-4 retry is permitted or still blocked
- recommended next sprint
- files changed
- confirmation no runtime/code/scoring/frontend/Gemini/fallback/compiled KB files changed
- git diff --stat
- git diff --name-only
- git status --short
```

Do not merge until Claude audit, GPT architectural review and human approval.

---

## Acceptance criteria

This sprint is complete only if:

```text
1. Recovery report exists at:
   docs/sprints/beta_readiness/P1-6R_thyroid_scoring_architecture_recovery.md

2. ADR exists at:
   docs/architecture/ADR-THYROID-SCORING-LAB-RANGE-ARCHITECTURE-1.md

3. Failed P1-6 branch is confirmed not merged.

4. Failed P1-6 thyroid artefacts are confirmed absent from main.

5. Current scoring architecture is assessed from actual code/tests, not inferred.

6. Report explicitly states whether thyroid scoring can proceed without hardcoded bands.

7. Report covers TSH, FT4, FT3 and thyroid antibodies.

8. FT3 low remains deferred/inactive.

9. No hardcoded global/default thyroid reference ranges are introduced.

10. No placeholder thyroid bands are introduced.

11. No thyroid signal is activated.

12. No scoring_policy.yaml change is made.

13. No runtime/domain/DTO/compiled card/frontend/Gemini/fallback parser files are changed.

14. Build deliverable register is updated with a short P1-6R entry.

15. Final report states whether P1-4 retry remains blocked and recommends the next sprint.

16. Final report includes validation output and clean git status.
```
