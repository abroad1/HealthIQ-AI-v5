# N-9B — Post-validation runtime refinement (implementation note)

Aligned with **hardened N-9B** scope: retail + body overview + **proof** that the longitudinal compiler path works. **No orchestrator injection.** **No golden-runner overlay.**

## N-9 weaknesses targeted

Per `docs/golden-narrative/AB_BENCHMARK_RUNTIME_VALIDATION_N9.md`:

1. **Retail summary empty** — IDL `clinical_only` vs compiler `phenotype_allowed`.
2. **Body overview too thin** — arbitration line vs graph + governed functional titles.
3. **Longitudinal** — demonstrate **`compile_narrative_report_v1`** with `state_transitions` + **`meta.prior_biomarker_lab_snapshot_v1`** (unit test only).

## What changed

| Area | Change |
|------|--------|
| Governed IDL | Benchmark one-carbon + residual-LDL rows → `frontend_allowed_term: phenotype_allowed`. |
| Compiler | `body_overview` stacks: primary driver, `supporting_systems`, capacity **≥90**, benchmark functional **`display_title`**s. |
| Longitudinal proof | **`test_n9b_longitudinal_path_proof_direct_compiler_call`** — calls **`compile_narrative_report_v1`** with `insight_graph` + `meta` only. |
| Golden runner | **Unchanged** (no longitudinal sidecar or user embed). |
| Orchestrator | **Unchanged** for N-9B longitudinal (no `user` embed). |
| Tests | `test_n9b_retail_summary_and_body_overview_with_published_idl`; IDL registry count **11**. |

## Optional harness data

- **`ab_n9b_lifestyle_bridge.json`** — still valid for **`--lifestyle-fixture`** on the standard AB JSON (N-4 bridges on lead narrative).

## Frontend re-entry

Controlled re-entry is more defensible where **`retail_summary`** and **`body_overview`** surface together. Production longitudinal remains **DB-linked priors** feeding the same compiler inputs the unit test exercises directly.
