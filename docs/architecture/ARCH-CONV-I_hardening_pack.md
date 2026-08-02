# ARCH-CONV-I — Phase 0 Hardening Pack (Gate 1 / Gate 2 STOP)

**Work ID:** `ARCH-CONV-I`  
**Branch:** `feature/arch-conv-i-alt-compiled-why-identity-resolution`  
**Risk:** HIGH  
**Change type:** MIXED  
**Execution model:** TWO_PHASE_START_FINISH  
**Implementation owner:** Core Engine agent  
**Status:** Phase 0 mapping complete. Gate 1 `PENDING`. Gate 2 `PENDING`. **Implementation prohibited** until both gates are recorded on disk and match this pack (or the prompt is revised and re-hardened).

**Hardening clearance:** `automation_bus/latest_prompt_hardening.json` — `ARCH-CONV-I` / `HARDENED` (Phase 0 + Gate STOP only).

---

## 0. Baseline (repository-grounded)

| Check | Result |
|---|---|
| Feature branch tip at start | `50a1708` (bus stage commit) |
| Stash | Empty |
| Active WP after start | `ARCH-CONV-I` / `STARTED` |
| `compiled_why_authority_register_v1.yaml` ALT / hepatic_alt rows | **Zero** for `signal_alt_high` and `signal_hepatic_alt_context` |
| Baseline counts | `COMPILED_ACTIVE=25`, `LEGACY_RETIRED=20`, `REJECTED=1`, frames=46 |
| Compiled ALT hepatocellular artefact | **Absent** |
| `signal_alt_high` / `signal_hepatic_alt_context` in `_PILOT_SIGNAL_IDS` | **Absent** |
| Legacy WHY path | `root_cause_registry_v1.py:32` → `alt_hypotheses_v1.yaml` (**live**) |
| Stage 1B reality check | **YES** — gap remains; not a no-op |

---

## 1. Stage 1B reality check (confirmed)

| Statement | Verdict | Evidence |
|---|---|---|
| `signal_hepatic_alt_context` remains wired to live legacy WHY | **TRUE** | `root_cause_registry_v1.py:32`; out-of-pilot → `"legacy"` |
| Neither identity has compiled-WHY authority | **TRUE** | Zero register rows; no hepatocellular compiled artefact |
| Legacy CRP-coupled hypothesis has no canonical `signal_alt_high` counterpart | **TRUE** | Only `alt_inflammatory_coupling_context_v1` uses CRP; no CRP frame under live `signal_alt_high` estate |
| Legacy hard-coded thresholds are non-SSOT and must not transfer | **TRUE** | AST>45 / GGT>60 / ALP>130 / bilirubin>20 in `pkg_hepatic_alt_context`; ARCH-CONV-D flag remains open |

---

## 2. Legacy WHY identity (`signal_hepatic_alt_context`)

| Element | Repository content |
|---|---|
| Package | `pkg_hepatic_alt_context` |
| Activation key | `signal_hepatic_alt_context::inv_alt_context` |
| Still activated (package layer) | **Yes** — `package_runtime_activation_register_v1.yaml:187-188` |
| Live WHY asset | `knowledge_bus/root_cause/hypotheses/alt_hypotheses_v1.yaml` |
| Asset SHA-256 | `1A8B35E9CEDDAB2F93B044E81FAF2A857C6C236C69CB493C0A06E5FE2593D698` |
| Hypothesis A | `alt_hepatic_cell_stress_pattern_v1` — hepatocellular-stress (AST/GGT confirmatory; bilirubin/ALP differentiators) |
| Hypothesis B | `alt_inflammatory_coupling_context_v1` — CRP / inflammatory coupling (**no canonical counterpart**) |
| Hard-coded override thresholds | AST `>45.0`, GGT `>60.0`, ALP `>130.0`, bilirubin `>20.0` (`signal_library.yaml` `hepatic_multimarker_pattern`) |

**WHY-only retirement key (either outcome):** `signal_hepatic_alt_context::inv_alt_context`  
Package / PSI / card / activation behaviour must remain unchanged under WHY-only retirement.

---

## 3. Canonical hepatocellular identity (Outcome A target ambiguity — Gate 1 must choose)

### Live activated Pass 3 hepatocellular (E2 successor)

| Element | Repository content |
|---|---|
| Activation key | `signal_alt_high::inv_alt_high_r_value_hepatocellular_biochemical_pattern` |
| Package | `pkg_kb52c_alt_high_hepatocellular_injury_pattern` |
| Activation status | **Activated** (`package_runtime_activation_register_v1.yaml:69-70`) |
| Role | Canonical hepatocellular R-value biochemical-pattern frame |
| Source authority | Pass 3 ALT hepatic-pattern research (package cites Pass 3 hash; no standalone investigation YAML on disk for this `spec_id`) |

### Superseded S24 hepatocellular (must not remain co-active)

| Element | Repository content |
|---|---|
| Activation key | `signal_alt_high::inv_alt_high_hepatocellular_injury` |
| Package | `pkg_s24_alt_high_hepatocellular_injury` |
| Investigation YAML | `knowledge_bus/research/investigation_specs/inv_alt_high_hepatocellular_injury_v1.yaml` |
| YAML SHA-256 | `7189A0761558937D4DD4397E823BBE06C7BEE0B13EF9BBE0B3AFC70A73B7413A` |
| Activation status | **SUPERSEDED** by Pass 3 key (`superseded_frames_arch_conv_e2`, register `:40-49`) |

**Phase 0 architectural recommendation (not a medical decision):** if Outcome A is selected, compile only the **live** Pass 3 activation key. Compiling the superseded S24 key would revive a co-active superseded identity.

### Content transferable under Outcome A (joint support only)

Transfer only content jointly supported by:

1. the selected canonical hepatocellular research/package narrative; and  
2. legacy `alt_hepatic_cell_stress_pattern_v1`.

Usable morphology-context themes: ALT elevation as hepatocellular-stress / ALT-predominant biochemical-pattern context; AST/GGT as supporting hepatic chemistry context; bilirubin/ALP as severity/pattern differentiators **without disease confirmation**.

### Content that must NOT transfer

- Legacy CRP / inflammatory-coupling hypothesis (`alt_inflammatory_coupling_context_v1`)
- Legacy hard-coded AST/GGT/ALP/bilirubin numeric thresholds
- Consumer Hy’s Law / DILI diagnosis
- MASLD / steatosis / fibrosis diagnosis from ALT alone
- Treatment directives
- Chronicity inference
- Disease-specific cause attribution / prognosis

---

## 4. `signal_alt_high` activation-frame estate (must remain unchanged)

| Activation key | Package | Role | ARCH-CONV-I action |
|---|---|---|---|
| `…::inv_alt_high_r_value_hepatocellular_biochemical_pattern` | `pkg_kb52c_alt_high_hepatocellular_injury_pattern` | Canonical hepatocellular | Outcome A compile candidate only |
| `…::inv_alt_high_r_value_mixed_biochemical_pattern` | `pkg_kb52c_alt_high_mixed_biochemical_pattern` | E2 mixed R-value | **No change** |
| `…::inv_alt_high_r_value_cholestatic_alp_predominant_context` | `pkg_kb52c_alt_high_cholestatic_alp_predominant_context` | E3 R≤2 subordinate | **No change** |
| `…::inv_alt_high_muscle_source_or_exertional_contribution` | `pkg_kb52c_alt_high_muscle_source_or_exertional_pattern` | E3 CK-gated contextual | **No change** |
| `…::inv_alt_high_metabolic_masld_context` | `pkg_kb52c_alt_high_metabolic_steatotic_liver_pattern` | E3 metabolic contextual | **No change** |
| `…::inv_alt_high_bilirubin_hys_law_severity_context` | `pkg_kb52c_alt_high_bilirubin_severity_context` | Override/escalation only | **No independent activation; no WHY compile** |
| `…::inv_alt_high_hepatocellular_injury` | `pkg_s24_alt_high_hepatocellular_injury` | Superseded S24 | **Do not reactivate / do not compile** |
| `signal_hepatic_alt_context::inv_alt_context` | `pkg_hepatic_alt_context` | Legacy live package | WHY-only retirement candidate; package unchanged |

R-value bands, package reachability, PSI status, ALP/GGT primary source authority, and bilirubin-severity override-only posture remain out of scope.

---

## 5. Two Gate 1 outcomes (only authorised dispositions)

### Outcome A — Narrow `MAP_AND_COMPILE`

- Compile only one hepatocellular activation key (Gate 1 must name it; Phase 0 recommends live Pass 3 key above).
- Retire `signal_hepatic_alt_context::inv_alt_context` for WHY ownership only.
- Exclude CRP/inflammatory-coupling hypothesis.
- Do not transfer hard-coded legacy thresholds.
- Preserve all E2/E3 R-value and contextual activation behaviour.
- **Headline register delta:** `+1 COMPILED_ACTIVE`, `+1 LEGACY_RETIRED`.

**Implementation hazard Gate 1 must acknowledge if Outcome A is chosen:**

1. `signal_alt_high` is **absent** from `ROOT_CAUSE_TARGET_SPECS` today — compiler does not iterate it; Outcome A may need a registry-target extension (configuration reuse, not a new compiler algorithm) for compiled emit to fire.
2. Adding `signal_alt_high` to `_PILOT_SIGNAL_IDS` without authority rows for other live sibling frames fail-closes those frames. Outcome A must either include governed skip-class rows for non-compiled live siblings, or Gate 1 must explicitly authorise a bounded disposition that avoids fail-closed leakage. Headline `+1/+1` may understate required sibling rows.

If safe Outcome A requires inventing content, a runtime alias, threshold transfer, or a new compiler mechanism → **STOP / re-scope** (Outcome B or revised prompt).

### Outcome B — `RETIRE_WITHOUT_SUCCESSOR`

- Retire `signal_hepatic_alt_context::inv_alt_context` for WHY ownership only.
- Do **not** create a compiled ALT WHY artefact.
- Do **not** add `signal_alt_high` to compiled-WHY pilot membership for this sprint.
- Package / PSI / card / activation / R-value behaviour unchanged.
- Record that Gate 1 judged canonical research insufficient for a safe compiled successor **or** that multi-frame fail-closed risk makes Outcome A unsafe without further scoping.
- **Register delta:** `+0 COMPILED_ACTIVE`, `+1 LEGACY_RETIRED`.

---

## 6. Proposed `why_role` (Outcome A only — Gate 1 must ratify)

**Primary recommendation:** `morphology_context` (flat; no `conditional_why_role`).

Rationale: Pass 3 / legacy stress wording is pattern/context language; disease confirmation, Hy’s Law diagnosis, MASLD/fibrosis, and treatment claims are prohibited.

**Alternative for Gate 1 only:** narrowed `causal` limited strictly to “hepatocellular enzyme-leakage / cell-stress pattern” with identical presentation prohibitions.

---

## 7. Mechanism sufficiency

| Outcome | New compiler mechanism required? | Reuse path |
|---|---|---|
| B | **No** | Add `signal_hepatic_alt_context` to pilot + `LEGACY_RETIRED` on `…::inv_alt_context` → `"skip"` (F/G/H parallel-id retirement shape) |
| A | **No new algorithm**, but configuration beyond naive +1/+1 may be required | Pilot + COMPILED_ACTIVE artefact + legacy retirement + possible registry target + sibling skip-class rows |

---

## 8. Intelligence Core surfaces (expected impact)

| Surface | Expected change after gates |
|---|---|
| `compiled_why_authority_register_v1.yaml` | Outcome A: +1 active + ≥1 retired; Outcome B: +1 retired only |
| `_PILOT_SIGNAL_IDS` / `why_authority_v1.py` | As required by ratified outcome |
| Compiled artefact / manifest | Outcome A only |
| `root_cause_authority_register_v1.yaml` | Outcome A consistency row only |
| `root_cause_registry_v1.py` | Outcome A may need `signal_alt_high` target; Outcome B leaves table row but pilot skip suppresses emit |
| Packages / PSI / SSOT / scoring / frontend | **Unchanged** |
| F / G / H regression suites | Must remain green |

---

## 9. Gate status

Gate 1: `ARCH-CONV-I-GATE1-HMR-PENDING` — `PENDING`  
Gate 2: `ARCH-CONV-I-GATE2-ANTHONY-PENDING` — `PENDING`

**Remain stopped.** Do not create compiled artefacts, alter authority registers, retire legacy ownership, or change runtime behaviour until both approvals are committed and consistent with this pack.
