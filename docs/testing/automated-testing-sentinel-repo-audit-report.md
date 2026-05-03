# HealthIQ AI — Background Testing Sentinel: Repo-Grounded Audit Report

**Audit source:** `docs/testing/automated testing repo-grounded audit,md`  
**Scope:** Inventory only — no code changes, no implementation design.  
**Method:** File-system and workflow inspection as of this audit pass.

---

## 1. Executive summary

The repository already contains a **large deterministic backend test estate** (unit + integration + enforcement), **rich fixture/snapshot machinery** (golden panel runner, replay manifest, phenotype panels, AB/VR-style panels), and **multiple control-plane scripts and gates**. That is a **strong foundation** for a Sentinel that classifies risk surfaces, selects tests, and surfaces regressions without touching product logic blindly.

**Gaps:** default **CI** (`.github/workflows/ci.yml`) runs **only** `backend/tests/unit` for Python plus frontend Jest with archive ignores — **not** the full pytest tree (integration, enforcement, e2e Python, slow markers). **Playwright** specs exist but are **not** evidenced as blocking in the sampled CI workflow. **Nightly** `validate.yml` invokes `backend/scripts/run_all_tests.py`, which **does not exist as a standalone script** in the repo (likely stale workflow or path error — see §11). Governance split (`AGENTS.md`) implies Sentinel automation must **respect** full Automation Bus SOP for `backend/core/`, `backend/ssot/`, `knowledge_bus/`, etc., versus lighter touch for `frontend/`.

**Phase 1 realistic now:** **partly** — yes for **backend/golden/enforcement/alias-oriented** Sentinel slices; **weaker** for **unified path→test selection** and **persisted-result replay as a single automated product gate** without additional wiring. Frontend trust-surface coverage exists but is **spotty** relative to escaped issues (coherence, slugs).

---

## 2. Current test inventory

### Backend — unit (`backend/tests/unit/`)

- **Scale:** On the order of **150+** `test_*.py` modules (pytest `testpaths = backend/tests`; default `-m "not slow"`).
- **Coverage character:** **Broad and deep** on analytics, scoring, clustering, arbitration, insight graph, narrative/IDL compilers, domain score assembly, Wave 1 narrative, golden panel runner, replay manifest, unit registry, normalisation, LLM parsing/validation boundaries, knowledge-bus contracts, and many SSOT-adjacent registries.
- **Sentinel mapping:** **Excellent** source for “deterministic tests to run when core analytics/SSOT change.” Many modules are **narrow** (single subsystem); some “golden” tests are **broad** end-to-end through the deterministic pipeline.
- **Activeness:** **Active** under local pytest and partial CI; **meaningful** — includes recent Wave 1 liver/mapping tests (e.g. `test_wave1_liver_marker_mapping_fix.py`, `test_wave1_liver_d7.py`, `test_domain_narrative_wave1.py`, `test_domain_score_assembler_v1.py`).

### Backend — integration (`backend/tests/integration/`)

- **Examples:** orchestrator + scoring, persistence service/flow, upload API, questionnaire pipeline, insight pipeline, venous aliases + orchestrator, unmapped quarantine, ratio registry, lab origin, criticality, clustering, export route, LLM isolation, etc. (~**21** modules observed).
- **Sentinel mapping:** **High value** for “did we break the wire-up?” — but **not** in default CI matrix sampled (`ci.yml` runs **unit only** for backend).

### Backend — enforcement (`backend/tests/enforcement/`)

- **Scale:** **35** substantive modules + `__init__.py`.
- **Purpose:** Architecture/policy guards (no raw fields in InsightGraph, registry not hardcoded, golden snapshot not raw, arbitration authority, retail explainer registry, duplicate ratio compute bans, etc.).
- **Sentinel mapping:** **Directly aligned** with Sentinel Phase 1/2 “governed surfaces” — these are **ideal** candidates for **always-on** or **path-triggered** runs when touching governed directories.

### Backend — e2e (`backend/tests/e2e/`)

- **Observed:** `test_persistence_e2e.py` — persistence flow with **Mock** DB session (labelled e2e but **not** full stack browser/HTTP).
- **Sentinel mapping:** Useful for persistence contract smoke; **not** a substitute for full-stack E2E.

### Frontend — Jest (`frontend/tests/` + root `tests/`)

- **Areas:** Components (Wave 1 cards, interpretation spine, dials, clinician report renderer), lib (upload reference range / `analysisBiomarkerKey`, narrative runtime, results hero alignment, actions hub), state stores, integration routes (persistence, error handling, launch contracts, **ops-s1a-trust-baseline**, wedge metrics), services (`analysis.test.ts`).
- **`tests_archive/`:** Legacy/sprint snapshots — **excluded** from CI via `--testPathIgnorePatterns=tests_archive`.
- **Sentinel mapping:** **Moderate** — good hooks for **slug leakage** and **Wave 1 presentation** (`Wave1DomainCards.test.tsx` maps missing markers to user-safe labels). **Limited** systematic coverage for **cross-section narrative coherence** (collapsed vs expanded) and **page-level authority** compared to manual UAT.

### E2E — Playwright (`frontend/tests/e2e/`, `frontend/tests/tests_new/e2e/`, root `tests/e2e/`)

- **Config:** `frontend/playwright.config.ts` — `testDir: ./tests/e2e`, base URL `localhost:3000`, multi-browser projects.
- **Specs:** `analysis-workflow.spec.ts`, `upload-autofill.spec.ts`, `persistence-pipeline.spec.ts`, `smoke.spec.ts` (plus archived copies).
- **Quality note:** Sampled `analysis-workflow.spec.ts` references UI strings (“Health Analysis Upload”, “Your Health Analysis Results”) that may **drift** from current product copy — **stale E2E risk** not verified against live app in this audit.
- **CI:** **Not observed** as a required job in the sampled `ci.yml` (Jest only for frontend matrix).

### Fixture / replay / golden

- **`test_golden_panel_runner.py`** — large; drives deterministic panel execution.
- **`test_replay_manifest.py`** — substantial; replay manifest contract.
- **Golden gate workflow** (see §4) runs golden runner + snapshot pack verification.

### Parser / alias / unit normalisation

- **`test_biomarker_alias_resolution.py`**, **`test_normalize_aliases.py`**, **`test_venous_aliases_orchestrator_integration.py`**, **`test_orchestrator_unmapped_quarantine.py`**, **`test_unit_alias_umol_v1.py`**, **`test_orchestrator_unit_normalisation.py`**, **`test_llm_parser_reference_bounds.py`**, **`test_wave1_liver_marker_mapping_fix.py`** (trace-style keys for GGT/bilirubin + assembler missing list).
- **Sentinel mapping:** **Strong** substrate for alias/canonical sweeps.

### Domain-card / narrative coherence

- **Backend:** `test_domain_narrative_wave1.py`, `test_domain_score_assembler_v1.py`, `test_wave1_liver_d7.py`, `test_wave1_liver_marker_mapping_fix.py`, investigation/narrative contracts, balanced systems presentation.
- **Frontend:** `Wave1DomainCards.test.tsx`, `resultsHeroAlignment.test.ts`, `primaryFindingShaping.test.ts`, `bodyOverviewPrimarySentence.test.ts`, narrative framing tests under `insights/`.

### Release / gate-related artifacts

- **`.github/workflows/ci.yml`** — backend unit + mypy + ruff; frontend Jest + lint + type-check; security job (truncated in read).
- **`.github/workflows/golden_gate.yml`** — enforcement pytest + golden panel runner + artifact checklist + NO-LLM log gate (branch-scoped triggers).
- **`.github/workflows/validate.yml`** — nightly DB + **broken reference** to missing `run_all_tests.py` (§11).
- **`backend/scripts/golden_gate_local.py`** — writes **`automation_bus/`** evidence stubs; aligns with “control plane / evidence generation” thinking.
- **`pytest.ini`** — excludes `slow` by default; **`testpaths = backend/tests`** only (no root-level pytest discovery outside that tree).

### Strengths / weaknesses (summary)

| Strengths | Weaknesses |
|-----------|------------|
| Large deterministic core tests + enforcement pack | CI does not run full backend test tree by default |
| Golden runner + snapshot pack + replay manifest tests | Nightly validate script path appears stale |
| Dedicated Wave 1 + liver mapping regression tests added | Playwright not clearly gated; possible spec drift |
| Rich fixtures (AB/VR, golden 160, phenotypes) | Frontend coherence/slug issues partly still manual |

---

## 3. Fixture and sample-data inventory

| Category | Location (representative) | Purpose | Reusable for Sentinel? | Notes |
|----------|---------------------------|---------|------------------------|-------|
| Large golden / collision-free panels | `backend/tests/fixtures/golden_panel_160.json`, `golden_panel_160_collision_free.json` | Deterministic panel runs | **Yes** | Golden gate uses `golden_panel_160.json` |
| AB / VR style panels | `backend/tests/fixtures/panels/ab_full_panel*.json`, `vr_full_panel*.json` | Acceptance / scenario testing | **Yes** | `run_ab_vr_acceptance_harness.py` exists |
| Phenotype / IDL fixtures | `backend/tests/fixtures/panels/phenotypes/*.json`, `phenotype_expectations_v1.yaml` | Targeted interpretation cases | **Yes** | Good for narrow regression packs |
| Lab reference profile micro | `lab_reference_profile_micro.json` | Range/profile edge cases | **Yes** | |
| Lifestyle JSON | `lifestyle_minimal.json`, `lifestyle_musculoskeletal_only.json` | Modifier / burden bridges | **Yes** | |
| LLM parse fixtures | `backend/tests/fixtures/llm/*.json` | Validator / parser contracts | **Partial** | Not full “live lab PDF” diversity |
| Knowledge package fixtures | `backend/tests/fixtures/pkg_*` | KB validation | **Yes** | Governance-heavy |
| Clinician report fixtures | `backend/tests/fixtures/reports/*.json` | Report renderer alignment | **Yes** | |
| Collision / arbitration | `collision_fixture_hdl.json`, `arbitration_scenarios_v*.json` | Edge cases | **Yes** | |

**Gaps:** Centralised **“escaped defect” JSON packs** (single folder named as such) **not observed** — defects are starting to accrue as **normal tests** (good) but **not** marketed as a unified pack. **Frontend mock payloads** for full analysis DTOs exist piecemeal in tests, not a single **persisted-result version matrix** fixture tree.

---

## 4. Control-plane and gate support

### Observed reusable pieces

- **Validators:** `backend/scripts/validate_*.py` (SSOT, signal library, package manifest, investigation spec, phenotype map, interaction map, metric namespace, RLS, insights, AB panel SSOT, etc.).
- **Harnesses:** `run_ab_vr_acceptance_harness.py`, `run_baseline_tests.py`, `verify_three_layer_pipeline.py`, `golden_gate_local.py`, `run_work_package.py`, `wave1_backfill_consumer_cards.py` (stored raw → normalisation → orchestrator for Wave 1 backfill).
- **Tools:** `backend/tools/run_golden_panel.py` (referenced from golden gate workflow).
- **Compliance:** `scripts/tests/verify_testing_compliance.py` (expects `TEST_LEDGER.md`, audit paths — **exists** in repo root per glob).
- **Artifacts:** Golden runs under `backend/artifacts/golden_runs/` (per workflow), validation reports path in `validate.yml`.
- **Policy tests:** Enforcement suite = **living control plane** for code structure.

### Boundaries Sentinel should respect

- **`AGENTS.md`:** Full Automation Bus SOP for core/SSOT/knowledge_bus; Sentinel must not **auto-remediate** governed medical/analytical content without human governance.
- **Enforcement + golden outputs:** Treat as **authorities** — Sentinel should **report** and **select tests**, not rewrite golden baselines silently.

### Should remain separate

- **LLM smoke / Gemini** tests exist in integration — Sentinel “narrow auto-fix” must **not** conflate with deterministic gates unless explicitly scoped.

---

## 5. Path-classification feasibility

**Verdict:** **Realistic** for a **first practical map** using top-level and second-level prefixes.

| Risk surface | Suggested path prefixes (repo-grounded) | Ambiguity |
|--------------|----------------------------------------|-----------|
| Parser / upload / alias | `backend/core/canonical/`, `frontend/app/(app)/upload/`, `frontend/app/lib/uploadReferenceRange.ts` | Duplicated/legacy tests under `tests/` vs `frontend/tests/` |
| SSOT / canonical | `backend/ssot/`, especially `biomarker_alias_registry.yaml`, `biomarkers.yaml`, `scoring_policy.yaml`, `ranges.yaml` | YAML sprawling; subdirectory granularity needed |
| Analytics / scoring / signals | `backend/core/analytics/`, `backend/core/scoring/`, `backend/core/insights/`, `knowledge_bus/` (research packages) | `knowledge_bus/` vs `backend/core` overlap in “intelligence” |
| Persistence / DTO / snapshot | `backend/services/storage/`, `backend/repositories/`, orchestrator output DTOs, `backend/tests/integration/test_persistence_*.py`, replay manifest in core | Multiple “e2e” meanings |
| Frontend trust | `frontend/app/(app)/results/`, `frontend/app/components/results/` | Presentation vs data shaping split across `lib/` |
| Governance / control | `backend/tests/enforcement/`, `backend/scripts/validate_*.py`, `.github/workflows/golden_gate.yml` | |

**Path ambiguity:** `tests/` at repo root vs `frontend/tests/` — **duplicate** integration/e2e trees increase mis-classification risk unless Sentinel normalises to **one** canonical test root per app.

---

## 6. Persisted-result feasibility

### What exists

- **Persistence integration tests** and **mock-driven e2e** persistence module.
- **Wave 1 backfill script** reconstructs unit-normalised panels from **stored `raw_biomarkers`** and reruns orchestrator (`wave1_backfill_consumer_cards.py`) — strong pattern for **replay**.
- **Replay manifest** tests and golden snapshot packs including `replay_manifest.json`.
- **Frontend:** integration tests for persistence pipeline and analysis store; Playwright `persistence-pipeline.spec.ts`.

### What is missing / unclear

- **Single documented “version N vs N+1 snapshot compatibility” suite** not surfaced in this audit pass (may be implicit in manifest tests — not fully opened).
- **Automated** “load production-shaped JSON from DB” loop **not** confirmed as a standard harness.

### Difficulty

- **Moderate:** Replay **machinery exists** (backfill + manifest + golden artifacts); **operationalising** as always-on Sentinel needs **stable fixture IDs**, **DB or file snapshots**, and **clear schemas** for stored analysis rows.

---

## 7. Frontend trust-surface feasibility

### Already tested (examples)

- **Slug masking for Wave 1 missing markers:** `Wave1DomainCards.test.tsx` (D-7 style user-safe labels; asserts no raw `total_bilirubin` / `ast` / `ggt` tokens in output for that scenario).
- **Copy alignment:** `resultsHeroAlignment.test.ts`, `primaryFindingShaping.test.ts`, `bodyOverviewPrimarySentence.test.ts`.
- **Trust baselines:** `frontend/tests/integration/ops-s1a-trust-baseline.test.ts`.
- **Narrative framing:** `InsightsPanel.narrative-framing.test.tsx`.

### Easy to add (typical)

- More **table-driven** tests on `Wave1DomainCards` for **coherence** (headline vs consequence tier) given fixed `ConsumerDomainScoreV1` payloads.
- Golden **snapshot tests** for rendered strings for a small set of DTO fixtures.

### Missing / still manual-heavy

- **Full page** results authority (primary finding vs Wave 1 vs trust strip “76 markers” vs “9 of 9”) — **browser UAT** still appears necessary for holistic checks.
- **Contradictory sections** across regions (collapsed vs expanded) — **not** seen as a consolidated automated suite in the sampled files.

---

## 8. Parser / alias feasibility

### Current support

- **AliasRegistryService** + **BiomarkerNormalizer** tests; **venous** orchestrator integration; **unmapped quarantine** integration.
- **Unit normalisation** orchestrator tests; **µmol** alias tests.
- **Trace-driven** liver keys in `test_wave1_liver_marker_mapping_fix.py` (gamma-glutamiltransferase key, bilirubin_total venous, assembler missing list with canonical `bilirubin`).
- **SSOT** validation scripts and **biomarker** resolution tests.

### Gaps

- **Systematic** “every display label in fixture X resolves” sweep **not** evidenced as one job (likely **feasible** to add as Sentinel Phase 1 **report-only** or pytest parametrize from YAML).
- **Frontend `analysisBiomarkerKey`** — covered in `uploadReferenceRange.test.ts` for limited special cases; **not** a comprehensive mirror of SSOT.

### Phase 1/2 alias sweep feasibility

**Feasible:** yes — combine **registry YAML** + **normalizer.resolve** + **small trace library** (new rows are cheap).

---

## 9. Escaped-defect regression feasibility

| Defect theme | Partially covered? | Evidence |
|--------------|-------------------|----------|
| GGT alias miss / trace key | **Yes** | `test_wave1_liver_marker_mapping_fix.py` |
| Bilirubin canonical vs `total_bilirubin` missing flag | **Yes** | Same file + assembler behaviour |
| Internal slug leakage (Wave 1) | **Partial** | `Wave1DomainCards.test.tsx` for missing-marker strip; not all surfaces |
| Wave 1 narrative contradiction | **Partial** | `test_wave1_liver_d7.py`, domain narrative tests; frontend coherence **narrow** |
| Stale persisted result | **Partial** | Backfill/replay machinery; **not** a single named “stale snapshot” regression |

**Coherent “escaped defect pack”:** **Yes, feasible** — natural home: **`backend/tests/regression/`** (new) or extend **`backend/tests/unit/`** with **`regression_*.py`** naming and a **`fixtures/regression/`** directory — **not** currently a dedicated folder; **enforcement** suite already plays a similar **policy** role.

---

## 10. Smallest realistic Sentinel Phase 1 slice

**Recommendation:** **Path-triggered (or scheduled) “deterministic test selector” + enforcement/golden smoke + alias trace sweep report** — **reporting-only** first.

**Why this slice first (repo-grounded):**

1. **Enforcement** (`backend/tests/enforcement/`) and **golden gate** already encode **non-negotiable** quality rules — Sentinel can **run them when `backend/core/**` or `backend/ssot/**` changes**.
2. **Integration** tests exist but are **skipped** by default PR CI — Sentinel can **surface** that gap as signal or optionally run a **small** integration subset keyed by path.
3. **Alias/regression** tests now exist with **trace-style** keys — a thin Sentinel layer can **append** new rows without architectural churn.
4. Avoids depending on **fragile Playwright** until specs are verified against current UI.

**Explicitly defer:** broad auto-remediation, full persisted DB replay loop, and LLM-dependent gates.

---

## 11. Open blockers / ambiguities

- **`backend/scripts/run_all_tests.py`** referenced by `.github/workflows/validate.yml` — **file not found** in repo (`glob` 0 hits). Nightly job may be **broken** or script renamed (`run_sprint10_tests.py` has a `run_all_tests` **method** only). **Needs human confirmation.**
- **Duplicate test trees** (`tests/` vs `frontend/tests/`) — which are **canonical** for CI and Sentinel indexing?
- **Playwright** specs — **currency** against `HealthIQ AI v5` product strings **not** validated in this audit.
- **`pytest -m "not slow"`** — Sentinel must know **marker** conventions or risk silent omission of important tests.
- **Exact** persisted analysis schema / versioning in production DB — **not** inspected (would need DB or API docs).

---

**End of report.**
