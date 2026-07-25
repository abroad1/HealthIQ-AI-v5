# ARCH-CONV-PKG1 — Frame Identity Surface Design

**Work ID:** `ARCH-CONV-PKG1`  
**Branch:** `feature/arch-conv-pkg1-frame-identity-closure`  
**Baseline HEAD:** `aacd52b10ffdd8d355cf778fdb45ad52d2188f99`  
**Phase:** 1 — Exposure and design confirmation  
**STOP Gate 1:** **PASS**

---

## 1. Shared helper standard

Reuse Package 2 contracts in `backend/core/knowledge/signal_result_index_v1.py`:

| Helper | Role |
|---|---|
| `index_by_activation_key` | Frame-preserving index; duplicate keys fail closed |
| `group_by_signal_id` | Non-destructive family grouping |
| `family_fired_states` | Named family presence (at_risk > suboptimal) |
| `participating_activation_keys` | Frame audit companion |
| `confidence_by_signal_family` | Named max-confidence family reduction |
| `activation_key_or_empty` / `require_activation_key` | Key reconstruction / fail-closed |

Also reuse `layer_b_frame_routing_v1.select_frame_prose_asset` / `resolve_lead_frame_from_top_finding` for narrative lead routing.

**Rule:** no new clinical frame-priority policy. Preserve all frames or label honest family aggregation.

---

## 2. Gate 0 pressure set (exact)

From `HEALTHIQ_AI_V5_CONTROLLED_BETA_ARCHITECTURE_COHORT.md` §5:

| signal_id | frames |
|---|---:|
| signal_homocysteine_high | 3 |
| signal_mcv_high | 3 |
| signal_iron_low | 2 |
| signal_tpo_ab_high | 2 |
| signal_egfr_low | 2 |
| signal_alt_high | 4 |
| signal_ferritin_high | 3 |
| signal_creatinine_high | 2 |

**Total:** 8 families / **21** frames (3+3+2+2+2+4+3+2). Gate 0 text said “22”; arithmetic and this package’s synthetic fixture use **21**. All must be exercised in tests.

---

## 3. Per-surface design

### 3.1 Interpretation display publication

| Field | Value |
|---|---|
| File | `interpretation_display_layer_publish_v1.py` |
| Functions | `_signal_fire_states`, `_supporting_summary_for_phenotype`, `publish_interpretation_display_layer_v1` |
| Current keying | Bare `signal_id` dicts (`states[sid]`, `by_id[sid]`) |
| Frame-destructive | Last-wins overwrite on multi-frame families |
| Intentional family behaviour | Severity is family/phenotype-level; precedence already `at_risk` > else — not a medical frame pick |
| Pressure-set reach | Any fired multi-frame family in `signal_results` |
| Required change | Use `family_fired_states` for fired/state; `group_by_signal_id` for marker summary (union metrics across frames); emit bundle `participating_activation_keys` |
| Compatibility risk | Low — additive metadata; severity uses explicit family helper instead of last-wins |
| Test strategy | Two frames different states → at_risk wins; both activation_keys retained on bundle |

### 3.2 Domain score assembly

| Field | Value |
|---|---|
| File | `domain_score_assembler.py` |
| Functions | `_collect_signal_ids`, six Wave-1 `ConsumerDomainScoreV1` builders |
| Current keying | `active_signal_ids` dedup by `signal_id` only |
| Frame-destructive | Multi-frame families collapse to one id in `active_signal_ids` |
| Intentional family behaviour | Domain cards are family-level product surfaces; aggregation must be explicit |
| Pressure-set reach | egfr, iron_low, alt_high, tpo_ab_high, creatinine_high, ferritin adjacency |
| Required change | Keep `active_signal_ids`; add `active_activation_keys` via frame-safe collection under the same predicate |
| Compatibility risk | Additive DTO field; frontend type updated |
| Test strategy | Multi-frame iron/egfr/alt → both keys present; score not double-counted |

### 3.3 Narrative report compilation

| Field | Value |
|---|---|
| File | `narrative_report_compiler_v1.py` |
| Functions | `_resolve_lead_signal_id`, lead_frame assembly in `compile_narrative_report_v1` |
| Current keying | Graph path returns bare `signal_id`; blanks `activation_key` unless payload `top_findings` |
| Frame-destructive | Blanking/replacement of resolved frame identity on graph-only path |
| Intentional family behaviour | Layer-B `select_frame_prose_asset` already honest-fallback; keep it |
| Pressure-set reach | Lead hints ∩ multi-frame: homocysteine_high, mcv_high, tpo_ab_high (+ free_t3_low) |
| Required change | Resolve lead frame from the matching fired graph row (deterministic order); never blank a present `activation_key`; record lead-family participating keys in `compiler_meta` |
| Compatibility risk | Low — additive meta; payload path unchanged |
| Test strategy | Graph-only multi-frame lead hint retains activation_key; single-frame still works |

### 3.4 Intervention selection

| Field | Value |
|---|---|
| File | `intervention_selector_v1.py` |
| Functions | `_build_candidate`, dedup in `select_interventions_v1` |
| Current keying | `signal_refs: [signal_id]` only; dedup drops peer-frame attribution |
| Frame-destructive | Cross-frame attribution loss on dedup |
| Intentional family behaviour | Intervention templates are system/family-level; frame refs are provenance |
| Pressure-set reach | Families on interaction chains |
| Required change | Add `activation_key_refs`; on dedup **union** frame refs (and signal_refs) instead of dropping |
| Compatibility risk | Additive field; keep `signal_refs` |
| Test strategy | Two frames same system → merged candidate keeps both activation_key_refs |

### 3.5 Signal interaction builder

| Field | Value |
|---|---|
| File | `signal_interaction_builder.py` |
| Functions | `build_signal_interactions_v1`, `load_interaction_map_v1` |
| Current keying | Static map nodes/edges = `signal_id`; runtime already uses family helpers + panel-global `participating_activation_keys` |
| Frame-destructive | Panel-global keys do not show which frames fed which node/chain |
| Intentional family behaviour | **Yes** — interaction map YAML is clinical family-level policy |
| Pressure-set reach | Map nodes intersecting pressure set (e.g. alt_high, homocysteine_high, mcv_high) |
| Required change | **Do not re-key YAML.** Keep family node identity. Attach per-node and per-chain `participating_activation_keys`; keep `aggregation_scope: signal_family` |
| Compatibility risk | Additive keys on graph/summary; nodes remain string list |
| Test strategy | Two alt frames → node_frame_participation lists both; chain carries union |

---

## 4. STOP Gate 1 assessment

| Trigger | Result |
|---|---|
| Surface requires choosing one medical frame over another | **No** — no clinical priority invented |
| New clinical priority policy required | **No** |
| Intentional safe family aggregation that must not be re-keyed | **Surface 5 map YAML** — keep family-level; make runtime audit honest |
| Fix expands into provenance/WHY/prose/PSI/thresholds/frontend inference | **No** — additive identity metadata + mechanical keying only |
| Gate 0 pressure-set unreproducible | **No** — 8 families documented |
| Package 2 eligibility required for Package 1 tests | **No** — synthetic multi-frame fixtures |

**STOP Gate 1: PASS — proceed to implementation.**

---

## 5. Validation gate plan

Add `backend/scripts/validate_launch_path_frame_identity_gate.py`:

- Behavioural multi-frame fixture across the five surfaces.
- Asserts frame preservation / explicit aggregation metadata.
- Deliberately invalid fixture (duplicate activation_key index) must fail closed.
- Wire into `run_architecture_validation_gate.py`.

---

## 6. Explicit non-goals

- No YAML interaction-map re-keying  
- No provenance eligibility / reachability changes  
- No WHY / prose / PSI / Gemini / threshold changes  
- No beta-readiness or architecture-completion claim  
