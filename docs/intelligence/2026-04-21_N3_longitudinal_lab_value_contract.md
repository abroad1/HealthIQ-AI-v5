# N-3 — Longitudinal lab value contract (implementation note)

## What changed

- `BiomarkerNode` (`backend/core/contracts/insight_graph_v1.py`) now includes optional `lab_value` and `lab_unit`. Field names avoid legacy enforcement patterns that blocked JSON keys `value` / `unit` on the graph.
- `build_insight_graph_v1` (`backend/core/analytics/insight_graph_builder.py`) populates these from the same measured inputs used for status scoring when values exist on scoring rows or `filtered_biomarkers`.
- `snapshot_linker._nodes_from_biomarkers_payload` (`backend/core/analytics/snapshot_linker.py`) copies measured value/unit from persisted biomarker rows when reconstructing prior graphs from `AnalysisResult.biomarkers` fallback path.
- `comparable_lab_delta` (`backend/core/analytics/longitudinal_numeric_v1.py`) provides a deterministic same-unit delta helper for later narrative compilation (no prose).

## Why

Prior longitudinal replay exposed status/score normalization but did not carry explicit lab numerics needed for benchmark-style “from X to Y” narration. N-3 closes that gap at the contract and reconstruction layer without changing transition semantics.

## What this unblocks

Later deterministic narrative compiler work can read `lab_value` / `lab_unit` on current and prior `InsightGraphV1.biomarker_nodes` (plus `comparable_lab_delta`) without inferring numbers from scores.

## Limits

- Unit mismatch or one-sided unit: delta helper returns `None` (safe refusal).
- LLM path continues to use status/score-derived views in `format_template_from_insight_graph`; raw numerics are not injected for prompt enrichment.
