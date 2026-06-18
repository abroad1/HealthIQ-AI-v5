# EIGHT-BLOCK-PROGRAMME-1 — Eight-Block Comparison and Programme Recommendation

---
work_id: EIGHT-BLOCK-PROGRAMME-1
branch: work/EIGHT-BLOCK-PROGRAMME-1-comparison-and-roadmap
status: MERGED_CLOSURE_COMPLETE
change_type: CONTENT
head_sha: (published HEAD)
merged_to_main: db1beb7
---

## Executive verdict

Documentation-only sprint producing the **canonical Cursor/Claude eight-block comparison and multi-sprint beta-readiness programme recommendation**. No runtime code, tests, or frontend/backend behaviour changed.

**GPT architectural decision:** ACCEPTED — programme paper is canonical for roadmap planning; `ADR-LAYER-BOUNDARY-RECONCILIATION-1` ratified alongside this paper; pending-ratification wording in ADR is non-blocking.

---

## Deliverable

| File | Purpose |
|------|---------|
| `docs/strategy/eight_block_beta_readiness/EIGHT_BLOCK_BETA_READINESS_COMPARISON_AND_PROGRAMME_RECOMMENDATION_2026-06-18.md` | Canonical comparison + ~16-sprint programme |

---

## Acceptance criteria

| # | Criterion | Result |
|---|-----------|--------|
| 1 | Uses ADR-LAYER-BOUNDARY-RECONCILIATION-1 | Pass |
| 2 | Compares Cursor and Claude audits | Pass |
| 3 | Incorporates late documents + R2 UAT | Pass |
| 4 | Identifies stale findings (6 HIGH UAT, ADR pending) | Pass |
| 5 | Sequenced dependency-aware programme | Pass |
| 6 | First three sprints clear | Pass |
| 7 | No Layer B work assigned to Layer C/Gemini/frontend | Pass |
| 8 | Reuses existing assets | Pass |
| 9 | CEO-level roadmap utility | Pass |
| 10 | No code changed | Pass |

---

## Post-Implementation Closure (published)

| Check | Result | Evidence |
|-------|--------|----------|
| Merge authorised | Yes | GPT + human approval |
| Sprint branch | `work/EIGHT-BLOCK-PROGRAMME-1-comparison-and-roadmap` | Fast-forward merge |
| `main` HEAD | (see publish step) | `git rev-parse main` |
| `origin/main` HEAD | (see publish step) | aligned |
| Code files in merge | **None** | Docs + bus artefacts only |
| Working tree | Clean | `git status --short` |
| Stash | Empty | `git stash list` |
| Kernel status | COMPLETE | `automation_bus/latest_cursor_status.json` |

**Next:** Do not author Phase 1 implementation prompts until programme paper is on `main` (now satisfied).
