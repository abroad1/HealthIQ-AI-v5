# KB-S53 — VR clinician report fixture: operator review pack

**Purpose:** Decide whether to **accept** the regenerated `clinician_report_v1_vr.json` before merge / gate continuation.  
**Scope:** Evidence and interpretation only (no implementation edits in this pack).  
**Baseline:** Old file = `797b236^` (parent of `feat(KB-S53-ABVR-HARNESS)` implementation commit). New file = current tree at `797b236`.

---

## 0. Operator decision (recorded)

**Date:** 2026-04-04  
**Status:** **ACCEPTED** — Regenerated VR clinician report fixture is **approved** as **stale fixture correction** (consistent with deterministic `signal_id` tie-break; KB-S53 did not change ranking code).  
**Cross-reference:** `KB-S53_AB_VR_ACCEPTANCE_HARNESS.md` §Operator acceptance; `VR_PRIMARY_CONCERN_RANKING_INVESTIGATION.md`.

---

## 1. Executive summary

**Outcome (see §0):** Operator **accepted** the regenerated fixture as **stale fixture correction**; primary-concern ordering is explained by existing deterministic tie-break (`signal_id` ascending) in `VR_PRIMARY_CONCERN_RANKING_INVESTIGATION.md`.

The VR “golden” clinician JSON was **fully replaced** in commit `797b236`. The diff is **not** cosmetic (JSON key order): **page1 primary narrative, root-cause block, data-quality counts, and section-level confirmatory tests** all changed.

**KB-S53 implementation commit `797b236` did not modify** `backend/core/analytics/report_compiler_v1.py`, root-cause compiler, scoring, or interaction-map code. The new JSON is what the **existing** pipeline deterministically emits today when running `run_golden_panel` on **`vr_full_panel_with_ranges.json`** and compiling via `compile_clinician_report_v1`.

The dominant semantic change is **primary concern** moving from **`signal_homocysteine_elevation_context`** to **`signal_alp_low`**, which (per code) tracks **`report_v1.top_findings[0]`** after upstream ordering — not a random fixture edit.

**Historical review framing (superseded by §0):** The prior open question was whether ALP-first reflected product intent vs a pipeline concern; operator acceptance records that under **current** ranking rules this is **expected** and the fixture update is **not** treated as a KB-S53 defect.

---

## 2. Exact old vs new field changes (grounded)

| Field | Old (`797b236^`) | New (`797b236`) |
|--------|------------------|-----------------|
| `sections.page1.primary_concern` | `signal_homocysteine_elevation_context (suboptimal)` | `signal_alp_low (suboptimal)` |
| `sections.page1.top_hypothesis_line` | `Top hypothesis: B12-associated pattern (confidence 0.60).` | `Top hypothesis: Low ALP — reduced alkaline phosphatase activity pattern (confidence 0.60).` |
| `sections.page1.key_findings[0]` | `signal_homocysteine_elevation_context is suboptimal. homocysteine is the primary driver.` | `signal_alp_low is suboptimal. alp is the primary driver.` |
| `data_quality.panel_completeness_present` | `6` | `9` |
| `data_quality.panel_completeness_expected` | `6` | `9` |
| `data_quality.lab_range_quality_by_primary_metric` | **6** strings | **9** strings (adds e.g. `alp`, `cortisol`, `creatine_kinase` lines among others) |
| `sections.confirmatory_tests` (top-level list) | **1** item (MMA) | **[]** (empty) |

Additional structural changes (summary): **`sections.root_cause`** switched from **homocysteine** finding + multi-hypothesis block to **ALP-low** hypotheses; **`confidence_and_missing_data`** text changed (missing-data branch vs none).

Full line diff:

```bash
git diff 797b236^..797b236 -- backend/tests/fixtures/reports/clinician_report_v1_vr.json
```

---

## 3. Why these specific fields changed (code-grounded)

Source: `backend/core/analytics/report_compiler_v1.py` — **`compile_clinician_report_v1`** (unchanged in KB-S53).

1. **`primary_concern`, `key_findings[0]`, `top_hypothesis_line`**  
   - `primary` is taken from **`top_findings[0]`** in the incoming `report_v1` payload (`primary = top_findings[0]`).  
   - `primary_concern` is `{primary_signal_id} ({primary_state})`.  
   - First key finding line uses `why_it_matters` from that same row.  
   - `top_hypothesis_line` uses the **first hypothesis** of the **root-cause finding** whose `signal_id` matches that primary signal.  
   - **Interpretation:** upstream **`report_v1.top_findings` ordering** now places **`signal_alp_low`** ahead of homocysteine context for this panel run. That is **not** produced by the fixture JSON file edit in KB-S53; it comes from **`compile_report_v1` / signal ordering** feeding the graph.

2. **`panel_completeness_present` / `panel_completeness_expected`**  
   - Both are derived from the **set of distinct `primary_metric` values** across **all** `top_findings` rows in the payload (`expected_metrics`), with present count = how many of those metrics have a biomarker row with non-null value and range quality checks.  
   - **Interpretation:** the **expanded or reordered `top_findings` set** now yields **9** distinct primary metrics instead of **6**, so completeness counts increased in lockstep.

3. **`lab_range_quality_by_primary_metric`**  
   - Built by iterating **`expected_metrics`** and appending `"<metric>: <quality>"` per metric.  
   - **Interpretation:** list length **6 → 9** because **`expected_metrics` grew** (same root cause as #2).

4. **`sections.confirmatory_tests`**  
   - Built from **`_collect_confirmatory_with_suppression`** on the **primary** root-cause finding and biomarker snapshot.  
   - **Interpretation:** with primary concern **ALP-low** and hypotheses that carry **no** confirmatory tests (or all suppressed), the **aggregated section list** can be **empty**; previously, homocysteine/B12 path surfaced **MMA** at section level.

---

## 4. Current deterministic VR output (reproduction evidence)

Regenerate the same artefact the sprint used (read-only check; from repo root, with `backend` as CWD for imports):

```powershell
Set-Location backend
python -c "
import json
from pathlib import Path
from tools.run_golden_panel import run_golden_panel
from core.analytics.report_compiler_v1 import compile_clinician_report_v1
from tests.support.panel_acceptance import vr_acceptance_fixture_path
out = Path('../.operator_review_vr_regen')
out.mkdir(exist_ok=True)
_, analysis_result = run_golden_panel(
    fixture_path=vr_acceptance_fixture_path(),
    output_root=out,
    run_id='operator-review-vr',
    write_narrative=False,
)
meta = analysis_result.get('meta') or {}
ig = meta.get('insight_graph') or {}
rv = ig.get('report_v1') or {}
bio = analysis_result.get('biomarkers') or []
compiled = compile_clinician_report_v1(report_v1_payload=rv, biomarker_rows=bio)
Path('../.operator_review_vr_regen/clinician_report_v1_vr.generated.json').write_text(
    json.dumps(compiled.model_dump(), indent=2, sort_keys=True) + '\n', encoding='utf-8')
print('Wrote .operator_review_vr_regen/clinician_report_v1_vr.generated.json')
"
```

Compare to committed fixture:

```powershell
fc .operator_review_vr_regen\clinician_report_v1_vr.generated.json backend\tests\fixtures\reports\clinician_report_v1_vr.json
```

Expect **no meaningful diff** if the tree matches `797b236` and the environment is the same.

---

## 5. Did KB-S53 change pipeline / analytics / root-cause / scoring code?

**No.** Commit `797b236` touched only:

- `backend/scripts/run_ab_vr_acceptance_harness.py`
- `backend/tests/fixtures/panels/*` (manifest + README)
- `backend/tests/support/*`
- `backend/tests/unit/test_*.py` (wiring to manifest paths)
- `backend/tests/fixtures/reports/clinician_report_v1_vr.json`
- `docs/investigations/*`

**No** files under `backend/core/pipeline/`, `backend/core/analytics/` (except test-only consumption paths), `backend/ssot/`, signal packages, or interaction maps were modified in that commit.

Therefore: the VR JSON delta reflects **current behaviour of pre-existing engine code**, not a new algorithm introduced inside KB-S53.

---

## 6. Classification

| Label | Applies? | Notes |
|-------|----------|--------|
| **STALE_FIXTURE_CORRECTION** | **Plausible** | Expected JSON was out of date vs **today’s** deterministic output; KB-S53 regenerated it without changing compilers. |
| **POSSIBLE_PIPELINE_CONCERN** | **Plausible** | If the **old** snapshot was correct for product intent, then **today’s** `top_findings[0]` (ALP vs homocysteine) may indicate an **earlier** regression or an undocumented ranking change — **investigation outside KB-S53 file list**. |

These are **not mutually exclusive**: the fixture can be “stale” relative to current code while current code is **still** wrong for product intent.

---

## 7. Recommendation (operator)

| Option | When to use |
|--------|-------------|
| **ACCEPT_FIXTURE_UPDATE** | Product/clinical owner confirms **`signal_alp_low` as primary concern** (first `top_finding`) on `vr_full_panel_with_ranges.json` is **intended** under current rules. |
| **INVESTIGATE_PIPELINE_BEFORE_MERGE** | Primary shift is **unexpected**; or team needs **bisect** / sign-off on `compile_report_v1` inputs (`top_findings` order) before blessing the new golden JSON. |

**Resolved (2026-04-04):** Operator selected **ACCEPT_FIXTURE_UPDATE** / **stale fixture correction** after ranking investigation (`VR_PRIMARY_CONCERN_RANKING_INVESTIGATION.md`). Prior conservative default is **superseded** for this workpackage.

---

## 8. Artifact hygiene

After review, delete any local regen folder (e.g. `.operator_review_vr_regen/`) if created; it should **not** be committed unless the operator chooses to add evidence attachments (out of scope for this pack).
