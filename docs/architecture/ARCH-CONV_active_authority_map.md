# ARCH-CONV — Active Authority Map

**Work ID:** `ARCH-CONV-RESIDUAL-AUDIT-1`  
**Date (UTC):** 2026-07-27  
**Purpose:** Map every active source capable of providing medical reasoning or output content to its authority role.  
**Runtime change:** NONE  

Authority role vocabulary:

```text
canonical authority
compiled derivative
duplicate authority
fallback authority
presentation-only asset
runtime-dead asset
uncertain
```

---

## 1. Target architecture lanes

| Lane | Intended owner | Current estate status |
|---|---|---|
| Canonical research | Investigation specs / Pass 3 JSON | Present; not runtime-executed |
| Deterministic compile | Knowledge Bus compile / promotion | Partial — pilot WHY + Wave 1 cards compiled |
| Governed runtime artefacts | Compiled hypotheses, cards, packages | Partial |
| Runtime loaders | SignalRegistry, hypothesis loaders, card loaders | Live |
| Layer B DTOs | InsightGraph, report_v1, IDL, narrative, clinician report | Live |
| Layer C | Frontend render/translation | Corrected for audited BOUNDARY_LEAKs |

---

## 2. Authority map by source family

### 2.1 Investigation specs

| Source | Runtime? | Authority role | Notes |
|---|---|---|---|
| `knowledge_bus/research/investigation_specs/inv_*.yaml` | No evaluator reads | **canonical authority** | Upstream of packages / compiled artefacts |
| Pass 3 batch JSON | Compile/promotion only | **canonical authority** | Lineage source for kb47 / kb52c etc. |

### 2.2 Compiled frame / WHY artefacts

| Source | Runtime? | Authority role | Cohort |
|---|---|---|---|
| `knowledge_bus/compiled/hypotheses/*.yaml` (9) | Yes — selected keys | **compiled derivative** | WHY pilot |
| `get_compiled_hypothesis_artefact_for_activation_key` | Yes | loader of compiled derivative | activation_key path |
| `get_compiled_hypothesis_artefact(signal_id)` | Compatibility risk | **duplicate / uncertain** if misused | signal_id collapse risk |
| `compiled_hypothesis_registry_v1` vitamin-D shadow set | Shadow compare | **runtime-dead** for emit merge | Must not merge into ROOT_CAUSE targets |

### 2.3 Signal libraries / packages

| Source | Runtime? | Authority role | Cohort |
|---|---|---|---|
| `packages/*/signal_library.yaml` | Yes | **compiled derivative** (or legacy-translated derivative) for fire/state/interpretation | Estate-wide |
| Package manifests + eligibility | Yes | supporting gate | kb47 honesty; others loadable |
| `generated_pilot/**` | No | **runtime-dead asset** | Staging only |

### 2.4 Legacy root-cause / hypothesis YAML

| Source | Runtime? | Authority role | Cohort |
|---|---|---|---|
| 40 `*_hypotheses_v1.yaml` via 41 registry targets | Yes for non-pilot | **canonical-of-legacy** (authoritative until migrated) | 36 non-pilot registry targets (verified exact count; frame count per target unresolved — see `ARCH-CONV-A_active_why_target_inventory.md` and `ARCH-CONV-A_medical_review_wave_plan.md` §1.1) |
| Same YAML for pilot COMPILED_ACTIVE frames | Loader skipped | **runtime-dead** for those keys | Compatibility registration remains |
| Shared `hcy_hypotheses_v1.yaml` for elevation_context | Yes | **duplicate authority** vs compiled hcy frames | Shadow dual |

### 2.5 Promoted Signal Intelligence (PSI)

| Source | Runtime? | Authority role |
|---|---|---|
| `promoted_signal_intelligence.yaml` | Not on Intelligence Core path | **runtime-dead asset** (compiled derivative on disk) |
| `load_promoted_signal_intelligence.py` | Exists; unwired | **runtime-dead** |

### 2.6 Hard-coded Python medical mappings

| Source | Runtime? | Authority role |
|---|---|---|
| `report_compiler_v1._why_template` | Yes | **fallback authority** (generic why-it-matters) |
| `why_engine_fallback_v1` | Yes when lead lacks WHY | **fallback authority** |
| Layer C feature thresholds in `insight_graph_builder` | Yes | **compiled-derivative-ish / hard-coded policy** — treat as **duplicate risk** vs research artefacts |
| Domain assembler labels / order | Yes | **presentation-only** (+ light policy) |
| Narrative lifestyle constants | Yes | **presentation-only** / governed constants |
| Scoring derived ranges | Yes | lab/scoring support, not narrative WHY |

### 2.7 IDL / retail explainers / narrative entities

| Source | Runtime? | Authority role |
|---|---|---|
| `idl_records_v1.yaml` | Yes | **presentation governed content** (Layer B publish) — acts as display authority |
| Retail explainer registry | Yes | **presentation-only** / SSOT |
| Narrative interpretation entities YAML | Yes | **compiled derivative / governed content** |
| MR-BATCH candidate prose YAML | No (authority blockers) | **runtime-dead** / candidate |

### 2.8 Health Systems Cards

| Source | Runtime? | Authority role |
|---|---|---|
| `knowledge_bus/compiled/health_system_cards/wave1_*.yaml` | Yes | **compiled derivative** |
| Flat liver card evidence | Yes | **compiled derivative** |
| Legacy hard-coded marker maps | No | **runtime-dead** |
| Visibility tier Python constants | Yes | **presentation-only** policy |

### 2.9 Phenotype / interaction / confirmatory / interventions

| Source | Runtime? | Authority role |
|---|---|---|
| Phenotype map | Yes | family-level **canonical-of-legacy** for phenotype membership |
| Interaction map | Yes | family-level chain authority |
| Confirmatory tests registry | Yes | **canonical** shared IDs |
| Intervention library | Yes | **canonical** intervention catalogue |

### 2.10 LLM prompts / frontend

| Source | Runtime? | Authority role |
|---|---|---|
| InsightSynthesizer + prompt templates | Policy-gated | **fallback / translation** — must not invent medical authority |
| MockLLM category blobs | Dev/test path | **fallback** / fixture-like |
| FE renderers consuming DTOs | Yes | **presentation-only** |
| FE governed copy modules | Yes | **presentation-only** product copy |

---

## 3. Who wins today (selection rules)

| Medical question class | Winning authority | Enforcement | Fail mode |
|---|---|---|---|
| Pilot frame WHY (`COMPILED_ACTIVE`) | Compiled artefact | `resolve_frame_why_authority` → mode `compiled` | Missing artefact fails closed on compile path |
| Pilot rejected frame | No WHY + no fire | Register `REJECTED` + `frame_runtime_authority_v1` | Fail-closed |
| Non-pilot WHY | Legacy YAML | Unconditional `"legacy"` return | Legacy emit |
| Card marker evidence (Wave 1) | Compiled card YAML | Assemblers refuse hard-coded fallback | Fail-closed on missing compiled |
| Signal fire | signal_library + eligibility + collision + reject filter | SignalRegistry/Evaluator | Blocked pkgs excluded; others fire |
| Consumer pattern labels | IDL publish | IDL registry + phenotype join | Missing → omitted / fallback paths |
| Clinician synthesis | `compile_clinician_report_v1` over `report_v1` | GET DTO builder | Derived at read |
| Layer C primary driver | `primary_driver_v1` | CORRECT-1 FE consumes backend | Missing → no FE invention |

---

## 4. Map of Day-One completeness by authority class

| Authority class | Estate coverage | Verdict |
|---|---|---|
| Signal activation (`signal_library`) | Near-estate | Active; not the same as compiled WHY Day-One |
| Compiled WHY | 9 compiled artefacts (10 ratified frames) across 5 of 41 verified WHY targets | **Pilot only** |
| Legacy WHY | Majority of WHY targets | **Still dominant** |
| Compiled cards | Wave 1 domains | Substantially complete for Wave 1 evidence |
| PSI | On disk, unwired | Intentionally non-authoritative |
| Layer C | Audited surfaces corrected | Substantially complete for BOUNDARY_LEAK inventory |

---

## 5. Implications for the decision gate

1. The accepted Day-One chain is **implemented and proven** for the migrated WHY cohort and Wave 1 card evidence.
2. The active estate still has a **second authoritative WHY lane** (legacy YAML) for the majority of `ROOT_CAUSE_TARGET_SPECS`.
3. Removing legacy immediately would silence or degrade medical explanation for most WHY-mapped signals — replacement artefacts are **not** already available estate-wide.
4. Therefore estate-wide Day-One convergence is a **completion programme**, not an already-finished state.
