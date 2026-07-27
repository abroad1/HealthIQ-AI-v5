# ARCH-CONV-A — Compile and Runtime Integration Design

**Work ID:** `ARCH-CONV-A-STAGE0`
**Date (UTC):** 2026-07-27
**Purpose:** Design the Package A compile/promotion boundary and internal execution phases. Design only — no compiler, loader, or registry code is changed by this document.
**Runtime change:** NONE

---

## 1. Compile and promotion boundary

Accepted chain (unchanged from the proven pilot):

```text
investigation_spec (knowledge_bus/research/investigation_specs/inv_*.yaml)
→ validation (schema + Knowledge Bus validator)
→ deterministic compiler (Pass 3 promotion path)
→ compiled hypothesis / WHY artefact (knowledge_bus/compiled/hypotheses/*.yaml)
→ manifest (compiled_why_authority_register_v1.yaml row)
→ governed runtime loader (why_authority_v1.resolve_frame_why_authority)
→ explicit frame selection (activation_key-addressed)
→ structured Layer B output (compile_root_cause_v1 → root_cause_v1)
```

No new architecture is introduced. Package A extends this proven chain to the remaining active targets; it does not redesign it.

### 1.1 Compiler inputs

- Investigation spec conforming to `knowledge_bus/research/investigation_specs/investigation_spec_schema_v3.0.0.yaml`.
- Medical review decision record (Gate 1 GPT structured review + Gate 2 Anthony ratification — see `ARCH-CONV-A_medical_review_wave_plan.md`).
- Target activation_key (from `root_cause_registry_v1.py` — must pre-exist or be assigned during Phase 1 identity closure, never invented at compile time).

### 1.2 Compiler outputs

- One compiled hypothesis/WHY artefact per ratified frame under `knowledge_bus/compiled/hypotheses/`.
- One authority register row per compiled artefact.

### 1.3 Schema and manifest field requirements (per artefact/register row)

```text
source_spec_id              — exact investigation_spec identifier consumed
activation_key               — must match registry; no bare signal_id fallback
frame identity fields        — direction/context disambiguator where >1 frame per signal family
medical decision status      — COMPILED_ACTIVE | REJECTED | DEFERRED (no other values; see §7 wave plan)
ratification evidence        — reference to Gate 1 + Gate 2 record (date, reviewer, decision)
content hash                 — of the compiled artefact, for provenance/versioning (feeds Package C)
compiler version              — version of the compiler that produced the artefact
authority version             — version of the authority register schema in effect
runtime compatibility version — minimum runtime/loader version required to interpret the artefact
```

These fields are a superset of what the 9 pilot artefacts already carry (verify exact current field set against `knowledge_bus/compiled/hypotheses/*.yaml` during Phase 0 — do not assume the pilot schema already contains all of the above; any gap is a schema-extension item inside Phase 0, not a new package).

### 1.4 Promotion gates

- Knowledge Bus Pass 3 promotion protocol applies unchanged (`docs/governance/KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL_v1.1.md`).
- No artefact may be marked `COMPILED_ACTIVE` in the register without Gate 1 + Gate 2 evidence references populated.
- Runtime must never read raw Pass 3 research directly — the compiled artefact + register row remain the sole runtime-facing authority. Package A artefacts are not permitted to become a second research authority: any wording that would compete with the investigation_spec as a citable source is a defect, not a feature.

### 1.5 Rollback artefacts

- Per-wave: prior register state (all rows outside the wave untouched) plus the ability to flip a wave's rows back to absent/`legacy` mode without code change (register-only revert).
- Legacy YAML remains on disk, unmodified, through Phase 5 (see §9) — it is never deleted before its retirement preconditions are met (`ARCH-CONV-A_legacy_retirement_policy.md`), so rollback of a wave is a register-row removal, not a file restoration.

---

## 2. Internal execution phases

### Phase 0 — Exact estate/index reconciliation

- **Inputs:** `root_cause_registry_v1.py`, `knowledge_bus/root_cause/hypotheses/*.yaml`, `knowledge_bus/compiled/hypotheses/*.yaml`, `compiled_why_authority_register_v1.yaml`, `compiled/estate_index_v1.yaml` (known stale, `ARCH-CONV_residual_runtime_inventory.md` §7.3).
- **Actions:** verify exact registry target count, exact legacy/compiled file counts, refresh the stale estate index, resolve identity defects flagged in `ARCH-CONV-A_active_why_target_inventory.md`.
- **Outputs:** `ARCH-CONV-A_active_why_target_inventory.md` (this Stage 0 package already requires it), refreshed estate index.
- **Implementation authority:** Cursor, under a CONTENT-classified Automation Bus work package (index/inventory refresh only — no medical content change).
- **Validation:** counts cross-checked against three independent sources (registry code, filesystem glob, authority register) must agree or the discrepancy is logged as a named defect.
- **STOP conditions:** any unresolved `signal_id` collision or missing `activation_key` blocks Phase 1 for that target (STOP A).
- **Rollback point:** none needed — read-only reconciliation.
- **Dependencies:** none.

### Phase 1 — Identity and canonical-source closure

- **Inputs:** Phase 0 inventory, `knowledge_bus/research/investigation_specs/inv_*.yaml`.
- **Actions:** assign/confirm activation_key and frame identity for every target; map each target to a canonical investigation_spec or flag as A4 (research incomplete/ambiguous). Frame count for each of the 36 remaining targets is treated as **UNKNOWN UNTIL this phase closes** — a one-target/one-frame assumption is provisional inventory planning only and must not be carried into Phase 2/3 for any target (`ARCH-CONV-A_medical_review_wave_plan.md` §1.1).
- **Outputs:** closed identity map, including a **complete target-to-frame map for all 41 targets** with an explicit declared frame count per target (no target left with an undeclared or assumed frame count entering Phase 2).
- **Implementation authority:** GPT (medical/architectural), Anthony ratification of identity closure — this is STOP A.
- **Validation:** no duplicate `signal_id` resolves to more than one frame without explicit disambiguating context; no signal-only lookup remains where a frame is ambiguous.
- **STOP conditions:** STOP A — inventory and identity closure (§ full spec in `ARCH-CONV-A_stop_gates_and_acceptance.md`).
- **Rollback point:** identity map is documentation-only; no runtime rollback needed.
- **Dependencies:** Phase 0.

### Phase 2 — Medical-review waves

- **Inputs:** closed identity map, canonical investigation_specs, wave plan (`ARCH-CONV-A_medical_review_wave_plan.md`).
- **Actions:** Gate 1 GPT structured review + Gate 2 Anthony ratification per wave.
- **Outputs:** ratification decision per frame: approved / rejected / narrowed / deferred (see wave plan §7 decision model).
- **Implementation authority:** GPT (Gate 1), Anthony (Gate 2).
- **Validation:** every promoted frame has both gate records; no frame promoted solely because equivalent legacy content already exists.
- **STOP conditions:** STOP B — medical ratification by wave.
- **Rollback point:** a rejected/deferred frame simply does not proceed to Phase 3; no rollback needed.
- **Dependencies:** Phase 1.

### Phase 3 — Deterministic compile and validation

- **Inputs:** Gate 1+2-approved frames.
- **Actions:** compile ratified frames into artefacts per §1.3 schema; run compiler/schema/determinism tests.
- **Outputs:** compiled artefacts + register rows (not yet runtime-active — register rows can exist in a pre-active state pending Phase 4 integration proof).
- **Implementation authority:** Cursor, under a MIXED-classified work package with tests listed.
- **Validation:** compiler determinism tests, manifest completeness tests (`ARCH-CONV-A_test_and_replay_strategy.md`).
- **STOP conditions:** none beyond standard Stage D audit; medical STOP already passed in Phase 2.
- **Rollback point:** artefact + register row deletion, no runtime exposure yet.
- **Dependencies:** Phase 2.

### Phase 4 — Governed runtime integration by wave

- **Inputs:** Phase 3 artefacts.
- **Actions:** activate register rows to `COMPILED_ACTIVE` for the wave; run exclusivity, fail-closed, and consumer/clinician alignment proofs on a representative wave first (STOP C) before repeating for remaining waves.
- **Outputs:** live compiled WHY authority for the wave's targets; legacy path proven non-selected for those activation_keys.
- **Implementation authority:** Cursor (activation), Claude (audit), GPT+Anthony (HIGH-risk dual approval).
- **Validation:** legacy-vs-compiled precedence tests, rejected-frame inactivation tests, fail-closed tests.
- **STOP conditions:** STOP C — first-wave runtime proof (must pass before estate-wide repetition of Phase 4 across subsequent waves).
- **Rollback point:** register row revert to prior state (absent/legacy) — no code rollback needed if Phase 4 mechanics are unchanged wave-to-wave.
- **Dependencies:** Phase 3; STOP C gates repetition beyond the first wave.

### Phase 5 — Legacy WHY retirement and reachability proof

- **Inputs:** completed waves, `ARCH-CONV-A_legacy_retirement_policy.md`.
- **Actions:** prove each retiring legacy source is runtime-unreachable for its migrated activation_keys; deregister loaders where a shared legacy file has no remaining active dependents.
- **Outputs:** legacy sources classified retired/isolated/proven-unreachable per `ARCH-CONV-A_legacy_retirement_policy.md`.
- **Implementation authority:** Cursor, Claude audit.
- **Validation:** reachability proof tests; no remaining registry target depends on a file proposed for deregistration.
- **STOP conditions:** STOP D — legacy retirement authority.
- **Rollback point:** loader deregistration is reversible until physical deletion, which requires separate authorisation per `ARCH-CONV-A_legacy_retirement_policy.md`.
- **Dependencies:** Phase 4 completion for all targets sharing a given legacy file.

### Phase 6 — Estate regression, replay and closure

- **Inputs:** all completed waves.
- **Actions:** full estate regression suite, representative replay panels, closure record authoring.
- **Outputs:** Package A closure record (successor to `ARCH-CONV_programme_closure_record.md` pattern).
- **Implementation authority:** Claude audit, GPT review, Anthony final ratification.
- **Validation:** all success criteria in `ARCH-CONV-A_stop_gates_and_acceptance.md` §Success Criteria.
- **STOP conditions:** none beyond final audit; this phase either PASSes or returns to the failing wave.
- **Rollback point:** N/A — closure phase.
- **Dependencies:** Phase 5 for all waves.

No phase is altered from this structure based on current repository evidence; the six phases map directly onto the four STOP gates without requiring additional phases or merging any of the above.
