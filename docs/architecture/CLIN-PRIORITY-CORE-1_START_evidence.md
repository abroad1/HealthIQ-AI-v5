# CLIN-PRIORITY-CORE-1 — START Evidence (Checkpoint 3)

**work_id:** `CLIN-PRIORITY-CORE-1`  
**branch:** `feature/clin-priority-core-1`  
**HEAD (evidence tip):** see `git rev-parse HEAD` at commit time  
**risk_level:** HIGH / MIXED  
**kernel:** restarted 2026-08-05T11:47:34Z at `ecef04f` after signal-preservation amendment; status `IN_PROGRESS`  
**Do not finish. Do not merge.** STOP for independent review.

## Verdict target

`BOUNDED_CORRECTIONS_READY_FOR_REVIEW` (post independent START STOP review)

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

- **Checkpoint 4 longitudinal:** completed in FINISH — see `CLIN-PRIORITY-CORE-1_FINISH_evidence.md` (`GOVERNED_LONGITUDINAL_RULE_COVERAGE: 6/6`)
- **Checkpoint 5 frontend:** completed in FINISH — `clinical_concern_set` rendered; `technical_tiebreak_lead` demoted when concern set present
- Schema-level removal of `primary_concern_mode` / full clinician-report lead retirement remains a release carry-forward (UI demotion complete)
- Final consumer serious-result copy where not already governed remains a release carry-forward

## Bounded corrections after independent START STOP review

**Independent verdict:** `START_STOP_APPROVED_WITH_BOUNDED_CORRECTIONS`  
**Starting HEAD for corrections:** `f36cc178cfb8493ceb50bfa476496df2828adf12`  
**Defect class:** Cursor resolved cross-domain vs generic domain-band tension in favour of subordinate generic domain bands for two approved scenarios.

### Authority applied

| Case | Authority |
|---|---|
| `XD-AS-1` / `RE-AS-12` | Cross-domain ruleset v0.5 §13; approval pack v1.2; renal AS-12 |
| `XD-AS-7` | `XD-ARTEFACT-1`; cross-domain ruleset v0.5; approval pack v1.2 |

### Logic corrected (`concern_constructor.py`)

1. **K⁺ >6.0 + hepatic enzyme ≥5×ULN within_days band:** promote hepatic finding to same-day Tier 0 so both form a same-day co-equal group (`XD-AS-1` / `RE-AS-12`). Generic ≥10×ULN enzyme same-day band must not defeat this ratified cross-domain outcome.
2. **TG >20 + Na 125–129:** elevate sodium to same-day Tier 0 with mandatory pseudohyponatraemia caveat (`XD-ARTEFACT-1` / `XD-AS-7`). Generic Na &lt;125 same-day band must not suppress/downgrade the sodium concern under the artefact rule.
3. **Same-day multi-member lead selection:** all same-day peers become co-leads with empty solo `lead_finding_ids` (no manufactured lead / no arbitrary internal ordering).

### Before / after

| Scenario | Before (incorrect) | After (restored) |
|---|---|---|
| `XD-AS-1` / `RE-AS-12` | K⁺ same_day Tier 0; HEP-F1 within_days Tier 1; not co-equal | Both same_day Tier 0; `same_day_coequal`; no solo lead |
| `XD-AS-7` | CN-F1 same_day Tier 0; RE-F5 within_days Tier 1 + caveat | Both same_day Tier 0; co-equal; caveat retained |

### Full fixture-authority comparison (109 unique)

Compared approval pack v1.2 table rows × fixture estate × implementation outputs.

| Result | Detail |
|---|---|
| Unique scenarios | 109 (110 fixture rows; `CONTRACT-FIX-1` ≡ `HEP-AS-1`) |
| Fixture vs implementation diffs | **NONE** |
| Unauthorised pack vs fixture diffs | **0** |
| Independently accepted corrections retained | `XD-AS-15` (severity mild→moderate); `XD-AS-17` (CN-F3); `XD-AS-25` (HEP-F3 mixed) |
| Pack table-row parse note | `HEP-AS-4` / `HEP-AS-10` / `RE-AS-2` / `RE-AS-11` carry `**(corrected)**` in the ID cell; present in pack §9, matched by implementation/fixtures |

### Post-correction verification

```text
PYTHONPATH=backend python backend/tools/run_clinical_priority_scenarios.py
→ passed: 110, failed: 0  (109 unique; zero skips)

pytest backend/tests/unit/test_clin_priority_cross_domain_corrections.py \
  backend/tests/unit/test_clinical_finding_models.py \
  backend/tests/unit/test_clinical_priority_scenario_runner.py -q
→ 12 passed

SIGNAL_ACTIVATION_BASELINE_TOTAL: 183
SIGNAL_ACTIVATION_PRESERVED_TOTAL: 183
SIGNALS_INTENTIONALLY_RETIRED: 0
```

### Files changed in bounded correction

- `backend/core/analytics/concern_constructor.py`
- `backend/tests/fixtures/clinical_priority_scenarios_v1.json`
- `backend/tools/generate_clinical_priority_fixtures_v2.py`
- `backend/tests/unit/test_clin_priority_cross_domain_corrections.py`
- `docs/architecture/CLIN-PRIORITY-CORE-1_checkpoint2_fixture_authority_notes.md`
- `docs/architecture/CLIN-PRIORITY-CORE-1_START_evidence.md`

### Confirmations (corrections)

- `finish` **not** run  
- No FINISH-phase longitudinal / frontend work  
- No merge  
- No upstream signal activation / Knowledge Bus promotion changes  

## Confirmations

- No Knowledge Bus promotion / activation-register changes for signal retirement  
- No precedence/arbitration/state_engine modifications  
- Amended §3A hierarchy applied; cross-domain ruleset outranks subordinate generic domain bands for `XD-AS-1`/`RE-AS-12`/`XD-AS-7` (see corrected Checkpoint 2 notes)

## Awaiting

Independent review of bounded corrections. Do not self-authorise FINISH.
