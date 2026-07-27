# ARCH-CONV-A — Stage 0 Outcome and Package Boundary

**Work ID:** `ARCH-CONV-A-STAGE0`
**Date (UTC):** 2026-07-27
**Programme decision (input, ratified):** `GO — RETAIN V5 AND COMPLETE BOUNDED CONVERGENCE`
**Stage:** Stage 0 — package design only. No implementation, no runtime change, no Automation Bus sprint prompt.
**Runtime change:** NONE
**Inputs consumed:** `ARCH-CONV_active_authority_map.md`, `ARCH-CONV_day_one_layer_completion_assessment.md`, `ARCH-CONV_dual_authority_findings.md`, `ARCH-CONV_legacy_dependency_register.md`, `ARCH-CONV_programme_closure_record.md`, `ARCH-CONV_residual_runtime_inventory.md`, `ARCH-CONV_v5_completion_vs_v6_decision.md` (the "six estate-audit artefacts" + ADR-equivalent decision pack).

---

## 1. Stage 0 outcome statement

The completion programme (Packages A, B, C) is not complete, and this Stage 0 package design is not itself a completion event, until all seven outcomes below hold across the active v5 estate:

```text
1. Every active medical WHY output is sourced from reviewed canonical research,
   compiled into governed runtime artefacts and resolved through explicit frame identity.

2. No live medical question can be answered by competing legacy and compiled authorities.

3. No fail-open fallback can silently restore retired or unreviewed medical content.

4. Every analysis can be reproduced against a complete authority, compiler,
   runtime and result-version manifest.

5. Analyses can be classified as current, stale or incompatible when medical
   authority or runtime behaviour changes.

6. Legacy runtime assets are either:
   - retired and removed;
   - isolated as bounded historic compatibility readers;
   - or proven runtime-unreachable.

7. Layer C remains render/translation only.
```

**Explicit statement:** the programme is INCOMPLETE today. Per `ARCH-CONV_active_authority_map.md` §4–5 and `ARCH-CONV_day_one_layer_completion_assessment.md`, outcome 1 holds only for the 5-signal/10-frame pilot cohort (9 `COMPILED_ACTIVE` + 1 `REJECTED`); outcome 2 fails at DUAL-01 and DUAL-05 (`ARCH-CONV_dual_authority_findings.md` §3); outcome 3 fails at L-04 (`why_engine_fallback_v1`, unconstrained fallback, `ARCH-CONV_legacy_dependency_register.md` L-04); outcome 4 and 5 are `PARTIAL` per the layer assessment's Replay/provenance section; outcome 6 is not yet true for L-01 (the ~36-target legacy YAML estate); outcome 7 is `SUBSTANTIALLY COMPLETE` (CORRECT-1 closed the audited `BOUNDARY_LEAK` inventory) but not formally re-proven at estate scale under Package A/B integration. This Stage 0 package design exists to make outcome 1 and outcome 6 achievable for the full estate; it does not itself satisfy them.

---

## 2. Minimum safe package count — validation

### 2.1 Method

Each of Packages A, B, C from `ARCH-CONV_v5_completion_vs_v6_decision.md` §5 is tested against the anti-micro-sprint gate: a package must not exist solely for governance, policy, configuration, documentation, inventory, compiler plumbing without a product outcome, one signal/frame, one validation rule, or one registry adjustment — unless runtime safety requires isolation, medical review cannot be resolved inside the package, unrelated architectural domains are involved, a mandatory STOP gate requires Anthony's approval before proceeding, or rollback/data-migration safety requires a separate release boundary.

### 2.2 Package A — Estate-wide WHY Authority Migration

| Field | Assessment |
|---|---|
| product outcome | Every production-reachable WHY target answers from a compiled, medically-ratified, activation_key-addressed artefact, or is an explicit fail-closed skip; legacy YAML is not selected for any migrated target. |
| why it cannot be absorbed elsewhere | It is the only package that touches canonical research review, compilation, and frame-identity closure. B and C both depend on A's compiled artefacts existing before they can eliminate dual authority (B) or version results against a stable authority manifest (C). Absorbing A into B would force fallback/dual-authority work to start before the compiled replacement it is retiring exists — sequencing failure, not scope failure. |
| why it is not a micro-sprint | It resolves ~36 of ~41 registry targets (exact count pending inventory verification, task 1), each requiring independent medical evidence review — this is bounded, outcome-based, estate-scale work, not one signal, one rule, or plumbing. |
| major implementation boundary | `knowledge_bus/research/investigation_specs/` → Knowledge Bus Pass 3 compiler → `knowledge_bus/compiled/hypotheses/` → `compiled_why_authority_register_v1.yaml` → `why_authority_v1.resolve_frame_why_authority` → `root_cause_compiler_v1`. |
| medical-review boundary | Gate 1 (structured GPT medical review) + Gate 2 (Anthony ratification) per wave, per `ARCH-CONV_v5_completion_vs_v6_decision.md` §4 and the previously adopted dual-gate model (see §7 of the source task and `ARCH-CONV-A_medical_review_wave_plan.md`). |
| rollback boundary | Per-wave: a wave's compiled artefacts can be reverted to `legacy` mode in the authority register without touching other waves' targets (register is per-activation_key, not global). |
| dependencies on other packages | None inbound. B depends on A's compiled artefacts to have a non-legacy authority to make exclusive. C depends on A's compile/manifest fields (`source_spec_id`, compiler version, content hash) to build provenance and versioning. |

### 2.3 Package B — Dual-Authority and Fallback Retirement

| Field | Assessment |
|---|---|
| product outcome | No unresolved dual authority answers the same medical question on a live path; no fail-open fallback silently restores retired/unreviewed content. |
| why it cannot be absorbed elsewhere | Dual-authority closure (DUAL-01, DUAL-05) and fallback quarantine (L-04) are cross-cutting concerns that span multiple Package A waves — they cannot be closed inside any single wave because e.g. DUAL-01 (homocysteine elevation-context) spans both a Package A migration target and a currently-unmigrated shared legacy file (`hcy_hypotheses_v1.yaml`, `ARCH-CONV_legacy_dependency_register.md` L-02). It also owns final physical retirement of *shared* legacy pathways, which is unsafe to do target-by-target while other Package A waves still depend on the same shared file. |
| why it is not a micro-sprint | Estate-wide fallback and precedence closure affects every WHY target, not one rule; it requires new selector-policy design work and cross-family medical disposition (elevation-context vs frame-specific WHY), not a config edit. |
| major implementation boundary | Cross-producer precedence selector (root_cause / IDL / `_why_template`), fallback quarantine policy in `root_cause_compiler_v1._compile_why_engine_fallback_finding`, family-aggregation policy for `signal_id`-grain joins (phenotype/interaction maps). |
| medical-review boundary | Elevation-context disposition and any new co-service family generalisation require Gate 1 + Gate 2; pure selector-mechanics changes (which authority wins when both fire) do not require new medical review once each side is already ratified. |
| rollback boundary | Selector logic can be feature-flagged per family; fallback quarantine can be reverted to prior fail-open behaviour without touching Package A compiled artefacts. |
| dependencies on other packages | Depends on Package A having produced compiled artefacts for the families in dual (cannot make hcy exclusive until hcy elevation-context has a compiled disposition — a Package A wave decision feeds Package B). Package C's stale/incompatible classification depends on Package B's exclusivity being final (a result cannot be marked "current" if its authority could still silently flip between compiled/legacy). |

### 2.4 Package C — Replay, Provenance and Result-Versioning Completion

| Field | Assessment |
|---|---|
| product outcome | Every analysis is reproducible against a complete authority/compiler/runtime/result-version manifest, and can be classified current/stale/incompatible when authority or runtime behaviour changes. |
| why it cannot be absorbed elsewhere | It is a distinct architectural domain (data/replay/versioning) from medical-content compilation (A) and selector/precedence logic (B). It also carries a **rollback/data-migration safety boundary**: historic waist-unit rows (L-11, 48 legacy bare rows, 12 used-incorrectly per `WAIST_UNIT_LEGACY_IMPACT_AUDIT.md`) require a release boundary distinct from any content-migration wave, because remediation touches persisted historic data, not runtime authority. |
| why it is not a micro-sprint | It spans a versioning policy, an emitter/test fix, and a historic-data disposition decision across the full analysis history table — not one registry adjustment. |
| major implementation boundary | Result-versioning policy (`LAUNCH-CORE-3`), output-authority provenance builder, replay manifest emission, regenerate route. |
| medical-review boundary | None required for versioning/provenance mechanics; medical review only if historic remap changes clinical inputs (waist unit correction is data-integrity, not new medical interpretation). |
| rollback boundary | Versioning policy changes are additive (new stale/current/incompatible classification) and do not require rollback of Package A/B artefacts; historic data remediation requires its own audit-trailed migration boundary, separate from any Package A/B release. |
| dependencies on other packages | Depends on Package A emitting the manifest fields (`source_spec_id`, compiler version, content hash, authority version) it needs to version against, and on Package B's exclusivity being final before "current" can be a stable classification. |

### 2.5 Anti-micro-sprint items explicitly absorbed (not standalone)

Per `ARCH-CONV_v5_completion_vs_v6_decision.md` §5: estate-index refresh, register/gate wiring updates, and docs-only dual registers are absorbed into Packages A/B/C internal phases — they do not justify separate packages because none require independent medical review, independent rollback boundary, or an unrelated architectural domain.

### 2.6 Verdict

```text
THREE PACKAGES CONFIRMED
```

No revision required. Each package has a distinct architectural domain (content compilation vs. precedence/fallback vs. data/replay), a distinct rollback boundary, and at least one STOP gate requiring Anthony's approval that cannot be satisfied inside another package's internal phases. Package count is not being inflated by treating any single signal, frame, or validation rule as its own package (see §2.5).

---

## 3. Package A product outcome (framing)

Package A is designed around a single outcome, not a file-migration count:

> Every currently active production WHY target has an explicit frame identity, a reviewed canonical medical authority, a deterministic compiled artefact and a governed runtime selection path.

It is explicitly **not** framed as "migrate approximately 36 YAML files" — the unit of work is the activation_key/frame, not the file, because (per `ARCH-CONV_active_authority_map.md` §2.4 and `ARCH-CONV_legacy_dependency_register.md` L-02) at least one legacy file (`hcy_hypotheses_v1.yaml`) is shared across multiple frames with different medical disposition, and file count does not equal target count. The exact authoritative target count is established in `ARCH-CONV-A_active_why_target_inventory.md` (pending verification against repository reality, not the carried-forward "~36/41" estimate).

---

## 4. Package A risk and change classification

| Field | Value | Basis |
|---|---|---|
| `risk_level` | **HIGH** | Confirmed. Touches `backend/core/knowledge/` root-cause registry/compiler and Knowledge Bus compiled artefacts — Intelligence Core per CLAUDE.md §Intelligence Core & Risk definition; also changes emitted medical WHY content estate-wide. |
| `change_type` | **MIXED** | Confirmed. Compiler/runtime-loader/registry code changes (BEHAVIOUR) plus new compiled medical content per wave (CONTENT) — MIXED always uses BEHAVIOUR controls. |
| `execution_model` | **TWO_PHASE_START_FINISH** | Confirmed. Estate-scale, multi-wave, requires Stage 3 start / Stage 5 finish discipline per wave rather than a single-phase execution. |
| Stage B mode | **Mode 2 (B2)** | Confirmed. This is a strategic/programmatic decision (estate-wide authority migration sequencing, medical-review capacity allocation, wave ordering) explicitly authorised at the ADR/decision-pack level (`ARCH-CONV_v5_completion_vs_v6_decision.md`), not a per-sprint file/schema/loader question resolvable inside Stage D hardening. |

Intelligence Core touchpoints: `root_cause_registry_v1.py`, `root_cause_compiler_v1.py`, `why_authority_v1.py`, `compiled_why_authority_register_v1.yaml`, Knowledge Bus compiler/promotion path. Emitted-behaviour changes: WHY content per migrated target changes from legacy wording to compiled wording — user-visible. Medical-content changes: yes, per wave, Gate 1/Gate 2 reviewed. Compiler changes: extends existing Pass-3-style compiler to remaining targets; no new compiler architecture. Runtime-loader changes: authority register grows per wave; no new loader architecture. Deletion/migration risk: legacy YAML retirement is deferred to post-exclusivity-proof (see `ARCH-CONV-A_legacy_retirement_policy.md`) — not deletion risk inside Package A itself. Required independent audit mode: Claude audit + GPT architectural review + dual approval (HIGH risk per SOP §10).

---

## 5. Package B and C boundary (what Package A does not own)

Package A owns: canonical WHY authority, frame identity closure, medical review, compiled WHY artefacts, runtime WHY selection, wave-level legacy replacement, local (per-wave) reachability proof.

Package A explicitly defers to Package B: estate-wide dual-authority elimination across families that span multiple Package A waves (DUAL-01, DUAL-05), fallback retirement (L-04), cross-producer precedence, family-aggregation policy closure, final physical retirement of *shared* legacy pathways.

Package A explicitly defers to Package C: full replay manifest completion, result-version policy advancement, stale/incompatible classification, historic waist-unit disposition, provenance key correctness (L-12) beyond what Package A's own compiled-artefact manifest fields supply.

**Boundary that cannot be safely separated:** the *decision* of whether a specific wave's dual authority (e.g. elevation-context) is resolved by compiling a distinct artefact (Package A act) or by a selector/precedence rule that suppresses one existing source (Package B act) must be made per-family inside Package A's medical-review wave, because it is a medical disposition question, not a mechanics question — but the selector *implementation* remains Package B's. This is recorded as a required Package A→B handoff artefact per wave (see `ARCH-CONV-A_medical_review_wave_plan.md` and `ARCH-CONV-A_stop_gates_and_acceptance.md` STOP B).
