# AUTOMATION BUS SOP v1.2  
**Final — Operationally Validated Edition (Execution Authority Enforcement Update)**

Status: LOCKED  
Authority: Control-Plane Enforcement  
Supersedes: All prior v1.2 drafts  

---

# 1. Purpose

The Automation Bus defines the deterministic control-plane governing all work packages in HealthIQ AI v5.2.

It enforces:

- Sequenced execution
- Immutable evidence
- State-machine discipline
- Branch isolation
- Deterministic regression gating
- Clear separation of authority
- Reproducibility suitable for future regulatory alignment

Critical execution invariants are enforced by mechanism.
Architectural authority integrity is enforced at Stage 1 (Authoring).

---

# 2. Role Separation (B.1 Model)

| Agent | Authority | Cannot Do |
|--------|------------|------------|
| GPT | Architecture authority | Cannot modify repo |
| Claude Code | Prompt hardening + mechanical audit | Cannot merge |
| Cursor | Code execution only | Cannot self-certify test success |
| Kernel (`run_work_package.py`) | State enforcement only | Cannot modify gate evidence |
| Gate (`golden_gate_local.py`) | Deterministic verification | Cannot modify status |
| Human operator | Merge authority | Cannot bypass kernel for in-scope work packages |

Notes:

- Artifact ownership (single-writer) is a governance convention enforced by review discipline, not by OS-level locking.
- Critical pass/fail is enforced by kernel + gate evidence.
- SSOT authority integrity is enforced at Stage 1 prior to prompt issuance.

---

# 3. Automation Artifacts (Single Writer Rule)

| File | Author |
|-------|--------|
| automation_bus/latest_cursor_prompt.md | GPT |
| automation_bus/latest_prompt_hardening.json | Claude |
| automation_bus/latest_cursor_status.json | Kernel |
| automation_bus/latest_gate_evidence.json | Gate |
| automation_bus/latest_gate_output.txt | Gate |
| automation_bus/latest_audit_summary.md | Claude |
| automation_bus/state/work_package_active.json | Kernel |

Artifacts are runtime state and are gitignored unless explicitly versioned.

---

# 4. Work Package Lifecycle

---

## Stage 0 — Branch Alignment (Pre-Implementation Check)

Before Cursor begins implementation, confirm current branch matches `branch:` in prompt front matter.

This prevents cross-branch contamination before any work begins.

---

## Stage 1 — Authoring (GPT)

GPT writes:

`automation_bus/latest_cursor_prompt.md`

Prompt must include YAML front matter:

```yaml
---
work_id: "<ID>"
branch: "<branch>"
risk_level: LOW | STANDARD | HIGH
execution_model: SINGLE_PHASE | TWO_PHASE_START_FINISH
---
```

### Stage 1 Authority Preflight (Mandatory)

Before writing `latest_cursor_prompt.md`, GPT must verify:

1. The authoritative SSOT file path from the current branch.
2. The runtime loader that consumes that SSOT file.
3. That no parallel or duplicate schema file exists for the same domain.
4. That the proposed changes will not create a second authoritative source.
5. That tests and runtime loaders reference the same authority file.

If any ambiguity exists regarding authoritative file location or loader wiring, the prompt must explicitly resolve it before proposing changes.

Failure to perform this check risks schema forks and silent authority drift.

This verification is architectural and mandatory. It is not delegated to kernel or gate.

---

Rules:

- `execution_model` is mandatory for infrastructure or control-plane work.
- Work package must define allowed and forbidden actions if sequencing-sensitive.
- If introducing a new script, prompt must explicitly state:

> Implementation-only. Do not execute target script during this sprint unless explicitly permitted.

---

## Stage 2 — Hardening (Claude Code)

Claude:

- Reviews prompt
- Tightens STOP conditions
- Validates file scope
- Ensures PowerShell compatibility
- Confirms `execution_model` correctness

Claude writes:

`automation_bus/latest_prompt_hardening.json`

Schema:

```json
{
  "bus_version": "1.2",
  "work_id": "...",
  "status": "HARDENED",
  "changes": [],
  "hardened_utc": "...",
  "hardened_by": "claude-code"
}
```

Execution is blocked unless `status == HARDENED`.

This is enforced mechanically by the kernel preflight.

---

## Stage 3 — Kernel Start

Command:

```powershell
python backend/scripts/run_work_package.py start
```

Kernel preflight must fail immediately if:

- Prompt missing
- Hardening file missing
- `hardening.status != HARDENED`
- `work_id` mismatch between prompt and hardening
- Working tree not clean
- Current branch ≠ prompt branch
- Prompt front matter malformed
- First non-empty line ≠ `---`
- Front matter not closed with `---`
- Required fields missing

If valid, kernel writes two artifacts:

1. Work package lifecycle state

```yaml
status: IN_PROGRESS
started_utc: ISO_UTC
branch: current_branch
head_sha: current_sha
work_id: ...
```

2. Execution authority token

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

### Mandatory Execution Guard

Before modifying any repository files, Cursor must verify:

1. `automation_bus/state/work_package_active.json` exists
2. `work_id` matches the prompt
3. Current branch matches the prompt branch

If the token is missing or mismatched, Cursor must STOP and report:

"Kernel start not executed or work package mismatch."

This prevents code modifications occurring outside an active work package lifecycle.

Important:

- Cursor is interactive.
- Kernel does not call Cursor.
- Kernel does not execute implementation code.
- Cursor must not modify `latest_cursor_status.json`.

---

## Stage 5 — Kernel Finish

Command:

```powershell
python backend/scripts/run_work_package.py finish
```

Kernel must:

- Verify current status == IN_PROGRESS
- Verify `work_id` consistency
- Invoke the gate:

```powershell
python backend/scripts/golden_gate_local.py
```

- Require gate to produce:
  - `automation_bus/latest_gate_evidence.json`
  - `automation_bus/latest_gate_output.txt`
- Treat gate evidence as immutable and never mutate it

### Gate Is the Mandatory Test Phase

Kernel finish runs the mandatory regression gate and will not mark COMPLETE unless the gate passes.

Completion rules:

If:

- gate exit_code == 0
- evidence.overall.status == PASS
- evidence.work_id matches prompt.work_id

Then kernel writes:

```yaml
status = COMPLETE
```

Else kernel writes:

```yaml
status = FAILED
```

Kernel must exit non-zero on FAILED.

Manual COMPLETE is disallowed by governance policy; the kernel is the authoritative state writer.

After successful finish the kernel must remove:

`automation_bus/state/work_package_active.json`

This closes the execution authority window.

---

# 5. Evidence Immutability Invariant

No control-plane script may modify:

- `automation_bus/latest_gate_evidence.json`
- `automation_bus/latest_gate_output.txt`

The kernel is a read-only consumer of evidence.

Violation = HIGH risk breach.

### Evidence Versioning

Gate evidence artifacts contain their own schema version identifier.

Evidence schema versioning is independent from SOP versioning.

This prevents governance documentation changes from invalidating historical audit artifacts.

---

# 6. Audit Summary (Claude)

After kernel finish:

Claude reads:

- `automation_bus/latest_gate_evidence.json`
- `automation_bus/latest_cursor_status.json`
- repository diff

Claude writes:

`automation_bus/latest_audit_summary.md`

## Audit Summary Schema (Authoritative)

YAML header must include:

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
recommendation:
escalation_required: true | false
---
```

Body must contain these sections (even if brief):

- Summary
- Files Touched
- Contract Assessment
- Recommended Action

---

# 7. HIGH Risk Rules

A work package is HIGH risk if it touches any of:

- `backend/ssot/`
- `backend/core/pipeline/`
- `backend/core/analytics/`
- `backend/scripts/run_work_package.py`
- `backend/scripts/golden_gate_local.py`
- `backend/scripts/update_cursor_status.py`

HIGH risk requires:

- Claude audit summary
- GPT architectural review
- Dual approval before merge

---

# 8. Docs-Only Bypass (Mechanically Enforced)

Docs-only bypass is allowed only when all changes are under `/docs/`.

Operator must run:

```powershell
git diff HEAD --name-only
```

If any file outside `/docs/` is present, the bus is required.

No human judgment exception.

---

# 9. Infrastructure / Control-Plane Execution Deferral

If a work package modifies any enforcement script:

- `backend/scripts/run_work_package.py`
- `backend/scripts/golden_gate_local.py`
- `backend/scripts/update_cursor_status.py`

Then execution must not occur until after:

- implementation is complete
- changes are committed and merged
- a fresh branch checkout is performed

Definition: fresh branch checkout

- Checkout a clean branch state after merge (e.g., checkout main and pull, then create a new feature branch), ensuring there are no uncommitted changes.

Control-plane scripts must not execute themselves mid-refactor.

---

# 10. Determinism Rules

All JSON written by control-plane scripts must:

- Use stable indentation
- Use sorted keys where applicable
- Use ISO UTC timestamps only
- Avoid randomness and UUID generation in kernel outputs

Kernel must:

- Exit non-zero on any failure
- Never silently continue
- Never swallow exceptions

---

# 11. Non-Negotiables

- No conversational bypass of kernel for in-scope work packages
- No manual writing of terminal status as substitute for kernel finish
- No gate skipping
- No evidence mutation
- No execution without HARDENED prompt
- No modification of control-plane scripts without HIGH classification
- No introduction of fallback parsers
- No creation of duplicate SSOT authority sources

---

# 12. Design Philosophy

The Automation Bus is:

- A deterministic governance layer
- A traceable change-control mechanism
- A control-plane integrity system

Critical execution invariants are enforced by mechanism.
Architectural authority integrity is enforced at Stage 1.

The bus enforces execution.
GPT enforces architectural correctness.

---

**Version: v1.2 Final — Operationally Validated Edition (Execution Authority Enforcement Update)**  
Status: LOCKED

