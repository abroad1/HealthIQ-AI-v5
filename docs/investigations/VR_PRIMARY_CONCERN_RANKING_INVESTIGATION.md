# VR primary concern ranking — read-only investigation

**Question:** Why does `signal_alp_low` rank above `signal_homocysteine_elevation_context` in `report_v1.top_findings`, making ALP-low the clinician `primary_concern`?  
**Mode:** Investigation only — no code/fixture/merge changes.  
**Method:** Deterministic `run_golden_panel` on the authoritative VR acceptance fixture + trace `compile_report_v1` in `report_compiler_v1.py`.

---

## 1. Executive summary

On the VR acceptance panel, **`signal_alp_low` and `signal_homocysteine_elevation_context` both emit `signal_state: suboptimal` and `confidence: 0.9`.**  
`compile_report_v1` sorts **all** `signal_results` with a fixed tuple key: **(1) descending state severity, (2) descending confidence, (3) ascending `signal_id` string.**

Because the first two keys are **identical** for these two signals, order is decided solely by the **third key — lexicographic `signal_id`.**  
`"signal_alp_low"` sorts **before** `"signal_homocysteine_elevation_context"` in ascending string order, so ALP-low receives **`priority_rank: 1`** and becomes **`top_findings[0]`**, hence the clinician report primary concern.

This is **fully determined by current code** (`EXPECTED_CURRENT_BEHAVIOUR` for the implementation as written). It is **not** evidence of non-determinism or KB-S53 having changed the pipeline. Whether that tie-break is **clinically desirable** is a separate product question; it is **not** a silent bug in the sense of arbitrary ordering.

**Recommendation:** **`ACCEPT_VR_FIXTURE_UPDATE`** — the regenerated VR clinician JSON is **consistent with the documented sort**. If homocysteine should win ties, that requires a **follow-on, explicit ranking policy** (not rejecting the fixture as “wrong”).

---

## 2. VR fixture used (authoritative)

- **Path:** `backend/tests/fixtures/panels/vr_full_panel_with_ranges.json`  
- **Registry:** `panel_acceptance_profiles_v1.yaml` → profile `vr_acceptance` (same path via `tests.support.panel_acceptance.vr_acceptance_fixture_path()`).

---

## 3. Relevant `signal_results` rows (current deterministic run)

Extracted from `insight_graph.signal_results` after `run_golden_panel` (representative run, `write_narrative=False`):

| `signal_id` | `signal_state` | `confidence` | `system` | `primary_metric` |
|-------------|----------------|-------------|----------|------------------|
| `signal_alp_low` | `suboptimal` | **0.9** | `nutritional` | `alp` |
| `signal_homocysteine_elevation_context` | `suboptimal` | **0.9** | `vascular` | `homocysteine` |

Both rows match on the first two sort dimensions.

---

## 4. Relevant `report_v1.top_findings` rows (excerpt)

From the same run (`insight_graph.report_v1.top_findings`):

| `priority_rank` | `signal_id` | `signal_state` | `confidence` | `primary_metric` |
|-----------------|-------------|----------------|-------------|------------------|
| 1 | `signal_alp_low` | `suboptimal` | 0.9 | `alp` |
| 2 | `signal_homocysteine_elevation_context` | `suboptimal` | 0.9 | `homocysteine` |
| 3 | `signal_homocysteine_high` | `suboptimal` | 0.9 | `homocysteine` |
| … | … | … | … | … |

---

## 5. Where ordering is decided (code)

**File:** `backend/core/analytics/report_compiler_v1.py`  
**Function:** `compile_report_v1`  
**Constants:** `_STATE_RANK = {"at_risk": 4, "suboptimal": 3, "optimal": 2, "unknown": 1}`  

**Sort (lines 436–443):**

```python
ordered_findings = sorted(
    signal_results,
    key=lambda row: (
        -_STATE_RANK.get(str(row.get("signal_state", "unknown")).strip(), 1),
        -float(row.get("confidence", 0.0) if isinstance(row.get("confidence", (int, float))) else 0.0),
        str(row.get("signal_id", "")),
    ),
)
```

`top_findings` are then enumerated in that order with `priority_rank = 1, 2, …` (lines 444–467).

**Clinician report** (`compile_clinician_report_v1`) takes **`top_findings[0]`** from the already-built `report_v1` payload to set `primary_concern` and page-1 lines — it does **not** re-rank.

---

## 6. Precise reason ALP-low ranks first

1. **State:** Both signals are `suboptimal` → `_STATE_RANK` = 3 → sort key component **−3** for both.  
2. **Confidence:** Both **0.9** → second component **−0.9** for both.  
3. **Tie-break:** Third component is **`signal_id` ascending**.  
   - `"signal_alp_low"` **&lt;** `"signal_homocysteine_elevation_context"` (lexicographic: `…_alp_…` before `…_homocysteine_…`).

Therefore **`signal_alp_low` is first** in `ordered_findings`, **`priority_rank` 1**, and **`compile_clinician_report_v1`** correctly surfaces it as **`primary_concern`**.

**Missing-data / completeness:** Not involved in this ordering step; data-quality fields in the clinician report are computed **after** primary selection from `top_findings` and biomarker rows (separate logic in `compile_clinician_report_v1`).

---

## 7. Judgement

| Option | Verdict |
|--------|---------|
| **EXPECTED_CURRENT_BEHAVIOUR** | **Yes** — output matches the implemented sort and tie-break. |
| **SUSPICIOUS_RANKING_BEHAVIOUR** | **No** — not arbitrary or flaky; **arguably suboptimal clinically** if lexicographic tie-break is not the intended product rule. |

---

## 8. Recommendation

| Option | Verdict |
|--------|---------|
| **ACCEPT_VR_FIXTURE_UPDATE** | **Yes** — accept the regenerated fixture as faithful to **current** deterministic behaviour. |
| **DO_NOT_ACCEPT_FIXTURE_UPDATE_YET** | **Only if** product explicitly rejects **alphabetic** tie-breaking for primary concern; then fix belongs in a **ranking-policy** sprint, not in reverted fixture truth. |

---

## 9. Reproduction (operator)

From repo root:

```powershell
Set-Location backend
python -c "
from pathlib import Path
import json
from tools.run_golden_panel import run_golden_panel
from tests.support.panel_acceptance import vr_acceptance_fixture_path
out = Path('../_vr_rank_repro')
out.mkdir(exist_ok=True)
_, ar = run_golden_panel(fixture_path=vr_acceptance_fixture_path(), output_root=out, run_id='repro', write_narrative=False)
ig = (ar.get('meta') or {}).get('insight_graph') or {}
for row in ((ig.get('report_v1') or {}).get('top_findings') or [])[:5]:
    if isinstance(row, dict):
        print(row.get('priority_rank'), row.get('signal_id'), row.get('signal_state'), row.get('confidence'))
"
```

---

## 10. Relation to KB-S53

KB-S53 did **not** change `report_compiler_v1.py`. Any difference vs an older VR clinician JSON is **snapshot drift** against this **long-standing** sort rule, not a regression introduced by the harness sprint.
