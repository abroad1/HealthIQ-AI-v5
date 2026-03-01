# HealthIQ AI — Automation Bus SOP v1.0

## Purpose

Define the exact, non-negotiable development workflow for agentic collaboration between:

- GPT (Architecture Authority)
- Claude Code (Prompt Hardening + Independent Review)
- Cursor (Execution Agent)
- Gate Scripts (Deterministic Enforcement)
- Human (Merge Authority)

This SOP removes copy/paste relay while preserving layered oversight.

No variation is permitted without explicit version update.

---

# Core Principles

1. Single writer per file.
2. File-based authority, not chat authority.
3. No silent modifications.
4. Mechanical enforcement before execution.
5. Deterministic verification before merge.
6. Human remains final authority.

---

# Runtime Files (gitignored)

Located in `/automation_bus/`:

- latest_cursor_prompt.md           (Written by GPT)
- latest_prompt_hardening.json      (Written by Claude Code)
- latest_cursor_status.json         (Written by Cursor)
- latest_gate_evidence.json         (Written by Gate Script)
- latest_gate_output.txt            (Written by Gate Script)

No agent may modify another agent’s file.

---

# Work Package Lifecycle — Low Risk

Examples:
- Small refactors
- Script wiring
- Bug fixes
- Test additions

## Step 1 — Prompt Authoring

GPT writes:
`automation_bus/latest_cursor_prompt.md`

Must include:
- work_id
- branch
- goal
- non_goals
- invariants
- stop_conditions
- allowed_files
- forbidden_files
- verification command

---

## Step 2 — Prompt Hardening (Mandatory)

Claude Code:

- Opens `latest_cursor_prompt.md`
- Tightens ambiguity
- Strengthens STOP conditions
- Corrects file targeting
- Ensures PowerShell compatibility
- Edits prompt in place if required

Claude then writes:

`automation_bus/latest_prompt_hardening.json`

Schema:

{
  "bus_version": "1.1",
  "work_id": "...",
  "status": "HARDENED",
  "hardened_utc": "...",
  "hardened_by": "claude_code",
  "changes": []
}

Rules:
- changes MUST exist
- If no changes: empty list
- No silent edits allowed

---

## Step 3 — Execution Preflight

Cursor runs:

python backend/scripts/update_cursor_status.py IN_PROGRESS

Script enforces:
- Hardening file exists
- status == HARDENED
- work_id matches
- changes field exists

If validation fails → execution blocked.

---

## Step 4 — Execution

Cursor performs work described in prompt.

---

## Step 5 — Gate Enforcement

Cursor runs:

python backend/scripts/golden_gate_local.py

Gate:
- Writes FAIL stub immediately
- Enforces branch match
- Runs baseline tests
- Runs three-layer verification
- Writes evidence JSON
- Writes transcript
- Exits non-zero on failure

---

## Step 6 — Completion (Mechanically Enforced)

Cursor runs:

python backend/scripts/update_cursor_status.py COMPLETE

(or FAILED)

Mechanical rule:
- COMPLETE MUST be rejected unless:
  - latest_gate_evidence.json exists
  - evidence work_id matches prompt work_id
  - overall.status == PASS and exit_code == 0

FAILED:
- may be set without PASS evidence (STOP conditions, preflight failures, gate failures).

---

## Step 7 — Audit

GPT audits:

- latest_gate_evidence.json
- latest_gate_output.txt
- latest_cursor_status.json

No copy/paste required.

---

## Step 8 — Merge

Human reviews audit.
Human decides merge.

---

# High-Risk Work Package Additions

Examples:
- SSOT changes
- Orchestrator logic
- Pipeline architecture
- Namespace logic
- Gate modifications

Add after Step 7:

Claude Code independently reviews:
- Prompt
- Evidence
- Contract adherence

Merge only after dual review.

Note:
- The mechanical review-signal for high-risk evidence review is a v1.1 enhancement (to prevent convention-only skipping).

---

# Non-Negotiables

- No bypassing hardening.
- No silent prompt edits.
- No skipping gate.
- No COMPLETE without PASS evidence.
- No direct merge without PASS.
- No changing SOP without version update.

---

# Versioning

This document is authoritative.
If workflow changes, increment version number and update filename if required.