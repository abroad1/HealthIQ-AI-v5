# HealthIQ AI — Phase 1 Sentinel: Implementation Report

**Report date:** 2026-05-03  
**Produced by:** Claude Code  
**Brief reference:** `docs/testing/brief for HealthIQ AI Phase 1 Sentinel.md`  
**Background audit:** `docs/testing/healthiq_sentinel_repo_audit_v1.md`  
**Repo-grounded:** All findings cite observed file paths. No assumptions made.

---

## 1. Scope Delivered

### What was built

| Component | Status | Description |
|---|---|---|
| A. Changed-file classifier | Built | `sentinel/classifier.py` — path-based surface/risk classifier |
| B. Alias/canonical sweep | Built | `backend/tests/regression/test_alias_canonical_sweep.py` — full registry sweep |
| C. Escaped-defect regression pack | Built | 5 named tests in `backend/tests/regression/` + pack manifest |
| D. Frontend slug/internal-label leakage guard | Built | `backend/tests/regression/test_slug_leakage_regression.py` + `frontend/tests/regression/slug-leakage-guard.test.ts` |
| E. Structured report output | Built | `sentinel/sentinel_runner.py` — JSON report per run to `sentinel/reports/` |

### What was intentionally not built

Per brief scope limits:

- No auto-remediation or auto-fix
- No branch creation or PR comment bots
- No merge blocking
- No full persisted-result replay harness (deferred to Phase 2+)
- No Playwright orchestration
- No Wave 1 coherence full coverage (Playwright-dependent — Phase 2+)
- No test-estate cleanup
- No broad dependency analysis
- No stale test removal

---

## 2. Files Added / Changed

### New files

| File | Purpose |
|---|---|
| `sentinel/classifier.py` | Changed-file risk classifier |
| `sentinel/sentinel_runner.py` | Sentinel CLI runner + JSON report writer |
| `sentinel/packs/escaped_defects_v1.json` | Named escaped-defect pack manifest |
| `sentinel/reports/.gitkeep` | Report output directory (placeholder) |
| `sentinel/state/.gitkeep` | State directory (placeholder) |
| `backend/tests/regression/__init__.py` | Package marker |
| `backend/tests/regression/test_alias_canonical_sweep.py` | Full alias registry sweep |
| `backend/tests/regression/test_ggt_alias_regression.py` | GGT alias miss regression |
| `backend/tests/regression/test_bilirubin_alias_regression.py` | Bilirubin canonical mismatch regression |
| `backend/tests/regression/test_slug_leakage_regression.py` | Backend slug leakage static guard |
| `backend/tests/regression/test_wave1_contradiction_status.py` | Wave 1 contradiction status/gap placeholder |
| `backend/tests/regression/test_persisted_result_replay_status.py` | Persisted replay gap placeholder + golden corpus check |
| `frontend/tests/regression/slug-leakage-guard.test.ts` | Frontend slug leakage static guard |

### Changed files

| File | Change | Reason |
|---|---|---|
| `backend/pyproject.toml` | Added `regression` marker | `--strict-markers` blocks any unregistered `@pytest.mark.regression` at collection time. The authoritative pytest config for `backend/` is `backend/pyproject.toml` (discovered via `configfile: pyproject.toml` from pytest's rootdir resolution). |
| `pytest.ini` | Added `regression` marker | Belt-and-suspenders for root-level invocations. |
| `frontend/jest.config.js` | Added `tests/regression` to `testMatch` | Jest's default `testMatch` did not include `tests/regression/` — tests in that directory would not be discovered without this addition. |

---

## 3. Changed-File Classifier

**Location:** `sentinel/classifier.py`

### Surfaces recognised

| Surface ID | Example paths | Risk assigned |
|---|---|---|
| `parser/alias/canonical` | `backend/core/canonical/`, `backend/services/parsing/` | STANDARD |
| `SSOT/canonical_authority` | `backend/ssot/` | HIGH |
| `analytics/scoring/signal` | `backend/core/pipeline/`, `backend/core/analytics/`, `backend/core/scoring/`, `backend/core/clustering/`, `backend/core/insights/` | HIGH (pipeline/analytics/scoring/clustering), STANDARD (insights) |
| `frontend/trust` | `frontend/app/components/results/`, `frontend/lib/narrativeRuntimePresentation.ts`, `frontend/lib/primaryFindingShaping.ts`, `frontend/lib/`, `frontend/app/components/ui/`, `frontend/app/components/layout/` | STANDARD (results/shaping), LOW (ui/layout) |
| `persistence/snapshot` | `backend/core/dto/`, `backend/core/models/`, `backend/core/snapshot/` | STANDARD |
| `governance/control_plane` | `backend/scripts/run_work_package.py`, `backend/scripts/golden_gate_local.py`, `automation_bus/`, `docs/` | HIGH (scripts/automation_bus), LOW (docs) |
| `knowledge_bus/intelligence` | `backend/core/knowledge/`, `knowledge_bus/packages/`, `knowledge_bus/research/` | HIGH (loaders/packages), LOW (research briefs) |

### How conservative it is

**Conservative by design.** Rules:
- Anything unrecognised defaults to `SURFACE_GOVERNANCE_CONTROL_PLANE` at `RISK_STANDARD` (not LOW).
- `knowledge_bus/packages/` is HIGH even if a change is a research-brief YAML — because the classifier cannot inspect content, it widens.
- `backend/core/insights/` is STANDARD (not LOW) because it straddles the Layer B/C boundary.
- Escalation triggers (`ESCALATION_SURFACES`) include analytics, SSOT, control-plane, and KB intelligence.

Per-surface test recommendation is exposed via `ClassificationResult.recommended_tests()`.

---

## 4. Alias / Canonical Sweep

**Location:** `backend/tests/regression/test_alias_canonical_sweep.py`

### Checks that run

| Test | What it checks |
|---|---|
| `test_registry_file_exists_and_loads` | SSOT registry YAML is present and parses |
| `test_every_alias_resolves_to_declared_canonical` | For every alias in the registry, `AliasRegistryService.resolve(alias)` returns the declared `canonical_id` |
| `test_canonical_id_resolves_to_itself` | Every `canonical_id` resolves to itself (identity invariant) |
| `test_no_alias_resolves_to_unmapped` | No alias returns an `unmapped_*` sentinel (unmapped = resolver fallback for unknown input) |

### GGT and bilirubin coverage

**GGT — explicitly covered.** `test_every_alias_resolves_to_declared_canonical` includes the misspelled runtime key `Gamma-GlutamilTransferase GGT (Venous)` (and its lowercased normalised form `gamma-glutamiltransferase_ggt_(venous)`) because these entries are present in `backend/ssot/biomarker_alias_registry.yaml:292–296`. The sweep iterates every alias in the registry, so both the correctly-spelled and misspelled variants are covered automatically.

**Bilirubin — explicitly covered.** The alias `bilirubin_total_(venous)` is present in the registry (`backend/ssot/biomarker_alias_registry.yaml:104`) with `canonical_id: bilirubin`. The sweep asserts this resolves correctly on every run.

---

## 5. Escaped-Defect Pack

**Manifest:** `sentinel/packs/escaped_defects_v1.json`

### Actively guarded (deterministic checks)

| Defect class | Guard | Test file | Evidence type |
|---|---|---|---|
| `ggt_alias_miss` | Active | `test_ggt_alias_regression.py` | 9 deterministic alias assertions using exact original failure inputs |
| `bilirubin_canonical_mismatch` | Active | `test_bilirubin_alias_regression.py` | 8 assertions including the pre-fix wrong canonical regression check |
| `slug_leakage` | Active | `test_slug_leakage_regression.py` | Static source scan of all `results/` `.tsx` files and narrative shaping libs |

### Status/reporting placeholders

| Defect class | Guard | Test file | Why placeholder |
|---|---|---|---|
| `wave1_contradiction` | Status-reporting | `test_wave1_contradiction_status.py` | Full deterministic guard requires Playwright rendering of domain card vs score alignment — Phase 2+ |
| `persisted_result_replay` | Status-reporting | `test_persisted_result_replay_status.py` | Full replay harness requires DTO schema comparison + Playwright frontend load — Phase 2+ |

The placeholder tests pass in Phase 1. They surface the gaps explicitly in CI output and in Sentinel reports rather than silently missing them.

---

## 6. Frontend Slug / Internal-Label Guard

**Locations:**
- `backend/tests/regression/test_slug_leakage_regression.py` — runs via pytest, reads frontend source from Python
- `frontend/tests/regression/slug-leakage-guard.test.ts` — runs via Jest, native TypeScript/Node context

### Surfaces checked

- `frontend/app/components/results/*.tsx` — all 14 customer-facing results components
- `frontend/app/lib/narrativeRuntimePresentation.ts`
- `frontend/app/lib/primaryFindingShaping.ts`

### Forbidden patterns

| Pattern | Description |
|---|---|
| `ph_*_v*` string literals | Internal phenotype ID format (e.g. `"ph_metabolic_early_ir_v1"`) |
| `FastAPI` | Backend framework implementation string |
| `unmapped_` | Alias resolver sentinel value (leaked resolver error) |
| `internal_id:` | YAML/dict key appearing as rendered text |

Both guards (backend pytest + frontend Jest) scan source text statically — no rendering or browser required.

---

## 7. Report Output

### Report schema

Each `sentinel_runner.py` run writes a JSON report to `sentinel/reports/sentinel_run_<id>.json`.

```json
{
  "sentinel_version": "1.0.0-phase1",
  "run_id": "<8-char uuid>",
  "utc": "<ISO-8601>Z",
  "trigger_type": "changed_files | surface | defect_class | all_regression",
  "branch": "<git branch>",
  "changed_files": ["<path>", ...],
  "classified_files": [{"path": "", "surface": "", "risk": "", "reason": ""}, ...],
  "classified_surfaces": ["<surface>", ...],
  "tests_selected": ["<path>", ...],
  "tests_run": ["<path>", ...],
  "test_counts": {"passed": 0, "failed": 0, "errors": 0, "skipped": 0},
  "pytest_exit_code": 0,
  "issues_found": [],
  "coverage_gaps": [],
  "escaped_defect_pack_status": {
    "<defect_class>": {"guard_type": "", "status": "", "test_file": ""}
  },
  "governance_escalation_required": false,
  "auto_remediation_attempted": false,
  "sentinel_note": "Phase 1 — report only. ..."
}
```

### Output location

`sentinel/reports/` — outside `automation_bus/`. Reports are written by the runner but never by any governance script.

### Example invocations

```bash
# Run full regression pack
python sentinel/sentinel_runner.py --all

# Run against changed files
python sentinel/sentinel_runner.py --changed-files backend/core/canonical/alias_registry_service.py

# Run a specific defect class
python sentinel/sentinel_runner.py --defect-class ggt_alias_miss

# Run a specific surface
python sentinel/sentinel_runner.py --surface parser/alias/canonical
```

---

## 8. Deterministic Proof

### Evidence attached to failures

Each failing test assertion includes:
- `input`: exact alias string or source file path passed to the check
- `expected`: the declared canonical or the absence of a forbidden pattern
- `actual`: what the resolver returned or what the regex found
- `pass/fail`: Python assert failure with embedded context string
- `customer impact`: stated in the docstring or assertion message (e.g. "GGT absent from liver panel → liver domain underpowered")
- `governance escalation`: stated in the docstring for each test class

No test relies on LLM judgement or heuristic scoring for its pass/fail verdict.

### How coverage gaps are surfaced

Coverage gaps appear in two places:
1. `sentinel/reports/sentinel_run_<id>.json` → `coverage_gaps` array
2. Placeholder tests (`test_wave1_contradiction_status.py`, `test_persisted_result_replay_status.py`) emit `pytest.skip` with explicit gap text when prerequisite conditions are unmet, making the gap visible in CI output

---

## 9. Governance Boundaries Preserved

### What Sentinel does not mutate

- `automation_bus/` artefacts — read-only for Sentinel
- `backend/ssot/` — read-only (alias registry read by tests, not modified)
- `knowledge_bus/` — not touched by any Sentinel test
- `backend/scripts/run_work_package.py`, `golden_gate_local.py` — not modified
- `frontend/app/` source files — read by static checks, never written

### What still escalates

Sentinel reports `governance_escalation_required: true` in its JSON report when:
- Changed files map to HIGH-risk surfaces (`analytics/scoring/signal`, `SSOT/canonical_authority`, `governance/control_plane`, `knowledge_bus/intelligence`)
- Any regression test fails (issues_found non-empty)

Sentinel **does not** approve its own findings. Governance review remains mandatory for HIGH-risk surfaces regardless of test result.

---

## 10. Tests Run

### Backend regression pack — run 2026-05-03

```
python -m pytest backend/tests/regression/ -m regression -v
```

**32 tests collected, 32 passed (4.85s)**

| Test file | Tests | Status |
|---|---|---|
| `test_alias_canonical_sweep.py` | 4 | PASS |
| `test_bilirubin_alias_regression.py` | 8 | PASS |
| `test_ggt_alias_regression.py` | 9 | PASS |
| `test_persisted_result_replay_status.py` | 4 | PASS |
| `test_slug_leakage_regression.py` | 5 | PASS |
| `test_wave1_contradiction_status.py` | 2 | PASS |

**Key findings from this run:**
- All active GGT alias checks pass — original failure input `"Gamma-GlutamilTransferase GGT (Venous)"` resolves correctly to `ggt`
- All bilirubin checks pass — `bilirubin_total_(venous)` resolves to `bilirubin`, not `total_bilirubin`
- Slug leakage guard — 0 forbidden patterns found in results components or shaping libs
- Wave 1 contract doc found at `docs/DOMAIN_NARRATIVE_CONTRACT_WAVE1.md` — passes structural check
- Golden run corpus exists (50+ timestamped runs) — 5 most recent timestamped runs pass minimum schema sanity

**Defects discovered during test authoring:**
- `verify_non_collision_a` and `verify_collision_test_b` directories in `backend/artifacts/golden_runs/` are diagnostic/fixture payloads (schema: `{error_payload, error_type, fixture, run_id, status}`), not standard analysis results. These are correctly excluded from the replay sanity check by filtering to UTC-timestamped directories only.

### Frontend Jest tests — not executed in this run

`frontend/tests/regression/slug-leakage-guard.test.ts` requires `cd frontend && npm test`. It is discoverable via the updated `jest.config.js` `testMatch`. Static source reads use Node `fs` — no rendering dependency.

---

## 11. Known Limits Intentionally Deferred

| Item | Reason | Phase |
|---|---|---|
| Wave 1 domain/score narrative coherence guard | Requires Playwright to render the full results page and compare visible text across sections | Phase 2+ |
| Persisted-result DTO schema comparison harness | Requires a DTO schema validator to compare golden run JSON against the current `backend/core/models/results.py` schema | Phase 2+ |
| Frontend mock sync check (`analysis-result.json` vs backend DTO) | Requires generating the current DTO schema and diffing against `frontend/app/lib/mock/analysis-result.json` | Phase 2+ |
| Playwright: render stored result and scan visible text for slugs | Backend static check covers source; runtime rendering requires Playwright | Phase 2+ |
| Full `sentinel_runner.py` pytest output parsing | Current output parser uses line-scanning heuristic on `-q` output. A pytest JSON plugin (`pytest-json-report`, already in backend deps) would give structured pass/fail per test | Phase 2 quality improvement |
| Automated git-hook trigger | Brief §3 allows optional scheduled sweep; not wired to git hooks in Phase 1 | Optional Phase 2 |
| `tests_new/` duplication audit | Audit flagged 16 files of uncertain status; not investigated or cleaned in this sprint | Separate cleanup sprint |

---

## 12. Uncommitted / Not Merged

All work is uncommitted and not merged to `main`. No work package was started via the Automation Bus kernel for this Sentinel slice.

The following untracked/modified files are the complete Phase 1 footprint:

```
sentinel/classifier.py                                   (new)
sentinel/sentinel_runner.py                              (new)
sentinel/packs/escaped_defects_v1.json                   (new)
sentinel/reports/.gitkeep                                (new)
sentinel/state/.gitkeep                                  (new)
backend/tests/regression/__init__.py                     (new)
backend/tests/regression/test_alias_canonical_sweep.py   (new)
backend/tests/regression/test_ggt_alias_regression.py    (new)
backend/tests/regression/test_bilirubin_alias_regression.py (new)
backend/tests/regression/test_slug_leakage_regression.py (new)
backend/tests/regression/test_wave1_contradiction_status.py (new)
backend/tests/regression/test_persisted_result_replay_status.py (new)
frontend/tests/regression/slug-leakage-guard.test.ts     (new)
backend/pyproject.toml                                   (modified — regression marker added)
pytest.ini                                               (modified — regression marker added)
frontend/jest.config.js                                  (modified — tests/regression added to testMatch)
```

No product code was modified. No governed assets (`backend/ssot/`, `knowledge_bus/`, `automation_bus/`) were written.

---

## Acceptance Criteria Status

| Criterion | Status |
|---|---|
| 1. Classify changed files into sensible broad risk surfaces | Met — `sentinel/classifier.py` |
| 2. Run or select a narrow alias/canonical sweep | Met — `test_alias_canonical_sweep.py` |
| 3. Run or report the escaped-defect regression pack | Met — 3 active, 2 status-reporting with explicit gap disclosure |
| 4. Detect/report frontend slug/internal-label leakage on scoped result surfaces | Met — backend pytest + frontend Jest static checks |
| 5. Produce a structured report for each run | Met — `sentinel/sentinel_runner.py` writes JSON to `sentinel/reports/` |
| 6. Does not modify product code or governed assets | Met — verified; all Sentinel files are new |
| 7. Clearly reports coverage gaps where proof is inadequate | Met — placeholder tests + `coverage_gaps` field in report |
| 8. Remains narrow and report-only | Met — no auto-remediation, no branch creation, no gate mutation |

---

*Report complete. All findings are repo-grounded. All 32 regression tests pass as of 2026-05-03.*
