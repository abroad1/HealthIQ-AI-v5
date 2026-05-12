# LC-S5 — Launch-core proving readiness preflight audit

**Audit ID:** `LC-S5-LAUNCH-CORE-PROVING-AND-HUMAN-VALIDATION` — pre-sprint preflight  
**Date:** 2026-05-12  
**Auditor:** Claude Code — read-only audit / investigation mode  
**Evidence standard:** Every factual claim cites file path and line number. Nothing inferred from memory or conversational summary.

---

## 1. Executive Summary

Sprints LC-S1 through LC-S4, WP2, WP3, and LC-OBS2 are all merged and confirmed complete. The governed analytical pipeline and frontend report carriage are in a materially improved state. The following critical items have been resolved since the WP2 proving run:

- `body_overview` is now rendered — `frontend/app/(app)/results/page.tsx:668–672`
- `NarrativeRetailSummaryCard` is now wired in a visible position — `results/page.tsx:632`
- Mock-mode honesty banner is implemented — `results/page.tsx:610–614`
- Legacy `insights[]` are gated from consumer paths (actions hub and results page) — `actions/page.tsx:60`, `results/page.tsx:218`
- Statin consumer copy is consumer-readable — `intervention_annotation_formatter_v1.py:66–69`
- Clinician synthesis markdown tokens stripped — `ClinicianReportRenderer.tsx:110–116`
- "What this means" defaults open — `results/page.tsx:666`
- `statin_signal_isolation` promoted to Sentinel — `sentinel/packs/escaped_defects_v1.json:73–82`

**The one non-negotiable sprint prerequisite** is that the proving fingerprints are stale. The current `latest_fingerprints.json` is stamped at git SHA `48efd2e` — that is the WP2 era, six commits before LC-S3, WP3, and LC-S4. Sprint 5's first step must be running the proving harness fresh to generate post-LC-S4 fingerprints.

**CHECKs 2/4/5/6** are partially addressed by LC-S4 but not yet fully automated as binary harness checks. Sprint 5 should encode the remaining binary checks and execute a human validation walkthrough.

**Sprint 5 readiness verdict:** READY TO AUTHOR. No blocking gaps. Proving harness must be run first. Scope is tests, harness additions, and human validation — no analytical engine work required.

---

## 2. Sprint 5 Readiness Verdict

| Condition | Status | Evidence |
|---|---|---|
| LC-S1 analytical hardening complete and merged | ✓ | `docs/sprints/LC-S1_analytical_hardening_completion_2026-05.md` |
| LC-S2 statin/context integration complete and merged | ✓ | `docs/sprints/LC-S2_context_integration_completion_2026-05.md` |
| WP2 Layer B → Layer C contract closure complete | ✓ | ADR `docs/architecture/ADR_WP2_layer_b_layer_c_contract_path_b.md` |
| LC-S3 narrative payload implementation complete | ✓ | `docs/sprints/LC-S3_layer_c_payload_implementation_completion_2026-05.md` |
| WP3 questionnaire rationalisation complete | ✓ | `docs/sprints/WP3_questionnaire_rationalisation_completion_2026-05.md` |
| LC-S4 report carriage complete | ✓ | `docs/sprints/LC-S4_launch_core_report_carriage_completion_2026-05.md` |
| LC-S4 Sentinel promotion (`statin_signal_isolation`) complete | ✓ | `sentinel/packs/escaped_defects_v1.json:73–82` |
| Proving fingerprints current (post-LC-S4) | ✗ STALE | `latest_fingerprints.json` SHA `48efd2e`; HEAD is `2247d98` |
| CHECKs 2/4/5/6 fully automated as binary harness checks | ✗ PARTIAL | CHECK 4 partially covered by Jest; CHECKs 2/5/6 not automated |
| Human validation walkthrough executed | ✗ NOT DONE | Awaiting Sprint 5 |

---

## 3. Current Proving Harness State

**File:** `backend/tools/launch_core_proving_harness.py`

The harness is intact and runnable. It:

- Reads `backend/tests/fixtures/proving/launch_core_matrix.json` (`launch_core_matrix.json:1–37`) for panel paths (AB, VR) and four scenario definitions
- Calls `run_golden_panel` for each (panel × scenario) combination, entirely in the backend — no frontend dependency
- Produces fingerprints covering: `status`, `top_finding_signal_ids`, `signal_state_by_id`, `consumer_band_labels`, `narrative` heads, `clinician_page1`, `idl`, `intervention`
- Writes markdown `PROVING_REPORT.md` and `latest_fingerprints.json` under `docs/audit-papers/launch-core-proving/`
- Computes invariant checks inline: statin-off vs statin-on analytical invariants, lifestyle payoff

**Post-LC-S4/WP3 compatibility assessment:**

The harness imports `compile_clinician_report_v1`, `InterventionAnnotationsV1`, and `run_golden_panel` — all unchanged by LC-S4 (LC-S4 touched the frontend and one formatter module only) and WP3 (which added questionnaire mapper fields not consumed by the harness). The harness should run without modification. However, a fresh run is required to confirm this and regenerate the fingerprints.

**Scenarios currently represented:**

| Panel | Scenario | Lifestyle fixture | Questionnaire data |
|---|---|---|---|
| AB | `baseline` | None | None |
| AB | `lifestyle_context` | `tests/fixtures/lifestyle_minimal.json` | None |
| AB | `statin_off` | None | `long_term_medications: ["None"]` |
| AB | `statin_on` | None | `long_term_medications: ["Statins (cholesterol medication)"]` |
| VR | `baseline` | None | None |
| VR | `lifestyle_context` | `tests/fixtures/lifestyle_minimal.json` | None |
| VR | `statin_off` | None | `long_term_medications: ["None"]` |
| VR | `statin_on` | None | `long_term_medications: ["Statins (cholesterol medication)"]` |

Source: `backend/tests/fixtures/proving/launch_core_matrix.json:1–37`

All four scenario types from the proving requirement are present: AB/VR baseline, lifestyle/context, statin-off, statin-on. The matrix has not been modified since WP2.

---

## 4. Current Proving Artefact Freshness

| Artefact | Status | Evidence |
|---|---|---|
| `docs/audit-papers/launch-core-proving/latest_fingerprints.json` | **STALE** — SHA `48efd2e` (WP2 era) | `latest_fingerprints.json:2` |
| `docs/audit-papers/launch-core-proving/PROVING_REPORT.md` | **STALE** — same WP2 run | `PROVING_REPORT.md:3` (`proving-wp2-layer-bc-closure`) |
| Artifact subdirectory | `artifacts/proving-wp2-layer-bc-closure/` | Named for WP2; no LC-S3/WP3/LC-S4 runs present |

**Current HEAD:** `2247d98` (git log, 2026-05-12)  
**Fingerprint SHA:** `48efd2e` — pre-LC-S3 (`1130c94`), pre-WP3 (`518f41f`), pre-LC-S4 (`c2c469b`), pre-statin Sentinel (`2247d98`)

The proving fingerprints are now **six commits stale**. Post-LC-S3, the narrative compiler was rewritten. Post-LC-S4, the statin consumer formatter changed. Post-WP3, questionnaire data shapes changed. The fingerprints do not reflect any of these changes.

**Sprint 5 first action (mandatory):** Run `python backend/tools/launch_core_proving_harness.py` from repo root to regenerate fingerprints against current main. Inspect the output for any regressions against the WP2 fingerprints before authoring CHECK automations.

**Known fingerprint gap (pre-existing, not new):** `PROVING_REPORT.md:35` shows `IDL enabled patterns: 4 titles=['', '', '', '']` for AB runs — the title strings are empty. This was true in the WP2 run and indicates the `pattern_title`/`title`/`headline` fields in IDL records are empty strings in the fingerprint JSON, not that IDL is broken. The IDL section of the harness reports count but not readable titles. This is a harness display limitation, not an analytical gap.

---

## 5. Remaining CHECK 2/4/5/6 Assessment

### CHECK 2 — Alcohol bridge appears in human language in `lead_narrative`

**Data-contract status:** The alcohol bridge is deterministically assembled. `_bridge_lines()` in `backend/core/analytics/narrative_report_compiler_v1.py` reads `meta.lifestyle_interpretation_bridges_v1` for `alcohol_methylation_macrocytosis` and merges bridge text into `lead_text`, which flows into `lead_narrative` via the LC-S3 assembly module.

**Frontend visibility after LC-S4:** `lead_narrative` is now rendered inside "What this means" (`results/page.tsx:682`), which now defaults open (`results/page.tsx:666` has `defaultOpen`). The bridge is visible without user interaction when a lifestyle fixture with alcohol data is active.

**Automated coverage:** None. The lifestyle_context scenario in the proving harness does inject a lifestyle fixture (`tests/fixtures/lifestyle_minimal.json`), but the harness does not assert the text of `lead_narrative`. There is no binary check confirming the bridge phrase appears in human language.

**Recommendation for Sprint 5:** Add a binary harness check asserting that `AB__lifestyle_context.narrative.lead_narrative_head` contains recognisable alcohol/lifestyle context language when the fixture includes relevant alcohol values. This requires either (a) adding the check to `launch_core_proving_harness.py` or (b) a new pytest module in `backend/tests/unit/` or `backend/tests/integration/`. After confirming current text content from a fresh harness run, encode as a substring assertion.

**Manual / human validation:** Also required — a reviewer should open the lifestyle_context run report and confirm the bridge reads naturally.

### CHECK 4 — No `legacy_v1` manifest entries visible on consumer path

**Current automated coverage:**
- `frontend/tests/lib/legacyInsightsVisibility.test.ts` — tests `filterConsumerInsights`, `isLegacyV1Insight`, `legacyInsightsDebugEnabled` (confirmed file exists, imported in `results/page.tsx:46`)
- `frontend/tests/lib/lcS4ResultsCopy.test.ts` — tests mock-mode disclosure string
- `frontend/tests/components/DeterministicNarrativeSurface.lc-s4.test.tsx` and related LC-S4 test suites — 7 suites, 19 tests (per `LC-S4_launch_core_report_carriage_completion_2026-05.md:52–54`)

**Code confirmation:**
- Actions hub: `actions/page.tsx:60` — `buildActionCardModels(data.clusters || [], data.recommendations, { maxItems: 8 })` — NO `insights` param. CLEAN.
- Results page: `results/page.tsx:210–216` — `buildActionCardModels(clusters, currentAnalysis?.recommendations, { maxItems: 5 })` — NO `insights` param. CLEAN.
- Results page InsightsPanel: `results/page.tsx:836–841` — gated behind `showInsightsPanelSection` where `showInsightsPanelSection = legacyInsightsDebugEnabled() || consumerInsights.length > 0` (`results/page.tsx:218`). On standard path, `consumerInsights = filterConsumerInsights(insights)` returns `[]` (all are legacy_v1). Panel is hidden. CLEAN.
- Advanced section alert: `results/page.tsx:798–806` — gated behind `consumerInsights.length > 0`. Hidden on standard path. CLEAN.

**Not in Sentinel pack:** The defect class is not promoted to `sentinel/packs/escaped_defects_v1.json`. The LC-S4 completion note (`LC-S4_launch_core_report_carriage_completion_2026-05.md:75–82`) lists this as a Sentinel carry-forward item.

**Recommendation for Sprint 5:** CHECK 4 is satisfied at the code level. The Jest tests cover the filtering logic. Sprint 5 should either (a) promote a backend-verifiable CHECK 4 test to Sentinel, or (b) note that CHECK 4 is covered by Jest and is a frontend-Sentinel-infrastructure gap (deferred). The human validation walkthrough should confirm no legacy_v1 content appears in the rendered actions list.

### CHECK 5 — No band/headline contradiction

**Current automated coverage:** `sentinel/packs/escaped_defects_v1.json` lists `wave1_contradiction` with `guard_type: "status_reporting"` and `status: "PLACEHOLDER"` (`escaped_defects_v1.json:33–39`). The test file `backend/tests/regression/test_wave1_contradiction_status.py` exists and is in the Sentinel runner (`sentinel_runner.py:52`) but reports status only — it does not assert absence of contradiction.

**Code-level check:** The Wave1 domain card sentence templates use governed copy (`domain_score_assembler.py`); the `headline_cv_coherent()` function selects copy based on band. There is no cross-section assertion that the IDL severity tone, domain band label, and headline sentence polarity are mutually consistent.

**Recommendation for Sprint 5:** Add a binary check to the proving harness or a pytest module that asserts, for each domain card row in the AB and VR fingerprints, that the `band_label` and `consequence_sentence_head` do not contradict (e.g., a `"stable"` band does not produce a sentence indicating danger; a `"strong"` band does not produce a sentence indicating safety). This can be implemented as a substring/tone check on the fingerprint output. Also promote `wave1_contradiction` from PLACEHOLDER to GUARDED in the Sentinel pack once the test asserts rather than just reporting.

**Manual review:** Required — a human tester should review each domain card band ↔ headline pair on both AB and VR runs.

### CHECK 6 — Clinician `primary_concern` and `retail_summary` reference the same lead pattern

**Current automated coverage:** None. The proving harness fingerprint captures `clinician_page1.primary_concern_head` and `narrative.retail_summary_head` for each run. In the WP2 fingerprints (stale), both reference "Methylation pathway pattern" / "Homocysteine Elevation Context" on AB runs — they do align. But this is not asserted by any test.

**Frontend visibility after LC-S4:** `NarrativeRetailSummaryCard` is now always visible (`results/page.tsx:632`) regardless of IDL presence, so the coherence check is now testable from the consumer surface for the first time.

**Recommendation for Sprint 5:** After a fresh harness run, add a binary assertion comparing the lead signal name in `clinician_page1.primary_concern_head` with the lead pattern named in `narrative.retail_summary_head`. Both should reference the same lead (e.g., both say "Homocysteine" on AB, same lead on VR). This is a post-harness-run addition requiring the fingerprint text to be read and encoded.

---

## 6. Human Validation Flow Assessment

### Questionnaire flow

WP3 produced a 38-question SSOT (`backend/ssot/questionnaire.json`) with 9 mandatory questions: `alcohol_drinks_weekly`, `biological_sex`, `date_of_birth`, `height`, `long_term_medications`, `sleep_hours_nightly`, `tobacco_use`, `waist_circumference`, `weight` (`WP3_questionnaire_rationalisation_completion_2026-05.md:52`).

The `QuestionnaireForm` component is embedded in the upload page (`upload/page.tsx:8` imports it). There is no separate `/questionnaire` route — the questionnaire is part of the upload flow. This is the expected single-page upload + questionnaire experience.

For statin proving: `long_term_medications` with `"Statins (cholesterol medication)"` is confirmed as the exact SSOT option label (`launch_core_matrix.json:30`). A human tester can select this during upload.

**The 9 mandatory questions are sufficient** for the statin and alcohol proving paths. The statin path needs only `long_term_medications`; the alcohol path needs `alcohol_drinks_weekly`.

### Upload journey

Upload page (`upload/page.tsx`) contains file drop, paste input, parsed table review, and questionnaire — all in one flow. After upload, the tester proceeds to `/results`.

### Results page surfaces

After LC-S4, the following are now visible without user interaction:
- Mock-mode honesty banner (when LLM is off — true in all current runs)
- `NarrativeRetailSummaryCard` — always-visible retail summary
- "What this means" section (now `defaultOpen`) containing: `ResultsBodyOverview`, investigation spine, IDL patterns, system understanding, lead narrative, next steps

A human tester can realistically run AB/VR proving through the app. The constraint is that the tester must provide real blood data whose values match the AB or VR panel profile, or the app must support fixture injection for proving purposes. The proving harness bypasses this by using panel fixture files directly — human testing uses real upload.

**Actions page:** Clean — no legacy recommendations surfacing.

### What must be captured during human testing

1. Screenshot of mock-mode honesty banner appearing before the hero
2. Confirmation that `NarrativeRetailSummaryCard` (retail summary) appears below the hero
3. Confirmation that "What this means" is open by default
4. Confirmation that `body_overview` text is visible within "What this means" (cross-system posture)
5. On a statin-on run: confirmation that statin context language appears in the cardiovascular domain card (consequence sentence) and in `body_overview`
6. On a lifestyle-context run: confirmation that alcohol bridge language appears in the lead narrative section
7. Confirmation that the Actions hub shows no generic/legacy recommendation cards
8. CHECK 5 confirmation: review each domain card band label vs the displayed headline sentence (no contradiction)
9. CHECK 6 confirmation: verify the retail summary card and the clinician primary concern (in advanced section) both name the same lead pattern

---

## 7. Report Carriage Verification after LC-S4

All five `NarrativeReportV1` fields assessed. Evidence from `frontend/app/(app)/results/page.tsx`.

### `body_overview`

**Status: CONFIRMED RENDERED.**  
`ResultsBodyOverview` is imported at `results/page.tsx:27` and rendered at lines 668–672 with `compiledBodyOverview={narrativeReport?.body_overview}` as first child inside "What this means". Statin appendix text from `format_intervention_annotation_narrative_appendix_v1()` flows into `body_overview` on statin-on runs and is now visible.

### `retail_summary`

**Status: CONFIRMED RENDERED (always-visible position).**  
`NarrativeRetailSummaryCard` is imported at `results/page.tsx:25` and rendered at line 632, outside any disclosure — directly after `ResultsPrimaryHero` and before driving signals. Always visible regardless of IDL presence. This resolves the critical IDL-bypass gap from the LC-S4 readiness audit.

### `lead_narrative`

**Status: CONFIRMED RENDERED (now visible by default).**  
`NarrativeLeadAndSupportingSections` renders `lead_narrative` at `results/page.tsx:682`. The enclosing "What this means" disclosure is `defaultOpen` at line 666. Lead narrative is visible without user interaction. Alcohol/lifestyle bridges in `lead_narrative` are visible by default.

### `next_steps_narrative`

**Status: CONFIRMED RENDERED (now visible by default).**  
`NarrativeLongitudinalAndNextSteps` at `results/page.tsx:683` renders `next_steps_narrative`. Same defaultOpen status.

### Mock-mode honesty banner

**Status: CONFIRMED IMPLEMENTED.**  
Lines 610–614: `{narrativeRuntime?.synthesizer_allow_llm_resolved === false ? <Alert ...>{LC_S4_MOCK_MODE_HONESTY_DISCLOSURE}</Alert> : null}`. Banner appears before `ResultsPrimaryHero`. Copy sourced from `lib/lcS4ResultsCopy.ts` (single source of truth).

### Legacy `insights[]` gating

**Status: CONFIRMED GATED.**
- Actions hub (`actions/page.tsx:60`): `buildActionCardModels` called without `insights` param.
- Results page (`results/page.tsx:210–216`): `buildActionCardModels` called without `insights` param.
- Results InsightsPanel (`results/page.tsx:836–841`): gated behind `showInsightsPanelSection` which requires `legacyInsightsDebugEnabled() || consumerInsights.length > 0`. On standard path, `consumerInsights = []` (all filtered by `filterConsumerInsights`). Panel hidden.
- Advanced alert (`results/page.tsx:798–806`): gated behind `consumerInsights.length > 0`. Hidden on standard path.

### Clinician synthesis markdown cleanup

**Status: CONFIRMED IMPLEMENTED.**  
`ClinicianReportRenderer.tsx:110–116` defines `stripSimpleMarkdownDecorators()` which strips `**...**`, `*...*`, and backtick spans. Applied at line 134: `const synthesis = stripSimpleMarkdownDecorators((deterministicClinicianSynthesis ?? '').trim())`.

### Statin consumer wording

**Status: CONFIRMED IMPROVED.**  
`backend/core/analytics/intervention_annotation_formatter_v1.py:66–69`: `format_intervention_annotation_consumer_cv_suffix_v1()` now returns: "Statin medication noted — this may help explain lower LDL-related readings on this panel. Taken from your questionnaire as context only; it does not change how signals are scored or ranked." Consumer-readable, no internal API language.

### "What this means" defaults open

**Status: CONFIRMED.**  
`results/page.tsx:666`: `<ResultsDisclosureSection title="What this means" ... defaultOpen>`. The `defaultOpen` prop (no value) defaults to `true` in the Radix Disclosure component.

### Render gaps remaining after LC-S4

None of the critical gaps from the LC-S4 readiness audit remain open. The following are acceptable non-gaps:
- `longitudinal_narrative`: Always empty string from backend by design. Correctly guarded in UI.
- `secondary_systems`: Always empty string from backend by design. Correctly guarded in UI.

**IDL titles in proving fingerprints:** `PROVING_REPORT.md:35` shows `IDL enabled patterns: 4 titles=['', '', '', '']`. This is a pre-existing fingerprint display gap (empty title fields in IDL record JSON), not a rendering gap. Not introduced by LC-S4.

---

## 8. Sentinel Status

### `statin_signal_isolation`

**Status: GUARDED.** Present in `sentinel/packs/escaped_defects_v1.json:73–82` with `guard_type: "active_deterministic"` and `status: "GUARDED"`. Test file `backend/tests/regression/test_lc_s4_statin_signal_isolation_regression.py` is in the sentinel runner map (`sentinel_runner.py:63–65`). The Sentinel promotion from LC-S4 is complete.

### Full Sentinel pack status (as of 2026-05-12)

| Defect class | Guard type | Status | Test file |
|---|---|---|---|
| `ggt_alias_miss` | active_deterministic | GUARDED | `test_ggt_alias_regression.py` |
| `bilirubin_canonical_mismatch` | active_deterministic | GUARDED | `test_bilirubin_alias_regression.py` |
| `slug_leakage` | active_deterministic | GUARDED | `test_slug_leakage_regression.py` |
| `wave1_contradiction` | status_reporting | **PLACEHOLDER** | `test_wave1_contradiction_status.py` |
| `persisted_result_replay` | status_reporting | **PLACEHOLDER** | `test_persisted_result_replay_status.py` |
| `narrative_compiler_why_surface` | active_deterministic | GUARDED | `test_narrative_compiler_why_surface_regression.py` |
| `questionnaire_exercise_unknown` | active_deterministic | GUARDED | `test_obs2_questionnaire_exercise_unknown_regression.py` |
| `narrative_payload_assembly` | active_deterministic | GUARDED | `test_narrative_payload_compiler_regression.py` |
| `statin_signal_isolation` | active_deterministic | GUARDED | `test_lc_s4_statin_signal_isolation_regression.py` |

Source: `sentinel/packs/escaped_defects_v1.json:1–83`

### Runner gap: `alias_sweep`

`sentinel_runner.py:52` lists `alias_sweep` as a defect class mapped to `backend/tests/regression/test_alias_canonical_sweep.py`, but `alias_sweep` does **not** appear in `escaped_defects_v1.json`. This is a minor drift — the runner knows about it but the pack does not. Not introduced by LC-S4; pre-existing.

### Frontend Sentinel infrastructure

The Sentinel runner (`sentinel_runner.py`) executes pytest only. Jest-based frontend tests (covering IDL clinical_only gate, legacy insights gating, mock-mode honesty) cannot run through the current Sentinel. The LC-S4 completion note explicitly lists these as Sentinel carry-forward items (`LC-S4_launch_core_report_carriage_completion_2026-05.md:75–82`). **Sprint 5 should not implement frontend Sentinel infrastructure** — that is a separate package per the carry-forward classification.

### Sprint 5 Sentinel recommendation

Sprint 5 may promote `wave1_contradiction` from PLACEHOLDER to GUARDED if the new proving harness CHECK 5 binary check is added and confirmed passing. This is optional, not required. Do not touch frontend Sentinel infrastructure in Sprint 5.

---

## 9. Recommended Sprint 5 Scope

### Recommendation: C — Combined automated proving + human validation

Sprint 5 should be a single package combining:

1. **Proving harness run** (mandatory pre-step, not a code change): Execute `python backend/tools/launch_core_proving_harness.py` from repo root to regenerate `docs/audit-papers/launch-core-proving/PROVING_REPORT.md` and `latest_fingerprints.json` against current main. Confirm no regressions vs WP2 fingerprints.

2. **Binary harness checks** (new code, BEHAVIOUR/CONTENT MIXED): Add CHECK 2, 5, and 6 as explicit assertions — either inside `launch_core_proving_harness.py` or as a new pytest file in `backend/tests/`. These are read-only analytical checks against the fingerprint output. No product code changes.

3. **`wave1_contradiction` graduation** (Sentinel pack update only): If CHECK 5 binary test is added and confirmed green, update `sentinel/packs/escaped_defects_v1.json` to promote `wave1_contradiction` from PLACEHOLDER to GUARDED. Link the new test file.

4. **Human validation walkthrough** (non-code): Execute a human walkthrough session using the checklist below (§11). Document the walkthrough results as a completiong note under `docs/sprints/`.

5. **Sprint 5 completion note**: Author `docs/sprints/LC-S5_proving_and_human_validation_completion_2026-05.md` confirming all checks passed.

### Not recommended: Split into two packages

Splitting adds Automation Bus overhead (two kernel runs, two gate passes) for work that can safely be sequenced within one sprint. The harness check additions are small (one file or a new pytest module) and do not warrant a separate bus lifecycle. The human walkthrough can be documented as part of the same sprint completion.

---

## 10. Recommended Sprint 5 Tests/Checks

| Check | Type | File | What to assert |
|---|---|---|---|
| CHECK 2 — alcohol bridge in lead_narrative | Proving harness binary check or pytest | New: `backend/tests/unit/test_lc_s5_proving_checks.py` | `AB__lifestyle_context` `lead_narrative_head` contains alcohol/methylation context language (substring match against known bridge phrase from a fresh harness run) |
| CHECK 5 — no band/headline contradiction | Proving harness binary check or pytest | New: `backend/tests/unit/test_lc_s5_proving_checks.py` | For each consumer domain row in AB and VR fingerprints: `band_label == "stable"` → `consequence_sentence_head` does not contain danger/emergency language; `band_label == "strong"` → sentence is not falsely reassuring |
| CHECK 6 — primary_concern ↔ retail_summary same lead | Proving harness binary check or pytest | New: `backend/tests/unit/test_lc_s5_proving_checks.py` | `clinician_page1.primary_concern_head` and `narrative.retail_summary_head` for AB and VR baselines both reference the same lead pattern name (e.g., both contain "Homocysteine" on AB) |
| CHECK 4 backend guard | Pytest | Existing frontend Jest; backend-side: verify `filterConsumerInsights([{manifest_id:"legacy_v1"}])` returns empty | Promote to Sentinel pack after verifying no regression (optional) |
| `wave1_contradiction` graduation | Sentinel pack update | `sentinel/packs/escaped_defects_v1.json` | Update status from PLACEHOLDER to GUARDED; link new CHECK 5 test as test_file |

All new tests should be under `@pytest.mark.regression` and a new `@pytest.mark.proving` mark for clarity.

---

## 11. Human Validation Checklist Proposal

Execute on a real browser session using a panel that produces AB-like or VR-like output, or using the proving harness output as reference context.

### Pre-walkthrough setup

- [ ] Fresh proving harness run completed; PROVING_REPORT.md regenerated
- [ ] All backend regression tests passing (pytest --m regression)
- [ ] Browser session: logged-in user account
- [ ] Ready to upload a blood test file with at least the mandatory 9 questionnaire answers

### Upload and questionnaire

- [ ] Upload a blood panel (PDF or text paste)
- [ ] Complete the 9 mandatory questionnaire fields including at minimum: sex, DOB, height, weight, alcohol, sleep, tobacco, waist, medications
- [ ] For statin run: select "Statins (cholesterol medication)" in `long_term_medications`
- [ ] For alcohol run: enter a non-zero value for `alcohol_drinks_weekly` (minimum: 7 drinks/week to trigger methylation bridge)
- [ ] Confirm analysis completes without error

### Results page — primary consumer view

- [ ] Mock-mode honesty banner is visible before the hero card
- [ ] Banner wording is exactly: "Your report is built from governed clinical rules applied to your lab data. AI-personalised narrative is not active in this view."
- [ ] Hero card displays a phenotype label (not a backend slug or internal identifier)
- [ ] `NarrativeRetailSummaryCard` (retail summary paragraph) is visible below the hero, before driving signals
- [ ] Driving signals section shows recognisable biomarker names (no `signal_*` slugs)
- [ ] Wave 1 domain cards are present

### "What this means" section

- [ ] Section is OPEN by default (no click required)
- [ ] `body_overview` text is visible at the top of the section (cross-system posture paragraph)
- [ ] On statin-on run: statin context language appears in `body_overview` (e.g., "Statin medication noted" or similar)
- [ ] On alcohol run: alcohol/methylation bridge language appears in lead narrative text (e.g., reference to alcohol intake or macrocytosis in context of methylation pattern)
- [ ] CHECK 5: for each visible domain card, band label and headline sentence are mutually consistent (no contradiction)
- [ ] CHECK 6: the retail summary card and the "primary finding" language in the clinician section (advanced) both name the same lead pattern

### Actions page

- [ ] No generic "Recommended actions" from legacy_v1 insights appearing
- [ ] Action cards are sourced from clusters or panel recommendations only
- [ ] No internal identifiers or API-style strings visible in action card text

### Advanced section

- [ ] Clinician synthesis is visible in the advanced section (collapsed by default)
- [ ] No `**bold**` or `*italic*` markdown tokens visible in rendered text (stripped correctly)
- [ ] InsightsPanel "Narrative summaries" section is NOT visible (legacy insights gated)
- [ ] No "N short narrative summaries available" alert visible in advanced section

### Non-goals for human walkthrough

- Do not test PDF export correctness (separate scope)
- Do not test paywall or pricing gate (separate scope)
- Do not test Gemini/LLM activation (not activated)

---

## 12. Risk Classification

**Sprint 5 change_type: CONTENT + BEHAVIOUR — classify as MIXED → governed using BEHAVIOUR controls.**

Most Sprint 5 code changes are test/harness additions only (read-only pipeline consumers). One Sentinel pack update modifies a governed JSON asset. No analytical engine, SSOT, Knowledge Bus, or control-plane scripts are touched.

| Sprint 5 deliverable | Files touched | Risk |
|---|---|---|
| Proving harness run (regenerate fingerprints) | Writes to `docs/audit-papers/launch-core-proving/` — no product code | DOC only |
| New CHECK 2/5/6 binary tests | `backend/tests/unit/test_lc_s5_proving_checks.py` (new file) | STANDARD |
| `wave1_contradiction` Sentinel graduation | `sentinel/packs/escaped_defects_v1.json` | STANDARD |
| Human walkthrough execution | No code — documentation only | DOC only |
| Sprint 5 completion note | `docs/sprints/LC-S5_*.md` | DOC only |

**Overall Sprint 5 risk: STANDARD.** No HIGH-risk triggers apply. The sprint does not touch Intelligence Core, SSOT, Knowledge Bus, pipeline orchestrator, or control-plane scripts.

Claude audit + GPT review are required per SOP before merge of the test additions. DOC-only deliverables (fingerprint regeneration, completion note) may use the docs-only bypass.

---

## 13. Non-Goals

Sprint 5 must not:

- Modify any analytical engine or Intelligence Core components
- Modify `backend/ssot/` files
- Modify `backend/core/pipeline/`, `backend/core/analytics/`, or `backend/core/contracts/`
- Modify `backend/scripts/run_work_package.py`, `golden_gate_local.py`, or `update_cursor_status.py`
- Implement frontend Sentinel infrastructure (Jest runner in Sentinel) — deferred
- Promote `legacy_insights_consumer_path`, `body_overview` carriage, or `mock_mode_honesty` to Sentinel pack — deferred to a separate Sentinel infrastructure sprint
- Modify `narrative_report_compiler_v1.py` or any narrative assembly module
- Modify questionnaire SSOT or mapper
- Enable Gemini or change runtime narrative policy
- Restructure `AnalysisDTO` — Path A deferral stands
- Author Sprint 6 scope

---

## 14. Open Questions / Blockers

| Question | Status | Blocking? |
|---|---|---|
| Proving harness — does it run without errors after WP3 mapper changes? | Unconfirmed until run. WP3 changes questionnaire mapper; harness injects `questionnaire_data` directly into the fixture. Assessment: should run unchanged, but only a fresh run confirms this. | YES — run before authoring tests |
| CHECK 2 bridge phrase — what exact language does the alcohol bridge produce on the `lifestyle_minimal.json` fixture? | Unknown until harness run — depends on fixture alcohol value and bridge template. | YES — needed to author substring assertion |
| CHECK 5 contradiction criteria — what exact substring patterns define "danger language" vs "reassurance language" for each band? | Requires reading current consequence sentence templates in `domain_score_assembler.py` to extract the governed phrase patterns. | YES — needed to author CHECK 5 assertion |
| CHECK 6 lead pattern name — does VR still produce "Homocysteine" as lead, or has the panel lead changed since WP2? | Stale fingerprints suggest VR is also Homocysteine-led, but this must be confirmed from fresh run. | YES — needed to author CHECK 6 assertion |
| `synthesis.py` GPT ratification gap — standing protocol finding from WP2 second-pass audit (`gate_compliance_audit_sprint3_readiness_second_pass.md:16–17`). Is this recorded and closed? | Still open per audit record. | NOT A SPRINT 5 BLOCKER — lifecycle governance gap only |
| `alias_sweep` in sentinel_runner but not in escaped_defects_v1.json — should this be reconciled? | Pre-existing gap. No action required for Sprint 5. | No |
| WP3 optional/advanced tier count reconciliation (2 optional vs 5 target; 12 advanced vs 9 target) — `WP3_questionnaire_rationalisation_completion_2026-05.md:70–74` | Governance SSOT retag, not Sprint 5 scope. | No |

---

## 15. Files Inspected

### Proving artefacts (full read)
- `docs/audit-papers/launch-core-proving/PROVING_REPORT.md`
- `docs/audit-papers/launch-core-proving/latest_fingerprints.json` (header section)

### Sprint completion notes (full or partial read)
- `docs/sprints/LC-S4_launch_core_report_carriage_completion_2026-05.md`
- `docs/sprints/LC-S3_layer_c_payload_implementation_completion_2026-05.md` (partial)
- `docs/sprints/WP3_questionnaire_rationalisation_completion_2026-05.md`

### Prior audit documents (partial read)
- `docs/audit-papers/lc_s4_report_carriage_readiness_audit.md` (full — used as reference for LC-S4 pre-state)
- `docs/audit-papers/gate_compliance_audit_sprint3_readiness_second_pass.md` (partial — sections 1–3 for CHECK definitions)

### Backend proving infrastructure
- `backend/tools/launch_core_proving_harness.py` (full)
- `backend/tests/fixtures/proving/launch_core_matrix.json` (full)

### Sentinel
- `sentinel/packs/escaped_defects_v1.json` (full)
- `sentinel/sentinel_runner.py` (full)

### Frontend report surfaces (targeted reads)
- `frontend/app/(app)/results/page.tsx` (lines 1–120, 120–240, 430–570, 570–700, 700–864)
- `frontend/app/(app)/actions/page.tsx` (lines 1–80)
- `frontend/app/lib/legacyInsightsVisibility.ts` (full)
- `frontend/app/lib/lcS4ResultsCopy.ts` (existence confirmed)
- `frontend/app/(app)/upload/page.tsx` (lines 1–60)
- `frontend/app/components/results/ClinicianReportRenderer.tsx` (targeted grep for markdown strip)

### Backend formatter
- `backend/core/analytics/intervention_annotation_formatter_v1.py` (full)

### Regression tests
- `backend/tests/regression/test_lc_s4_statin_signal_isolation_regression.py` (partial)

### Git history
- `git log --oneline -10` — confirmed HEAD `2247d98` vs fingerprint SHA `48efd2e`

---

## Non-Document Files Modified

**NONE.** This audit read code and documentation files only. No implementation files, backend files, frontend files, SSOT files, Knowledge Bus files, Automation Bus artefacts, or Sentinel files were modified.

---

## Sprint 5 Ready to Author?

**YES — with one mandatory pre-action:** Run the proving harness fresh before authoring the CHECK 2/5/6 binary assertions. The harness text output (alcohol bridge phrase, consequence sentences, lead pattern names) must be known before the assertions can be written. Sprint 5 prompt should include the proving run as an explicit Stage 1B / Reality Check step.
