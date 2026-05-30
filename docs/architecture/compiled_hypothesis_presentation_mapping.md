# Compiled Hypothesis → RootCauseHypothesisV1 Presentation Mapping

**Status:** LOCKED for ARCH-RT-5 pilot  
**Authority:** ARCH-RT-4 carry-forward, ARCH-RT-5 M3

## Fields

| Compiled field | Runtime DTO field | Rule |
|----------------|-------------------|------|
| `summary_template` | `RootCauseHypothesisV1.summary` | **Primary** presentation/runtime wording (max 200 chars). |
| `physiological_claim` | *(not mapped directly)* | Governed clinical reasoning claim; audit and divergence only unless explicit transform approved. |
| `title` | `RootCauseHypothesisV1.title` | Direct map. |
| `evidence_for` (strings) | `RootCauseHypothesisV1.evidence_for[]` | Map each string to `RootCauseEvidenceItemV1.item` at promotion time. |
| `evidence_against` (strings) | `RootCauseHypothesisV1.evidence_against[]` | Same as evidence_for. |
| `missing_data_policy` | `RootCauseHypothesisV1.missing_data[]` | Requires structured parse at promotion; pilot uses policy text only in shadow. |
| `confirmatory_tests` | `RootCauseHypothesisV1.confirmatory_tests[]` | Registry lookup required. |

## Runtime helper

`compiled_hypothesis.runtime_summary_for_hypothesis(row, promoted=True)` returns `summary_template` only and **fails closed** when absent.

`runtime_summary_for_hypothesis(row, promoted=False)` may fall back to truncated `physiological_claim` for shadow comparison only.

## ARCH-RT-5C decision

| Path | Status |
|------|--------|
| `signal_vitamin_d_low` compiled artefact | **runtime_promoted_compiled** — wired into `compile_root_cause_v1()` via `_compile_compiled_hypothesis_finding()` |
| Legacy YAML | **Retained** — `load_vitamin_d_low_hypotheses_v1()` unchanged; not called for promoted signal at runtime |
| Non-pilot root-cause | Unchanged — legacy `_compile_finding()` path only |

## Multi-frame

No multi-frame hypothesis promotion in ARCH-RT-5. Root-cause compiler `signal_id` first-match remains documented limitation.
