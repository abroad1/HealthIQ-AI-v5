# ARCH-CONV-PKGB-1 — Phase 0 Hardening Pack (Gate 1 / Gate 2 STOP)

**Work ID:** `ARCH-CONV-PKGB-1`  
**Branch:** `feature/arch-conv-pkgb-1-homocysteine-exclusivity-resolver-closure`  
**Risk:** HIGH  
**Change type:** MIXED  
**Execution model:** TWO_PHASE_START_FINISH  
**Implementation owner:** Core Engine agent  
**Status:** Gate 1 `APPROVED_WITH_NARROWING` (`ARCH-CONV-PKGB-1-GATE1-HMR-2026-08-02`). Gate 2 `PENDING`. **Runtime implementation not authorised.**

**Hardening clearance:** `automation_bus/latest_prompt_hardening.json` — `ARCH-CONV-PKGB-1` / `HARDENED`.

---

## 0. Baseline (repository-grounded)

| Check | Result |
|---|---|
| Feature branch tip at Phase 0 | `b8777e9` (bus stage commit) |
| Stash | Empty (governed; no triage required) |
| Active WP after start | `ARCH-CONV-PKGB-1` / `IN_PROGRESS` |
| Register totals (live load) | `COMPILED_ACTIVE=26`, `LEGACY_RETIRED=25`, `REJECTED=1`, frames=52 |
| `signal_homocysteine_high` authority | 2× `COMPILED_ACTIVE` + 1× `REJECTED` (metabolic) |
| `signal_homocysteine_elevation_context` in `_PILOT_SIGNAL_IDS` | **Absent** |
| Shared asset | `knowledge_bus/root_cause/hypotheses/hcy_hypotheses_v1.yaml` (`primary_signal_id: signal_homocysteine_elevation_context`) |
| Stage 1B reality check | **YES** — all six defects remain; not a no-op |

---

## 1. Stage 1A — Authority preflight (recorded)

### 1.1 Compiled-WHY authority for `signal_homocysteine_high`

| activation_key | authority_state | artefact |
|---|---|---|
| `signal_homocysteine_high::inv_homocysteine_high_b_vitamin_related_methylation_impairment` | `COMPILED_ACTIVE` | `knowledge_bus/compiled/hypotheses/inv_homocysteine_high_b_vitamin_related_methylation_impairment.yaml` |
| `signal_homocysteine_high::inv_homocysteine_high_renal_clearance_reduction` | `COMPILED_ACTIVE` | `knowledge_bus/compiled/hypotheses/inv_homocysteine_high_renal_clearance_reduction.yaml` |
| `signal_homocysteine_high::inv_homocysteine_high_metabolic` | `REJECTED` | none — do not compile / promote / fallback |

Evidence: `knowledge_bus/governance/compiled_why_authority_register_v1.yaml:36-70`.  
Pilot membership: `backend/core/knowledge/why_authority_v1.py:25` (`signal_homocysteine_high` in `_PILOT_SIGNAL_IDS`).

### 1.2 Live legacy WHY path for `signal_homocysteine_elevation_context`

| Element | Repository fact |
|---|---|
| Registry row | `root_cause_registry_v1.py:29` — `RootCauseTargetSpec("signal_homocysteine_elevation_context", lrc.load_hcy_hypotheses_v1, "hcy_hypotheses_v1.yaml")` |
| Package activation | `package_runtime_activation_register_v1.yaml:195-196` — `signal_homocysteine_elevation_context::inv_elevation_context` → `pkg_homocysteine_elevation_context` |
| Pilot cohort | **Not** in `_PILOT_SIGNAL_IDS` (`why_authority_v1.py:22-54`) |
| Resolver mode today | Out-of-pilot → `"legacy"` (`why_authority_v1.py:164-165`) |
| Live proof | `resolve_frame_why_authority(signal_id="signal_homocysteine_elevation_context", activation_key="signal_homocysteine_elevation_context::inv_elevation_context")` → `("legacy", None)` |

### 1.3 Shared physical asset / loader / dual registration

| Surface | Path / line |
|---|---|
| Shared YAML | `knowledge_bus/root_cause/hypotheses/hcy_hypotheses_v1.yaml:4` — `primary_signal_id: "signal_homocysteine_elevation_context"` |
| Loader | `lrc.load_hcy_hypotheses_v1` |
| Dual `RootCauseTargetSpec` | `root_cause_registry_v1.py:29-30` — elevation-context **and** high both point at the same loader/file |

### 1.4 Ratified `FOLD_SUPPRESS` disposition

Already ratified under ARCH-CONV-A Wave 0 / STOP A; **not** a new medical decision:

- `docs/architecture/ARCH-CONV-A_wave0_suppression_closure.md:13-25` — `disposition: FOLD_SUPPRESS`; independent frame count 0; shared YAML still connected; Package B hand-off for exclusivity.
- `docs/architecture/ARCH-CONV-A_phase1_target_to_frame_map.md:69` — STOP A ratified FOLD_SUPPRESS; shared file not disconnected — Package B hand-off.
- Carry-forward still open: `docs/sprints/launch_core_carry_forward_register.md:102` — `CF-ARCH-CONV-DUAL-HCY-1` / Residual Package B / Open.

### 1.5 Resolver / fail-closed behaviour

| Behaviour | Evidence |
|---|---|
| Bare-key branch | `why_authority_v1.py:134-147` — if pilot and `not key`: unique `COMPILED_ACTIVE` → `compiled`; else → `fail_closed` |
| Fail-closed raise | `root_cause_compiler_v1.py:737-741` — `mode == "fail_closed"` raises `ValueError` |
| Live bare TC | `resolve_frame_why_authority(signal_id="signal_total_cholesterol_high", activation_key="")` → `("fail_closed", None)` |
| Keyed retired skip | For a keyed `LEGACY_RETIRED` row, mode is already `"skip"` (`why_authority_v1.py:155-157`) — defect is the **bare-key zero-compiled** path only |

### 1.6 Pilot `signal_id`s with zero `COMPILED_ACTIVE` rows

Live enumeration (all `_PILOT_SIGNAL_IDS` vs register):

| signal_id | row states | governance shape |
|---|---|---|
| `signal_ldl_high` | 2× `LEGACY_RETIRED` | uniform all-retired |
| `signal_hdl_low` | 2× `LEGACY_RETIRED` | uniform all-retired |
| `signal_total_cholesterol_high` | 2× `LEGACY_RETIRED` | uniform all-retired |
| `signal_hgb_low` | 1× `LEGACY_RETIRED` | uniform all-retired |
| `signal_hepatic_alt_context` | 1× `LEGACY_RETIRED` | uniform all-retired (expected ARCH-CONV-I consequence) |

**No materially different governance shape** among these five — STOP condition for separate adjudication is **not** triggered. Part B may use one governed rule covering all five.

### 1.7 Current failing assertions (`test_root_cause_v1_homocysteine.py`)

| Test | Stale / defective expectation | Ratified / correct posture |
|---|---|---|
| `test_root_cause_v1_hba1c_hypotheses_emit_for_hba1c_signal` (`:209`) | expects `hba1c_glycaemic_exposure_pattern_v1` | `hyp_hba1c_elevated_glycaemia_context` (ARCH-CONV-H) |
| `test_root_cause_v1_arch_conv_b_uses_compiled_creatinine_urea_and_legacy_urate` (`:500`) | expects `urate_elevated_serum_hyperuricaemia_v1` | `hyp_urate_elevated_non_causal_context` (ARCH-CONV-G) |
| `test_root_cause_v1_r8_total_cholesterol_high_emits_governed_hypotheses_not_fallback` (`:505+`) | bare-key TC still raises / expects legacy emission | governed non-emitting skip; **no** new TC compiled WHY |

### 1.8 No new medical research / package / frontend required

Confirmed by hardening and this Phase 0 mapping: FOLD_SUPPRESS already ratified; resolver fix is mechanical; HbA1c/urate are assertion alignment only.

### 1.9 L-04 / L-05 / L-06 remain out of scope

`docs/architecture/ARCH-CONV_legacy_dependency_register.md` — L-04/L-05/L-06 product-policy preconditions unmet. Explicitly excluded from this sprint.

---

## 2. Stage 1B — Reality check

| Statement | Verdict |
|---|---|
| `signal_homocysteine_elevation_context` still reaches legacy WHY content | **TRUE** |
| `signal_homocysteine_high` already has compiled-WHY authority | **TRUE** (2 COMPILED_ACTIVE) |
| Both identities still reference the shared homocysteine hypothesis asset | **TRUE** |
| Bare-key resolver still raises for `signal_total_cholesterol_high` | **TRUE** (`fail_closed`) |
| HbA1c and urate hypothesis-ID tests are stale | **TRUE** |
| Defects are not already resolved | **TRUE** — not a no-op |

---

## 3. Stage 1C — Intelligence Core surfaces (expected impact after Gate 2)

| Surface | Expected post-Gate-2 change |
|---|---|
| `why_authority_v1.py` | Bare-key zero-compiled pilot → governed `skip`; elevation-context enter pilot + retired/skip path if that mechanism is chosen |
| `compiled_why_authority_register_v1.yaml` | Likely `+1 LEGACY_RETIRED` for elevation-context WHY-only (if register mechanism chosen) |
| `root_cause_registry_v1.py` / shared YAML | Narrowest exclusivity may disconnect elevation-context from shared selector **or** leave asset on disk while skip prevents emit — Phase 1 chooses narrowest proven mechanism |
| `root_cause_compiler_v1.py` | No L-04 change; fail-closed raise retained for genuine ambiguity |
| Tests | New `test_arch_conv_pkgb_1_exclusivity_resolver.py`; stale ID assertions corrected; F/G/H/I remain green |
| Package / PSI / SSOT / frontend | **Unchanged** |

Expected behaviour change limited to prompt § Stage 1C items 1–3 only.

---

## 4. Proposed Phase 1 mechanism options (Gate 1 chooses; Cursor implements narrowest after Gate 2)

### Option A — WHY-only retirement via existing authority model (recommended by hardening)

- Add `signal_homocysteine_elevation_context` to `_PILOT_SIGNAL_IDS`.
- Add register row `signal_homocysteine_elevation_context::inv_elevation_context` as `LEGACY_RETIRED` (WHY-only), mirroring ARCH-CONV-I retirement of `signal_hepatic_alt_context::inv_alt_context`.
- Package / PSI / activation remain unchanged.
- Shared YAML may remain on disk; emit blocked by `skip`.

### Option B — Disconnect elevation-context from shared selector

- Remove or redirect the elevation-context `RootCauseTargetSpec` so it cannot load/emit shared hypotheses.
- Must not change package/signal activation reachability.
- Must not alter `signal_homocysteine_high` compiled content.

### Option C — Other existing governed skip/retired disposition

Only if Phase 1 proves it is narrower than A/B while preserving determinism.

**Gate 1 must confirm FOLD_SUPPRESS implementation intent and that no new medical hypothesis/narrative is required.** Mechanism selection among A/B/C is architectural within that medical boundary.

---

## 5. Part B — Bare-key resolver correction (mechanical)

When pilot `signal_id` has **zero** `COMPILED_ACTIVE` rows and activation_key is empty:

- Today: unconditional `fail_closed` → runtime `ValueError`.
- Required: governed non-emitting `skip` when all relevant rows are retired/rejected/non-owning.
- Preserve `fail_closed` for genuine ambiguity (e.g. multiple `COMPILED_ACTIVE`, missing governance, contradictory state).
- Do **not** create compiled authority for total cholesterol or any of the five zero-compiled pilots.
- Cover all five structural-class members in tests, not only TC.

---

## 6. Part C — Stale test corrections (assertion-only)

| Family | Ratified hypothesis ID |
|---|---|
| HbA1c | `hyp_hba1c_elevated_glycaemia_context` |
| Urate | `hyp_urate_elevated_non_causal_context` |

No production content change to satisfy old tests.

---

## 7. Explicit exclusions (unchanged from prompt)

- No change to `signal_homocysteine_high` compiled medical content
- No independent WHY authority for elevation-context
- No L-04 / L-05 / L-06 product-policy decisions
- No Package C replay/versioning
- No new TC medical content / `COMPILED_ACTIVE`
- No frontend / package activation / PSI / scoring changes

---

## 8. Gate STOP

Gate 1: **RECORDED** — `ARCH-CONV-PKGB-1-GATE1-HMR-2026-08-02` / `APPROVED_WITH_NARROWING`.  
Gate 2: **PENDING** — Anthony must ratify Gate 1 exactly.

**Runtime implementation remains forbidden until Gate 2 is recorded and `runtime_changes_authorised: true`.**

Work package remains `IN_PROGRESS`.
