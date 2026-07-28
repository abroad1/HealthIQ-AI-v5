# ARCH-CONV-A — Phase 0 Estate Reconciliation

**Work ID:** `ARCH-CONV-A`  
**Date (UTC):** 2026-07-27  
**Branch:** `feature/arch-conv-a-estate-why-authority-migration`  
**Baseline main:** `942de1ffda260bdcab8ab00ded17f4602dba478a`  
**Runtime change:** NONE for WHY emit path. Governance inventory refresh only (`estate_index_v1.yaml`, D-9 provenance register corrections).

---

## 1. Verified counts (re-derived 2026-07-27)

| Metric | Stage 0 | Phase 0 live | Match |
|---|---:|---:|---|
| `ROOT_CAUSE_TARGET_SPECS` | 41 | 41 | YES |
| Legacy `*_hypotheses_v1.yaml` | 40 | 40 | YES |
| Compiled hypothesis YAML on disk | 9 | 9 | YES |
| Authority register frames | 10 (9 ACTIVE + 1 REJECTED) | 10 | YES |
| Investigation specs `inv_*.yaml` | 43 | 43 | YES |
| Pilot signal families (`_PILOT_SIGNAL_IDS`) | 5 | 5 | YES |
| Package A remaining targets | 36 | 36 | YES |

**Migrated cohort (5 targets / 10 frames):**  
`signal_vitamin_d_low`, `signal_homocysteine_high`, `signal_mcv_high`, `signal_free_t3_low`, `signal_tpo_ab_high`.

---

## 2. Runtime caller map

| Role | Path | Emit? |
|---|---|---|
| Sole WHY emitter | `backend/core/analytics/root_cause_compiler_v1.py` `compile_root_cause_v1` | YES |
| Direct caller | `backend/core/analytics/report_compiler_v1.py` | calls emitter |
| InsightGraph | `backend/core/analytics/insight_graph_builder.py` | calls report compiler |
| Orchestrator | `backend/core/pipeline/orchestrator.py` | HTTP analysis path |
| HTTP | `backend/app/routes/analysis.py` start + regenerate | production entry |
| Scheduled/background WHY workers | none found | NO |

**Unmapped production WHY emitters:** NO.

---

## 3. Current WHY authorities

| Authority | Role | Emit gating? |
|---|---|---|
| `compiled_why_authority_register_v1.yaml` via `why_authority_v1` | Per-activation_key compiled/rejected selection | YES |
| `ROOT_CAUSE_TARGET_SPECS` + legacy loaders | Legacy family-level WHY for non-compiled targets | YES (legacy mode) |
| `root_cause_authority_register_v1.yaml` | Provenance classification stamp only | NO (not emit) |
| `estate_index_v1.yaml` | Launch/inventory index | NO (no emit callers) |

---

## 4. Estate-index correction

Refreshed `knowledge_bus/compiled/estate_index_v1.yaml`:

- `compiled_hypothesis_artefacts`: **1 → 9** (all `COMPILED_ACTIVE` frames from authority register)
- REJECTED hcy-metabolic frame intentionally omitted
- Card artefacts unchanged (**10**)
- Declared `why_authority_source_of_truth: compiled_why_authority_register_v1.yaml`

Updated stale ARCH-RT-5 launch-gate assertion (previously expected 7 cards / 1 hypothesis against a file that already had 10 cards).

---

## 5. LLM allow-flag finding

`HEALTHIQ_NARRATIVE_LLM` / `HEALTHIQ_ENABLE_LLM` / orchestrator `allow_llm` affect Layer C narrative synthesizer only.  
**They do not gate `compile_root_cause_v1` or WHY hypothesis selection.**

---

## 6. D-9 disposition (Phase 0)

`root_cause_authority_register_v1.yaml` refreshed:

- `package_a_scoping_authority: false`
- `why_emit_authority_source_of_truth` points at compiled WHY register
- Vitamin D artefact path corrected to live `signal_vitamin_d_low.yaml`
- `signal_free_t3_low` moved from `ROOT_CAUSE_REQUIRES_FUTURE_MAPPING` to explicit `ROOT_CAUSE_GOVERNED_ACTIVE` compiled entry
- Pilot multi-frame families recorded as family-level provenance pointers to the activation-key register
- Fallback quarantine entry preserved

---

## 7. Wave allocation confirmation

Stage 0 Wave 0–6 allocation confirmed against live registry (36 Package A targets). No reassignment required by Phase 0 evidence. Phase 1 may adjust only where identity plurality / D-3 merge requires it (see Phase 1 map).

---

## 8. Baseline discrepancies logged

| ID | Finding | Disposition |
|---|---|---|
| P0-D1 | ARCH-RT-5 launch-gate test expected 7 cards vs live 10 | Fixed with estate refresh |
| P0-D2 | Estate index listed 1 compiled WHY vs 9 on disk | Refreshed |
| P0-D3 | Stale provenance register contradicted pilot | D-9 refresh |
| P0-D4 | Stage 0 classified `signal_ferritin_low` as A4; live `inv_ferritin_spec_v1.yaml` has `signal_id: signal_ferritin_low`, direction `low` | Reclassified A3 in Phase 1 |
| P0-D5 | No scheduled WHY workers | Confirmed absent |
