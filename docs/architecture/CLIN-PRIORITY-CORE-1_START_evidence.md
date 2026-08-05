# CLIN-PRIORITY-CORE-1 — START Evidence (Checkpoint 3)

**work_id:** `CLIN-PRIORITY-CORE-1`  
**branch:** `feature/clin-priority-core-1`  
**HEAD (evidence tip):** see `git rev-parse HEAD` at commit time  
**risk_level:** HIGH / MIXED  
**kernel:** restarted 2026-08-05T11:47:34Z at `ecef04f` after signal-preservation amendment; status `IN_PROGRESS`  
**Do not finish. Do not merge.** STOP for independent review.

## Verdict target

`START_READY_FOR_INDEPENDENT_STOP_REVIEW`

## Kernel restart evidence

| Item | Value |
|---|---|
| Pre-amendment HEAD | `d9b92b2` |
| Amendment commit | `ecef04f` — `docs(bus): amend CLIN-PRIORITY-CORE-1 prompt for signal preservation and re-harden` |
| Fresh `cursor_started_utc` | `2026-08-05T11:47:34Z` |
| Fresh token `head_sha` at start | `ecef04fd46556d2c327e1e6f218f2a9890349c3c` |
| Prompt SHA-256 | `6AD7D88EB2E6644F4F04DF9081D095F4BB304AD0EBAB907D2937D7BB125997C2` |
| Hardening | `HARDENED` linked to same post-amendment prompt hash |

## Canonical paths

| Role | Path |
|---|---|
| Clinical authority | contract v0.6.3; ruleset v0.5; HMR register v0.4; closure v0.4; approval pack v1.2; clinician-first v1.0 |
| Signal baseline | `docs/architecture/CLIN-PRIORITY-CORE-1_signal_activation_baseline.md` |
| Models | `backend/core/models/clinical_finding.py` |
| Compiled artefact | `knowledge_bus/compiled/prioritisation/compiled_prioritisation_rules.yaml` |
| Compile manifest | `knowledge_bus/compiled/manifests/` (`clin_priority_prioritisation_*`) |
| Loader | `backend/core/analytics/prioritisation_registry.py` |
| Concern construction | `backend/core/analytics/concern_constructor.py` |
| InsightGraph / DTO | additive `clinical_concern_set` on `insight_graph_v1.py` + `results.py`; builder calls constructor |
| Scenario harness | `backend/tools/run_clinical_priority_scenarios.py` |
| Fixtures | `backend/tests/fixtures/clinical_priority_scenarios_v1.json` |
| Fixture authority notes | `docs/architecture/CLIN-PRIORITY-CORE-1_checkpoint2_fixture_authority_notes.md` |

## Signal preservation metrics

| Metric | Value |
|---|---|
| `SIGNAL_ACTIVATION_BASELINE_TOTAL` | **183** |
| `SIGNAL_ACTIVATION_PRESERVED_TOTAL` | **183** (SignalRegistry reload after Checkpoint 2) |
| `SUPPORTING_SIGNAL_BASELINE_TOTAL` | **0** (no `dependencies.signals` in estate; supporting biomarkers only) |
| `SUPPORTING_SIGNAL_PRESERVED_TOTAL` | **0** |
| `SIGNALS_INTENTIONALLY_RETIRED` | **0** |

Constituent `activation_key` provenance retained on consolidated findings (constructor + hepatic/estate tests).

## Scenario coverage

```text
PYTHONPATH=backend python backend/tools/run_clinical_priority_scenarios.py --run-id estate-109-verify
→ passed: 110, failed: 0
APPROVED_SCENARIO_ESTATE_COVERAGE: 109/109 unique (CONTRACT-FIX-1 ≡ HEP-AS-1)
skipped: 0
```

```text
PYTHONPATH=backend python -m pytest backend/tests/unit/test_clinical_finding_models.py \
  backend/tests/unit/test_clinical_priority_scenario_runner.py -q
→ 10 passed
```

## Key behavioural proofs

| Proof | Result |
|---|---|
| Hepatic pilot CONTRACT-FIX-1 / HEP-AS-1..14 | Pass |
| `XD-AS-32` no-forced-lead | Pass — three Tier-1 findings; no manufactured co-leads |
| Serious findings non-downgrade | Pass (Tier 0 / same-day retained as data classification) |
| FIB-4 | Internal calc unchanged; not used as finding authority; ignored if present in derived |
| CV-risk % | Not computed |
| Disease-name quarantine | Held where scenarios require |
| `technical_tiebreak_lead` | Not reused for finding-level lead selection |

## FIB-4 disposition

Internal `ratio_registry.fib_4` exists (KB-S10, 2026-03-09). Not consumer-facing fibrosis finding authority. Left unchanged. Concern construction never classifies fibrosis via FIB-4 (HEP-AS-10 / XD-AS-18).

## Commits on feature branch (implementation span)

1. `ecef04f` — amend prompt + re-harden + pre-restart status  
2. `c415cd5` — Phase 0 signal activation baseline  
3. `ba73de5` — models + hepatic compiler  
4. `3492792` — hepatic concern construction  
5. `cf240fb` — hepatic scenario tests  
6. `ff3f40e` — six-domain compiled estate  
7. `0b47ec5` — cross-domain concern prioritisation  
8. `2017902` — 109-scenario acceptance estate  

(+ this evidence commit)

## Explicit incompleteness (FINISH carry-forwards)

- **Checkpoint 4 longitudinal:** only RE-AS-3 / RE-AS-5 minimums implemented; `GOVERNED_LONGITUDINAL_RULE_COVERAGE: 6/6` **not** claimed  
- **Checkpoint 5 frontend:** `technical_tiebreak_lead` UI retirement / render-only concern-set consumption **not** complete  
- Orchestrator → AnalysisDTO population may still need FINISH hardening beyond InsightGraph builder wiring  
- `run_work_package.py finish` **not** run  
- **No merge**

## Confirmations

- No Knowledge Bus promotion / activation-register changes for signal retirement  
- No precedence/arbitration/state_engine modifications  
- Amended §3A hierarchy applied; fixture vs pack prose conflicts escalated to ratified domain rules (see Checkpoint 2 notes), not silent newest-doc override of the signal estate  

## Awaiting

Independent STOP review (Claude Code / human). Do not self-authorise FINISH.
