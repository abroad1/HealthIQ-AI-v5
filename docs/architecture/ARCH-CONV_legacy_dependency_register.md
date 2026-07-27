# ARCH-CONV — Legacy Dependency Register

**Work ID:** `ARCH-CONV-RESIDUAL-AUDIT-1`  
**Date (UTC):** 2026-07-27  
**Scope:** Every `ACTIVE AUTHORITATIVE`, `ACTIVE SUPPORTING`, `COMPATIBILITY-ONLY`, or `SHADOW / DUAL-SERVICE` legacy dependency with removal preconditions.  
**Runtime change:** NONE  

Difficulty scale: `SMALL` · `MEDIUM` · `LARGE` · `VERY LARGE` · `UNBOUNDED`

---

## 1. How to read this register

For each dependency:

```text
legacy component
runtime caller
signals / frames affected
output surfaces affected
medical authority held
replacement under Day-One architecture
replacement already available: YES / NO
dependency removal difficulty
medical-review requirement
data-migration requirement
test-estate requirement
deletion preconditions
risk if removed immediately
risk if retained
```

---

## 2. Priority dependencies

### L-01 — Legacy root-cause YAML estate (non-pilot)

| Field | Value |
|---|---|
| legacy component | `knowledge_bus/root_cause/hypotheses/*_hypotheses_v1.yaml` + `ROOT_CAUSE_TARGET_SPECS` loaders |
| runtime caller | `compile_root_cause_v1` via `resolve_frame_why_authority` → mode `"legacy"` |
| signals / frames affected | 36 of 41 registry targets (verified exact count, all non–WHY-pilot signal_ids; frame count per target unresolved until Phase 1 identity closure — do not assume one target equals one frame, see `ARCH-CONV-A_active_why_target_inventory.md` and `ARCH-CONV-A_medical_review_wave_plan.md` §1.1) |
| output surfaces affected | `root_cause_v1`, clinician WHY, ranked findings explanations, confirmatory-test attachment |
| medical authority held | **ACTIVE AUTHORITATIVE** causal/hypothesis content |
| replacement under Day-One | Per-`activation_key` compiled hypothesis artefacts + authority register rows |
| replacement already available | **NO** (only 9 compiled artefacts exist) |
| dependency removal difficulty | **VERY LARGE** (content + review + compile + parity) |
| medical-review requirement | **Yes** — per wave / per frame |
| data-migration requirement | Soft — historic analyses may need regenerate/stale policy after authority change |
| test-estate requirement | High — per-signal parity + authority gates |
| deletion preconditions | Compiled artefact + register `COMPILED_ACTIVE` + dual-emit proof absent + gate green |
| risk if removed immediately | Mass silence / incorrect fallback WHY across non-pilot estate |
| risk if retained | Continues Day-One incompleteness; dual-path architecture persists |

### L-02 — Homocysteine elevation-context legacy WHY (shadow dual)

| Field | Value |
|---|---|
| legacy component | `signal_homocysteine_elevation_context` → `load_hcy_hypotheses_v1` / `hcy_hypotheses_v1.yaml` |
| runtime caller | `compile_root_cause_v1` (legacy mode; not in pilot frozenset) |
| signals / frames affected | Elevation-context family; narrative adjacency to compiled `signal_homocysteine_high::*` |
| output surfaces affected | Clinician summaries, interventions refs, consumer adjacency |
| medical authority held | **SHADOW / DUAL-SERVICE** (overlapping medical question space) |
| replacement under Day-One | Compiled frame(s) under authority register **or** explicit governed elevation-context artefact with non-overlap rules |
| replacement already available | **NO** (wording corrected; authority not migrated) |
| dependency removal difficulty | **MEDIUM**–**LARGE** |
| medical-review requirement | **Yes** |
| data-migration requirement | Possibly regenerate affected analyses |
| test-estate requirement | Dual-authority exclusivity tests |
| deletion preconditions | Medical disposition of elevation-context vs frame-specific WHY; compiled path live; dual-emit tests |
| risk if removed immediately | Loss of elevation-context explanation on panels that rely on it |
| risk if retained | Persistent dual narrative authority beside compiled hcy frames |

### L-03 — Pilot legacy YAML dual registration (compatibility)

| Field | Value |
|---|---|
| legacy component | Pilot signal rows still listed in `ROOT_CAUSE_TARGET_SPECS` with legacy loaders |
| runtime caller | Import-time validation loads assets; emit path skips when mode=`compiled` |
| signals / frames affected | vitamin_d, hcy high frames, mcv, free_t3_low, tpo frames |
| output surfaces affected | None for COMPILED_ACTIVE emit (intended) |
| medical authority held | **COMPATIBILITY-ONLY** at emit; **ACTIVE** if mode flipped/misconfigured |
| replacement under Day-One | Register-only selection; eventual loader deregistration |
| replacement already available | **YES** for emit (compiled) |
| dependency removal difficulty | **MEDIUM** |
| medical-review requirement | No for deregistration after exclusivity proven |
| data-migration requirement | No |
| test-estate requirement | Keep exclusivity gates; update registry validation |
| deletion preconditions | Long-window exclusivity proof; no test harness depends on legacy emit for those keys |
| risk if removed immediately | Breaks import validation / historical tests if done carelessly |
| risk if retained | Low emit risk; residual confusion / accidental reactivation surface |

### L-04 — `why_engine_fallback_v1` placeholder authority

| Field | Value |
|---|---|
| legacy component | `_compile_why_engine_fallback_finding` in `root_cause_compiler_v1.py` |
| runtime caller | Root-cause compiler when ranked lead lacks governed finding |
| signals / frames affected | Any lead without mapped WHY |
| output surfaces affected | Clinician/consumer WHY surfaces |
| medical authority held | **ACTIVE AUTHORITATIVE fallback** |
| replacement under Day-One | Fail-closed honest omission **or** compiled “insufficient evidence” artefact |
| replacement already available | **PARTIAL** (skip exists for REJECTED; not generalised) |
| dependency removal difficulty | **MEDIUM** |
| medical-review requirement | Yes for user-facing replacement wording |
| data-migration requirement | No |
| test-estate requirement | Silence vs fallback policy tests |
| deletion preconditions | Product policy on missing-WHY behaviour ratified |
| risk if removed immediately | Empty WHY on many leads |
| risk if retained | Soft fail-open medical wording outside compiled estate |

### L-05 — Generic `_why_template` / layered why-it-matters

| Field | Value |
|---|---|
| legacy component | `report_compiler_v1._why_template` (+ IDL why fields) |
| runtime caller | Clinician report assembly |
| signals / frames affected | Broad |
| output surfaces affected | Clinician “why it matters” |
| medical authority held | **ACTIVE SUPPORTING** / weak fallback authority |
| replacement under Day-One | Compiled/governed per-frame why-it-matters only |
| replacement already available | **PARTIAL** (IDL + compiled summaries cover some) |
| dependency removal difficulty | **MEDIUM** |
| medical-review requirement | Conditional |
| data-migration requirement | No |
| test-estate requirement | Template absence regressions |
| deletion preconditions | Coverage proof for ranked signals |
| risk if removed immediately | Blank clinician fields |
| risk if retained | Parallel wording authority |

### L-06 — Family-level phenotype / interaction maps (`signal_id`)

| Field | Value |
|---|---|
| legacy component | `phenotype_map_v1.yaml`, `interaction_map_v1.yaml`, family index helpers |
| runtime caller | IDL publish, interaction builder, narrative joins |
| signals / frames affected | All multi-frame families entering those surfaces |
| output surfaces affected | Patterns, chains, phenotype membership |
| medical authority held | **ACTIVE AUTHORITATIVE** at family grain |
| replacement under Day-One | Explicit family aggregation policy **or** activation_key-native maps |
| replacement already available | **PARTIAL** (PKG1 added participating_activation_keys auditability; core joins still family-keyed by design in places) |
| dependency removal difficulty | **LARGE** |
| medical-review requirement | Yes if aggregation semantics change clinical meaning |
| data-migration requirement | No |
| test-estate requirement | Multi-frame pressure sets |
| deletion preconditions | Product decision: family aggregation is intentional vs defect |
| risk if removed immediately | Break phenotype/IDL/chains |
| risk if retained | Frame collapse at family surfaces (may be acceptable if explicit) |

### L-07 — Hard-coded Layer B thresholds in InsightGraph Layer C features

| Field | Value |
|---|---|
| legacy component | Threshold constants in `insight_graph_builder._build_layer_c_features` |
| runtime caller | InsightGraph assembly |
| signals / frames affected | Metabolic/ratio feature flags |
| output surfaces affected | Layer C insight tokens |
| medical authority held | **ACTIVE AUTHORITATIVE** feature gating |
| replacement under Day-One | Compiled/governed feature policy artefacts |
| replacement already available | **NO** |
| dependency removal difficulty | **MEDIUM** |
| medical-review requirement | Yes |
| data-migration requirement | Possible regenerate |
| test-estate requirement | Feature parity tests |
| deletion preconditions | Artefact + loader + FE contract |
| risk if removed immediately | Layer C sections empty/wrong |
| risk if retained | Hidden Python medical policy |

### L-08 — Domain assembler presentation/policy constants

| Field | Value |
|---|---|
| legacy component | Domain labels, IDL preference order, allowlists in `domain_score_assembler.py` |
| runtime caller | Health Systems Card assembly |
| signals / frames affected | Wave 1 domains |
| output surfaces affected | Cards / subsystem presentation |
| medical authority held | **ACTIVE SUPPORTING** (not marker evidence) |
| replacement under Day-One | Compiled presentation manifests |
| replacement already available | **PARTIAL** |
| dependency removal difficulty | **MEDIUM** |
| medical-review requirement | Low–medium |
| data-migration requirement | No |
| test-estate requirement | Card render parity |
| deletion preconditions | Manifest coverage |
| risk if removed immediately | Card labelling regressions |
| risk if retained | Acceptable short-term if evidence remains compiled |

### L-09 — LLM / MockLLM insight synthesis path

| Field | Value |
|---|---|
| legacy component | `InsightSynthesizer`, prompts, MockLLM blobs |
| runtime caller | Orchestrator (policy-gated) |
| signals / frames affected | Insight narrative categories |
| output surfaces affected | Insights panel |
| medical authority held | **ACTIVE SUPPORTING** / potential fallback |
| replacement under Day-One | Deny-default translation-only over Layer B JSON |
| replacement already available | **YES** as policy posture; MockLLM still present |
| dependency removal difficulty | **SMALL**–**MEDIUM** |
| medical-review requirement | If enabling LLM in prod |
| data-migration requirement | No |
| test-estate requirement | Deny-default gates |
| deletion preconditions | Confirm prod flags; retire mock medical blobs from any reachable path |
| risk if removed immediately | Low if already unused |
| risk if retained | Config-flip reactivation risk |

### L-10 — Frontend governed static copy modules

| Field | Value |
|---|---|
| legacy component | `layerCInsightCopy.ts`, `systemUnderstandingCopy.ts` |
| runtime caller | Results Layer C sections |
| signals / frames affected | Presentation around backend tokens |
| output surfaces affected | Consumer educational copy |
| medical authority held | **ACTIVE SUPPORTING** presentation |
| replacement under Day-One | Continue as presentation-only **or** move copy to governed backend DTOs |
| replacement already available | **YES** as presentation strategy |
| dependency removal difficulty | **SMALL** |
| medical-review requirement | If medical claims creep in |
| data-migration requirement | No |
| test-estate requirement | Layer C boundary tests |
| deletion preconditions | Replacement DTO fields |
| risk if removed immediately | Empty section chrome |
| risk if retained | Acceptable if boundary tests hold |

### L-11 — Historic waist-unit persisted analyses

| Field | Value |
|---|---|
| legacy component | Bare `waist_circumference` historic rows |
| runtime caller | Replay/regenerate/read of old analyses |
| signals / frames affected | Analyses with waist-dependent logic |
| output surfaces affected | Historic results fidelity |
| medical authority held | **COMPATIBILITY-ONLY** data debt |
| replacement under Day-One | Explicit unit contract (already live for new input) + stale/regenerate policy |
| replacement already available | **PARTIAL** (forward-fix live; historic remediation not done) |
| dependency removal difficulty | **MEDIUM** |
| medical-review requirement | No (data integrity) |
| data-migration requirement | **Yes** |
| test-estate requirement | Versioning/stale markers |
| deletion preconditions | Ratified remap or force-regenerate policy |
| risk if removed immediately | N/A (data, not code) |
| risk if retained | 12 known incorrectly-used historic rows (audited) |

### L-12 — Output-authority provenance fixture key debt

| Field | Value |
|---|---|
| legacy component | Provenance paths / tests using `signal_homocysteine_high::inv_homocysteine_high` |
| runtime caller | Provenance builder / regression tests |
| signals / frames affected | Homocysteine provenance identity |
| output surfaces affected | Provenance manifests / auditability |
| medical authority held | **ACTIVE SUPPORTING** (identity correctness) |
| replacement under Day-One | Real activation_key identity only |
| replacement already available | **PARTIAL** |
| dependency removal difficulty | **SMALL**–**MEDIUM** |
| medical-review requirement | No |
| data-migration requirement | Possibly historic provenance rows |
| test-estate requirement | Update provenance regressions |
| deletion preconditions | Confirm no live emitter still invents bare key |
| risk if removed immediately | Test gaps |
| risk if retained | Misleading provenance identity |

### L-13 — Non-reachable kb47 packages retained on disk

| Field | Value |
|---|---|
| legacy component | 14 PKG2 `non_reachable` packages |
| runtime caller | Excluded by eligibility (unless env opt-in) |
| signals / frames affected | Androgen/CK/eos cohort |
| output surfaces affected | None in production when excluded |
| medical authority held | **COMPATIBILITY-ONLY** / test opt-in |
| replacement under Day-One | Extract+attach later or permanent exclude |
| replacement already available | N/A |
| dependency removal difficulty | **MEDIUM** |
| medical-review requirement | Before re-inclusion |
| data-migration requirement | No |
| test-estate requirement | Opt-in harnesses |
| deletion preconditions | Disposition decision + no test-only need |
| risk if removed immediately | Lose recoverable lineage assets |
| risk if retained | Low if eligibility gate holds; env opt-in is residual risk |

---

## 3. Estate-wide dependency summary

| Class | Count of material dependencies in this register | Bounded? |
|---|---:|---|
| ACTIVE AUTHORITATIVE legacy | Dominated by L-01 (+ L-04/L-07) | Yes — countable registry |
| SHADOW / DUAL | L-02 (+ layered why templates) | Yes — localised |
| COMPATIBILITY | L-03, L-11, L-13 | Yes |
| ACTIVE SUPPORTING | L-05, L-08, L-09, L-10, L-12 | Yes |

**Conclusion:** Remaining legacy dependencies are **numerous but enumerable**. The single dominating blocker to estate Day-One WHY convergence is **L-01**, which is large because of medical-review and compile volume, not because the architecture is unknown.
