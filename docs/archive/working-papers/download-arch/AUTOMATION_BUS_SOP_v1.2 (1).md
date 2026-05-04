# HealthIQ AI

# AUTOMATION BUS SOP v1.2

**Status:** Locked for Circulation\
**Supersedes:** v1.1\
**Date:** 2026-03-02

------------------------------------------------------------------------

# 0. Architectural Intent

The Automation Bus is part of HealthIQ's control plane.

It exists to ensure:

-   Deterministic execution\
-   Separation of powers\
-   No self-reported PASS states\
-   No conversational enforcement reliance\
-   Audit traceability\
-   Architectural drift protection

If compliance depends on memory, it is not compliance.\
Governance must be enforced by mechanism.

------------------------------------------------------------------------

# 1. Separation of Powers (B.1 Model)

  ----------------------------------------------------------------------------
  Function              Responsible Agent                     Type
  --------------------- ------------------------------------- ----------------
  Strategic             GPT                                   Longitudinal
  Architecture                                                judgment

  Prompt Authoring      GPT                                   Contract
                                                              authority

  Prompt Hardening      Claude Code                           Scope tightening

  Execution             Cursor                                Implementation
                                                              only

  Mechanical Audit      Claude Code                           Deterministic

  Architectural Audit   GPT (STANDARD/HIGH)                   Pattern &
                                                              invariant
                                                              oversight

  Merge Authority       Human                                 Final approval
  ----------------------------------------------------------------------------

No single agent controls the full lifecycle.

------------------------------------------------------------------------

# 2. Risk Stratification (Mandatory)

Each work package must declare in YAML front matter:

``` yaml
risk_level: LOW | STANDARD | HIGH
```

## LOW

Minor refactors, logging changes, test additions.

Requires: - Hardening - Single-entry execution - Gate PASS - Claude
mechanical audit - No GPT involvement unless escalated

## STANDARD

Structural refactors, Layer B changes, internal migrations.

Requires: - Hardening - Single-entry execution - Gate PASS - Claude
mechanical audit - GPT review of audit summary

## HIGH

SSOT changes, schema changes, registry logic, InsightGraph core, gate
logic, execution kernel changes.

Requires: - Hardening - Single-entry execution - Gate PASS - Claude
mechanical audit - GPT architectural review - Dual approval before merge

------------------------------------------------------------------------

# 3. Execution Kernel

All execution must occur via:

    backend/scripts/run_work_package.py

This script enforces governance but does not execute Cursor directly.

Execution model:

1.  Validate prompt exists\
2.  Validate hardening JSON exists\
3.  Validate matching work_id\
4.  Validate clean working tree\
5.  Write IN_PROGRESS\
6.  Cursor (interactive agent) reads and executes instructions from
    latest_cursor_prompt.md\
7.  Run golden_gate_local.py\
8.  Write COMPLETE or FAILED strictly based on gate\
9.  Prevent state skipping

Conversational execution outside this process is prohibited.

------------------------------------------------------------------------

# 4. Deterministic State Machine

    DRAFT → HARDENED → IN_PROGRESS → COMPLETE | FAILED

No intermediate governance states allowed.

------------------------------------------------------------------------

# 5. Mechanical Audit (Claude Code)

After execution:

Claude reads: - latest_gate_evidence.json\
- latest_gate_output.txt\
- latest_cursor_status.json\
- git diff

Claude writes:

    automation_bus/latest_audit_summary.md

------------------------------------------------------------------------

# 6. Audit Summary Schema (Mandatory)

## YAML Front Matter

``` yaml
---
bus_version: "1.2"
work_id: "<string>"
risk_level: "LOW|STANDARD|HIGH"
branch: "<branch>"
head_sha: "<git sha>"
gate_status: "PASS|FAIL"
scope_compliant: true|false
contract_adjacent: true|false
boundary_files_touched: true|false
forbidden_files_touched: true|false
failure_class: "NONE|MECHANICAL|ARCHITECTURAL"
escalation_required: true|false
recommendation: "MERGE|RETRY|ESCALATE|REJECT"
---
```

Missing fields invalidate audit.

------------------------------------------------------------------------

## Required Body Structure

### 1. Executive Summary

Brief PASS/FAIL overview and classification.

### 2. Files Touched

Bullet list of changed files.

### 3. Contract & Boundary Assessment

Explain contract_adjacent and boundary_files_touched.

### 4. Gate Verification Results

Baseline, three-layer, and exit code.

### 5. Failure Analysis (if applicable)

Root cause and classification.

### 6. Recommended Action

Aligned with recommendation field.

------------------------------------------------------------------------

# 7. Failure Classification

If gate_status = FAIL:

-   MECHANICAL → retry permitted\
-   ARCHITECTURAL → escalate to GPT

------------------------------------------------------------------------

# 8. Contract & Boundary Definitions

contract_adjacent = true if touching:

-   backend/ssot/\
-   backend/core/pipeline/\
-   backend/core/analytics/\
-   backend/core/snapshot/\
-   Ratio registry\
-   InsightGraph schema

boundary_files_touched = true if modifying:

-   Layer boundaries\
-   Canonical computation logic\
-   Cluster logic\
-   Enforcement rules\
-   Data flow between layers

If uncertain → set to true.

------------------------------------------------------------------------

# 9. GPT Involvement Rules

GPT reviews only latest_audit_summary.md.

Mandatory for: - HIGH risk - STANDARD risk - escalation_required =
true - failure_class = ARCHITECTURAL

Not required for LOW PASS.

------------------------------------------------------------------------

# 10. Documentation-Only Bypass (Mechanically Enforced)

Permitted only if:

1.  git diff shows all modified files under /docs/\
2.  No runtime files changed\
3.  Baseline tests PASS\
4.  No schema version increment

Otherwise LOW risk bus required.

------------------------------------------------------------------------

# 11. Operator Handoff Format

Each stage must end with:

    TERMINAL_STATUS: <TOKEN>
    NEXT_ACTION: <ONE-LINE INSTRUCTION>

## Allowed TERMINAL_STATUS Tokens

Claude (Hardening): - READY_FOR_CURSOR\
- REJECT_PROMPT\
- ESCALATE_TO_GPT

Cursor: - COMPLETE\
- FAILED

Claude (Audit): - PASS\
- RETRY\
- ESCALATE_TO_GPT

NEXT_ACTION must reference work_id only.

------------------------------------------------------------------------

# 12. Non-Negotiables

-   No execution outside run_work_package.py\
-   No COMPLETE without PASS\
-   No silent file edits\
-   No modifying another agent's file\
-   No weakening gate enforcement\
-   No conversational enforcement dependency

Automatic HIGH classification required for modification of:

-   run_work_package.py\
-   golden_gate_local.py\
-   update_cursor_status.py\
-   Audit summary generator\
-   Automation bus schema

------------------------------------------------------------------------

# 13. Expected Impact

v1.2 provides:

-   Deterministic enforcement\
-   Clear separation of powers\
-   Mechanical retry loop\
-   Reduced human cognitive load\
-   Escalation clarity\
-   Control-plane hardening

This version is approved for adversarial circulation and validation.
