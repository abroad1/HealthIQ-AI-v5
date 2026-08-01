# ARCH-CONV-E3 Implementation Evidence

**Work ID:** `ARCH-CONV-E3`  
**Branch:** `feature/arch-conv-e3-alt-contextual-authority`  
**Gate 1:** `ARCH-CONV-E3-GATE1-HMR-2026-08-01`  
**Gate 2:** `ARCH-CONV-E3-GATE2-ANTHONY-PENDING` (merge blocked until ratified)

## Verified starting state

- ARCH-CONV-E2 merged to `main` and Gate 2 ratified.
- Six ALT packages present with mandatory assets.
- Hepatocellular + mixed activated; four contextual packages withheld.
- Canonical Pass 3 hash `7F20BF9A06B3427217AD7F753C4D9304E5D5A2C46C484699257778844B9D3267` unchanged.
- No stash entries present at preflight.

## Research rule → runtime mechanism mapping

| Context | Disposition | Runtime mechanism |
|---|---|---|
| Cholestatic / ALP-predominant | ACTIVATE subordinate contextual | Existing R≤2 `mandatory_pre_emission_gates`; hyp selection returns `None` for hepatocellular when R≤2; role subordination (not `liver_injury_axis` supporting family) |
| Muscle / exertional | ACTIVATE lab-only subordinate | `mandatory_pre_emission_gates`: `creatine_kinase` `lab_range_boundary` `above_max` |
| Bilirubin severity | OVERRIDE escalation only | `or_alt_high_with_bilirubin_high` (+ siblings) on active ALT frames with `presentation_safety.consumer_hys_law_diagnosis: PROHIBITED`; package withheld |
| Metabolic / MASLD | ACTIVATE lab-only subordinate | Compound `any_of` gate via extended `_passes_mandatory_pre_emission_gates` (`hba1c`/`triglycerides`/`ggt` above_max or `hdl_cholesterol` below_min) |

## Collision / coexistence table

| Pair | Behaviour |
|---|---|
| ALP/GGT primary vs ALT cholestatic | ALP/GGT remain sole cholestatic SOURCE primary; ALT R≤2 is biochemical pattern context. `signal_alt_high` not added as liver supporting family (named-key filter / family-level suppress would harm hepatocellular/mixed). Activation-key-level suppress deferred as contract gap. |
| Hepatocellular vs mixed vs cholestatic | Band ownership: R≥5 hep; 2\<R\<5 mixed; R≤2 cholestatic; R missing → hep rank-2 general |
| Muscle vs hep | Coexist when CK above lab max; muscle does not suppress liver concern |
| Bilirubin | Escalation on active frames only; no competing primary package |

## Activation-register delta

- Version `1.3.0` → `1.4.0`; work_id `ARCH-CONV-E3`
- `activated_frame_count` `174` → `177`
- Added: cholestatic, muscle, metabolic activation keys
- Withheld retained: bilirubin severity only

## Before / after runtime ALT identities

**Before:** hepatocellular, mixed  
**After:** hepatocellular, mixed, cholestatic, muscle, metabolic  
**Still withheld:** bilirubin severity  
**Still superseded:** S24 ALT-high

## Unresolved blockers (explicit)

1. No governed runtime user-context contract (`context_modifier_catalogue_draft_v1.yaml` non-runtime) — blocks exercise/metabolic declared-history paths only.
2. No Pass 3 numeric threshold for “very high ALT” — blocks that specific suppress safeguard only.
3. Activation-key-level suppress of cholestatic ALT when ALP primary present requires collision-contract extension — deferred.

## Proof: no invented medical thresholds / no raw Pass 3 runtime read / no frontend inference

- Gates use lab-range status only.
- Hypothesis selection and package assets remain the runtime path; Pass 3 JSON is not imported by evaluator code.
- No frontend files modified.

## Tests run

```text
PYTHONPATH=backend python -m pytest \
  backend/tests/unit/test_arch_conv_e3_alt_contextual_authority.py \
  backend/tests/unit/test_arch_conv_e2_r_value_runtime_authority.py \
  backend/tests/unit/test_arch_conv_e_runtime_activation_boundary.py \
  backend/tests/unit/test_arch_conv_e_alt_package_assets.py \
  backend/tests/unit/test_signal_evaluator.py::test_signal_registry_alt_high_multi_frame_pilot \
  -q
```

Result: **PASS** (exit 0).

Package validators: muscle + metabolic + other ALT packages validated via activation-boundary suite.

## Files changed (implementation)

See `git diff --name-only` on the feature branch for the authoritative list.
