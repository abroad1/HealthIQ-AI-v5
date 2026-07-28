# ARCH-CONV-A — STOP C Wave 1 Runtime Proof

**Work ID:** `ARCH-CONV-A`  
**Branch:** `feature/arch-conv-a-estate-why-authority-migration`  
**Date (UTC):** 2026-07-28  
**Scope:** First-wave runtime proof for the five ratified Wave 1 thyroid frames only  
**Decision artefact:** `docs/architecture/ARCH-CONV-A_wave1_thyroid_gate1_gate2_decision.md`

## STOP C Declaration

```text
STOP C first-wave runtime proof: COMPLETE
```

Wave 1 thyroid runtime integration is now bounded and proven for:

```text
signal_tsh_high::inv_tsh_high_hypothyroidism
signal_tsh_low::inv_tsh_low_hyperthyroidism
signal_free_t3_high::inv_free_t3_high_t3_predominant_thyrotoxicosis
signal_free_t4_high::inv_free_t4_high_thyrotoxicosis_context
signal_free_t4_low::inv_free_t4_low_thyroid_hormone_deficiency
```

No authority is granted by this artefact to proceed beyond STOP C.

## Runtime Integration Performed

The authorised first-wave runtime integration was completed by:

- recording Gate 1 / Gate 2 ratification in the durable decision artefact and Wave 1 decision register;
- adding five compiled thyroid WHY artefacts under `knowledge_bus/compiled/hypotheses/`;
- adding five Wave 1 authority rows to `knowledge_bus/governance/compiled_why_authority_register_v1.yaml`;
- extending the runtime pilot cohort in `backend/core/knowledge/why_authority_v1.py`;
- aligning compiled-output provenance and estate inventory registers;
- encoding ratified TSH / FT4 / FT3 narrowing in the thyroid package signal libraries;
- hardening runtime identity resolution so the duplicate live `S24` and `KB52C` TSH package sources resolve to the same approved frame IDs without duplicate compiled WHY emission.

## Ratified Runtime Boundaries Proven

The implemented runtime now proves:

- `TSH high + FT4 low` routes to the primary thyroid-hormone-deficiency lane.
- `TSH high + FT4 normal` routes to the raised-TSH / subclinical context lane only.
- `TSH high + FT4 high` does not emit the ordinary hypothyroid compiled WHY lane.
- `TSH low + FT4 high and/or FT3 high` routes to a thyrotoxicosis-compatible lane.
- `TSH low + FT4 normal + FT3 normal` routes to the low-TSH / subclinical context lane only.
- `TSH low + FT4 low` does not emit the ordinary hyperthyroid compiled WHY lane.
- `FT3 high + TSH low/suppressed + FT4 not elevated` routes to the T3-predominant lane.
- `FT3 high + FT4 high` suppresses the T3-specific lane so the broader FT4-high thyrotoxicosis lane wins.
- `FT4 high + TSH normal/high` fails closed for the ordinary thyrotoxicosis compiled WHY lane.
- `FT4 low + TSH low or inappropriately normal` fails closed for the ordinary primary-deficiency compiled WHY lane.

## STOP C Proof Requirements

Required STOP C proof from `docs/architecture/ARCH-CONV-A_stop_gates_and_acceptance.md`:

- compiled WHY is canonical for its activation keys: **PROVEN**
- legacy cannot win for the promoted keys: **PROVEN**
- rejected frames are runtime-inert: **PROVEN**
- runtime fails closed: **PROVEN**
- consumer and clinician outputs remain aligned: **PROVEN through retained nearby thyroid completion and compiled-WHY compatibility tests**
- provenance is emitted for compiled WHY: **PROVEN**

## Focused Verification

Validation and proof executed:

```text
python backend/scripts/validate_compiled_why_authority_gate.py
python -m pytest backend/tests/regression/test_arch_conv_a_wave1_thyroid_stop_c.py backend/tests/regression/test_batch2_thyroid_tsh_gating.py backend/tests/regression/test_arch_conv_correct1_programme_closure.py
python -m pytest backend/tests/unit/test_arch_rt5_launch_gate.py backend/tests/unit/test_p1_25_thyroid_completion.py backend/tests/unit/test_compiled_hypothesis_arch_rt4.py backend/tests/unit/test_why_authority_pkg3.py backend/tests/unit/test_compiled_hypothesis_arch_rt5c.py
```

Observed results:

- `validate_compiled_why_authority_gate.py`: `PASS`
- regression compatibility sweep: `38 passed`
- unit compatibility sweep: `54 passed`

## Bounded Corrections Applied During STOP C

Two bounded runtime corrections were required during the proof:

1. **TSH dual-source activation identity alignment**
   - `pkg_kb52c_tsh_high_primary_hypothyroid_pattern`
   - `pkg_kb52c_tsh_low_thyrotoxic_pattern`
   - aligned to the ratified Wave 1 frame IDs in `signal_activation_identity_v1.py`.

2. **Duplicate runtime row protection**
   - `SignalRegistry` now deterministically resolves duplicate activation-key collisions instead of crashing when parallel package sources address the same approved frame.
   - `root_cause_compiler_v1.py` now deduplicates identical runtime rows before compiled WHY assembly.

These changes are bounded to governed activation identity and deterministic emission control. No medical broadening was introduced.

## Explicit Non-Actions

- Automation Bus `finish` was not called.
- No merge was performed.
- No legacy thyroid WHY asset was deleted or disconnected.
- No bilirubin WHY frame was compiled or activated.
- No Package B hand-off work was performed.
- No work beyond STOP C was started.

## Remaining Out-of-Scope Items

- `signal_thyroid_tsh_context` remains outside this Wave 1 compiled promotion and was not newly compiled here.
- Legacy retirement remains a future STOP D concern.
- Estate-wide repetition beyond the first proven wave remains blocked pending later approval.
