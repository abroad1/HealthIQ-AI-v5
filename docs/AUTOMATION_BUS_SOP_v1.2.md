# AUTOMATION BUS SOP v1.2  
**Final — Operationally Validated Edition**

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
- Regulatory-grade reproducibility

Governance must be enforced by mechanism, not memory.

---

# 2. Role Separation (B.1 Model)

| Agent | Authority | Cannot Do |
|--------|------------|------------|
| GPT | Architecture authority | Cannot modify repo |
| Claude Code | Mechanical audit + prompt hardening | Cannot merge |
| Cursor | Code execution only | Cannot self-certify |
| Kernel | State enforcement only | Cannot modify evidence |
| Gate | Deterministic verification | Cannot modify state |
| Human | Merge authority | Cannot bypass kernel |

No agent writes another agent’s artifact.

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

Artifacts are runtime state and gitignored unless explicitly versioned.

---

# 4. Work Package Lifecycle

---

## Stage 0 — Branch Alignment (Pre-Execution Check)

Before Cursor begins implementation:

Confirm current branch matches `branch:` in prompt front matter.

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

Rules:

- `execution_model` is mandatory for infrastructure or control-plane work.
- Work package must define allowed and forbidden actions if sequencing-sensitive.
- If introducing a new script, prompt must state explicitly:

> Implementation-only. Do not execute target script during this sprint unless explicitly permitted.

---

## Stage 2 — Hardening (Claude Code)

Claude:

- Reviews prompt
- Tightens STOP conditions
- Validates file scope
- Ensures PowerShell compatibility
- Confirms execution_model correctness

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

---

## Stage 3 — Kernel Start

Command:

```powershell
python backend/scripts/run_work_package.py start
```

Kernel preflight must fail immediately if:

- Prompt missing
- Hardening file missing
- work_id mismatch
- Working tree not clean
- Current branch ≠ prompt branch
- Prompt malformed
- First non-empty line ≠ `---`
- Front matter not closed
- Required fields missing

If valid, write:

```yaml
status: IN_PROGRESS
started_utc: ISO_UTC
branch: current_branch
head_sha: current_sha
work_id: ...
```

Kernel must not run the gate during `start`.

---

## Stage 4 — Cursor Execution

Cursor reads hardened prompt.

Cursor performs implementation work.

Important:

- Cursor is interactive.
- Kernel does not call Cursor.
- Kernel does not execute implementation code.
- Cursor must not run gate manually.
- Cursor must not modify status file directly.

---

## Stage 5 — Kernel Finish

Command:

```powershell
python backend/scripts/run_work_package.py finish
```

Kernel must:

- Verify status == IN_PROGRESS
- Verify work_id consistency
- Run golden gate
- Require gate to produce:
  - latest_gate_evidence.json
  - latest_gate_output.txt
- Treat evidence as immutable

### Gate Is Mandatory Test Phase

Kernel finish runs the mandatory regression gate and will not mark COMPLETE unless the gate passes.

Completion rules:

If:

- exit_code == 0
- evidence.overall.status == PASS
- work_id matches

Then set:

```yaml
status = COMPLETE
```

Else set:

```yaml
status = FAILED
```

Kernel must exit non-zero on FAILED.

Manual COMPLETE is disallowed.

---

# 5. Evidence Immutability Invariant

No control-plane script may modify:

- latest_gate_evidence.json
- latest_gate_output.txt

Kernel is read-only consumer.

Violation = HIGH risk breach.

---

# 6. Audit Summary (Claude)

After finish:

Claude reads:

- latest_gate_evidence.json
- latest_cursor_status.json
- git diff

Claude writes:

`automation_bus/latest_audit_summary.md`

Required YAML header:

```yaml
---
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

Required body sections:

- Summary
- Files Touched
- Contract Assessment
- Recommended Action

---

# 7. HIGH Risk Rules

HIGH risk if:

- backend/ssot modified
- backend/core/pipeline modified
- backend/core/analytics modified
- run_work_package.py modified
- golden_gate_local.py modified
- update_cursor_status.py modified

HIGH risk requires:

- Claude audit
- GPT architectural review
- Dual approval before merge

---

# 8. Docs-Only Bypass (Mechanically Enforced)

Allowed only if:

```powershell
git diff --name-only
```

returns files exclusively under `/docs/`.

If any file outside `/docs/` is present:

Bus required.

No human judgment exception.

---

# 9. Infrastructure Introduction Rule

If work package modifies:

- run_work_package.py
- golden_gate_local.py
- update_cursor_status.py

Execution must not occur until after:

- Implementation complete
- Merge complete
- Fresh branch checkout

Control-plane scripts must not execute themselves mid-refactor.

---

# 10. Determinism Rules

All JSON must:

- Use sorted keys
- Stable indentation
- ISO UTC timestamps only
- No randomness
- No UUID generation in kernel

Kernel must:

- Exit non-zero on any failure
- Never silently continue
- Never swallow exceptions

---

# 11. Non-Negotiables

- No conversational bypass of kernel
- No manual COMPLETE writing
- No gate skipping
- No evidence mutation
- No execution without HARDENED prompt
- No modification of control-plane scripts without HIGH classification
- No extension of legacy clustering engine
- No introduction of fallback parsers

---

# 12. Design Philosophy

The Automation Bus is:

- A deterministic governance layer
- A regulatory defensibility mechanism
- A control-plane integrity system

If compliance depends on memory, it is not compliance.

Governance must be mechanical.

---

**Version: v1.2 (Operationally Validated Edition)**  
Status: LOCKED

