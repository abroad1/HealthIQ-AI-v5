# N-9B — Post-validation runtime refinement (implementation note)

Aligned with **hardened N-9B** scope: retail + body overview + longitudinal/lifestyle parity on the validation path. No `secondary_systems` assembly (rolled back as out-of-contract).

## N-9 weaknesses targeted

Per `docs/golden-narrative/AB_BENCHMARK_RUNTIME_VALIDATION_N9.md`:

1. **Retail summary empty** — IDL `clinical_only` gating vs compiler `phenotype_allowed`.
2. **Body overview too thin** — single arbitration line vs graph + governed functional titles.
3. **Longitudinal / lifestyle parity** — golden harness had no DB-linked priors; longitudinal stayed empty on the AB runner.

## What changed

| Area | Change |
|------|--------|
| Governed IDL | `ph_one_carbon_homocysteine_macrocytosis_v1` and `ph_lipid_residual_ldl_favourable_transport_v1` → `frontend_allowed_term: phenotype_allowed`. |
| Compiler | `body_overview` stacks: primary driver, `supporting_systems`, systems with capacity **≥90**, benchmark functional **`display_title`**s (N-6 via interpretation entities). |
| Golden harness | Optional **`narrative_harness_overrides_v1`** sidecar merged by `run_golden_panel`: injects `prior_biomarker_lab_snapshot_v1` + `state_transitions`, then **re-runs `compile_narrative_report_v1`** on the completed DTO (harness-only; biology unchanged). |
| CLI | `--narrative-harness-overlay` pointing at JSON containing only `narrative_harness_overrides_v1`. |
| Fixtures | `ab_n9b_narrative_harness_overlay.json` (longitudinal); `ab_n9b_lifestyle_bridge.json` (optional N-4 alcohol bridge). |
| Tests | `test_n9b_retail_summary_and_body_overview_with_published_idl`; `test_golden_panel_narrative_harness_overlay_exercises_longitudinal`; IDL registry count **11**. |

## Commands (AB path)

**Lifestyle bridge (N-4):**

```text
python tools/run_golden_panel.py --fixture tests/fixtures/panels/ab_full_panel_with_ranges.json --lifestyle-fixture tests/fixtures/panels/ab_n9b_lifestyle_bridge.json --run-id n9b-ab-lifestyle
```

**Longitudinal harness (synthetic prior + transitions):**

```text
python tools/run_golden_panel.py --fixture tests/fixtures/panels/ab_full_panel_with_ranges.json --narrative-harness-overlay tests/fixtures/panels/ab_n9b_narrative_harness_overlay.json --run-id n9b-ab-longitudinal
```

## Frontend re-entry

Controlled re-entry is more defensible where **`retail_summary`** and **`body_overview`** surface together. Full benchmark longitudinal prose still expects real linked panels in production; the overlay reproduces the **compiler path** for audit and CI.
