# P1-15 — First Production PSI Opt-In Pilot with Contract STOP Gate

## 1. Contract verification evidence

| Authority question | Answer | Evidence |
|---|---|---|
| Production package store | `knowledge_bus/packages/` | Package manifests and artefacts under per-package directories |
| Package manifest schema | `knowledge_bus/schema/package_manifest_schema.yaml` | Optional `promoted_signal_intelligence` field triggers PSI validation only |
| PSI schema | `knowledge_bus/schema/promoted_signal_intelligence_schema_v1.yaml` | KB-S47d contract |
| Package validator | `backend/scripts/validate_knowledge_package.py` | Orchestrates manifest, research, signal, PSI validators |
| PSI validator | `backend/scripts/validate_promoted_signal_intelligence.py` | Structural PSI compliance |
| Runtime loader consumes production PSI? | **No on launch-critical path** | `backend/tests/unit/test_arch_rt5e_psi_runtime_wiring_decision.py` — orchestrator, signal_evaluator, report_compiler, root_cause_compiler, orchestrator_phases_v1, domain_narrative_wave1, health_system_card_evidence, compiled_hypothesis, load_root_cause_hypotheses do **not** import `load_promoted_signal_intelligence` |
| Effect of opt-in today | **Validation / lifecycle inventory only** | `load_promoted_signal_intelligence_for_package` exists but is not imported by launch-critical modules; `behavioural_impact: NONE` on all opted-in packages |
| Duplicate authority | **No** | Staged pilot copies remain under `generated_pilot/`; production copies are separate governed assets |
| Compile manifest regeneration | **Not required** | Production opt-in uses manifest field + PSI file placement only |

**STOP gate 1 — Runtime boundary:** **PASS.** Opt-in with `behavioural_impact: NONE` does not wire PSI into InsightGraph, scoring, DTOs, frontend, Gemini, or report compilers on current launch-critical paths.

## 2. Existing production opt-in overlap findings

| Metric | Value |
|---|---|
| Production packages with `promoted_signal_intelligence:` before sprint | 20 |
| Package prefix | All `pkg_kb47_*` (Batch 2 hormone/thyroid/CBC subset) |
| PSI files present | 20/20 |
| Package validation | PASS (pre-existing governed activation cohort) |
| `behavioural_impact` | `SIGNAL_RUNTIME_ACTIVATION` on kb47 packages |
| Overlap with 41 staged P1-10/11/12 PSI | **None** — different package IDs and source specs |
| Overlap with 22 P1-14 activation-ready candidates | **None** |

**STOP gate 2 — Existing opt-in conflict:** **PASS.** Existing kb47 opt-ins are a separate governed runtime-activation cohort and do not ambiguously overlap staged pilot estate.

## 3. Candidate mapping summary

Mapping artefact: `P1-15_production_psi_opt_in_mapping.yaml`

| Classification | Count |
|---|---|
| READY_FOR_OPT_IN | 22 |
| BLOCKED_* | 0 |

**Mapping notes:**

- 18 candidates: staged `package_id` matches production directory name exactly.
- 4 candidates: staged `pkg_kb52c_*` maps to production `pkg_kb58_*` via matching `source_spec_id` in compile manifest and production manifest description (single unambiguous match each).

All 22 received pre-opt-in `validate_knowledge_package.py` **PASS**.

## 4. Final opted-in cohort

**22/22** activation-ready candidates opted in:

- PSI copied byte-identically from staged pilot to production package as `promoted_signal_intelligence.yaml`
- `promoted_signal_intelligence: promoted_signal_intelligence.yaml` added to each production `package_manifest.yaml`
- `behavioural_impact: NONE` preserved on all packages
- No changes to `research_brief.yaml` or `signal_library.yaml`

Representative packages: `pkg_kb60_total_cholesterol_high_atherogenic_hypercholesterolemia`, `pkg_kb52c_alt_high_hepatocellular_injury_pattern`, `pkg_kb58_rbc_high_erythrocytosis_pattern`, `pkg_kb52c_ferritin_low_iron_store_depletion`.

## 5. Blocked candidates

No activation-ready candidate was blocked at mapping stage. P1-14 blocked cohorts (9 biomarker, 7 derived, 3 medical-review) were **not** opted in.

## 6. Validation commands and outputs

```powershell
python backend/scripts/validate_knowledge_package.py --package-dir knowledge_bus/packages/<pkg>
python backend/scripts/validate_promoted_signal_intelligence.py --model knowledge_bus/packages/<pkg>/promoted_signal_intelligence.yaml
python backend/scripts/validate_staged_psi_activation_readiness.py
python -c "import yaml; from pathlib import Path; p=Path('docs/sprints/beta_readiness/P1-15_production_psi_opt_in_mapping.yaml'); data=yaml.safe_load(p.read_text(encoding='utf-8')); assert data['work_id']=='P1-15'; assert data['opted_in_count']==22; print('mapping parsed ok')"
```

**Results:**

- Post-opt-in package validation: **22/22 PASS**
- Post-opt-in PSI validation: **22/22 PASS**
- Staged activation-readiness validator (post opt-in):

```text
psi_files_found: 41
compile_manifests_found: 41
production_opt_ins_found: 42
activation_ready_count: 4
blocked_count: 37
top_blocker: NOT_ELIGIBLE_FOR_ACTIVATION (18)
```

Expected regression on staged audit counts: 18 staged packages with matching production `package_id` now report production opt-in (`NOT_ELIGIBLE_FOR_ACTIVATION`). Four staged `pkg_kb52c_*` items mapped to `pkg_kb58_*` production packages remain `ACTIVATION_READY` on staged audit (different production directory name). Hash integrity on staged compile manifests unchanged. No staged `runtime_active: true`.

## 7. Runtime / user-facing activation confirmation

- No `behavioural_impact` changed to `SIGNAL_RUNTIME_ACTIVATION` on opted-in packages
- No orchestrator / scoring / DTO / frontend / Gemini / report compiler changes
- No staged PSI or staged compile manifest edits
- No medical content edits

## 8. Medical content confirmation

All production PSI files are byte-identical copies of staged pilot PSI. No biomarker IDs, signal IDs, or medical wording changed.

## 9. Blocked cohort non-promotion

Zero identity-blocked, derived-marker-blocked, or medical-review-blocked PSI opted in.

## 10. Recommended next product-forward package

**P1-16 — SSOT biomarker identity adjudication for blocked staged PSI cohort**

Resolve `non_hdl`, `wbc`, `lym`, `plt` and supporting alias blockers before opt-in of the 9 biomarker-blocked staged packages; parallel **P1-DERIVED-METRIC-TRANSFERRIN-SAT-1** for 7 iron-panel PSI.

## 11. Business value

First governed production PSI opt-in pilot establishes validation-governed Layer B assets in production packages without launch-critical runtime wiring, enabling future activation sprints on a verified 22-package cohort.
