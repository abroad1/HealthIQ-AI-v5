---
work_id: BETA-BASELINE-REGISTER-1
branch: work/BETA-BASELINE-REGISTER-1-final-strategy-and-register
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: CONTENT
---

# BETA-BASELINE-REGISTER-1 — Adopt Final Beta-Readiness Strategy Baseline and Create Build Register

## Objective

Adopt the final definitive beta-readiness strategy document as the programme baseline for the eight-block beta-readiness build, and create the lightweight build deliverable register that will track completed sprint outcomes across the programme.

This is a documentation/governance sprint only.

Do not change runtime code.
Do not change tests.
Do not change frontend behaviour.
Do not change backend behaviour.
Do not begin P1-1 domain mapping.
Do not alter medical logic, parser logic, scoring, reports, Gemini, Layer B or Layer C runtime behaviour.
Do not rewrite the final strategy document unless there is a clear typo in path/title metadata that must be corrected.

---

## Branch and state checks

Start from `main`.

```powershell
git switch main
git pull
git status --short
git switch -c work/BETA-BASELINE-REGISTER-1-final-strategy-and-register
```

Do not proceed if the working tree is dirty, except for the expected file already placed by the user if it is not yet committed.

Confirm the Automation Bus active work package/state file if required by SOP.

---

## Authoritative input

The final definitive strategy document has been saved by the user at:

```text
docs/strategy/beta_readiness/HEALTHIQ_AI_BETA_READINESS_DEFINITIVE_STRATEGY_FINAL_2026-06-20.md
```

This document is now the first authority document for the eight-block beta-readiness build strategy and future P1-1 planning.

Also read:

```text
docs/architecture/ADR-LAYER-BOUNDARY-RECONCILIATION-1.md
docs/strategy/eight_block_beta_readiness/EIGHT_BLOCK_BETA_READINESS_COMPARISON_AND_PROGRAMME_RECOMMENDATION_2026-06-18.md
docs/AUTHORITY_MAP.md
```

Purpose of reading these is only to confirm consistency and authority placement. Do not rewrite them.

---

## Required actions

### 1. Verify final strategy document exists

Confirm this file exists:

```text
docs/strategy/beta_readiness/HEALTHIQ_AI_BETA_READINESS_DEFINITIVE_STRATEGY_FINAL_2026-06-20.md
```

Verify it is the final version and is suitable to act as the programme baseline.

Do not replace it with an older draft.

### 2. Register the strategy baseline if appropriate

Inspect:

```text
docs/AUTHORITY_MAP.md
```

If this file is the repo’s standard mechanism for registering authoritative strategy documents, add a minimal entry for:

```text
docs/strategy/beta_readiness/HEALTHIQ_AI_BETA_READINESS_DEFINITIVE_STRATEGY_FINAL_2026-06-20.md
```

Classify it consistently with other authoritative strategy/planning documents.

Do not broadly rewrite `AUTHORITY_MAP.md`.

If unsure whether to update `AUTHORITY_MAP.md`, do not update it; instead record in the final report that it should be reviewed by GPT/human.

### 3. Create the lightweight build deliverable register

Create:

```text
docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md
```

If the directory does not exist, create it.

The register must be short and programme-focused. It must not duplicate audit reports or git history.

Use this opening structure:

```markdown
# HealthIQ AI — Beta Readiness Build Deliverable Register

Purpose:

To track what has been delivered against the eight-block beta-readiness build programme, what remains open, and what should happen next.

This register is a lightweight continuity log for the HealthIQ AI beta-readiness programme. It is not a substitute for formal audits, ADRs, closure papers, test evidence, or merge records.

Entries should record only:
- what was delivered / ticked off from the programme;
- carry-forwards;
- material blockers or risks;
- recommended next sprint.

Entries should not list every file touched or every non-change.
```

Then add the first entry:

```markdown
## BETA-BASELINE-REGISTER-1 — Final strategy baseline and build register

**Status:** Complete  
**Date closed:** 2026-06-20  
**Programme block(s):** Phase 0 — Governance and evidence consolidation  

### Delivered / ticked off
- Final definitive beta-readiness strategy baseline adopted as the first authority document for the eight-block build programme.
- Lightweight build deliverable register created for sprint-to-sprint continuity.
- Register path established at `docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md`.

### Carry-forwards
- P1-1 must use the final strategy baseline as its first authority document.
- Future sprint closures must append a short register entry using this format.

### Blockers / risks
- None from this baseline/register sprint, unless repository authority registration remains unresolved.

### Recommended next sprint
- P1-1 — Launch-core domain build-materials map.
```

If the sprint is not complete or a blocker is found, update the entry honestly rather than forcing “Complete”.

---

## Build programme register rule for future sprints

At closure, future beta-readiness sprints should append a short entry using this format:

```markdown
## <WORK_ID> — <Sprint title>

**Status:** Complete / Partial / Blocked  
**Date closed:** <YYYY-MM-DD>  
**Programme block(s):** <e.g. Block 1 Core systems, Block 3 Layer B prose>  

### Delivered / ticked off
- <what this sprint completed against the beta-readiness programme>
- <major decision, map, document, implementation or validation outcome>

### Carry-forwards
- <what still needs to be done later>
- <known gaps exposed by this sprint>

### Blockers / risks
- <only material blockers or risks that affect future work>

### Recommended next sprint
- <next work package recommendation>
```

Rules:

* Keep the entry short.
* Do not list every file touched.
* Do not list every file not touched.
* Do not duplicate the formal audit or closure report.
* Focus on programme continuity: what is now done, what remains, and what comes next.

---

## Expected changed files

Expected:

```text
docs/strategy/beta_readiness/HEALTHIQ_AI_BETA_READINESS_DEFINITIVE_STRATEGY_FINAL_2026-06-20.md
docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md
```

Optional:

```text
docs/AUTHORITY_MAP.md
```

Only update `docs/AUTHORITY_MAP.md` if clearly appropriate.

No code, test, frontend, backend, parser, analytics, scoring, report, Gemini or runtime files may change.

---

## Validation

Run:

```powershell
git diff --stat
git diff --name-only
git status --short
```

Confirm only expected documentation/governance files changed.

No tests are required unless repository policy requires documentation checks.

---

## Required final report

Return:

```text
- branch name
- whether final strategy document exists at the canonical path
- whether AUTHORITY_MAP was updated
- whether BUILD_DELIVERABLE_REGISTER.md was created
- exact register path
- summary of first register entry
- confirmation no code/test/frontend/backend/runtime files changed
- validation output
- git status --short
```

Do not merge until GPT architectural review and human approval.

---

## Acceptance criteria

This work is complete only if:

```text
1. The final definitive strategy document exists at:
   docs/strategy/beta_readiness/HEALTHIQ_AI_BETA_READINESS_DEFINITIVE_STRATEGY_FINAL_2026-06-20.md

2. The build deliverable register exists at:
   docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md

3. The register contains a short entry for BETA-BASELINE-REGISTER-1.

4. The register format is lightweight and does not require every file touched / not touched.

5. Future sprint register guidance is included.

6. No runtime code, test code, frontend code or backend code is changed.

7. P1-1 is identified as the recommended next sprint.
```
