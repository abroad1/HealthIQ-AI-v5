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

`compiled_hypothesis.runtime_summary_for_hypothesis()` returns `summary_template` when present, else truncated `physiological_claim` (fail-safe only — launch promotion must supply `summary_template`).

## ARCH-RT-5 decision

| Path | Status |
|------|--------|
| `signal_vitamin_d_low` compiled artefact | **shadow_only** — mapping defined, **not** wired into `compile_root_cause_v1()` |
| Legacy YAML | Remains production authority |
| Estate promotion | **deferred_non_launch_blocker** pending M3 compiler wiring follow-on |

## Multi-frame

No multi-frame hypothesis promotion in ARCH-RT-5. Root-cause compiler `signal_id` first-match remains documented limitation.
