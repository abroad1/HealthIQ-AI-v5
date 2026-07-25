# HealthIQ AI v5 — Convergence Viability Assessment

**Work ID:** `ARCH-CONV-GATE0`  
**Branch:** `feature/arch-conv-gate0-cohort-viability`  
**Baseline HEAD:** `d798beab9b2bb7dcad9b48ed0f0a4f0153be8948`  
**Status:** COMPLETE for Gate 0 analysis  
**Decision:** **REDESIGN**

---

## 1. Executive decision

```text
REDESIGN
```

v5 remains salvageable under a bounded convergence programme, but a pure **GO** is not permitted because medical-review ownership and capacity for the WHY pilot are **not evidenced** (Gate 0 acceptance criterion and GO precondition fail without invention).

The package sequence must be revised to insert an explicit human medical-review confirmation gate before Package 3B, while allowing Packages 1 and 2 to proceed on architecture tracks.

This is **not** V6: kill criteria for cohort isolation, lineage recoverability, estate-wide disruption, and executable WHY architecture pilot are **not** met.

---

## 2. Identity exposure findings

All five residual surfaces are **live** on the analysis path and remain **`signal_id`-keyed** for core join/rank/select behaviour. Frame collapse is **mechanically possible**. Concurrent production multi-frame exposure across all five surfaces is **UNVERIFIABLE as a product traffic fact**; mechanism defect is verified.

| Surface | File / functions | Current keying | Frame collapse possible? | Active multi-frame families that can reach it | Launch-critical? | Fix vs harden |
|---|---|---|---|---|---|---|
| IDL publish | `interpretation_display_layer_publish_v1.py` — `_signal_fire_states`, `_supporting_summary_for_phenotype`, `publish_interpretation_display_layer_v1` | `signal_id` dict keys | Yes | Any multi-frame family present in insight graph signal rows (e.g. §5 pressure set) | Yes — orchestrator live | Full behaviour fix in Package 1 |
| Domain scores | `domain_score_assembler.py` — `_collect_signal_ids`, Wave 1 assemblers | `signal_id` only | Yes | Wave 1 multi-frame families (egfr, iron_low, alt_high, etc.) | Yes — Wave 1 cards | Full behaviour fix in Package 1 |
| Narrative compiler | `narrative_report_compiler_v1.py` — `_fired_suboptimal_signal_ids`, `_resolve_lead_signal_id`, `compile_narrative_report_v1` | Lead by `signal_id`; `activation_key` only when `top_findings` present | Yes when payload/lead path is family-keyed | Lead hints ∩ multi-frame: `homocysteine_high`, `mcv_high`, `tpo_ab_high`; also `free_t3_low` | Yes | Full behaviour fix + regression for lead path |
| Intervention selector | `intervention_selector_v1.py` — `_signal_chain_context`, `_build_candidate`, `select_interventions_v1` | `signal_id` in `signal_refs` | Yes | Families flowing through interaction summary | Yes — insight graph path | Full behaviour fix |
| Interaction builder | `signal_interaction_builder.py` — node load + `build_signal_interactions_v1` | Nodes/confidence by `signal_id`; `participating_activation_keys` metadata only | Yes (family aggregation helper collapses frames) | All multi-frame families entering interaction map | Yes | Full behaviour fix of node/confidence identity; intentional family aggregation must become explicit/non-destructive |

**Exposed identity surfaces count:** **5 / 5** named surfaces have verified live callers and collapse mechanics.

**Package 1 justification:** full behaviour fix package is justified; cosmetic-only hardening is insufficient for interaction-builder core logic.

---

## 3. Provenance-blocked runtime findings

### Launch-critical BLOCKED cohort

| Fact | Value |
|---|---|
| Inventory BLOCKED rows | **16** |
| `pkg_kb47_*` on disk | **20** (all loadable) |
| Currently reachable (can load / can fire when biomarkers present) | **20 / 20** — `SignalRegistry` has no provenance suppression |
| Can rank / appear in user-facing compilers | **Yes mechanistically** if fired — same as other signals |
| Appears in representative/golden **fixtures** by package name | **No** fixture mentions found |
| Appears in golden **outputs** | **UNVERIFIABLE** without re-run |
| Canonical research source | **Yes** — all 20 `source_spec_id` values present in `Batch_2_Pass_3.json` |
| Explicit lineage recoverable | **Yes** — EXTRACT_AND_ATTACH feasible; standalone `inv_*.yaml` absent today |
| Recommended action (Wave 1 overlap: thyroid + egfr) | **EXTRACT_AND_ATTACH** |
| Recommended action (androgen panel) | **EXTRACT_AND_ATTACH** + keep **EXCLUDE_FROM_BETA_COHORT** until medical/context gates close |
| Recommended action (CK / eosinophils) | **EXTRACT_AND_ATTACH** or **EXCLUDE_FROM_BETA_COHORT** (product choice); **DEFER** from Wave 1 beta surface |
| Do not | Remove packages in Gate 0 |

### Product impact if suppressed (MAKE_NON_REACHABLE)

| Slice | Product impact | Medical impact |
|---|---|---|
| Thyroid free_t3/t4 kb47 | Wave 1 thyroid card/signal loss for those markers | High — thyroid is a launch domain |
| egfr_low kb47 | Wave 1 kidney filtration signal loss | High — kidney domain |
| Androgen panel | Limited Wave 1 impact (not Wave 1 domains); removes androgen context signals | Medium — already context-blocked for promotion |
| CK / eosinophils | Limited Wave 1 card impact | Medium/low for controlled-beta card claim |

**Suppression is not required for salvage** if lineage attach is executed for INCLUDE rows. Suppression remains a fallback for non-Wave-1 rows if extraction capacity is exceeded.

---

## 4. Canonical lineage recoverability

| Cohort | Recoverable now? | Kill-criterion risk |
|---|---|---|
| kb47 launch-critical (20) | **Yes** — batch Pass 3 JSON | Low if Package 2 scoped to attach |
| Wave 1 INCLUDE core | Mostly package + research artefacts; kb47 subset as above | Low |
| Estate `batch_json_blocked_pending_spec_extraction` (**147**) | Not all required for controlled-beta architecture cohort | Do **not** treat as Gate 0 kill if cohort stays bounded |

**Proposed lineage failure threshold (for human approval):**

> If more than **0** of the Wave 1-overlapping INCLUDE kb47 frames (thyroid free_t3/t4 + egfr ×2 = **6** frames) cannot be tied to genuine Pass 3 / inv authority without invention, stop and reconsider V6 for the provenance track.  
> If more than **25%** of the broader launch-critical kb47 set (**>5 of 20**) cannot be recovered, stop Package 2 expansion and force product choose EXCLUDE_FROM_BETA_COHORT vs V6.

---

## 5. Medical-review viability

| Question | Finding |
|---|---|
| Medical-review owner | **UNRESOLVED** — no named owner/FTE in required Gate 0 inputs or BUILD register |
| Review inputs | Definable from precedents (hypothesis artefacts, frames, evidence limits, emission samples) |
| Review output format | Precedents: `BATCH2-MEDREVIEW-1_*`, `MED-REV-1_*`, `MED-REV-2_*` |
| Expected decision route | Engineering Package 3A → medical sign-off → Package 3B activation |
| Unresolved dependencies | Owner, capacity, calendar commitment |
| Pilot completable in programme window? | **UNVERIFIABLE** without human capacity confirmation |

**STOP condition 7 (prompt):** medical-review ownership cannot be established → **escalated here**; ownership was not invented.

**Gate 0 plan STOP (“no credible medical-review route”):** historical MR process artefacts exist, but **capacity/route commitment for this pilot is not credible until a human owner confirms**. This blocks **GO**, supports **REDESIGN**, does not by itself prove V6.

---

## 6. Proposed programme ceilings (for human approval)

| Ceiling | Proposed value | Notes |
|---|---|---|
| Maximum planned architecture packages | **3** (Package 1, Package 2, Package 3A+3B coordinated) | Matches planning paper |
| Maximum unplanned follow-on / mandatory correction packages | **1** | Already fixed — do not change |
| Maximum unauthorised material scope growth per package | **25%** | Already fixed — do not change |
| Maximum programme duration | **8 calendar weeks** from Package 1 start through final architecture audit | PROPOSED |
| Maximum engineering effort | **6 engineer-weeks** total across Packages 1–3A (suggest split: P1=2.5, P2=2, P3A=1.5) | PROPOSED; excludes idle wait on MR |
| Maximum medical-review effort | **UNRESOLVED** — propose placeholder **5 signal reviews + 1 retirement confirmation** only after owner named | Cannot invent FTE |
| Lineage failure threshold | As §4 | PROPOSED |

---

## 7. Kill-criteria assessment

| Criterion | Met now? | Assessment |
|---|---|---|
| 11.1 Cohort-isolation failure | **No** | Cohort isolatable: Wave 1 + kb47 launch-critical + bounded WHY pilot |
| 11.2 Canonical-lineage failure | **No** | kb47 lineage recoverable at material scale for the intended cohort |
| 11.3 Authority-retirement failure | **N/A yet** | Deferred to Package 3B proof |
| 11.4 Cross-layer duplication | **Open residual** | Five identity surfaces are the known residual; not already unfixable |
| 11.5 Scope-growth ceiling | **No breach** | Fixed ceilings retained |
| 11.6 Time/cost ceiling | **Not set until human approves §6** | Proposed values above |
| 11.7 Medical-review viability failure | **At risk / unresolved** | Blocks GO; triggers redesign of Package 3B entry conditions |
| 11.8 Independent-assurance failure | **No** | Prior CC vs Cursor variance is refinement-level, not programme-killing |

---

## 8. Revised sequence (REDESIGN)

```text
Gate 0 (this package) — cohort + viability
→ Package 1 — activation-frame identity closure (5 surfaces)
→ Gate 1 — independent audit
→ Package 2 — provenance / reachability honesty for launch-critical INCLUDE (+ optional DEFER attaches)
→ Gate 2 — independent audit
→ Gate 2.5 — HUMAN medical-review owner + capacity confirmation for WHY pilot
      (hard gate: no Package 3B without named owner and committed capacity)
→ Package 3A — WHY architecture machinery for pilot only
→ Package 3B — medical pilot activation + vitamin_d legacy retirement proof
→ Final architecture audit
```

If Gate 2.5 fails: keep Packages 1–2 gains; reduce Package 3B to vitamin_d retirement-only architecture proof **or** freeze WHY migration and reassess V6 for the medical-intelligence track only — without undoing identity/provenance salvage.

**Do not author Package 1 implementation prompts in this package.**

---

## 9. GO precondition checklist

| GO precondition | Result |
|---|---|
| Launch-critical cohort isolatable | **PASS** |
| Identity scope bounded | **PASS** (5 surfaces) |
| Provenance lineage or safe exclusion feasible | **PASS** |
| WHY pilot bounded | **PASS** (5 signals / 10 frames) |
| Medical-review route credible | **FAIL** (owner/capacity unresolved) |
| Programme ceilings settable | **PASS** (proposed; need human approval) |

Hence **REDESIGN**, not GO, not V6.

---

## 10. Quantitative summary

| Item | Count |
|---|---:|
| Proposed beta signal families (architecture INCLUDE core) | predicate-bounded ≈15–25 |
| Activation frames estate-wide | 197 |
| Active multi-frame families estate-wide | 51 |
| Multi-frame in Package 1 pressure set | 8 |
| Exposed identity surfaces | 5 |
| Blocked launch-critical inventory rows | 16 |
| Blocked/kb47 packages currently reachable | 20 |
| Packages requiring lineage extraction (kb47) | 20 |
| Packages recommended for beta-surface suppression | 0 mandatory; androgen/CK/eos may be excluded from beta claim |
| WHY pilot signals / frames | 5 / 10 |
| Medical reviews required (new + confirmation) | 4 + 1 |

---

## 11. Explicit non-claims

- No controlled-beta readiness declaration.
- No runtime, schema, test, or medical-content changes in this package.
- No Package 1 implementation prompt authored.
- No invented medical-review owner or capacity commitment.
