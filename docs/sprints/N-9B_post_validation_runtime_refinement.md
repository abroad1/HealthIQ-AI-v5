# N-9B — Post-validation runtime refinement (implementation note)

## N-9 weaknesses targeted

Per `docs/golden-narrative/AB_BENCHMARK_RUNTIME_VALIDATION_N9.md`:

1. **Retail summary empty** — IDL marked benchmark phenotypes `clinical_only` while the narrative compiler only assembled retail copy for `phenotype_allowed`.
2. **Body overview too thin** — single arbitration line vs calmer-system / theme context available from the insight graph and governed functional titles.
3. **Longitudinal / lifestyle parity** — harness still has no DB-linked priors; **lifestyle bridges** can be exercised on the same AB path by passing optional lifestyle JSON to the golden runner (see below). No new longitudinal architecture.
4. **Additional bounded gap** — **`secondary_systems`** was unused; N-9 called out missing “what is working well” / reassurance — populated deterministically from high `system_capacity_scores` outside the primary driver’s system prefix.

## What changed

| Area | Change |
|------|--------|
| Governed IDL | `ph_one_carbon_homocysteine_macrocytosis_v1` and `ph_lipid_residual_ldl_favourable_transport_v1` → `frontend_allowed_term: phenotype_allowed` so retail-facing narrative can use the same governed labels/subtitles as Section 5 cards. |
| Compiler | `body_overview` now stacks: primary driver, supporting systems, **≥90 capacity “calmer” systems**, and **benchmark functional `display_title`s** from N-6 (via interpretation entities). |
| Compiler | `secondary_systems` filled with non-lead high-capacity systems (excludes primary driver id prefix). |
| Tests | `test_n9b_retail_summary_and_secondary_systems_with_published_idl`; IDL registry count assertions updated to **11** records (repo reality). |
| Fixture | `backend/tests/fixtures/panels/ab_n9b_lifestyle_bridge.json` — optional `alcohol_units_per_week` for golden-runner bridge coverage. |

## AB golden runner — lifestyle bridge (optional)

From `backend/`:

```text
set PYTHONPATH=.
python tools/run_golden_panel.py --fixture tests/fixtures/panels/ab_full_panel_with_ranges.json --lifestyle-fixture tests/fixtures/panels/ab_n9b_lifestyle_bridge.json --run-id n9b-ab-lifestyle-check
```

When homocysteine coherence holds, `meta.lifestyle_interpretation_bridges_v1` can activate and the compiler appends bridge lines to the lead narrative (existing N-4 behaviour).

## Frontend re-entry recommendation

**Controlled frontend re-entry is now more defensible** for surfaces that show `retail_summary`, `body_overview`, and pattern cards together: retail copy is no longer structurally empty for the AB benchmark phenotypes, and overview/reassurance layers carry deterministic context without new LLM or architecture.

Broad parity with the **full** benchmark prose (multi-paragraph patient summary, panel-0 longitudinal story) still depends on **richer inputs** (questionnaire, linked priors) and optional follow-on assembly—not claimed closed in this sprint.
