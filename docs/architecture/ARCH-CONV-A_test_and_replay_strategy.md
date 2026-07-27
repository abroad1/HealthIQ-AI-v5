# ARCH-CONV-A — Test and Replay Strategy

**Work ID:** `ARCH-CONV-A-STAGE0`
**Date (UTC):** 2026-07-27
**Purpose:** Define Package A's verification strategy. Design only — no tests are written by this document.
**Runtime change:** NONE

---

## 1. Required test classes (estate-wide, not per-wave)

```text
compiler schema and determinism tests        — same artefact schema in → same compiled output out, every run
manifest completeness tests                   — every required field in §1.3 of the integration design present and non-null
activation_key and frame-identity tests       — no target resolvable by signal_id alone where >1 frame exists
legacy-vs-compiled precedence tests           — compiled always wins for COMPILED_ACTIVE keys; legacy never re-selected
rejected-frame inactivation tests             — REJECTED/DEFERRED frames do not fire, rank, or emit WHY
fail-closed tests                             — missing/malformed compiled artefact produces honest omission, not silent legacy fallback or invented content
consumer/clinician alignment tests            — consumer narrative and clinician report agree on which authority answered a given WHY
intervention-reference tests                  — compiled WHY's intervention citations resolve against the intervention library
provenance tests                              — compiled WHY emits real activation_key-based provenance (closes L-12 pattern for new waves)
representative panel replay                   — see §2
historical analysis replay where inputs are available — regenerate route re-run against pre-migration stored inputs, compare WHY output pre/post wave
Layer C non-inference regressions             — extend CORRECT-1 BOUNDARY_LEAK suite to any new consumer/clinician surface touched by a wave
existing Package 1–3 and CORRECT-1 protections — must remain green; Package A must not regress the proven pilot cohort
```

These reuse the existing test patterns already proven for the pilot cohort (`validate_compiled_why_authority_gate.py`, PKG3/CORRECT-1 suites, MCV inventory-coexistence test) rather than inventing a new test architecture — Package A is extension of a proven pattern, not new test infrastructure.

## 2. Per-wave panel requirements

For every migration wave (`ARCH-CONV-A_medical_review_wave_plan.md`), define:

- **positive panel** — biomarker/context inputs that should fire the frame and produce the ratified compiled WHY.
- **negative/gate-unmet panel** — inputs that fire the underlying signal but do not meet the frame's evidence gate; compiled WHY must not appear.
- **ambiguous panel** — inputs where more than one frame in the wave's family could plausibly apply; must resolve to exactly one frame or to the governed co-service policy (mirroring the MCV precedent, `ARCH-CONV_dual_authority_findings.md` DUAL-03).
- **missing-data panel** — required biomarker/context absent; must fail closed, not fall back to legacy or invent.
- **contradictory-evidence panel** (where clinically relevant) — conflicting biomarker signals within the same family; resolution must follow the wave's medical-review decision on contradiction handling (per CLAUDE.md §12: "contradiction resolution must prefer the strongest clinically grounded anchor, not merely the nearest alternative").

## 3. Sufficiency of current phenotype/test estate

**Assessment:** the current estate (CORRECT-1, PKG1–3 protections, MCV co-service tests, output-authority provenance regression) is sufficient as a *pattern* but not sufficient in *coverage* — it exists only for the 5-signal/10-frame pilot. Package A must expand this same pattern to each new wave's families; it is not creating a new pattern. This expansion work is scoped inside Phase 3/Phase 4 of the compile/runtime integration design (`ARCH-CONV-A_compile_and_runtime_integration_design.md`) and is not a separate package, per the anti-micro-sprint gate (test expansion has no independent medical-review or rollback boundary distinct from the wave it belongs to).

## 4. Regression protection

Every wave's test run must include the full existing pilot-cohort suite (CORRECT-1 + PKG1–3) as a non-negotiable regression gate — a wave that passes its own panels but breaks the pilot cohort is a STOP C failure for that wave, not a pass with a known issue.
