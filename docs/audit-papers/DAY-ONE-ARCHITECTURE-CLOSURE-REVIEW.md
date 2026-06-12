# Day-One Architecture Closure Review

**Review date:** 2026-06-12  
**Reviewer:** Claude Code (Sonnet 4.6)  
**Scope:** Read-only post-BATCH2-CONTEXT-COMPLETION-1 Wave 1 launch governance assessment  
**Branch reviewed:** `main` (HEAD `edcec857`)

---

## Executive verdict

**ACCEPTED_WITH_CONDITIONS**

The HealthIQ AI day-one architecture is sufficiently safe, governed, traceable, and guarded for Wave 1 launch. All programmatic guardrails pass. All validators pass. No raw research reads at runtime. Context-dependent packages are fail-closed and inactive. The live results path is render-only.

Conditions are not launch blockers under the Wave 1 scope as currently defined — they are activation prerequisites that must be satisfied before any context-dependent package can be activated, and post-launch hardening items that do not affect the live product today.

```
ACCEPTED_WITH_CONDITIONS

Condition C-1: CF-BATCH2-010 androgen clinical sign-off must exist as a repo artefact before
               any androgen activation sprint is authorised.
Condition C-2: ARCH-ORCH-RESTRUCTURE-1 orchestrator phase restructuring must be completed
               before any context-dependent package is activated (whether androgen, FT3 low,
               or any future context-dependent cohort).
Condition C-3: FT3 low enable_lower_bound: false and missing thyroid_medication_disclosed
               metadata must be explicitly resolved before FT3 low activation is considered.
Condition C-4: ClusterInsightPanel frontend clinical inference code must be removed or
               refactored before ClusterInsightPanel is imported in any live results page.
```

---

## Repository baseline

| Item | Value |
|------|-------|
| Branch | `main` |
| HEAD | `edcec857df8ce3ffd0cc34fb221a397e259d7ec1` |
| Working tree | Clean (no uncommitted changes) |
| BATCH2-CONTEXT-COMPLETION-1 merged | **Yes** — top of git log |

**BATCH2-CONTEXT-COMPLETION-1 merge confirmed.** This review is a full (not preliminary) audit.

Recent commits confirm the full context-runtime stream is present:
```
edcec85 chore(bus): BATCH2-CONTEXT-COMPLETION-1 kernel COMPLETE
bbb20f4 feat(context): implement Batch 2 disclosed runtime semantics
96d4925 chore(bus): activate BATCH2-CONTEXT-COMPLETION-1
4eca922 chore(bus): CONTEXT-CLEARANCE-1 kernel COMPLETE
86e2eb3 chore(bus): CONTEXT-CLEARANCE-1 kernel IN_PROGRESS
```

---

## Source documents inspected

| File | Present | Notes |
|------|---------|-------|
| `docs/architecture/ADR-RT-001_research_to_runtime_day_one_architecture.md` | Yes | ACCEPTED 2026-05-28 |
| `docs/sprints/healthiq_day_one_architecture_rework_sprint_plan_FINAL.md` | Yes | Full sprint 0–6 plan |
| `docs/sprints/launch_core_carry_forward_register.md` | Yes | All items read |
| `docs/audit-papers/CONTEXT-RUNTIME-1_…` | Yes | status: IMPLEMENTATION_COMPLETE |
| `docs/audit-papers/CONTEXT-THREADING-1_…` | Yes | status: IMPLEMENTATION_COMPLETE |
| `docs/audit-papers/CONTEXT-CLEARANCE-1_…` | Yes | status: IMPLEMENTATION_COMPLETE |
| `docs/audit-papers/BATCH2-CONTEXT-COMPLETION-1_runtime_semantics_…` | Yes | status: IMPLEMENTATION_COMPLETE_NO_ACTIVATION |
| `docs/audit-papers/BATCH2-CONTEXT-COMPLETION-1_architecture_delta_report.md` | Yes | Read |
| `knowledge_bus/governance/runtime_context_requirements_model_v1.yaml` | Yes | runtime_consumed: true |
| `knowledge_bus/governance/runtime_context_semantics_model_v1.yaml` | Yes | runtime_consumed: false (clearance only) |
| `knowledge_bus/governance/context_runtime_execution_register_v1.yaml` | Yes | 0 activated; 9 gated |
| `knowledge_bus/governance/batch2_context_clearance_register_v1.yaml` | Yes | 0 eligible; 8 BLOCKED_PENDING_CLINICAL_SIGNOFF |
| `knowledge_bus/governance/batch2_remaining_blockers_execution_register_v1.yaml` | Yes | 11 packages; all blocked |
| `knowledge_bus/governance/batch2_remainder_resolution_register_v1.yaml` | Yes | 14 investigated |
| `knowledge_bus/governance/batch2_androgen_panel_medical_review_v1.yaml` | Yes | 8 frames reviewed |
| `knowledge_bus/governance/batch2_androgen_context_modifier_binding_v1.yaml` | Yes | Governance binding only; runtime_active=false |
| `knowledge_bus/governance/medical_frame_identity_index_v1.yaml` | Yes | Index head read |
| `backend/scripts/validate_day_one_architecture.py` | Yes | Run — PASS |
| `backend/tests/architecture/test_day_one_architecture_guardrails.py` | Yes | Run — PASS |
| `sentinel/packs/day_one_architecture_guardrails_v1.json` | Yes | 6 guarded defect classes |
| `docs/architecture/intelligence_authority_inventory.md` | Yes | Research NOT runtime-consumed |
| `docs/architecture/research_to_runtime_traceability_matrix.md` | Present (not re-read; superseded by ARCH-RT-5 audit) | |
| `docs/architecture/package_generation_inventory.md` | Present | |
| `docs/architecture/activation_compile_gap_report.md` | Yes | Key gap items documented |
| `docs/architecture/root_cause_registry_inventory.md` | Present | |
| `docs/architecture/psi_coverage_and_manifest_opt_in_report.md` | Yes | PSI runtime-dead confirmed |
| `docs/architecture/legacy_package_retirement_candidates.md` | Present | |
| `docs/audit-papers/ARCH-RT-6_day_one_architecture_acceptance_audit.md` | Yes | accepted_for_wave1_launch |
| `docs/architecture/ARCH-RT-5_full_regeneration_and_launch_gate_report.md` | Yes | Governance gate complete |

---

## Validators and test evidence

### Appendix A output (full)

```
python backend/scripts/run_architecture_validation_gate.py
───────────────────────────────────────────────────────────
validation_status: PASS   (medical_frame_identity_index)
errors: 0
validation_status: PASS   (context_modifier_catalogue)
errors: 0
day_one_architecture_validation: PASS
medical_intelligence_architecture_validation: PASS
[architecture-gate] validate_medical_frame_identity_index
[architecture-gate] validate_context_modifier_catalogue
[architecture-gate] validate_day_one_architecture
[architecture-gate] validate_medical_intelligence_architecture
[architecture-gate] pytest_architecture_guardrails
[architecture-gate] pytest_governance_regression
architecture_validation_gate: PASS

python backend/scripts/validate_day_one_architecture.py
───────────────────────────────────────────────────────────
day_one_architecture_validation: PASS

python backend/scripts/validate_medical_frame_identity_index.py \
  --index knowledge_bus/governance/medical_frame_identity_index_v1.yaml
───────────────────────────────────────────────────────────
validation_status: PASS
errors: 0

python backend/scripts/validate_context_modifier_catalogue.py \
  --catalogue knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml
───────────────────────────────────────────────────────────
validation_status: PASS
errors: 0

python -m pytest backend/tests/architecture/test_day_one_architecture_guardrails.py -q
───────────────────────────────────────────────────────────
.... [100%]
4 passed

python -m pytest backend/tests/regression/test_runtime_context_evaluation.py -q
───────────────────────────────────────────────────────────
................... [100%]
19 passed

python -m pytest backend/tests/regression/test_context_threading.py -q
───────────────────────────────────────────────────────────
........ [100%]
8 passed

python -m pytest backend/tests/governance/test_batch2_context_clearance_register.py \
               backend/tests/governance/test_runtime_context_semantics_model.py -q
───────────────────────────────────────────────────────────
.......... [100%]
10 passed
```

**Commands not present / not run:**
- `python backend/scripts/validate_day_one_architecture.py` — present and run (PASS above)
- `python backend/scripts/run_architecture_validation_gate.py` — present and run (PASS above)

**Skipped per architecture-gate log:** `test_medical_intelligence_architecture_sentinels.py:67` — self-skip when full gate already executed (expected behaviour).

---

## ADR-RT-001 alignment

**Verdict: ALIGNED (with one documented interim deviation)**

ADR-RT-001 accepted target pipeline:
```
investigation_spec (validated)
  → governed compile (manifest-emitting)
    → package triple + optional PSI + hypothesis artefact + card evidence artefact
      → thin runtime loaders
        → presentation-safe DTOs
          → frontend render-only
```

### Current state vs target

| Layer | Target | Current state | Gap |
|-------|--------|---------------|-----|
| Research authority | investigation_spec v3.0.0 only | `investigation_spec` corpus exists; not read at runtime | Governed |
| Compile | manifest-emitting governed compiler | Pilot manifests exist (ARCH-RT-3/4); no estate-wide activation compiler | Classified deferred |
| Package triple | compiled artefacts | Mixed: 1 compiled card (glycaemic), 1 compiled hypothesis (vitamin_d, shadow), 6 hard-coded Wave 1 subsystems (classified legacy), 40 root-cause YAML (classified legacy) | Acceptable Wave 1 residual |
| Runtime loaders | thin loaders receiving governed inputs | SignalRegistry/Evaluator (signal_library.yaml); root_cause_compiler_v1.py (YAML); wave1_subsystem_evidence.py (hard-coded, classified legacy) | PSI runtime-dead (deferred, non-blocking); hard-coded card evidence classified |
| DTOs | presentation-safe | Pydantic models; no raw source_trace exposed to frontend | PASS |
| Frontend | render-only | Live results path render-only; ClusterInsightPanel (not live) has inference residual | PASS with residual |

### Newly merged work alignment check

BATCH2-CONTEXT-COMPLETION-1 changes:
- `runtime_context_evaluator.py`: added `disclosed` requirement mode — deterministic, no LLM reasoning, no threshold changes. **ALIGNED.**
- 6 `signal_library.yaml` files: disclosed key reclassification — metadata only, no clinical content changes. **ALIGNED.**
- Governance registers: updated; no runtime consumption. **ALIGNED.**

No newly merged work violates ADR-RT-001.

---

## Runtime raw research read assessment

**Verdict: PASS**

### Evidence

| Search target | Locations searched | Result |
|--------------|-------------------|--------|
| `Pass_3` in runtime modules | `backend/core/`, `backend/app/` | None found in runtime pipeline |
| `investigation_spec` imports | `backend/core/pipeline/`, `backend/core/analytics/` | None |
| `Batch_.*_Pass_3` | runtime paths | None |
| `knowledge_bus/research/investigation_specs` | runtime paths | None |

### PSI translator status

`backend/core/knowledge/investigation_spec_to_promoted_signal.py` exists and references investigation specs in its function signature. It is **compile-only**:
- Imported by: tests, validators, and the KB ingest toolchain only.
- Not imported by: `orchestrator.py`, `signal_evaluator.py`, `domain_score_assembler.py`, or any pipeline module.
- Confirmed by: grep of all runtime paths; `validate_day_one_architecture.py` sentinel rule 25-26 (`day_one_no_runtime_investigation_spec_reads`) passes.

### `package_provenance_scan_v1.py` clarification

`backend/core/knowledge/package_provenance_scan_v1.py` references `knowledge_bus/research/study_` paths. It is a governance scan tool (imports `launch_estate_v1`), not imported by any pipeline or evaluator module. Not a runtime violation.

---

## Frontend render-only assessment

**Verdict: PASS (with one non-live residual — see below)**

### Live results path

`ClusterSummary` (imported by `frontend/app/(app)/results/page.tsx:15`) is render-only:
- Renders backend-provided DTO fields: `name`, `description`, `recommendations`, `severity`, `score`, `confidence`, `biomarkers`, `category`, `systemEducationalExplainer`.
- Score/severity colour functions are visual helpers mapping backend-provided numeric values to CSS classes — not clinical inference.
- `cluster.recommendations` is a backend-provided string array from the DTO — not generated in the frontend.

`BiomarkerDials.tsx`: `interpretation` field is a backend-provided DTO field rendered via `retailInterpretationForExpansion()` (a presentation safety function) — not frontend-generated clinical text.

ARCH-RT-6 sentinel guard `day_one_frontend_render_only` covers `Wave1SubsystemEvidenceSection` (no marker-role inference helpers) — **PASS**.

### Non-live residual — ClusterInsightPanel

**Finding:** `frontend/app/components/clusters/ClusterInsightPanel.tsx` contains `getClinicalRecommendations()` (lines 88–121) which generates clinical copy from cluster name pattern matching:

```typescript
if (cluster.severity === 'critical' || cluster.severity === 'high') {
  recommendations.push('Immediate medical attention recommended');
}
if (cluster.name.toLowerCase().includes('cardiovascular')) {
  recommendations.push('Focus on heart-healthy diet and exercise');
}
// etc.
```

This is frontend medical inference. However:
- `ClusterInsightPanel` is **not imported by any live results page.** The results page imports `ClusterSummary` only.
- `ClusterInsightPanel` is exported from `frontend/app/components/clusters/index.ts` — it is reachable if imported.
- Grep of all page/route files confirms no live page imports `ClusterInsightPanel`.

**Classification: POST_LAUNCH_HARDENING** — not reachable in the live product today, but the code exists and is potentially importable. Classified as Condition C-4: must be removed or refactored before `ClusterInsightPanel` is imported in any live page.

The ARCH-RT-6 sentinel perimeter does not extend to this component (it guards `Wave1SubsystemEvidenceSection`). The sentinel perimeter should be extended post-launch to cover cluster components if they are promoted to the live results path.

---

## Context-dependent Batch 2 status

### Disclosed-context semantics

BATCH2-CONTEXT-COMPLETION-1 implemented:
1. `build_runtime_context_snapshot()` records `*_disclosed` and `*_status_disclosed` keys when questionnaire fields are answered.
2. `evaluate_runtime_context_requirements()` supports `disclosed` requirement mode (fail-closed unless disclosure key is `True`).
3. 6 packages remediated: `present` requirement on medication/clinical fields reclassified to `disclosed` keys.

Backward compatibility maintained: existing `present` and `lab_range_boundary` branches unchanged.

### Package activation status

| Package group | Count | Status |
|--------------|-------|--------|
| Androgen packages | 8 | `inactive`, `compiled_not_promoted`, fail-closed gated |
| FT3 low | 1 | `inactive`, `compiled_not_promoted`, blocked |
| **Total context-dependent** | **9** | **0 activated** |

All activation STOP gates confirm: **approval phrase not received; 0 packages activated.**

### Androgen position

All 8 androgen packages:
- `clearance_decision: BLOCKED_PENDING_CLINICAL_SIGNOFF`
- `activation_eligibility: false`
- No clinical sign-off artefact in repo
- Disclosed semantics remediated (BATCH2-CONTEXT-COMPLETION-1)
- Runtime fail-closed context gate implemented

**Classification: CONDITIONAL_BLOCKER**

These packages are not active and cannot fire. They do not block Wave 1 launch. They block any future androgen activation sprint until CF-BATCH2-010 is resolved with a repo artefact and ARCH-ORCH-RESTRUCTURE-1 is complete.

### FT3 low position

FT3 low (`pkg_kb47_free_t3_low_low_t3_syndrome`):
- `clearance_decision: DEFERRED_NON_LAUNCH_CRITICAL`
- `activation_layer_blockers: [enable_lower_bound_false]`
- Missing `thyroid_medication_disclosed` in package metadata (non-misclassification gap — BATCH2-CONTEXT-COMPLETION-1 residual observation)
- Active thyroid trio (FT3 high, FT4 high/low) is runtime-active with TSH gates and covers thyroid Wave 1 scope

**Classification: ACCEPTABLE_WAVE1_RESIDUAL** — FT3 low is explicitly deferred and non-launch-critical relative to the active thyroid subset.

---

## Carry-forward classification table

| ID | Current status | Current launch blocker flag | Claude reassessed classification | Rationale | Recommended action |
|----|---------------|----------------------------|---------------------------------|-----------|-------------------|
| CF-MEDREV2-001 | Open | No | ACCEPTABLE_WAVE1_RESIDUAL | No live users; current-context regeneration works for Wave 1. Profile lineage is a post-launch determinism hardening concern. | Post-launch result lineage sprint |
| CF-MEDREV2-002 | Open | No | POST_LAUNCH_HARDENING | v1 lineage acceptable for Wave 1; proper lineage table needed before multi-version history claims. | Versioned result lineage sprint |
| CF-MEDREV2-004 | Open | No | ACCEPTABLE_WAVE1_RESIDUAL | Test is weaker than ideal but product behaviour is correct. | Test-hardening sprint |
| CF-KBUTIL1-001 | Open | No | POST_LAUNCH_HARDENING | Manual compile path from KB-UTIL-1 works for pilot; estate-wide pipeline needed before scaled regeneration. | KB-UTIL-2 or ARCH-RT compile hardening |
| CF-KBUTIL1-002 | Open | No | POST_LAUNCH_HARDENING | Hypothesis/contradiction surfacing deferred; LAYER-B-1 prepared foundation; safe surfacing requires governed sprint. | Research intelligence surfacing sprint |
| CF-LAYERB1-001 | Open | No | POST_LAUNCH_HARDENING | Full NarrativePayloadV1 persistence deferred from LAYER-B-1; needed before LLM translation sprint (no LLM translation sprint planned for Wave 1). | LLM-NAR-0 design sprint |
| CF-ARCHLEG1-001 | Open | No | ACCEPTABLE_WAVE1_RESIDUAL | 40 YAML / 1 compiled root-cause; migration_required but not launch-blocking per ARCH-LEGACY-1 audit. Guarded by validator. | ARCH-RT-4+ migration programme |
| CF-ARCHLEG1-004 | Open | No | POST_LAUNCH_HARDENING | CRP guards added; full promotion inventory still open. Does not affect Wave 1 live signals. | ARCH-RT-4+ |
| CF-CREATININE-001 | Open | No | POST_LAUNCH_HARDENING | s24 eGFR/potassium overrides not in kb52c; albuminuric frame not indexed. Required before s24 retirement. | CREATININE-PASS3-ENRICH-1 |
| CF-CONTEXT-MOD-2 | Open | No | CONDITIONAL_BLOCKER | Modifier evaluation binder not implemented. Not a Wave 1 launch blocker (no context-dependent packages active). Blocks any activation of context-dependent packages. | CONTEXT-MOD-2 sprint before any activation |
| CF-PASS3FRAME-002 | Open | No | POST_LAUNCH_HARDENING | 7 packages blocked_pending_pass3_enrichment. Not Wave 1 active signals. | CREATININE-PASS3-ENRICH-1+ |
| CF-PASS3FRAME-003 | Open | No | ACCEPTABLE_WAVE1_RESIDUAL | Bulk ROUTE_A promotion paused; ARCH-SENTINEL-1 sentinel guards naive promotion gate. Safe for Wave 1. | Maintain pause; resolve CF-PASS3FRAME-002 first |
| CF-MRIMPROVE-002 | Deferred | No | POST_LAUNCH_HARDENING | kb45 provenance ambiguity; packages classified; not a runtime risk. | KB hygiene sprint |
| CF-MRIMPROVE-003 | Deferred | No | POST_LAUNCH_HARDENING | Architecture-doc anchor packages (8); thin context signals; runtime-loaded but low risk. | KB-UTIL-2 |
| CF-MRIMPROVE-004 | Open | No | POST_LAUNCH_HARDENING | pkg_lipid_transport provenance gap; package active but provenance gap classified. | KB hygiene / provenance recovery |
| CF-MEDTREE-001 | Open | No | POST_LAUNCH_HARDENING | Generator exists; manual regen works; CI auto-refresh not urgent for Wave 1. | MED-FRAME-TREE-2 or CI-DOCS-1 |
| CF-BATCH2-010 | Open | No | CONDITIONAL_BLOCKER | No androgen clinical sign-off artefact in repo. Not a Wave 1 launch blocker (androgenic packages inactive). Blocks all androgen activation. | Androgen clinical sign-off sprint (pre-activation only) |
| CF-CONTEXT-MOD-3 | Resolved | — | RESOLVED | Runtime context evaluation implemented (CONTEXT-RUNTIME-1, CONTEXT-THREADING-1). CF resolved. | — |
| ARCH-ORCH-RESTRUCTURE-1 | Open | No | CONDITIONAL_BLOCKER | Orchestrator still uses raw questionnaire_data bridge at Step 1.6; create_analysis_context runs at Step 2. Not unsafe for Wave 1 (context-dependent packages all inactive). Must be completed before any context-dependent activation. | Day-one architecture sprint (before any activation) |
| CF-CONTEXT-SEMANTICS-1 | Resolved | — | RESOLVED | Taxonomy resolved by CONTEXT-CLEARANCE-1; runtime implementation by BATCH2-CONTEXT-COMPLETION-1. | — |

---

## ARCH-ORCH-RESTRUCTURE-1 decision

### Current state

At orchestrator Step 1.6, `build_runtime_context_snapshot(questionnaire_responses=questionnaire_data)` is called and the resulting snapshot is passed to `evaluate_all(runtime_context=runtime_ctx)` before `create_analysis_context()` runs at Step 2. This means signal evaluation accesses questionnaire data via the snapshot builder rather than receiving a fully assembled `AnalysisContext`.

### Does the current bridge create unsafe runtime behaviour today?

**No.** The `build_runtime_context_snapshot()` function reads from `questionnaire_data` (the same raw dict that `create_analysis_context` would process). It correctly extracts:
- `biological_sex`, `date_of_birth`, `long_term_medications`, `supplements`, `symptoms`, `chronic_conditions`

All 9 context-dependent packages (androgen + FT3 low) are currently **inactive** — their context gates never fire in production. No active signal currently declares `runtime_context_requirements`. The bridge is functionally correct for the current active signal estate.

### Does it violate the target architecture in principle but remain safe for Wave 1?

**Yes** — in principle. The target architecture requires thin runtime loaders to receive governed, assembled inputs. The bridge reads raw questionnaire payloads directly rather than a governed assembled context. This is an architectural debt item, not a runtime correctness problem under the Wave 1 scope.

### Does it need to be completed before launch, or can it remain a classified architectural residual?

**It can remain a classified architectural residual for Wave 1**, provided no context-dependent package is activated before the restructuring is complete.

### Recommendation

**POST_LAUNCH_HARDENING** for Wave 1 as currently scoped.

**CONDITIONAL_BLOCKER** for any future context-dependent package activation sprint. ARCH-ORCH-RESTRUCTURE-1 must be on the critical path for any androgen, FT3 low, or future context-dependent activation sprint.

---

## Card / hypothesis / PSI / provenance residual assessment

### Card evidence estate

| Component | Current state | Classification |
|-----------|---------------|----------------|
| Glycaemic subsystem (ARCH-RT-3 pilot) | Compiled, governed, manifest-emitting | ACCEPTABLE_WAVE1_RESIDUAL — pilot proves architecture |
| 6 hard-coded Wave 1 subsystems (`wave1_subsystem_evidence.py`) | Classified `legacy_active`; guarded by sentinel | ACCEPTABLE_WAVE1_RESIDUAL — validator prevents reintroduction of total_bilirubin defect |
| Estate-wide compiled card evidence | Not yet generated | POST_LAUNCH_HARDENING — ARCH-RT-5 split; planned but deferred |
| IDL / retail explainer | Runtime-consumed on narrative path | ACCEPTABLE_WAVE1_RESIDUAL — gates presentation safety |

Sentinel guard `day_one_wave1_compiled_card_authority` — GUARDED (PASS).

### Hypothesis / root-cause estate

| Component | Current state | Classification |
|-----------|---------------|----------------|
| Vitamin D compiled hypothesis (ARCH-RT-4 pilot) | Compiled, shadow mode; `summary_template` runtime-promoted | ACCEPTABLE_WAVE1_RESIDUAL — pilot proves architecture |
| 40 root-cause YAML | `legacy_active`; classified; runtime-consumed by `root_cause_compiler_v1.py` | ACCEPTABLE_WAVE1_RESIDUAL — functional WHY layer; guarded by validator |
| Estate-wide compiled hypothesis | Not yet generated | POST_LAUNCH_HARDENING |
| Multi-frame root-cause promotion | Blocked pending frame-selection policy | POST_LAUNCH_HARDENING |

Sentinel guard `day_one_compiled_hypothesis_promotion` — GUARDED (PASS).

### PSI runtime wiring

| Item | State | Classification |
|------|-------|----------------|
| PSI artefacts on disk | 20 × `pkg_kb47_*` | Present |
| PSI runtime consumed | No — loader not imported by pipeline | POST_LAUNCH_HARDENING |
| PSI required for Wave 1 launch-critical claims | No — per ARCH-RT-5E decision | ACCEPTABLE_WAVE1_RESIDUAL |

ADR-RT-001: PSI gap closure is post–ARCH-RT-1. No launch-critical claims depend on PSI runtime wiring.  
Sentinel guard `day_one_psi_runtime_isolation` — GUARDED (PASS).

### Package provenance / compile manifests

| Item | State | Classification |
|------|-------|----------------|
| All 186 packages classified | Yes — no `unknown_requires_review` | ACCEPTABLE_WAVE1_RESIDUAL |
| Inferred provenance not written as explicit `source_spec_id` | Yes — guarded | ACCEPTABLE_WAVE1_RESIDUAL |
| kb52c batch JSON source extraction | Blocked pending spec extraction; packages classified | ACCEPTABLE_WAVE1_RESIDUAL |
| Estate-wide explicit `source_spec_id` on manifests | Deferred | POST_LAUNCH_HARDENING |
| Pilot compile manifests (ARCH-RT-3/4) | Present and valid | ACCEPTABLE_WAVE1_RESIDUAL |

Sentinel guard `day_one_package_provenance_classification` — GUARDED (PASS).  
Sentinel guard `day_one_compile_manifest_integrity` — GUARDED (PASS).

---

## Launch-governance verdict

```
ACCEPTED_WITH_CONDITIONS
```

### Assessment against ADR-RT-001 launch standard

The sprint plan's stated standard for day-one is:

> Day-one does not mean perfect final architecture; it means governed enough for Wave 1 with residuals classified and guarded.

Assessed against that standard:

| Criterion | Status |
|-----------|--------|
| No raw research reads at runtime | **PASS** |
| No frontend medical inference (live path) | **PASS** |
| No fallback or dummy parsers | **PASS** |
| No ungoverned clinical reasoning | **PASS** |
| Context-dependent packages fail-closed pending STOP-gated approval | **PASS** |
| Lab-derived reference ranges used where available | **PASS** (SSOT authority) |
| Packages as compile targets, not parallel research authorities | **PASS** |
| All validators pass | **PASS** |
| Residuals classified and guarded | **PASS** |

---

## Remaining conditions

```
C-1: CF-BATCH2-010 — androgen clinical sign-off artefact must exist in repo before any
     androgen activation sprint is authorised. This is not a Wave 1 launch blocker but
     is a hard prerequisite for any androgen clinical activation.

C-2: ARCH-ORCH-RESTRUCTURE-1 — orchestrator phase restructuring must be completed before
     any context-dependent package (androgen, FT3 low, or future cohort) is activated.
     The current questionnaire_data bridge is safe for Wave 1 but is not the target architecture.

C-3: FT3 low has two separate activation-layer blockers:
     (a) enable_lower_bound: false — must be explicitly reviewed and changed with approval
     (b) thyroid_medication_disclosed key missing from package metadata — must be added
     Neither condition may be resolved implicitly; both require explicit sprint authorisation.

C-4: ClusterInsightPanel frontend clinical inference logic (getClinicalRecommendations,
     lines 88–121) must be removed or refactored before ClusterInsightPanel is imported
     by any live page. The ARCH-RT-6 sentinel perimeter does not currently cover this
     component.
```

None of C-1 through C-4 are Wave 1 launch blockers under the current scope (no context-dependent packages active; ClusterInsightPanel not in live flow).

---

## Recommended next action

**Proceed to product launch-readiness work.**

The architecture is sufficiently governed for Wave 1. The programmatic guardrails are in place and passing. The conditions above are pre-activation prerequisites and post-launch hardening items, not launch blockers.

No targeted architecture hardening sprint is needed before Wave 1 launch.

If androgen or FT3 low activation is a Wave 1 launch goal (which the current scope does not indicate), then the prerequisite order is:

```
1. ARCH-ORCH-RESTRUCTURE-1 (orchestrator phase restructuring)
2. CONTEXT-MOD-2 (Layer B context modifier evaluation binder)
3. CF-BATCH2-010 (androgen clinical sign-off artefact)
4. Androgen activation sprint with STOP gate
```

That sequence remains deferred until clinical sign-off is obtained and is not recommended as a Wave 1 pre-launch requirement.

---

## Evidence gaps

| Gap | Impact on review | Classification |
|-----|-----------------|----------------|
| `docs/architecture/research_to_runtime_traceability_matrix.md` present but not re-read (superseded by ARCH-RT-5 audit) | Limits traceability matrix freshness check | Low — ARCH-RT-5 traceability audit is more authoritative |
| `ClusterInsightPanel` not covered by ARCH-RT-6 sentinel perimeter | Sentinel does not guard against future import of inference-generating component | Recommendation: extend sentinel perimeter if cluster path is promoted |
| `context_runtime_execution_register_v1.yaml` contains stale note: `orchestrator_threading: not_yet_wired_signal_evaluation_precedes_questionnaire_merge` | This note predates CONTEXT-THREADING-1; threading is now done | Cosmetic stale note in governance register; not a runtime issue |
| FT3 low `thyroid_medication_disclosed` gap acknowledged in BATCH2-CONTEXT-COMPLETION-1 residual observations but not reflected in package metadata | Package metadata does not yet list `thyroid_medication_disclosed` as a required_disclosed_context field | Noted; part of Condition C-3 |

---

## Appendix B — Files inspected

**Architecture documents:**
- `docs/architecture/ADR-RT-001_research_to_runtime_day_one_architecture.md`
- `docs/architecture/activation_compile_gap_report.md`
- `docs/architecture/intelligence_authority_inventory.md`
- `docs/architecture/psi_coverage_and_manifest_opt_in_report.md`
- `docs/architecture/ARCH-RT-5_full_regeneration_and_launch_gate_report.md`

**Sprint plans:**
- `docs/sprints/healthiq_day_one_architecture_rework_sprint_plan_FINAL.md`
- `docs/sprints/launch_core_carry_forward_register.md`

**Audit papers:**
- `docs/audit-papers/CONTEXT-RUNTIME-1_reusable_runtime_context_evaluation_layer.md`
- `docs/audit-papers/CONTEXT-THREADING-1_runtime_context_orchestrator_threading.md`
- `docs/audit-papers/CONTEXT-CLEARANCE-1_context_semantics_and_batch2_clearance.md`
- `docs/audit-papers/BATCH2-CONTEXT-COMPLETION-1_runtime_semantics_and_stop_gated_activation.md`
- `docs/audit-papers/BATCH2-CONTEXT-COMPLETION-1_architecture_delta_report.md`
- `docs/audit-papers/ARCH-RT-6_day_one_architecture_acceptance_audit.md`

**Governance:**
- `knowledge_bus/governance/runtime_context_requirements_model_v1.yaml`
- `knowledge_bus/governance/runtime_context_semantics_model_v1.yaml`
- `knowledge_bus/governance/context_runtime_execution_register_v1.yaml`
- `knowledge_bus/governance/batch2_context_clearance_register_v1.yaml`
- `knowledge_bus/governance/batch2_remaining_blockers_execution_register_v1.yaml`
- `knowledge_bus/governance/batch2_remainder_resolution_register_v1.yaml`
- `knowledge_bus/governance/batch2_androgen_panel_medical_review_v1.yaml`
- `knowledge_bus/governance/batch2_androgen_context_modifier_binding_v1.yaml`
- `knowledge_bus/governance/medical_frame_identity_index_v1.yaml` (header)

**Runtime code (read-only):**
- `backend/core/pipeline/orchestrator.py` (Step 1.6 threading section)
- `backend/core/pipeline/orchestrator_phases_v1.py`
- `backend/core/knowledge/investigation_spec_to_promoted_signal.py` (grep only)
- `backend/core/knowledge/package_provenance_scan_v1.py` (grep only)
- `backend/core/analytics/runtime_context_evaluator.py` (referenced via audit papers)

**Frontend (read-only):**
- `frontend/app/components/clusters/ClusterSummary.tsx`
- `frontend/app/components/clusters/ClusterInsightPanel.tsx`
- `frontend/app/(app)/results/page.tsx` (import scan)
- `frontend/app/components/biomarkers/BiomarkerDials.tsx` (grep)

**Sentinel / validators:**
- `sentinel/packs/day_one_architecture_guardrails_v1.json`
- `backend/scripts/validate_day_one_architecture.py`
- `backend/scripts/run_architecture_validation_gate.py`
- `backend/tests/architecture/test_day_one_architecture_guardrails.py`
