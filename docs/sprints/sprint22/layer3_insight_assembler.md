# Sprint 22 — Layer 3 Insight Assembler

## Overview

Layer 3 "Insight Assembly" is a deterministic, rule-based assembler that converts Layer 1+2 analysis output into a stable user-facing insight artifact. No LLM. No timestamps. No speculation.

## Contract Summary

- **Root object**: `Layer3InsightsV1`
  - `schema_version`: Exactly `"1.0.0"` (do not auto-increment)
  - `insights`: List of `InsightCard`
  - `summary`: Optional deterministic dict (no timestamps)

- **InsightCard**:
  - `insight_id`: Stable deterministic ID (e.g. `cardiovascular__system_pressure`)
  - `system_id`: System identifier
  - `title`: User-facing title
  - `severity`: `"action"` | `"watch"` | `"info"`
  - `confidence`: `"high"` | `"medium"` | `"low"`
  - `evidence`: EvidenceBlock
  - `interpretation`: Deterministic text
  - `next_steps`: List[str]
  - `flags`: Optional[List[str]]

- **EvidenceBlock** (omit empty sections):
  - `biomarkers`, `derived_markers`, `lifestyle`, `system_burdens`

## 11 Card Definitions

Exactly 11 system cards, each with `insight_id` format `<system_id>__system_pressure`:

| system_id      | insight_id                    |
|----------------|-------------------------------|
| cardiovascular | cardiovascular__system_pressure |
| metabolic      | metabolic__system_pressure     |
| hepatic        | hepatic__system_pressure      |
| immune         | immune__system_pressure      |
| renal          | renal__system_pressure       |
| hormonal       | hormonal__system_pressure    |
| hematological  | hematological__system_pressure |
| musculoskeletal| musculoskeletal__system_pressure |
| nutritional    | nutritional__system_pressure  |
| autonomic      | autonomic__system_pressure   |
| thyroid        | thyroid__system_pressure    |

## Severity Thresholds

Based on adjusted burden (0–1):

- **action**: burden >= 0.66
- **watch**: burden >= 0.33
- **info**: otherwise

## Confidence Downgrade Rules

- Default: `"high"`
- If lifestyle `confidence_penalty` for this system:
  - >= 0.15 → `"low"`
  - >= 0.10 → `"medium"`
  - else → remain `"high"`
- If any biomarker in evidence lacks lab reference range (min or max missing): cap at `"medium"` (never `"high"`)

## Determinism Guarantees

- No datetime, no UUIDs, no random, no file I/O
- No hashing for IDs; rule-based string construction only
- Stable ordering: action → watch → info, then alphabetical by `system_id`, then `insight_id`
- Byte-identical `layer3_insights.json` across repeated runs with same inputs

## Interpretation Template

```
"Your <system> signals are in the <band> range based on this panel."
```

Band: `elevated` (>=0.66), `moderate` (>=0.33), `optimal` (<0.33).

If lifestyle contributed to that system, append:

```
" Lifestyle factors contributed to this signal."
```

## Non-Goals (Explicit)

- **No diagnosis**: Insights are informational, not diagnostic
- **No LLM**: Purely rule-based, no language model
- **No speculation**: Grounded only in biomarkers, derived_markers, system burden vector, lifestyle artifact, existing user profile fields
- **No API/DB/CI changes**: Evaluation harness only; no endpoint or workflow changes
