# ARCH-CONV-A — Identity and Source Readiness

**Work ID:** `ARCH-CONV-A-STAGE0`
**Date (UTC):** 2026-07-27
**Purpose:** Audit Package A targets for identity defects against the accepted model (`signal_id` = family identity, `activation_key` = runtime activation identity, investigation/frame identity = medical interpretation identity) and state each defect's required resolution point. Design only.
**Runtime change:** NONE
**Source evidence:** `ARCH-CONV-A_active_why_target_inventory.md` (verified repository inventory, 41/41 registry targets)

---

## 1. Identity model recap

```text
signal_id        = signal-family identity          (ROOT_CAUSE_TARGET_SPECS key)
activation_key    = runtime activation identity      (signal_id::source_spec_id, authority-register key)
investigation/frame identity = medical interpretation identity (per compiled artefact / investigation_spec)
```

Package A must not compile ambiguous frame identity into the estate. Every defect below is classified against exactly one resolution point: **before medical review**, **during compilation**, **during runtime integration**, or **Package B**.

---

## 2. Defect register

### D-1 — Registry schema cannot express frame plurality (estate-wide, structural)

**Evidence:** `RootCauseTargetSpec` (`backend/core/knowledge/root_cause_registry_v1.py:19-24`) has no `activation_key` field; all 41/41 entries lack it structurally (inventory §6). Three signal_ids already resolve to multiple runtime frames invisibly at the registry layer: `signal_homocysteine_high` (3 frames), `signal_mcv_high` (3 frames), `signal_tpo_ab_high` (2 frames) (inventory §5).

**Resolution point: BEFORE MEDICAL REVIEW.** Every non-pilot target entering Phase 1 (identity closure) must be explicitly assessed for expected frame count before its investigation spec is scoped for Gate 1 review — a target scoped as "1 frame" that turns out to need 2+ frames mid-review would force re-scoping after review effort is spent. This is not a schema rewrite requirement (the runtime already handles plurality correctly via the authority register and a guarded fail-closed fallback, inventory §5 and §8.1) — it is a Phase 1 process requirement: declare expected frame count per target before compiling.

**Recommended disposition:** Phase 1 identity closure produces an explicit "frame count declaration" per target (1 or N, with N frames named) as a required field in the wave plan, sourced from the investigation_spec content, not inferred later.

### D-2 — Shared legacy file serving two identities (shadow dual)

**Evidence:** `hcy_hypotheses_v1.yaml` backs both `signal_homocysteine_elevation_context` (fully legacy, no spec found — A6) and `signal_homocysteine_high` (2 of 3 frames compiled — A1) (inventory §7). This is the only shared-file case among all 40 legacy files (verified by regex scan, inventory §7).

**Resolution point: BEFORE MEDICAL REVIEW for the disposition decision; PACKAGE B for the selector/precedence mechanics if the disposition is "coexist under a selector" rather than "compile a distinct elevation-context frame."** Per `ARCH-CONV-A_stage0_outcome_and_package_boundary.md` §5, the medical disposition (does elevation-context deserve its own compiled frame, or does it get folded into/suppressed by the existing homocysteine_high frames) is a Package A Gate 1/Gate 2 decision; the selector implementation if coexistence is chosen is Package B's. This is Wave 0 in `ARCH-CONV-A_medical_review_wave_plan.md` precisely because it blocks L-02 shared-file retirement (`ARCH-CONV-A_legacy_retirement_policy.md` §4) for both targets.

### D-3 — Bilirubin identity duplication

**Evidence:** `signal_bilirubin_high` (#29) and `signal_hyperbilirubinemia` (#30) are plausibly the same clinical concept registered as two separate `signal_id`s, each with its own legacy YAML file and no investigation spec for either (inventory §5, final paragraph).

**Resolution point: BEFORE MEDICAL REVIEW.** This must be resolved as an identity question — either they are genuinely distinct signal definitions (different thresholds/marker basis) and should proceed as two separate Package A targets, or one is a legacy duplicate that should be retired/merged before any compile effort is spent on either. Compiling two artefacts for what is medically one frame would itself create a new estate-internal dual authority. This is a Phase 1 (identity closure, STOP A) item, not a Phase 2 medical-content question — it must be settled by comparing the two signal_library definitions, not by investigation-spec research.

### D-4 — Ambiguous / unconfirmed spec-to-target matches (A4, 8 targets)

**Evidence:** `signal_hepatic_alt_context`, `signal_thyroid_tsh_context`, `signal_systemic_inflammation`, `signal_lipid_transport_dysfunction`, `signal_iron_overload_context`, `signal_oxygen_transport_capacity`, `signal_ferritin_low`, `signal_hepatic_metabolic_stress` — each has a candidate investigation_spec but the direction, granularity, or composite-vs-single-marker framing does not confirm a 1:1 match (inventory §3, §4).

**Resolution point: BEFORE MEDICAL REVIEW (spec confirmation), then normal Phase 2 review.** Each must have its candidate spec explicitly confirmed or rejected as the canonical source during Phase 1 identity closure — an A4 target must not enter Gate 1 review carrying an unconfirmed spec match, since Gate 1 review of the wrong spec wastes reviewer effort and risks compiling content that doesn't match the actual signal_id's evaluation logic. Where no spec is confirmable, the target is reclassified A5 (no spec) and routed to fresh canonical research scoping rather than Gate 1 review of a mismatched candidate.

### D-5 — No spec found (A5, 11 targets)

**Evidence:** `signal_insulin_resistance`, `signal_apoa1_cardio_risk`, `signal_total_cholesterol_high`, `signal_iron_deficiency_context`, `signal_transferrin_high`, `signal_transferrin_low`, `signal_alp_low`, `signal_bilirubin_high`, `signal_hyperbilirubinemia`, `signal_hypercortisolism`, `signal_tgab_high` (inventory §9, corrected tally).

**Resolution point: BEFORE MEDICAL REVIEW.** No compile or Gate 1 review can begin until a canonical investigation_spec is authored (Knowledge Bus research intake, outside Package A's own scope but a precondition for Package A's Phase 2 on these targets — see `ARCH-CONV-A_medical_review_wave_plan.md` §Medical Evidence Gaps).

### D-6 — Legacy filenames used as de facto identity

**Evidence:** `asset_filename` on `RootCauseTargetSpec` is a legacy YAML filename, not a governed identifier; the loader indirection (`root_cause_registry_v1.py`) means the filename *is* the only static pointer to "which content answers this signal's WHY" for all 36 non-pilot targets (inventory §2, item 1).

**Resolution point: DURING COMPILATION.** Once a target is compiled, `source_spec_id` (from the investigation_spec) becomes its authoritative identity per the manifest fields in `ARCH-CONV-A_compile_and_runtime_integration_design.md` §1.3; the legacy filename stops being an identity carrier for that target the moment its register row exists. No registry schema change is required before compilation begins — this is resolved as a side effect of the normal compile step, not a separate identity-closure task.

### D-7 — Load-order / lexicographic frame selection risk

**Evidence:** the only guarded fallback that could exhibit order sensitivity is the bare-`signal_id` lookup in `resolve_frame_why_authority` (`why_authority_v1.py:110-123`), which fails closed (not silently order-dependent) when more than one `COMPILED_ACTIVE` frame matches with no activation_key on the row (inventory §8.1). No unguarded order-dependent selection was found for any of the 41 targets.

**Resolution point: DURING RUNTIME INTEGRATION.** Each wave's Phase 4 (`ARCH-CONV-A_compile_and_runtime_integration_design.md`) must include a positive test that the fail-closed guard fires correctly for any target expected to grow multiple frames (D-1) — this is a per-wave runtime-integration test, not a pre-review identity-closure blocker, because the guard already exists and behaves safely; the test merely proves it continues to for new targets.

### D-8 — Registry validation only guards `signal_id`, not `activation_key`, uniqueness

**Evidence:** `validate_root_cause_registry` (`root_cause_registry_v1.py:97-123`) raises on duplicate `signal_id` only; it has no visibility into `activation_key` collisions because the field doesn't exist on the dataclass (D-1).

**Resolution point: DURING COMPILATION.** `compiled_why_authority_register_v1.yaml`'s own load path (`why_authority_v1.py:41-65`) is the actual activation_key-uniqueness enforcement point today and already works correctly for the 10 pilot rows — Package A relies on this existing enforcement continuing to apply as new rows are added, wave by wave. No new validator is required; this is confirmed adequate, not a gap.

### D-9 — Stale governance register contradicts current pilot state

**Evidence:** `knowledge_bus/governance/root_cause_authority_register_v1.yaml` (dated 2026-06-14) still lists `signal_free_t3_low` as `ROOT_CAUSE_REQUIRES_FUTURE_MAPPING` and cites a non-existent filename for the vitamin-D artefact (inventory §2, item 3).

**Resolution point: BEFORE MEDICAL REVIEW (Phase 0).** This file must not be consulted as authority for any Package A wave scoping decision; Phase 0 (estate/index reconciliation, `ARCH-CONV-A_compile_and_runtime_integration_design.md`) must either refresh it to match `compiled_why_authority_register_v1.yaml` or explicitly deprecate it in favour of the single authority register, to prevent a future wave's Gate 1 reviewer from being misled by contradictory register state.

---

## 3. Summary — resolution point distribution

| Resolution point | Defects |
|---|---|
| Before medical review | D-1 (frame-count declaration), D-2 (disposition decision only), D-3, D-4, D-5, D-9 |
| During compilation | D-6, D-8 |
| During runtime integration | D-7 |
| Package B | D-2 (selector mechanics only, if coexistence chosen) |

**No target may enter Gate 1 medical review (Phase 2) while carrying an unresolved before-medical-review defect.** This is enforced structurally by STOP A (`ARCH-CONV-A_stop_gates_and_acceptance.md`), which requires the closed identity map — including frame-count declarations, confirmed spec matches, and the bilirubin/elevation-context dispositions — before any wave proceeds past Phase 1.
