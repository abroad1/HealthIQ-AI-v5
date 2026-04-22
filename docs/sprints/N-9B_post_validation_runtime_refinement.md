# N-9B — Post-validation runtime refinement (implementation note)

Aligned with **hardened N-9B** scope: retail + body overview + longitudinal/lifestyle parity on the validation path. No `secondary_systems` assembly. **No golden-runner overlay** — longitudinal is embedded in a **single fixture**.

## N-9 weaknesses targeted

Per `docs/golden-narrative/AB_BENCHMARK_RUNTIME_VALIDATION_N9.md`:

1. **Retail summary empty** — IDL `clinical_only` gating vs compiler `phenotype_allowed`.
2. **Body overview too thin** — single arbitration line vs graph + governed functional titles.
3. **Longitudinal** — golden harness without DB priors; compiler path must be exercisable from **one self-contained panel JSON**.

## What changed

| Area | Change |
|------|--------|
| Governed IDL | Benchmark one-carbon + residual-LDL rows → `frontend_allowed_term: phenotype_allowed`. |
| Compiler | `body_overview` stacks: primary driver, `supporting_systems`, capacity **≥90**, benchmark functional **`display_title`**s. |
| Orchestrator | If `user` contains **`narrative_longitudinal_embed_v1`** (`prior_biomarker_lab_snapshot_v1`, `state_transitions`), merge into `meta` / `meta["insight_graph"]` immediately before **`compile_narrative_report_v1`** (fixture/CI only; production callers omit the key). |
| Fixture | `ab_full_panel_with_ranges_longitudinal_embed_v1.json` — same biomarkers as AB acceptance; **`user.narrative_longitudinal_embed_v1`** carries prior labs + transitions. |
| Golden runner | **Unchanged** from pre-overlay behaviour (no sidecar, no re-compile). |
| Tests | `test_n9b_retail_summary_and_body_overview_with_published_idl`; `test_golden_panel_longitudinal_embed_fixture_exercises_narrative`; IDL registry count **11**. |

## Commands

**AB + embedded longitudinal (single file):**

```text
python tools/run_golden_panel.py --fixture tests/fixtures/panels/ab_full_panel_with_ranges_longitudinal_embed_v1.json --run-id n9b-ab-longitudinal-embed
```

**Lifestyle bridge (optional, separate small JSON):**

```text
python tools/run_golden_panel.py --fixture tests/fixtures/panels/ab_full_panel_with_ranges.json --lifestyle-fixture tests/fixtures/panels/ab_n9b_lifestyle_bridge.json --run-id n9b-ab-lifestyle
```

## Frontend re-entry

Controlled re-entry is more defensible where **`retail_summary`** and **`body_overview`** surface together. Production longitudinal remains **DB-linked priors**; the embed is for **deterministic harness parity** only.
