# ADR — WP2 Layer B → Layer C contract (Path B)

## Status

Accepted — WP2-LAYER-B-LAYER-C-TECHNICAL-CLOSURE (Pre-Sprint 3 technical closure).

## Context

Pre-Sprint 1 §3.9 governs the analytical boundary: **Layer B decides; Layer C synthesises.** Layer C must not invent, alter, reorder, reinterpret, or strengthen analytical truth.

Structural promotion of Layer B artefacts onto `AnalysisDTO` was discussed as Path A; WP2 deliberately narrows scope to contract readiness without `AnalysisDTO` restructuring.

## Decision

1. **`ReportV1`** remains the short-term **typed Layer B source** for `top_findings`, `root_cause_v1`, clinician-report inputs, and ranked finding / hypothesis material carried with the insight graph.
2. **`NarrativePayloadV1`** is the formal **Layer B → Layer C handoff object** for Sprint 3 readiness: structured section intents, claim boundaries, and references to the same typed Layer B models (no duplicate medical definitions).
3. **`NarrativeReportV1`** remains the **Layer C deterministic prose output** of `compile_narrative_report_v1()` (N-8 narrative compiler).
4. **`AnalysisDTO` restructuring** (Path A — first-class `top_findings` / `root_cause_v1` on the DTO) is **deferred** unless future evidence shows Path B cannot satisfy product safety.
5. **Layer C must not rely on arbitrary `meta` keys for medical meaning**; validator and narrative inputs should consume explicit Layer B fields (e.g. via `report_v1` / payload digests), not undocumented meta soup.
6. **Path A** remains an optional later architectural cleanup, **not** a prerequisite for Sprint 3 authoring.

## Consequences

- Orchestrator builds `NarrativePayloadV1` from `InsightGraphV1.report_v1` and passes it into the narrative compiler as an optional typed parameter.
- LLM output validation can consume Layer B fields mirrored into the validator prompt envelope (lead signal id, allowed hypothesis ids).
- Consumers continue to read ranked findings via `meta.insight_graph.report_v1` until Path A is explicitly approved.

## Compliance

This ADR does not change biomarker logic, signal ranking, Knowledge Bus content, or SSOT authority files.
