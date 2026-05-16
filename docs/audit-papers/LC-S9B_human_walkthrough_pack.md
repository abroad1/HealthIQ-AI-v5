# LC-S9B — Human walkthrough pack (Sprint 5 launch-core proving)

**work_id:** LC-S9B  
**Evidence stamp:** see `docs/audit-papers/launch-core-proving/latest_fingerprints.json` (`git_short_sha` at generation time)  
**Harness:** `python backend/tools/launch_core_proving_harness.py`

## How to reproduce reports locally

1. Start backend (`uvicorn` / project default) and frontend (`npm run dev` in `frontend/`).
2. Sign in (e.g. test-user3) or use golden-panel API path used by harness.
3. For each scenario below, run the harness (writes golden outputs under `docs/audit-papers/launch-core-proving/artifacts/<stamp>/`) or start analysis from merged fixtures in `artifacts/<stamp>/_merged_fixtures/`.

**Binary checks (automated):**

```powershell
python backend/tools/launch_core_proving_harness.py
python -m pytest backend/tests/regression/test_lc_s5_proving_checks.py -q
```

---

## Scenario matrix

| ID | Panel | Scenario | Expected lead family | Lifestyle / statin expectation |
|----|-------|----------|----------------------|--------------------------------|
| 1 | AB | baseline | Homocysteine | No intervention annotation |
| 2 | AB | lifestyle_context | Homocysteine | `lead_narrative` includes alcohol / methylation bridge language |
| 3 | AB | statin_off | Homocysteine | No intervention; CV consequence without statin caveat |
| 4 | AB | statin_on | Homocysteine | Intervention present; CV consequence mentions statin |
| 5 | VR | baseline | Homocysteine | Same as AB baseline pattern |
| 6 | VR | lifestyle_context | Homocysteine | Narrative differs from baseline; lifestyle bridge tokens |
| 7 | VR | statin_off | Homocysteine | No intervention |
| 8 | VR | statin_on | Homocysteine | Intervention + CV consequence statin caveat |

---

## Per-scenario checklist

### AB baseline (`AB__baseline`)

- **Fixture:** `backend/tests/fixtures/panels/ab_full_panel_with_ranges.json`
- **Expected lead:** Homocysteine Elevation Context (at_risk)
- **CHECK 6:** `primary_concern_head` and `retail_summary_head` both mention homocysteine
- **Pass if:** Results load; hero does not show raw `signal_*` IDs; no internal “No governed WHY for signal_…” copy

### AB lifestyle_context (`AB__lifestyle_context`)

- **Fixture:** AB panel + `backend/tests/fixtures/lifestyle_minimal.json` (alcohol_units_per_week=10)
- **Expected:** Narrative fingerprint differs from baseline; `lead_narrative_head` contains alcohol / methylation / lifestyle bridge token
- **CHECK 2:** automated `test_check2_lifestyle_context_narrative_differs_from_baseline`

### AB statin_off / statin_on

- **Questionnaire:** `long_term_medications`: `["None"]` vs `["Statins (cholesterol medication)"]`
- **Expected:** Top findings and band labels identical; intervention only on statin_on; cardiovascular `consequence_sentence` changes on statin_on
- **CHECK 4:** automated fingerprint test

### VR scenarios (`VR__*`)

- Same checks as AB using `vr_full_panel_with_ranges.json`.

---

## Consumer UI walkthrough (optional live)

1. Complete or load an analysis from AB panel fixture (via upload/dev tooling).
2. Open `/results?analysis_id=<id>`.
3. Confirm:
   - Primary hero uses homocysteine-led copy (not raw signal slug).
   - Advanced section: biomarker dials + uploaded-panel fidelity still present (FE-S8E regression).
   - No “No governed WHY for signal_…” in hero or page1 primary concern (LC-S9B fallback copy).

---

## Binary CHECK summary (current build)

| CHECK | Description | Automated test |
|-------|-------------|----------------|
| 2 | Lifestyle visible payoff | `test_check2_*` (orchestrator + matrix fingerprints) |
| 4 | Statin intervention bounded | `test_check4_*` |
| 5 | Band vs consequence polarity | `test_check5_*` |
| 6 | Clinician vs retail lead alignment | `test_check6_*` |

---

## Known acceptable caveats

- Questionnaire validation warnings in harness logs (minimal intake scenarios) — expected for baseline/statin matrix rows.
- Not every ranked signal has a full governed WHY asset; fallback is honest and non-speculative.
- `body_overview` may be identical statin off/on while CV domain consequence carries statin caveat (by design).

## Sign-off block (human)

| Tester | Date | Verdict (per scenario 1–8) | Notes |
|--------|------|----------------------------|-------|
| _name_ | _date_ | PASS / FAIL | |
