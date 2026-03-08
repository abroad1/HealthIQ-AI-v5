# HealthIQ Architecture Decision Registry

**Status:** Active
**Maintained by:** Architecture Authority (GPT) + Claude Code
**Location:** `architecture/`

---

## Purpose

This registry is the constitutional record of HealthIQ AI v5. Each ADR documents a
key architectural decision that defines how the system must be built. ADRs are
**immutable once accepted** — they are never edited. If an architecture evolves, a
new ADR is created that supersedes the prior one. The history of decisions is preserved.

Every engineer, sprint work package, and AI agent working on this codebase must treat
accepted ADRs as non-negotiable constraints.

---

## Registry

| ADR | Title | Status | Date | Supersedes |
|-----|-------|--------|------|------------|
| [ADR-001](ADR-001-platform-non-negotiables.md) | Platform Non-Negotiables and Governance Invariants | Accepted | 2026-03-08 | — |
| [ADR-002](ADR-002-deterministic-analysis-engine.md) | Deterministic Three-Layer Analysis Architecture | Accepted | 2026-03-08 | — |
| [ADR-003](ADR-003-knowledge-bus-architecture.md) | Knowledge Bus Evidence Architecture | Accepted | 2026-03-08 | — |
| [ADR-004](ADR-004-disease-specific-signal-evaluation.md) | Disease-Specific Signal Evaluation Architecture | Superseded | 2026-03-08 | Superseded by ADR-005 |
| [ADR-005](ADR-005-disease-specific-signal-evaluation-v2.md) | Disease-Specific Signal Evaluation Architecture (v2) | Accepted | 2026-03-08 | ADR-004 |

---

## How to use ADRs

### Referencing in code

Every file that implements an ADR-governed component must include a reference at the top:

```python
"""
Architecture reference: ADR-004 Disease-Specific Signal Evaluation Architecture
See: architecture/ADR-004-disease-specific-signal-evaluation.md
"""
```

### Referencing in sprint work packages

Every sprint work package prompt must list which ADRs it implements:

```
Implements: ADR-004
Must not violate: ADR-001, ADR-002, ADR-003
```

### Creating a new ADR

1. Assign the next sequential number
2. Use the standard template structure (see any existing ADR)
3. Set status to `Proposed` until reviewed
4. Change to `Accepted` after architecture authority review
5. Add to this index
6. Never edit an accepted ADR — create a new one that supersedes it

---

## ADR Status Definitions

| Status | Meaning |
|--------|---------|
| `Proposed` | Under review — not yet binding |
| `Accepted` | Binding — all implementation must comply |
| `Superseded` | Replaced by a newer ADR — preserved for history |
| `Deprecated` | No longer applicable — reason documented in the ADR |
