# ARCH-CONV-A — STOP C Wave 2 Runtime Proof

**Work ID:** `ARCH-CONV-A`  
**Branch:** `feature/arch-conv-a-estate-why-authority-migration`  
**Date (UTC):** 2026-07-28  
**Scope:** Wave 2 runtime proof for the three ratified lipid frames only  
**Decision artefact:** `docs/architecture/ARCH-CONV-A_wave2_lipid_gate1_gate2_decision.md`  
**Decision register:** `docs/architecture/ARCH-CONV-A_wave2_medical_decision_register.yaml`

## STOP C Declaration

```text
STOP C Wave 2 lipid runtime proof: COMPLETE
```

Wave 2 lipid runtime integration is now bounded and proven for:

```text
signal_ldl_cholesterol_high::inv_ldl_high_dyslipidaemia
signal_hdl_cholesterol_low::inv_hdl_low_cardiovascular
signal_triglycerides_high::inv_triglycerides_high_metabolic
```

Gate references:

```text
GPT-GATE1-ARCH-CONV-A-W2-LIPID-2026-07-28-v1
ANTHONY-GATE2-ARCH-CONV-A-W2-LIPID-2026-07-28-v1
```

No authority is granted by this artefact to proceed beyond Wave 2 STOP C.

## Runtime Integration Performed

- recorded Gate 1 / Gate 2 ratification in the durable decision artefact and Wave 2 decision register;
- reconciled LDL / TG identities to embedded canonical `spec_id` values (no filename `_v1` activation keys);
- added three compiled lipid WHY artefacts under `knowledge_bus/compiled/hypotheses/`;
- added three Wave 2 `COMPILED_ACTIVE` authority rows plus Pass-3 / blocked-target `LEGACY_RETIRED` rows;
- extended the runtime pilot cohort in `backend/core/knowledge/why_authority_v1.py`;
- encoded HDL as `why_role: morphology_context` (canonical equivalent of CONTEXT_ONLY);
- encoded LDL and TG as narrowed causal lanes without diagnosis / treatment language;
- retired competing Pass-3 parallel WHY for `signal_ldl_high`, `signal_hdl_low`, Pass-3 TG, and unauthorised total-cholesterol frames;
- aligned estate index and root-cause authority register provenance entries.

## Ratified Runtime Boundaries Proven

- LDL high alone → LDL signal present; bounded atherogenic-risk WHY; no diagnosis or treatment recommendation.
- HDL low alone → HDL signal present; morphology_context only; no causal WHY.
- Triglycerides high alone → TG signal present; bounded metabolic-risk WHY; no assumed single cause.
- LDL high + HDL low → one coherent lipid interpretation; HDL remains context only.
- Triglycerides high + HDL low → integrated adverse lipid pattern; no independent HDL causal WHY.
- LDL + TG + HDL → two causal lanes + HDL context; no three-frame causal output.
- No `_v1` duplicate activation identities.
- No total-cholesterol / ApoA1 / lipid-transport-dysfunction Wave 2 causal authority.
- Wave 1 thyroid boundaries unchanged on lipid panels.

## Focused Verification

Validation and proof executed:

```text
python backend/scripts/validate_compiled_why_authority_gate.py
python -m pytest backend/tests/regression/test_arch_conv_a_wave2_lipid_stop_c.py
python -m pytest backend/tests/regression/test_arch_conv_a_wave1_thyroid_stop_c.py backend/tests/regression/test_arch_conv_correct1_programme_closure.py
python -m pytest backend/tests/unit/test_why_authority_pkg3.py backend/tests/unit/test_arch_rt5_launch_gate.py backend/tests/unit/test_duplicate_authority_resolution_v1.py
python -m pytest backend/tests/regression
```

Observed results:

- `validate_compiled_why_authority_gate.py`: `PASS` (`frames=27`, `compiled_active=17`, `rejected=1`, `legacy_retired=9`)
- Wave 2 STOP C suite: `10 passed`
- Wave 1 thyroid + CORRECT-1 / unit protections: `PASS`
- Full regression vs `main`: **13 failures on branch**, **13 failures on main**, **0 new regressions**

## Explicit Non-Actions

- Automation Bus `finish` was not called.
- No merge was performed.
- No legacy lipid WHY asset was deleted or disconnected from disk.
- No blocked Wave 2 targets were compiled or activated.
- No Wave 1 thyroid medical boundaries were altered.
- No Wave 3 work was started.
- No external medical content was introduced beyond the governed research chain and ratified narrowing.

## Independent Wave 2 STOP C Re-audit Closure

Independent Wave 2 STOP C audit result:

```text
Wave 2 STOP C: PASS
audit recommendation: PROCEED_TO_WAVE_3_PLANNING
new regressions versus main: 0
```

Wave 3 renal STOP B pack assembly is authorised under this recommendation. Wave 3 compile / runtime activation remains blocked until Gate 1 / Gate 2 ratification.
