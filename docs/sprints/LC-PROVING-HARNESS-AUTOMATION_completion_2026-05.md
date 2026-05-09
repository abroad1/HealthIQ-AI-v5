# LC-PROVING-HARNESS-AUTOMATION — completion note (2026-05)

## Scenario matrix

| Panel | Scenario | Questionnaire | Lifestyle |
|-------|-----------|----------------|-----------|
| AB | `baseline` | omitted | none |
| AB | `lifestyle_context` | omitted | `tests/fixtures/lifestyle_minimal.json` |
| AB | `statin_off` | `long_term_medications: ["None"]` | none |
| AB | `statin_on` | `long_term_medications: ["Statins (cholesterol medication)"]` | none |
| VR | same four rows | same | same |

Matrix file: `backend/tests/fixtures/proving/launch_core_matrix.json`.

## Tooling

- **Driver:** `backend/tools/launch_core_proving_harness.py` — merges scenario payloads into temporary panel JSON (no changes to `run_golden_panel.py`), calls `run_golden_panel` for each cell.
- **Reuse:** Same golden-panel path as `verification_ledger_run.py` (`tools.run_golden_panel.run_golden_panel`). Panel fixtures: `ab_full_panel_with_ranges.json`, `vr_full_panel_with_ranges.json`. Lifestyle: `lifestyle_minimal.json`.
- **`verification_clinician_report.py`:** Not invoked as a subprocess; clinician surface is summarised from each run’s `analysis_result` (aligned with how ledger tooling inspects JSON).

## Output format

- **`docs/audit-papers/launch-core-proving/PROVING_REPORT.md`** — Markdown table of scenarios, per-run fingerprints (top findings, bands, narrative/clinician heads, IDL counts, intervention presence), explicit **statin-off vs statin-on invariant** checks, and **baseline vs lifestyle_context** comparison.
- **`docs/audit-papers/launch-core-proving/latest_fingerprints.json`** — Machine-readable fingerprints for the last run (updated each execution).

Bulk `analysis_result.json` trees land under `docs/audit-papers/launch-core-proving/artifacts/<stamp>/` during a run; they may be deleted after review to keep git lean.

## How to rerun

From repository root:

```bash
python backend/tools/launch_core_proving_harness.py
```

Optional:

```bash
python backend/tools/launch_core_proving_harness.py --stamp my-run-id --matrix backend/tests/fixtures/proving/launch_core_matrix.json --out docs/audit-papers/launch-core-proving
```

## Harness tests

```bash
cd backend && python -m pytest tests/unit/test_launch_core_proving_harness.py -v
```

## Stage 4A closure — observations carried forward

### OBS-2 (requires GPT/human confirmation)

AB band label diverges between baseline (no questionnaire) and statin_off (explicit 'None'). This was surfaced by the harness and requires GPT/human confirmation on whether these states are expected to differ.

## Stage 4A closure protocol

- Harness implementation committed on `feature/lc-proving-harness-automation`.
- Bounded unit tests for matrix integrity and fixture merge in place.
- Human-review outputs documented (`PROVING_REPORT.md`, `latest_fingerprints.json`); bulk golden artefacts optional local-only.
- OBS-2 recorded above before kernel `finish`.
