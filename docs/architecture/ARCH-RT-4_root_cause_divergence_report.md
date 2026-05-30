# ARCH-RT-4 Root-Cause Divergence Report

**Pilot signal:** `signal_vitamin_d_low`  
**Legacy YAML:** `knowledge_bus/root_cause/hypotheses/vitamin_d_low_hypotheses_v1.yaml`  
**Compiled artefact:** `knowledge_bus/compiled/hypotheses/signal_vitamin_d_low.yaml`  
**Investigation spec (compile source):** `inv_vitamin_d_low_deficiency_v1.yaml`

## Matching hypothesis IDs

| hypothesis_id | In legacy YAML | In compiled artefact | Title match |
|---------------|----------------|----------------------|-------------|
| `vitamin_d_nutritional_status_context_v1` | Yes | Yes | Yes |

No orphan hypotheses on either side for this pilot.

## Claims present in both

- Low 25-hydroxyvitamin D nutritional status framing.
- Evidence strength **strong** (legacy `evidence_strength`; compiled `evidence_strength`).
- Vitamin D signal firing and below-range marker support (legacy via rules; compiled via `evidence_for` strings).
- Within-range counter-evidence (legacy `evidence_against_rules`; compiled `evidence_against`).
- Calcium missing-data context (legacy `missing_data_markers`; compiled `missing_data_policy`).

## Claims present only in investigation spec / compiled artefact

- Full `physiological_claim` sentence from spec `evidence.physiological_claim` (compiled artefact).
- Spec `narrative.mechanism` / `biological_pathway` content is **not** fully duplicated in legacy YAML (compiled carries claim-level translation only).

## Claims present only in legacy YAML

- Rule-based `evidence_for_rules` / `evidence_against_rules` with `rule_id`, `markers_all`, `direction` predicates.
- `summary_template` retail-safe sentence (legacy runtime uses this for emitted `summary`).
- `required_markers` / `confirmatory_markers` / `safety_class` / `differentiator_markers` blocks.

## evidence_for / evidence_against differences

- Legacy: structured rules evaluated at compile/runtime boundary.
- Compiled: static string lists aligned to rule `evidence_for_item` text where possible.
- Sets are **semantically aligned** but not byte-identical (acceptable pilot delta).

## Missing-data handling

- Legacy: per-marker `missing_data_markers` with `marker_id` + `reason`.
- Compiled: single `missing_data_policy` paragraph.
- Wording differs; intent aligned (calcium contextual depth).

## Confirmatory tests

- Both legacy and compiled: **empty** `confirmatory_tests` (STOP #5 N/A).

## Contradiction markers

- Both: empty / none for this hypothesis.

## Retail wording / summary_template

- Legacy `summary_template` is the consumer-facing summary source today.
- Compiled `physiological_claim` is governance-richer and not identical to `summary_template`.
- Runtime compiler still maps legacy YAML → `RootCauseHypothesisV1.summary`; compiled path does not replace this in ARCH-RT-4.

## Blocks runtime pilot?

**No** — hypothesis IDs align; divergence is structural/translation-level, not missing hypothesis coverage.

## Recommendation

**acceptable_with_carry_forward**

Carry-forwards:

- Promote compiled authority only after compiler mapping from compiled schema → `RootCauseHypothesisV1` is agreed.
- Resolve summary vs physiological_claim presentation under IDL/retail boundaries.
- Add confirmatory test mapping when repeat 25(OH)D enters registry.
