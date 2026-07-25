# P3-LAYERB-INTEL-1 — Migration and Coverage Inventory

**Work ID:** P3-LAYERB-INTEL-1  
**Date:** 2026-07-25  
**Baseline SHA:** `0c90f9538850918bf07545e9be917b62d9083a63` (main after Package 2 merge)  
**Stage B Mode:** MODE_2 (architecture-extension)

---

## 1. Active Layer B content authorities

| Authority | Path | Entries | Selection key today | Runtime | Production vs other |
|---|---|---|---|---|---|
| Retail biomarker explainers | `backend/ssot/retail_explainer_v1/registry.yaml` | 40 / 104 canonical biomarkers | `biomarker_id` | Yes (`attach_retail_explainers_v1`) | Production; **no `review_status` field** |
| Retail system explainers | same registry | 10 | cluster system key | Yes | Production |
| Pathway explainers | `knowledge_bus/pathway_explainers_v1/pathway_explainers_v1.yaml` | 5 | via entity `pathway_explainer_id` | Yes (narrative compiler) | Production prose pack |
| Functional interpretation | `knowledge_bus/functional_interpretation_v1/functional_interpretation_v1.yaml` | 4 | via entity `functional_interpretation_domain_id` | Yes | Production prose pack |
| Interpretation entities | `knowledge_bus/interpretation_entities_v1/benchmark_interpretation_entities_v1.yaml` | 4 | `compiler_role` + optional `signal_ids` | Yes | Production benchmark |
| Legacy root-cause YAML | `backend/core/knowledge/root_cause_registry_v1.py` | 41 targets | `signal_id` family + live rules | Yes | Production; findings labelled `family_level` |
| Compiled hypothesis | `knowledge_bus/compiled/hypotheses/` + pilot registry | **1** (`signal_vitamin_d_low`) | `signal_id` + artefact `activation_key` | Yes (promoted) | Production pilot |
| Context modifier catalogue | `knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml` | 42 | n/a | **No** (`runtime_active: false` all) | Draft governance only |
| MR-BATCH-001B candidates | `docs/sprints/beta_readiness/MR-BATCH-001B_candidate_prose_assets.yaml` | (batch) | test harness only | **No** | **Test-only** — zero `backend/core`, `backend/app`, `frontend/app` imports |

---

## 2. Runtime selection paths (pre-change)

1. **Retail:** `biomarker_id` / system key — not frame-aware.
2. **Narrative lead prose:** `_resolve_lead_signal_id` + `_select_lead_entity_row` by bare `signal_id` / hint frozensets — **not** `activation_key`.
3. **Root-cause WHY:** Package 2 preserves multi-frame findings; compiled path still binds the same vitamin-D artefact per family row when promoted; legacy YAML always `authority_scope=family_level`.
4. **Modifiers:** no binder; catalogue non-runtime.
5. **Frontend:** render-only for Layer B DTOs; `activation_key`/`source_spec_id` typed but unused; no modifier types.

---

## 3. Bounded migration cohort

**In-scope for Layer B infrastructure + controlled-beta reassessment readiness (≤12 frames):**

| # | Frame / signal | Role | Current prose | Current WHY | Modifier need | Provenance | Medical review |
|---|---|---|---|---|---|---|---|
| 1 | `signal_vitamin_d_low::inv_vitamin_d_low_deficiency` | Reference compiled WHY | Retail vitamin_d + narrative packs | Compiled pilot (production) | None active | COMPILED_MANIFEST | Already production |
| 2–5 | free_t3_high/low, free_t4_high/low (kb47 frames) | Launch-critical multi-frame thyroid | Legacy family WHY + retail | Legacy YAML family_level | None active | BLOCKED package lineage | Required before frame-specific compiled WHY / Round 2 |
| 6–7 | `signal_tsh_high`, `signal_tsh_low` | Thyroid family completeness | Retail tsh | Legacy YAML | None active | Governed YAML | Required before Round 2 / compiled promotion |
| 8 | `signal_ldl_cholesterol_high` | Narrative routing exercise | Pathway/functional/entity | Legacy YAML | None active | Governed YAML | Required before Round 2 |
| 9 | `signal_homocysteine_high` (+ elevation_context sibling) | Multi-signal lead path | Richest pack coverage | Legacy YAML | None active | Governed YAML | Required before Round 2 |

**Explicitly deferred (not migrated this package):**

- Remaining kb47 BLOCKED packs (CK×2, eGFR×2, eosinophil×4, DHEA, FAI, free-testosterone×2) pending `inv_` extraction.
- Broad legacy WHY estate rewrite.
- Activating any of 42 draft modifiers without medical approval + `runtime_active`.

---

## 4. Asset class confirmation

| Class | Examples | May become production in this package? |
|---|---|---|
| Production | vitamin_d compiled WHY; existing retail/pathway/functional/entity packs; legacy YAML WHY | Retain; do not rewrite medical meaning |
| Legacy family-level | Most root-cause YAML findings | Retain with honest `LEGACY_FAMILY_LEVEL` fallback label |
| Candidate / test-only | MR-BATCH-001B | **Never** — isolation enforced by gate |
| Pending medical review | Round 2 prose; new compiled WHY beyond vitamin_d | **Not production** until explicit medical approval recorded |

---

## 5. MR-BATCH-001B isolation

Confirmed: zero production imports under `backend/core/`, `backend/app/`, `frontend/app/`. Only test support + docs. Gate must fail if any production import appears.

---

## 6. Design gaps addressed by this package

1. **Frame-aware prose routing** — greenfield contract + runtime stamp (activation_key preferred; family fallback labelled).
2. **Modifier binder** — greenfield; fail-safe empty while catalogue remains non-runtime.
3. **`review_status` / production authority** — new Layer B asset authority registry (governance) so Round 2 / compiled promotion cannot claim production without checkable approval.
4. **Layer B integrity gate** — CI-wired detection of wrong-frame, candidate imports, missing provenance, false production status, non-determinism probes.

---

## 7. STOP Gate 1 disposition (recorded)

| Question | Decision |
|---|---|
| Frame routing policy ambiguous? | **No** — policy accepted: prefer `activation_key` match → `source_spec_id` → labelled `LEGACY_FAMILY_LEVEL` by `signal_id`; never borrow another frame’s asset. |
| Modifier precedence needs product/medical decision? | **Yes for activation** — catalogue has zero `runtime_active` rows. Binder ships fail-safe (no clinical modifiers bound) until medical approval flips rows. |
| WHY mapping without defensible frame? | **Escalate promotion** — do not invent frame-specific compiled WHY for BLOCKED kb47 packs; keep vitamin_d as sole promoted compiled WHY until medical review approves expansion. |
| Provenance unresolved for proposed promoted asset? | **Block promotion** — BLOCKED lineage cannot become EXPLICIT/production Round 2. |
| Broad legacy rewrite required? | **No** — cohort bounded. |
| Frontend medical inference? | **Forbidden** — additive DTO provenance only; FE remains render-only. |

**STOP Gate 1: PASS for infrastructure wiring; medical-review gate remains REQUIRED before any new Round 2 prose or expanded compiled WHY production authority.**
