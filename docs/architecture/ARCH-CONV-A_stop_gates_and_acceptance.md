# ARCH-CONV-A — STOP Gates and Acceptance Criteria

**Work ID:** `ARCH-CONV-A-STAGE0`
**Date (UTC):** 2026-07-27
**Purpose:** Define Package A's human STOP gates and measurable success criteria. Design only.
**Runtime change:** NONE

---

## 1. STOP gates

Four gates, matching Phase 1/2/4/5 boundaries in `ARCH-CONV-A_compile_and_runtime_integration_design.md`. Assessed as sufficient — not combined further — because each protects a distinct failure mode (identity ambiguity, unratified medical content, unproven runtime exclusivity, premature legacy removal) and each requires a different accountable party's sign-off.

### STOP A — Inventory and identity closure

**Gate:** No target — of the 41 verified registry targets, including all 36 remaining outside the pilot — may enter Phase 2 (medical review) or Phase 3 (compilation) until STOP A has approved that target's row in the **complete target-to-frame map**. Frame count for the 36 remaining targets is **UNKNOWN UNTIL PHASE 1 IDENTITY AND SOURCE CLOSURE**; a one-target/one-frame assumption is provisional inventory planning only (`ARCH-CONV-A_medical_review_wave_plan.md` §1.1) and is not a substitute for this gate. This is an estate-wide gate, not a per-wave one — a wave may not begin Phase 2 for any of its targets while that target's frame count remains undeclared.

Anthony/GPT confirm:
- exact active WHY target count (from `ARCH-CONV-A_active_why_target_inventory.md`, not the carried-forward "~36/41" estimate);
- **complete target-to-frame mapping for all 41 targets** — an explicit frame count per target (1 or N, with N frames named where N>1), not inferred or assumed, including every one of the 36 remaining targets, three of which already have proven multi-frame precedent in the pilot cohort (`ARCH-CONV-A_identity_and_source_readiness.md` D-1);
- canonical source mapping (investigation_spec per target, or explicit A4 flag);
- unresolved identity collisions (duplicate `signal_id` without disambiguating frame identity, missing `activation_key`, load-order-dependent selection);
- wave allocation (per `ARCH-CONV-A_medical_review_wave_plan.md`).

**Sign-off:** Anthony ratification of the closed identity map, including the complete target-to-frame map. No target's Gate 1 medical review or compilation may begin ahead of this ratification for that target.

### STOP B — Medical ratification by wave

**Gate:** No reviewed frame may be promoted (Phase 3 compile) without an explicit medical decision and Anthony ratification.

Recorded per frame: approve / reject / narrow / defer, with the Gate 1 (GPT structured review) and Gate 2 (Anthony ratification) evidence references populated in the register row per `ARCH-CONV-A_compile_and_runtime_integration_design.md` §1.3. No frame is promoted merely because equivalent legacy content already exists (source task constraint, §7).

**Sign-off:** Anthony, per wave, before that wave enters Phase 3.

### STOP C — First-wave runtime proof

**Gate:** Before estate-wide integration proceeds beyond the first wave, the representative wave must prove:
- compiled WHY is canonical for its activation_keys;
- legacy cannot win (precedence test);
- rejected frames are runtime-inert;
- runtime fails closed (no silent restore of unreviewed content);
- consumer and clinician outputs remain aligned;
- provenance is emitted for the compiled WHY.

This mirrors the proof already demonstrated for the pilot cohort under CORRECT-1 (`ARCH-CONV_programme_closure_record.md` §3) — STOP C requires the same evidence class repeated on the first *new* wave before Phase 4 is trusted to repeat unattended across subsequent waves.

**Sign-off:** Claude audit + GPT review + Anthony ratification (HIGH-risk dual approval).

### STOP D — Legacy retirement authority

**Gate:** No legacy source may be deleted until:
- all callers are mapped;
- replacement is active;
- replay is equivalent, or intentionally changed with recorded disposition;
- rollback artefacts exist;
- runtime unreachability is proven.

Full evidence requirements per legacy-source type in `ARCH-CONV-A_legacy_retirement_policy.md`.

**Sign-off:** Anthony, per legacy source (not per wave — a shared legacy file's retirement gate fires only once all dependent waves have completed Phase 4).

### 1.1 Sufficiency assessment

Four gates are sufficient. They are not combined because each maps to a different failure class and a different point of no return: STOP A prevents compiling ambiguous identity (a compile-time mistake that would be expensive to unwind after Gate 1/2 review has already spent effort on the wrong frame boundary); STOP B prevents unratified medical content going live; STOP C prevents an unproven runtime mechanism being trusted at scale; STOP D prevents irreversible deletion. Merging any two would mean asking Anthony to ratify two different kinds of risk (e.g. identity correctness and medical content) in one sign-off, which weakens the specific accountability the source task requires.

---

## 2. Package A success criteria

```text
100% of active WHY targets inventoried
100% of active targets have explicit frame identity
100% have canonical-source disposition
100% of promoted frames medically reviewed and ratified
100% of promoted WHY artefacts deterministically compiled
no promoted target depends on legacy WHY authority
no rejected frame remains runtime-reachable
no signal-only lookup can select an ambiguous frame
all wave replay suites pass
consumer/clinician alignment passes
provenance is emitted for compiled WHY
legacy sources retired or explicitly bounded pending Package B
no Layer C medical inference introduced
```

## 3. Declaration outcomes

- **PASS** — all success criteria hold for every wave; no open STOP gate; Package A closure record authored and ratified (Phase 6).
- **CORRECT** — success criteria hold after a bounded, single authorised correction package addressing a specific defect found post-integration (mirroring the CORRECT-1 precedent) — this is a recoverable state, not a restart.
- **STOP** — a wave cannot close its STOP gate (e.g. STOP C fails: legacy still wins on a proven precedence test, or a rejected frame is found runtime-reachable). A STOP on one wave does not fail the whole package; it holds that wave and any waves sharing its legacy file, per `ARCH-CONV-A_compile_and_runtime_integration_design.md` Phase 5 dependency rule.

Package A as a whole is declared PASS only when every wave individually reaches PASS or CORRECT, and Phase 6 estate regression/replay/closure succeeds.
