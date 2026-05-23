# LC-S17 — Knowledge Bus Registration and Coverage Framework

**Work package:** LC-S16-17-19  
**Date:** 2026-05-23

## 1. Executive summary

Knowledge Bus promotion tooling exists (`run_knowledge_package.py`, `validate_knowledge_package.py`). Runtime loads **all** package `signal_library.yaml` files without lifecycle gating. This sprint defines lifecycle states, package types, and distinguishes machine-enforced vs documentation-only controls. Machine enforcement added: lifecycle enum, required-file checks, orphan reporter (`validate_kb_package_estate_orphans_v1.py`).

## 2. Current runtime Knowledge Bus path

| Stage | Authority |
|-------|-----------|
| Load | `SignalRegistry` in `signal_evaluator.py` — all `knowledge_bus/packages/*/signal_library.yaml`, excludes `pkg_example` only |
| Promotion | `backend/scripts/run_knowledge_package.py` — writes `knowledge_bus/current/active_package.json`, `latest_knowledge_status.json` |
| Validation | `validate_knowledge_package.py` — manifest, research_brief, signal_library, optional PSI |
| Root cause | `knowledge_bus/root_cause/hypotheses/*.yaml` via `load_root_cause_hypotheses.py` |
| Estate inventory | `knowledge_bus/governance/package_estate_KB-S49_v1.yaml` (descriptive; not runtime gate) |

## 3. Lifecycle states

| State | Entry criteria | Exit criteria | Runtime effect |
|-------|----------------|---------------|----------------|
| **draft** | Package dir created; files incomplete | Passes `validate_knowledge_package.py` | Not loaded |
| **validated** | Validator exit 0; artifacts in `backend/artifacts/knowledge_status.json` | Promoted / marked runtime-loaded | Not loaded until runtime policy added |
| **runtime-loaded** | Present on disk with standard three files; passes signal library schema | Superseded or removed | **Loaded today** by `SignalRegistry` |
| **signal-only** | Standard package without PSI manifest key | PSI promotion | Signals fire; no PSI layer |
| **WHY-enabled** | Manifest `promoted_signal_intelligence` + on-disk PSI YAML | Frontend-surfaced | PSI + root-cause targets; narrative/WHY compilers |
| **frontend-surfaced** | IDL record or narrative section maps asset to retail field | Sentinel-protected | Visible on results journey |
| **Sentinel-protected** | Deterministic regression + Sentinel class registered | — | CI guard |

**Owner/reviewer:** GPT (framework), Claude (audit), Human (merge).

## 4. Package types

| Type | Description |
|------|-------------|
| signal-only | Standard three-file package; signals without PSI |
| WHY-enabled | PSI manifest + `promoted_signal_intelligence.yaml` |
| IDL-display-enabled | IDL record in `interpretation_display_layer_v1` estate |
| lifestyle-modifier | Lifestyle bridge packages (modifier semantics) |
| medication-overlay | Intervention annotation overlays (e.g. statin context) |
| combination-case | Phenotype / interaction map combinations |

## 5. Required files by package type

| Type | Required files |
|------|----------------|
| signal-only | `package_manifest.yaml`, `research_brief.yaml`, `signal_library.yaml` |
| WHY-enabled | Above + `promoted_signal_intelligence.yaml` |
| IDL-display-enabled | IDL record YAML + publish mapping (see IDL publish layer) |
| lifestyle-modifier | signal package + lifestyle bridge contract (documented) |
| medication-overlay | `intervention_annotations` path + safety rules reference |
| combination-case | phenotype map / interaction map entries + backing packages |

## 6. Runtime loading expectations

- **Today:** All non-example packages with valid `signal_library.yaml` load.
- **Future:** Gate `runtime-loaded` by manifest lifecycle field (backlog).

## 7. WHY enablement expectations

- Root-cause hypothesis YAML under `knowledge_bus/root_cause/hypotheses/`.
- `root_cause_compiler_v1` maps `signal_id` → hypothesis loader.
- Narrative LC-S3 assembly consumes `NarrativePayloadV1` with `report_v1.root_cause_v1`.

## 8. Frontend surfacing expectations

- IDL: `interpretation_display_layer_v1.records[]` with `enabled_for_frontend: true`.
- Hero/body: prefer IDL + `narrative_report_v1` over generic fallback (`resultsPageLayout.ts`).
- Domain cards: `consumer_domain_scores[]` only.

## 9. Sentinel expectations

Defect classes registered in `sentinel/packs/escaped_defects_v1.json` pointing to `test_lc_s16_17_19_kb_surface_payload_contract.py`.

## 10. Machine-enforced controls

| Control | Enforcement |
|---------|-------------|
| Lifecycle state enum validity | `kb_lifecycle_contract_v1.LIFECYCLE_STATES` + regression test |
| Standard package required files | `package_has_required_files` sample scan in regression |
| WHY-enabled required files | `WHY_ENABLED_PACKAGE_FILES` + regression on PSI packages |
| Signal library schema | Existing `validate_signal_library.py` (per-package) |
| Orphan package detection | `detect_orphan_packages()` + `validate_kb_package_estate_orphans_v1.py` |
| Frontend contract root keys | `frontend_contract_v1.FRONTEND_CONSUMED_ROOT_KEYS` + regression |

## 11. Documented-now / machine-enforced-later controls

| Control | Backlog |
|---------|---------|
| Runtime gating by lifecycle state | Manifest `lifecycle_state` field + `SignalRegistry` filter |
| Full asset coverage report for active signals | KB-S52+ inventory refresh automation |
| Frontend-surfacing status per WHY-enabled asset | LC-S18 surfacing matrix |
| Root-cause hypothesis metadata validator (repo-wide) | Extend `validate_knowledge_package` orchestration |

## 12. Advisory-only guidance

- Uplift prioritisation in `package_estate_KB-S49_v1.yaml` (ranks legacy → v3).
- Clinical signoff markdown in packages (not a runtime gate).

## 13. Orphan package detection

**Reporter:** `python backend/scripts/validate_kb_package_estate_orphans_v1.py`

As of 2026-05-23, **109** package directories exist on disk that are not listed in `package_estate_KB-S49_v1.yaml` (mostly `pkg_kb52c_*`, `pkg_kb58_*`, `pkg_kb60_*`, `pkg_kb61_*`). **Zero** inventory entries missing on disk.

**Disposition:** Documented drift — inventory refresh is **not** in LC-S16-17-19 scope (no KB content expansion). Reporter returns exit code 1 when drift exists; regression asserts structured report + documentation (not zero drift).

## 14. Coverage reporting

- Phenotype map orphans: `validate_phenotype_map.py`.
- Interaction map orphans: `validate_interaction_map_v1.py`.
- Package estate coverage: pending inventory regeneration (LC-S18).

## 15. How LC-S16 findings affected this framework

- Confirmed runtime loads packages not in inventory → orphan reporter mandatory.
- Confirmed frontend-surfaced path separate from signal-only load → lifecycle states `frontend-surfaced` and `WHY-enabled` distinct.

## 16. Required future validators / backlog items

1. Regenerate `package_estate_KB-S49_v1.yaml` from disk (KB-S52+ batch).
2. Manifest `lifecycle_state` field with validator.
3. Consumer-safe payload filter removing `meta.insight_graph` from retail API (LC-S19 follow-on).
4. Asset coverage matrix: active signal_id → IDL / narrative / domain surfacing status.
