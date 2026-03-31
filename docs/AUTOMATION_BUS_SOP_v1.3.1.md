# AUTOMATION BUS SOP v1.3.1
## Intelligence Governance Edition

**Status:** LOCKED
**Authority:** Control-Plane + Intelligence Governance
**Supersedes:** v1.3

---

# 1. Purpose

The Automation Bus defines the deterministic control-plane governing all work packages in HealthIQ AI.

Version 1.3.1 extends the system beyond execution control into full intelligence governance. It ensures that all analytical logic, behavioural outputs, and reasoning pathways remain:

- Deterministic
- Auditable
- Reproducible
- Architecturally controlled

This SOP enforces:

- Sequenced execution of work packages
- Immutable evidence capture
- Strict state-machine discipline
- Branch isolation
- Deterministic regression gating
- Intelligence-layer integrity
- Prevention of behavioural drift
- Elimination of no-op or redundant sprints

This system is designed to support future regulatory alignment and clinical-grade software assurance.

The integrity of this system directly determines the clinical defensibility of every report delivered to users and their clinicians.

---

# 2. Role Separation (B.1 Model)

| Agent | Authority | Cannot Do |
|--------|-----------|-----------|
| GPT | Architecture design and intelligence governance | Cannot modify repository |
| Claude | Prompt hardening and audit validation | Cannot merge or implement code |
| Cursor | Code implementation only | Cannot self-certify correctness |
| Kernel | State enforcement and execution gating | Cannot modify evidence |
| Gate | Deterministic verification | Cannot override results |
| Human | Final merge authority | Cannot bypass system safeguards |

No single agent is permitted to complete the full lifecycle independently.

---

# 3. Intelligence Core Definition

## 3.1 Definition

The Intelligence Core includes any component that directly influences analytical reasoning or output generation, including:

- Root cause compilers
- Signal evaluators
- Analytical pipeline logic
- InsightGraph construction
- Output assembly mechanisms
- Ranking, filtering, and prioritisation logic
- Governed-content loaders that affect emitted reasoning

## 3.2 Rule

Any work package that interacts with the Intelligence Core is classified as HIGH risk by default, regardless of file path.

---

# 4. Behavioural Risk Classification

## 4.1 Mandatory Change Type Declaration

Every work package must declare a change type in its front matter:

```yaml
change_type: CONTENT | BEHAVIOUR | MIXED
````

## 4.2 Definitions

### CONTENT

* SSOT updates
* YAML modifications
* Knowledge expansion
* Non-executable data changes
* Documentation-only changes that do not alter emitted reasoning

### BEHAVIOUR

* Compiler logic
* Evaluator logic
* Pipeline behaviour
* Output generation logic
* Ranking or ordering mechanisms
* Any code that changes analytical output construction, filtering, or emission

### MIXED

* Any work involving both content and behavioural elements
* Any work that adds governed content assets consumed by Intelligence Core components
* Any work where emitted reasoning changes because new assets are loaded by compilers, evaluators, or output assemblers

MIXED is always governed using BEHAVIOUR controls.

## 4.3 Behaviour Rule

Any change that alters how outputs are constructed, ranked, filtered, or emitted must be treated as HIGH risk.

---

# 5. Automation Artifacts

The Automation Bus operates through the following required artifacts:

* `automation_bus/latest_cursor_prompt.md` — active work package definition
* `automation_bus/latest_prompt_hardening.json` — hardened prompt metadata
* `automation_bus/latest_cursor_status.json` — kernel-owned lifecycle state
* `automation_bus/latest_gate_evidence.json` — gate evidence
* `automation_bus/latest_gate_output.txt` — gate output log
* `automation_bus/latest_audit_summary.md` — Claude audit summary
* `automation_bus/state/work_package_active.json` — active execution authority token

All artifacts must remain consistent and aligned at all times.

Artifacts are runtime state and are gitignored unless explicitly versioned.

---


# 6. Post-Implementation Closure Protocol

This stage is mandatory for every governed work package after implementation is complete and before `run_work_package.py finish` is executed.

Its purpose is to prevent:
- accidental inclusion of out-of-scope files
- hidden dirty working trees
- stray tooling files entering governed sprint branches
- ambiguous stash state
- branch confusion during closure
- false claims of merge readiness

## 6.1 Ownership

Cursor owns post-implementation repo hygiene and closure preparation.

The user must not perform routine manual Git housekeeping during normal sprint closure unless:
- recovery is required
- Cursor is blocked by tooling failure
- explicit architectural review instructs otherwise

Cursor may not treat its own summary as proof.
Repo state must be demonstrated through command output.

## 6.2 Mandatory Closure Audit

Before `python backend/scripts/run_work_package.py finish`, Cursor must run and report:

```powershell
git branch --show-current
git status --short
git log --oneline -n 5
git diff --name-only
git diff --cached --name-only
git stash list
```

If relevant to closure readiness, Cursor must also report:
- untracked files
- ignored files that may affect repo hygiene
- HEAD vs `main` diff summary

## 6.3 Required Classification

Cursor must explicitly classify:

- tracked modified files
- staged files
- untracked files
- tooling files
- out-of-scope files
- stash entries potentially related to the active sprint

Tooling files include at minimum:
- `.codex/`
- `.vscode/`
- `AGENTS.md`
- local helper/config files not explicitly in sprint scope

## 6.4 Tooling File Isolation Rule

Tooling files must not ride along inside a governed sprint branch unless the sprint explicitly covers tooling or control-plane/tooling changes.

If tooling files are present in a non-tooling sprint, Cursor must STOP and report the issue as a closure blocker.

Tooling changes must be isolated into:
- a dedicated tooling branch
- or a dedicated tooling sprint

## 6.5 Stash Rule

Stash is emergency-only during sprint closure.

Cursor must not use stash during normal closure unless it first states:

- exactly why stash is required
- exactly which files will enter the stash
- whether untracked files are involved
- whether ignored files are involved
- the exact recovery command needed to restore the stash contents

If ignored files are involved, Cursor must explicitly state that standard stash behaviour does not include ignored files unless handled with the correct mode.

No stash creation, pop, apply, or drop is permitted without explicit user approval once closure has entered stash-remediation territory.

## 6.6 Finish Readiness Gate

Cursor must not run:

```powershell
python backend/scripts/run_work_package.py finish
```

until it has explicitly confirmed all of the following:

- current branch matches the sprint branch
- working tree is clean
- no unrelated tracked modifications remain
- no stray untracked files remain that matter to closure
- no tooling files are leaking into sprint scope
- no ambiguous or forgotten stash exists for the sprint
- latest commit contains only in-scope work

If any condition fails, Cursor must STOP and produce a remediation plan.

## 6.7 Closure vs Merge Authority

Finish readiness is not merge authority.

After finish succeeds, Cursor may report merge readiness, but must not merge unless the human explicitly authorises it.

Human remains the final merge authority.

## 6.8 Post-Finish Confirmation

After successful finish, Cursor must re-run and report:

```powershell
git branch --show-current
git status --short
git log --oneline -n 5
git stash list
```

Cursor must explicitly state:

- whether the branch is closure-clean
- whether any stash entries remain from the sprint
- whether any tooling or out-of-scope files remain
- whether the repo is ready for merge review

## 6.9 Local Merge Execution Rule

If the human explicitly authorises local merge, Cursor may execute the local merge workflow.

Before merge, Cursor must confirm:
- finish has succeeded
- branch is clean
- no unresolved stash ambiguity remains
- no tooling-file leakage remains

After merge, Cursor must report:
- final `main` HEAD SHA
- whether the sprint branch still exists locally
- whether the sprint branch still exists remotely, if relevant
- whether any stash entries remain from the sprint
- whether the working tree is clean on `main`

## 6.10 Forbidden Closure Behaviour

The following are prohibited:

- claiming repo cleanliness without command evidence
- using stash as routine closure convenience
- mixing tooling files into governed sprint branches
- running finish against a dirty or ambiguous repo state
- merging without explicit human approval
- asking the user to perform routine manual Git housekeeping unless recovery is unavoidable


# 7. Work Package Lifecycle

## Stage 0 — Branch Alignment

* A dedicated branch must exist for the work package
* The current branch must match the declared `branch` in front matter
* No work may proceed without correct branch alignment

This prevents cross-branch contamination before any implementation begins.

---

## Stage 1 — Authoring (GPT)

GPT writes:

`automation_bus/latest_cursor_prompt.md`

### Required Front Matter

```yaml
---
work_id:
branch:
risk_level:
execution_model:
change_type:
---
```

All fields are mandatory. Missing or incorrect fields invalidate the prompt.

### Allowed Values

* `risk_level`: LOW | STANDARD | HIGH
* `execution_model`: SINGLE_PHASE | TWO_PHASE_START_FINISH
* `change_type`: CONTENT | BEHAVIOUR | MIXED

---

## Stage 1A — Authority Preflight

Before writing `latest_cursor_prompt.md`, GPT must verify:

1. The authoritative SSOT file path from the current branch
2. The runtime loader that consumes that authoritative file
3. That no parallel or duplicate authority source exists for the same domain
4. That the proposed changes will not create a second authoritative source
5. That tests and runtime loaders reference the same authority file

If any ambiguity exists regarding authoritative file location or loader wiring, the prompt must explicitly resolve it before proposing changes.

Failure to perform this check risks schema forks and silent authority drift.

This verification is architectural and mandatory. It is not delegated to the kernel or gate.

---

## Stage 1B — Reality Check

Before writing a prompt, GPT must explicitly determine:

> Does the current baseline still exhibit the problem this sprint is intended to solve?

If the answer is NO:

* The sprint must be cancelled, skipped, or re-scoped
* A prompt must not be written

No-op or redundant remediation sprints are prohibited unless explicitly re-authorised.

---

## Stage 1C — Intelligence Preflight

For BEHAVIOUR or MIXED work, GPT must identify:

* All affected Intelligence Core components
* The behavioural surface area impacted
* Expected output changes
* The canonical regression targets required
* The compiler, evaluator, loader, and consumer paths relevant to the change

---

## Stage 1D — Prompt Integrity Checklist

Before writing the prompt, GPT must verify:

* The first non-empty line is exactly `---`
* The front matter closes with exactly `---`
* All required fields are present
* `change_type` is declared
* Risk classification is correct
* Branch name is valid
* STOP conditions reflect real sprint scope
* Authority file path and loader path are explicitly verified
* The canonical test module path is known before prompt finalisation

Failure in any item invalidates the prompt.

---

## Stage 2 — Hardening (Claude)

Claude must:

* Validate prompt structure
* Ensure compliance with this SOP
* Tighten STOP conditions
* Confirm alignment with architectural intent
* Ensure PowerShell compatibility
* Confirm `execution_model` correctness

Claude writes:

`automation_bus/latest_prompt_hardening.json`

Schema:

```json
{
  "bus_version": "1.3.1",
  "work_id": "...",
  "status": "HARDENED",
  "changes": [],
  "hardened_utc": "...",
  "hardened_by": "claude-code"
}
```

Execution is blocked unless `status == HARDENED`.

### Standard Hardening Invocation

Every hardening request must use this exact phrase:

> **harden work_id: [ID] — verify source content and produce evidence checklist**

The phrase `verify source content and produce evidence checklist` is mandatory. It is not optional flavour — it is the trigger for Stage 2C compliance. If Claude receives a hardening request without this phrase, Claude must append it before proceeding and note it was missing.

---

## Stage 2A — Authority Verification During Hardening

Claude must verify during hardening:

* Authoritative file paths declared in Stage 1A **exist in the repository** — confirmed by reading the file, not by inference
* No duplicate authority sources are detectable within the prompt scope
* The prompt’s stated authority assumptions match the actual repo state

**File existence is not sufficient. Claude must read the content of every source file the sprint will operate on.**

For ingestion sprints, Claude must read:
1. The actual source batch or spec file — extracting representative entries
2. The schema contract file — identifying every accepted field type and comparator
3. The runtime evaluator — confirming it handles every field type present in the source

Every field type in the source must be cross-referenced against both the schema and the runtime. Schema and runtime can diverge. Both must be checked independently.

If any field in the source cannot be cleanly mapped to a current schema field and a current runtime handler without introducing an assumption, Claude must set `status: BLOCKED` and report the exact mismatch.

**Claiming prior task results without an artifact is prohibited.** If a preflight or compatibility check is referenced as "already confirmed," Claude must verify whether that task produced a written artifact. If no artifact exists, Claude must independently re-verify the specific claims by reading the source files. Claude must state explicitly in the hardening JSON whether findings are artifact-backed or independently re-verified.

This is a repo-reality check, distinct from GPT’s Stage 1A architectural check.

---

## Stage 2B — Behavioural Hardening

For BEHAVIOUR or MIXED work, Claude must ensure:

* Behavioural scope is explicitly defined
* Regression targets are included
* No hidden scope creep exists
* STOP conditions protect behavioural correctness
* Determinism risks are explicitly surfaced

---

## Stage 2C — Mandatory Hardening Evidence Table

**This stage is mandatory for every sprint. It is not optional and cannot be skipped.**

Claude must produce a hardening evidence checklist as part of every hardening output. This checklist is separate from the hardening JSON and must appear in Claude’s response to the user so that the human or GPT can verify it without opening the JSON file.

### Required checklist format

```
## Hardening Evidence Checklist — [work_id]

### Front Matter
| Field         | Value                        | Status |
|---------------|------------------------------|--------|
| work_id       | ...                          | PASS   |
| branch        | ...                          | PASS   |
| risk_level    | ...                          | PASS   |
| execution_model | ...                        | PASS   |
| change_type   | ...                          | PASS   |

### Authority Paths — File Existence + Content Read
| File | Exists | Content Read | Key Finding | Status |
|------|--------|--------------|-------------|--------|
| [path] | YES | YES — [what was read and what line/field confirmed the claim] | ... | PASS/BLOCKED |

### Source File Cross-Reference (ingestion sprints)
| Source Field | Schema Accepts | Runtime Handles | Status |
|--------------|---------------|-----------------|--------|
| [field_name] | YES — [schema file line N] | YES — [evaluator file line N] | PASS/BLOCKED |

### Prior Task Findings
| Claimed Finding | Artifact Exists | Independently Re-verified | Status |
|-----------------|-----------------|--------------------------|--------|
| [claim] | YES/NO | YES/NO — [evidence] | PASS/BLOCKED |

### Forbidden Files
| File | Required by Sprint? | Status |
|------|---------------------|--------|
| backend/core/analytics/ | NO | PASS |
| [other forbidden paths] | NO | PASS |

### Overall Hardening Verdict
[ ] HARDENED — all checks pass, citations present, no blockers found
[ ] BLOCKED — [exact blocker stated]
```

### Enforcement rule

**If any row in the evidence checklist contains no file path and line number citation, the hardening is incomplete.**

The human or GPT reviewer must reject the hardening and request a redo if:
* Any authority path claim has no file+line citation
* Any source field cross-reference row is missing
* The "Content Read" column shows NO for any source file
* The "Prior Task Findings" section is absent when a prior task is referenced in the prompt

A hardening JSON that says `"CONFIRMED"` with no evidence is not a completed hardening. It is a placeholder.

---

## Stage 3 — Kernel Start

Command:

```powershell
python backend/scripts/run_work_package.py start
```

Kernel preflight must fail immediately if:

* Prompt is missing
* Hardening file is missing
* `hardening.status != HARDENED`
* `work_id` mismatch exists between prompt and hardening
* Working tree is not clean
* Current branch does not match prompt branch
* Prompt front matter is malformed
* First non-empty line is not `---`
* Front matter is not closed with `---`
* Required fields are missing

If valid, kernel writes two artifacts:

### 1. Work Package Lifecycle State

```yaml
status: IN_PROGRESS
started_utc: ISO_UTC
branch: current_branch
head_sha: current_sha
work_id: ...
```

### 2. Execution Authority Token

File:

`automation_bus/state/work_package_active.json`

Example:

```json
{
  "work_id": "...",
  "branch": "...",
  "head_sha": "...",
  "started_utc": "..."
}
```

This token represents kernel-issued execution authority.

Cursor must not begin implementation without this file.

Kernel must not run the gate during `start`.

---

## Stage 4 — Cursor Execution

Cursor reads the hardened prompt and performs the implementation work.

Before modifying any repository files, Cursor must verify:

1. `automation_bus/state/work_package_active.json` exists
2. `work_id` matches the prompt
3. The current branch matches the prompt branch

If the token is missing or mismatched, Cursor must STOP and report:

> Kernel start not executed or work package mismatch.

Cursor must:

* Follow prompt scope exactly
* Make only in-scope changes
* Avoid introducing additional logic
* Preserve determinism

Cursor must not:

* Reinterpret requirements
* Self-certify success
* Modify `latest_cursor_status.json`

---

## Stage 5 — Kernel Finish

Command:

```powershell
python backend/scripts/run_work_package.py finish
```

Kernel must:

* Verify current status is `IN_PROGRESS`
* Verify `work_id` consistency
* Invoke the gate:

```powershell
python backend/scripts/golden_gate_local.py
```

* Require the gate to produce:

  * `automation_bus/latest_gate_evidence.json`
  * `automation_bus/latest_gate_output.txt`
* Treat gate evidence as immutable and never mutate it

### Completion Rules

If:

* gate exit code = 0
* evidence.overall.status = PASS
* evidence.work_id matches prompt.work_id

Then kernel writes:

```yaml
status: COMPLETE
```

Else kernel writes:

```yaml
status: FAILED
```

Kernel must exit non-zero on FAILED.

After successful finish, kernel must remove:

`automation_bus/state/work_package_active.json`

This closes the execution authority window.

---

# 8. No-op Sprint Protection

If preflight determines:

* No remaining defect
* No uncovered functionality
* No unresolved behavioural issue

Then:

* The sprint must not be created
* A prompt must not be written

No-op remediation work is prohibited unless explicitly re-authorised.

---

# 9. Evidence Immutability

The following artifacts must never be modified by control-plane scripts after creation:

* `automation_bus/latest_gate_evidence.json`
* `automation_bus/latest_gate_output.txt`

All evidence artifacts must:

* Be generated during execution
* Remain immutable after creation
* Accurately reflect system state

No manual modification is permitted.

Evidence schema versioning is independent of SOP versioning.

---

# 10. Audit Summary Requirements

After kernel finish, Claude reads:

* `automation_bus/latest_gate_evidence.json`
* `automation_bus/latest_cursor_status.json`
* repository diff

Claude writes:

`automation_bus/latest_audit_summary.md`

### Required YAML Header Fields

```yaml
---
audit_schema_version: "1.0"
work_id:
risk_level:
gate_status:
failure_type: NONE | MECHANICAL | ARCHITECTURAL
files_touched:
contract_adjacent: true | false
boundary_files_touched: true | false
content_review: COMPLETE | NOT_APPLICABLE
behaviour_review: COMPLETE | NOT_APPLICABLE
recommendation:
escalation_required: true | false
---
```

### Required Body Sections

* Summary
* Files Touched
* Contract Assessment
* Recommended Action

### Behavioural Audit Requirements

For Intelligence Core work, the audit must explicitly confirm:

* Determinism preserved
* No unintended behavioural drift
* Output structure unchanged unless intentionally changed
* Ranking and ordering stable unless intentionally changed
* No hidden side effects
* Content review completed if governed content changed
* Behaviour review completed if emitted reasoning could change

---

# 11. HIGH Risk Rules

A work package is HIGH risk if:

* It touches Intelligence Core
* It modifies behavioural logic
* It affects output generation
* It touches any of:

  * `backend/ssot/`
  * `backend/core/pipeline/`
  * `backend/core/analytics/`
  * `backend/scripts/run_work_package.py`
  * `backend/scripts/golden_gate_local.py`
  * `backend/scripts/update_cursor_status.py`

HIGH risk requires:

* Claude audit summary
* GPT architectural review
* Dual approval before merge

---

# 12. Docs-Only Bypass

Docs-only bypass is allowed only when all changes are under `/docs/`.

Operator must run:

```powershell
git diff HEAD --name-only
```

If any file outside `/docs/` is present, the Automation Bus is required.

No human judgment exception exists.

---

# 13. Infrastructure / Control-Plane Execution Deferral

If a work package modifies any enforcement script:

* `backend/scripts/run_work_package.py`
* `backend/scripts/golden_gate_local.py`
* `backend/scripts/update_cursor_status.py`

Then execution must not occur until after:

* Implementation is complete
* Changes are committed and merged
* A fresh branch checkout is performed

Definition of fresh branch checkout:

* Checkout a clean branch state after merge, such as checking out main and pulling, then creating a new feature branch, ensuring there are no uncommitted changes

Control-plane scripts must not execute themselves mid-refactor.

---

# 14. Determinism Rules

All JSON written by control-plane scripts must:

* Use stable indentation
* Use sorted keys where applicable
* Use ISO UTC timestamps only
* Avoid randomness and UUID generation in kernel outputs

All Intelligence Core changes must prove:

> Identical input produces identical output.

There must be:

* No randomness
* No hidden state
* No implicit ordering dependencies
* No silent behavioural drift

Kernel must:

* Exit non-zero on any failure
* Never silently continue
* Never swallow exceptions

---

# 15. Non-Negotiable Rules

The following rules cannot be violated:

* No behavioural change without explicit declaration
* No silent output drift
* No execution without a HARDENED prompt
* No sprint without real work
* No bypassing of Kernel or Gate
* No modification of evidence artifacts
* No deviation from branch isolation
* No conversational bypass of kernel for in-scope work packages
* No manual writing of terminal status as substitute for kernel finish
* No gate skipping
* No modification of control-plane scripts without HIGH classification
* No introduction of fallback parsers
* No creation of duplicate SSOT authority sources
* No hardening without a Stage 2C evidence checklist — file existence alone is not hardening
* No "CONFIRMED" claim in a hardening JSON without a cited file path and line number
* No inheritance of prior task findings without an artifact or independent re-verification
* No source file treated as compatible without its content having been read and cross-referenced against schema and runtime
* No `run_work_package.py finish` without passing the mandatory Post-Implementation Closure Protocol
* No tooling-file leakage (`.codex/`, `.vscode/`, `AGENTS.md`, or equivalent local tooling assets) into governed sprint branches unless explicitly in scope
* No stash use as routine sprint-closure convenience

---

# 16. Design Philosophy

The Automation Bus is:

* A deterministic execution system
* A governance layer for intelligence
* A safeguard against architectural drift
* A control-plane for reasoning systems

It enforces:

* Truth over assumption
* Structure over improvisation
* Determinism over approximation

GPT defines architecture.
Claude enforces discipline.
Cursor implements.
Kernel validates state.
Gate verifies deterministically.

The system guarantees integrity.

---

**Version:** v1.3.1
**Edition:** Intelligence Governance Edition — Hardening Evidence Standard
**Status:** LOCKED

```
```
