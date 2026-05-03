# HealthIQ AI — Sentinel Background Testing: Repo-Grounded Audit

**Audit date:** 2026-05-03  
**Auditor:** Claude Code  
**Basis:** Direct repo inspection. All findings cite observed file paths. No assumptions made where evidence was not found.

---

## 1. Executive Summary

The repo is **materially more test-ready than a typical early-stage product**, with 197 backend Python test files (~35k lines), 50 frontend test files, a rich fixture estate, and an established control-plane with 14 validator scripts. The analytical engine has deep unit test coverage and a credible fixture infrastructure.

However, the repo is **not yet ready for an autonomous Sentinel system**. The gaps are specific:

- No single test explicitly guards against internal slug/ID leakage to users.
- The five known escaped defects have no named regression tests.
- Persisted-result replay is structurally possible but currently relies on mock DB sessions rather than real stored shapes.
- The path classification needed for Sentinel's risk classifier is straightforward but not yet formalised.

**Phase 1 realistic?** — **Partly.** A bounded Phase 1 slice is achievable now using existing fixtures and the alias/SSOT infrastructure. A full Phase 1 Sentinel is not — the escaped-defect pack, slug-leakage guards, and real persisted-result replay need to be authored first.

---

## 2. Current Test Inventory

### 2.1 Real coverage map

**Backend: `backend/tests/` — 197 files, ~35,174 lines**

| Category | Files | What it covers | Active? | Depth |
|---|---|---|---|---|
| `unit/` | ~146 | Analytics primitives, scoring, arbitration, clustering, signals, LLM client, root-cause compiler, state engine, questionnaire mapper, DTO builders | Yes | Broad and deep |
| `enforcement/` | 37 | Canonical-only enforcement, arbitration, calibration, causal layer, clustering, evidence, golden panels, precedence, layer integrity, state transitions | Yes | Narrow but purposeful |
| `integration/` | 20 | Clustering, confidence, export, fallback service, Gemini, insights, lab origin, LLM parsing, orchestrator, persistence flow/service, questionnaire API+pipeline, ratios, scoring, upload SSOT, venous aliases | Yes | Moderate |
| `e2e/` | 1 | `test_persistence_e2e.py` — full persistence flow | Yes, but uses mock DB session, not real DB | Shallow |
| `smoke/` | 1 | Fixture endpoint — 6 biomarkers only | Yes | Very narrow |
| `performance/` | 1 | Connection pooling | Yes | Narrow |
| `security/` | 2 | GDPR compliance, RLS policies | Yes | Narrow |

**Frontend: `frontend/tests/` — 50 files**

| Category | Files | What it covers | Active? | Depth |
|---|---|---|---|---|
| `lib/` | 8 | actionsHub, bodyOverviewPrimarySentence, historyErrors, narrativeRuntimePresentation, primaryFindingShaping, questionnaireSchema, resultsHeroAlignment, uploadReferenceRange | Yes | Moderate |
| `components/` | 8 | BiomarkerDials, BiomarkerForm, ClusterSummary, InsightsPanel, InterpretationPatternsSection, ResultsInvestigationSpine, SystemUnderstandingSection, Wave1DomainCards, ClinicianReportRenderer | Yes | Moderate |
| `integration/` | 7 | Error handling, launch route contracts, OPS-S1A trust baseline, OPS-S1B operational artefacts, persistence, store-service integration, wedge metrics | Yes | Moderate |
| `e2e/` | 4 | analysis-workflow, persistence-pipeline, smoke, upload-autofill | Playwright-based; unknown CI status | Potentially broad |
| `state/` | 3 | analysisStore, clusterStore, uiStore | Yes | Narrow |
| `services/` | 1 | analysis service | Yes | Narrow |
| `queries/` | 1 | analysisResult query | Yes | Narrow |
| `hooks/` | 1 | useHistory | Yes | Narrow |

**Notable:** `frontend/tests/tests_new/` contains ~16 files that appear to mirror the primary test suite. Origin unclear — may be a copy artefact.

### 2.2 Strengths

- Backend unit test coverage of the analytics engine is genuine and broad. Arbitration, scoring, clustering, signal evaluation, root-cause compilation, and the state engine all have dedicated test files.
- The enforcement tier (`enforcement/`) is a structurally sound design — tests that fire when architecture contracts are violated.
- Frontend `OPS-S1A` and `OPS-S1B` are excellent precedents: lightweight static checks that guard specific trust surfaces.
- Venous alias integration test (`test_venous_aliases_orchestrator_integration.py`) directly covers a real escaped-defect class.

### 2.3 Weaknesses

- The backend "e2e" persistence test uses `unittest.mock` DB sessions — it is not a true end-to-end persistence test.
- The smoke test uses 6 hardcoded biomarkers and checks a fixture endpoint, not a real pipeline run.
- No frontend test explicitly asserts that `internal_id` or raw backend slugs are not rendered to users.
- No regression tests for any of the five known escaped defects by name.
- `tests_new/` is unexplained and may indicate stale artefact risk.

### 2.4 Sentinel mapping

| Sentinel need | Current test asset | Gap |
|---|---|---|
| Canonical/alias enforcement | `enforcement/test_canonical_only.py`, alias unit tests | No sweep against full SSOT alias registry |
| Parser/upload surface | `test_upload_ssot_metadata.py`, `uploadReferenceRange.test.ts` | No live-like payload replay |
| Signal/scoring stability | Extensive unit tests | No output-level snapshot comparison |
| Slug leakage guard | `OPS-S1A` (backend strings only) | No runtime component-level check |
| Persisted result replay | Integration/e2e exist but use mocks | No real-result replay |
| Escaped-defect pack | None | Entirely absent |

---

## 3. Fixture and Sample-Data Inventory

**Location: `backend/tests/fixtures/` — 57 files**

### 3.1 Panel fixtures (`panels/` — 20 files)

| Fixture | Purpose | Reusable for Sentinel? | Notes |
|---|---|---|---|
| `ab_full_panel.json` | Full AB blood panel | Yes | Core replay asset |
| `ab_full_panel_with_profiles.json` | Panel + reference profiles | Yes | Richer replay |
| `ab_full_panel_with_ranges.json` | Panel + lab ranges | Yes | Good for parser fidelity |
| `vr_full_panel.json` | Full VR panel | Yes | Companion to AB |
| `vr_full_panel_with_ranges.json` | VR + ranges | Yes | — |
| `ab_n9b_lifestyle_bridge.json` | Lifestyle integration fixture | Yes | Tests lifestyle path |
| `canonical_small.json` | Minimal canonical set | Yes | Fast smoke target |
| `lab_reference_profile_micro.json` | Micro lab reference | Yes | Narrow |
| `amber_hepatic.json`, `green_metabolic.json`, `red_metabolic.json` | Domain-labelled panels | Yes | Good for domain output checks |
| `panel_template.json` | Generic template | Partial | Needs population |
| `panel_acceptance_profiles_v1.yaml` | Acceptance criteria | Yes | Governance asset |
| `golden_panel_160.json` | 160-biomarker golden panel | Yes — primary | Key Sentinel asset |
| `golden_panel_160_collision_free.json` | Collision-free variant | Yes | Regression |
| `golden_panel_sprint14_2_thyroid_immune_mini.json` | Thyroid/immune mini | Yes | Domain-specific |
| `collision_fixture_hdl.json` | HDL collision case | Yes | Defect-class coverage |

### 3.2 Phenotype fixtures (`panels/phenotypes/` — 11 YAML files)

Covers: hepatic ALT inflammatory, insulin resistance early, iron deficiency/overload, lipid transport, renal stress, thyroid-lipid, vascular HCY, homocysteine/macrocytosis, TSH-axis metabolic. All appear to be valid YAML scenario fixtures. Directly reusable for phenotype assertion tests.

### 3.3 Golden run artifacts (`backend/artifacts/golden_runs/` — 50+ timestamped directories)

Each directory contains a full `analysis_result.json` output from a real pipeline run. Format: timestamped UTC directories. Named variants include `ci-golden-160`, `debug-golden-160`, `n9-ab-validation-20260422`, `qa-uat-unscored-diag`, others.

These are the most valuable Sentinel assets in the repo. They represent ground-truth outputs that can be replayed against future pipeline runs for regression detection. Currently used informally; no automated comparison mechanism exists.

### 3.4 Arbitration scenario fixtures (`arbitration_scenarios_v1.json`, `v2.json`)

Purpose: test the arbitration engine against competing signal scenarios. Directly reusable.

### 3.5 LLM parsing fixtures (`fixtures/llm/` — 3 files)

`valid_llm_result_v2.json`, `invalid_numeric_invention.json`, `invalid_unknown_field.json`. Good edge-case coverage for parser validation.

### 3.6 Frontend mock data (`frontend/app/lib/mock/` — 8 files)

`analysis-result.json`, `biomarkers.json`, `questionnaire.json`, `reports.json`, `upload-response.json`, `user-profile.json`. Useful for frontend component testing but are static mocks — not derived from real pipeline outputs.

### 3.7 Key gaps

- No fixture that deliberately encodes known-bad alias inputs (GGT by wrong name, bilirubin with wrong key) to test alias resolution under adversarial conditions.
- No fixture for the "stale persisted result" scenario — an old-schema result loaded into current frontend.
- Frontend mocks are not versioned against the backend DTO schema — no guarantee they stay in sync.
- No parser/upload fixture that simulates a realistic OCR/CSV lab report format (raw lab PDF output).

---

## 4. Control-Plane and Gate Support

### 4.1 What exists

**Execution kernel:** `backend/scripts/run_work_package.py` (~400 lines)  
Handles sprint lifecycle: `start`, `finish`, token writing/deletion, git branch verification, gate invocation. Well-structured. Writes `automation_bus/state/work_package_active.json`.

**Gate script:** `backend/scripts/golden_gate_local.py` (~230 lines)  
Runs git state checks, parses front matter, generates gate evidence JSON to `automation_bus/latest_gate_evidence.json`. Writes `latest_gate_output.txt`. This is a functioning gate artefact that Sentinel could observe.

**Validator scripts (14):** `validate_signal_library.py` (51KB), `validate_investigation_spec.py` (18KB), `validate_intelligence_model.py` (20KB), `validate_phenotype_map.py` (14KB), `validate_knowledge_package.py`, `validate_insights.py`, `validate_rls_policies.py` (15KB), `validate_intervention_effects_registry.py` (12KB), `validate_promoted_signal_intelligence.py` (20KB), `validate_research_brief.py` (13KB), and others.

These are deep, SSOT-grounded validators. They are the closest thing in the repo to a Sentinel Phase 1 component — they enforce governed contracts on intelligence assets.

**Audit evidence artefacts:**  
`automation_bus/latest_audit_summary.md`, `latest_gate_evidence.json`, `latest_gate_output.txt`, `latest_prompt_hardening.json`. These are already structured for machine consumption.

**Test runner scripts:**  
`run_baseline_tests.py`, `run_sprint10_tests.py` — sprint-specific test orchestration. Indicate a pattern of targeted test runs per sprint rather than continuous full-suite execution.

### 4.2 What is reusable for Sentinel

- The gate evidence JSON schema is a candidate for Sentinel's change-event input.
- The validator scripts can be wrapped as Sentinel checks without modification.
- The golden run artifact directory is directly usable as a replay corpus.
- `pytest.ini` markers (`slow`, `integration`, `unit`) enable targeted test selection — exactly what a Sentinel test-selector needs.

### 4.3 What Sentinel must not mutate

- `automation_bus/state/work_package_active.json` — exclusive ownership of the kernel.
- `automation_bus/latest_gate_evidence.json`, `latest_gate_output.txt` — written by the gate; Sentinel should read, not write.
- Any file under `backend/ssot/` — SSOT is governed; Sentinel must read only.
- `backend/scripts/run_work_package.py`, `golden_gate_local.py` — control-plane scripts; HIGH risk class; Sentinel must not modify.
- `automation_bus/latest_audit_summary.md`, `latest_prompt_hardening.json` — governance artefacts; read-only for Sentinel.

### 4.4 What should remain separate

Sentinel's own state and reporting should live outside the existing automation bus namespace — suggested: `sentinel/` at repo root, with `sentinel/reports/`, `sentinel/state/`, `sentinel/packs/`. This avoids any risk of polluting governance artefacts.

---

## 5. Path-Classification Feasibility

### 5.1 Assessment

Path-based classification is **realistic** for this repo. The directory structure maps directly onto HealthIQ's three-layer architecture with reasonable precision.

### 5.2 Clear surfaces

| Surface | Paths | Ambiguity |
|---|---|---|
| Parser / upload / alias | `backend/services/parsing/`, `backend/core/canonical/`, `backend/app/routes/alias_api.py`, `backend/ssot/biomarker_alias_registry.yaml` | Low |
| SSOT / canonical mapping | `backend/ssot/`, `backend/core/canonical/` | Low |
| Analytics / scoring / signal | `backend/core/analytics/`, `backend/core/scoring/`, `backend/core/clustering/` | Low |
| Intelligence Core (pipeline) | `backend/core/pipeline/orchestrator.py`, `backend/core/pipeline/context_factory.py` | Low |
| Persistence / result DTO | `backend/core/models/results.py`, `backend/core/models/database.py`, `backend/core/dto/` | Low |
| Frontend trust surfaces | `frontend/app/components/results/`, `frontend/lib/narrativeRuntimePresentation.ts`, `frontend/lib/primaryFindingShaping.ts` | Moderate |
| Governance / control-plane | `backend/scripts/run_work_package.py`, `backend/scripts/golden_gate_local.py`, `automation_bus/` | Low |
| Knowledge Bus | `knowledge_bus/`, `backend/core/knowledge/` | Moderate — straddles content and intelligence load |

### 5.3 Path ambiguity zones

- `backend/core/insights/` — insight synthesis sits between Layer B (analytical assembly) and Layer C (narrative). A change here could affect both tiers. Classify as BEHAVIOUR-risk by default.
- `backend/core/dto/builders.py` — DTO construction could be neutral or could encode display decisions. Needs case-by-case review.
- `knowledge_bus/packages/*/signal_library.yaml` — content files that load directly into the intelligence engine (governed MIXED class per SOP). Path-only classification would miss this.
- `frontend/lib/` — mixes display helpers (safe) with data shaping functions (`primaryFindingShaping.ts`, `resultsHeroAlignment.ts`) that affect what users see. Not all `lib/` files are equivalent.

### 5.4 First practical path map

```
HIGH-risk surfaces:
  backend/core/pipeline/
  backend/core/analytics/
  backend/core/scoring/
  backend/core/clustering/
  backend/ssot/
  backend/scripts/run_work_package.py
  backend/scripts/golden_gate_local.py
  knowledge_bus/packages/*/signal_library.yaml

STANDARD-risk surfaces:
  backend/core/canonical/
  backend/services/parsing/
  backend/core/dto/
  backend/core/insights/
  backend/core/models/
  frontend/lib/narrativeRuntimePresentation.ts
  frontend/lib/primaryFindingShaping.ts
  frontend/app/components/results/

LOW-risk surfaces:
  frontend/app/components/ui/
  frontend/app/components/layout/
  frontend/lib/utils.ts
  docs/
  knowledge_bus/packages/*/research_brief.yaml
```

---

## 6. Persisted-Result Replay Feasibility

### 6.1 What exists

- `backend/core/models/results.py` (297 lines) — result model with persistence schema.
- `backend/core/models/database.py` (522 lines) — full ORM including results table.
- `backend/tests/integration/test_persistence_flow.py`, `test_persistence_service.py` — integration-level persistence tests.
- `backend/tests/e2e/test_persistence_e2e.py` — uses mock DB session; not a real replay test.
- `backend/artifacts/golden_runs/` — 50+ full `analysis_result.json` files from real pipeline runs. These are the most usable replay assets in the repo.

### 6.2 What is missing

- No automated test that loads a stored golden run JSON and asserts it renders correctly in the current frontend without regression.
- No version field comparison: if `analysis_result.json` schema evolves, there is no test that catches old-vs-new shape incompatibility.
- The persistence "e2e" test uses `unittest.mock` — it does not exercise the real database path.
- No test that loads an old-timestamped golden run (e.g., `20260224T171501Z/analysis_result.json`) through the current pipeline validator and asserts compatibility.

### 6.3 Difficulty assessment

**Moderate.** The golden run corpus already exists and is structurally sound. The missing piece is a comparison harness: a script that loads each golden run JSON, passes it through a DTO validator, and flags structural divergence. This is buildable without new infrastructure — it only requires reading the existing golden run files and comparing against the current DTO schema. Frontend replay (loading old JSON into the current results page) is harder and likely requires Playwright.

---

## 7. Frontend Trust-Surface Testing Feasibility

### 7.1 What is already tested

- **OPS-S1A** (`ops-s1a-trust-baseline.test.ts`): Guards the landing page against HIPAA, bank-level, and medical-grade claim strings. Checks legal routes exist. Checks footer links. Checks login page doesn't expose "FastAPI" string. These are static file reads — fast and reliable.
- **OPS-S1B** (`ops-s1b-operational-artifacts.test.ts`): Checks that compliance/ops artefact files exist on disk and contain required phrases. Well-structured.
- **InterpretationPatternsSection.test.tsx**: Uses `internal_id: 'ph_test_a_v1'` in test fixtures, but the test appears to cover rendering logic and ordering, not slug leakage.
- `uploadReferenceRange.test.ts`: Covers venous slug variant mapping to canonical (`apolipoprotein venous slug variants to canonical apob_apoa1_ratio`). Directly relevant.

### 7.2 What would be easy to add

- A static check that `internal_id` values (matching pattern `^ph_[a-z0-9_]+_v[0-9]+$`) are not present in rendered component output strings. Could be a Jest test reading component output via `render()`.
- OPS-S1A-style checks extended to results page and analysis page source files for backend identifier strings.
- A snapshot test of the Wave1DomainCards or InsightsPanel component that asserts no raw slugs appear in rendered output.

### 7.3 What is currently missing

- No test that passes a mock result with `internal_id: "ph_metabolic_early_ir_v1"` into a results component and asserts the rendered text does not show the raw slug.
- No test for contradictory visible sections (e.g., a "low risk" summary header alongside a "critical finding" card).
- No test for impossible-looking display values (e.g., a domain score of 0 rendering alongside "excellent" label).
- No Playwright test that opens a rendered results page and scans visible text for slug patterns.
- The `tests_new/` directory contents are not confirmed to be active — if stale, they add noise.

### 7.4 Where live-browser/UAT checks still seem necessary

Domain-card coherence (e.g., whether the InsightGraph sections and the domain score summary tell the same story) is not reliably capturable in unit tests alone. The narrative involves multiple data sources combining in the display layer. Playwright visual/content checks would be needed for this, and they are more fragile.

---

## 8. Parser/Alias Coverage Feasibility

### 8.1 What exists

**Direct alias test coverage:**
- `backend/tests/test_alias_registry_service.py` — service-level alias resolution
- `backend/tests/test_alias_registry_singleton.py` — singleton pattern
- `backend/tests/unit/test_biomarker_alias_resolution.py` — biomarker-specific alias resolution
- `backend/tests/unit/test_normalize_aliases.py` — normalisation round-trips
- `backend/tests/unit/test_unit_alias_umol_v1.py` — unit alias conversions
- `backend/tests/integration/test_venous_aliases_orchestrator_integration.py` — end-to-end venous variant resolution through the orchestrator
- `backend/tools/validation/validate_aliases_and_ranges.py` — SSOT alias/range validator
- `frontend/tests/lib/uploadReferenceRange.test.ts` — frontend venous slug variant coverage

**SSOT alias registry:**  
`backend/ssot/biomarker_alias_registry.yaml` (15.7KB) is the authoritative alias map. It is referenced by the alias registry service.

**GGT and bilirubin in codebase:**  
Both GGT and bilirubin have analytics coverage in `domain_score_assembler.py`, `root_cause_compiler_v1.py`, and `load_root_cause_hypotheses.py`. The alias registry presumably contains their canonical mappings — the recent fix commits confirm they have been addressed at code level.

### 8.2 What is missing

- No test that iterates the full `biomarker_alias_registry.yaml` and for each alias entry, fires a normalization call and asserts it resolves to the correct canonical key. This is the "alias sweep."
- No test for GGT specifically that uses the wrong-name input (e.g., `"ggt"`, `"gamma_gt"`, `"gamma-glutamyl_transferase"`) and asserts it resolves to the canonical form.
- No test for bilirubin with the wrong-variant key (e.g., `"bilirubin_total"`, `"total_bilirubin_(venous)"`) against the canonical.
- No "live-like payload replay" test — there is no fixture that simulates a raw OCR'd or CSV'd lab report with real-world label noise.

### 8.3 Sentinel Phase 1/2 feasibility from current repo

**Feasible.** The infrastructure exists: the SSOT alias registry, the normalisation function, and panel fixtures are all present. A Phase 1 alias sweep is a matter of test authoring, not new infrastructure. The `validate_aliases_and_ranges.py` script already performs a form of this — it needs to be converted into a pytest fixture that runs against the full registry.

The main gap is escaped-defect coverage: GGT and bilirubin should have named regression tests that use the exact inputs that caused the real failures.

---

## 9. Escaped-Defect Regression Feasibility

### 9.1 Assessment by defect

| Escaped defect | Current coverage | Gap |
|---|---|---|
| GGT alias miss | GGT appears in analytics code; alias service has unit tests; no test uses the wrong-name GGT input | No named regression test for the specific alias that failed |
| Bilirubin canonical mismatch | `_liver_panel_has_bilirubin_coverage` function exists in assembler; no test uses wrong-key bilirubin input | No named regression test |
| Internal slug leakage | `OPS-S1A` catches backend strings in login page only; no component-level slug rendering check | Missing entirely |
| Wave 1 narrative contradiction | `DOMAIN_NARRATIVE_CONTRACT_WAVE1.md` exists as a spec; no automated test enforces it against a real rendered output | Missing entirely |
| Stale persisted result behaviour | Persistence integration tests exist but use mocks; no test loads an old golden run through current pipeline | Missing entirely |

### 9.2 Does the repo support a coherent escaped-defect pack?

**Yes, structurally.** The fixtures, SSOT, alias registry, and golden run corpus all exist. What is missing is a `backend/tests/regression/` directory (or equivalent) that contains:

1. One pytest test per escaped defect, using exact inputs that caused the original failure.
2. These tests should be marked `@pytest.mark.regression` and run in CI on every commit to HIGH-risk surfaces.

### 9.3 Where should the pack live?

Suggested: `backend/tests/regression/` for backend defects, `frontend/tests/regression/` for frontend/display defects. This mirrors the existing test directory conventions and allows targeted `pytest -m regression` runs.

---

## 10. Smallest Realistic Sentinel Phase 1 Slice

### Recommendation: Alias/canonical sweep + escaped-defect regression pack

**What it is:**

1. A `backend/tests/regression/` directory with five named tests — one per known escaped defect.
2. A pytest test that iterates `backend/ssot/biomarker_alias_registry.yaml` and asserts every alias resolves to its canonical form through the existing normalisation function.
3. A frontend Jest test that passes a result mock containing `internal_id` slugs into the results display components and asserts the raw slug does not appear in rendered output.

**Why this first:**

- **Zero new infrastructure required.** The alias registry, normalisation function, result fixtures, and golden panels all exist. This is test authoring only.
- **Direct repo grounding.** GGT and bilirubin alias misses, and slug leakage, are already identified as real failure modes. The fixtures needed to reproduce them are at hand.
- **Sentinel entry point.** Once these tests exist, the path-classifier can be pointed at alias/canonical and frontend trust surfaces, and Sentinel's test-selector has a real test pack to dispatch.
- **Golden gate integration.** `golden_gate_local.py` already runs gate checks per sprint. A `pytest -m regression` call can be added to its gate steps without modifying the gate script's structure.
- **Precedent exists.** `OPS-S1A` and `OPS-S1B` demonstrate the team's ability to write lightweight, targeted regression guards that do not require infrastructure changes.

**What it defers:**

- Persisted-result replay harness (moderate effort, needs DTO schema comparison logic).
- Wave 1 narrative coherence (needs Playwright or content-analysis tooling).
- Full autonomous Sentinel dispatcher and reporting pipeline.

---

## 11. Open Blockers and Ambiguities

| Item | What is unclear | Follow-up needed |
|---|---|---|
| `frontend/tests/tests_new/` | Appears to mirror the primary test suite. Origin unknown — copy artefact, migration in progress, or abandoned? | Confirm with team whether these 16 files are active, stale, or superseded |
| Backend e2e test quality | `test_persistence_e2e.py` uses mock DB — not a true e2e test. Real database test coverage is unverified. | Check whether `backend/healthiq_test.db` or `test.db` are used by any test in CI |
| Playwright CI status | Four Playwright tests exist in `frontend/tests/e2e/`. Whether these run in CI and pass consistently is not determinable from the repo structure alone. | Check CI/CD config and last Playwright run status |
| `tests_new/` duplication risk | If stale, it may mask failures by giving a false coverage picture. | Delete or migrate with confirmation |
| GGT and bilirubin fix verification | Recent commits fixed GGT and bilirubin alias handling. No regression test exists yet to lock this in. | Confirmed fixable: add regression tests using original failure inputs |
| Frontend mock/DTO sync | `frontend/app/lib/mock/analysis-result.json` is static — no verified link to the backend DTO schema version. If the DTO changes, the mock may silently diverge. | Check whether a schema validation step exists against frontend mocks |
| `backend/core/insights/` risk class | This directory straddles Layer B and Layer C. A change here may or may not affect emitted reasoning. | Define whether `insights/synthesis.py` and `insights/modules/` are classified as Intelligence Core by SOP §3 or as Layer C translation |
| Knowledge bus content loaders | `backend/core/knowledge/load_root_cause_hypotheses.py` and related loaders feed directly into the intelligence pipeline. Path-based classification alone would miss these as MIXED-class changes. | Explicitly add knowledge loader paths to the HIGH-risk surface map |

---

*Audit complete. All findings are repo-grounded. No code was written. No sprint prompts were produced.*
