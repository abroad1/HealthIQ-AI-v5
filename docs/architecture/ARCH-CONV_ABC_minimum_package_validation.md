# ARCH-CONV — ABC Minimum Package Validation

**Work ID:** `ARCH-CONV-A-STAGE0`
**Date (UTC):** 2026-07-27
**Purpose:** Concise programme-level confirmation that three outcome-based packages remain the minimum safe structure for the ratified `GO — RETAIN V5 AND COMPLETE BOUNDED CONVERGENCE` decision.
**Runtime change:** NONE

---

## Verdict

```text
THREE PACKAGES CONFIRMED
```

## One-line outcomes

| Package | Outcome | Domain | Rollback boundary | Mandatory STOP owned |
|---|---|---|---|---|
| A — Estate WHY Authority Migration | Every active WHY target has ratified compiled authority + governed selection | Medical content compilation | Per-activation_key register revert | STOP A (identity), STOP B (ratification), STOP C (first-wave proof) |
| B — Dual-Authority and Fallback Retirement | No live medical question answerable by two authorities; no silent fail-open | Precedence/selector logic | Per-family feature flag revert | Elevation-context and any new co-service medical disposition |
| C — Replay, Provenance, Result-Versioning | Every analysis reproducible and classifiable current/stale/incompatible | Data/replay/versioning | Isolated historic-data migration boundary | Silent historic rewrite without audit trail |

## Why not fewer than three

- A and B cannot merge: B's fallback/precedence work must remain live and revertible independent of any single Package A wave's medical review outcome; merging forces global rollback risk onto local content decisions.
- A and C cannot merge: C's rollback boundary (persisted historic data) is a data-migration safety domain distinct from A's content-compilation domain; CLAUDE.md branch/rollback discipline requires this separation.
- B and C cannot merge: B is runtime selector logic with no data-migration component; C is data/versioning with no medical-disposition component. No shared architectural domain.

## Why not more than three

No candidate sub-scope (estate-index refresh, register/gate wiring, docs-only dual registers, single-signal migrations, single validation rules) requires independent medical review, an independent rollback boundary, or an unrelated architectural domain — all are absorbed into A/B/C internal phases per the anti-micro-sprint gate (full package-by-package assessment in `ARCH-CONV-A_stage0_outcome_and_package_boundary.md` §2).

## Sequencing dependency

```text
A produces compiled artefacts + manifest fields
  → B consumes them to make authority exclusive and retire shared fallbacks
    → C consumes A's manifest + B's final exclusivity to version/classify results
```

A is the only package that can begin Stage 0 design and (post-ratification) formal SOP authoring immediately; B and C wait on wave-level outputs from A per family, not on A's full completion — internal phase design in `ARCH-CONV-A_compile_and_runtime_integration_design.md` addresses this handoff explicitly.

## Evidence gaps

1. Exact target/frame count pending `ARCH-CONV-A_active_why_target_inventory.md` verification (do not treat "~36/41" as final — see that document for the authoritative count).
2. Production traffic share per signal family remains unmeasured (static reachability only) — does not block package-structure validation, does affect wave *ordering* inside Package A only.
