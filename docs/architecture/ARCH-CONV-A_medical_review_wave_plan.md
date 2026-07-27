# ARCH-CONV-A — Medical Review Wave Plan

**Work ID:** `ARCH-CONV-A-STAGE0`
**Date (UTC):** 2026-07-27
**Purpose:** Design the fewest safe internal medical-review waves for the 36 non-pilot Package A targets. Design only — no medical review is conducted by this document.
**Runtime change:** NONE
**Source evidence:** `ARCH-CONV-A_active_why_target_inventory.md` (41/41 registry targets verified; 5 already `COMPILED_ACTIVE` pilot, 36 remaining)

---

## 1. Grouping method

Targets are grouped by shared biomarker evidence and common differential logic (organ-system/axis grouping), not by traffic share (unmeasured, per `ARCH-CONV_residual_runtime_inventory.md` §7.1) and not one-signal-per-wave. Groups are sized so no wave requires medical review capacity beyond what a single Gate 1 (GPT structured review) + Gate 2 (Anthony ratification) cycle can reasonably absorb, while every wave shares enough clinical context that reviewing it as one unit is more efficient and more consistent than reviewing targets individually.

Wave count: **7** (1 disposition wave + 6 organ-system waves), covering all 36 non-pilot targets exactly once.

### 1.1 Frame-count qualification (mandatory reading before any per-wave table below)

The 36 remaining targets are a verified **target** count (`ARCH-CONV-A_active_why_target_inventory.md`). The **frame** count for those 36 targets is **UNKNOWN UNTIL PHASE 1 IDENTITY AND SOURCE CLOSURE**. Three pilot signal_ids already resolve to 2–3 runtime frames each (`ARCH-CONV-A_identity_and_source_readiness.md` D-1), so a one-target/one-frame assumption for the remaining 36 must not be carried past provisional inventory planning. Every "frame count" cell in §2 below states a provisional target-count floor only, not a frame-count claim. No target enters Phase 2 (medical review) or Phase 3 (compilation) until STOP A has approved that target's row in the complete target-to-frame map (`ARCH-CONV-A_stop_gates_and_acceptance.md` STOP A, updated).

---

## 2. Wave sequence

### Wave 0 — Homocysteine elevation-context disposition

| Field | Content |
|---|---|
| product/medical outcome | Resolve DUAL-01/L-02: decide whether elevation-context deserves its own compiled frame or is suppressed/folded under existing compiled hcy frames via a Package B selector |
| signal families | signal_homocysteine_elevation_context (1 target) |
| frame count | UNKNOWN UNTIL PHASE 1 IDENTITY AND SOURCE CLOSURE — 1 target, frame count contingent on the elevation-context disposition itself (0 frames if suppressed, 1+ if ratified as distinct) |
| current legacy authority | `hcy_hypotheses_v1.yaml` (shared with signal_homocysteine_high, D-2) |
| canonical research readiness | NONE FOUND — no investigation_spec targets elevation-context specifically (inventory §3 row 1) |
| medical-review work required | Disposition-level: is elevation-context a distinct medically meaningful frame or already covered by the 3 existing homocysteine_high frames? |
| compile work required | Only if disposition is "distinct frame" — then full canonical research + compile as A5 |
| runtime integration work required | Selector/precedence design is Package B if coexistence is chosen; simple compiled-frame integration (Phase 3/4) if a distinct frame is ratified |
| intervention/report dependencies | Shares intervention citation space with signal_homocysteine_high |
| representative replay panel | Any input firing both signal_homocysteine_high and signal_homocysteine_elevation_context simultaneously |
| STOP gate | STOP B (medical ratification) — this wave's outcome gates whether L-02 (`ARCH-CONV-A_legacy_retirement_policy.md`) can proceed to runtime disconnection |
| wave completion evidence | Signed disposition record; if distinct frame chosen, standard Phase 3/4 evidence; if suppressed, a Package B handoff ticket |

Sequenced first because it is the sole dual-served target (highest medical risk per unit of work) and blocks a shared-file retirement that no other wave depends on resolving first.

### Wave 1 — Thyroid axis completion

| Field | Content |
|---|---|
| product/medical outcome | Full thyroid-axis WHY coverage (TSH, free T3, free T4, TPO-Ab, TgAb) under compiled authority, completing the axis the pilot partially covers (free_t3_low, tpo_ab_high already compiled) |
| signal families | signal_tsh_high, signal_tsh_low, signal_thyroid_tsh_context, signal_free_t3_high, signal_free_t4_high, signal_free_t4_low, signal_tgab_high (7 targets) |
| frame count | UNKNOWN UNTIL PHASE 1 IDENTITY AND SOURCE CLOSURE — 7 targets is a provisional target-count floor, not a frame-count assumption; no target-to-frame mapping is final until STOP A closes (see `ARCH-CONV-A_identity_and_source_readiness.md` D-1) |
| current legacy authority | 7 separate `*_hypotheses_v1.yaml` files, no shared-file case within this wave |
| canonical research readiness | 5 A3 (tsh_high, tsh_low, free_t3_high, free_t4_high, free_t4_low have matching specs); 1 A4 (thyroid_tsh_context — no confirmed spec, D-4); 1 A5 (tgab_high — no spec, D-5) |
| medical-review work required | Primary vs. secondary thyroid dysfunction differential; autoimmune (TPO-Ab/TgAb) vs. non-autoimmune framing consistency with already-compiled pilot frames |
| compile work required | 5 straightforward (spec exists); 2 require research/spec confirmation first (thyroid_tsh_context, tgab_high) |
| runtime integration work required | Standard Phase 3/4 per target; verify no cross-target dual with already-compiled free_t3_low/tpo_ab_high frames |
| intervention/report dependencies | Thyroid intervention library entries; consumer/clinician thyroid panel narrative |
| representative replay panel | Primary hypothyroid (TSH high + free T4 low), primary hyperthyroid (TSH low + free T4/T3 high), autoimmune-only (TPO-Ab/TgAb high, euthyroid) |
| STOP gate | STOP B per this wave |
| wave completion evidence | 7/7 targets ratified or explicitly deferred; thyroid-axis consumer/clinician alignment test passes |

Sequenced second: highest-surfacing endocrine domain, already has proven compiled precedent (2 of 5 pilot signals are thyroid), majority spec-ready.

### Wave 2 — Lipid / cardiometabolic panel

| Field | Content |
|---|---|
| product/medical outcome | Compiled WHY for the routine lipid panel and its cardiovascular-risk context signals |
| signal families | signal_ldl_cholesterol_high, signal_hdl_cholesterol_low, signal_triglycerides_high, signal_total_cholesterol_high, signal_apoa1_cardio_risk, signal_lipid_transport_dysfunction (6 targets) |
| frame count | UNKNOWN UNTIL PHASE 1 IDENTITY AND SOURCE CLOSURE — 6 targets is a provisional target-count floor, not a frame-count assumption |
| current legacy authority | 6 separate files |
| canonical research readiness | 3 A3 (ldl, hdl, triglycerides); 1 A5 (total_cholesterol_high — no spec, superseded conceptually by LDL/HDL but registered separately); 1 A5 (apoa1_cardio_risk); 1 A4 (lipid_transport_dysfunction — composite signal, no confirmed 1:1 spec) |
| medical-review work required | Whether total_cholesterol_high should remain an independent frame or be explicitly subsumed by LDL/HDL-specific frames (identity/scope question, resolved in this wave's Gate 1, not deferred) |
| compile work required | 3 straightforward; 3 require spec authoring/confirmation |
| runtime integration work required | Standard Phase 3/4; verify total_cholesterol_high does not create a new composite-vs-specific dual analogous to DUAL-01 |
| intervention/report dependencies | Lipid/cardiovascular intervention library entries |
| representative replay panel | Isolated LDL elevation, isolated HDL deficiency, combined dyslipidaemia, elevated triglycerides with normal LDL/HDL |
| STOP gate | STOP B; additional attention to whether total_cholesterol_high's disposition creates a new DUAL-class finding requiring Package B involvement |
| wave completion evidence | 6/6 ratified/deferred; no new unresolved dual introduced |

### Wave 3 — Renal function panel

| Field | Content |
|---|---|
| product/medical outcome | Compiled WHY for renal-clearance markers |
| signal families | signal_creatinine_high, signal_urea_high, signal_urate_high (3 targets) |
| frame count | UNKNOWN UNTIL PHASE 1 IDENTITY AND SOURCE CLOSURE — 3 targets is a provisional target-count floor, not a frame-count assumption |
| current legacy authority | 3 separate files |
| canonical research readiness | All 3 A3 — specs exist for all (urate maps to `inv_uric_acid_high_metabolic.yaml`, a naming variant, confirm during Phase 1) |
| medical-review work required | Shared renal-clearance differential context (already touched by the compiled hcy renal_clearance_reduction frame — confirm no unintended overlap) |
| compile work required | 3, all spec-ready |
| runtime integration work required | Standard Phase 3/4; explicit cross-check against the already-compiled `signal_homocysteine_high::inv_homocysteine_high_renal_clearance_reduction` frame for narrative consistency (not a dual — different signal_ids — but same underlying renal mechanism, consumer narrative should not contradict) |
| intervention/report dependencies | Renal intervention library entries |
| representative replay panel | Isolated creatinine elevation, isolated urea elevation, combined renal-pattern elevation, isolated urate elevation (gout-context) |
| STOP gate | STOP B |
| wave completion evidence | 3/3 ratified; renal narrative consistency check against existing hcy renal frame passes |

Smallest wave — sequenced third to bank an easy, fully spec-ready completion before the two research-heavy waves (4, 5).

### Wave 4 — Hepatic / biliary panel

| Field | Content |
|---|---|
| product/medical outcome | Compiled WHY for liver-function markers, resolving the bilirubin identity duplication first |
| signal families | signal_hepatic_alt_context, signal_ggt_high, signal_alp_high, signal_alp_low, signal_bilirubin_high, signal_hyperbilirubinemia, signal_hepatic_metabolic_stress (7 targets) |
| frame count | UNKNOWN UNTIL PHASE 1 IDENTITY AND SOURCE CLOSURE — target count is 6 or 7 depending on D-3 (bilirubin_high / hyperbilirubinemia) resolution, and frame count per surviving target is separately unresolved until STOP A closes; must be settled before this wave's Gate 1 review, per `ARCH-CONV-A_identity_and_source_readiness.md` D-3 |
| current legacy authority | 7 separate files (or 6 effective identities if D-3 resolves to a merge) |
| canonical research readiness | 2 A3 (ggt_high, alp_high); 1 A4 (hepatic_alt_context — direction mismatch with candidate spec, D-4); 4 A5 (alp_low, bilirubin_high, hyperbilirubinemia, hepatic_metabolic_stress) |
| medical-review work required | D-3 identity resolution (before Gate 1); hepatocellular vs. cholestatic vs. haemolytic bilirubin differential if both bilirubin targets are retained as distinct |
| compile work required | 2 straightforward; remainder require spec authoring/confirmation, highest research burden of the mid-sized waves |
| runtime integration work required | Standard Phase 3/4 |
| intervention/report dependencies | Hepatic intervention library entries |
| representative replay panel | Isolated ALT elevation (hepatocellular), isolated GGT/ALP elevation (cholestatic/biliary), isolated bilirubin elevation, combined hepatic panel |
| STOP gate | STOP A (identity, for D-3) must close before this wave's STOP B |
| wave completion evidence | D-3 resolved; 6 or 7 targets ratified/deferred |

### Wave 5 — Iron / haematology panel

| Field | Content |
|---|---|
| product/medical outcome | Compiled WHY for iron-status and red-cell markers, complementing the already-compiled MCV frames |
| signal families | signal_ferritin_low, signal_ferritin_high, signal_hemoglobin_low, signal_iron_deficiency_context, signal_iron_overload_context, signal_oxygen_transport_capacity, signal_transferrin_high, signal_transferrin_low (8 targets) |
| frame count | UNKNOWN UNTIL PHASE 1 IDENTITY AND SOURCE CLOSURE — 8 targets is a provisional target-count floor, not a frame-count assumption |
| current legacy authority | 8 separate files |
| canonical research readiness | 2 A3 (ferritin_high, hemoglobin_low); 3 A4 (iron_overload_context, oxygen_transport_capacity, ferritin_low — candidate specs unconfirmed); 3 A5 (iron_deficiency_context, transferrin_high, transferrin_low — no spec) |
| medical-review work required | Highest research burden of any wave (largest, most A4/A5-heavy); iron-deficiency vs. overload differential must align narratively with the already-compiled MCV macrocytosis/megaloblastic frames (shared haematology domain) |
| compile work required | 2 straightforward; 6 require spec authoring/confirmation |
| runtime integration work required | Standard Phase 3/4; consumer/clinician narrative cross-check against compiled MCV frames for consistency (anaemia-context overlap) |
| intervention/report dependencies | Iron/haematology intervention library entries |
| representative replay panel | Iron-deficiency anaemia (low ferritin + low Hgb + high transferrin), anaemia of chronic disease pattern, iron overload (high ferritin, context-dependent), isolated transferrin abnormality |
| STOP gate | STOP B; largest single medical-review effort in the programme — flagged explicitly as the wave most likely to test medical-review capacity limits |
| wave completion evidence | 8/8 ratified/deferred; MCV-frame narrative consistency check passes |

Sequenced fifth (not first, despite size) because it has the lowest spec-readiness ratio (2/8 A3) — the programme banks faster, lower-research waves first per the prioritisation rule in §3.

### Wave 6 — Metabolic / systemic residual

| Field | Content |
|---|---|
| product/medical outcome | Compiled WHY for remaining metabolic/systemic context signals not covered by the domain waves above |
| signal families | signal_hba1c_high, signal_insulin_resistance, signal_systemic_inflammation, signal_hypercortisolism (4 targets) |
| frame count | UNKNOWN UNTIL PHASE 1 IDENTITY AND SOURCE CLOSURE — 4 targets is a provisional target-count floor, not a frame-count assumption |
| current legacy authority | 4 separate files |
| canonical research readiness | 1 A3 (hba1c_high); 1 A4 (systemic_inflammation — composite, unconfirmed 1:1 spec); 2 A5 (insulin_resistance, hypercortisolism — no spec) |
| medical-review work required | These four share no single organ axis — grouped here only because each is a lower-shared-structure residual context signal, not because they share differential logic. This is the one wave where the grouping is by "remaining, not otherwise groupable" rather than shared medical structure; flagged explicitly rather than forced into an artificial family. |
| compile work required | 1 straightforward; 3 require spec authoring |
| runtime integration work required | Standard Phase 3/4 |
| intervention/report dependencies | Metabolic/endocrine intervention library entries |
| representative replay panel | Isolated HbA1c elevation, insulin-resistance context with normal HbA1c, systemic inflammation context, hypercortisolism context |
| STOP gate | STOP B |
| wave completion evidence | 4/4 ratified/deferred |

Sequenced last: no shared-family retirement benefit, lowest spec-readiness ratio alongside Wave 5, and no dual-authority urgency.

---

## 3. Prioritisation rationale (matches source task ordering, adapted to evidence)

1. Wave 0 first — the only active dual-served target (highest medical risk per unit of work), not because of unmeasured traffic share.
2. Wave 1 (thyroid) second — highest-surfacing domain with proven compiled precedent already in the pilot cohort, and majority spec-ready (5/7 A3).
3. Waves 2–3 (lipid, renal) next — majority or fully spec-ready, retiring straightforward legacy paths quickly and building medical-review-process momentum before the two research-heavy waves.
4. Waves 4–5 (hepatic, iron/haematology) — highest research burden, sequenced after the programme has demonstrated wave-cycle throughput on faster waves; Wave 4 first because it has a smaller, boundable identity-defect (D-3) to close before proceeding, whereas Wave 5 has no comparable blocker but the largest raw research volume.
5. Wave 6 (metabolic residual) last — lowest shared structure, no dual-authority or shared-file urgency.

This does not use production traffic share as an ordering mechanism (unmeasured, per source evidence) — ordering uses medical risk (dual authority), spec-readiness ratio, and domain precedent only.

---

## 4. Gate 1 / Gate 2 application per wave

Per source task §7 (previously adopted dual-gate model):

- **Batched review:** within a wave, canonical research entries sharing the same organ-system differential (e.g. all 5 thyroid A3 targets) may be reviewed together in a single Gate 1 session, since they share evaluator/reviewer context.
- **Separate frame-level ratification required:** any target with multiple candidate frames (none currently identified outside the already-compiled pilot cohort, but Wave 1/4/5 must re-check during Phase 1 per D-1) requires per-frame Gate 2 ratification, not one blanket wave approval.
- **No copy-forward of legacy wording or hypotheses without independent Gate 1 review** — this applies to every A3/A4/A5 target; a matching investigation_spec existing does not exempt it from Gate 1, and legacy YAML wording is never treated as pre-approved evidence (CLAUDE.md §12: "legacy wording... must not be treated as current medical authority").
- **Approval / rejection / narrowing / deferment:** each target's Gate 2 outcome is one of these four; a rejected frame becomes structurally inactive via the same `frame_runtime_authority_v1` mechanism already proven for the pilot's rejected hcy_metabolic frame (`ARCH-CONV_dual_authority_findings.md` DUAL-04).
- **Insufficient evidence:** where a target is A5 (no spec) and fresh canonical research does not resolve to a clinically defensible causal WHY, the disposition is "context-only, no causal WHY compiled" — the signal continues to fire/rank under `signal_library` but produces no compiled or legacy causal narrative, consistent with outcome 3 (no fail-open fallback) rather than falling back to `why_engine_fallback_v1` (Package B's L-04 closure).

---

## 5. Medical evidence gaps (explicit, do not proceed silently)

1. 11 A5 targets have no canonical investigation_spec at all — Knowledge Bus research intake (outside Package A's own authoring scope, but a precondition input) must produce these before the relevant wave's Phase 2 can begin. This is a scheduling dependency, not a Package A scope item.
2. 8 A4 targets have an unconfirmed candidate spec — Phase 1 must explicitly confirm or reject the match; an unconfirmed match must not silently proceed into Gate 1 review as if confirmed.
3. Wave sizing (7 waves, 36 targets) assumes roughly comparable per-target review effort; actual Gate 1 review time for research-heavy waves (4, 5) may run longer than spec-ready waves (2, 3) — this is a capacity/scheduling risk, not a package-structure risk, and does not change the wave grouping.
