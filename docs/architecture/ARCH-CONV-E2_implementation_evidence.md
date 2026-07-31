# ARCH-CONV-E2 — Evidence Report

**work_id:** `ARCH-CONV-E2`  
**branch:** `feature/arch-conv-e2-alt-rvalue-runtime-authority`  
**risk_level:** HIGH / MIXED  
**result:** implementation complete — awaiting independent Claude Code audit, GPT architectural review, and Anthony merge authority

## Verified starting state

All ten prompt starting-point facts were true at kernel start (`main` / `origin/main` @ `4bcdaef`):

- six `pkg_kb52c_alt_high_*` packages present with mandatory assets + PSI, no `intelligence_model.yaml`
- all six withheld from runtime activation before this package
- activation register gated placement vs activation
- `pkg_s24_alt_high_hepatocellular_injury` was the sole active `signal_alt_high` frame
- former Batch 5 keys superseded / not reactivated
- `r_value_alt_alp` absent from `ratio_registry.py`
- ALP/GGT `liver_injury_axis` unchanged as cholestatic authority

Canonical Pass 3 SHA-256 (unchanged):

`7F20BF9A06B3427217AD7F753C4D9304E5D5A2C46C484699257778844B9D3267`

## Contemporaneous / same-sample contract (Phase 0)

No repository `sample_id` / multi-draw pairing convention exists.  
`BiomarkerPanel` is a single-snapshot `Dict[str, BiomarkerValue]`.  

**Governed rule adopted:** markers present on the same analysis panel are contemporaneous by the single-panel snapshot contract. No fabricated multi-timestamp pairing mechanism was added. Provenance records `pairing: same_panel_snapshot`.

## R-value metric

| Item | Value |
|---|---|
| ID | `r_value_alt_alp` |
| Formula | `(ALT / ALT lab ULN) / (ALP / ALP lab ULN)` |
| ULN source | `reference_range.max` with `source == "lab"` only |
| Registry version | `1.2.0` |
| Boundaries | `R >= 5` hepatocellular; `2 < R < 5` mixed; `R <= 2` cholestatic |

Fail-closed omissions (exposed via `derived_result.omitted` / `derived_ratios_meta.omitted`):

- missing ALT/ALP result
- missing / non-lab / non-positive / invalid ULN
- missing `reference_ranges` argument
- divide-by-zero / invalid ratio

Orchestrator now passes `input_reference_ranges` into `compute()`. Policy/SSOT bounds are never used as ULN substitutes.

## Collision-authority decision table

| Situation | Decision |
|---|---|
| ALP primary + GGT supporting | Unchanged `liver_injury_axis` suppression |
| ALT hepatocellular (`R >= 5`) + ALP/GGT | Coexist as distinct biochemical-pattern layer |
| ALT mixed (`2 < R < 5`) + ALP/GGT | Coexist as distinct layer |
| ALT cholestatic R-value (`R <= 2`) | **PROMOTE_BUT_WITHHOLD** — would duplicate cholestatic_source_axis |
| Intra-ALT R-band selection | Package `mandatory_pre_emission_gates` on `r_value_alt_alp` (existing evaluator contract; Pass 3 thresholds verbatim) |
| Missing R-value eligibility | No `signal_alt_high` pattern frame emits (fail closed) |

New group: `alt_biochemical_pattern_axis` (`hepatocellular_injury_axis`) in `signal_authority_collision_model_v1.yaml`.  
Empty `supporting_signal_families` is intentional — exclusivity is gate-based; family-level named-key filtering would incorrectly drop sibling ALT frames.

## Per-package promotion / activation

| Package | Decision | Runtime |
|---|---|---|
| `pkg_kb52c_alt_high_hepatocellular_injury_pattern` | `PROMOTE_AND_ACTIVATE` | activated |
| `pkg_kb52c_alt_high_mixed_biochemical_pattern` | `PROMOTE_AND_ACTIVATE` | activated |
| `pkg_kb52c_alt_high_cholestatic_alp_predominant_context` | `PROMOTE_BUT_WITHHOLD` | withheld |
| `pkg_kb52c_alt_high_muscle_source_or_exertional_pattern` | `DEFERRED_WITH_EXPLICIT_REASON` | withheld |
| `pkg_kb52c_alt_high_bilirubin_severity_context` | `DEFERRED_WITH_EXPLICIT_REASON` | withheld |
| `pkg_kb52c_alt_high_metabolic_steatotic_liver_pattern` | `PROMOTE_BUT_WITHHOLD` | withheld |

Vocabulary note: `PROMOTE_AND_ACTIVATE` / `PROMOTE_BUT_WITHHOLD` / `DEFERRED_WITH_EXPLICIT_REASON` did not pre-exist in-repo; introduced as the first promotion+activation decision axis layered on the binary activation register (hardening observation).

## Legacy ALT disposition

| Identity | Disposition |
|---|---|
| `signal_alt_high::inv_alt_high_hepatocellular_injury` (S24) | **SUPERSEDED** — removed from `activated_frames` |
| Former Batch 5 inferred keys | Remain superseded / unreachable; not reactivated |
| `signal_hepatic_alt_context` | Remains activated for legacy context WHY |
| Compiled WHY for new ALT R-value frames | Not claimed complete — `root_cause_registry_v1.py` still registers predecessor only |

When R-value is ineligible, no `signal_alt_high` pattern frame emits (fail closed for R-dependent classification).

## Registry before / after

| Metric | Before (ARCH-CONV-E) | After (ARCH-CONV-E2) |
|---|---:|---:|
| `activated_frame_count` | 173 | 174 |
| Active `signal_alt_high` keys | S24 only | hepatocellular + mixed R-value |
| Withheld ARCH-CONV-E ALT keys | 6 | 4 |

## Tests run

```text
python -m pytest backend/tests/unit/test_arch_conv_e2_r_value_runtime_authority.py \
  backend/tests/unit/test_arch_conv_e_runtime_activation_boundary.py \
  backend/tests/unit/test_arch_conv_e_alt_package_assets.py \
  backend/tests/unit/test_ratio_registry.py \
  backend/tests/regression/test_signal_authority_collision_enforcement.py -q
→ PASS

python -m pytest backend/tests/regression/test_arch_conv_c_alp_ggt_stop_c.py -q
→ 20 passed

python backend/scripts/validate_compiled_why_authority_gate.py
→ PASS; 37 frames, 21 compiled_active, 1 rejected, 15 legacy_retired
```

## Confirmations

- No raw Pass 3 research read at runtime
- No frontend medical inference added
- No Pass 3 JSON modification
- Former Batch 5 keys not reactivated
- ALP/GGT cholestatic enforcement preserved (GGT still suppressed when ALP primary present alongside ALT hepatocellular)

## Unresolved / deferred

- Cholestatic ALT R-value frame withheld until a key-level (not family-level) collision suppress can avoid duplicating ALP/GGT without a resolver contract change
- Muscle / bilirubin / MASLD deferred pending distinguishing pre-emission gates
- Compiled WHY migration for `signal_alt_high` R-value frames not executed in this package
- Medical-frame identity index may still list stale Batch 5 rows (hygiene; out of minimal scope)

## Files changed (scoped)

See `git diff --name-only` on the implementation commit. Primary surfaces:

- `backend/core/analytics/ratio_registry.py`
- `backend/core/pipeline/orchestrator.py`
- `knowledge_bus/governance/signal_authority_collision_model_v1.yaml`
- `knowledge_bus/governance/package_runtime_activation_register_v1.yaml`
- six ALT package manifests (+ R-value signal_library gates)
- unit/regression tests + this evidence report
