# P3-LAYERB-INTEL-1 — Implementation and Verification Report

**Work ID:** P3-LAYERB-INTEL-1  
**Branch:** `feature/p3-layerb-intel-1-frame-routing-why-depth`  
**Date:** 2026-07-25

---

## 1. Executive outcome

Delivered Layer B **infrastructure** for frame-aware prose routing, governed modifier binding (fail-safe), production-authority registry, narrative selection provenance stamps, and a CI-wired Layer B integrity gate — without promoting unreviewed medical prose, without expanding compiled WHY beyond the vitamin_d pilot, and without activating PSI / MR-BATCH / Gemini.

**Medical review gate:** REQUIRED and **not obtained** for Round 2 prose or compiled-WHY expansion; those assets remain `pending_medical_review` / non-importable. Controlled beta is **not** declared.

---

## 2. Baseline SHA

`0c90f9538850918bf07545e9be917b62d9083a63` (main after ARCH-RT-IDENTITY-PROV-1 + C1 merge)

---

## 3. Migration cohort

Documented in `docs/architecture/P3-LAYERB-INTEL-1_migration_and_coverage_inventory.md`.

Bounded cohort (9 frames): vitamin_d compiled reference; free_t3/t4 kb47 thyroid frames; tsh high/low; ldl_cholesterol_high; homocysteine_high. Deferred: remaining BLOCKED kb47 packs pending inv_ extraction + medical review.

---

## 4. Medical-review evidence

| Asset class | Decision |
|---|---|
| Existing vitamin_d compiled WHY | Retain production (prior pilot approval) |
| Round 2 prose cohort | **Not authored** — `pending_medical_review` in authority registry |
| Compiled WHY expansion beyond vitamin_d | **Not promoted** — same |
| Draft modifier catalogue (42) | Remain `runtime_active: false`; binder returns empty fail-safe |
| MR-BATCH-001B | Remains `test_only`; production import scan PASS |

Schema validation is **not** treated as medical approval.

---

## 5. Files changed (implementation)

- `docs/architecture/P3-LAYERB-INTEL-1_migration_and_coverage_inventory.md`
- `docs/audit-papers/P3-LAYERB-INTEL-1_implementation_and_verification_report.md` (this file)
- `knowledge_bus/governance/layer_b_asset_authority_v1.yaml`
- `backend/core/knowledge/layer_b_frame_routing_v1.py`
- `backend/core/knowledge/layer_b_modifier_binder_v1.py`
- `backend/core/knowledge/layer_b_asset_authority_v1.py`
- `backend/core/analytics/narrative_report_compiler_v1.py` (frame routing + modifier provenance stamps)
- `backend/scripts/validate_layer_b_integrity_gate.py`
- `backend/scripts/run_architecture_validation_gate.py` (wire gate)
- `backend/tests/unit/test_p3_layerb_intel_1.py`
- `frontend/app/types/analysis.ts` (additive selection-provenance types)
- `docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md`
- Automation Bus artefacts for this work_id

**Package 2 identity/provenance contracts:** unchanged.

---

## 6. Routing and modifier decisions

**Frame routing policy v1.0.0:** activation_key match → source_spec_id match → labelled `LEGACY_FAMILY_LEVEL` by signal_id; never borrow another frame’s activation-key-specific asset; candidate/test_only/pending rejected in production.

**Modifier binder v1.0.0:** only `runtime_active` + `production_authority in {approved,production}`; exclusive_group contradictions omit both (fail-safe); deterministic ascending `modifier_id` precedence. Current catalogue yields empty selection.

---

## 7. Compiled WHY changes

None beyond retaining the existing vitamin_d pilot. Expansion cohort recorded as pending medical review.

---

## 8. STOP Gate 1

PASS for infrastructure; medical-review required before Round 2 / WHY expansion (recorded in inventory §7).

---

## 9. Commands and exit codes

*(Filled after verification suite.)*

| Command | Exit |
|---|---|
| `python -m pytest backend/tests/unit/test_p3_layerb_intel_1.py -q` | 0 |
| `python backend/scripts/validate_layer_b_integrity_gate.py` | 0 |
| `python backend/scripts/validate_day_one_architecture.py` | 0 |
| `python backend/scripts/validate_day_one_launch_estate_gate.py` | 0 |
| `python backend/scripts/run_architecture_validation_gate.py` | 0 |
| `python -m pytest backend/tests/unit/test_arch_rt_identity_prov_1.py -q` | 0 |
| `python -m pytest backend/tests/unit -k "root_cause_compiler or compile_root_cause" -q` | 0 |
| `python -m pytest backend/tests/unit/test_clinician_report_runtime_alignment.py -q` | 0 |
| `python -m pytest backend/tests -k "narrative_report or retail_explainer or no_llm or NO_LLM" -q` | 0 |
| `python -m pytest backend/tests/unit/test_replay_manifest.py -q` | 0 |
| `python -m pytest backend/tests/unit/test_golden_panel_runner.py -q` | 0 |
| `python -m pytest backend/tests -k "mr_batch" -q` | 0 |
| `npx tsc --noEmit` (frontend) | 0 |

---

## 10. Acceptance-criteria table

| Criterion | Disposition |
|---|---|
| Migration cohort bounded and documented | PASS |
| STOP Gate 1 passed or escalated | PASS (infra) + medical escalation recorded |
| Frame-aware prose routing production-wired | PASS (narrative compiler + routing module) |
| Modifier binding deterministic and governed | PASS (fail-safe empty until approval) |
| Approved compiled WHY cohort production-wired | PASS (vitamin_d only; expansion deferred) |
| Round 2 assets explicit medical approval | **DEFERRED** — none promoted; pending_medical_review |
| Candidate/test-only isolated | PASS |
| Provenance through DTO/replay | PASS (meta stamps + tests) |
| Layer B integrity gate CI-wired | PASS |
| Required tests pass | See §9 |
| No PSI/Gemini/MR-BATCH promotion | PASS |
| No controlled-beta claim | PASS |

---

## 11. STOP-condition assessment

| # | Disposition |
|---|---|
| 1 Medical review rejects asset | Not triggered (no new production assets submitted) |
| 2 Ambiguous source authority | Not triggered for infrastructure; BLOCKED packs deferred |
| 3 Unsupported frame inference | Not triggered — family fallback labelled |
| 4 Modifier clinical meaning change | Not triggered — no modifiers activated |
| 5 Package 2 redesign | Not triggered |
| 6 Candidate required for tests | Not triggered |
| 7 Expand beyond cohort | Not triggered |
| 8 Unexplained gate failure | See §9 |

---

## 12. Unresolved carry-forwards

1. Human medical review of Round 2 prose + compiled WHY expansion for thyroid/LDL/homocysteine cohort.
2. `inv_` extraction for BLOCKED kb47 packs before beta-eligible explicit lineage.
3. Activating any context-modifier catalogue rows (`runtime_active` + approved authority).
4. Optional FE render of `layer_b_frame_routing` / modifier stamps (types added; UI still unused).
5. Retail explainer per-entry `review_status` schema (gap documented; authority registry covers Layer B gate for now).
