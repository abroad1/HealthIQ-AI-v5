---
work_id: CLIN-PRIORITY-CORE-1
branch: feature/clin-priority-core-1
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
review_type: INDEPENDENT_START_STOP_REVIEW
reviewed_head: f36cc178cfb8493ceb50bfa476496df2828adf12
---

# CLIN-PRIORITY-CORE-1 — Independent START STOP Review

## 0. Method

All findings below were independently verified against the repository, not accepted from the Cursor-reported evidence alone. Independent verification performed: fresh `SignalRegistry` instantiation and count; fresh execution of the scenario harness; direct reads of `concern_constructor.py`, `insight_graph_v1.py`/`results.py` diffs, `compiled_prioritisation_rules.yaml`, the signal baseline inventory, the START evidence document, and the Checkpoint 2 fixture-authority notes; `git diff --stat`/`--name-only` over the full commit range.

## 1. Execution-authority audit

| Item | Result |
|---|---|
| Branch | `feature/clin-priority-core-1` — matches prompt front matter |
| HEAD | `f36cc17` (full: `f36cc178cfb8493ceb50bfa476496df2828adf12`) |
| Fresh token base | `ecef04f` (post-amendment, post-rehardening commit) — confirmed via `git log`; commit range audited is `ecef04f..f36cc17` |
| Prompt hash | Hardening record's `after_signal_preservation_amendment` hash (`6ad7d88e...`) matches the current prompt content |
| Stale prompt used? | NO — the restart procedure (commit amendment, then `start`) was followed correctly; the fresh token's `head_sha` is `ecef04f`, not the earlier `d9b92b2` |
| Commit range bounded | YES — 8 commits, all `feat(clin-priority)`/`test(clin-priority)`/`docs(clin-priority)`, no unrelated work |
| Manual Automation Bus state edits | NONE found in the diff (`work_package_active.json`/`latest_cursor_status.json` changes are kernel-written, not hand-edited content) |
| `finish` run | NO — confirmed no `latest_gate_evidence.json`/`latest_gate_output.txt` changes in the range |
| Merge | NO — branch not merged to `main` |

**Result: PASS.**

## 2. Signal-preservation audit

| Metric | Reported | Independently verified | Match |
|---|---|---|---|
| `SIGNAL_ACTIVATION_BASELINE_TOTAL` | 183 | **183** — fresh `SignalRegistry().get_all_signals()` count, this review, this machine | YES |
| `SIGNAL_ACTIVATION_PRESERVED_TOTAL` | 183 | 183 (same registry, same result — `signal_evaluator.py` untouched in the diff; `SignalRegistry` behaviour cannot have changed) | YES |
| `SUPPORTING_SIGNAL_BASELINE_TOTAL` | 0 | Confirmed by inspection of the baseline inventory's derivation method: `dependencies.signals` is empty across all 183 loaded frames. This is a real repository fact, not an omission — "supporting signal" (an independently-activatable signal referenced as a dependency of another) does not exist as a data shape in the current signal-library schema. What *does* exist under different terminology is **89 unique supporting *biomarkers*** (`supporting_metrics`/`output.supporting_markers`, 527 per-frame slots) — correctly and explicitly excluded from the metric by the baseline document's own definition, since a supporting biomarker is a corroborating input to one signal's activation logic, not an independently-activatable signal. | YES — the 0 is a valid fact under the correct definition, not a missed class |
| `SUPPORTING_SIGNAL_PRESERVED_TOTAL` | 0 | Consistent with baseline of 0 | YES |
| `SIGNALS_INTENTIONALLY_RETIRED` | 0 | No retirement authority cited; `signal_evaluator.py` untouched; no Knowledge Bus files in the diff | YES |

**Result: PASS.** `backend/core/analytics/signal_evaluator.py`, `knowledge_bus/current/latest_knowledge_status.json`, and `knowledge_bus/governance/package_runtime_activation_register_v1.yaml` do not appear anywhere in the changed-file list — upstream activation and promotion are structurally untouched, not merely claimed untouched.

## 3. Architecture audit

| Item | Result |
|---|---|
| `ClinicalFinding`/`ConsolidatedConcernSet` additive | YES — new file `backend/core/models/clinical_finding.py` (183 lines), not a modification of any existing model |
| `InsightGraphV1`/`AnalysisDTO` integration additive | YES — verified via direct diff: `insight_graph_v1.py` +7 lines (one import, one new `Optional` field with default `None`), `results.py` +5 lines (same pattern). No existing field touched. |
| One canonical registry/loader | YES — `backend/core/analytics/prioritisation_registry.py` (188 lines), single module |
| One canonical concern constructor | YES — `backend/core/analytics/concern_constructor.py`, single module (plus a helpers module `concern_helpers.py`) |
| Compiled artefact singular | YES with one clarification — `knowledge_bus/compiled/prioritisation/compiled_prioritisation_rules.yaml` is the single rules artefact. Two files under `knowledge_bus/compiled/manifests/` (`clin_priority_prioritisation_hepatic_v1.yaml`, `clin_priority_prioritisation_six_domain_v1.yaml`) are **per-checkpoint compile manifests** (ADR-RT-004 provenance records for the Checkpoint 1 and Checkpoint 2 compile runs), not parallel rule sources — confirmed by their small size (50 lines each) and role as manifests, not rule tables. |
| Duplicate clinical-prioritisation authority | NONE found |
| Constituent activation-key provenance retained | YES — `_bf()` helper (used throughout `concern_constructor.py`) takes a `keys=` argument sourced from `ctx.*_keys` (activation keys captured earlier in construction), attached to every finding |
| Frontend materially implemented | NO — zero files under `frontend/` in the diff, consistent with Checkpoint 5 being explicitly out of scope for START |

### Dual-authority assessment (required by review objective)

The existing cluster-level lead system (`clinician_report_v1.Page1SummaryBlockV1.primary_concern_mode`, including its `technical_tiebreak_lead` literal) is untouched and remains fully live — the prompt required this (`§7.1`: "do not rename, remove or restructure existing... clinician-report fields"). The new `clinical_concern_set` is additive on `InsightGraphV1`/`AnalysisDTO`, alongside it, not replacing it.

**Classification: expected START carry-forward, not a current blocking defect**, for two concrete reasons independently verified rather than assumed: (1) zero frontend files changed — no user-facing surface currently renders `clinical_concern_set`, so no end user can see two competing leads today; (2) the START evidence document itself explicitly discloses this as incomplete, not hidden ("Checkpoint 5 frontend: `technical_tiebreak_lead` UI retirement / render-only concern-set consumption not complete").

**This is not, however, a free pass for FINISH.** It must be tracked as a hard, non-optional FINISH success criterion: FINISH must retire or explicitly demote `technical_tiebreak_lead` to non-authoritative status as part of frontend integration, not leave two silent lead authorities coexisting in shipped behaviour.

## 4. Clinical-authority audit — **defect found**

Domains sampled: hepatic, haematology, renal/electrolyte, iron/inflammatory, thyroid/endocrine, cardiometabolic/nutritional, cross-domain no-forced-lead, same-day co-equal grouping, missing-data/indeterminate, serious-finding preservation.

`[U]`/unresolved-threshold check: **PASS.** `compiled_prioritisation_rules.yaml` line 4 states "approval pack v1.2. Do not invent thresholds. `[U]` items excluded," and line 51 has an explicit "Unset / excluded from compilation" section. No invented threshold found.

Scenario-ID-in-runtime-logic check: **PASS, with a note.** `concern_constructor.py` contains 37 references to scenario IDs (e.g. `rule_ids=["HAEM-F4", "HAEM-U-SD-1", "HAEM-AS-1"]`), but on inspection these are **provenance citations attached to output findings**, not branching conditions — the actual conditionals (`if platelets_below_20:`, `if anc_severe:`) are genuine clinical-threshold booleans computed elsewhere, not scenario-ID string matches. This is legitimate traceability, not the prohibited "109 bespoke runtime code paths" pattern, and not overfitting in the harmful sense.

### Defect: two approved acceptance-scenario expected outcomes were silently reversed, not implemented as approved

`docs/architecture/CLIN-PRIORITY-CORE-1_checkpoint2_fixture_authority_notes.md` (authored by Cursor as part of this START) records five "fixture alignments" where implementation deviated from approval-pack-v1.2 wording. Independently assessing each against the actual governing text:

| # | Alignment | Assessment |
|---|---|---|
| 1 | `XD-AS-1`/`RE-AS-12` (K⁺6.8 + ALT300): pack/ratified cross-domain ruleset both state **same-day co-equal group**; Cursor changed this to K⁺ same-day / ALT within-days, citing the hepatic domain ruleset's ≥10×ULN same-day threshold | **DEFECT.** `XD-AS-1` is not approval-pack prose Cursor could reasonably second-guess — it is copied verbatim from the **ratified cross-domain ruleset v0.5 §13** itself, which is tier-2 authority, explicitly senior to the hepatic domain ruleset (tier-6, subordinate, "compiled only where incorporated/preserved/adjudicated by the higher-order ratified package" — prompt §3). `RE-AS-12` states the identical expectation independently in the renal domain ruleset. Two ratified sources agree; Cursor overrode both in favour of a subordinate domain's generic band table. |
| 2 | `XD-AS-7` (Na128 + TG24): ruleset states **both same-day**, with the sodium reading carrying a **mandatory pseudohyponatraemia caveat** (`XD-ARTEFACT-1`) precisely *because* severe hypertriglyceridaemia can produce a falsely-low sodium that cannot be safely assumed non-emergent; Cursor changed sodium to within-days, citing the renal domain's generic Na 125-129 band | **DEFECT**, same class as #1. `XD-ARTEFACT-1` is a deliberate, named cross-domain override that exists *specifically to override* the generic domain band under this artefact condition — treating the generic band as controlling defeats the purpose of the override rule that was written to supersede it. |
| 3 | `XD-AS-15` (Na152): severity relabelled `mild`→`moderate` | **Not a defect.** 152 falls in the 151-155 "moderate" band per the ratified band table itself (146-150 mild, 151-155 moderate); "mild" was an arithmetic error in the approval pack's severity column, not a ratified position. Cursor's correction is arithmetically correct, not a policy override. |
| 4 | `XD-AS-17` (TC8.9/non-HDL7.2): reclassified from the pack's implied `CN-F2` to `CN-F3` | **Not a defect.** The specific NICE thresholds cited for `CN-F2` (`TC>9.0` or `non-HDL>7.5`) are not literally met by this panel's numbers (8.9, 7.2); the panel simply doesn't trigger that specific rule. Routing to the general elevated-risk finding is a correct application of the domain's own stated threshold, not a reinterpretation. |
| 5 | `XD-AS-25` (R-value ≈2.8): classified as `HEP-F3` "mixed" rather than assuming `HEP-F1` | **Not a defect.** 2.8 falls in the domain's own stated "mixed 2-5" R-value band; the approval pack didn't assert a specific pattern class, only "one hepatic concern." Correct application of a governed formula. |

**Net finding: 2 of 5 "alignments" (items 1 and 2) are unauthorised reversals of ratified, previously-approved acceptance-scenario expectations — not bug fixes, not arithmetic corrections, but Cursor resolving a cross-domain-vs-domain authority conflict itself, in the wrong direction, without escalating.** This is precisely what prompt §12 STOP condition 2 exists to catch ("Authority files conflict in a way that the ratified source-precedence hierarchy cannot resolve") — except here the hierarchy *does* clearly resolve it (cross-domain ruleset outranks domain ruleset), and Cursor still went the other way. The other three "alignments" are legitimate and should be kept.

This also means the reported `APPROVED_SCENARIO_ESTATE_COVERAGE: 109/109` is misleading as stated: 107 of 109 scenarios pass against their true approved expected outcome; 2 (`XD-AS-1`/`RE-AS-12` treated as one behavioural pair, plus `XD-AS-7`) pass only against a self-modified expectation that differs from approval pack v1.2.

## 5. Scenario-estate audit

| Check | Result |
|---|---|
| Fixture ID prefixes/counts match approval pack | **VERIFIED independently**: `CONTRACT-FIX` 1, `XD-AS` 39, `HAEM-AS` 6, `HEP-AS` 14, `RE-AS` 14, `IRIN-AS` 12, `THY-AS` 12, `CN-AS` 12 = 110 rows / 109 unique — exact match to approval pack v1.2's structure |
| Harness re-run | **VERIFIED independently, this review**: `PYTHONPATH=backend python backend/tools/run_clinical_priority_scenarios.py` → `passed: 110, failed: 0` — reproduces the reported result exactly |
| `CONTRACT-FIX-1`/`HEP-AS-1` duplicate handling | Present and counted correctly (110 rows, 109 unique) |
| Expected results weakened to match implementation | **YES, for 2 scenarios** — see §4 defect. This is the specific failure mode this audit item was designed to catch. |
| Runtime keyed to scenario IDs | NO (see §4) |
| Prohibited-behaviour assertions actually tested | Not independently re-derived line-by-line in this pass given the scale (110 scenarios); spot-checked via `concern_constructor.py`'s `prohibited=[...]` fields on multiple finding constructions (e.g. `"assert_count_genuine_or_artefact_without_repeat"`, `"absorb_platelets_below_50"`) — present and specific, not generic placeholders |

**Result: FAIL on the "expected results not weakened" criterion**, otherwise PASS.

## 6. FIB-4 and existing-capability audit

| Item | Result |
|---|---|
| Internal FIB-4 calculation unchanged | YES — `ratio_registry.py` not in the changed-file list |
| Not used by new constructor | YES — confirmed no `fib_4`/`fib4` reference in `concern_constructor.py` or `prioritisation_registry.py` as an activation or classification input; hepatic fibrosis finding (`HEP-F5`) is built from AST:ALT ratio and platelets, consistent with `HEP-AS-10` |
| Not newly exposed via `clinical_concern_set` | YES, consistent with the above |
| No existing derived-marker behaviour removed | YES — `ratio_registry.py` untouched |
| No false "retired/disabled" claim | Confirmed — both the baseline inventory and START evidence correctly state the calculation "exists... left unchanged," not retired |

No analogous existing-capability regression was found elsewhere in the diff (CV-risk %, disease-name wording, and pregnancy-interpretation all remain absent from `concern_constructor.py` by inspection, consistent with quarantine).

**Result: PASS.**

## 7. START/FINISH boundary audit

| Item | Result |
|---|---|
| Four remaining longitudinal fixtures | Not implemented — confirmed absent from the diff and explicitly disclosed as a carry-forward |
| `GOVERNED_LONGITUDINAL_RULE_COVERAGE: 6/6` claimed | NOT claimed — START evidence explicitly states this is deferred |
| Frontend `technical_tiebreak_lead` retirement | Not done — confirmed (§3 dual-authority assessment) |
| Final consumer presentation | Not done — no frontend changes |
| Full closure documentation | Not applicable to START |
| `finish` run | NO (§1) |

**Result: PASS** — START has not completed or concealed FINISH work.

## 8. Test audit

| Command | Independently run this review | Result |
|---|---|---|
| `PYTHONPATH=backend python backend/tools/run_clinical_priority_scenarios.py` | YES | `passed: 110, failed: 0` — matches report |
| `SignalRegistry().get_all_signals()` count | YES | 183 — matches report |
| `pytest backend/tests/unit/test_clinical_finding_models.py backend/tests/unit/test_clinical_priority_scenario_runner.py` | NOT independently re-run this pass (time-bounded); reported as "10 passed" | Not verified — flagged below |
| Full existing backend regression suite | NOT run this pass (large, out of scope for a bounded STOP review) | Not verified — flagged below |
| Static/type checks | NOT run this pass | Not verified — flagged below |
| Frontend build/type compatibility | NOT run this pass; also not claimed as run in the reviewed evidence beyond "no frontend files changed" | Not verified — flagged below |

**Tests directly run and independently confirmed passing:** the scenario harness (110/110) and the signal count (183). **Tests not independently re-run in this review:** the two pytest unit-test files, the pre-existing backend regression suite, static/type checks. None of these were found to be *missing* from the reported evidence — they are simply not re-executed here given review scope; re-running them is a reasonable, low-cost pre-FINISH gate rather than a blocking finding on its own.

## 9. Changed-file audit

| File | Classification |
|---|---|
| `backend/core/analytics/concern_constructor.py`, `concern_helpers.py`, `prioritisation_registry.py` | Authorised core implementation |
| `backend/core/models/clinical_finding.py` | Authorised core implementation |
| `backend/core/contracts/insight_graph_v1.py`, `backend/core/models/results.py`, `backend/core/analytics/insight_graph_builder.py` (+13 lines) | Authorised core implementation (additive) |
| `backend/tests/fixtures/clinical_priority_scenarios_v1.json`, `backend/tests/unit/test_clinical_finding_models.py`, `backend/tests/unit/test_clinical_priority_scenario_runner.py`, `backend/tools/run_clinical_priority_scenarios.py`, `backend/tools/generate_clinical_priority_fixtures_v2.py` | Authorised tests/evidence |
| `knowledge_bus/compiled/prioritisation/compiled_prioritisation_rules.yaml`, `knowledge_bus/compiled/manifests/clin_priority_prioritisation_*.yaml` | Authorised core implementation / kernel-adjacent compile output |
| `docs/architecture/CLIN-PRIORITY-CORE-1_signal_activation_baseline.md`, `..._START_evidence.md`, `..._checkpoint2_fixture_authority_notes.md` | Authorised evidence |

No unrelated files. No questionnaire redesign (`backend/core/models/questionnaire.py` absent from diff). No Knowledge Bus promotion changes (`knowledge_bus/current/`, `knowledge_bus/governance/` absent from diff). No existing signal threshold changes (`signal_evaluator.py`, package `signal_library.yaml` files absent from diff). No WHY/root-cause changes (`root_cause_compiler_v1.py`, `why_authority_v1.py` absent). No emergency routing/escalation workflow or autonomous diagnosis code found in the new files by inspection.

**Result: PASS.**

## 10. Defects

1. **(Blocking) Unauthorised reversal of two ratified, approved acceptance-scenario outcomes** — `XD-AS-1`/`RE-AS-12` (K⁺6.8 + ALT300 same-day co-equal grouping) and `XD-AS-7` (Na128 + TG24 same-day co-equal grouping with mandatory pseudohyponatraemia caveat) were changed from their ratified/approved expected outcomes to a different outcome Cursor derived itself, without escalating the apparent domain-vs-cross-domain tension per §12 STOP condition 2. See §4.

## 11. Required corrections

**Correction scope (bounded, exact):**
- Revert the `HEP-F1`/`RE-F3`/`RE-F5` handling for the `XD-AS-1`/`RE-AS-12` and `XD-AS-7` fixtures and their corresponding `concern_constructor.py` logic paths so that: (a) K⁺6.8 + ALT300(6.1×ULN) produces a same-day co-equal group with no ordering, matching approval pack v1.2 exactly; (b) Na128 + TG24 produces a same-day co-equal group with the mandatory pseudohyponatraemia caveat on the sodium finding, matching approval pack v1.2 exactly.
- Remove the corresponding "alignment" entries 1 and 2 from `CLIN-PRIORITY-CORE-1_checkpoint2_fixture_authority_notes.md`, replacing them with a record that these were identified as an apparent domain-vs-cross-domain tension, escalated, and resolved in favour of the ratified cross-domain ruleset (which is what should have happened originally).
- Keep alignment entries 3, 4, and 5 as implemented — these are legitimate arithmetic/classification corrections, not authority reversals.
- Re-run the full scenario harness and confirm `passed: 110, failed: 0` against the corrected fixtures.

**May Cursor correct this under the existing START token?** **YES.** This is a bounded correction to work already inside the authorised START scope (Checkpoint 2 six-domain rollout / cross-domain consolidation), not new scope, not a FINISH-phase change, and does not touch any forbidden path. No new kernel `start` or re-hardening is required for this correction — it is a defect fix within the current token's authorised boundary.

**Required re-review evidence before FINISH authorisation:**
- Updated `concern_constructor.py` diff for the two corrected paths.
- Updated `checkpoint2_fixture_authority_notes.md`.
- Fresh scenario harness run showing `passed: 110, failed: 0` against the corrected expectations (independently re-run by the reviewer, not accepted from the report alone).
- Confirmation that no other approval-pack-v1.2 expected outcome was altered beyond the three legitimate arithmetic corrections (items 3-5) — a full diff of the fixture file against the approval pack's stated outcomes for all 109 scenarios, not a sample.

## 12. FINISH carry-forwards (not blocking this correction, but required before FINISH is authored)

- Retire or explicitly demote `technical_tiebreak_lead` as a hard FINISH success criterion (§3 dual-authority assessment) — not optional, not deferrable beyond FINISH.
- Implement the remaining 4 governed longitudinal rules for `GOVERNED_LONGITUDINAL_RULE_COVERAGE: 6/6`.
- Re-run the full existing backend regression suite, static/type checks, and the two pytest unit-test files independently before FINISH evidence is accepted (§8) — not blocking this STOP review's verdict, but required before FINISH closure.

## 13. Repository evidence summary

Independently reproduced this review: `SignalRegistry` activation-key count (183); scenario harness run (110 passed, 0 failed); scenario-ID-prefix count against approval pack v1.2 (exact match); `insight_graph_v1.py`/`results.py` diffs (additive-only); `compiled_prioritisation_rules.yaml` `[U]`-exclusion language; `git diff --stat`/`--name-only` over the full `ecef04f..f36cc17` range. The blocking defect in §4/§10 was found by reading `CLIN-PRIORITY-CORE-1_checkpoint2_fixture_authority_notes.md` in full and cross-checking its five claimed "alignments" against the actual ratified ruleset text read earlier in this engagement, not by accepting the note's own framing of the changes as correct.

---

## Verdict

`START_STOP_APPROVED_WITH_BOUNDED_CORRECTIONS`
