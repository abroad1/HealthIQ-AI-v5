# ARCH-CONV-A — Legacy Retirement Policy

**Work ID:** `ARCH-CONV-A-STAGE0`
**Date (UTC):** 2026-07-27
**Purpose:** Define the evidence required before any legacy WHY source moves through retirement states. Design only — no legacy asset is disabled, deregistered, deleted, or archived by this document.
**Runtime change:** NONE

---

## 1. Retirement state model

Package A distinguishes five distinct states, not a single "retired" binary:

```text
legacy authority retirement   — the source stops being selected by resolve_frame_why_authority (register flips to compiled mode)
runtime disconnection         — the loader for the source is deregistered (no code path reads it, even if selection logic changed)
physical deletion             — the file is removed from the working tree
archival retention            — the file is moved to an archive location, out of the active runtime tree but retrievable
historic compatibility        — the file remains loadable specifically to service historic replay of pre-migration analyses, under an explicit bounded reader
```

A legacy source only ever needs to pass through the states relevant to its disposition — most Package A targets need only "legacy authority retirement"; full "physical deletion" is a Package-B-adjacent decision reserved until no target (including future waves) depends on the shared file.

## 2. Required evidence per state transition

| Transition | Required evidence before it may occur |
|---|---|
| → legacy authority retirement | Wave's STOP B (medical ratification) and STOP C (first-wave runtime proof, or equivalent per-wave proof for subsequent waves) both closed; precedence test proves compiled wins; register row flipped. |
| → runtime disconnection | All registry targets referencing the file are in "legacy authority retirement" state; reachability proof shows zero remaining callers; STOP D closed for this file. |
| → physical deletion | Runtime disconnection complete; rollback artefact captured (last-known-good copy in Git history is sufficient — no separate backup required); no test harness depends on the file (including opt-in/env-gated test paths, cf. `ARCH-CONV_legacy_dependency_register.md` L-13 pattern); Anthony explicit authorisation (STOP D). |
| → archival retention | Alternative to physical deletion when historic/audit value is judged worth preserving outside the active tree; same preconditions as physical deletion minus the "no further need" requirement. |
| → historic compatibility (bounded reader) | Only for files needed to reproduce **already-persisted** historic analyses; the reader must be isolated (no path from bounded reader back into live analysis) and explicitly documented as historic-only, never as a fallback for new analyses. |

## 3. Non-negotiable constraints (from source task §14)

- **Do not retain reachable legacy fallback "just in case."** A file that could still be silently selected by any live code path is not eligible for any retirement state beyond "active" — this is a Package A/B defect (dual authority), not a retirement candidate.
- **Do not delete a shared legacy asset where unconverted targets still depend on it.** Per `ARCH-CONV_legacy_dependency_register.md` L-02, `hcy_hypotheses_v1.yaml` is shared between a Package-A-migrated frame and the still-legacy elevation-context frame — this file cannot enter "runtime disconnection" or later states until elevation-context's disposition (a Package A/B boundary decision, see `ARCH-CONV-A_stage0_outcome_and_package_boundary.md` §5) is resolved.

## 4. Application to known legacy dependencies

| Dependency (register ID) | Current state | Package A target state | Blocking condition |
|---|---|---|---|
| L-01 legacy root-cause YAML estate | ACTIVE AUTHORITATIVE | legacy authority retirement, per wave | STOP B + STOP C per wave |
| L-02 hcy elevation-context shared file | SHADOW/DUAL-SERVICE | legacy authority retirement blocked pending medical disposition | Package A/B boundary decision (elevation-context frame vs selector) |
| L-03 pilot legacy YAML dual registration | COMPATIBILITY-ONLY | runtime disconnection (deregister loaders) | Long-window exclusivity proof already available for pilot; low remaining risk |
| L-04 `why_engine_fallback_v1` | ACTIVE AUTHORITATIVE fallback | Not a Package A retirement target — owned by Package B (fallback quarantine policy) | N/A — cross-reference only |
| L-13 non-reachable kb47 packages | COMPATIBILITY-ONLY | archival retention or continued exclusion, pending disposition decision | Medical review before any re-inclusion; not a Package A blocker either way |

## 5. Package A retirement scope boundary

Package A owns driving legacy sources into "legacy authority retirement" and, where safe (no shared-file blocker), "runtime disconnection," on a wave-by-wave basis. **Physical deletion and archival retention of any file with cross-wave or cross-package dependency (L-02 class) are explicitly deferred to Package B**, which owns "final physical retirement of shared legacy pathways" per `ARCH-CONV_v5_completion_vs_v6_decision.md` §5. Package A's Phase 5 (`ARCH-CONV-A_compile_and_runtime_integration_design.md`) produces the retirement-readiness evidence; it does not itself authorise physical deletion of shared assets.
