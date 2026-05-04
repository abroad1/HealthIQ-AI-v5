# HealthIQ AI --- Automation Bus SOP v1.1

**Status:** Active\
**Type:** Governance Control Plane\
**Applies To:** All runtime-impacting changes\
**Authority Level:** Non-Negotiable

This document defines the exact, enforced development workflow for
multi-agent execution across:

-   GPT (Architecture Authority)
-   Claude Code (Prompt Hardening + Independent Review)
-   Cursor (Execution Agent)
-   Gate Scripts (Deterministic Enforcement)
-   Human (Merge Authority)

This is not a suggestion.\
It is the control plane.

No variation is permitted without explicit version update.

------------------------------------------------------------------------

# 1. Core Principles

1.  Single writer per file.
2.  File-based authority --- never chat-based authority.
3.  No silent modifications.
4.  Mechanical enforcement before execution.
5.  Deterministic verification before merge.
6.  Layer sovereignty preserved (A / B / C).
7.  Human remains final merge authority.

------------------------------------------------------------------------

# 2. Runtime Files (gitignored)

Located in `/automation_bus/`:

-   `latest_cursor_prompt.md` --- Written by GPT\
-   `latest_prompt_hardening.json` --- Written by Claude Code\
-   `latest_cursor_status.json` --- Written by Cursor\
-   `latest_gate_evidence.json` --- Written by Gate Script\
-   `latest_gate_output.txt` --- Written by Gate Script

No agent may modify another agent's file.

File ownership is absolute.

------------------------------------------------------------------------

# 3. Work Package Lifecycle --- Low Risk

Examples:

-   Refactors
-   Script wiring
-   Bug fixes
-   Test additions
-   Enforcement in report-only mode

------------------------------------------------------------------------

## Step 1 --- Prompt Authoring (GPT)

GPT writes:

`automation_bus/latest_cursor_prompt.md`

Prompt must include:

-   work_id
-   branch
-   goal
-   non_goals
-   invariants
-   stop_conditions
-   allowed_files
-   forbidden_files
-   verification_command

No incomplete prompts permitted.

------------------------------------------------------------------------

## Step 2 --- Prompt Hardening (Mandatory)

Claude Code:

-   Opens `latest_cursor_prompt.md`
-   Tightens ambiguity
-   Strengthens STOP conditions
-   Validates allowed_files scope
-   Corrects file targeting
-   Ensures PowerShell compatibility
-   Edits prompt in place if required

Claude must then write:

`automation_bus/latest_prompt_hardening.json`

Schema:

``` json
{
  "bus_version": "1.1",
  "work_id": "...",
  "status": "HARDENED",
  "hardened_utc": "...",
  "hardened_by": "claude_code",
  "changes": []
}
```

Rules:

-   `changes` field MUST exist.
-   If no changes were required → empty list.
-   Silent edits are prohibited.
-   work_id must match prompt file.
-   bus_version must match this SOP version.

Execution cannot begin without this file.

------------------------------------------------------------------------

## Step 3 --- Execution Preflight (Cursor)

Cursor runs:

``` bash
python backend/scripts/update_cursor_status.py IN_PROGRESS
```

Script enforces:

-   Hardening file exists
-   status == HARDENED
-   work_id matches prompt
-   changes field exists
-   bus_version matches expected

If validation fails → execution blocked.

No override permitted.

------------------------------------------------------------------------

## Step 4 --- Execution (Cursor)

Cursor performs work exactly as described in hardened prompt.

No file outside `allowed_files` may be modified.

STOP conditions must be respected.

------------------------------------------------------------------------

## Step 5 --- Gate Enforcement (Cursor)

Cursor runs:

``` bash
python backend/scripts/golden_gate_local.py
```

Gate must:

-   Immediately write FAIL stub
-   Enforce branch match
-   Run baseline tests
-   Run three-layer verification
-   Produce structured evidence JSON
-   Produce transcript file
-   Exit non-zero on failure

Gate is deterministic authority.

------------------------------------------------------------------------

## Step 6 --- Completion (Mechanically Enforced)

Cursor runs:

``` bash
python backend/scripts/update_cursor_status.py COMPLETE
```

(or FAILED)

Mechanical Enforcement Rule:

COMPLETE must be rejected unless:

-   `latest_gate_evidence.json` exists
-   evidence.work_id matches prompt.work_id
-   overall.status == PASS
-   exit_code == 0

Self-reporting COMPLETE is prohibited.

FAILED may be set if:

-   STOP condition triggered
-   Preflight failed
-   Gate failed

------------------------------------------------------------------------

## Step 7 --- Audit (GPT)

GPT audits:

-   latest_gate_evidence.json
-   latest_gate_output.txt
-   latest_cursor_status.json

No copy/paste required.

Audit confirms:

-   Scope compliance
-   No file drift
-   Deterministic enforcement integrity
-   Layer boundary preserved

------------------------------------------------------------------------

## Step 8 --- Merge (Human)

Human reviews:

-   GPT audit
-   Diff
-   Architectural implications

Human decides merge.

No automated merge.

------------------------------------------------------------------------

# 4. High-Risk Work Package Additions

High-risk examples:

-   SSOT changes
-   Orchestrator logic
-   Ratio registry
-   Cluster schema
-   Snapshot schema
-   Gate modifications
-   Layer boundary enforcement
-   InsightGraph contract changes

Additional Requirement:

After Step 7:

Claude Code must independently review:

-   Prompt
-   Evidence
-   Contract adherence
-   Layer boundary compliance

Merge only after dual review.

Note: High-risk review is governance-enforced but not yet mechanically
blocked at COMPLETE stage (future enhancement candidate).

------------------------------------------------------------------------

# 5. Documentation-Only Classification (v1.1 Clarification)

Automation Bus is required for any change affecting:

-   backend/
-   ssot/
-   tests/
-   automation_bus/
-   .github/workflows/
-   Runtime behaviour
-   Snapshot schema
-   InsightGraph structure
-   Registry logic
-   Contract definitions
-   Version increments

Automation Bus is NOT required for documentation-only edits under
`/docs` provided ALL conditions are met:

1.  No runtime behaviour altered.
2.  No schema or contract semantics altered.
3.  No version increment.
4.  `git diff --name-only` shows only `/docs` files changed.
5.  Human reviews diff before merge.
6.  Baseline + three-layer verification pass on main after merge.

If ambiguity exists → use the bus.

No "sometimes we skip the bus."

------------------------------------------------------------------------

# 6. Prompt File Integrity Requirements (v1.1 Amendment)

Prompt files are part of the control plane.

Strict formatting required.

## Formatting Requirements

-   File must be UTF-8 (without BOM).
-   YAML front matter must begin with `---`.
-   Keys must use plain ASCII characters.
-   No escaped underscores (e.g. `work\_id` invalid).
-   No HTML entities (e.g. `&nbsp;`).
-   No smart quotes.
-   No Markdown escape artifacts.

## Creation Standard

-   Use plain text editor only (e.g., Notepad).
-   Rich text or formatted Markdown editors prohibited.
-   Do not paste from rendered Markdown blocks that escape underscores.

## Verification Requirement

Before hardening:

-   Confirm file path.
-   Compute file hash (`Get-FileHash`).
-   Visually confirm YAML header structure.

Future enhancement (optional): Prompt linter rejecting malformed YAML
keys.

------------------------------------------------------------------------

# 7. Non-Negotiables

-   No bypassing hardening.
-   No silent prompt edits.
-   No skipping gate.
-   No COMPLETE without PASS evidence.
-   No editing another agent's file.
-   No weakening enforcement to avoid surfacing debt.
-   No changing SOP without explicit version increment.

------------------------------------------------------------------------

# 8. Versioning

This document governs Automation Bus v1.1.

If workflow mechanics change:

-   Increment version.
-   Update filename if required.
-   Update bus_version in hardening JSON schema.

No silent evolution.
