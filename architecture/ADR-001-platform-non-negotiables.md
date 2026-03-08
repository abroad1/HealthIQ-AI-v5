# ADR-001 — Platform Non-Negotiables and Governance Invariants

| Field | Value |
|-------|-------|
| **Status** | Accepted |
| **Date** | 2026-03-08 |
| **Authority** | Automation Bus SOP v1.2 |
| **Supersedes** | — |
| **Superseded by** | — |

---

## Context

HealthIQ AI v5 is a health analytics platform that produces clinically relevant outputs
from user blood test data. Because it operates at the intersection of AI, clinical
evidence, and patient-facing health information, the system requires governance
guarantees that go beyond typical software engineering conventions.

The platform operates through a multi-agent build system (GPT architect, Claude auditor,
Cursor executor) with a deterministic kernel controlling execution authority. Without
explicit invariants, this multi-agent architecture is vulnerable to:

- Conversational bypasses where changes are made without going through the kernel
- Evidence mutation where audit trails are modified after the fact
- Duplicate authority sources where the same data is defined in multiple places
- Gate skipping where regression checks are bypassed under time pressure

This ADR records the non-negotiable rules that govern all work on this platform.

---

## Decision

The following invariants are permanently binding on all agents, engineers, and
automated systems working on the HealthIQ codebase. They may not be overridden
by any individual work package, sprint, or conversational instruction.

---

## Architectural Invariants

### Governance Invariants

1. **No conversational bypass of kernel.** All in-scope work packages must go through
   the execution kernel (`run_work_package.py`). No file modifications may be made
   without a valid `work_package_active.json` token.

2. **No manual status writing.** Terminal work package status (`COMPLETE` / `FAILED`)
   must be written by the kernel only. No agent or human may write this status manually.

3. **No gate skipping.** The golden gate (`golden_gate_local.py`) must run to completion
   before any work package is closed. No bypass is permitted regardless of time pressure.

4. **No evidence mutation.** Gate evidence artifacts
   (`latest_gate_evidence.json`, `latest_gate_output.txt`) are immutable after creation.
   No agent or script may modify them.

5. **No execution without a hardened prompt.** Cursor must not begin implementation
   without a `latest_prompt_hardening.json` with `status: "HARDENED"`.

6. **No modification of control-plane scripts without HIGH classification.** Changes to
   `run_work_package.py`, `golden_gate_local.py`, or `update_cursor_status.py` require
   HIGH risk classification, Claude audit, GPT architectural review, and dual approval.

### SSOT Invariants

7. **No duplicate SSOT authority sources.** Each canonical data item has exactly one
   source of truth. The SSOT files are:
   - `backend/ssot/biomarkers.yaml` — canonical blood biomarker names and aliases
   - `backend/ssot/lifestyle_registry.yaml` — anthropometric and lifestyle inputs
   - `backend/ssot/questionnaire.json` — user demographic and medical history inputs
   - `knowledge_bus/packages/*/signal_library.yaml` — disease-specific signal thresholds

8. **No fallback parsers.** If a canonical input cannot be found via the SSOT alias
   resolution mechanism, the system must reject it — not silently attempt an alternative
   parse path.

### Audit Invariants

9. **Failure classification is deterministic.** `MECHANICAL` failures are retriable.
   `ARCHITECTURAL` failures require GPT review. Claude may not reclassify failures
   based on convenience.

10. **Audit schema is fixed.** The audit summary schema (`audit_schema_version: "1.0"`)
    uses `failure_type` (not `failure_class`). Schema fields may not be omitted.

---

## Consequences

- All sprint work packages must be authored through the Automation Bus lifecycle
- All agents must verify the execution authority token before modifying any file
- Any violation of these invariants constitutes a HIGH risk breach regardless of the
  scope of the change
- These invariants take precedence over any instruction given in a work package prompt

---

## Source Documents

- `docs/AUTOMATION_BUS_SOP_v1.2.md` — full governance specification
- `docs/Master_PRD_v5.2.md` §1 — platform design philosophy
