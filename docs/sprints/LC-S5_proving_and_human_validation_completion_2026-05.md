# LC-S5 — Launch-core proving and human validation (completion note)

**Work ID:** LC-S5-LAUNCH-CORE-PROVING-AND-HUMAN-VALIDATION  
**Branch:** `sprint5/launch-core-proving-and-human-validation`  
**Date:** 2026-05-12

## Fresh proving harness run

- **Command:** `python backend/tools/launch_core_proving_harness.py` (from repo root)  
- **Result:** Success (`exit code 0`). Outputs written to:
  - `docs/audit-papers/launch-core-proving/PROVING_REPORT.md`
  - `docs/audit-papers/launch-core-proving/latest_fingerprints.json`
- **Stamp (report):** `20260512T203559Z` (see `PROVING_REPORT.md` header)
- **Fingerprint `git_short_sha`:** `58bcd8f` (matches branch tip; see `latest_fingerprints.json` after final harness refresh).

## Matrix covered

AB × VR × `baseline`, `lifestyle_context`, `statin_off`, `statin_on` (per `launch_core_matrix.json`).

## CHECK 2 (alcohol bridge in `lead_narrative`)

- **Status:** **PASS** — `backend/tests/regression/test_lc_s5_proving_checks.py::test_check2_alcohol_bridge_language_when_moderate_threshold_met`  
- **Method:** Direct `AnalysisOrchestrator.run` on AB panel with `lifestyle_inputs` including `alcohol_units_per_week: 10` (≥ moderate threshold per hardening note 2B-001). Asserts bridge vocabulary (`alcohol`, `macrocytosis`, `lifestyle bridge`, `methylation`, etc.) appears in `lead_narrative`.  
- **Note:** `AB__lifestyle_context` matrix row uses `lifestyle_minimal.json` (7 units/week) and does **not** assert alcohol bridge text in fingerprints.

## CHECK 4 (legacy `legacy_v1` on consumer path)

- **Status:** **Satisfied by LC-S4 Jest** (`legacyInsightsVisibility`, results/actions wiring) per `lc_s5_proving_readiness_preflight_audit.md`; **not** promoted to backend Sentinel in this sprint (frontend Sentinel runner gap remains).

## CHECK 5 (band vs headline contradiction)

- **Status:** **PASS** — `test_check5_wave1_consumer_domain_band_vs_consequence_consistency` scans all `consumer_domain_rows` in `latest_fingerprints.json` with conservative regex rules (stable/optimal vs emergency wording; elevated bands vs falsely reassuring copy).

## CHECK 6 (clinician primary concern vs retail summary lead)

- **Status:** **PASS** — `test_check6_clinician_retail_lead_family_alignment_ab_vr_baseline` asserts `homocysteine` appears in both `primary_concern_head` and `retail_summary_head` for `AB__baseline` and `VR__baseline`.

## Sentinel

- **`wave1_contradiction`:** Promoted from **PLACEHOLDER** to **GUARDED** / `active_deterministic`; test path now `backend/tests/regression/test_lc_s5_proving_checks.py` (`sentinel/packs/escaped_defects_v1.json`, `sentinel/sentinel_runner.py`, `sentinel/classifier.py`).  
- **Removed:** `backend/tests/regression/test_wave1_contradiction_status.py` (superseded).  
- **`statin_signal_isolation`:** Re-run after LC-S5 — **0 issues / 0 gaps** (`python sentinel/sentinel_runner.py --defect-class statin_signal_isolation`).

## Human validation walkthrough

- **Status:** **Prepared as checklist only** (no browser execution in this agent session).  
- **Limitation:** Real upload/results/Actions verification (screenshots, mock-mode banner, hero slug check, etc.) remains **manual** — carried forward per sprint prompt.

## Tests run (reported)

```text
python -m pytest backend/tests/regression/test_lc_s5_proving_checks.py -m regression --tb=short -q
python -m pytest backend/tests/regression -m regression --tb=line -q
python sentinel/sentinel_runner.py --defect-class wave1_contradiction
python sentinel/sentinel_runner.py --defect-class statin_signal_isolation
```

## Frontend Sentinel infrastructure (carried forward)

- Frontend Jest Sentinel runner support  
- IDL `clinical_only` gate promotion  
- Legacy insights consumer-path backend Sentinel promotion  
- `body_overview` / `retail_summary` carriage promotion  
- Mock-mode honesty conditional render test and promotion  

## Non-goals confirmed

No changes to analytical engine, SSOT, Knowledge Bus, questionnaire assets, narrative compiler, frontend report pages, or Automation Bus control-plane scripts (only tests, proving docs, Sentinel pack/runner/classifier).
