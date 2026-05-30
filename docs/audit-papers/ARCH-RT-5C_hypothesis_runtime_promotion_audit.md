# ARCH-RT-5C — Hypothesis Runtime Promotion Audit

**Generated:** 2026-05-30  
**Work package:** ARCH-RT-5C_hypothesis_runtime_promotion

## Pilot status

| Item | Classification |
|------|----------------|
| Pilot signal | `signal_vitamin_d_low` |
| Promoted to runtime | **YES** |
| Runtime behaviour changed | **YES** — `compile_root_cause_v1()` routes pilot through compiled bridge |
| Legacy YAML retained | **YES** — `vitamin_d_low_hypotheses_v1.yaml` and loader unchanged |
| `summary_template` enforced | **YES** — validator + `promoted=True` fail-closed |
| `physiological_claim` blocked from runtime summary | **YES** |
| Multi-frame promotion | **NOT introduced** — single hypothesis row only |
| Remaining root-cause estate | Legacy YAML for 40 other signals unchanged |

## Checks

| Requirement | Status |
|-------------|--------|
| Artefact validates | **PASS** |
| Compile manifest resolves | **PASS** — `arch_rt4_vitamin_d_hypothesis.yaml` |
| Cross-load boundary preserved | **PASS** — semver 1.0.0 vs v1 separation |
| Production registry not replaced | **PASS** — `ROOT_CAUSE_TARGET_SPECS` unchanged |
| PSI / card / frontend untouched | **PASS** |

## Outcome

**Complete.** One compiled hypothesis pathway promoted with governed presentation mapping and legacy preservation.
